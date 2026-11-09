"""Dịch vụ kiểm chứng (Bước 34; T7.1, T7.2): FastAPI bọc phương pháp P đầu-cuối.

    GET  /mau-san-pham  danh sách mẫu có data/nguon/<ma_mau>/doan.jsonl: {ma_mau, ten, nhom, hang}
    POST /kiem-chung    {"van_ban": "...", "ma_mau": "..."} -> {"phien_ban_he_thong", "ket_qua": [...], "thoi_gian_ms"}

POST /kiem-chung tách tuyên bố tự động (tach_tuyen_bo.tach_bai, đã lọc theo thuộc tính của nhóm) rồi chạy p.kiem_chung cho từng
tuyên bố; mỗi phần tử ket_qua: tuyen_bo, thuoc_tinh (thuộc tính dự kiến của bước tách), nhan (DUNG, SAI, LECH, CHUA_DU), doan_nguon
([{ma_doan, noi_dung}] các đoạn tài liệu chính hãng làm bằng chứng), trich (câu trích giá trị), ly_do. Lỗi LLM (quota, mạng, khóa,
đầu ra không dùng được) trả HTTP 503 với mã lỗi an toàn của llm.py, không kèm khóa hay chi tiết của nhà cung cấp.

Cấu hình qua biến môi trường (nạp thêm từ .env nếu có python-dotenv, lúc dựng client thật, không ghi đè biến đã có):
    KIEMCHUNG_MO_HINH (gemini-3.6-flash), KIEMCHUNG_K (5), KIEMCHUNG_CACH_TACH (am_tiet), KIEMCHUNG_TIMEOUT_S (90),
    KIEMCHUNG_CACHE_DIR (ket_qua/llm_cache_api, tách khỏi bộ nhớ đệm thực nghiệm), KIEMCHUNG_NHAT_KY (ket_qua/llm_calls_api.jsonl),
    KIEMCHUNG_COMMIT (mã commit khi trong image không có .git). Đường dẫn tương đối tính từ gốc repo.

Chạy thử:
    PYTHONPATH=src .venv/Scripts/python.exe -m uvicorn kiemchung.api:app --port 8000
"""
import hashlib
import os
from pathlib import Path
import subprocess
import threading
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from . import p as pp, tach_tuyen_bo as tach, trich_xuat as tx, truy_hoi as th
from .cau_hinh import doc_mau
from .doi_chung.b0 import NHA_CUNG_CAP
from .llm import LLMClient, LLMError

try:
    from dotenv import load_dotenv
except ImportError:  # chưa cài python-dotenv: chỉ dùng biến môi trường có sẵn
    load_dotenv = None

GOC = th.GOC
MO_HINH_MAC_DINH = "gemini-3.6-flash"
K_MAC_DINH = 5
CACH_TACH_MAC_DINH = "am_tiet"
TIMEOUT_MAC_DINH = 90.0
SO_LAN_THU_LAI = 2
DO_DAI_TOI_DA = 20_000


class YeuCau(BaseModel):
    van_ban: str = Field(max_length=DO_DAI_TOI_DA)
    ma_mau: str

    @field_validator("van_ban")
    @classmethod
    def _khac_rong(cls, v):
        if not v.strip():
            raise ValueError("van_ban không được rỗng")
        return v


def _sha(chu):
    return hashlib.sha256(chu.encode("utf-8")).hexdigest()


