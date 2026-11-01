import difflib
import importlib.util
import json
import re
import unicodedata
from pathlib import Path

import pytest

from kiemchung import chia_doan as cd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chia_doan_script", ROOT / "scripts/chia_doan.py")
script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(script)

NGUON = ROOT / "data/nguon"


def doc_that(ma_mau, trang="url"):
    thu_muc = NGUON / ma_mau / ("bo_sung" if trang == "bo_sung" else "")
    van_ban = (thu_muc / "page.txt").read_text(encoding="utf-8")
    ma_html = (thu_muc / "page.html").read_text(encoding="utf-8")
    return cd.chia_doan(van_ban, cd.doc_chu_thich_html(ma_html))


def doan_chua(doan, mau, truong="noi_dung"):
    """Đoạn đầu tiên có `mau` trong trường truong; ký hiệu chú thích ('Wide3') chỉ còn trong noi_dung_goc."""
    mau = cd.GACH_DAC_BIET.sub("-", mau)  # đoạn đã chuẩn hóa ('Wi‑Fi' -> 'Wi-Fi')
    ket_qua = [d for d in doan if mau in d[truong]]
    assert ket_qua, f"không đoạn nào chứa {mau!r}"
    return ket_qua[0]


# --- Apple: số chú thích dính cuối chữ ---

def test_apple_so_dinh_chu_khong_bat_nham_so_lieu():
    assert cd.so_chu_thich_dinh_chu("Pin Và Nguồn Điện5") == [(5, True)]
    assert cd.so_chu_thich_dinh_chu("5G (sub‑6 GHz) với 4x4 MIMO8") == [(8, True)]
    assert cd.so_chu_thich_dinh_chu("Sạc lên đến 50% trong 20 phút6 với bộ tiếp hợp 40W") == [(6, False)]
    for so_lieu in ["Công nghệ ProMotion với tốc độ làm mới thích ứng lên đến 120Hz",
                    "Hệ thống camera 48MP Dual Fusion", "iPhone 17", "Chip A19", "Chip Apple N1",
                    "Bluetooth v5.4", "Phiên bản A3520**"]:
        assert cd.so_chu_thich_dinh_chu(so_lieu) == [], so_lieu


APPLE_CHU_THICH = {
    1: "Dung lượng khả dụng nhỏ hơn và có thể thay đổi do nhiều yếu tố.",
    2: "Kích thước và trọng lượng khác nhau tùy theo cấu hình và quy trình sản xuất.",
    5: "Tất cả các xác nhận về thời lượng pin phụ thuộc vào cấu hình mạng; các kết quả thực tế sẽ khác nhau.",
    6: "Sạc không dây MagSafe lên đến 25W với bộ tiếp hợp nguồn 30W trở lên.",
}
APPLE_VAN_BAN = "\n".join([
    "Dung Lượng Lưu Trữ1", "256GB", "512GB",
    "Kích Thước Và Trọng Lượng2", "Rộng:", "", "71,5 mm", "",
    "Chip", "Chip A19", "Công nghệ ProMotion với tốc độ làm mới thích ứng lên đến 120Hz",
    "Hệ thống camera 48MP Dual Fusion", "Chip Apple N1", "Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét)",
    "Pin Và Nguồn Điện5", "", "Thời gian xem video", "Lên đến 30 giờ", "",
    "Sạc không dây Qi2 lên đến 25W6",
    "Face ID", "Hỗ trợ bởi công nghệ TrueDepth",
    *APPLE_CHU_THICH.values(),
])


def test_apple_gan_chu_thich_dung_so_va_khong_gan_nham():
    doan = cd.chia_doan(APPLE_VAN_BAN, APPLE_CHU_THICH)
    pin = doan_chua(doan, "Lên đến 30 giờ")
    assert APPLE_CHU_THICH[5] in pin["chu_thich"] and APPLE_CHU_THICH[6] in pin["chu_thich"]
    assert APPLE_CHU_THICH[2] not in pin["chu_thich"]  # 'Qi2' là tên mã, không phải chú thích 2
    for mau in ["120Hz", "48MP", "Chip A19", "Chip Apple N1", "IP68"]:
        d = doan_chua(doan, mau)
        assert APPLE_CHU_THICH[1] not in d["chu_thich"] or "Dung Lượng" in d["noi_dung"]
        assert not [c for c in d["chu_thich"] if c in (APPLE_CHU_THICH[5], APPLE_CHU_THICH[6])] or "Pin Và" in d["noi_dung"]
    # Các dòng chú thích đã nằm trong chu_thich, không lặp lại trong nội dung đoạn.
    assert all(APPLE_CHU_THICH[5] not in d["noi_dung"] for d in doan)


def test_chu_thich_html_apple_samsung_va_ol():
    apple = ('<ol><li id="footnote-1" data-footnote="x">Dung lượng&nbsp;khả dụng nhỏ hơn.</li>'
             '<li id="footnote-2" data-footnote="y">Kích thước <a href="#">khác</a> nhau.</li></ol>'
             '<ul><li id="footnote-00">** Số máy.</li></ul>')
    assert cd.doc_chu_thich_html(apple) == {1: "Dung lượng khả dụng nhỏ hơn.", 2: "Kích thước khác nhau."}
    samsung = ('<li role="listitem" data-sup="sup-4"> <span class="text_disclaimer">Blade Lights chỉ có trên Buds3 Pro.</span>'
               '<button type="button"><img alt="Back to Location"></button> </li>'
               '<li data-sup="5"> <span>Có thể cấu hình.<br>Xem Cài đặt.</span> <button>Quay lại Địa điểm</button> </li>')
    assert cd.doc_chu_thich_html(samsung) == {4: "Blade Lights chỉ có trên Buds3 Pro.", 5: "Có thể cấu hình. Xem Cài đặt."}
    ol = "<ol><li>Một.</li><li>Hai.</li><li>Ba.</li></ol><ol><li>x</li></ol>"
    assert cd.doc_chu_thich_html(ol) == {1: "Một.", 2: "Hai.", 3: "Ba."}
    assert cd.doc_chu_thich_html("<p>Không có chú thích</p>") == {}


# --- Xiaomi: dòng dồn và dấu * nối liền ---

XIAOMI_DONG_KICH_THUOC = ("Chiều cao: 163,2mmChiều rộng: 78,0mmĐộ dày: 7,50mmTrọng lượng: 194g*Dữ liệu do Phòng thí nghiệm "
                          "nội bộ của Xiaomi thử nghiệm, kết quả thực tế có thể sẽ khác.")
XIAOMI_CHU_THICH = "Dữ liệu do Phòng thí nghiệm nội bộ của Xiaomi thử nghiệm, kết quả thực tế có thể sẽ khác."


def test_xiaomi_tach_dau_sao_noi_lien():
    con_lai, ky_hieu, noi_lien, ca_dong = cd.tach_dau_sao(XIAOMI_DONG_KICH_THUOC)
    assert con_lai == "Chiều cao: 163,2mmChiều rộng: 78,0mmĐộ dày: 7,50mmTrọng lượng: 194g*"
    assert noi_lien == [("*", XIAOMI_CHU_THICH, len(con_lai) - 1)] and ky_hieu == [] and ca_dong is None
    assert cd.tach_nhan(con_lai) == ["Chiều cao: 163,2mm", "Chiều rộng: 78,0mm", "Độ dày: 7,50mm", "Trọng lượng: 194g*"]


