# Báo cáo thử độ bao phủ cấu hình trên 3 sản phẩm ngoài 12 mẫu (T-11)

- **Ngày thực hiện:** 18/11/2026
- **Người thực hiện:** Gemini 4 Carbon
- **Căn cứ đối chiếu:** `data/cau_hinh/chung.yaml`, `data/cau_hinh/dien_thoai.yaml`, `data/cau_hinh/tai_nghe.yaml`, `data/cau_hinh/dong_ho.yaml` (bản trên đĩa ngày `18/11/2026`, gồm các bổ sung Bước 28 vừa cập nhật như `"ANC Bật"`/`"ANC Tắt"` và `"khi bơi"`)
- **Dữ liệu chi tiết:** `ket_qua/bao_phu/cum_3_san_pham.json` (168 mục)

---

## 1. URL chính hãng đã dùng và ngày truy cập

Cả 3 sản phẩm đề xuất ngày 27/10/2026 (`luan_van/nhat_ky.md` dòng 33) đều có trang chính hãng tiếng Việt hoạt động bình thường (`HTTP 200`), không trùng với 12 mẫu trong `data/mau_san_pham.csv`, nên **không cần chọn sản phẩm thay thế** và **không dùng bất kỳ trang bán lẻ nào**. Với sản phẩm có tách trang thông số kỹ thuật và trang giới thiệu sản phẩm (kèm chú thích cuối trang và mục hỏi đáp FAQ), cả hai trang đều được đọc để thu thập đầy đủ giá trị và điều kiện quyết định; phần đánh giá của người dùng và cột của sản phẩm khác trong bảng so sánh được loại bỏ đúng theo mục 4 của `data/huong_dan_gan_nhan.md`.

| Sản phẩm | Mã máy trên trang | Nhóm (`nhom`) | Vai trò trang | URL chính hãng tiếng Việt | Ngày truy cập |
|---|---|---|---|---|---|
| **OPPO Reno14** (OPPO Reno14 5G) | `CPH2737` | `dien_thoai` | Trang thông số kỹ thuật | `https://www.oppo.com/vn/smartphones/series-reno/reno14/specs/` | 18/11/2026 |
| **OPPO Reno14** (OPPO Reno14 5G) | `CPH2737` | `dien_thoai` | Trang sản phẩm, chú thích 1–31 & FAQ | `https://www.oppo.com/vn/smartphones/series-reno/reno14/` | 18/11/2026 |
| **OPPO Enco Air5 Pro** | `ETEL1` | `tai_nghe` | Trang thông số kỹ thuật | `https://www.oppo.com/vn/accessories/enco-air5-pro/specs/` | 18/11/2026 |
| **OPPO Enco Air5 Pro** | `ETEL1` | `tai_nghe` | Trang sản phẩm & tuyên bố miễn trừ 1–14 | `https://www.oppo.com/vn/accessories/enco-air5-pro/` | 18/11/2026 |
| **Galaxy Watch Ultra2** | `SM-L715FZKAXXV` | `dong_ho` | Trang sản phẩm tích hợp `#specs`, FAQ & chú thích 1–46 | `https://www.samsung.com/vn/watches/galaxy-watch/galaxy-watch-ultra2-titanium-gray-lte-sm-l715fzkaxxv/` | 18/11/2026 |

---

## 2. Bảng số đếm độ bao phủ và kết luận đối chiếu ngưỡng 80%

### 2.1 Tổng hợp theo sản phẩm (trên toàn bộ 168 cụm gắn với giá trị trong `cum_3_san_pham.json`)

| Sản phẩm | Nhóm | `nhan_ra` | `khong_nhan_ra` | `khong_ro` | Tổng cụm | Tỷ lệ `nhan_ra / tổng cụm` |
|---|---|---:|---:|---:|---:|---:|
| **OPPO Reno14** | `dien_thoai` | 18 | 18 | 3 | 39 | **18 / 39 (46,2%)** |
| **OPPO Enco Air5 Pro** | `tai_nghe` | 49 | 38 | 0 | 87 | **49 / 87 (56,3%)** |
| **Galaxy Watch Ultra2** | `dong_ho` | 11 | 31 | 0 | 42 | **11 / 42 (26,2%)** |
| **Tổng cộng** | **3 nhóm** | **78** | **87** | **3** | **168** | **78 / 168 (46,4%)** |

### 2.2 Phân rã chi tiết theo từng thuộc tính đã khai báo trong YAML

