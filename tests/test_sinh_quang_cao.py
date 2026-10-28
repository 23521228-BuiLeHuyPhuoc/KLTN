from datetime import datetime
import json
from pathlib import Path
import re

import pytest

from kiemchung import sinh_quang_cao as sq

GOC = Path(__file__).resolve().parents[1]
TOKEN = "token-bi-mat-cua-phien-thu"


def doc_dong_goc():
    with open(GOC / "ket_qua" / "khao_sat_quang_cao_goc.jsonl", encoding="utf-8") as f:
        return [json.loads(d) for d in f]


DONG_GOC = doc_dong_goc()


def tach_cau_lenh(prompt):
    """(tên ngành, tên loại bài, tên giọng, thông số bổ sung hoặc '') đọc lại từ câu lệnh CopyPro đã lưu."""
    nganh = re.search(r"Bạn là chuyên gia copywriting cho ngành (.+)\.", prompt).group(1)
    loai, giong = re.search(r"Hãy viết (.+) với tone (.+)\.", prompt).groups()
    bo_sung = re.search(r"Thông tin bổ sung: (.*)\.\nĐộ dài", prompt, re.DOTALL)
    return nganh, loai, giong, bo_sung.group(1) if bo_sung else ""


def dong_goc(ma_mau, loai_bai, che_do):
    (dong,) = [d for d in DONG_GOC if (d["ma_mau"], d["loai_bai"], d["che_do"]) == (ma_mau, loai_bai, che_do)]
    return dong


def ten_lua_chon_tu_du_lieu():
    """Bảng tên lựa chọn dựng lại từ 18 dòng thật (slug thực nghiệm -> tên CopyPro hiển thị)."""
    bang = {"industries": {}, "copyTypes": {}, "tones": {}}
    for d in DONG_GOC:
        nganh, loai, giong, _ = tach_cau_lenh(d["prompt_copypro_luu"])
        bang["industries"][sq.NGANH] = nganh
        bang["copyTypes"][d["loai_bai"]] = loai
        bang["tones"][sq.GIONG] = giong
    return bang


@pytest.fixture()
def phien():
    return sq.PhienDangNhap("http://may-gia/api", TOKEN, ten_lua_chon_tu_du_lieu())


# ---- ghep_cau_lenh: trùng từng ký tự với câu lệnh CopyPro đã lưu ----

def test_du_lieu_goc_la_18_dong_ba_mau_ba_loai_hai_che_do():
    assert len(DONG_GOC) == 18
    assert {(d["ma_mau"], d["loai_bai"], d["che_do"]) for d in DONG_GOC} == {
        (m, loai, cd) for m in {d["ma_mau"] for d in DONG_GOC} for loai in sq.LOAI_BAI for cd in sq.CHE_DO}


@pytest.mark.parametrize("dong", DONG_GOC, ids=lambda d: f"{d['ma_mau']}-{d['loai_bai']}-{d['che_do']}")
def test_ghep_cau_lenh_trung_prompt_copypro_da_luu(dong):
    nganh, loai, giong, thong_so = tach_cau_lenh(dong["prompt_copypro_luu"])
    assert bool(thong_so) == (dong["che_do"] == "ten_thong_so")
    cau_lenh = sq.ghep_cau_lenh(nganh, loai, giong, dong["ten_nhap"], dong["loai_bai"], bo_sung=thong_so)
    assert cau_lenh == dong["prompt_copypro_luu"]


def ghep(loai_bai, **kw):
    return sq.ghep_cau_lenh("Công nghệ", "Tên loại", "Chuyên nghiệp", "Máy A", loai_bai, **kw)


def test_dong_dinh_dang_landing_short_medium_long():
    chung_dau = ["Hero headline: tiêu đề chính của hero section.", "Subheadline: câu phụ làm rõ giá trị."]
    chung_giua = ["Lợi ích chính: 3 bullet.", "Bằng chứng: review, số liệu, cam kết hoặc social proof."]
    chung_cuoi = ["Lời kêu gọi hành động: nút hoặc lời kêu gọi hành động chính.",
                  "Không viết thành email, SEO metadata hoặc một caption social ngắn."]
    pain = "Pain point: vấn đề khách hàng đang gặp."
    offer = "Offer: ưu đãi hoặc lý do hành động ngay."
    assert sq.dong_dinh_dang("landing", "short") == "\n".join(chung_dau + chung_giua + chung_cuoi)
    assert sq.dong_dinh_dang("landing", "medium") == "\n".join(chung_dau + chung_giua + [offer] + chung_cuoi)
    assert sq.dong_dinh_dang("landing", "long") == "\n".join(chung_dau + [pain] + chung_giua + [offer] + chung_cuoi)