def test_xiaomi_chu_thich_dung_o_cho_nhan_moi():
    dong = "Tốc độ lấy mẫu cảm ứng tức thì 2.560Hz**Kích hoạt trong chế độ Game TurboGam màu: DCI-P3Độ sâu màu: 68 tỷ màu"
    con_lai, _, noi_lien, _ = cd.tach_dau_sao(dong)
    assert [(r, t) for r, t, _ in noi_lien] == [("**", "Kích hoạt trong chế độ Game Turbo")]
    assert con_lai.endswith("2.560Hz**Gam màu: DCI-P3Độ sâu màu: 68 tỷ màu")
    assert con_lai[noi_lien[0][2]] == "*"  # vị trí chỉ đúng dấu * trong chữ còn lại
    # Hai chú thích liền nhau tách ở dấu * kế tiếp; chú thích nhiều câu giữ đến hết dòng.
    _, _, hai, _ = cd.tach_dau_sao("USB-C*Bộ sạc không bao gồm. Máy được khuyến cáo dùng củ 67W.*Cổng USB-C chỉ cho thiết bị số.")
    assert [t for _, t, _ in hai] == ["Bộ sạc không bao gồm. Máy được khuyến cáo dùng củ 67W.", "Cổng USB-C chỉ cho thiết bị số."]
    _, _, ip, _ = cd.tach_dau_sao("IP68**Thiết bị đã được thử nghiệm. Điều kiện: ngâm 3 mét.Vui lòng lưu ý rằng nước muối làm giảm khả năng.")
    assert ip[0][1].endswith("làm giảm khả năng.") and len(ip) == 1
    # '*' mở đầu một cụm chữ trong dòng ('(*Bật AOD)') không phải chú thích: giữ nguyên dòng.
    assert cd.tach_dau_sao("Lên đến 30 giờ (*Bật AOD)") == ("Lên đến 30 giờ (*Bật AOD)", [], [], None)
    # '*' đứng cuối cụm (Apple) là ký hiệu, không mở chú thích.
    dong_apple = "hoặc 1.181.000đ/th. trong 24 tháng.*"
    assert cd.tach_dau_sao(dong_apple) == (dong_apple, [("*", len(dong_apple) - 1)], [], None)


def test_xiaomi_doan_giu_nguyen_con_so_va_chu_thich():
    doan = cd.chia_doan("Kích thước\n" + XIAOMI_DONG_KICH_THUOC + "\nBộ vi xử lý\nMediaTek Dimensity 8400-Ultra")
    kt = doan_chua(doan, "Chiều cao: 163,2mm")
    assert kt["muc"] == "Kích thước" and kt["noi_dung"].startswith("Kích thước\n")
    for mau in ["Chiều rộng: 78,0mm", "Độ dày: 7,50mm", "Trọng lượng: 194g"]:
        assert mau in kt["noi_dung"]  # bốn con số cùng một đoạn với chú thích của chúng
    assert kt["chu_thich"] == [XIAOMI_CHU_THICH] and "Dữ liệu do" not in kt["noi_dung"]
    assert "MediaTek" in "".join(d["noi_dung"] for d in doan)  # tên hãng dính chữ hoa không bị tách


def test_ranh_gioi_khong_cat_don_vi_va_ten_hang():
    assert cd.vi_tri_ranh_gioi("120HzMàn hình phẳng") == []
    assert cd.vi_tri_ranh_gioi("MediaTek MoMo FaceTime Corning® Gorilla®") == []
    assert [i for i, _ in cd.vi_tri_ranh_gioi("Độ dày: 7,50mmTrọng lượng: 194g")] == [14]


# --- Samsung: * ở dòng riêng, số cách chữ, chú thích bị xuống hàng ---

def test_samsung_dau_sao_o_dong_rieng_gan_vao_doan_truoc():
    doan = cd.chia_doan("Điểm Samsung Reward ước tính\n0 p\n*Điểm Samsung Reward tích lũy thực tế có thể khác với ước tính\nHàng không bán")
    assert len(doan) == 1
    assert doan[0]["chu_thich"] == ["Điểm Samsung Reward tích lũy thực tế có thể khác với ước tính"]
    assert "*" not in doan[0]["noi_dung"] and "0 p" in doan[0]["noi_dung"]


SAMSUNG_CHU_THICH = {
    33: "Một số nội dung có thể phải trả thêm phí.",
    34: "Với tính năng bật/tắt ANC, tai nghe và hộp tai nghe cung cấp tối đa 30 giờ phát khi sạc đầy. Dựa trên thử nghiệm nội bộ.",
    35: "IP57 dựa trên các điều kiện thử nghiệm ngâm ở độ sâu 1 mét nước ngọt trong tối đa 30 phút.",
}
SAMSUNG_VAN_BAN = "\n".join([
    "Kết nối liên tục", "",
    "Giữ cho âm nhạc và âm thanh của bạn luôn tuôn chảy, bất cứ khi nào và bất cứ nơi nào bạn đi. 33, 34, 35", "",
    "Thời gian phát", "Tắt Tính năng ANC", "Đến", "7", "/", "30", "giờ",
    "BẬT Tính năng ANC", "Đến", "6", "/", "26", "giờ", "Bluetooth", "V", "5,4", "",
    SAMSUNG_CHU_THICH[33],
    # Chú thích 34 bị xuống hàng thành hai dòng nên không thể đánh số theo vị trí.
    "Với tính năng bật/tắt ANC, tai nghe và hộp tai nghe cung cấp tối đa 30 giờ phát khi sạc đầy.",
    "Dựa trên thử nghiệm nội bộ.",
    SAMSUNG_CHU_THICH[35],
])


def test_samsung_so_lieu_va_chu_thich_dieu_kien_cung_doan():
    doan = cd.chia_doan(SAMSUNG_VAN_BAN, SAMSUNG_CHU_THICH)
    d = doan_chua(doan, "Tắt Tính năng ANC")
    assert d["muc"] == "Kết nối liên tục"
    for mau in ["Đến\n7\n/\n30\ngiờ", "Đến\n6\n/\n26\ngiờ"]:
        assert mau in d["noi_dung"]  # 7/30 giờ nằm cùng đoạn với chú thích điều kiện ANC
    assert SAMSUNG_CHU_THICH[34] in d["chu_thich"]
    assert SAMSUNG_CHU_THICH[33] in d["chu_thich"] and SAMSUNG_CHU_THICH[35] in d["chu_thich"]
    assert cd.so_chu_thich_cach_chu("Thiết kế ấn tượng hoàn toàn mới 1, 4, 5") == [1, 4, 5]
    assert cd.so_chu_thich_cach_chu("Hệ số 4,35") == [] and cd.so_chu_thich_cach_chu("Bluetooth 6") == []
    # Cùng kiểu nhóm số cuối dòng: sau dấu kết câu có khoảng trắng (một số hoặc danh sách), hoặc dính sau dấu câu.
    assert cd.so_chu_thich_cach_chu("ngày dài đầy năng lượng! 7") == [7]
    assert cd.so_chu_thich_cach_chu("Nhanh hơn, tiện hơn, dễ dàng hơn. 10") == [10]
    assert cd.so_chu_thich_cach_chu("ngủ cá nhân hóa. 2,5") == [2, 5]
    assert cd.so_chu_thich_cach_chu("hoạt động hàng ngày.4,32") == [4, 32]
    assert cd.so_chu_thich_cach_chu("thiết kế đệm đẹp mắt. 40, 41, 42 43, 44") == [40, 41, 42, 43, 44]  # hai cụm liền nhau
    assert cd.so_chu_thich_cach_chu("Pin chạy 31 giờ 4,35") == [] and cd.so_chu_thich_cach_chu("Galaxy Watch7") == []