| Sản phẩm | Thuộc tính (`thuoc_tinh`) | Có công bố trên trang? | `nhan_ra` | `khong_nhan_ra` | `khong_ro` | Tổng cụm | Tỷ lệ nhận ra |
|---|---|---|---:|---:|---:|---:|---:|
| OPPO Reno14 | `thoi_luong_pin` | Có (`2.25 ngày`, `10 Giờ`) | 0 | 3 | 0 | 3 | 0,0% |
| OPPO Reno14 | `sac_nhanh` | Có (`48 phút`) | 1 | 1 | 1 | 3 | 33,3% |
| OPPO Reno14 | `cong_suat_sac` | Có (`80W`) | 0 | 1 | 0 | 1 | 0,0% |
| OPPO Reno14 | `do_sang` | Có (`600nits`, `1200nits`) | 1 | 2 | 1 | 4 | 25,0% |
| OPPO Reno14 | `tan_so_quet` | Có (`120Hz`) | 2 | 2 | 0 | 4 | 50,0% |
| OPPO Reno14 | `zoom` | Có (`3,5X`, `18X`, `2X`, `3.5x`) | 9 | 5 | 0 | 14 | 64,3% |
| OPPO Reno14 | `khang_nuoc` | Có (`IP69`, `IP68`, `IP66`) | 3 | 2 | 1 | 6 | 50,0% |
| OPPO Reno14 | `dung_luong_pin` | Có (`6000mAh`, `5840mAh`) | 2 | 2 | 0 | 4 | 50,0% |
| OPPO Enco Air5 Pro | `thoi_luong_pin` | Có (12 số phát nhạc + 6 số đàm thoại) | 45 | 37 | 0 | 82 | 54,9% |
| OPPO Enco Air5 Pro | `sac_nhanh` | Không công bố dạng `gio` sau `X phút sạc` *(chỉ có sạc đầy `60/90 phút`, xem mục 4)* | 0 | 0 | 0 | 0 | — |
| OPPO Enco Air5 Pro | `khang_nuoc` | Có (`IP55` tai nghe, `không` hộp sạc) | 2 | 1 | 0 | 3 | 66,7% |
| OPPO Enco Air5 Pro | `dung_luong_pin` | Có (`62 mAh`, `530 mAh`) | 2 | 0 | 0 | 2 | 100,0% |
| Galaxy Watch Ultra2 | `thoi_luong_pin` | Có (`60 giờ`, `80 giờ`, `20 giờ`, `16 giờ`) | 6 | 14 | 0 | 20 | 30,0% |
| Galaxy Watch Ultra2 | `sac_nhanh` | Có (`30 phút` tới `40%`) | 1 | 3 | 0 | 4 | 25,0% |
| Galaxy Watch Ultra2 | `khang_nuoc` | Có (`100 mét`/`10 ATM`, `40 mét` lặn, `IPX8`, `IP69K`) | 2 | 11 | 0 | 13 | 15,4% |
| Galaxy Watch Ultra2 | `do_sang` | Có (`5000 nits`) | 2 | 3 | 0 | 5 | 40,0% |

### 2.3 Đối chiếu độ nhạy khi khử trùng cụm điều kiện lặp giữa nhiều dòng giá trị của cùng `(sản phẩm, thuộc tính)`

Do bảng thông số của `OPPO Enco Air5 Pro` tách ma trận 12 giá trị phát nhạc và 6 giá trị đàm thoại, các cụm như `"phát nhạc"`, `"âm lượng 50%"`, `"AAC"`, `"LHDC"`, `"(tai nghe + hộp sạc)"` lặp lại qua nhiều giá trị. Để kiểm tra kết luận không bị chi phối bởi tần suất lặp dòng bảng, bảng dưới đếm theo **cụm điều kiện duy nhất** trong từng cặp `(sản phẩm, thuộc tính)`:

| Sản phẩm | `nhan_ra` (duy nhất) | `khong_nhan_ra` (duy nhất) | `khong_ro` (duy nhất) | Tổng cụm duy nhất | Tỷ lệ nhận ra (khử trùng) |
|---|---:|---:|---:|---:|---:|
| OPPO Reno14 | 13 | 17 | 3 | 33 | 13 / 33 (39,4%) |
| OPPO Enco Air5 Pro | 15 | 8 | 0 | 23 | 15 / 23 (65,2%) |
| Galaxy Watch Ultra2 | 9 | 28 | 0 | 37 | 9 / 37 (24,3%) |
| **Tổng khử trùng** | **37** | **53** | **3** | **93** | **37 / 93 (39,8%)** |

### 2.4 Kết luận đối chiếu ngưỡng 80%

> **KẾT LUẬN: KHÔNG ĐẠT NGƯỠNG 80%.**
> Tỷ lệ nhận ra toàn cục chỉ đạt **46,4% (`78 / 168`)** (hoặc **39,8% (`37 / 93`)** nếu khử trùng theo thuộc tính), thấp hơn ngưỡng dừng **80%** của Bước 16 tới **33,6 điểm phần trăm**, và không có sản phẩm đơn lẻ nào đạt ngưỡng (`46,2%`, `56,3%`, `26,2%`).

Kết quả này khớp đúng dự đoán ghi trước ngày 26/10/2026 (`data/cau_hinh/bao_phu_dieu_kien.md` mục 7): 4 mẫu tập phát triển chưa có điện thoại OPPO, tai nghe OPPO và đồng hồ Samsung, nên từ điển đóng hiện tại bỏ sót hàng loạt chiều điều kiện phổ biến của các hãng này (codec Bluetooth `AAC`/`LHDC`, mức âm lượng thử pin `50%`, màn hình `AOD On`/`AOD Off`, camera `Sau`/`Trước`, chế độ `HBM`, chuẩn lặn `EN13319` giới hạn 40 m so với 100 m ISO 22810, chuẩn `IP69`/`IP69K`, củ sạc ghi theo `5V/2A`). Theo đúng quy trình Bước 16 (`CHI_TIET_TUYEN_TINH_KHOA_LUAN.md` dòng 498), **cần bổ sung các quy tắc và cách diễn đạt tổng quát từ chính 3 trang ngoài mẫu này trước khi khóa cấu hình ở Mốc 3 (Bước 33)**.

---

## 3. Danh sách cụm `khong_nhan_ra` và đề xuất bổ sung vào YAML

