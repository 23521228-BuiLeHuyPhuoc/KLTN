"""Small extraction probe for step 2, not the extraction/decision pipeline P."""
from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError

from .llm import LLMResult


class Extraction(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    san_pham: str | None
    phien_ban: str | None
    bo_phan: str | None
    thuoc_tinh: str | None
    gia_tri: float | str | None
    don_vi: str | None
    dieu_kien: dict[str, str]
    kieu_gia_tri: Literal["toi_da", "dien_hinh", "dinh_muc", "khang_dinh", "khong_neu"]
    trich: dict[str, str]
    mac_dinh: list[str]


SYSTEM_PROMPT = """Trích xuất thông số trong MỘT câu tiếng Việt, chỉ trả JSON.
Đây là thử trích xuất, không kiểm chứng đúng/sai. Giữ nguyên số trong câu kể cả
khi câu sai sự thật. Chỉ dùng câu được cung cấp, không dùng kiến thức về sản phẩm.
Không điền cách hiểu mặc định: trường không nêu là null, dieu_kien={}, mac_dinh=[].
Mỗi trường khác null và mỗi điều kiện cần có trich nguyên văn từ câu (khóa như
san_pham, gia_tri, dieu_kien.che_do_chong_on). Không cần trích cho khong_neu.
Quy ước đầu ra của bộ thử (chưa là cấu hình phương pháp P):
- thuoc_tinh: thoi_luong_pin, thoi_gian_sac, do_sang, khang_nuoc.
- Đơn vị: gio, phut, nit; chuẩn IP là gia_tri chuỗi và don_vi=null.
- bo_phan chỉ điền khi nêu rõ: 'hộp sạc' -> hop_sac; 'tai nghe' -> tai_nghe.
- dieu_kien: che_do_chong_on=bat/tat/xuyen_am;
  che_do_nguon=nguon_dien_thap; che_do_hien_thi=cuc_dai nếu nói 'cực đại'.
- Sạc: giá trị là số phút, dieu_kien.moc_sac giữ nguyên cụm phần trăm
  ('lên đến 50%' hoặc '50%'); cong_suat_sac giữ nguyên '40W trở lên' nếu có.
  'lên đến' bổ nghĩa mốc phần trăm không biến số phút thành kiểu toi_da.
- 'đến'/'lên đến' bổ nghĩa thời lượng -> toi_da; 'luôn' -> khang_dinh;
  không nêu -> khong_neu. 'Cực đại' của độ sáng là chế độ hiển thị.
- Không suy ra chống ồn từ tên sản phẩm, chế độ thường, diện tích 25%, phiên bản
  GPS, bộ sạc hay bộ phận nếu không được nêu. 'pin 7 giờ' vẫn là thoi_luong_pin.
Tuân thủ lược đồ JSON sau:
""" + json.dumps(Extraction.model_json_schema(), ensure_ascii=False, sort_keys=True)


def messages_for(case: dict) -> list[dict[str, str]]:
    # Expected answers and source explanations never enter the model prompt.
    return [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": case["text"]}]


SCORE_FIELDS = ["san_pham", "phien_ban", "bo_phan", "thuoc_tinh", "gia_tri",
                "don_vi", "dieu_kien", "kieu_gia_tri"]


def evaluate(text: str, case: dict) -> dict:
    """Diagnostics against prewritten fixtures; never creates verification labels."""
    try:
        parsed = Extraction.model_validate_json(text).model_dump()
    except (ValidationError, ValueError):
        return {"schema_valid": False, "field_correct": {f: False for f in SCORE_FIELDS},
                "omitted_conditions": None, "invented_conditions": None,
                "wrong_conditions": None, "bad_quotes": None, "missing_quotes": None,
                "unexpected_defaults": None}
    expected = case["expected"]
    actual_dk, expected_dk = parsed["dieu_kien"], expected["dieu_kien"]
    required_quotes = {f for f in SCORE_FIELDS if f != "dieu_kien" and
                       parsed[f] is not None and parsed[f] != "khong_neu"}
    required_quotes.update(f"dieu_kien.{k}" for k in actual_dk)
    return {
        "schema_valid": True,
        "field_correct": {f: parsed[f] == expected[f] for f in SCORE_FIELDS},
        "omitted_conditions": sorted(set(expected_dk) - set(actual_dk)),
        "invented_conditions": sorted(set(actual_dk) - set(expected_dk)),
        "wrong_conditions": sorted(k for k in set(actual_dk) & set(expected_dk)
                                   if actual_dk[k] != expected_dk[k]),
        "bad_quotes": sorted(k for k, v in parsed["trich"].items()
                             if not v.strip() or v not in case["text"]),
        "missing_quotes": sorted(required_quotes - set(parsed["trich"])),
        "unexpected_defaults": parsed["mac_dinh"],
    }


def mock_transport(request: dict, timeout_s: float) -> LLMResult:
    """Intentional empty fixture, NOT an LLM and NOT benchmark evidence."""
    output = {f: None for f in SCORE_FIELDS}
    output.update(dieu_kien={}, kieu_gia_tri="khong_neu", trich={}, mac_dinh=[])
    return LLMResult(json.dumps(output, ensure_ascii=False), request["provider"],
                     request["model"], "offline-empty-fixture-v1", {}, "stop")