def test_ky_hieu_khong_tim_duoc_noi_dung_duoc_dem():
    van_ban = ("Tiêu đề lớn\nGiữ cho âm nhạc luôn tuôn chảy, bất cứ khi nào bạn đi. 33, 34\n"
               + SAMSUNG_CHU_THICH[33] + "\n" + SAMSUNG_CHU_THICH[35])
    doan, thong_ke = cd.chia_doan_day_du(van_ban, {33: SAMSUNG_CHU_THICH[33], 35: SAMSUNG_CHU_THICH[35]})
    assert thong_ke["ky_hieu"] == 2 and thong_ke["khong_tim_duoc"] == ["34"]
    assert thong_ke["khong_duoc_dan"] == [35]  # 35 có trong trang nhưng không ký hiệu nào dẫn tới
    assert [d["muc"] for d in doan].count("Chú thích") == 1  # ... nên thành đoạn riêng


# --- Ký hiệu sau dấu câu, không đúng thứ tự xuất hiện (ca OPPO và S25 Ultra, sửa lần 2) ---

OPPO_VAN_BAN = "\n".join([
    "Pin Silicon-carbon OPPO",
    "Khai mở sức mạnh và hiệu năng vô song với công nghệ silicon-carbon cho điện cực dương. Lo gì hết pin, "
    "tự tin trải nghiệm ngày dài đầy năng lượng! 7",
    "5630mAh", "Dung lượng tiêu chuẩn", "12%", "Dung lượng cải thiện8",
    "Siêu Sạc Nhanh SuperVOOCTM", "80W và AirVOOCTM 50W",
    "Mở ra kỷ nguyên sạc nhanh bất kể có dây hay không dây. Nhanh hơn, tiện hơn, dễ dàng hơn. 10",
    "Lưu Ý:",
    "7. 5.630mAh là giá trị tiêu chuẩn của dung lượng pin. Giá trị định mức của dung lượng pin là 5.490mAh.",
    "8. Thay đổi so với OPPO Find X7.",
    "10. Khi điện áp đầu vào là 200-240V, công suất đầu ra tối đa là 80W.",
])


def test_oppo_so_sau_dau_cham_phu_ca_khoi_so_lieu_di_sau():
    doan = cd.chia_doan(OPPO_VAN_BAN)
    pin = doan_chua(doan, "5630mAh")
    assert pin["chu_thich"][0].startswith("5.630mAh là giá trị tiêu chuẩn") and "5.490mAh" in pin["chu_thich"][0]
    assert any(c.startswith("Thay đổi so với OPPO Find X7") for c in pin["chu_thich"])  # 'cải thiện8' dính chữ
    sac = doan_chua(doan, "80W và AirVOOCTM 50W")
    assert any(c.startswith("Khi điện áp đầu vào là 200-240V") for c in sac["chu_thich"])
    assert not [d for d in doan if d["muc"] == "Chú thích"]  # không chú thích nào bị bỏ rơi


def test_that_oppo_bo_sung_5630mah_va_80w():
    doan = doc_that("dt-oppo-findx8", "bo_sung")
    pin = doan_chua(doan, "5630mAh\nDung lượng tiêu chuẩn")
    assert any(c.startswith("5.630mAh là giá trị tiêu chuẩn") for c in pin["chu_thich"])
    sac = doan_chua(doan, "80W và AirVOOCTM 50W")
    assert any(c.startswith("Khi điện áp đầu vào là 200-240V") for c in sac["chu_thich"])


S25_CHU_THICH = {1: "Gemini là nhãn hiệu của Google LLC.", 2: "Kết quả có thể khác nhau tùy điều kiện chụp.",
                 3: "So sánh với các sản phẩm trước đó.", 4: "Dựa trên các điều kiện kiểm tra trong phòng thí nghiệm."}


def test_s25_so_dinh_chu_cuoi_dong_khong_theo_thu_tu():
    van_ban = "\n".join([
        "Chỉ cần nhấn và ra lệnh là xong1",
        "Thời lượng pin vượt trội4",
        "Chụp bởi Galaxy S25 Ultra #withGalaxy",
        "Chi tiết sắc nét nhất từ Wide đến Tele và thậm chí là Ultra Wide3",
        "UW Macro", "Tập trung vào vẻ đẹp phi thường từ những điều giản dị và ghi lại từng chi tiết với độ chính xác cao.",
        "Galaxy Watch7",  # tên máy cuối dòng: không phải ký hiệu
        *S25_CHU_THICH.values()])
    doan = cd.chia_doan(van_ban, S25_CHU_THICH)
    wide = doan_chua(doan, "Ultra Wide3", "noi_dung_goc")
    assert S25_CHU_THICH[3] in wide["chu_thich"] and wide["noi_dung"].endswith("là Ultra Wide")  # ký hiệu 3 bị bỏ khỏi noi_dung
    # chú thích 1, 3, 4 đều có ký hiệu dẫn tới; chỉ chú thích 2 (không ai nhắc) thành đoạn riêng
    assert [d["noi_dung"].split("\n")[0] for d in doan if d["muc"] == "Chú thích"] == ["Chú thích 2"]


def test_that_s25_ultra_wide3():
    doan = doc_that("dt-samsung-galaxys25ultra", "bo_sung")
    wide = doan_chua(doan, "thậm chí là Ultra Wide3", "noi_dung_goc")
    assert any(c.startswith("So sánh với các sản phẩm trước đó") for c in wide["chu_thich"])


def test_noi_long_thu_tu_khong_bat_nham_so_lieu_va_ten_ma():
    chu_thich = {k: f"Chú thích số {k} nói về điều kiện kiểm tra." for k in range(1, 8)}
    dong_vi_du = [
        "Các định dạng được hỗ trợ bao gồm HEVC, H.264 và AV1",          # AV1: tên chuẩn, 1 là chú thích có thật
        "OPPO Enco Buds3",                                                # tên máy cuối dòng
        "Galaxy Watch7",
        "Sạc không dây Qi2 lên đến 25W và HDR với Dolby Vision, HDR10+/HDR10, và HLG",  # tên mã giữa dòng
        "Pin chạy liên tục 31 giờ 4,35",                                  # số thập phân
        "Bluetooth 6", "Wi‑Fi 7 (802.11be) với 2x2 MIMO", "Chip A19", "iPhone 17",
    ]
    doan = cd.chia_doan("\n".join(["Chỉ cần nhấn và ra lệnh là xong3", *dong_vi_du, *chu_thich.values()]), chu_thich)
    for dong in dong_vi_du:
        d = doan_chua(doan, dong)
        assert chu_thich[3] not in d["chu_thich"] or "xong3" in d["noi_dung_goc"]
        assert not [c for c in d["chu_thich"] if c != chu_thich[3]], (dong, d["chu_thich"])
    assert cd.so_ke_tiep_cuoi_dong("Chip Apple Ultra Wideband thế hệ thứ 210", 10, chu_thich | {10: "x"}) == [(10, 40)]
    assert cd.so_ke_tiep_cuoi_dong("Galaxy S24 Ultra 512", 7, chu_thich) == []  # 12 không phải số kế tiếp (7)
    assert cd.so_ke_tiep_cuoi_dong("Phiên bản 2024", 24, {24: "x"}) == []  # năm 4 chữ số


def test_chu_thich_le_giua_trang_gan_vao_phan_phia_tren():
    van_ban = "\n".join(["Bộ sưu tập Gold Collection 5", "Nét thẩm mỹ hài hòa, toát lên sự cao cấp", "Tìm hiểu thêm",
                         "5. Các sản phẩm khác trong Bộ sưu tập Gold Collection được bán riêng.", "Màn hình hàng đầu phân khúc"])
    doan, thong_ke = cd.chia_doan_day_du(van_ban)
    assert thong_ke["gan_theo_vi_tri"] == [5] and thong_ke["khong_duoc_dan"] == []
    gold = doan_chua(doan, "Gold Collection 5")
    assert gold["chu_thich"] == ["Các sản phẩm khác trong Bộ sưu tập Gold Collection được bán riêng."]


