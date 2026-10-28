"""Sinh quảng cáo bằng API backend CopyPro chạy ở máy (Bước 11, T3.3).

Câu lệnh được ghép lại đúng từng ký tự như buildPrompt() của giao diện CopyPro
(frontend/src/app/generate/Generator.tsx: CONTENT_LENGTH_LABELS, LENGTH_TOKEN_LIMITS,
getCopyTypeFormatPrompt). Chỉ chép ba loại bài dùng trong thực nghiệm: description, social, landing.

Mỗi bài sinh ra lưu thành data/quang_cao/<ma_qc>.json kèm payload đã gửi, câu lệnh ghép, câu lệnh
CopyPro lưu lại và phiên bản CopyPro, để chạy lại và đối chiếu được. Token không bao giờ ghi vào tệp.
Không ghi đè tệp đã có. Bài do CopyPro trả bằng bài mẫu (fallback, không phải LLM) hoặc mã HTTP khác
200 thì ném LoiCopyPro và không ghi tệp.

Chạy (cần CopyPro đang chạy ở máy; địa chỉ và tài khoản đọc từ COPYPRO_API, COPYPRO_EMAIL,
COPYPRO_MAT_KHAU):
    python -m kiemchung.sinh_quang_cao --mau dt-apple-iphone17 --ten "iPhone 17" --loai social \\
        --che-do ten --mo-hinh gemini-3-6-flash --lan 1
"""
import argparse
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

GOC = Path(__file__).resolve().parents[2]
THU_MUC_RA = GOC / "data" / "quang_cao"
DIA_CHI_MAC_DINH = "http://localhost:4000/api"
# Tài khoản thử do `yarn seed` của CopyPro tạo trên CSDL ở máy, không phải tài khoản thật.
EMAIL_MAC_DINH = "customer@copypro.vn"
MAT_KHAU_MAC_DINH = "customer123"
THOI_GIAN_CHO = 30
THOI_GIAN_CHO_TAO_BAI = 240

# Chép từ Generator.tsx.
NHAN_DO_DAI = {"short": "ngắn gọn", "medium": "vừa đủ chi tiết", "long": "dài và giàu chi tiết"}
GIOI_HAN_TOKEN = {"short": 900, "medium": 1800, "long": 3200}

# Thiết lập cố định theo T3.3.
NGANH = "technology"
GIONG = "professional"
DO_DAI = "medium"
SO_PHIEN_BAN = 1
# Backend CopyPro tự đặt khi gọi LLM, không nhận từ giao diện; ghi lại để biết điều kiện sinh bài.
THAM_SO_BACKEND = {"temperature": 0.75, "top_p": 0.9}

LOAI_BAI = ("description", "social", "landing")
CHE_DO = ("ten", "ten_thong_so")
MA_LLM = {"gemini-3-6-flash": "gemini", "groq-gpt-oss-120b": "gptoss"}  # mã khác giữ nguyên mã
# Tên mô hình gửi sang nhà cung cấp (GEMINI_MODEL_MAP, GROQ_MODEL_MAP trong aiService.js của CopyPro).
# CopyPro chỉ trả mã của nó, nên ghi tên này để còn biết đúng mô hình nếu sau này mô hình bị ngừng (T9.1).
MO_HINH_NHA_CUNG_CAP = {"gemini-3-6-flash": "gemini-3.6-flash", "groq-gpt-oss-120b": "openai/gpt-oss-120b"}
NHOM_LUA_CHON = ("industries", "copyTypes", "tones")


class LoiCopyPro(Exception):
    """CopyPro không trả bài do LLM: mã HTTP khác 200, bài mẫu fallback, phản hồi thiếu trường."""


@dataclass
class PhienDangNhap:
    dia_chi: str
    token: str = field(repr=False)
    ten_lua_chon: dict  # {"industries": {slug: tên}, "copyTypes": {...}, "tones": {...}}


def so_js(x):
    """In số như JavaScript: 0.7 -> '0.7', 1.0 -> '1' (Python in '1.0')."""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


def goi_api(phuong_thuc, url, token=None, du_lieu=None, timeout=THOI_GIAN_CHO):
    """Gọi API CopyPro, trả (mã HTTP, JSON đã giải mã thành dict). Chỗ duy nhất đụng mạng; test thay hàm này.
    Mã khác 2xx vẫn trả về bình thường để nơi gọi quyết định; không kết nối được thì ném LoiCopyPro."""
    dau = {"Accept": "application/json"}
    if token:
        dau["Authorization"] = f"Bearer {token}"
    than = None
    if du_lieu is not None:
        than = json.dumps(du_lieu, ensure_ascii=False).encode("utf-8")
        dau["Content-Type"] = "application/json; charset=utf-8"
    yeu_cau = urllib.request.Request(url, data=than, headers=dau, method=phuong_thuc)
    try:
        with urllib.request.urlopen(yeu_cau, timeout=timeout) as tra_loi:
            ma, tho = tra_loi.status, tra_loi.read()
    except urllib.error.HTTPError as e:
        ma, tho = e.code, e.read()
    except OSError as e:  # URLError, hết giờ, mất kết nối
        raise LoiCopyPro(f"không gọi được {url}: {e}") from e
    chu = tho.decode("utf-8", "replace")
    try:
        nd = json.loads(chu)
    except ValueError:
        nd = None
    return ma, nd if isinstance(nd, dict) else {"message": chu[:200]}