def _ma_commit():
    """Mã commit git ngắn của gốc repo; không đọc được thì lấy KIEMCHUNG_COMMIT, rồi 'khong-ro'."""
    try:
        kq = subprocess.run(["git", "-C", str(GOC), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=5)
        if kq.returncode == 0 and kq.stdout.strip():
            return kq.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return os.environ.get("KIEMCHUNG_COMMIT") or "khong-ro"


def phien_ban_he_thong(mo_hinh, k, cach_tach, ma_commit):
    """Chuỗi định danh cấu hình đã chạy: commit, mô hình, k, cách tách, mã băm (12 ký tự đầu) câu lệnh trích xuất và câu lệnh tách."""
    return (f"commit={ma_commit}; mo_hinh={mo_hinh}; k={k}; cach_tach={cach_tach}; "
            f"cau_lenh_trich_xuat={_sha(tx.CAU_LENH_TRICH_XUAT)[:12]}; cau_lenh_tach={_sha(tach.CAU_LENH_TACH)[:12]}")


def _duong(chu, mac_dinh):
    duong = Path(os.environ.get(chu) or mac_dinh)
    return duong if duong.is_absolute() else GOC / duong


def _tao_client():
    if load_dotenv is not None:
        load_dotenv(GOC / ".env", override=False, interpolate=False)
    return LLMClient(_duong("KIEMCHUNG_CACHE_DIR", "ket_qua/llm_cache_api"),
                     _duong("KIEMCHUNG_NHAT_KY", "ket_qua/llm_calls_api.jsonl"),
                     timeout_s=float(os.environ.get("KIEMCHUNG_TIMEOUT_S") or TIMEOUT_MAC_DINH), max_retries=SO_LAN_THU_LAI)


def tao_app(client=None, mo_hinh=None, k=None, cach_tach=None, thu_muc_nguon=None):
    """Dựng ứng dụng. client: llm.LLMClient tiêm từ ngoài (test dùng transport giả); None thì dựng client thật ở lần gọi đầu.
    Tham số để trống lấy từ biến môi trường rồi giá trị mặc định. thu_muc_nguon mặc định data/nguon."""
    mo_hinh = mo_hinh or os.environ.get("KIEMCHUNG_MO_HINH") or MO_HINH_MAC_DINH
    k = k if k is not None else int(os.environ.get("KIEMCHUNG_K") or K_MAC_DINH)
    cach_tach = cach_tach or os.environ.get("KIEMCHUNG_CACH_TACH") or CACH_TACH_MAC_DINH
    thu_muc_nguon = Path(thu_muc_nguon) if thu_muc_nguon else th.THU_MUC_NGUON
    if mo_hinh not in NHA_CUNG_CAP:
        raise ValueError(f"mô hình chưa có nhà cung cấp: {mo_hinh!r}")
    if k < 1:
        raise ValueError("k phải từ 1 trở lên")
    if cach_tach not in th.CACH_TACH:
        raise ValueError(f"cách tách phải là một trong {th.CACH_TACH}")
    ma_commit = _ma_commit()
    khoa = threading.Lock()   # LLMClient không gộp lời gọi đồng thời: mỗi lần chỉ một yêu cầu kiểm chứng
    dung = {"client": client}

    def mau_trong_kho():
        return [m for m in doc_mau() if (thu_muc_nguon / m["ma_mau"] / "doan.jsonl").is_file()]

    app = FastAPI(title="Dịch vụ kiểm chứng thông số", version="1")

    @app.get("/mau-san-pham")
    def danh_sach_mau():
        return [{"ma_mau": m["ma_mau"], "ten": m["ten"], "nhom": m["nhom"], "hang": m["hang"]} for m in mau_trong_kho()]

    @app.post("/kiem-chung")
    def kiem_chung(yeu_cau: YeuCau):
        bat_dau = time.perf_counter()
        if yeu_cau.ma_mau not in {m["ma_mau"] for m in mau_trong_kho()}:
            raise HTTPException(422, "ma_mau không có trong kho tài liệu")
        bai = {"ma_qc": f"api-{_sha(yeu_cau.van_ban)[:12]}", "ma_mau": yeu_cau.ma_mau, "noi_dung": yeu_cau.van_ban}
        try:
            with khoa:
                if dung["client"] is None:
                    dung["client"] = _tao_client()
                kq_tach = tach.tach_bai(dung["client"], mo_hinh, bai)
                if kq_tach["loi"]:
                    raise LLMError(kq_tach["loi"])
                van_doan = dict(th.doc_doan(yeu_cau.ma_mau, thu_muc_nguon)) if kq_tach["tuyen_bo"] else {}
                ket_qua = []
                for tb in kq_tach["tuyen_bo"]:
                    kq = pp.kiem_chung(tb["tuyen_bo"], yeu_cau.ma_mau, dung["client"], mo_hinh, k, cach_tach,
                                       thu_muc_nguon=thu_muc_nguon)
                    ket_qua.append(_phan_tu(tb, kq, van_doan))
        except LLMError as e:
            raise HTTPException(503, f"Dịch vụ mô hình ngôn ngữ tạm thời không dùng được ({e.code}).") from None
        return {"phien_ban_he_thong": phien_ban_he_thong(mo_hinh, k, cach_tach, ma_commit), "ket_qua": ket_qua,
                "thoi_gian_ms": round((time.perf_counter() - bat_dau) * 1000, 1)}

    return app


def _phan_tu(tb, kq, van_doan):
    """Một phần tử của ket_qua từ tuyên bố đã tách (tb), kết quả P (kq) và {mã đoạn: văn bản} của mẫu."""
    return {"tuyen_bo": tb["tuyen_bo"], "thuoc_tinh": tb["thuoc_tinh_du_kien"], "nhan": kq["nhan"],
            "doan_nguon": [{"ma_doan": ma, "noi_dung": van_doan.get(ma)} for ma in kq["bang_chung"]],
            "trich": kq["trich"], "ly_do": kq["ly_do"]}


app = tao_app()