Tổng cộng có **87 lượt (`53` tổ hợp `(sản phẩm, thuộc tính, cụm)` duy nhất)** kết luận `khong_nhan_ra`. Đặc biệt, có **4 nhóm cụm không chỉ bị bỏ sót (`dieu_kien_khac`) mà còn gây khớp nhầm chiều/nhầm cực trong mã hiện tại**:
1. `"khi tắt Chế độ tiết kiệm pin"` (`dong_ho.thoi_luong_pin`): chứa chuỗi con `"tiết kiệm pin"` nên bị gán ngược thành `che_do_nguon = nguon_thap` thay vì `thuong`.
2. `"(với hộp sạc)"` (`tai_nghe.thoi_luong_pin`): chứa `"hộp sạc"` nên bị gán nhầm thành `bo_phan = hop_sac` (riêng hộp sạc) thay vì `kem_hop_sac` (tổng kèm hộp sạc).
3. `"(tai nghe + hộp sạc)"` (`tai_nghe.thoi_luong_pin`): khớp đồng thời cả `bo_phan.tai_nghe` lẫn `bo_phan.hop_sac`, sinh `xung_dot` thay vì `kem_hop_sac`.
4. `"HBM: 1200nits (Tiêu chuẩn)"` (`dien_thoai.do_sang`): OPPO dịch `Typical` thành `(Tiêu chuẩn)` (kiểu giá trị điển hình), nhưng `dien_thoai.yaml` lại khớp `"(tiêu chuẩn)"` sang `che_do_hien_thi.tieu_chuan`, gộp nhầm độ sáng HBM 1200 nits vào cùng chế độ tiêu chuẩn với 600 nits (sinh lỗi mâu thuẫn giả `D1b`).

### 3.1 Nhóm điện thoại (`dien_thoai.yaml` & `chung.yaml`) — 18 lượt (17 tổ hợp duy nhất)

| Cụm `khong_nhan_ra` (số lượt) | Thuộc tính | Nguyên nhân hiện tại | Đề xuất bổ sung vào YAML (tệp · khóa điều kiện · giá trị · cách diễn đạt) |
|---|---|---|---|
| `"DoU"` (1x) | `thoi_luong_pin` | Chưa có kịch bản dùng hỗn hợp tiêu chuẩn DoU; đơn vị `"ngày"` chưa có trong `chuan_hoa.don_vi` | `chung.yaml`: thêm `ngay: ["ngày"]` vào `chuan_hoa.don_vi` và quy đổi `1 ngày = 24 giờ` ở `quy_doi`. `dien_thoai.yaml`: dưới `cach_dien_dat.hoat_dong`, thêm khóa `su_dung_hon_hop: {phia: tai_lieu, tu_tai_lieu: ["DoU"], hieu_biet_chung: ["sử dụng hỗn hợp"]}` |
| `"MOBA Game"` (1x), `"Mobile Legends: Bang Bang"` (1x) | `thoi_luong_pin` | `cach_dien_dat.hoat_dong` chưa có hoạt động chơi game | `dien_thoai.yaml`: dưới `cach_dien_dat.hoat_dong`, thêm khóa `choi_game: {tu_tai_lieu: ["MOBA Game", "Game MOBA", "Mobile Legends: Bang Bang"], hieu_biet_chung: ["chơi game", "chiến game", "game MOBA"]}` |
| `"từ 1% đến 100%"` (1x) | `sac_nhanh` | Có hai con số `%` trong cùng cụm nên luật nhận theo đơn vị sinh `xung_dot` | `dien_thoai.yaml` + `trich_xuat.py`: trong `cach_dien_dat.moc_phan_tram.gia_tri_so`, bổ sung mẫu khoảng sạc từ mức đầu ≤ 1% tới mức đích `B%` (lấy mốc đích `B%` khi có dạng `"từ <số>% đến <số>%"` hoặc `"từ 1-<số>%"`) |
| `"SUPERVOOCTM"` (1x) | `cong_suat_sac` | Chưa khai báo tên chuẩn/củ sạc nhanh độc quyền tách với PD/PPS | `dien_thoai.yaml`: thêm điều kiện `chuan_sac: phu_kien` (mặc định `nhu_hang_cong_bo` khi máy kèm củ sạc trong hộp, hoặc mở rộng `cach_dien_dat.bo_tiep_hop` / `chuan_sac` với `["SUPERVOOC", "SUPERVOOCTM", "VOOC", "PD", "PPS"]`) |
| `"HBM"` (1x) | `do_sang` | Chưa có viết tắt High Brightness Mode | `dien_thoai.yaml`: thêm `"HBM"`, `"chế độ độ sáng cao"` vào `cach_dien_dat.che_do_hien_thi.tu_tang_sang` (hoặc gộp `ngoai_troi` và `tu_tang_sang` như ghi chú dòng 217 của `dien_thoai.yaml`) |
| `"(Tiêu chuẩn)"` trên dòng `HBM: 1200nits (Tiêu chuẩn)` (1x) | `do_sang` | OPPO dùng `(Tiêu chuẩn)` dịch chữ `(Typical)` (`kieu_gia_tri.dien_hinh`); bị khớp nhầm sang `che_do_hien_thi.tieu_chuan` | `dien_thoai.yaml`: chỉ nhận `"(tiêu chuẩn)"` là `che_do_hien_thi.tieu_chuan` khi dòng chưa có chế độ hiển thị khác (`HBM`, `HDR`, `ngoài trời`); bổ sung `"tiêu chuẩn"` vào cụm kiểu giá trị điển hình khi đứng trong ngoặc ngay sau đơn vị mà chế độ hiển thị đã xác định |
| `"(60/90/120Hz)"` (1x) | `tan_so_quet` | Cụm liệt kê các bậc tần số động chưa khai báo; `tim_gia_tri` tách nhầm `90/120Hz` | `dien_thoai.yaml` / `chuan_hoa.py`: nhận dạng chuỗi nhiều mức ngăn bởi `/` có từ 3 số trở lên (`60/90/120Hz`) là `kieu_tan_so: thich_ung` thay vì cặp `bo_phan` |
| `"Thích Ứng Thông Minh"` (1x) | `tan_so_quet` | `"Thông Minh"` xen giữa `"Thích Ứng"` và `"120Hz"` làm trượt `tim_kieu_gia_tri`; `kieu_tan_so.thich_ung` thiếu `"thích ứng"` rời | `dien_thoai.yaml`: thêm `"màn hình thích ứng"`, `"thích ứng thông minh"`, `"thích ứng"` vào `cach_dien_dat.kieu_tan_so.thich_ung` |
| `"Sau"` (2x), `"Trước"` (1x) | `zoom` | `thuoc_tinh.zoom` chưa có điều kiện `bo_phan`, làm `2X` (video trước) đụng `18X` (video sau) | `dien_thoai.yaml`: thêm `bo_phan: bo_phan` vào `thuoc_tinh.zoom.dieu_kien_bat_buoc`, `hieu_thong_thuong.bo_phan: camera_sau`, và khai báo `cach_dien_dat.bo_phan: {camera_sau: ["camera sau", "mặt sau", "sau"], camera_truoc: ["camera trước", "camera selfie", "mặt trước", "trước"]}` (`chi_thuoc_tinh: [zoom]`) |
| `"Camera Tele"` (1x), `"zoom quang"` (1x) | `zoom` | `loai_zoom.quang_hoc` chỉ có `"telephoto"` và `"quang học"` (không khớp ranh giới từ với `"tele"`, `"zoom quang"`) | `dien_thoai.yaml`: thêm `"camera tele"`, `"ống kính tele"`, `"zoom quang"` vào `cach_dien_dat.loai_zoom.quang_hoc` |
| `"chỉ hỗ trợ nước ngọt"` (1x) | `khang_nuoc` | `loai_nuoc.nuoc_ngot` chỉ có `"nước ngọt tĩnh lặng"` | `dien_thoai.yaml`: thêm `"nước ngọt"` vào `cach_dien_dat.loai_nuoc.nuoc_ngot` (đồng bộ với `tai_nghe.yaml`); đồng thời mở rộng `chung.yaml: chuan_hoa.ma_ip` cho chữ số nước `9` (`IP69`, nhánh tia nước áp suất/nhiệt độ cao) |
| `"sử dụng vỏ chống nước chuyên nghiệp"` (1x) | `khang_nuoc` | Chưa có điều kiện phụ kiện bảo vệ khi chụp ảnh dưới nước | `dien_thoai.yaml`: thêm `phu_kien_bao_ve: phu_kien` cho `khang_nuoc` (`hieu_thong_thuong: khong_mua_them`, `cach_dien_dat`: `["vỏ chống nước", "vỏ chống nước chuyên nghiệp", "vỏ bảo vệ", "túi chống nước"]`) |
| `"Giá trị tiêu chuẩn"` (1x), `"(giá trị thông thường)"` (1x) | `dung_luong_pin` | `kieu_dung_luong.dien_hinh` chỉ có `"(thông thường)"`, `"(typ)"`, `"điển hình"` | `dien_thoai.yaml`: bỏ ngoặc bao quanh trong `kieu_dung_luong.dien_hinh` thành `"thông thường"`, `"typ"`, và thêm `"giá trị thông thường"`, `"giá trị tiêu chuẩn"` (kèm kiểm tra quy ước Typical > Rated khi hãng dịch ngược) |