def test_so_hien_thi_cua_chu_thich_lay_tu_lien_ket_ky_hieu():
    ma_html = ('<p>Video.<sup><a href="#d" data-sup-tag="sup-58">56</a></sup> <a data-sup-tag="sup-59">57</a></p>'
               '<li class="x" data-sup="sup-55"><span>Chú thích 55.</span></li>'
               '<li class="x" data-sup="sup-58"><span>Video mô phỏng.</span></li>'
               '<li class="x" data-sup="sup-59"><span>UX thực tế khác.</span></li>')
    assert cd.nhan_hien_thi_html(ma_html) == {58: 56, 59: 57}
    assert cd.doc_chu_thich_html(ma_html) == {55: "Chú thích 55.", 56: "Video mô phỏng.", 57: "UX thực tế khác."}


def test_that_chu_thich_khong_duoc_dan_tren_tap_phat_trien():
    for ma_mau, trang, con_lai in [("dt-apple-iphone17", "url", []), ("dh-apple-watchse3", "url", []),
                                   ("tn-samsung-buds3pro", "url", []),
                                   ("dt-xiaomi-15t", "bo_sung", [1, 2, 12])]:  # 3 ký hiệu ẩn: không có trong page.txt/html
        thu_muc = NGUON / ma_mau / ("bo_sung" if trang == "bo_sung" else "")
        van_ban = (thu_muc / "page.txt").read_text(encoding="utf-8")
        bang = cd.doc_chu_thich_html((thu_muc / "page.html").read_text(encoding="utf-8"))
        _, thong_ke = cd.chia_doan_day_du(van_ban, bang)
        assert thong_ke["khong_duoc_dan"] == con_lai, ma_mau
    doan = doc_that("dt-apple-iphone17")
    thu_2 = doan_chua(doan, "thế hệ thứ 210", "noi_dung_goc")
    assert any("Ultra Wideband chỉ khả dụng" in c for c in thu_2["chu_thich"])
    assert "thế hệ thứ 2\n" in thu_2["noi_dung"]  # số 2 của 'thế hệ thứ 2' ở lại, ký hiệu 10 bị bỏ
    assert not any(c.startswith("Dung lượng khả dụng") for c in doan_chua(doan, "HEVC, H.264 và AV1")["chu_thich"])
    buds = doc_that("tn-samsung-buds3pro")  # Samsung đánh số hiển thị 56-59 cho mã 58-61 trong thẻ
    nhanh = doan_chua(buds, "bảng cài đặt nhanh khi ứng dụng đang phát nội dung")
    assert any(c.startswith("Video được mô phỏng") for c in nhanh["chu_thich"])
    assert any(c.startswith("Có trên các thiết bị Samsung Galaxy") for c in nhanh["chu_thich"])


# --- Xiaomi bổ sung: chú thích có số ghi sẵn trong văn bản ---

def test_chu_thich_co_so_ghi_san_trong_van_ban():
    van_ban = "\n".join(["Tần số quét1", "120Hz", "Thời lượng pin hàng đầu", "1600 chu kỳ sạc2", "",
                         "Lưu ý:", "1. Màn hình hỗ trợ tần số quét tối đa 120Hz.", "2. Pin vẫn giữ được mức dung lượng ≥80% sau 1600 chu kỳ sạc."])
    doan = cd.chia_doan(van_ban)
    tan_so = doan_chua(doan, "120Hz")
    assert "Màn hình hỗ trợ tần số quét tối đa 120Hz." in tan_so["chu_thich"]
    pin = doan_chua(doan, "1600 chu kỳ")
    assert "Pin vẫn giữ được" in pin["chu_thich"][-1]
    assert all("Lưu ý" not in d["noi_dung"] and "1. " not in d["noi_dung"] for d in doan)


def test_chu_thich_chua_dan_toi_van_con_trong_tai_lieu():
    doan = cd.chia_doan("Màn hình 6,83 inch\n7. Chú thích không ai nhắc tới.\n8. Chú thích thứ hai cũng thế.")
    chu_thich = [d for d in doan if d["muc"] == "Chú thích"]
    assert len(chu_thich) == 2 and "Chú thích không ai nhắc tới" in chu_thich[0]["noi_dung"]


# --- PDF: dòng phân trang và chữ có tab ---

PDF = "\n".join(["=== Trang 1 ===", "HƯỚNG DẪN NGƯỜI", "DÙNG", "", "=== Trang 2 ===",
                 "Nhập\tthông\ttin\tv ề \t chu \t kỳ", "1 Chạm vào Theo dõi chu kỳ.", "2 Chạm vào Nhập kỳ kinh.", "",
                 "=== Trang 3 ===", "Thời lượng pin 7 giờ khi dùng bình thường.", "*"])


def test_pdf_ngat_doan_o_dong_phan_trang():
    doan = cd.chia_doan(PDF)
    assert all("===" not in d["noi_dung"] for d in doan)
    assert [d["dong"] for d in doan] == [[2, 3], [6, 8], [11, 11]]  # không đoạn nào bắc ngang hai trang
    assert doan[1]["noi_dung"].startswith("Nhập thông tin v ề chu kỳ")  # tab -> khoảng trắng
    assert all(d["chu_thich"] == [] for d in doan)  # PDF không có chú thích kiểu trang web


def test_dong_trong_va_dong_lap_bi_bo_nhung_giu_dau_gach_cheo():
    dong = cd.doc_dong("A1\n\n   \n•\nA1\nA1\nPlay\nĐến\n/\n30")
    assert [(d.so, d.chu) for d in dong] == [(1, "A1"), (8, "Đến"), (9, "/"), (10, "30")]


def test_lam_sach_chuan_hoa_nfc_gach_noi_va_ky_tu_an():
    nfd = unicodedata.normalize("NFD", "Nhiệt độ")
    assert nfd != "Nhiệt độ"
    assert cd.lam_sach(nfd) == "Nhiệt độ"
    assert cd.lam_sach("5G (sub‑6 GHz)") == "5G (sub-6 GHz)"
    assert cd.lam_sach("Pin­​ 5000 mAh") == "Pin 5000 mAh"


# --- Mã đoạn ---

def test_danh_ma_doan_lien_tuc_giua_cac_trang():
    d = {"muc": "Pin", "noi_dung": "Pin\nLên đến 7 giờ", "noi_dung_goc": "Pin\nLên đến 7 giờ1", "chu_thich": [], "dong": [1, 2],
         "ky_hieu_bo": []}
    ket_qua = cd.danh_ma_doan("tn-samsung-buds3pro", [("url", [d, d]), ("bo_sung", [d])])
    assert [x["id"] for x in ket_qua] == ["tn-samsung-buds3pro#001", "tn-samsung-buds3pro#002", "tn-samsung-buds3pro#003"]
    assert [x["trang"] for x in ket_qua] == ["url", "url", "bo_sung"]
    assert set(ket_qua[0]) == {"id", "ma_mau", "trang", "muc", "noi_dung", "noi_dung_goc", "chu_thich", "dong", "ky_hieu_bo"}
    assert ket_qua[0]["noi_dung_goc"] == "Pin\nLên đến 7 giờ1"  # ky_hieu_bo chỉ là nhật ký, không ghi vào doan.jsonl
    assert cd.danh_ma_doan("m", [("url", [d])], 4)[0]["id"] == "m#0001"
    assert script.so_chu_so_ma(999) == 3 and script.so_chu_so_ma(1000) == 4