def test_description_va_social_khong_doi_theo_do_dai():
    for loai in ("description", "social"):
        assert sq.dong_dinh_dang(loai, "short") == sq.dong_dinh_dang(loai, "medium") == sq.dong_dinh_dang(loai, "long")
    assert sq.dong_dinh_dang("social", "long").splitlines()[0] == "Hook: câu mở đầu kéo chú ý."
    assert sq.dong_dinh_dang("description", "long").splitlines()[-1] == (
        "Không dùng format email, SEO metadata hoặc caption mạng xã hội.")


def test_loai_bai_hoac_do_dai_la_bao_loi():
    with pytest.raises(ValueError):
        sq.dong_dinh_dang("email", "medium")
    with pytest.raises(ValueError):
        sq.dong_dinh_dang("social", "rat_dai")
    with pytest.raises(ValueError):
        ghep("social", do_dai="rat_dai")


def test_do_dai_quyet_dinh_nhan_va_gioi_han_token():
    for do_dai, nhan, token in (("short", "ngắn gọn", 900), ("medium", "vừa đủ chi tiết", 1800),
                                ("long", "dài và giàu chi tiết", 3200)):
        cau_lenh = ghep("landing", do_dai=do_dai)
        assert f"Độ dài mong muốn: {nhan}." in cau_lenh
        assert f"Giới hạn output tối đa: {token} tokens." in cau_lenh
    assert "Giới hạn output tối đa: 500 tokens." in ghep("social", max_output_tokens=500)


def test_dong_mac_dinh_khi_bo_trong_va_dong_nhap_khi_co():
    trong = sq.ghep_cau_lenh("Công nghệ", "Tên loại", "Chuyên nghiệp", "", "social").splitlines()
    assert "Sản phẩm/dịch vụ: chưa được cung cấp, hãy tự giả định hợp lý theo ngành đã chọn." in trong
    assert ("Từ khóa chính: chưa được cung cấp, ưu tiên lợi ích rõ ràng và lời kêu gọi hành động mạnh."
            in trong)
    assert "Đối tượng mục tiêu: khách hàng tiềm năng phổ thông." in trong
    assert not any(d.startswith("Thông tin bổ sung") for d in trong)
    co = ghep("social", tu_khoa="pin trâu", doi_tuong="dân văn phòng", bo_sung="A\nB").splitlines()
    assert "Sản phẩm/dịch vụ: Máy A." in co
    assert "Từ khóa chính: pin trâu." in co
    assert "Đối tượng mục tiêu: dân văn phòng." in co
    assert co[co.index("Thông tin bổ sung: A"):][:2] == ["Thông tin bổ sung: A", "B."]


def test_nhieu_phien_ban_liet_ke_tung_phien_ban_va_nhiet_do_in_nhu_js():
    cau_lenh = ghep("social", so_phien_ban=3, nhiet_do=1.0).splitlines()
    assert "Tạo đúng 3 phiên bản riêng biệt." in cau_lenh
    i = cau_lenh.index("Định dạng bắt buộc:")
    assert cau_lenh[i + 1:i + 5] == ["Phiên bản 1: ...", "Phiên bản 2: ...", "Phiên bản 3: ...",
                                     "Mỗi phiên bản phải tự đứng độc lập, không gom chung thành một đoạn lớn."]
    assert cau_lenh[-1] == "Temperature tham khảo: 1."
    assert ghep("social").splitlines()[-1] == "Temperature tham khảo: 0.7."


def test_so_js():
    assert sq.so_js(0.7) == "0.7"
    assert sq.so_js(1.0) == "1"
    assert sq.so_js(0.75) == "0.75"
    assert sq.so_js(2) == "2"
    assert sq.so_js(0.0) == "0"
    assert sq.so_js(-0.0) == "0"
    assert sq.so_js(0.1 + 0.2) == "0.30000000000000004"


# ---- thay hàm gọi API, không đụng mạng ----

def phan_hoi_tot(du_lieu, **ghi_de):
    item = {"id": "bai-123", "prompt": du_lieu["prompt"], "outputText": "Quảng cáo thử có dấu tiếng Việt.",
            "modelUsed": "gemini-3.6-flash-preview", **ghi_de.pop("item", {})}
    data = {"item": item, "usage": {"promptTokens": 300, "completionTokens": 200, "totalTokens": 500},
            "template": None, "fallback": False, "plagiarism": None, **ghi_de}
    return 200, {"success": True, "data": data}