def _data(nd):
    d = nd.get("data")
    return d if isinstance(d, dict) else {}


def _loi_http(viec, ma, nd):
    return LoiCopyPro(f"{viec}: mã HTTP {ma}: {nd.get('message')}")


def dang_nhap(dia_chi, email, mat_khau):
    """Lấy token từ POST /auth/user/login. Cookie đăng nhập có cờ Secure nên không dùng được qua http;
    gửi token bằng header Authorization: Bearer."""
    ma, nd = goi_api("POST", f"{dia_chi}/auth/user/login", du_lieu={"email": email, "password": mat_khau})
    if ma != 200:
        raise _loi_http("đăng nhập", ma, nd)
    token = _data(nd).get("token")
    if not token:
        raise LoiCopyPro("đăng nhập: phản hồi không có data.token")
    return token


def lay_lua_chon(dia_chi, token):
    """Bảng tên hiển thị {nhóm: {slug: name}} từ GET /generate-options."""
    ma, nd = goi_api("GET", f"{dia_chi}/generate-options", token=token)
    if ma != 200:
        raise _loi_http("lấy generate-options", ma, nd)
    data = _data(nd)
    return {nhom: {m["slug"]: m["name"] for m in data.get(nhom) or []} for nhom in NHOM_LUA_CHON}


def mo_phien(dia_chi=None, email=None, mat_khau=None):
    """Đăng nhập và lấy bảng tên lựa chọn. Bỏ trống thì lấy từ biến môi trường, rồi tới giá trị mặc định."""
    dia_chi = (dia_chi or os.environ.get("COPYPRO_API") or DIA_CHI_MAC_DINH).rstrip("/")
    email = email or os.environ.get("COPYPRO_EMAIL") or EMAIL_MAC_DINH
    mat_khau = mat_khau or os.environ.get("COPYPRO_MAT_KHAU") or MAT_KHAU_MAC_DINH
    token = dang_nhap(dia_chi, email, mat_khau)
    return PhienDangNhap(dia_chi, token, lay_lua_chon(dia_chi, token))


def dong_dinh_dang(loai_bai, do_dai):
    """Các dòng 'Format riêng theo loại nội dung', chép từ getCopyTypeFormatPrompt (Generator.tsx).
    Dòng phụ thuộc độ dài trả '' ở chỗ JS dùng chuỗi rỗng rồi .filter(Boolean)."""
    if do_dai not in NHAN_DO_DAI:
        raise ValueError(f"độ dài không hợp lệ: {do_dai}")
    if loai_bai == "description":
        dong = [
            "Mô tả ngắn: đoạn mở đầu giới thiệu sản phẩm/dịch vụ.",
            "Lợi ích chính: 2-3 bullet.",
            "Đặc điểm nổi bật: 2-3 bullet.",
            "Lời kêu gọi hành động: lời kêu gọi mua, đăng ký hoặc liên hệ.",
            "Không dùng format email, SEO metadata hoặc caption mạng xã hội.",
        ]
    elif loai_bai == "social":
        dong = [
            "Hook: câu mở đầu kéo chú ý.",
            "Caption: nội dung chính dễ đọc trên mạng xã hội.",
            "Lời kêu gọi hành động: hành động mong muốn.",
            "Hashtags: 3-6 hashtag liên quan.",
            "Không thêm Subject, Preview text, SEO title hoặc Meta description.",
        ]
    elif loai_bai == "landing":
        dong = [
            "Hero headline: tiêu đề chính của hero section.",
            "Subheadline: câu phụ làm rõ giá trị.",
            "Pain point: vấn đề khách hàng đang gặp." if do_dai == "long" else "",
            "Lợi ích chính: 3 bullet.",
            "Bằng chứng: review, số liệu, cam kết hoặc social proof.",
            "Offer: ưu đãi hoặc lý do hành động ngay." if do_dai != "short" else "",
            "Lời kêu gọi hành động: nút hoặc lời kêu gọi hành động chính.",
            "Không viết thành email, SEO metadata hoặc một caption social ngắn.",
        ]
    else:
        raise ValueError(f"loại bài chưa chép từ Generator.tsx: {loai_bai}")
    return "\n".join(d for d in dong if d)