# --- Trên trang thật của 4 mẫu tập phát triển ---

def test_that_iphone17_pin_va_dieu_kien_sac():
    doan = doc_that("dt-apple-iphone17")
    pin = doan_chua(doan, "Thời gian xem video\nLên đến 30 giờ")
    assert any(c.startswith("Tất cả các xác nhận về thời lượng pin") for c in pin["chu_thich"])
    assert any(c.startswith("Sạc không dây MagSafe lên đến 25W") for c in pin["chu_thich"])
    assert doan_chua(doan, "Công nghệ ProMotion")["chu_thich"] == []  # 120Hz không có chú thích
    chip = doan_chua(doan, "Chip A19")
    assert not any("Ultra Wideband" in c for c in chip["chu_thich"])


def test_that_watch_se3_thoi_luong_pin():
    doan = doc_that("dh-apple-watchse3")
    pin = doan_chua(doan, "Pin dùng cả ngày, lên đến 18 giờ")
    assert any(c.startswith("Thời lượng pin cả ngày được tính dựa trên") for c in pin["chu_thich"])
    assert not any("Thời lượng pin" in c for c in doan_chua(doan, "Chip S10")["chu_thich"])  # S10 là tên chip


def test_that_xiaomi_15t_kich_thuoc_va_man_hinh():
    doan = doc_that("dt-xiaomi-15t")
    kt = doan_chua(doan, "Trọng lượng: 194g")
    assert "Chiều cao: 163,2mm" in kt["noi_dung"]
    assert any(c.startswith("Dữ liệu do Phòng thí nghiệm nội bộ") for c in kt["chu_thich"])
    ip = doan_chua(doan, "IP68")
    assert ip["chu_thich"] and ip["chu_thich"][0].startswith("Thiết bị đã được thử nghiệm")
    assert not any("**" in d["noi_dung"] and not d["chu_thich"] for d in doan)  # ký hiệu * nào cũng có chú thích đi kèm


def test_that_samsung_buds3_pro_thoi_gian_phat_va_chu_thich_30_gio():
    doan = doc_that("tn-samsung-buds3pro")
    d = doan_chua(doan, "Tắt Tính năng ANC\nĐến\n7\n/\n30\ngiờ")
    assert "BẬT Tính năng ANC\nĐến\n6\n/\n26\ngiờ" in d["noi_dung"]
    assert any(c.startswith("Với tính năng bật/tắt ANC, tai nghe và hộp tai nghe cung cấp tối đa 30 giờ") for c in d["chu_thich"])
    reward = doan_chua(doan, "0 p")
    assert any(c.startswith("Điểm Samsung Reward tích lũy thực tế") for c in reward["chu_thich"])


@pytest.mark.parametrize("ma_mau,trang", [("dt-apple-iphone17", "url"), ("dt-xiaomi-15t", "url"), ("dt-xiaomi-15t", "bo_sung"),
                                          ("tn-samsung-buds3pro", "url"), ("dh-apple-watchse3", "url")])
def test_that_moi_doan_bat_dau_bang_ten_muc_va_dong_hop_le(ma_mau, trang):
    thu_muc = NGUON / ma_mau / ("bo_sung" if trang == "bo_sung" else "")
    so_dong = len((thu_muc / "page.txt").read_text(encoding="utf-8").split("\n"))
    doan = doc_that(ma_mau, trang)
    assert doan
    for d in doan:
        assert d["noi_dung_goc"].startswith(d["muc"])  # muc giữ nguyên, có thể còn ký hiệu cuối ('Định nghĩa lại âm thanh nguyên bản 1')
        assert 1 <= d["dong"][0] <= d["dong"][1] <= so_dong
        assert len(d["noi_dung_goc"]) <= cd.CAP_CUNG and len(d["noi_dung"]) <= len(d["noi_dung_goc"])


# --- Script: ghi tệp, thống kê, mẫu kiểm ---

def test_chia_mot_mau_va_ghi_jsonl_on_dinh(tmp_path):
    row = {r["ma_mau"]: r for r in script.doc_mau()}["tn-samsung-buds3pro"]
    theo_trang, tk = script.chia_mot_mau(row)
    assert [t for t, _ in theo_trang] == ["url"]
    assert tk["khong_tim_duoc"] == [] and tk["khong_duoc_dan"] == [] and tk["khong_co_trong_txt"] == []
    doan = cd.danh_ma_doan(row["ma_mau"], theo_trang)
    dich = tmp_path / "doan.jsonl"
    script.ghi_jsonl(dich, doan)
    tho = dich.read_bytes()
    assert b"\r" not in tho and tho.endswith(b"\n") and "Tắt Tính năng ANC".encode() in tho  # LF, không escape \uXXXX
    doc_lai = [json.loads(dong) for dong in tho.decode("utf-8").splitlines()]
    assert doc_lai == [{k: d[k] for k in script.TRUONG_JSONL} for d in doan] and doc_lai[0]["id"] == "tn-samsung-buds3pro#001"
    assert "ky_hieu_bo" not in doc_lai[0]  # nhật ký chỉ để báo cáo, không ghi vào doan.jsonl
    script.ghi_jsonl(tmp_path / "lan2.jsonl", cd.danh_ma_doan(row["ma_mau"], script.chia_mot_mau(row)[0]))
    assert (tmp_path / "lan2.jsonl").read_bytes() == tho  # chạy lại ra đúng từng byte


def test_trang_cua_mau_theo_url_bo_sung(tmp_path):
    cua_url = {"ma_mau": "a", "url_bo_sung": ""}
    assert script.trang_cua_mau(cua_url, tmp_path) == [("url", tmp_path / "a")]
    assert script.trang_cua_mau({"ma_mau": "b", "url_bo_sung": "https://x/"}, tmp_path) == [
        ("url", tmp_path / "b"), ("bo_sung", tmp_path / "b" / "bo_sung")]


def test_lay_mau_kiem_co_dinh_seed_va_uu_tien_chu_so():
    doan = [{"id": f"m{i % 3}#{i:03d}", "ma_mau": f"m{i % 3}", "trang": "url", "muc": "", "chu_thich": [], "dong": [1, 2],
             "noi_dung": ("Pin 7 giờ" if i % 2 else "Màu bạc")} for i in range(60)]
    mau, so_co_so = script.lay_mau_kiem(doan, 20, 5)
    assert len(mau) == 20 and so_co_so == 30
    assert mau == script.lay_mau_kiem(doan, 20, 5)[0] != script.lay_mau_kiem(doan, 20, 6)[0]
    assert {d["ma_mau"] for d in mau} == {"m0", "m1", "m2"} and all(any(c.isdigit() for c in d["noi_dung"]) for d in mau)
    assert "Seed: 5" in script.viet_kiem_md(mau, so_co_so, 60, 5)


# --- Bỏ ký hiệu chú thích khỏi noi_dung, giữ noi_dung_goc (31/10/2026) ---

def khoang(chu, ky_hieu, loai=cd.KY_HIEU_SO, so=()):
    """KhoangBo bao đúng `ky_hieu` đầu tiên tìm thấy trong chu."""
    a = chu.index(ky_hieu)
    return cd.KhoangBo(a, a + len(ky_hieu), loai, tuple(so))


