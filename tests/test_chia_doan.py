import importlib.util
import json
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


def doan_chua(doan, mau):
    mau = cd.GACH_DAC_BIET.sub("-", mau)  # đoạn đã chuẩn hóa ('Wi‑Fi' -> 'Wi-Fi')
    ket_qua = [d for d in doan if mau in d["noi_dung"]]
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
    wide = doan_chua(doan, "Ultra Wide3")
    assert S25_CHU_THICH[3] in wide["chu_thich"]
    # chú thích 1, 3, 4 đều có ký hiệu dẫn tới; chỉ chú thích 2 (không ai nhắc) thành đoạn riêng
    assert [d["noi_dung"].split("\n")[0] for d in doan if d["muc"] == "Chú thích"] == ["Chú thích 2"]


def test_that_s25_ultra_wide3():
    doan = doc_that("dt-samsung-galaxys25ultra", "bo_sung")
    wide = doan_chua(doan, "thậm chí là Ultra Wide3")
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
        assert chu_thich[3] not in d["chu_thich"] or "xong3" in d["noi_dung"]
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
    assert any("Ultra Wideband chỉ khả dụng" in c for c in doan_chua(doan, "thế hệ thứ 210")["chu_thich"])
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
    d = {"muc": "Pin", "noi_dung": "Pin\nLên đến 7 giờ", "chu_thich": [], "dong": [1, 2]}
    ket_qua = cd.danh_ma_doan("tn-samsung-buds3pro", [("url", [d, d]), ("bo_sung", [d])])
    assert [x["id"] for x in ket_qua] == ["tn-samsung-buds3pro#001", "tn-samsung-buds3pro#002", "tn-samsung-buds3pro#003"]
    assert [x["trang"] for x in ket_qua] == ["url", "url", "bo_sung"]
    assert set(ket_qua[0]) == {"id", "ma_mau", "trang", "muc", "noi_dung", "chu_thich", "dong"}
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
        assert d["noi_dung"].startswith(d["muc"])
        assert 1 <= d["dong"][0] <= d["dong"][1] <= so_dong
        assert len(d["noi_dung"]) <= cd.CAP_CUNG


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
    assert doc_lai == doan and doc_lai[0]["id"] == "tn-samsung-buds3pro#001"
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