def ghep_cau_lenh(ten_nganh, ten_loai, ten_giong, ten_san_pham, loai_bai, tu_khoa="", doi_tuong="",
                  bo_sung="", do_dai="medium", so_phien_ban=1, max_output_tokens=None, nhiet_do=0.7):
    """Câu lệnh gửi CopyPro, chép từ buildPrompt() của Generator.tsx. ten_*: tên hiển thị (name) của
    ngành, loại bài, giọng; loai_bai: slug loại bài (chọn dòng định dạng). Chuỗi rỗng là chưa nhập."""
    if do_dai not in NHAN_DO_DAI:
        raise ValueError(f"độ dài không hợp lệ: {do_dai}")
    if max_output_tokens is None:
        max_output_tokens = GIOI_HAN_TOKEN[do_dai]
    dong = [
        f"Bạn là chuyên gia copywriting cho ngành {ten_nganh}.",
        f"Hãy viết {ten_loai} với tone {ten_giong}.",
        f"Sản phẩm/dịch vụ: {ten_san_pham}." if ten_san_pham
        else "Sản phẩm/dịch vụ: chưa được cung cấp, hãy tự giả định hợp lý theo ngành đã chọn.",
        f"Từ khóa chính: {tu_khoa}." if tu_khoa
        else "Từ khóa chính: chưa được cung cấp, ưu tiên lợi ích rõ ràng và lời kêu gọi hành động mạnh.",
        f"Đối tượng mục tiêu: {doi_tuong}." if doi_tuong
        else "Đối tượng mục tiêu: khách hàng tiềm năng phổ thông.",
        f"Thông tin bổ sung: {bo_sung}." if bo_sung else "",
        f"Độ dài mong muốn: {NHAN_DO_DAI[do_dai]}.",
        f"Giới hạn output tối đa: {max_output_tokens} tokens.",
        f"Tạo đúng {so_phien_ban} phiên bản riêng biệt.",
        "Định dạng bắt buộc:",
        *[f"Phiên bản {i + 1}: ..." for i in range(so_phien_ban)],
        "Mỗi phiên bản phải tự đứng độc lập, không gom chung thành một đoạn lớn.",
        "Format riêng theo loại nội dung:",
        dong_dinh_dang(loai_bai, do_dai),
        "Dùng tiếng Việt tự nhiên, đầy đủ dấu, có lời kêu gọi hành động rõ ràng.",
        f"Temperature tham khảo: {so_js(nhiet_do)}.",
    ]
    return "\n".join(d for d in dong if d)


def ma_quang_cao(ma_mau, mo_hinh, loai_bai, che_do, lan):
    """qc-<ma_mau>-<llm>-<loai_bai>-<che_do>-<lan>."""
    return f"qc-{ma_mau}-{MA_LLM.get(mo_hinh, mo_hinh)}-{loai_bai}-{che_do}-{lan}"


def _ten_hien_thi(phien, nhom, slug):
    ten = phien.ten_lua_chon.get(nhom, {}).get(slug)
    if not ten:
        raise LoiCopyPro(f"generate-options không có {nhom} '{slug}'")
    return ten