def test_bo_ky_hieu_giua_hai_tu_van_con_mot_khoang_trang():
    chu = "Sạc lên đến 50% trong 20 phút6 với bộ tiếp hợp 40W trở lên"
    moi, nhat_ky = cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "6", so=[6])])
    assert moi == "Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên"
    a = chu.index("6")
    assert nhat_ky == [{"vi_tri": a, "vi_tri_moi": a, "chu": "6", "loai": "so", "so": [6], "thieu": [], "xu_ly": ""}]
    chu = "Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp8"  # dính cuối chữ ở cuối dòng
    assert cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "8", so=[8])])[0] == "Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp"
    chu = "Rộng: 7,5 mm\nLên đến 30 giờ1\nMàu"  # ký hiệu cuối một dòng giữa đoạn: dòng sau giữ nguyên
    assert cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "1", so=[1])])[0] == "Rộng: 7,5 mm\nLên đến 30 giờ\nMàu"


def test_bo_ky_hieu_cuoi_dong_sau_khoang_trang_bo_luon_khoang_trang_do():
    chu = "tự tin trải nghiệm ngày dài đầy năng lượng! 7\n5630mAh"
    moi, nhat_ky = cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "7", so=[7])])
    assert moi == "tự tin trải nghiệm ngày dài đầy năng lượng!\n5630mAh" and nhat_ky[0]["xu_ly"] == "bo_cach_truoc"
    chu = "thiết kế đệm đẹp mắt. 40, 41, 42 43, 44"  # cả cụm nhiều số là một chỗ bỏ
    cum = cd.KhoangBo(chu.index("40"), len(chu), cd.KY_HIEU_SO, (40, 41, 42, 43, 44))
    assert cd.bo_ky_hieu_chu_thich(chu, [cum])[0] == "thiết kế đệm đẹp mắt."
    chu = "ghi lại chính xác.4,32"  # dính ngay sau dấu chấm
    assert cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "4,32", so=[4, 32])])[0] == "ghi lại chính xác."


def test_bo_ky_hieu_dinh_chu_sau_thi_chen_mot_khoang_trang_va_ghi_lai():
    chu = "tức thì 2.560Hz**Gam màu: DCI-P3"
    moi, nhat_ky = cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "**", cd.KY_HIEU_SAO_NOI_LIEN)])
    assert moi == "tức thì 2.560Hz Gam màu: DCI-P3" and nhat_ky[0]["xu_ly"] == "chen_cach"
    assert moi[:nhat_ky[0]["vi_tri_moi"]] == "tức thì 2.560Hz "
    chu = "Gemini***Hệ thống"  # ba dấu liền nhau là một chỗ bỏ, chỉ chèn một khoảng trắng
    a = chu.index("*")
    moi, nhat_ky = cd.bo_ky_hieu_chu_thich(chu, [cd.KhoangBo(a + i, a + i + 1, cd.KY_HIEU_SAO_NOI_LIEN) for i in range(3)])
    assert moi == "Gemini Hệ thống" and [x["xu_ly"] for x in nhat_ky] == ["chen_cach", "", ""]
    chu = "Trọng lượng: 194g*"  # cuối chuỗi: không có gì để chèn
    assert cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "*", cd.KY_HIEU_SAO_NOI_LIEN)])[0] == "Trọng lượng: 194g"


def test_bo_ky_hieu_giua_hai_khoang_trang_va_truoc_dau_cau():
    chu = "pin 8 giờ"
    moi, nhat_ky = cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "8", so=[8])])
    assert moi == "pin giờ" and nhat_ky[0]["xu_ly"] == "bo_cach_sau"
    chu = "ra lệnh là xong 6."
    assert cd.bo_ky_hieu_chu_thich(chu, [khoang(chu, "6", so=[6])])[0] == "ra lệnh là xong."
    assert cd.bo_ky_hieu_chu_thich("không có ký hiệu", []) == ("không có ký hiệu", [])


BO_CHU_THICH = {
    1: "Dung lượng khả dụng nhỏ hơn và có thể thay đổi do nhiều yếu tố.",
    4: "Tất cả các xác nhận về thời lượng pin phụ thuộc vào cấu hình mạng.",
    6: "Sạc 50% đo với bộ tiếp hợp 40W trở lên được bán riêng.",
    8: "Chế Độ Nguồn Điện Thấp bao gồm cả theo dõi giấc ngủ.",
}
BO_VAN_BAN = "\n".join([
    "Dung Lượng Lưu Trữ1", "256GB", "512GB",
    "Pin Và Nguồn Điện4", "", "Thời gian xem video", "Lên đến 30 giờ", "",
    "Sạc lên đến 50% trong 20 phút6 với bộ tiếp hợp 40W trở lên (được bán riêng) sử dụng cáp sạc USB‑C",
    "Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp8",
    "Kết Nối", "Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét)", "Chip Apple A2305", "Pin 5.000mAh", "Galaxy Buds3 Pro",
    *BO_CHU_THICH.values(),
])


def test_bo_so_chu_thich_khoi_noi_dung_va_giu_ma_va_so_lieu():
    doan = cd.chia_doan(BO_VAN_BAN, BO_CHU_THICH)
    sac = doan_chua(doan, "Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W")
    assert "20 phút6 với" in sac["noi_dung_goc"] and "phút6" not in sac["noi_dung"]
    assert sac["noi_dung"].endswith("Chế Độ Nguồn Điện Thấp") and sac["noi_dung_goc"].endswith("Chế Độ Nguồn Điện Thấp8")
    assert "USB-C" in sac["noi_dung"] and BO_CHU_THICH[6] in sac["chu_thich"] and BO_CHU_THICH[8] in sac["chu_thich"]
    luu_tru = doan_chua(doan, "Dung Lượng Lưu Trữ\n256GB")  # tiêu đề cũng bỏ số: 'Lưu Trữ1' -> 'Lưu Trữ'
    assert luu_tru["noi_dung_goc"].startswith("Dung Lượng Lưu Trữ1\n") and BO_CHU_THICH[1] in luu_tru["chu_thich"]
    # Tên mã và số liệu không phải ký hiệu nên còn nguyên ở cả hai trường.
    ket_noi = doan_chua(doan, "Đạt mức IP68 (chống nước ở độ sâu tối đa 6 mét)")
    for chu in ["IP68", "6 mét", "Chip Apple A2305", "Pin 5.000mAh", "Galaxy Buds3 Pro"]:
        assert chu in ket_noi["noi_dung"] and chu in ket_noi["noi_dung_goc"], chu
    # Chỉ khác nhau ở ký hiệu: bỏ chúng khỏi noi_dung_goc (theo nhật ký) ra đúng noi_dung.
    for d in doan:
        con_lai, dau = [], 0
        for x in sorted(d["ky_hieu_bo"], key=lambda x: x["vi_tri"]):
            assert d["noi_dung_goc"][x["vi_tri"]:x["vi_tri"] + len(x["chu"])] == x["chu"]
            con_lai.append(d["noi_dung_goc"][dau:x["vi_tri"]])
            dau = x["vi_tri"] + len(x["chu"])
        con_lai.append(d["noi_dung_goc"][dau:])
        assert "".join("".join(con_lai).split()) == "".join(d["noi_dung"].split())
    so_bo = sorted(k for d in doan for x in d["ky_hieu_bo"] for k in x["so"])
    assert so_bo == [1, 4, 6, 8]  # đúng bốn ký hiệu, không bỏ nhầm 68, 3, 2305, 5.000