### 3.2 Nhóm tai nghe (`tai_nghe.yaml`) — 38 lượt (8 tổ hợp duy nhất)

| Cụm `khong_nhan_ra` (số lượt) | Thuộc tính | Nguyên nhân hiện tại | Đề xuất bổ sung vào YAML (tệp · khóa điều kiện · giá trị · cách diễn đạt) |
|---|---|---|---|
| `"AAC"` (6x), `"LHDC"` (6x) | `thoi_luong_pin` | `tai_nghe.yaml` chưa có điều kiện codec âm thanh dù đổi `AAC` → `LHDC` giảm pin từ 54h xuống 39h | `tai_nghe.yaml`: thêm `codec_am_thanh: che_do_hoat_dong` vào `thuoc_tinh.thoi_luong_pin.dieu_kien_bat_buoc` (`hieu_thong_thuong: aac` hoặc `kem_thuan_loi_nhat` nếu quảng cáo nêu Hi-Res/LHDC), khai báo `cach_dien_dat.codec_am_thanh`: `aac: ["AAC", "chế độ AAC"]`, `lhdc: ["LHDC", "LHDC 5.0", "chế độ LHDC"]`, `ldac: ["LDAC"]`, `sbc: ["SBC"]` |
| `"âm lượng 50%"` (12x) | `thoi_luong_pin` | Chưa khai báo điều kiện đo mức âm lượng thử pin; bị rơi vào `dieu_kien_khac` → `D1a` cho cả 12 dòng | `tai_nghe.yaml`: thêm `muc_am_luong: dieu_kien_do` vào `thoi_luong_pin.dieu_kien_bat_buoc` (`hieu_thong_thuong: nhu_hang_cong_bo`), `dieu_kien_so.muc_am_luong: {don_vi: phan_tram, thoa_khi: tuyen_bo_lon_hon_hoac_bang}` (hoặc `bang`), `cach_dien_dat.muc_am_luong.gia_tri_so: ["âm lượng", "mức âm lượng"]` |
| `"(tai nghe + hộp sạc)"` (6x), `"(với hộp sạc)"` (3x) | `thoi_luong_pin` | `bo_phan.kem_hop_sac` thiếu cả hai cụm; sinh `xung_dot` hoặc khớp nhầm sang `hop_sac` | `tai_nghe.yaml`: thêm `"tai nghe + hộp sạc"`, `"với hộp sạc"` vào `cach_dien_dat.bo_phan.kem_hop_sac` (do cụm dài khớp trước nên `"tai nghe + hộp sạc"` và `"với hộp sạc"` sẽ thắng `"tai nghe"` / `"hộp sạc"` đơn lẻ) |
| `"ANC On"` (2x), `"ANC Off"` (2x) | `thoi_luong_pin` | `che_do_chong_on` mới có tiếng Việt (`"bật/tắt ANC"`, `"ANC Bật/Tắt"`), chưa có tiếng Anh | `tai_nghe.yaml`: thêm `"ANC On"` vào `cach_dien_dat.che_do_chong_on.bat`; thêm `"ANC Off"` vào `cach_dien_dat.che_do_chong_on.tat` |
| `"Tránh sử dụng khi vận động mạnh"` (1x) | `khang_nuoc` | `hoat_dong_bi_cam` chỉ mới có nhóm bơi/biển | `tai_nghe.yaml`: dưới `cach_dien_dat.hoat_dong_bi_cam`, thêm `"vận động mạnh"`, `"tập luyện cường độ cao"` (hoặc khóa con `van_dong_manh`) |