class MayGia:
    """Thay sq.goi_api: ghi lại mọi lời gọi, trả phản hồi định sẵn giống CopyPro."""

    def __init__(self, tao_bai=phan_hoi_tot):
        self.loi_goi = []
        self.tao_bai = tao_bai

    def __call__(self, phuong_thuc, url, token=None, du_lieu=None, timeout=30):
        self.loi_goi.append({"phuong_thuc": phuong_thuc, "url": url, "token": token, "du_lieu": du_lieu,
                             "timeout": timeout})
        if url.endswith("/auth/user/login"):
            return 200, {"success": True, "data": {"token": TOKEN, "user": {"email": du_lieu["email"]}}}
        if url.endswith("/generate-options"):
            return 200, {"data": {
                "industries": [{"slug": s, "name": n} for s, n in ten_lua_chon_tu_du_lieu()["industries"].items()],
                "copyTypes": [{"slug": s, "name": n} for s, n in ten_lua_chon_tu_du_lieu()["copyTypes"].items()],
                "tones": [{"slug": s, "name": n} for s, n in ten_lua_chon_tu_du_lieu()["tones"].items()]}}
        if url.endswith("/contents/generate"):
            return self.tao_bai(du_lieu)
        raise AssertionError(f"gọi lạ: {url}")

    def goi_tao_bai(self):
        return [c for c in self.loi_goi if c["url"].endswith("/contents/generate")]


@pytest.fixture()
def may(monkeypatch):
    for ten in ("COPYPRO_API", "COPYPRO_EMAIL", "COPYPRO_MAT_KHAU"):
        monkeypatch.delenv(ten, raising=False)
    may_gia = MayGia()
    monkeypatch.setattr(sq, "goi_api", may_gia)
    return may_gia


def doc_ban_ghi(thu_muc, ma_qc):
    return json.loads((thu_muc / f"{ma_qc}.json").read_text(encoding="utf-8"))


CAC_TRUONG = ["ma_qc", "ma_mau", "ten_nhap", "loai_bai", "che_do", "lan", "mo_hinh", "mo_hinh_tra_ve",
              "mo_hinh_nha_cung_cap", "thoi_diem",
              "ma_bai_copypro", "phien_ban_copypro", "tai_gui", "cau_lenh", "prompt_copypro_luu", "prompt_trung",
              "noi_dung", "usage", "fallback", "tham_so_backend"]
CAC_KHOA_TAI_GUI = ["prompt", "type", "industry", "tone", "language", "model", "modelMode", "length", "variations",
                    "maxOutputTokens", "templateId", "projectId"]


def test_sinh_mot_bai_gui_dung_payload_nhu_giao_dien(phien, may, tmp_path):
    dong = dong_goc("dt-apple-iphone17", "social", "ten")
    sq.sinh_mot_bai(phien, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1,
                    phien_ban_copypro="abc1234", thu_muc_ra=tmp_path)
    (goi,) = may.goi_tao_bai()
    assert goi["phuong_thuc"] == "POST"
    assert goi["url"] == "http://may-gia/api/contents/generate"
    assert goi["token"] == TOKEN
    assert goi["timeout"] == 240
    tai_gui = goi["du_lieu"]
    assert list(tai_gui) == CAC_KHOA_TAI_GUI
    assert tai_gui == {
        "prompt": dong["prompt_copypro_luu"], "type": "social", "industry": "technology",
        "tone": "professional", "language": "vi", "model": "gemini-3-6-flash", "modelMode": "base",
        "length": "medium", "variations": 1, "maxOutputTokens": 1800, "templateId": None, "projectId": None}