def sinh_mot_bai(phien, ma_mau, ten_san_pham, loai_bai, che_do, mo_hinh, lan, thong_so="",
                 phien_ban_copypro="", thu_muc_ra=THU_MUC_RA):
    """Sinh một bài qua POST /contents/generate đúng như giao diện, ghi <thu_muc_ra>/<ma_qc>.json và
    trả bản ghi (dict). thong_so là chuỗi dùng làm 'Thông tin bổ sung' khi che_do == 'ten_thong_so',
    phải rỗng khi che_do == 'ten'."""
    if loai_bai not in LOAI_BAI:
        raise ValueError(f"loại bài không hợp lệ: {loai_bai}")
    if che_do not in CHE_DO:
        raise ValueError(f"chế độ không hợp lệ: {che_do}")
    if (che_do == "ten_thong_so") != bool(thong_so):
        raise ValueError("thong_so phải có khi che_do là 'ten_thong_so' và phải rỗng khi che_do là 'ten'")
    ma_qc = ma_quang_cao(ma_mau, mo_hinh, loai_bai, che_do, lan)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", ma_qc):
        raise ValueError(f"mã quảng cáo có ký tự không dùng làm tên tệp được: {ma_qc}")
    duong_dan = Path(thu_muc_ra) / f"{ma_qc}.json"
    if duong_dan.exists():  # kiểm trước để không tốn một lượt gọi LLM
        raise FileExistsError(f"đã có {duong_dan}, không ghi đè")

    cau_lenh = ghep_cau_lenh(
        _ten_hien_thi(phien, "industries", NGANH), _ten_hien_thi(phien, "copyTypes", loai_bai),
        _ten_hien_thi(phien, "tones", GIONG), ten_san_pham, loai_bai,
        bo_sung=thong_so, do_dai=DO_DAI, so_phien_ban=SO_PHIEN_BAN)
    tai_gui = {
        "prompt": cau_lenh, "type": loai_bai, "industry": NGANH, "tone": GIONG, "language": "vi",
        "model": mo_hinh, "modelMode": "base", "length": DO_DAI, "variations": SO_PHIEN_BAN,
        "maxOutputTokens": GIOI_HAN_TOKEN[DO_DAI], "templateId": None, "projectId": None,
    }
    ma, nd = goi_api("POST", f"{phien.dia_chi}/contents/generate", token=phien.token, du_lieu=tai_gui,
                     timeout=THOI_GIAN_CHO_TAO_BAI)
    if ma != 200:
        raise _loi_http(f"sinh {ma_qc}", ma, nd)
    data = _data(nd)
    if data.get("fallback"):
        raise LoiCopyPro(f"sinh {ma_qc}: CopyPro trả bài mẫu (fallback), không phải bài do LLM")
    item = data.get("item")
    if not isinstance(item, dict) or not (item.get("outputText") or "").strip():
        raise LoiCopyPro(f"sinh {ma_qc}: phản hồi không có data.item.outputText")

    ban_ghi = {
        "ma_qc": ma_qc, "ma_mau": ma_mau, "ten_nhap": ten_san_pham, "loai_bai": loai_bai,
        "che_do": che_do, "lan": lan, "mo_hinh": mo_hinh, "mo_hinh_tra_ve": item.get("modelUsed"),
        "mo_hinh_nha_cung_cap": MO_HINH_NHA_CUNG_CAP.get(mo_hinh),
        "thoi_diem": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "ma_bai_copypro": item.get("id"), "phien_ban_copypro": phien_ban_copypro,
        "tai_gui": tai_gui, "cau_lenh": cau_lenh, "prompt_copypro_luu": item.get("prompt"),
        "prompt_trung": item.get("prompt") == cau_lenh, "noi_dung": item["outputText"],
        "usage": data.get("usage"), "fallback": False, "tham_so_backend": dict(THAM_SO_BACKEND),
    }
    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    with open(duong_dan, "x", encoding="utf-8", newline="\n") as f:  # "x": không ghi đè
        json.dump(ban_ghi, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return ban_ghi


def main(argv=None):
    parser = argparse.ArgumentParser(description="Sinh một quảng cáo bằng CopyPro (API backend ở máy).")
    parser.add_argument("--mau", required=True, help="mã mẫu sản phẩm (cột ma_mau của mau_san_pham.csv)")
    parser.add_argument("--ten", required=True, help="tên sản phẩm nhập vào ô Sản phẩm/dịch vụ")
    parser.add_argument("--loai", required=True, choices=LOAI_BAI)
    parser.add_argument("--che-do", required=True, choices=CHE_DO)
    parser.add_argument("--mo-hinh", required=True, help="mã mô hình CopyPro, vd gemini-3-6-flash")
    parser.add_argument("--lan", type=int, default=1)
    parser.add_argument("--thong-so-tep", help="tệp văn bản thông số (chỉ khi --che-do ten_thong_so)")
    parser.add_argument("--phien-ban-copypro", default="", help="commit của CopyPro đang chạy")
    parser.add_argument("--thu-muc-ra", default=str(THU_MUC_RA))
    tham_so = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    if (tham_so.che_do == "ten_thong_so") != bool(tham_so.thong_so_tep):
        parser.error("--thong-so-tep bắt buộc khi --che-do ten_thong_so và không dùng khi --che-do ten")
    thong_so = ""
    if tham_so.thong_so_tep:
        thong_so = Path(tham_so.thong_so_tep).read_text(encoding="utf-8").strip()  # bỏ xuống dòng cuối tệp
    if not tham_so.phien_ban_copypro:
        print("Cảnh báo: chưa có --phien-ban-copypro, bản ghi sẽ không ghi được phiên bản CopyPro.",
              file=sys.stderr)
    try:
        phien = mo_phien()
        ban_ghi = sinh_mot_bai(phien, tham_so.mau, tham_so.ten, tham_so.loai, tham_so.che_do,
                               tham_so.mo_hinh, tham_so.lan, thong_so, tham_so.phien_ban_copypro,
                               Path(tham_so.thu_muc_ra))
    except (LoiCopyPro, FileExistsError) as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        return 1
    print(f"ma_qc: {ban_ghi['ma_qc']}")
    print(f"so_ky_tu: {len(ban_ghi['noi_dung'])}")
    print(f"prompt_trung: {ban_ghi['prompt_trung']}")
    print(f"tong_token: {(ban_ghi['usage'] or {}).get('totalTokens')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