### 3.3 Nhóm đồng hồ (`dong_ho.yaml` & `chung.yaml`) — 31 lượt (28 tổ hợp duy nhất)

| Cụm `khong_nhan_ra` (số lượt) | Thuộc tính | Nguyên nhân hiện tại | Đề xuất bổ sung vào YAML (tệp · khóa điều kiện · giá trị · cách diễn đạt) |
|---|---|---|---|
| `"AOD On"` (1x), `"(*AOD Bật)"` (1x), `"tính năng Always On Display được bật"` (1x), `"AOD Off"` (1x), `"Always On Display được tắt"` (1x) | `thoi_luong_pin` | `dong_ho.yaml` chưa có chiều điều kiện màn hình luôn bật (AOD làm đổi pin từ 80h xuống 60h) | `dong_ho.yaml`: thêm `man_hinh_luon_bat: che_do_hoat_dong` vào `thuoc_tinh.thoi_luong_pin.dieu_kien_bat_buoc` (`hieu_thong_thuong: kem_thuan_loi_nhat` hoặc `bat` khi hãng dùng AOD On làm mốc chính), khai báo `cach_dien_dat.man_hinh_luon_bat`: `bat: ["AOD On", "AOD Bật", "*AOD Bật", "bật AOD", "bật Always On Display", "Always On Display được bật"]`, `tat: ["AOD Off", "AOD Tắt", "tắt AOD", "tắt Always On Display", "Always On Display được tắt"]` |
| `"Ở chế độ pin bình thường"` (2x), `"khi tắt Chế độ tiết kiệm pin"` (2x), `"Chế độ tiết kiệm pin khi tập thể dục"` (2x) | `thoi_luong_pin` | `che_do_nguon.thuong` chỉ có `"chế độ thường"`; cụm `"khi tắt Chế độ tiết kiệm pin"` bị khớp ngược sang `nguon_thap` | `dong_ho.yaml`: thêm `"chế độ pin bình thường"`, `"tắt chế độ tiết kiệm pin"`, `"khi tắt chế độ tiết kiệm pin"`, `"tắt chế độ tiết kiệm pin khi tập thể dục"` vào `cach_dien_dat.che_do_nguon.thuong` (nhờ quy tắc cụm dài khớp trước, `"tắt chế độ tiết kiệm pin"` sẽ thắng `"tiết kiệm pin"`); thêm `"chế độ tiết kiệm pin khi tập thể dục"` vào `nguon_thap` |
| `"các tình huống sử dụng thông thường"` (1x) | `thoi_luong_pin` | `hoat_dong.su_dung_binh_thuong` chưa có từ `"thông thường"` | `dong_ho.yaml`: thêm `"sử dụng thông thường"`, `"dùng thông thường"` vào `cach_dien_dat.hoat_dong.su_dung_binh_thuong` |
| `"GPS hoạt động liên tục"` (1x), `"GPX"` (1x) | `thoi_luong_pin` | `hoat_dong` chưa có chế độ định vị GPS liên tục (20h) và dẫn đường GPX (16h) | `dong_ho.yaml`: dưới `cach_dien_dat.hoat_dong`, thêm `gps_lien_tuc: ["GPS hoạt động liên tục", "bật GPS liên tục"]` và `dan_duong_gpx: ["GPX", "sử dụng GPX", "tuyến đường GPX"]` |
| `"chế độ máy bay được bật"` (1x) | `sac_nhanh` | Chưa có điều kiện chế độ kết nối khi sạc nhanh | `dong_ho.yaml`: thêm `che_do_ket_noi: che_do_hoat_dong` vào `sac_nhanh.dieu_kien_bat_buoc` (`hieu_thong_thuong: nhu_hang_cong_bo`), `cach_dien_dat.che_do_ket_noi.may_bay: ["chế độ máy bay", "chế độ máy bay được bật", "bật chế độ máy bay"]` |
| `"bộ sạc không dây chuyên dụng (EP-OL715)"` (1x) | `sac_nhanh` | `cap_sac` chỉ có cáp từ tính của Apple | `dong_ho.yaml`: thêm `"bộ sạc không dây chuyên dụng"`, `"đế sạc không dây"`, `"sạc không dây đi kèm"` vào `cach_dien_dat.cap_sac.cap_di_kem` |
| `"Bộ chuyển đổi nguồn PD 5V/2A (TA)"` (1x) | `sac_nhanh` | `bo_tiep_hop` thiếu `"Bộ chuyển đổi nguồn"` và `dieu_kien_so` không đọc được tích `V × A` (`5V/2A = 10W`) | `dong_ho.yaml` + `chuan_hoa.py`: thêm `"bộ chuyển đổi nguồn"`, `"bộ sạc PD"` vào `cach_dien_dat.bo_tiep_hop.gia_tri_so`; bổ sung hàm quy đổi biểu thức `<U>V/<I>A` hoặc `<U>V ⎓ <I>A` sang `U × I` (W) khi đọc `dieu_kien_so` đơn vị `W` |
| `"theo tiêu chuẩn ISO22810"` (1x) | `khang_nuoc` | Trang Samsung viết dính `"ISO22810"` không khoảng trắng; thiếu `"10ATM"`, `"10 ATM"`, `"độ sâu 100m"` | `dong_ho.yaml`: thêm `"ISO22810"`, `"10ATM"`, `"10 ATM"`, `"độ sâu 100m"`, `"100 mét"` vào `cach_dien_dat.chuan_do_sau.iso_22810` |
| `"đạt chứng nhận EN13319"` (1x), `"hoạt động lặn"` (1x), `"trong hồ bơi"` (1x), `"vùng nước hở"` (1x) | `khang_nuoc` | Đồng hồ đạt `10 ATM` (100 m ISO 22810) nhưng lặn thực tế theo `EN13319` chỉ tối đa **40 m**; `dong_ho.yaml` chưa có `EN13319`, chưa có `do_sau` dạng số, và đang cứng nhắc cấm `"lặn sâu"` theo Watch SE 3 | `dong_ho.yaml`: (1) thêm `do_sau` và `thoi_gian_ngam` vào `khang_nuoc.dieu_kien_so` như điện thoại/tai nghe; (2) thêm giá trị `en_13319: ["EN13319", "EN 13319", "chứng nhận EN13319"]` vào `chuan_do_sau`; (3) mở rộng `hoat_dong_cho_phep.duoc_phep` với `["hoạt động lặn", "lặn", "trong hồ bơi", "hồ bơi", "vùng nước hở", "vùng nước mở"]` và phân biệt giới hạn độ sâu theo từng hoạt động (lặn ≤ 40 m so với áp suất tĩnh 100 m) |
| `"nước muối 5%"` (1x), `"nước có chứa 4 ppm clo"` (1x), `"nước ngọt"` (1x), `"lên đến 1,5 mét"` (1x), `"tối đa 30 phút"` (1x), `"các tia nước áp suất cao, nhiệt độ cao"` (1x) | `khang_nuoc` | `dong_ho.khang_nuoc` chưa khai báo `loai_nuoc`, `do_sau`, `thoi_gian_ngam` cho bài thử IP (`IPX8` 1,5 m / 30 phút, `IP69K`/`IPX9K` tia nước áp suất & nhiệt độ cao) | `dong_ho.yaml` + `chung.yaml`: đồng bộ các khóa `loai_nuoc`, `do_sau`, `thoi_gian_ngam`, `tia_nuoc` từ `dien_thoai.yaml` sang `dong_ho.yaml`; bổ sung chữ số nước `9` / `9K` vào `chung.yaml: chuan_hoa.ma_ip` |
| `"độ sáng đỉnh cục bộ"` (1x), `"trong điều kiện ánh sáng xung quanh cao"` (1x), `"dưới ánh nắng trực tiếp"` (1x) | `do_sang` | `dong_ho.do_sang` chưa có `dien_tich_do` (cục bộ so với toàn màn hình) và `che_do_hien_thi` chỉ có `"bình thường"` | `dong_ho.yaml`: đồng bộ với `dien_thoai.yaml` — thêm `dien_tich_do: dieu_kien_do` (với giá trị `"đỉnh cục bộ"` / `"cục bộ"` đối lập `"toàn màn hình"`) và thêm chế độ sáng cao ngoài trời vào `cach_dien_dat.che_do_hien_thi`: `["trong điều kiện ánh sáng xung quanh cao", "ánh sáng xung quanh cao", "dưới ánh nắng trực tiếp", "dưới ánh nắng gay gắt", "dưới ánh nắng"]` |