def test_sinh_mot_bai_ghi_tep_json_day_du(phien, may, tmp_path):
    ban_ghi = sq.sinh_mot_bai(phien, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1,
                              phien_ban_copypro="abc1234", thu_muc_ra=tmp_path)
    ma_qc = "qc-dt-apple-iphone17-gemini-social-ten-1"
    tep = tmp_path / f"{ma_qc}.json"
    van_ban = tep.read_text(encoding="utf-8")
    assert van_ban.startswith('{\n  "ma_qc": ')  # thụt lề 2
    assert "Quảng cáo thử có dấu tiếng Việt." in van_ban and "\\u" not in van_ban  # ensure_ascii=False
    assert TOKEN not in van_ban
    luu = json.loads(van_ban)
    assert luu == ban_ghi
    assert list(luu) == CAC_TRUONG
    (goi,) = may.goi_tao_bai()
    assert luu["tai_gui"] == goi["du_lieu"]
    assert luu["ma_qc"] == ma_qc
    assert (luu["ma_mau"], luu["ten_nhap"], luu["loai_bai"], luu["che_do"], luu["lan"]) == (
        "dt-apple-iphone17", "iPhone 17", "social", "ten", 1)
    assert luu["mo_hinh"] == "gemini-3-6-flash"
    assert luu["mo_hinh_tra_ve"] == "gemini-3.6-flash-preview"
    assert luu["ma_bai_copypro"] == "bai-123"
    assert luu["phien_ban_copypro"] == "abc1234"
    assert luu["cau_lenh"] == dong_goc("dt-apple-iphone17", "social", "ten")["prompt_copypro_luu"]
    assert luu["prompt_copypro_luu"] == luu["cau_lenh"] and luu["prompt_trung"] is True
    assert luu["noi_dung"] == "Quảng cáo thử có dấu tiếng Việt."
    assert luu["usage"] == {"promptTokens": 300, "completionTokens": 200, "totalTokens": 500}
    assert luu["fallback"] is False
    assert luu["tham_so_backend"] == {"temperature": 0.75, "top_p": 0.9}
    assert datetime.fromisoformat(luu["thoi_diem"]).utcoffset() is not None  # có múi giờ


def test_che_do_ten_thong_so_dua_thong_so_vao_thong_tin_bo_sung(phien, may, tmp_path):
    dong = dong_goc("tn-samsung-buds3pro", "landing", "ten_thong_so")
    thong_so = tach_cau_lenh(dong["prompt_copypro_luu"])[3]
    ban_ghi = sq.sinh_mot_bai(phien, "tn-samsung-buds3pro", "Samsung Galaxy Buds3 Pro", "landing", "ten_thong_so",
                              "groq-gpt-oss-120b", 2, thong_so, thu_muc_ra=tmp_path)
    assert ban_ghi["ma_qc"] == "qc-tn-samsung-buds3pro-gptoss-landing-ten_thong_so-2"
    assert ban_ghi["cau_lenh"] == dong["prompt_copypro_luu"]
    assert may.goi_tao_bai()[0]["du_lieu"]["model"] == "groq-gpt-oss-120b"
    assert (tmp_path / "qc-tn-samsung-buds3pro-gptoss-landing-ten_thong_so-2.json").exists()


def test_ma_quang_cao():
    assert sq.ma_quang_cao("m1", "gemini-3-6-flash", "social", "ten", 3) == "qc-m1-gemini-social-ten-3"
    assert sq.ma_quang_cao("m1", "groq-gpt-oss-120b", "landing", "ten_thong_so", 1) == (
        "qc-m1-gptoss-landing-ten_thong_so-1")
    assert sq.ma_quang_cao("m1", "mo-hinh-khac", "description", "ten", 1) == "qc-m1-mo-hinh-khac-description-ten-1"


def test_prompt_trung_false_khi_copypro_luu_cau_lenh_khac(phien, monkeypatch, tmp_path):
    monkeypatch.setattr(sq, "goi_api", MayGia(
        lambda du_lieu: phan_hoi_tot(du_lieu, item={"prompt": du_lieu["prompt"] + " (đã sửa)"})))
    ban_ghi = sq.sinh_mot_bai(phien, "dh-apple-watchse3", "Apple Watch SE 3", "description", "ten",
                              "gemini-3-6-flash", 1, thu_muc_ra=tmp_path)
    assert ban_ghi["prompt_trung"] is False
    assert ban_ghi["prompt_copypro_luu"] == ban_ghi["cau_lenh"] + " (đã sửa)"


def test_khong_ghi_de_tep_da_co(phien, may, tmp_path):
    tham_so = (phien, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1)
    sq.sinh_mot_bai(*tham_so, thu_muc_ra=tmp_path)
    tep = tmp_path / "qc-dt-apple-iphone17-gemini-social-ten-1.json"
    truoc = tep.read_bytes()
    with pytest.raises(FileExistsError):
        sq.sinh_mot_bai(*tham_so, thu_muc_ra=tmp_path)
    assert tep.read_bytes() == truoc
    assert len(may.goi_tao_bai()) == 1  # lần hai báo lỗi trước khi gọi LLM
    sq.sinh_mot_bai(*tham_so[:-1], 2, thu_muc_ra=tmp_path)  # lần khác thì ghi bình thường
    assert len(list(tmp_path.glob("*.json"))) == 2