def test_dau_sao_khong_co_chu_thich_hoac_dung_rieng_khong_bi_bo():
    van_ban = "\n".join(["Chống nước", "Đạt chuẩn IP68* hàng đầu", "Chú thích * biểu tượng", "Đánh giá 5* cho sản phẩm",
                         "*Thử nghiệm trong phòng thí nghiệm."])
    doan = cd.chia_doan(van_ban)
    chu = "\n".join(d["noi_dung"] for d in doan)
    assert "IP68 hàng đầu" in chu  # có dòng chú thích bắt đầu bằng '*' nên '*' sau IP68 là ký hiệu
    assert "Chú thích * biểu tượng" in chu  # đứng riêng giữa hai khoảng trắng: nhãn đọc màn hình, không phải ký hiệu
    assert "IP68* hàng đầu" in "\n".join(d["noi_dung_goc"] for d in doan)
    khong_chu_thich = cd.chia_doan("Đánh giá 5* cho sản phẩm\nMàu sắc")  # trang không có chú thích '*': giữ nguyên
    assert "5* cho" in khong_chu_thich[0]["noi_dung"] and khong_chu_thich[0]["ky_hieu_bo"] == []


def test_ky_hieu_da_nhan_ra_ma_khong_co_khoang_bo_la_loi_chu_khong_bo_sot(monkeypatch):
    van_ban = "\n".join(["Kết nối liên tục", "Thiết kế ấn tượng hoàn toàn mới 1, 4, 5", "Một.", "Hai.", "Ba.", "Bốn.", "Năm."])
    chu_thich = {1: "Một.", 2: "Hai.", 3: "Ba.", 4: "Bốn.", 5: "Năm."}
    doan = cd.chia_doan(van_ban, chu_thich)
    assert doan[0]["noi_dung"] == "Kết nối liên tục\nThiết kế ấn tượng hoàn toàn mới"  # nhóm số cuối dòng bỏ cả cụm
    # Nếu ký hiệu đã nhận ra mà không có khoảng để bỏ thì phải báo lỗi, không lặng lẽ để lại trong noi_dung.
    monkeypatch.setattr(cd, "khoang_nhom_cuoi", lambda chu, bat_dau, so_lon_nhat: [])
    with pytest.raises(ValueError, match="không khớp với khoảng cần bỏ"):
        cd.chia_doan(van_ban, chu_thich)


# --- doan.jsonl thật: có noi_dung_goc, và chỉ khác noi_dung ở ký hiệu chú thích ---

MA_MAU_THAT = sorted(p.parent.name for p in NGUON.glob("*/doan.jsonl"))
SO_DOAN_THAT = 1245  # tổng số đoạn của 12 mẫu (Bước 7), không đổi khi bỏ ký hiệu


def doc_doan_that(ma_mau):
    return [json.loads(d) for d in (NGUON / ma_mau / "doan.jsonl").read_text(encoding="utf-8").splitlines()]


def test_that_doan_jsonl_co_du_12_mau_va_so_doan_khong_doi():
    assert len(MA_MAU_THAT) == 12
    assert sum(len(doc_doan_that(ma)) for ma in MA_MAU_THAT) == SO_DOAN_THAT


@pytest.mark.parametrize("ma_mau", MA_MAU_THAT)
def test_that_doan_jsonl_khop_ban_sinh_lai_tung_byte(ma_mau, tmp_path):
    row = {r["ma_mau"]: r for r in script.doc_mau()}[ma_mau]
    script.ghi_jsonl(tmp_path / "doan.jsonl", cd.danh_ma_doan(ma_mau, script.chia_mot_mau(row)[0]))
    assert (tmp_path / "doan.jsonl").read_bytes() == (NGUON / ma_mau / "doan.jsonl").read_bytes()


def test_that_noi_dung_goc_chi_khac_noi_dung_o_ky_hieu_chu_thich():
    so_doi = 0
    for ma_mau in MA_MAU_THAT:
        for d in doc_doan_that(ma_mau):
            assert isinstance(d["noi_dung_goc"], str) and d["noi_dung_goc"], d["id"]
            goc, nd = d["noi_dung_goc"], d["noi_dung"]
            if goc == nd:
                continue
            so_doi += 1
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, goc, nd, autojunk=False).get_opcodes():
                if tag != "equal":
                    # chỗ khác chỉ là số, dấu phẩy, dấu * (và khoảng trắng đi kèm); chỗ chèn chỉ là một khoảng trắng
                    assert re.fullmatch(r"[\d,\s*]+", goc[i1:i2]) and nd[j1:j2] in ("", " "), (d["id"], goc[i1:i2], nd[j1:j2])
    assert so_doi == 190  # 184 đoạn đổi nhờ nhận diện, thêm 6 đoạn nhờ bảng ghi tay


def test_that_cac_ca_ky_hieu_va_cac_ca_khong_phai_ky_hieu():
    iphone = doc_doan_that("dt-apple-iphone17")
    sac = next(d for d in iphone if "Sạc lên đến 50% trong 20 phút" in d["noi_dung_goc"])
    assert "Sạc lên đến 50% trong 20 phút với bộ tiếp hợp 40W trở lên" in sac["noi_dung"]
    assert "Sạc lên đến 50% trong 20 phút6 với bộ tiếp hợp 40W trở lên" in sac["noi_dung_goc"]
    watch = next(d for d in doc_doan_that("dh-apple-watchse3") if "Chế Độ Nguồn Điện Thấp8" in d["noi_dung_goc"])
    assert "Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp\n" in watch["noi_dung"]
    xiaomi = "\n".join(d["noi_dung"] for d in doc_doan_that("dt-xiaomi-15t"))
    assert "50 phút sạc đầy 100%\n" in xiaomi and "IP68" in xiaomi
    ap = "\n".join(d["noi_dung"] for d in iphone)
    for chu in ["IP68", "A19", "Qi2", "USB-C", "iOS 27"]:
        assert chu in ap, chu
    samsung = "\n".join(d["noi_dung"] for d in doc_doan_that("tn-samsung-buds3pro"))
    assert "Galaxy Buds3 Pro" in samsung and "IP57" in samsung  # tên mã giữ số


# --- Bảng ghi tay: bỏ thêm ký hiệu bị sót, giữ lại '5*' (31/10/2026) ---

GHI_TAY_CHU_THICH = {1: "Dung lượng khả dụng nhỏ hơn.", 4: "Xác nhận về pin phụ thuộc cấu hình mạng.",
                     6: "Sạc 50% đo với bộ tiếp hợp 40W trở lên.", 8: "Chế Độ Nguồn Điện Thấp gồm theo dõi giấc ngủ."}
GHI_TAY_VAN_BAN = "\n".join([
    "Dung Lượng Lưu Trữ1", "256GB",
    "Pin Và Nguồn Điện4", "Thời gian xem video", "Lên đến 30 giờ",
    "Sạc lên đến 50% trong 20 phút6 với bộ tiếp hợp 40W trở lên",
    "Sạc MagSafe lên đến 50% trong 30 phút6 với bộ tiếp hợp 30W trở lên",  # số 6 nhắc lại giữa dòng: chuan_bi_manh bỏ sót
    "Sạc lại sau 30 phút6 với bộ tiếp hợp 30W trở lên",
    "Lên đến 32 giờ ở Chế Độ Nguồn Điện Thấp8",
    *GHI_TAY_CHU_THICH.values(),
])


def doan_ghi_tay(bo_them=(), giu_lai=()):
    """Đoạn thô của GHI_TAY_VAN_BAN rồi qua danh_ma_doan với hai bảng đã cho."""
    tho = cd.chia_doan(GHI_TAY_VAN_BAN, GHI_TAY_CHU_THICH)
    return tho, cd.danh_ma_doan("m", [("url", tho)], bo_them=bo_them, giu_lai=giu_lai)