---

## 4. Danh sách thuộc tính có công bố trên trang nhưng YAML chưa khai báo

Các thuộc tính dưới đây có số liệu định lượng (nhiều thuộc tính kèm điều kiện rõ) trên trang chính hãng của 3 sản phẩm nhưng chưa nằm trong `thuoc_tinh` của tệp YAML nhóm tương ứng. Theo đúng hướng dẫn mục 4 của brief, **các thuộc tính này không tính vào mẫu số hay tử số của tỷ lệ bao phủ ở mục 2**.

| Nhóm | Sản phẩm | Thuộc tính / dạng thông số chưa khai báo | Giá trị và điều kiện công bố trên trang | Ghi chú |
|---|---|---|---|---|
| `dong_ho` | Galaxy Watch Ultra2 | **`dung_luong_pin` (mAh)** | `800 mAh` kèm kiểu giá trị `Typical` / `Dung lượng điển hình` / `Giá trị đặc trưng` (thử nghiệm theo IEC 61960) | `dien_thoai.yaml` và `tai_nghe.yaml` đều đã có `dung_luong_pin`, riêng `dong_ho.yaml` chưa khai báo (khớp phát hiện `T-29`) |
| `dong_ho` | Galaxy Watch Ultra2 | **Còi báo động an toàn SOS (`coi_bao_dong`)** | Âm lượng `lên tới 86 decibel`, khoảng cách nghe thấy `tối đa 180 mét` khi nhấn giữ Nút phản ứng nhanh `5 giây` (tùy môi trường và pin) | Thông số quảng cáo nổi bật của dòng đồng hồ thể thao/dã ngoại |
| `dong_ho` | Galaxy Watch Ultra2 | **Nhiệt độ hoạt động / độ bền môi trường (`MIL-STD-810H`)** | Chịu nhiệt độ `từ -20°C đến 55°C` với điều kiện **`khi đeo trên cổ tay`** (chú thích 5: quá nóng/lạnh có thể tự dừng sạc hoặc tắt máy) | Có điều kiện đeo trên cổ tay rất dễ bị quảng cáo lược bỏ |
| `dong_ho` | Galaxy Watch Ultra2 | **Dung lượng lưu trữ khả dụng & RAM** | Bộ nhớ `64 GB`, **có sẵn lưu trữ `49.3 GB`**, RAM `2 GB` | Thuộc nhóm ngoài phạm vi hiện tại (mục 8 `bao_phu_dieu_kien.md`) |
| `dong_ho` | Galaxy Watch Ultra2 | **Kích thước, độ phân giải, trọng lượng, xung nhịp CPU** | Màn hình `1,52 inch` / `1.5" (38.5mm)`, `498 x 498`, thân máy `47.4 x 47.1 x 10.7 mm`, nặng `61.5 g` (riêng thân máy), CPU 3 nm 5 nhân `2.1GHz, 1.95GHz` | Trọng lượng chỉ tính thân máy không kèm dây |
| `tai_nghe` | OPPO Enco Air5 Pro | **Thời gian sạc đầy (`thoi_gian_sac`, đơn vị `phút`)** | `60 phút (tai nghe)` / `90 phút (tai nghe + hộp sạc)` ở `nhiệt độ 25°C` với `bộ sạc tiêu chuẩn của OPPO` | `tai_nghe.yaml` chỉ mới khai báo `sac_nhanh` đơn vị `gio` (sạc X phút nghe Y giờ), chưa có thời gian sạc đầy tính bằng phút |
| `tai_nghe` | OPPO Enco Air5 Pro | **Độ sâu & dải tần chống ồn chủ động (`do_sau_chong_on`)** | Cường độ khử ồn `lên đến 55 dB` (tối đa phòng thí nghiệm OPPO) và dải tần `5000 Hz` | Một trong những con số được quảng cáo nhiều nhất của tai nghe ANC (xem thêm nhật ký Bước 11) |
| `tai_nghe` | OPPO Enco Air5 Pro | **Kháng gió khi đàm thoại** | Cuộc gọi rõ ràng khi `gió lên đến 25 km/h` (3 micro AI) | Thông số có điều kiện tốc độ gió tối đa |
| `tai_nghe` | OPPO Enco Air5 Pro | **Chất lượng âm thanh Hi-Res / tần số lấy mẫu** | Tần số lấy mẫu `lên đến 96 kHz`, bit rate `1 Mbps` với `LHDC 5.0` (chỉ trên ColorOS 12.0+ hoặc Android 8.0+ cài HeyMelody; **không hỗ trợ iOS**); đáp ứng `20 Hz~40 KHz`; nhạy `122dB@1kHz` | Có điều kiện hệ điều hành và ứng dụng rất chặt |
| `tai_nghe` | OPPO Enco Air5 Pro | **Phạm vi Bluetooth, điện áp/dòng sạc, trọng lượng** | `Bluetooth 6.0`, phạm vi tối đa `10m`; đầu vào `5V ⎓ 1.5A` (hộp sạc), `5V ⎓ 0.2A` (tai nghe); nặng `4.4 ± 0.2g` (tai nghe), `43 ± 1g` (tai nghe + hộp sạc) | Thông số phần cứng phụ |
| `dien_thoai` | OPPO Reno14 | **Sạc nhanh dạng 2: số giờ dùng sau X phút sạc** | `12.8 Giờ Liên Lạc` sau `10 Phút sạc` (chú thích 20) | `dong_ho.yaml` khai báo cả hai dạng cho `sac_nhanh` (`phut_hoac_gio`), nhưng `dien_thoai.yaml` chỉ khai báo dạng 1 (`don_vi: phut` tới mốc phần trăm) |
| `dien_thoai` | OPPO Reno14 | **Tần số lấy mẫu cảm ứng** | `Tối đa: 240Hz`, `Mặc định: 120Hz` | Đã nêu ở mục 8 `bao_phu_dieu_kien.md` (ngoài phạm vi hiện tại) |
| `dien_thoai` | OPPO Reno14 | **Dải màu, độ phân giải & tốc độ khung hình video** | `100% DCI-P3` (ở 3 chế độ màu); video `4K 60/30 fps`, `SLO-MO 1080P 480/120fps`, `720P 960/240fps` tách camera `Sau`/`Trước` | Ngoài phạm vi 8 thuộc tính điện thoại |
| `dien_thoai` | OPPO Reno14 | **Thời lượng duy trì ổn định FPS / tản nhiệt khi chơi game & cảm ứng găng tay** | `MOBA Game: 120FPS, 3 Giờ`; `25℃, 10 Giờ`; `35℃, 8 Giờ` (nhiệt độ vỏ `< 41℃`); cảm ứng găng tay dày `trong vòng 5mm`; hiệu suất chip CPU `+20%`, GPU `+60%`, NPU `+230%` | Bài thử độ ổn định khung hình/nhiệt độ và tính năng phụ |