def test_tao_thu_muc_ra_neu_chua_co(phien, may, tmp_path):
    ra = tmp_path / "con" / "quang_cao"
    sq.sinh_mot_bai(phien, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1, thu_muc_ra=ra)
    assert (ra / "qc-dt-apple-iphone17-gemini-social-ten-1.json").exists()


def test_fallback_la_loi_va_khong_ghi_tep(phien, monkeypatch, tmp_path):
    monkeypatch.setattr(sq, "goi_api", MayGia(lambda du_lieu: phan_hoi_tot(du_lieu, fallback=True)))
    with pytest.raises(sq.LoiCopyPro, match="fallback"):
        sq.sinh_mot_bai(phien, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1,
                        thu_muc_ra=tmp_path)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("ma", [400, 401, 403, 429, 500, 503])
def test_ma_http_khac_200_la_loi_va_khong_ghi_tep(phien, monkeypatch, tmp_path, ma):
    monkeypatch.setattr(sq, "goi_api", MayGia(lambda du_lieu: (ma, {"success": False, "message": "Hết hạn mức"})))
    with pytest.raises(sq.LoiCopyPro) as loi:
        sq.sinh_mot_bai(phien, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1,
                        thu_muc_ra=tmp_path)
    assert str(ma) in str(loi.value) and "Hết hạn mức" in str(loi.value)
    assert list(tmp_path.iterdir()) == []