def test_bang_ghi_tay_bo_ky_hieu_bi_sot_va_khong_doi_chu_thich():
    tho, truoc = doan_ghi_tay()
    assert "30 phút6 với bộ tiếp hợp 30W" in truoc[0]["noi_dung"]  # chuan_bi_manh chỉ nhận '20 phút6' đầu tiên
    _, sau = doan_ghi_tay(bo_them=(("m#001", "30 phút6", "6"),))
    d, d0 = sau[0], truoc[0]
    assert d["noi_dung"].count("30 phút với bộ tiếp hợp 30W") == 2 and "phút6" not in d["noi_dung"]  # mọi chỗ của ngữ cảnh
    assert d["noi_dung_goc"] == d0["noi_dung_goc"] and d["chu_thich"] == d0["chu_thich"]  # chỉ noi_dung đổi
    assert [x["chu"] for x in d["ky_hieu_bo"] if x["loai"] == cd.KY_HIEU_GHI_TAY] == ["6", "6"]
    assert [x["so"] for x in d["ky_hieu_bo"] if x["loai"] == cd.KY_HIEU_GHI_TAY] == [[6], [6]]
    assert {k: d[k] for k in d if k not in ("noi_dung", "ky_hieu_bo")} == {k: d0[k] for k in d0 if k not in ("noi_dung", "ky_hieu_bo")}
    # Ký hiệu đã nhận từ trước vẫn như cũ; chỗ bỏ thêm không làm đổi các chỗ đó.
    def khoa(nhat_ky):
        return [(x["vi_tri"], x["chu"], x["loai"], x["so"]) for x in nhat_ky]
    assert khoa(x for x in d["ky_hieu_bo"] if x["loai"] != cd.KY_HIEU_GHI_TAY) == khoa(d0["ky_hieu_bo"])
    assert "20 phút với" in d["noi_dung"] and "Thấp\n" in d["noi_dung"] + "\n"
    # Ký hiệu nhiều số, cuối dòng: bỏ cả cụm và khoảng trắng đứng trước.
    chu = cd.danh_ma_doan("m", [("url", [{"muc": "", "noi_dung": "Pin\nPhát lại 31 giờ 4,35\nMàu", "chu_thich": [],
                                          "noi_dung_goc": "Pin\nPhát lại 31 giờ 4,35\nMàu", "dong": [1, 3], "ky_hieu_bo": []}])],
                          bo_them=(("m#001", "31 giờ 4,35", "4,35"),))[0]
    assert chu["noi_dung"] == "Pin\nPhát lại 31 giờ\nMàu" and chu["ky_hieu_bo"][0]["so"] == [4, 35]


@pytest.mark.parametrize("muc, mong", [
    (("m#001", "ngoài đoạn 6", "6"), "không thấy ngữ cảnh"),
    (("m#001", "20 phút6 với 30 phút6", "6"), "đúng một lần"),  # ngữ cảnh chứa ký hiệu hai lần
    (("m#001", "30 phút", "6"), "đúng một lần"),  # ngữ cảnh không chứa ký hiệu
    (("m#001", "Pin Và Nguồn Điện", "Đ"), "phải là số chú thích"),  # không bỏ chữ
    (("m#001", "Thời gian xem video", "video"), "phải là số chú thích"),
    (("m#001", "20 phút6", "6"), "đã được bỏ rồi"),  # chuan_bi_manh đã bỏ chỗ này: mục thừa
    (("m#009", "30 phút6", "6"), "mã đoạn không tồn tại"),
])
def test_bang_ghi_tay_bao_loi_khi_muc_khong_khop_van_ban(muc, mong):
    with pytest.raises(ValueError, match=mong):
        doan_ghi_tay(bo_them=(muc,))


def test_bang_ghi_tay_mau_khac_khong_bi_anh_huong_va_muc_trung_la_loi():
    assert doan_ghi_tay(bo_them=(("khac#001", "30 phút6", "6"),))[1][0]["noi_dung"] == doan_ghi_tay()[1][0]["noi_dung"]
    with pytest.raises(ValueError, match="đã được bỏ rồi"):  # hai mục cùng ngữ cảnh: mục sau thừa
        doan_ghi_tay(bo_them=(("m#001", "30 phút6", "6"), ("m#001", "30 phút6 với bộ", "6")))


def test_bang_giu_lai_giu_5_sao_trong_danh_gia_con_sao_chu_thich_thi_bo():
    van_ban = "\n".join(["Chống nước", "Đạt chuẩn IP68* hàng đầu", "Đánh giá 5* cho sản phẩm", "*Thử nghiệm trong phòng thí nghiệm."])
    tho = cd.chia_doan(van_ban)
    mac_dinh = cd.danh_ma_doan("m", [("url", tho)])[0]
    assert "IP68 hàng đầu" in mac_dinh["noi_dung"] and "5 cho" in mac_dinh["noi_dung"]  # chuan_bi_manh nhận cả hai dấu *
    d = cd.danh_ma_doan("m", [("url", tho)], giu_lai=(("m#001", "5* cho", "*"),))[0]
    assert "5* cho" in d["noi_dung"] and "IP68 hàng đầu" in d["noi_dung"]  # chỉ giữ '5*'
    assert d["noi_dung_goc"] == mac_dinh["noi_dung_goc"] and d["chu_thich"] == mac_dinh["chu_thich"]
    assert [x["chu"] for x in d["ky_hieu_bo"]] == ["*"] and "IP68" in d["noi_dung_goc"]
    with pytest.raises(ValueError, match="không có ký hiệu nào đã bị bỏ"):  # không có dấu * nào đã bị bỏ ở đó
        cd.danh_ma_doan("m", [("url", tho)], giu_lai=(("m#001", "Chống nước", "C"),))
    with pytest.raises(ValueError, match="không thấy ngữ cảnh"):
        cd.danh_ma_doan("m", [("url", tho)], giu_lai=(("m#001", "5* khác", "*"),))


def test_that_bang_ghi_tay_dang_dung_khop_doan_jsonl():
    theo_mau = {}
    for ma_doan, ngu_canh, ky in cd.KY_HIEU_BO_THEM:
        ma_mau = ma_doan.split("#")[0]
        theo_mau[ma_mau] = theo_mau.get(ma_mau, 0) + 1
        d = next(x for x in doc_doan_that(ma_mau) if x["id"] == ma_doan)
        assert ngu_canh in d["noi_dung_goc"] and ngu_canh not in d["noi_dung"], (ma_doan, ngu_canh)
        assert ngu_canh.replace(ky, "").strip() in d["noi_dung"], (ma_doan, ngu_canh)
    assert theo_mau == {"dt-apple-iphone17": 1, "dt-xiaomi-15t": 6, "dh-apple-watchse3": 1,
                        "dt-samsung-galaxys25ultra": 12, "dh-samsung-galaxywatch8": 1}
    iphone = {d["id"]: d for d in doc_doan_that("dt-apple-iphone17")}
    assert "30 phút với bộ tiếp hợp 30W" in iphone["dt-apple-iphone17#016"]["noi_dung"]
    xiaomi = {d["id"]: d for d in doc_doan_that("dt-xiaomi-15t")}
    assert "AI10" not in xiaomi["dt-xiaomi-15t#041"]["noi_dung"] and xiaomi["dt-xiaomi-15t#041"]["noi_dung_goc"].count("AI10") == 14  # 13 chỗ bỏ bằng bảng, 1 chỗ chuan_bi_manh đã nhận
    # '5*' trong lời đánh giá: giữ ở cả hai trường, nhưng chu_thich của đoạn vẫn như trước (bảng không đổi cách gắn chú thích).
    watch = {d["id"]: d for d in doc_doan_that("dh-samsung-galaxywatch8")}["dh-samsung-galaxywatch8#129"]
    assert "5* product" in watch["noi_dung"] and "5* product" in watch["noi_dung_goc"]
    assert cd.KY_HIEU_GIU_LAI == (("dh-samsung-galaxywatch8#129", "5* product", "*"),)