---

## 5. Những chỗ chưa chắc chắn, biên phân loại và bất thường trên trang hãng

1. **Ba cụm gán `khong_ro` trong `cum_3_san_pham.json`:**
   - `"Từ 1-100%"` (`OPPO Reno14`, `sac_nhanh`, giá trị `48 phút`): `dieu_kien_so.moc_phan_tram` nhận ra đích `100%` theo đơn vị `%`, nhưng làm rơi mất mốc xuất phát `1%` (khác quy ước ngầm `0%` cạn pin của Apple/Xiaomi); hơn nữa ngay ở phần FAQ cùng trang, khi viết thành `"từ 1% đến 100%"`, bộ trích xuất gặp hai số `%` nên báo `xung_dot`.
   - `"(Tiêu chuẩn)"` gắn với `Độ sáng bình thường: 600nits (Tiêu chuẩn)` (`OPPO Reno14`, `do_sang`): về mặt chữ thì khớp `dien_thoai.yaml: cach_dien_dat.che_do_hien_thi.tieu_chuan`, nhưng đặt cạnh dòng kế tiếp `HBM: 1200nits (Tiêu chuẩn)` thì thấy rõ bản tiếng Việt của OPPO dùng `(Tiêu chuẩn)` để dịch `(Typical)` (`kieu_gia_tri: dien_hinh`), không phải tên chế độ hiển thị.
   - `"không được thiết kế để lặn chuyên nghiệp"` (`OPPO Reno14`, `khang_nuoc`, `IP69`): chứa từ `"lặn"` có trong `hoat_dong_bi_cam.di_bien_di_boi`, nhưng OPPO chỉ cấm *lặn chuyên nghiệp* trong khi vẫn quảng cáo chụp ảnh/quay video dưới nước ngọt tối đa `2 mét / 30 phút`.