def test_phan_hoi_thieu_bai_la_loi(phien, monkeypatch, tmp_path):
    monkeypatch.setattr(sq, "goi_api", MayGia(lambda du_lieu: phan_hoi_tot(du_lieu, item={"outputText": "  "})))
    with pytest.raises(sq.LoiCopyPro, match="outputText"):
        sq.sinh_mot_bai(phien, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1,
                        thu_muc_ra=tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_tham_so_sai_bao_loi_truoc_khi_goi_api(phien, may, tmp_path):
    co_ban = (phien, "dt-apple-iphone17", "iPhone 17")
    with pytest.raises(ValueError):  # chế độ ten mà có thông số
        sq.sinh_mot_bai(*co_ban, "social", "ten", "gemini-3-6-flash", 1, "thông số", thu_muc_ra=tmp_path)
    with pytest.raises(ValueError):  # chế độ ten_thong_so mà thiếu thông số
        sq.sinh_mot_bai(*co_ban, "social", "ten_thong_so", "gemini-3-6-flash", 1, thu_muc_ra=tmp_path)
    with pytest.raises(ValueError):
        sq.sinh_mot_bai(*co_ban, "email", "ten", "gemini-3-6-flash", 1, thu_muc_ra=tmp_path)
    with pytest.raises(ValueError):
        sq.sinh_mot_bai(*co_ban, "social", "ten_khac", "gemini-3-6-flash", 1, thu_muc_ra=tmp_path)
    with pytest.raises(ValueError):  # mã dùng làm tên tệp không được chứa dấu gạch chéo
        sq.sinh_mot_bai(phien, "../ra-ngoai", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1,
                        thu_muc_ra=tmp_path)
    assert may.loi_goi == [] and list(tmp_path.iterdir()) == []


def test_thieu_ten_lua_chon_la_loi(may, tmp_path):
    thieu = sq.PhienDangNhap("http://may-gia/api", TOKEN, {"industries": {}, "copyTypes": {}, "tones": {}})
    with pytest.raises(sq.LoiCopyPro, match="industries"):
        sq.sinh_mot_bai(thieu, "dt-apple-iphone17", "iPhone 17", "social", "ten", "gemini-3-6-flash", 1,
                        thu_muc_ra=tmp_path)
    assert may.loi_goi == []


def test_token_khong_lo_ra_o_repr():
    assert TOKEN not in repr(sq.PhienDangNhap("http://may-gia/api", TOKEN, {}))


# ---- đăng nhập, lấy lựa chọn, dòng lệnh ----

def test_mo_phien_dung_bien_moi_truong_va_bearer(monkeypatch):
    monkeypatch.setenv("COPYPRO_API", "http://may-khac:5000/api/")
    monkeypatch.setenv("COPYPRO_EMAIL", "a@b.vn")
    monkeypatch.setenv("COPYPRO_MAT_KHAU", "mk-thu")
    may_gia = MayGia()
    monkeypatch.setattr(sq, "goi_api", may_gia)
    phien = sq.mo_phien()
    dang_nhap, lua_chon = may_gia.loi_goi
    assert (dang_nhap["phuong_thuc"], dang_nhap["url"]) == ("POST", "http://may-khac:5000/api/auth/user/login")
    assert dang_nhap["du_lieu"] == {"email": "a@b.vn", "password": "mk-thu"}
    assert dang_nhap["token"] is None
    assert (lua_chon["phuong_thuc"], lua_chon["url"], lua_chon["token"]) == (
        "GET", "http://may-khac:5000/api/generate-options", TOKEN)
    assert phien.dia_chi == "http://may-khac:5000/api" and phien.token == TOKEN
    assert phien.ten_lua_chon == ten_lua_chon_tu_du_lieu()


def test_mo_phien_mac_dinh_la_tai_khoan_seed_o_may(may):
    sq.mo_phien()
    dang_nhap = may.loi_goi[0]
    assert dang_nhap["url"] == "http://localhost:4000/api/auth/user/login"
    assert dang_nhap["du_lieu"] == {"email": "customer@copypro.vn", "password": sq.MAT_KHAU_MAC_DINH}


def test_dang_nhap_that_bai_la_loi(monkeypatch):
    monkeypatch.setattr(sq, "goi_api", lambda *a, **kw: (401, {"success": False, "message": "Sai mật khẩu"}))
    with pytest.raises(sq.LoiCopyPro, match="401.*Sai mật khẩu"):
        sq.dang_nhap("http://may-gia/api", "a@b.vn", "x")
    monkeypatch.setattr(sq, "goi_api", lambda *a, **kw: (200, {"data": {}}))
    with pytest.raises(sq.LoiCopyPro, match="token"):
        sq.dang_nhap("http://may-gia/api", "a@b.vn", "x")


def test_main_in_ket_qua_va_ghi_tep(may, tmp_path, capsys):
    tep_thong_so = tmp_path / "thong_so.txt"
    thong_so = tach_cau_lenh(dong_goc("dh-apple-watchse3", "social", "ten_thong_so")["prompt_copypro_luu"])[3]
    tep_thong_so.write_text(thong_so + "\n", encoding="utf-8")  # xuống dòng cuối tệp không vào câu lệnh
    ra = tmp_path / "ra"
    ma_thoat = sq.main(["--mau", "dh-apple-watchse3", "--ten", "Apple Watch SE 3", "--loai", "social",
                        "--che-do", "ten_thong_so", "--mo-hinh", "gemini-3-6-flash", "--lan", "1",
                        "--thong-so-tep", str(tep_thong_so), "--phien-ban-copypro", "abc1234",
                        "--thu-muc-ra", str(ra)])
    assert ma_thoat == 0
    in_ra = capsys.readouterr().out
    assert "ma_qc: qc-dh-apple-watchse3-gemini-social-ten_thong_so-1" in in_ra
    assert f"so_ky_tu: {len('Quảng cáo thử có dấu tiếng Việt.')}" in in_ra
    assert "prompt_trung: True" in in_ra
    assert "tong_token: 500" in in_ra
    ban_ghi = doc_ban_ghi(ra, "qc-dh-apple-watchse3-gemini-social-ten_thong_so-1")
    assert ban_ghi["cau_lenh"] == dong_goc("dh-apple-watchse3", "social", "ten_thong_so")["prompt_copypro_luu"]
    assert ban_ghi["phien_ban_copypro"] == "abc1234"


def test_main_loi_copypro_tra_ma_1(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(sq, "goi_api", MayGia(lambda du_lieu: phan_hoi_tot(du_lieu, fallback=True)))
    ma_thoat = sq.main(["--mau", "dt-apple-iphone17", "--ten", "iPhone 17", "--loai", "social",
                        "--che-do", "ten", "--mo-hinh", "gemini-3-6-flash", "--thu-muc-ra", str(tmp_path)])
    assert ma_thoat == 1
    assert "fallback" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_main_che_do_ten_thong_so_thieu_tep_la_loi_dong_lenh(may, tmp_path):
    with pytest.raises(SystemExit) as thoat:
        sq.main(["--mau", "dt-apple-iphone17", "--ten", "iPhone 17", "--loai", "social",
                 "--che-do", "ten_thong_so", "--mo-hinh", "gemini-3-6-flash", "--thu-muc-ra", str(tmp_path)])
    assert thoat.value.code == 2
    assert may.loi_goi == []