2. **Biên giữa cụm ngữ cảnh thử nghiệm và điều kiện quyết định:**
   - Cụm `"cài đặt mặc định"` lặp ở cả 6 dòng phát nhạc của `OPPO Enco Air5 Pro` (`Thời gian phát nhạc (AAC, cài đặt mặc định, âm lượng 50%, ...)`) và cụm `"nhiệt độ phòng"` / `"nhiệt độ 25°C"` khi sạc được xếp là ngữ cảnh quy trình thử chuẩn (tương tự `tn-samsung-buds3pro#038` trong `bao_phu_dieu_kien.md`) nên không đưa vào mẫu số điều kiện quyết định. Tuy nhiên, vì các cụm này **chưa có mặt trong `chung.yaml: ngu_canh_khong_quyet_dinh`**, nếu LLM trích chúng ở Bước 22 thì `hieu_dieu_kien` hiện tại sẽ đẩy vào `dieu_kien_khac` và chặn thành `D1a`. Nên bổ sung `"cài đặt mặc định"`, `"nhiệt độ phòng"`, `"nhiệt độ 25°C"` vào `ngu_canh_khong_quyet_dinh`.

3. **Biên so khớp hậu tố của `tim_kieu_gia_tri` so với so khớp nguyên cụm:**
   - Các cụm `"lên tới"` (`OPPO Reno14`, `120Hz`), `"Lên tới"` (`Galaxy Watch Ultra2`, `5000 nits`, `40 %`) và `"xuống đến"` (`Galaxy Watch Ultra2`, `40 mét`) được tính là `nhan_ra` vì hàm `tim_kieu_gia_tri` hiện hành trong `src/kiemchung/chuan_hoa.py` khớp từ cuối `"tới"` / `"đến"` đứng liền trước con số. Nếu chấm chặt theo khớp toàn bộ chuỗi sau chuẩn hóa, 4 lượt này chuyển sang `khong_nhan_ra` và tỷ lệ bao phủ giảm tiếp còn **74 / 168 (44,0%)** — không làm thay đổi kết luận. Vẫn nên thêm thẳng `"lên tới"` và `"xuống đến"` vào `chung.yaml: kieu_gia_tri.toi_da`.

4. **Phân biệt thời lượng pin với thời lượng ổn định khung hình / sạc nhanh dạng 2 trên `OPPO Reno14`:**
   - Khối tản nhiệt / HyperBoost 2.0 trên trang `OPPO Reno14` có các dòng `MOBA Game: 120FPS, 3 Giờ Chơi Mượt Mà`, `FPS Game: 60FPS, 3 Giờ Chơi Mượt Mà` (chú thích 15 ghi rõ số này đo trên **Reno14 Pro 5G**, không phải Reno14 5G), `MOBA Game: 25℃, 10 Giờ` và `35℃, 8 Giờ`. Đọc chú thích 14–15 cho thấy đây là thời gian duy trì ổn định tốc độ khung hình và nhiệt độ vỏ `< 41℃`, nên được xếp vào mục 4 thay vì `thoi_luong_pin` (riêng con số `10 Giờ MOBA Game` nằm trong khối `6000mAh Pin Lớn` với chú thích 21 được tính vào `thoi_luong_pin`). Tương tự, dòng `12.8 Giờ Liên Lạc / 10 Phút sạc` thuộc sạc nhanh dạng 2 chưa khai báo cho điện thoại; nếu gộp cả 2 cụm điều kiện của dòng này vào mẫu số, tỷ lệ của `OPPO Reno14` là `18 / 41 (43,9%)` và tổng 3 sản phẩm là `78 / 170 (45,9%)`.

5. **Ba mâu thuẫn / lỗi biên tập ngay trên trang chính hãng Việt Nam (đáng lưu ý cho xử lý `D1b` và chuẩn hóa số):**
   - **Dịch ngược Định mức / Điển hình trên OPPO Reno14:** Trang thông số ghi `Giá trị định mức: 6000mAh/ 23.52Wh` và `Giá trị tiêu chuẩn: 5840mAh/22.90Wh` (theo vật lý pin IEC 61960, số nhỏ `5840mAh` mới là Rated/Định mức và số lớn `6000mAh` là Typical/Thông thường — đúng như chú thích 18 ở trang sản phẩm ghi `6000mAh (giá trị thông thường)`).
   - **Mâu thuẫn môi trường nước trên OPPO Reno14:** Chú thích 10 ghi *"Khả năng chống nước của thiết bị chỉ hỗ trợ nước ngọt, vui lòng không đặt điện thoại di động vào nước biển mà không có vỏ bảo vệ"*, nhưng câu trả lời FAQ trên cùng trang lại viết *"máy luôn sẵn sàng sử dụng khi ở hồ bơi, bãi biển"*.
   - **Lỗi gõ thông số trên OPPO Enco Air5 Pro:** (a) Thẻ tóm tắt trên trang sản phẩm ghi trùng `Chế độ AAC. ANC OFF(Chỉ tai nghe)` cho cả `13 Giờ` lẫn `7 Giờ` (trong khi bảng thông số ghi `7 giờ` là `Bật ANC`); (b) bảng thông số đàm thoại gõ thừa khoảng trắng giữa số thập phân `"5 .5h"`, khiến biểu thức chính quy đọc số hiện tại không nhận ra `5.5` mà tách rời `5` và `.5h`.
