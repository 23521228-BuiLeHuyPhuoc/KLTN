# Kiểm việc bỏ ký hiệu chú thích khỏi noi_dung (31/10/2026)

Số chú thích của trang hãng (trên web là chữ số nhỏ in cao: `Thấp8`, `20 phút6`, ` 1, 4, 5` ở cuối dòng) và dấu `*`, `**` làm ký hiệu chú thích đã bị bỏ khỏi `noi_dung` của `data/nguon/<ma_mau>/doan.jsonl`; `noi_dung_goc` giữ văn bản trước khi bỏ, từng byte. Phần lớn là các khoảng mà `chia_doan` đã dùng để gắn chú thích vào đoạn (`chuan_bi_manh`), không có bộ nhận diện riêng; ký hiệu thật mà nhận diện đó bỏ sót thì bỏ thêm bằng bảng ghi tay `KY_HIEU_BO_THEM` (mục 7). Số trong tên mã (`IP68`, `Buds3`, `A2305`), số liệu (`5.000mAh`) và `USB-C` không phải ký hiệu nên còn nguyên. Ba ngoại lệ cho dấu `*` mà `chia_doan` vẫn nhận ra (để gắn chú thích) nhưng không bỏ: dấu `*` mà trang không có dòng chú thích nào bắt đầu bằng đúng chuỗi đó, dấu `*` đứng giữa hai khoảng trắng (nhãn đọc màn hình "Chú thích * biểu tượng" của Apple), và `5*` trong lời đánh giá (điểm 5 sao) giữ lại bằng bảng ghi tay `KY_HIEU_GIU_LAI`. Báo cáo này do `scripts/kiem_bo_so_chu_thich.py` sinh ra; mục 4 đến 6 là việc để người kiểm xem, mục 7 liệt kê hai bảng ghi tay.

## Bất biến đã kiểm bằng code

- Bản sinh lại từ `page.txt`/`page.html` giống `doan.jsonl` trên đĩa từng byte: **đạt**.
- `noi_dung_goc` bằng `noi_dung` của bản git `0d95e46` (trước khi bỏ ký hiệu) cho mọi đoạn, và `id`, `ma_mau`, `trang`, `muc`, `chu_thich`, `dong`, số đoạn, thứ tự không đổi: **đạt**.
- Với mọi đoạn, bỏ các ký hiệu đã ghi nhận khỏi `noi_dung_goc` ra đúng `noi_dung` (không kể khoảng trắng; khoảng trắng chỉ đổi ở các chỗ ghi ở mục 2), đoạn không có ký hiệu thì `noi_dung` = `noi_dung_goc`: **đạt**.

## 1. Bảng tổng

| Mẫu | Đoạn | Đoạn đổi | Chỗ xóa | Ký hiệu số | Ký hiệu sao `*` | Sao mở chú thích nối liền | Số bỏ bằng bảng ghi tay |
|---|---:|---:|---:|---:|---:|---:|---:|
| dt-apple-iphone17 | 51 | 20 | 34 | 31 | 2 | 0 | 1 |
| dt-xiaomi-15t | 60 | 14 | 48 | 20 | 0 | 15 | 14 |
| tn-samsung-buds3pro | 69 | 20 | 27 | 94 | 0 | 0 | 0 |
| dh-apple-watchse3 | 29 | 13 | 28 | 27 | 0 | 0 | 1 |
| dt-oppo-findx8 | 69 | 13 | 17 | 17 | 0 | 0 | 0 |
| dt-samsung-galaxys25ultra | 166 | 34 | 47 | 58 | 0 | 0 | 15 |
| dt-xiaomi-redminote14proplus5g | 70 | 15 | 21 | 0 | 15 | 6 | 0 |
| tn-apple-airpodspro3 | 22 | 12 | 32 | 32 | 0 | 0 | 0 |
| tn-apple-airpods4 | 12 | 7 | 16 | 16 | 0 | 0 | 0 |
| tn-xiaomi-redmibuds6pro | 32 | 10 | 22 | 0 | 22 | 0 | 0 |
| dh-samsung-galaxywatch8 | 626 | 27 | 29 | 61 | 0 | 0 | 1 |
| dh-xiaomi-watchs4 | 39 | 5 | 16 | 0 | 16 | 0 | 0 |
| **Cộng** | **1245** | **190** | **337** | **356** | **55** | **21** | **32** |

- Chỗ xóa là một cụm liền nhau (`14, 15` là một chỗ, hai ký hiệu số). Ký hiệu sao là dấu `*`/`**` đứng sau chữ làm ký hiệu (`IP68**`, `24 tháng.*`); sao mở chú thích nối liền là dấu `*` dính liền chữ sau mà `chia_doan` đã bóc nội dung chú thích đó đi (`194g*`, `Hz**`), nội dung chú thích nằm ở `chu_thich`. Cột cuối là số ký hiệu số bỏ bằng bảng ghi tay (đã tính vào Chỗ xóa, không tính vào cột Ký hiệu số).
- Đoạn Galaxy Watch8 phần lớn lấy từ PDF hướng dẫn sử dụng nên không có ký hiệu để bỏ; chỉ trang chính (`url`) có.

## 2. Chỗ chỉnh khoảng trắng khi bỏ

- Ký hiệu dính liền chữ sau không có khoảng trắng (`2.560Hz**Gam màu`), đã chèn một dấu cách để hai chữ không dính nhau: **3** chỗ.
  - `dt-xiaomi-15t#004` `**`: `…ấy mẫu cảm ứng tức thì 2.560Hz⟦**⟧Gam màu: DCI-P3 Độ sâu màu: 68…` -> `…y mẫu cảm ứng tức thì 2.560Hz ⟦⟧Gam màu: DCI-P3 Độ sâu màu: 68…`
  - `dt-xiaomi-15t#011` `**`: `…o SIM + eSIM hoặc eSIM + eSIM)⟦**⟧Băng tần mạng: GSM: 2/3/5/8 WC…` -> `… SIM + eSIM hoặc eSIM + eSIM) ⟦⟧Băng tần mạng: GSM: 2/3/5/8 WC…`
  - `dt-xiaomi-redminote14proplus5g#007` `*`: `…nano SIM hoặc nano SIM + eSIM)⟦*⟧Bluetooth 5.4 Wi-Fi: Wi-Fi 6/6…` -> `…ano SIM hoặc nano SIM + eSIM) ⟦⟧Bluetooth 5.4 Wi-Fi: Wi-Fi 6/6…`
- Ký hiệu nằm giữa hai dấu cách: bỏ một dấu cách để còn đúng một, **0** chỗ.
- Ký hiệu cuối dòng đứng sau một dấu cách (`năng lượng! 7`): bỏ luôn dấu cách đó, **66** chỗ (không liệt kê).

## 3. Danh sách đầy đủ từng chỗ đã xóa (337 chỗ)

Mỗi dòng: mã đoạn, loại, ký hiệu đã xóa, ngữ cảnh khoảng 30 ký tự mỗi bên (`⟦…⟧` là chỗ xóa, `⏎` là xuống dòng).

### dt-apple-iphone17 (34 chỗ)

- `dt-apple-iphone17#002` · sao `*` · `…1.181.000đ/th. trong 24 tháng.⟦*⟧⏎Chú thích * biểu tượng⏎Mua⏎Tổ…`
- `dt-apple-iphone17#002` · số `1` · `… Oải Hương)⏎Dung Lượng Lưu Trữ⟦1⟧⏎256GB⏎512GB`
- `dt-apple-iphone17#003` · số `2` · `Kích Thước Và Trọng Lượng⟦2⟧⏎Rộng:⏎71,5 mm⏎Cao:⏎149,6 mm⏎D…`
- `dt-apple-iphone17#007` · số `3` · `…Nước, Chống Nước, Và Chống Bụi⟦3⟧⏎Đạt mức IP68 (chống nước ở độ…`
- `dt-apple-iphone17#007` · số `4` · `…ăng hữu ích trên các ứng dụng.⟦4⟧⏎Tìm hiểu thêm⏎Chip`
- `dt-apple-iphone17#016` · số `5` · `Pin Và Nguồn Điện⟦5⟧⏎Thời gian xem video⏎Lên đến 3…`
- `dt-apple-iphone17#016` · số `6` · `…⏎Sạc lên đến 50% trong 20 phút⟦6⟧ với bộ tiếp hợp 40W trở lên (…`
- `dt-apple-iphone17#016` · số (ghi tay) `6` · `…⏎Sạc lên đến 50% trong 30 phút⟦6⟧ với bộ tiếp hợp 30W trở lên s…`
- `dt-apple-iphone17#017` · số `7` · `…SOS Khẩn Cấp⏎Phát Hiện Va Chạm⟦7⟧⏎Mạng Di Động Và Không Dây⏎Phi…`
- `dt-apple-iphone17#017` · sao `**` · `…g Và Không Dây⏎Phiên bản A3520⟦**⟧⏎FDD-5G NR (Băng tần n1, n2, n…`
- `dt-apple-iphone17#017` · số `8` · `…z)⏎5G (sub-6 GHz) với 4x4 MIMO⟦8⟧⏎LTE Gigabit với 4x4 MIMO8⏎Chi…`
- `dt-apple-iphone17#017` · số `8` · `…MIMO8⏎LTE Gigabit với 4x4 MIMO⟦8⟧⏎Chip mạng không dây Apple N1`
- `dt-apple-iphone17#018` · số `9` · `…i-Fi 7 (802.11be) với 2x2 MIMO⟦9⟧⏎Bluetooth 6⏎Công nghệ mạng Th…`
- `dt-apple-iphone17#018` · số `10` · `…le Ultra Wideband thế hệ thứ 2⟦10⟧⏎NFC có chế độ đọc⏎Thẻ Truy Cậ…`
- `dt-apple-iphone17#020` · số `11` · `…mera, Trí Thông Minh Thị Giác,⟦11⟧ Đèn Pin, Ghi Âm, Nhận Dạng Nh…`
- `dt-apple-iphone17#021` · số `6` · `… không dây MagSafe lên đến 25W⟦6⟧⏎Sạc không dây Qi2 lên đến 25W…`
- `dt-apple-iphone17#021` · số `6` · `…⏎Sạc không dây Qi2 lên đến 25W⟦6⟧⏎Dãy nam châm⏎Nam châm căn chỉ…`
- `dt-apple-iphone17#022` · số `12` · `…SIM⏎SIM kép (nano SIM và eSIM)⟦12⟧⏎Hỗ trợ eSIM kép12⏎Tìm hiểu th…`
- `dt-apple-iphone17#022` · số `12` · `…SIM và eSIM)12⏎Hỗ trợ eSIM kép⟦12⟧⏎Tìm hiểu thêm về eSIM⏎Tìm hiể…`
- `dt-apple-iphone17#024` · số `13` · `Gọi Video⟦13⟧⏎Gọi video FaceTime qua mạng d…`
- `dt-apple-iphone17#025` · số `13` · `…u nhỏ với camera sau⏎Gọi Thoại⟦13⟧⏎FaceTime âm thanh⏎Gọi Wi-Fi8⏎…`
- `dt-apple-iphone17#025` · số `8` · `…13⏎FaceTime âm thanh⏎Gọi Wi-Fi⟦8⟧⏎SharePlay⏎Chia sẻ màn hình`
- `dt-apple-iphone17#027` · số `14` · `… bộ chuyển đổi được bán riêng)⟦14⟧`
- `dt-apple-iphone17#028` · số `15` · `Siri⟦15⟧⏎Nhận trợ giúp thực hiện các c…`
- `dt-apple-iphone17#029` · số `4` · `…ri tự nhiên hơn và hữu ích hơn⟦4⟧⏎Tìm hiểu thêm về Siri`
- `dt-apple-iphone17#036` · số `16` · `…ố tính năng)⏎Truy cập Internet⟦16⟧⏎Quá trình đồng bộ hóa với Mac…`
- `dt-apple-iphone17#040` · số `17` · `… giảm tác động đến môi trường:⟦17⟧`
- `dt-apple-iphone17#042` · số `18` · `…c làm từ 30% vật liệu tái chế,⟦18⟧ bao gồm:⏎85% nhôm trong vỏ má…`
- `dt-apple-iphone17#043` · số `19` · `…e 17 đến từ nguồn điện tái tạo⟦19⟧⏎Vượt yêu cầu của Bộ Năng Lượn…`
- `dt-apple-iphone17#043` · số `20` · `…ỳ dành cho hệ thống bộ sạc pin⟦20⟧⏎Bao Bì⏎100% bao bì được làm t…`
- `dt-apple-iphone17#043` · số `21` · `…Bì⏎100% bao bì được làm từ sợi⟦21⟧⏎Bao bì của iPhone 17 được thi…`
- `dt-apple-iphone17#043` · số `22` · `…thiết bị trong mỗi chuyến hàng⟦22⟧`
- `dt-apple-iphone17#044` · số `23` · `…Trình Không Rác Thải của Apple⟦23⟧⏎Sử dụng hóa chất thông minh h…`
- `dt-apple-iphone17#045` · số `25` · `… điểm tín dụng mua iPhone mới.⟦25⟧ Tốt cho cả bạn và môi trường.…`

### dt-xiaomi-15t (48 chỗ)

- `dt-xiaomi-15t#002` · sao nối liền `*` · `…DDR5X 8533Mbps Bộ nhớ: UFS 4.1⟦*⟧⏎Kích thước⏎Chiều cao: 163,2mm…`
- `dt-xiaomi-15t#002` · sao nối liền `*` · `… dày: 7,50mm Trọng lượng: 194g⟦*⟧`
- `dt-xiaomi-15t#004` · sao nối liền `**` · `…ấy mẫu cảm ứng tức thì 2.560Hz⟦**⟧Gam màu: DCI-P3 Độ sâu màu: 68…`
- `dt-xiaomi-15t#005` · sao nối liền `*` · `…ợ PD3.0 / PD2.0 Cổng sạc USB-C⟦*⟧*`
- `dt-xiaomi-15t#005` · sao nối liền `*` · `… PD3.0 / PD2.0 Cổng sạc USB-C*⟦*⟧`
- `dt-xiaomi-15t#010` · sao nối liền `*` · `… kiếm bằng GoogleGoogle Gemini⟦*⟧****⏎Hệ thống tản nhiệt⏎Hệ thố…`
- `dt-xiaomi-15t#010` · sao nối liền `*` · `…kiếm bằng GoogleGoogle Gemini*⟦*⟧***⏎Hệ thống tản nhiệt⏎Hệ thốn…`
- `dt-xiaomi-15t#010` · sao nối liền `*` · `…iếm bằng GoogleGoogle Gemini**⟦*⟧**⏎Hệ thống tản nhiệt⏎Hệ thống…`
- `dt-xiaomi-15t#010` · sao nối liền `*` · `…ếm bằng GoogleGoogle Gemini***⟦*⟧*⏎Hệ thống tản nhiệt⏎Hệ thống …`
- `dt-xiaomi-15t#010` · sao nối liền `*` · `…m bằng GoogleGoogle Gemini****⟦*⟧⏎Hệ thống tản nhiệt⏎Hệ thống X…`
- `dt-xiaomi-15t#011` · sao nối liền `**` · `…o SIM + eSIM hoặc eSIM + eSIM)⟦**⟧Băng tần mạng: GSM: 2/3/5/8 WC…`
- `dt-xiaomi-15t#011` · sao nối liền `**` · `…5/77/78 Mạng không dây Wi-Fi 6⟦**⟧*`
- `dt-xiaomi-15t#011` · sao nối liền `*` · `…77/78 Mạng không dây Wi-Fi 6**⟦*⟧`
- `dt-xiaomi-15t#012` · sao nối liền `**` · `…hả năng chống bụi và nước⏎IP68⟦**⟧⏎Phát video và âm thanh⏎Loa ké…`
- `dt-xiaomi-15t#014` · sao nối liền `*` · `…h và Thẻ bảo hành / Túi hút ẩm⟦*⟧`
- `dt-xiaomi-15t#035` · số `3` · `…iúp tránh mệt mỏi khi sử dụng.⟦3⟧⏎Xuất sắc từ trong ra ngoài⏎Bề…`
- `dt-xiaomi-15t#035` · số `4` · `…năng chống nước đến độ sâu 3m.⟦4⟧⏎Tăng cường⏎Khả năng chống trầ…`
- `dt-xiaomi-15t#035` · số (ghi tay) `5` · `…n.⏎Bộ sưu tập Gold Collection ⟦5⟧`
- `dt-xiaomi-15t#037` · số `6` · `…ơng phản⏎5000000:1⏎Tần số quét⟦6⟧⏎120Hz⏎Tốc độ lấy mẫu cảm ứng⏎…`
- `dt-xiaomi-15t#037` · số `7` · `…Tốc độ lấy mẫu cảm ứng tức thì⟦7⟧⏎2560Hz⏎Màn hình siêu sáng 3.2…`
- `dt-xiaomi-15t#039` · số `8` · `…m cho cả thị giác và cảm giác.⟦8⟧⏎+13%⏎Viền hẹp hơn8⏎Bảo vệ mắt…`
- `dt-xiaomi-15t#039` · số `8` · `…à cảm giác.8⏎+13%⏎Viền hẹp hơn⟦8⟧⏎Bảo vệ mắt mọi lúc⏎Tự nhiên v…`
- `dt-xiaomi-15t#041` · số `9` · `…à hình ảnh trên toàn hệ thống.⟦9⟧⏎Nhận dạng giọng nói AI10⏎Phiê…`
- `dt-xiaomi-15t#041` · số `10` · `…thống.9⏎Nhận dạng giọng nói AI⟦10⟧⏎Phiên dịch AI10⏎Tìm kiếm AI10…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…g giọng nói AI10⏎Phiên dịch AI⟦10⟧⏎Tìm kiếm AI10⏎Hình nền động A…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…10⏎Phiên dịch AI10⏎Tìm kiếm AI⟦10⟧⏎Hình nền động AI10⏎Viết AI10⏎…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…Tìm kiếm AI10⏎Hình nền động AI⟦10⟧⏎Viết AI10⏎Nhận dạng giọng nói…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…I10⏎Hình nền động AI10⏎Viết AI⟦10⟧⏎Nhận dạng giọng nói AI10⏎Phiê…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…ết AI10⏎Nhận dạng giọng nói AI⟦10⟧⏎Phiên dịch AI10⏎Tìm kiếm AI10…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…g giọng nói AI10⏎Phiên dịch AI⟦10⟧⏎Tìm kiếm AI10⏎Hình nền động A…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…10⏎Phiên dịch AI10⏎Tìm kiếm AI⟦10⟧⏎Hình nền động AI10⏎Viết AI10⏎…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…Tìm kiếm AI10⏎Hình nền động AI⟦10⟧⏎Viết AI10⏎Nhận dạng giọng nói…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…I10⏎Hình nền động AI10⏎Viết AI⟦10⟧⏎Nhận dạng giọng nói AI10⏎Phiê…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…ết AI10⏎Nhận dạng giọng nói AI⟦10⟧⏎Phiên dịch AI10⏎Tìm kiếm AI10…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…g giọng nói AI10⏎Phiên dịch AI⟦10⟧⏎Tìm kiếm AI10⏎Hình nền động A…`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…10⏎Phiên dịch AI10⏎Tìm kiếm AI⟦10⟧⏎Hình nền động AI10`
- `dt-xiaomi-15t#041` · số (ghi tay) `10` · `…Tìm kiếm AI10⏎Hình nền động AI⟦10⟧`
- `dt-xiaomi-15t#045` · số `11` · `…ắn tin khi đang di chuyển⏎+49%⟦11⟧⏎Cầm ngang⏎Chơi game hoặc xem …`
- `dt-xiaomi-15t#045` · số `11` · `…⏎Chơi game hoặc xem video⏎+63%⟦11⟧⏎Cầm khi gọi điện⏎Kê sát vào t…`
- `dt-xiaomi-15t#045` · số `11` · `…sát vào tai trong khi gọi⏎+26%⟦11⟧⏎Hiệu suất vượt trội⏎Khả năng …`
- `dt-xiaomi-15t#047` · số `13` · `… lâu dài.⏎≥80%⏎1600 chu kỳ sạc⟦13⟧⏎Tối đa 13,19 giờ⏎Sử dụng liên…`
- `dt-xiaomi-15t#047` · số `14` · `… đa 13,19 giờ⏎Sử dụng liên tục⟦14⟧⏎Sạc nhanh HyperCharge 67W15⏎5…`
- `dt-xiaomi-15t#047` · số `15` · `…ục14⏎Sạc nhanh HyperCharge 67W⟦15⟧⏎50 phút sạc đầy 100%14⏎Hệ thố…`
- `dt-xiaomi-15t#047` · số `14` · `…rge 67W15⏎50 phút sạc đầy 100%⟦14⟧⏎Hệ thống Xiaomi 3D IceLoop`
- `dt-xiaomi-15t#048` · số `16` · `…ịnh.⏎+13%⏎Diện tích bề mặt LHP⟦16⟧⏎+11%⏎Tấm than chì trên khung …`
- `dt-xiaomi-15t#048` · số `16` · `…%⏎Tấm than chì trên khung giữa⟦16⟧⏎Các tính năng khác⏎Máy quét v…`
- `dt-xiaomi-15t#048` · số `17, 18` · `…kép chuẩn Dolby Atmos®⏎Wi-Fi 6⟦17, 18⟧⏎Bluetooth 6.0⏎NFC đa chức năn…`
- `dt-xiaomi-15t#048` · số `19` · `…ạn nhiều dịch vụ VIP/Đặc quyền⟦19⟧⏎3 tháng trải nghiệm⏎miễn phí …`

### tn-samsung-buds3pro (27 chỗ)

- `tn-samsung-buds3pro#006` · số `1, 2, 3` · `… dưới góc nhìn hoàn toàn mới. ⟦1, 2, 3⟧`
- `tn-samsung-buds3pro#007` · số `4, 5, 9` · `…i thanh ánh sáng Blade Lights ⟦4, 5, 9⟧⏎Cặp tai nghe Galaxy Buds3 Pro…`
- `tn-samsung-buds3pro#007` · số `6` · `…m chìm nhờ chất âm tuyệt đỉnh ⟦6⟧⏎Nhiều đường kẻ tạo ra các hìn…`
- `tn-samsung-buds3pro#008` · số `7, 8` · `Adaptive Noise Control ⟦7, 8⟧⏎Một chiếc tai nghe Galaxy Bud…`
- `tn-samsung-buds3pro#009` · số `2, 3, 10` · `…được tính chỉnh bởi Galaxy AI ⟦2, 3, 10⟧⏎Galaxy AI đã có mặt⏎" Tai ngh…`
- `tn-samsung-buds3pro#011` · số `1, 4, 5` · `…iết kế ấn tượng hoàn toàn mới ⟦1, 4, 5⟧⏎Thiết kế công thái học cùng c…`
- `tn-samsung-buds3pro#011` · số `1, 4, 11, 12` · `…B-C và khả năng sạc tai nghe. ⟦1, 4, 11, 12⟧`
- `tn-samsung-buds3pro#013` · số `1` · `… luôn chắc chắn không bị rơi. ⟦1⟧`
- `tn-samsung-buds3pro#015` · số `1` · `…nghĩa lại âm thanh nguyên bản ⟦1⟧⏎Nhiều đường kẻ tạo ra các hìn…`
- `tn-samsung-buds3pro#017` · số `1, 13` · `…ng trên các tần số khác nhau. ⟦1, 13⟧⏎Loa 2 chiều được nâng cấp⏎Khá…`
- `tn-samsung-buds3pro#017` · số `1, 13` · `…mà lẽ ra đã không được chú ý. ⟦1, 13⟧`
- `tn-samsung-buds3pro#018` · số `1, 6` · `…ức tạp đúng như âm thanh gốc. ⟦1, 6⟧⏎16bit / 44.1kHz⏎24bit / 96kHz…`
- `tn-samsung-buds3pro#018` · số `1, 2, 10, 14, 15, 16` · `…n tai nghe Buds hoàn toàn mới ⟦1, 2, 10, 14, 15, 16⟧`
- `tn-samsung-buds3pro#019` · số `1, 17` · `…phù hợp với độ chính xác cao. ⟦1, 17⟧`
- `tn-samsung-buds3pro#020` · số `1, 7, 8, 18, 40` · `…h, mà không lo bị ngắt quãng. ⟦1, 7, 8, 18, 40⟧⏎Một chiếc tai nghe Galaxy Bud…`
- `tn-samsung-buds3pro#025` · số `2, 3, 9, 10, 19, 20, 21` · `…sự vượt qua rào cản ngôn ngữ. ⟦2, 3, 9, 10, 19, 20, 21⟧⏎Chế độ nghe⏎Chế độ hội thoại⏎…`
- `tn-samsung-buds3pro#028` · số `1, 54, 55` · `…ộc gọi Bluetooth thông thường ⟦1, 54, 55⟧⏎Đến ngay TV 360 Audio⏎Chìm đắ…`
- `tn-samsung-buds3pro#028` · số `1, 22, 23` · `…nh nghe và xem sống động hơn. ⟦1, 22, 23⟧`
- `tn-samsung-buds3pro#029` · số `9, 24` · `…m việc và vui chơi liền mạch. ⟦9, 24⟧`
- `tn-samsung-buds3pro#031` · số `56, 57, 58, 59` · `… ứng dụng đang phát nội dung. ⟦56, 57, 58, 59⟧⏎Dù bạn thích chế độ 360 Audio…`
- `tn-samsung-buds3pro#034` · số `9, 25, 26, 27, 28` · `…ơng tác với những người khác. ⟦9, 25, 26, 27, 28⟧⏎Điều khiển⏎dễ dàng với⏎câu lệ…`
- `tn-samsung-buds3pro#034` · số `9, 19, 29, 30, 31, 41` · `…3 pro thực hiện phần còn lại. ⟦9, 19, 29, 30, 31, 41⟧⏎Tận hưởng không gian bình yên…`
- `tn-samsung-buds3pro#035` · số `9, 19, 32, 42, 43` · `…ạnh phúc hơn, khỏe khoắn hơn. ⟦9, 19, 32, 42, 43⟧`
- `tn-samsung-buds3pro#037` · số `44, 45, 46, 47, 48, 49, 50, 51, 52, 53` · `…h các tính năng theo ý thích. ⟦44, 45, 46, 47, 48, 49, 50, 51, 52, 53⟧⏎Ứng dụng Galaxy Wearable⏎Ứng …`
- `tn-samsung-buds3pro#037` · số `1` · `…th⏎Sẵn sàng cho mọi cuộc chơi ⟦1⟧`
- `tn-samsung-buds3pro#038` · số `33, 34, 35, 36, 37` · `…nào và bất cứ nơi nào bạn đi. ⟦33, 34, 35, 36, 37⟧⏎Thời gian phát⏎Tắt Tính năng …`
- `tn-samsung-buds3pro#039` · số `37, 38, 39` · `…⏎Galaxy Buds lý tưởng với bạn ⟦37, 38, 39⟧⏎Bạc⏎Trắng⏎BUY NOW⏎Bạc⏎Trắng⏎B…`

### dh-apple-watchse3 (28 chỗ)

- `dh-apple-watchse3#003` · số `1` · `…mạnh mẽ với Apple Intelligence⟦1⟧`
- `dh-apple-watchse3#004` · số (ghi tay) `1` · `…⏎Apple Intelligence và Siri AI⟦1⟧⏎Apple Intelligence thế hệ mới…`
- `dh-apple-watchse3#005` · số `2` · `…thế hệ thứ 2⏎Cảm biến nhiệt độ⟦2⟧⏎La bàn⏎Cao độ kế luôn bật⏎Gia…`
- `dh-apple-watchse3#006` · số `3` · `… thấp⏎Thông báo nhịp không đều⟦3⟧⏎Ứng dụng Theo Dõi Chu Kỳ tiên…`
- `dh-apple-watchse3#006` · số `4` · `…đoạn tiền mãn kinh và mãn kinh⟦4⟧⏎Ứng dụng Thuốc5⏎Ứng dụng Chú …`
- `dh-apple-watchse3#006` · số `5` · `…nh và mãn kinh4⏎Ứng dụng Thuốc⟦5⟧⏎Ứng dụng Chú Tâm⏎Ứng dụng Tiế…`
- `dh-apple-watchse3#006` · số `6` · `…gủ⏎Thông báo ngưng thở khi ngủ⟦6⟧⏎Màn Hình`
- `dh-apple-watchse3#007` · số `7` · `…i khả năng chống nứt gấp 4 lần⟦7⟧⏎Độ sáng đỉnh 1000 nit⏎Độ sáng…`
- `dh-apple-watchse3#008` · số `8` · `…18 giờ khi sử dụng bình thường⟦8⟧⏎Lên đến 32 giờ ở Chế Độ Nguồn…`
- `dh-apple-watchse3#008` · số `8` · `…2 giờ ở Chế Độ Nguồn Điện Thấp⟦8⟧⏎Lên đến 7 giờ khi tập luyện n…`
- `dh-apple-watchse3#008` · số `9` · `…7 giờ khi tập luyện ngoài trời⟦9⟧⏎Tích hợp pin sạc lithium-ion⏎…`
- `dh-apple-watchse3#008` · số `10` · `…lithium-ion⏎Khả năng sạc nhanh⟦10⟧`
- `dh-apple-watchse3#009` · số `10` · `…n đến 80% trong khoảng 45 phút⟦10⟧⏎Sạc 15 phút cho thời gian sử …`
- `dh-apple-watchse3#009` · số `11` · `…dụng bình thường lên đến 8 giờ⟦11⟧⏎Sạc 8 phút cho thời gian theo…`
- `dh-apple-watchse3#009` · số `11` · `…heo dõi giấc ngủ lên đến 8 giờ⟦11⟧⏎Tìm hiểu thêm`
- `dh-apple-watchse3#013` · số `12` · `…nh năng tạo lộ trình tùy chỉnh⟦12⟧⏎Các bản đồ địa hình cho hàng …`
- `dh-apple-watchse3#015` · số `13` · `… Tập Khác⏎An Toàn⏎SOS Khẩn Cấp⟦13⟧⏎Phát Hiện Ngã13`
- `dh-apple-watchse3#015` · số `13` · `…n⏎SOS Khẩn Cấp13⏎Phát Hiện Ngã⟦13⟧`
- `dh-apple-watchse3#016` · số `13` · `Phát Hiện Va Chạm⟦13⟧⏎Giám sát tiếng ồn⏎Quay Về⏎Kiể…`
- `dh-apple-watchse3#016` · số `14` · `…ộ sâu 50m (chống nước khi bơi)⟦14⟧⏎Kết Nối⏎Tất cả các phiên bản⏎…`
- `dh-apple-watchse3#016` · số `15` · `…leo, QZSS và BeiDou)⏎Apple Pay⟦15⟧⏎GymKit⏎Phiên bản A3326 và A33…`
- `dh-apple-watchse3#016` · số `16` · `…và A3328⏎Hỗ trợ RedCap cho LTE⟦16⟧⏎FDD-LTE (Băng tần 1, 2, 3, 4,…`
- `dh-apple-watchse3#020` · số `17` · `…c làm từ 40% vật liệu tái chế,⟦17⟧ bao gồm:⏎100% nhôm trong vỏ l…`
- `dh-apple-watchse3#020` · số `18` · `…bì⏎100% bao bì được làm từ sợi⟦18⟧`
- `dh-apple-watchse3#021` · số `19` · `…SE 3 đến từ nguồn điện tái tạo⟦19⟧⏎100% mức tiêu thụ năng lượng …`
- `dh-apple-watchse3#021` · số `20` · `…ia cho các hệ thống bộ sạc pin⟦20⟧⏎Rác thải`
- `dh-apple-watchse3#022` · số `21` · `…Trình Không Rác Thải của Apple⟦21⟧⏎Sử dụng hóa chất thông minh h…`
- `dh-apple-watchse3#022` · số `22` · `…ử dụng hóa chất thông minh hơn⟦22⟧⏎Tất cả vật liệu được sử dụng …`

### dt-oppo-findx8 (17 chỗ)

- `dt-oppo-findx8#023` · số `1` · `… sạc không dây AirVOOCTM 50W. ⟦1⟧⏎Thời thượng. Mạnh Mẽ. Mượt Mà…`
- `dt-oppo-findx8#024` · số `2` · `…giới mới.⏎193g⏎Nhẹ không tưởng⟦2⟧⏎7.85mm⏎Mỏng ấn tượng2⏎6.59"⏎T…`
- `dt-oppo-findx8#024` · số `2` · `…ng tưởng2⏎7.85mm⏎Mỏng ấn tượng⟦2⟧⏎6.59"⏎Tỷ lệ vàng`
- `dt-oppo-findx8#025` · số `2` · `…ưu tỷ lệ màn hình và thân máy.⟦2⟧⏎Trên tay một biểu tượng tinh …`
- `dt-oppo-findx8#029` · số `3` · `…đang⏎diễn ra gần ngay tầm mắt.⟦3⟧⏎1×⏎2×⏎6×⏎30×⏎Camera Tele Tiềm…`
- `dt-oppo-findx8#031` · số `4` · `…chuyển động có nhanh đến đâu. ⟦4⟧⏎Khám phá thư viện ảnh nghệ th…`
- `dt-oppo-findx8#049` · số `5` · `…% cho trải nghiệm phát video. ⟦5⟧⏎3nm`
- `dt-oppo-findx8#051` · số `6` · `…iác quan trong từng trận game.⟦6⟧⏎59.7fps⏎Genshin⏎119.9fps⏎MLBB`
- `dt-oppo-findx8#054` · số `7` · `…hiệm ngày dài đầy năng lượng! ⟦7⟧⏎5630mAh⏎Dung lượng tiêu chuẩn…`
- `dt-oppo-findx8#054` · số `8` · `…chuẩn⏎12%⏎Dung lượng cải thiện⟦8⟧⏎6.5h⏎Quay phim liên tục ở chế…`
- `dt-oppo-findx8#054` · số `9` · `…liên tục ở chế độ Dolby Vision⟦9⟧⏎5.1h⏎-20℃ Quay phim liên tục …`
- `dt-oppo-findx8#054` · số `9` · `…liên tục ở chế độ Dolby Vision⟦9⟧`
- `dt-oppo-findx8#055` · số `10` · `…h hơn, tiện hơn, dễ dàng hơn. ⟦10⟧⏎Phụ Kiện Từ Tính OPPO Mag⏎Chạ…`
- `dt-oppo-findx8#060` · số `11` · `…hi tay bạn và màn hình bị ướt.⟦11⟧⏎IP68⏎IP69⏎Cảm Ứng Kháng Nước⏎…`
- `dt-oppo-findx8#061` · số `13` · `…hoại mượt mà hơn bao giờ hết. ⟦13⟧⏎4500nits⏎Độ sáng tối đa⏎120Hz…`
- `dt-oppo-findx8#062` · số `14` · `…⏎3840Hz⏎PWM Điều chỉnh độ sáng⟦14⟧⏎Tìm Hiểu Thêm`
- `dt-oppo-findx8#065` · số `15` · `… cả khi điện thoại đã bị tắt. ⟦15⟧⏎FAQ⏎Độ bền của Find X8 như th…`

### dt-samsung-galaxys25ultra (47 chỗ)

- `dt-samsung-galaxys25ultra#034` · số (ghi tay) `1` · `…hỉ cần nhấn và ra lệnh là xong⟦1⟧⏎phát⏎Galaxy S25 Ultra nhìn th…`
- `dt-samsung-galaxys25ultra#034` · số (ghi tay) `2,3` · `…roVisual Engine tiên tiến nhất⟦2,3⟧⏎phát`
- `dt-samsung-galaxys25ultra#035` · số (ghi tay) `4` · `…chơi.⏎Thời lượng pin vượt trội⟦4⟧⏎phát⏎Cảnh quan thành phố thay…`
- `dt-samsung-galaxys25ultra#036` · số `5` · `…ột thiết kế táo bạo, hiện đại.⟦5⟧⏎Giới thiệu dòng sản phẩm đầy …`
- `dt-samsung-galaxys25ultra#036` · số (ghi tay) `6` · `…hẩm đầy ấn tượng của chúng tôi⟦6⟧⏎360° loading⏎Xanh Titan⏎Đen T…`
- `dt-samsung-galaxys25ultra#037` · số (ghi tay) `33` · `… dày⏎8.2 mm⏎Trọng lượng⏎218 g ⟦33⟧⏎Galaxy S21 Ultra 5G⏎Độ dày⏎8.…`
- `dt-samsung-galaxys25ultra#037` · số (ghi tay) `33` · `… dày⏎8.9 mm⏎Trọng lượng⏎227 g ⟦33⟧⏎Thiết kế mượt mà, cấu trúc bề…`
- `dt-samsung-galaxys25ultra#038` · số `5` · `…xy S25 Ultra luôn được bảo vệ.⟦5⟧⏎Loại kính cứng nhất của Galax…`
- `dt-samsung-galaxys25ultra#038` · số `7` · `…vệ tốt cho máy Galaxy của bạn.⟦7⟧⏎Kháng nước và bụi⏎Với xếp hạn…`
- `dt-samsung-galaxys25ultra#038` · số `8` · `…ợt trội hơn những gì bạn nghĩ.⟦8⟧⏎Dịch vụ chăm sóc được chứng n…`
- `dt-samsung-galaxys25ultra#038` · số (ghi tay) `34` · `…bởi các chuyên gia của Samsung⟦34⟧⏎Tìm hiểu thêm`
- `dt-samsung-galaxys25ultra#039` · số (ghi tay) `1` · `…hỉ cần nhấn và ra lệnh là xong⟦1⟧⏎phát`
- `dt-samsung-galaxys25ultra#040` · số `1` · `… cập Google Gemini và ra lệnh.⟦1⟧⏎Cách sử dụng Thực hiện tác vụ…`
- `dt-samsung-galaxys25ultra#050` · số `9` · `…phong cách trò chuyện của bạn.⟦9⟧⏎Cách sử dụng Gemini Live`
- `dt-samsung-galaxys25ultra#057` · số `10` · `…i tiết về hoạt động hàng ngày.⟦10⟧⏎Cách sử dụng Now Brief`
- `dt-samsung-galaxys25ultra#072` · số `11` · `… mà không cần chuyển ứng dụng.⟦11⟧⏎Cách sử dụng Khoanh tròn để t…`
- `dt-samsung-galaxys25ultra#083` · số `12` · `…ió và nhiều âm thanh khác nữa.⟦12⟧⏎Cách sử dụng Lọc âm thanh (Au…`
- `dt-samsung-galaxys25ultra#108` · số `13,14` · `…hoạt động và nhịp tim của bạn.⟦13,14⟧⏎Tìm hiểu thêm`
- `dt-samsung-galaxys25ultra#110` · số `15` · `…ại thông minh Galaxy của mình.⟦15⟧⏎Tìm hiểu thêm về Galaxy AI`
- `dt-samsung-galaxys25ultra#111` · số (ghi tay) `3` · `…roVisual Engine tiên tiến nhất⟦3⟧⏎Công nghệ ProVisual Engine th…`
- `dt-samsung-galaxys25ultra#111` · số `16` · `…ảnh tốt nhất từ trước đến nay.⟦16⟧⏎phát⏎Cận cảnh bên trong ống k…`
- `dt-samsung-galaxys25ultra#113` · số `2,3` · `…cảnh quay đêm sẽ bị nhiễu nữa.⟦2,3⟧⏎Những bức chân dung hoành trá…`
- `dt-samsung-galaxys25ultra#113` · số `2` · `… hệt như nhìn bằng mắt thường.⟦2⟧`
- `dt-samsung-galaxys25ultra#114` · số (ghi tay) `3` · `…Tele và thậm chí là Ultra Wide⟦3⟧⏎UW Macro⏎UW⏎Chụp bởi Galaxy S…`
- `dt-samsung-galaxys25ultra#115` · số `3` · `… mang lại độ rõ nét vượt trội.⟦3⟧⏎Space Zoom. Nhìn những thứ bạ…`
- `dt-samsung-galaxys25ultra#115` · số `17,18` · `…âng cao bằng AI của chúng tôi.⟦17,18⟧⏎phát`
- `dt-samsung-galaxys25ultra#117` · số `3,19` · `…rất nhiều chỉnh sửa linh hoạt.⟦3,19⟧⏎Cách sử dụng Expert RAW`
- `dt-samsung-galaxys25ultra#125` · số `20` · `… làm giảm chất lượng hình ảnh.⟦20⟧⏎phát⏎Màn hình chính của Galax…`
- `dt-samsung-galaxys25ultra#126` · số `21,22,23` · `…napdragon® 8 Elite cho Galaxy.⟦21,22,23⟧⏎CPU⏎37⏎xử lý nhanh hơn⏎GPU⏎30…`
- `dt-samsung-galaxys25ultra#128` · số `21,24` · `…n điều chỉnh cài đặt màn hình.⟦21,24⟧⏎Tuổi thọ pin vượt trội⏎Công n…`
- `dt-samsung-galaxys25ultra#128` · số `4` · `…g thức video hàng giờ đồng hồ.⟦4⟧⏎Xem video lên đến⏎31⏎giờ⏎So s…`
- `dt-samsung-galaxys25ultra#128` · số (ghi tay) `4,35` · `…5 Ultra⏎Phát lại Video⏎31 giờ ⟦4,35⟧⏎Galaxy S21 Ultra 5G`
- `dt-samsung-galaxys25ultra#129` · số (ghi tay) `4,35` · `…ân chia⏎Phát lại Video⏎22 giờ ⟦4,35⟧⏎Dung lượng lưu trữ lên đến 1 …`
- `dt-samsung-galaxys25ultra#129` · số `25` · `… đến 256 GB, 512 GB hoặc 1 TB.⟦25⟧⏎One UI 7 hoàn toàn mới, dành …`
- `dt-samsung-galaxys25ultra#131` · số `26` · `… các widget được thiết kế lại.⟦26⟧⏎phát⏎Màn hình chính của Galax…`
- `dt-samsung-galaxys25ultra#133` · số `27,28,29` · `…ụng của mình một cách dễ dàng.⟦27,28,29⟧⏎Tìm hiểu thêm`
- `dt-samsung-galaxys25ultra#136` · số `30` · `…sống thông minh, được kết nối.⟦30⟧⏎Galaxy S25 ∣ S25+⏎Tìm hiểu th…`
- `dt-samsung-galaxys25ultra#139` · số `6` · `…Ngọc Titan và Vàng Hồng Titan.⟦6⟧⏎Đi tới màu sắc`
- `dt-samsung-galaxys25ultra#140` · số `5,21` · `…trải nghiệm xem thoải mái hơn.⟦5,21⟧⏎Đi tới thiết kế`
- `dt-samsung-galaxys25ultra#141` · số `21,31` · `…ải tiến và camera mạnh mẽ hơn.⟦21,31⟧⏎Tìm hiểu thêm và So sánh`
- `dt-samsung-galaxys25ultra#142` · số `1,3,9,10,12` · `…ền mạch trên Galaxy S25 Ultra.⟦1,3,9,10,12⟧⏎Tìm hiểu thêm về Galaxy AI`
- `dt-samsung-galaxys25ultra#146` · số `2,21` · `… mọi khoảng cách, kể cả macro.⟦2,21⟧⏎Đi tới camera`
- `dt-samsung-galaxys25ultra#147` · số `4,32` · `… tận hưởng nhiều giờ giải trí.⟦4,32⟧⏎Đi đến hiệu năng⏎Điều gì khiế…`
- `dt-samsung-galaxys25ultra#147` · số `5,7,8` · `…y xước, bụi và nước hàng ngày.⟦5,7,8⟧⏎Đi tới độ bền`
- `dt-samsung-galaxys25ultra#148` · số `21,22,23` · `… chơi trong thời gian dài hơn.⟦21,22,23⟧⏎Đi đến hiệu năng⏎Điện thoại G…`
- `dt-samsung-galaxys25ultra#149` · số `27,28,29` · `…ị Galaxy mới với Smart Switch.⟦27,28,29⟧⏎Đi tới Switch to Galaxy`
- `dt-samsung-galaxys25ultra#150` · số `15` · `…ọn không tham gia cá nhân hóa.⟦15⟧⏎Đi tới quyền riêng tư`

### dt-xiaomi-redminote14proplus5g (21 chỗ)

- `dt-xiaomi-redminote14proplus5g#002` · sao nối liền `*` · `…và RAM⏎8+256GBLPDDR4X + UFS2.2⟦*⟧⏎Bảo quản ở nơi thoáng mát, kh…`
- `dt-xiaomi-redminote14proplus5g#007` · sao nối liền `*` · `…nano SIM hoặc nano SIM + eSIM)⟦*⟧Bluetooth 5.4 Wi-Fi: Wi-Fi 6/6…`
- `dt-xiaomi-redminote14proplus5g#008` · sao nối liền `*` · `…⏎Hỗ trợ 2x2 MIMO, Wi-Fi Direct⟦*⟧*⏎Chống nước và chống bụi⏎IP68…`
- `dt-xiaomi-redminote14proplus5g#008` · sao nối liền `*` · `…Hỗ trợ 2x2 MIMO, Wi-Fi Direct*⟦*⟧⏎Chống nước và chống bụi⏎IP68*…`
- `dt-xiaomi-redminote14proplus5g#008` · sao nối liền `*` · `…*⏎Chống nước và chống bụi⏎IP68⟦*⟧⏎NFC⏎Có⏎Định vị và điều hướng⏎…`
- `dt-xiaomi-redminote14proplus5g#010` · sao nối liền `*` · `…Thẻ bảo hành/Thông tin an toàn⟦*⟧⏎NHỮNG CHI TIẾT KHÁC⏎Xuất xứ`
- `dt-xiaomi-redminote14proplus5g#035` · sao `*` · `…khả năng bảo vệ đạt chuẩn IP68⟦*⟧ hàng đầu phân khúc, nghĩa là …`
- `dt-xiaomi-redminote14proplus5g#035` · sao `*` · `…trong thời gian tối đa 30 phút⟦*⟧.`
- `dt-xiaomi-redminote14proplus5g#036` · sao `*` · `…ăng chịu lực rơi của mặt trước⟦*⟧⏎Kính Corning® Gorilla® Glass …`
- `dt-xiaomi-redminote14proplus5g#037` · sao `*` · `… năng chịu lực rơi của mặt sau⟦*⟧⏎Mặt lưng kính Corning® Gorill…`
- `dt-xiaomi-redminote14proplus5g#038` · sao `*` · `…tổng thể của thiết bị thêm 10%⟦*⟧ so với thế hệ trước.⏎Gia cố b…`
- `dt-xiaomi-redminote14proplus5g#040` · sao `*` · `…tổng thể của thiết bị thêm 10%⟦*⟧ so với thế hệ trước.⏎Gia cố b…`
- `dt-xiaomi-redminote14proplus5g#042` · sao `*` · `…tổng thể của thiết bị thêm 10%⟦*⟧ so với thế hệ trước.⏎Gia cố b…`
- `dt-xiaomi-redminote14proplus5g#056` · sao `*` · `… bật chế độ Game Turbo.⏎2560Hz⟦*⟧⏎Tốc độ lấy mẫu cảm ứng tức th…`
- `dt-xiaomi-redminote14proplus5g#056` · sao `*` · `…độ lấy mẫu cảm ứng tức thì⏎16X⟦*⟧⏎Độ phân giải cảm ứng siêu cao`
- `dt-xiaomi-redminote14proplus5g#058` · sao `*` · `…rội.⏎30%⏎Nâng cao hiệu suất AI⟦*⟧`
- `dt-xiaomi-redminote14proplus5g#059` · sao `*` · `…cầu sạc thường xuyên.⏎19,5 giờ⟦*⟧⏎Mạng xã hội⏎9 giờ*⏎Xem video …`
- `dt-xiaomi-redminote14proplus5g#059` · sao `*` · `…n.⏎19,5 giờ*⏎Mạng xã hội⏎9 giờ⟦*⟧⏎Xem video phát trực tuyến⏎15 …`
- `dt-xiaomi-redminote14proplus5g#059` · sao `*` · `…m video phát trực tuyến⏎15 giờ⟦*⟧⏎Điều hướng`
- `dt-xiaomi-redminote14proplus5g#062` · sao `*` · `…ho bạn nhiều dịch vụ độc quyền⟦*⟧⏎3 tháng sử dụng Spotify Premi…`
- `dt-xiaomi-redminote14proplus5g#063` · sao `*` · `…nh miễn phí trong vòng 6 tháng⟦*⟧⏎https://www.mi.com/vn/support…`

### tn-apple-airpodspro3 (32 chỗ)

- `tn-apple-airpodspro3#002` · số `1` · `…a từng nghe⏎Âm Thanh Thích Ứng⟦1⟧⏎Chế độ Xuyên Âm2⏎Nhận Biết Cu…`
- `tn-apple-airpodspro3#002` · số `2` · `…anh Thích Ứng1⏎Chế độ Xuyên Âm⟦2⟧⏎Nhận Biết Cuộc Hội Thoại1⏎Tác…`
- `tn-apple-airpodspro3#002` · số `1` · `…n Âm2⏎Nhận Biết Cuộc Hội Thoại⟦1⟧⏎Tách Lời Nói3⏎Âm Lượng Được C…`
- `tn-apple-airpodspro3#002` · số `3` · `…t Cuộc Hội Thoại1⏎Tách Lời Nói⟦3⟧⏎Âm Lượng Được Cá Nhân Hóa4`
- `tn-apple-airpodspro3#002` · số `4` · `…Nói3⏎Âm Lượng Được Cá Nhân Hóa⟦4⟧`
- `tn-apple-airpodspro3#003` · số `5` · `…o dõi chuyển động đầu chủ động⟦5⟧⏎EQ Thích Ứng⏎Ghi âm chất lượn…`
- `tn-apple-airpodspro3#003` · số `6` · `…Thính Giác⏎Kiểm Tra Thính Giác⟦6⟧⏎Thiết Bị Trợ Thính6⏎Giảm Âm T…`
- `tn-apple-airpodspro3#003` · số `6` · `…Thính Giác6⏎Thiết Bị Trợ Thính⟦6⟧⏎Giảm Âm Thanh Lớn`
- `tn-apple-airpodspro3#004` · số `7` · `…heo dõi nhịp tim khi tập luyện⟦7⟧⏎Điều khiển cảm ứng⏎Chip⏎Chip …`
- `tn-apple-airpodspro3#005` · số `8` · `…i cuộc gọi,⏎bật hoặc tắt tiếng⟦8⟧⏎Nhấn một lần để mở điều khiển…`
- `tn-apple-airpodspro3#005` · số `9` · `…ột lần để mở điều khiển camera⟦9⟧⏎Nhấn hai lần để kết thúc cuộc…`
- `tn-apple-airpodspro3#006` · số `4` · `Tương Tác Siri⟦4⟧⏎Chống Bụi,⏎Chống Mồ Hôi⏎Và Ch…`
- `tn-apple-airpodspro3#006` · số `10` · `…ụi,⏎Chống Mồ Hôi⏎Và Chống Nước⟦10⟧⏎Chống bụi, chống mồ hôi và ch…`
- `tn-apple-airpodspro3#006` · số `11` · `…Thước⏎Và Trọng Lượng (Mỗi Bên)⟦11⟧⏎19,2 mm⏎30,9 mm⏎Cao:⏎30,9 mm⏎…`
- `tn-apple-airpodspro3#007` · số `12` · `…oa để sử dụng với ứng dụng Tìm⟦12⟧⏎Pin⏎AirPods Pro 3⏎Thời gian n…`
- `tn-apple-airpodspro3#007` · số `13` · `…n và Theo Dõi Chuyển Động Đầu)⟦13⟧⏎Thời gian nghe lên đến 6,5 gi…`
- `tn-apple-airpodspro3#007` · số `14` · `…n nhịp tim trong khi tập luyện⟦14⟧⏎Thời gian nghe lên đến 10 giờ…`
- `tn-apple-airpodspro3#007` · số `15` · `…g tính năng Thiết Bị Trợ Thính⟦15⟧`
- `tn-apple-airpodspro3#008` · số `16` · `… 3 với Hộp Sạc MagSafe (USB-C)⟦16⟧⏎Thời gian nghe lên đến 24 giờ…`
- `tn-apple-airpodspro3#008` · số `17` · `…ính năng Chủ Động Khử Tiếng Ồn⟦17⟧⏎5 phút để trong hộp sạc có th…`
- `tn-apple-airpodspro3#008` · số `18` · `…ng thời gian nghe khoảng 1 giờ⟦18⟧`
- `tn-apple-airpodspro3#010` · số `6` · `…g bao gồm:⏎Kiểm Tra Thính Giác⟦6⟧⏎Thiết Bị Trợ Thính6⏎Giảm Âm T…`
- `tn-apple-airpodspro3#010` · số `6` · `…Thính Giác6⏎Thiết Bị Trợ Thính⟦6⟧⏎Giảm Âm Thanh Lớn⏎Âm thanh Ng…`
- `tn-apple-airpodspro3#010` · số `19` · `…nh Lớn⏎Âm thanh Nghe Trực Tiếp⟦19⟧⏎Mức âm thanh tai nghe⏎Thích N…`
- `tn-apple-airpodspro3#013` · số `20` · `… giảm tác động đến môi trường:⟦20⟧⏎Xem Báo Cáo Môi Trường Về Sản…`
- `tn-apple-airpodspro3#014` · số `21` · `…c làm từ 40% vật liệu tái chế,⟦21⟧ bao gồm:⏎100% nhôm trong bản …`
- `tn-apple-airpodspro3#014` · số `22` · `…bì⏎100% bao bì được làm từ sợi⟦22⟧`
- `tn-apple-airpodspro3#015` · số `23` · `…25% thiết bị trong mỗi chuyến.⟦23⟧⏎Năng lượng⏎40% lượng điện dùn…`
- `tn-apple-airpodspro3#015` · số `24` · `…o 3 đến từ nguồn điện tái tạo.⟦24⟧⏎Đáp ứng các yêu cầu của Bộ Nă…`
- `tn-apple-airpodspro3#015` · số `25` · `…ỳ dành cho hệ thống bộ sạc pin⟦25⟧`
- `tn-apple-airpodspro3#016` · số `26` · `…rình Không Rác Thải của Apple.⟦26⟧⏎Sử dụng hóa chất thông minh h…`
- `tn-apple-airpodspro3#016` · số `27` · `…ử dụng hóa chất thông minh hơn⟦27⟧`

### tn-apple-airpods4 (16 chỗ)

- `tn-apple-airpods4#002` · số `1` · `Công Nghệ Âm Thanh⟦1⟧⏎Trình điều khiển Apple với độ…`
- `tn-apple-airpods4#002` · số `2` · `… có thể tùy chỉnh⏎Tách Lời Nói⟦2⟧⏎Chế độ Âm Thanh Không Gian Cá…`
- `tn-apple-airpods4#002` · số `3` · `…o dõi chuyển động đầu chủ động⟦3⟧`
- `tn-apple-airpods4#004` · số `4` · `…i cuộc gọi, bật hoặc tắt tiếng⟦4⟧⏎Nhấn một lần để mở điều khiển…`
- `tn-apple-airpods4#004` · số `5` · `…ột lần để mở điều khiển camera⟦5⟧⏎Nhấn hai lần để kết thúc cuộc…`
- `tn-apple-airpods4#004` · số `6` · `…ản lý thông báo và hơn thế nữa⟦6⟧⏎Chống Bụi, Chống Mồ Hôi và Ch…`
- `tn-apple-airpods4#004` · số `7` · `…ụi, Chống Mồ Hôi và Chống Nước⟦7⟧`
- `tn-apple-airpods4#005` · số `8` · `…P54)⏎Kích Thước Và Trọng Lượng⟦8⟧⏎AirPods 4 (Mỗi Bên)⏎Cao: 30,2…`
- `tn-apple-airpods4#006` · số `9` · `… lên đến 5 giờ với một lần sạc⟦9⟧⏎AirPods 4 với Hộp Sạc (USB-C)…`
- `tn-apple-airpods4#006` · số `10` · `…⏎Thời gian nghe lên đến 30 giờ⟦10⟧⏎5 phút để trong hộp sạc có th…`
- `tn-apple-airpods4#006` · số `11` · `…ng thời gian nghe khoảng 1 giờ⟦11⟧`
- `tn-apple-airpods4#007` · số `12` · `…o gồm:⏎Âm thanh Nghe Trực Tiếp⟦12⟧⏎Mức âm thanh tai nghe⏎Thích N…`
- `tn-apple-airpods4#010` · số `13` · `… giảm tác động tới môi trường:⟦13⟧⏎Vật liệu⏎100% thiếc trong mối…`
- `tn-apple-airpods4#010` · số `14` · `…hế⏎100% bao bì được làm từ sợi⟦14⟧`
- `tn-apple-airpods4#011` · số `15` · `… Hoa Kỳ về hệ thống bộ sạc pin⟦15⟧⏎Rác thải⏎Không có cơ sở lắp r…`
- `tn-apple-airpods4#011` · số `16` · `…ử dụng hóa chất thông minh hơn⟦16⟧⏎Không chứa thủy ngân, BFR và …`

### tn-xiaomi-redmibuds6pro (22 chỗ)

- `tn-xiaomi-redmibuds6pro#011` · sao `*` · `… 55dB với nhiều mức điều chỉnh⟦*⟧⏎Tích hợp âm thanh đa chiều vớ…`
- `tn-xiaomi-redmibuds6pro#011` · sao `*` · `…iều chỉnh theo chuyển động đầu⟦*⟧`
- `tn-xiaomi-redmibuds6pro#012` · sao `*` · `… tần số siêu rộng lên đến 4kHz⟦*⟧⏎Tận hưởng 2 tháng nghe nhạc m…`
- `tn-xiaomi-redmibuds6pro#012` · sao `*` · `… quảng cáo với Spotify Premium⟦*⟧⏎hủy khuyến mãi này bất cứ lúc…`
- `tn-xiaomi-redmibuds6pro#017` · sao `*` · `…cảnh.⏎+40% Độ sâu khử tiếng ồn⟦*⟧⏎+14,16% Tổng mức khử ồn chủ đ…`
- `tn-xiaomi-redmibuds6pro#017` · sao `*` · `…% Tổng mức khử ồn chủ động ANC⟦*⟧⏎Tần số khử tiếng ồn⏎Độ sâu kh…`
- `tn-xiaomi-redmibuds6pro#018` · sao `*` · `… quả chống ồn.⏎16.000 lần/giây⟦*⟧⏎Tần suất lấy mẫu cao nhất*`
- `tn-xiaomi-redmibuds6pro#018` · sao `*` · `…iây*⏎Tần suất lấy mẫu cao nhất⟦*⟧`
- `tn-xiaomi-redmibuds6pro#020` · sao `*` · `…ộc gọi⏎12 m/giây⏎Khử tiếng gió⟦*⟧⏎Thiết kế đẹp sắc sảo⏎Trung th…`
- `tn-xiaomi-redmibuds6pro#021` · sao `*` · `…n thông qua độ dài của dải đèn⟦*⟧.`
- `tn-xiaomi-redmibuds6pro#023` · sao `*` · `…ệm thông minh⏎Chia sẻ âm thanh⟦*⟧⏎Hỗ trợ kết nối đồng thời hai …`
- `tn-xiaomi-redmibuds6pro#023` · sao `*` · `…chung mới đã!⏎Google Fast Pair⟦*⟧⏎Chỉ cần mở nắp để ghép đôi⏎Nh…`
- `tn-xiaomi-redmibuds6pro#023` · sao `*` · `…6 Pro với các thiết bị Android⟦*⟧ qua Bluetooth chỉ bằng một lầ…`
- `tn-xiaomi-redmibuds6pro#023` · sao `*` · `…i nghe ở đâu.⏎Chia sẻ âm thanh⟦*⟧⏎Hỗ trợ kết nối đồng thời hai …`
- `tn-xiaomi-redmibuds6pro#024` · sao `*` · `Google Fast Pair⟦*⟧⏎Chỉ cần mở nắp để ghép đôi⏎Nh…`
- `tn-xiaomi-redmibuds6pro#024` · sao `*` · `…6 Pro với các thiết bị Android⟦*⟧ qua Bluetooth chỉ bằng một lầ…`
- `tn-xiaomi-redmibuds6pro#024` · sao `*` · `…i nghe ở đâu.⏎Chia sẻ âm thanh⟦*⟧⏎Hỗ trợ kết nối đồng thời hai …`
- `tn-xiaomi-redmibuds6pro#025` · sao `*` · `…Thời lượng pin sau một lần sạc⟦*⟧⏎2 giờ⏎Sạc nhanh trong 5 phút*…`
- `tn-xiaomi-redmibuds6pro#025` · sao `*` · `…*⏎2 giờ⏎Sạc nhanh trong 5 phút⟦*⟧⏎36 giờ⏎Sử dụng cùng với hộp s…`
- `tn-xiaomi-redmibuds6pro#025` · sao `*` · `…6 giờ⏎Sử dụng cùng với hộp sạc⟦*⟧⏎Nâng cấp trải nghiệm vuốt chạ…`
- `tn-xiaomi-redmibuds6pro#026` · sao `*` · `Xiaomi Earbuds⟦*⟧⏎Dễ dàng tùy chỉnh⏎Tải ứng dụn…`
- `tn-xiaomi-redmibuds6pro#026` · sao `*` · `…há.⏎Khả năng chống nước và bụi⟦*⟧⏎Tìm tai nghe của bạn⏎Tính năn…`

### dh-samsung-galaxywatch8 (29 chỗ)

- `dh-samsung-galaxywatch8#009` · số `1` · `… mm và 44 mm, màu Xám và Bạc. ⟦1⟧⏎Chiếc đồng hồ`
- `dh-samsung-galaxywatch8#010` · số `3` · `…n và thậm chí cả khi bạn ngủ. ⟦3⟧`
- `dh-samsung-galaxywatch8#012` · số `3, 4` · `…ải mái nhất từ trước đến nay. ⟦3, 4⟧`
- `dh-samsung-galaxywatch8#014` · số `3` · `…sắc nét, sống động và dễ đọc. ⟦3⟧⏎pause⏎view more`
- `dh-samsung-galaxywatch8#015` · số (ghi tay) `1` · `…y đeo phù hợp với ngày của bạn⟦1⟧⏎view more⏎Dây đeo Thể thao⏎vi…`
- `dh-samsung-galaxywatch8#016` · số `2,5` · `…ờ lịch trình ngủ cá nhân hóa. ⟦2,5⟧⏎Hướng dẫn sử dụng tính năng H…`
- `dh-samsung-galaxywatch8#034` · số `2,6` · `…dụng tối đa từng khoảnh khắc. ⟦2,6⟧`
- `dh-samsung-galaxywatch8#036` · số `7` · `… đầy năng lượng cho ngày mới. ⟦7⟧⏎view more`
- `dh-samsung-galaxywatch8#037` · số `8,9,10,11` · `…hoạt động sớm hơn trong ngày. ⟦8,9,10,11⟧⏎view more⏎Chọn nhịp bước, chạ…`
- `dh-samsung-galaxywatch8#038` · số `2,12` · `…mốc, giúp bạn phá vỡ rào cản. ⟦2,12⟧`
- `dh-samsung-galaxywatch8#058` · số `13` · `…để đạt được mục tiêu chạy bộ. ⟦13⟧⏎view more`
- `dh-samsung-galaxywatch8#060` · số `14,15,16,17` · `…n đều được ghi lại chính xác. ⟦14,15,16,17⟧⏎view more⏎Sức ép lên mạch máu…`
- `dh-samsung-galaxywatch8#061` · số `2,18,19` · `…tốt hơn cho bạn vào ngày mai. ⟦2,18,19⟧⏎Hướng dẫn sử dụng tính năng đ…`
- `dh-samsung-galaxywatch8#078` · số `20,21,22,23` · `…chắc tình trạng tim của mình. ⟦20,21,22,23⟧⏎view more⏎ECG`
- `dh-samsung-galaxywatch8#079` · số `24` · `…ảo sức khỏe tim mạch của bạn. ⟦24⟧⏎view more`
- `dh-samsung-galaxywatch8#080` · số `2,25,26,27,28` · `…hỏe và giảm nguy cơ mắc bệnh. ⟦2,25,26,27,28⟧⏎Samsung Health`
- `dh-samsung-galaxywatch8#082` · số `29` · `…g hơn với hướng dẫn chi tiết. ⟦29⟧⏎view more`
- `dh-samsung-galaxywatch8#084` · số `11,14,30` · `…n tới mục tiêu bạn đã đặt ra. ⟦11,14,30⟧⏎view more⏎Giúp tâm trí của bạ…`
- `dh-samsung-galaxywatch8#087` · số `31,32,33` · `…ến bộ của bạn theo thời gian. ⟦31,32,33⟧⏎view more`
- `dh-samsung-galaxywatch8#090` · số `34` · `…ngày mới một cách tự tin hơn. ⟦34⟧⏎view more`
- `dh-samsung-galaxywatch8#091` · số `35,36` · `…bạn cần ngay trên cổ tay bạn. ⟦35,36⟧⏎One UI 8 Watch hoàn toàn mới`
- `dh-samsung-galaxywatch8#092` · số `37` · `…ng một nơi với thanh Now Bar. ⟦37⟧⏎Galaxy Watch8 hiển thị các mà…`
- `dh-samsung-galaxywatch8#093` · số `38,39` · `…ọn từ màu sắc đến thành phần. ⟦38,39⟧⏎Dây đeo Thể thao⏎Dây đeo Vải⏎…`
- `dh-samsung-galaxywatch8#095` · số `40, 41, 42 43, 44, 45, 46` · `…hợp vào thiết kế đệm đẹp mắt. ⟦40, 41, 42 43, 44, 45, 46⟧⏎Ứng dụng Galaxy Wearable⏎Ứng …`
- `dh-samsung-galaxywatch8#110` · số `3,4` · `…hơn và vừa vặn thoải mái hơn. ⟦3,4⟧⏎Tại sao Galaxy Watch8 lại tốt…`
- `dh-samsung-galaxywatch8#112` · số `1` · `…, Nhỏ (40 mm) và Lớn (44 mm). ⟦1⟧⏎Galaxy Watch8 có thể theo dõi…`
- `dh-samsung-galaxywatch8#112` · số `10` · `… sức khỏe tinh thần tốt nhất. ⟦10⟧`
- `dh-samsung-galaxywatch8#116` · số `14` · `… minh chạy Android 12 trở lên.⟦14⟧⏎Galaxy Watch8 có GPS băng tần…`
- `dh-samsung-galaxywatch8#116` · số `16,17` · `… L5 GPS để tăng độ chính xác. ⟦16,17⟧⏎Sạc Galaxy Watch8 như thế nào…`

### dh-xiaomi-watchs4 (16 chỗ)

- `dh-xiaomi-watchs4#014` · sao `*` · `…h dễ dàng với Xiaomi Smart Hub⟦*⟧⏎Chỉ cần một chạm để xem thông…`
- `dh-xiaomi-watchs4#014` · sao `*` · `…hỏe và hơn 150 chế độ thể thao⟦*⟧ để lựa chọn⏎Thời lượng pin lê…`
- `dh-xiaomi-watchs4#014` · sao `*` · `…Thời lượng pin lên đến 15 ngày⟦*⟧⏎Hiệu suất cao`
- `dh-xiaomi-watchs4#015` · sao `*` · `…nit ở chế độ HBM.⏎326⏎PPI⏎60Hz⟦*⟧⏎Tốc độ làm mới⏎1.500 nit*⏎Độ …`
- `dh-xiaomi-watchs4#015` · sao `*` · `…60Hz*⏎Tốc độ làm mới⏎1.500 nit⟦*⟧⏎Độ sáng HBM*⏎2.200 nit*⏎Độ sá…`
- `dh-xiaomi-watchs4#015` · sao `*` · `…làm mới⏎1.500 nit*⏎Độ sáng HBM⟦*⟧⏎2.200 nit*⏎Độ sáng cực đại*⏎Đ…`
- `dh-xiaomi-watchs4#015` · sao `*` · `…00 nit*⏎Độ sáng HBM*⏎2.200 nit⟦*⟧⏎Độ sáng cực đại*⏎Điều khiển c…`
- `dh-xiaomi-watchs4#015` · sao `*` · `…BM*⏎2.200 nit*⏎Độ sáng cực đại⟦*⟧⏎Điều khiển cảm ứng chống ẩm⏎T…`
- `dh-xiaomi-watchs4#015` · sao `*` · `…15 ngày⏎Thời lượng pin 15 ngày⟦*⟧ đảm bảo thời gian sử dụng trê…`
- `dh-xiaomi-watchs4#025` · sao `*` · `… nhịp tim trên đồng hồ đến 98%⟦*⟧.⏎Theo dõi độ bão hòa oxy tron…`
- `dh-xiaomi-watchs4#025` · sao `*` · `… bão hòa oxy trong máu cả ngày⟦*⟧⏎Theo dõi mức độ căng thẳng cả…`
- `dh-xiaomi-watchs4#025` · sao `*` · `… dõi mức độ căng thẳng cả ngày⟦*⟧⏎Theo dõi giấc ngủ nâng cao cả…`
- `dh-xiaomi-watchs4#025` · sao `*` · `… dõi giấc ngủ nâng cao cả ngày⟦*⟧⏎Hơn 150 chế độ thể thao⏎Lý tư…`
- `dh-xiaomi-watchs4#030` · sao `*` · `…o số liên lạc khẩn cấp của bạn⟦*⟧.`
- `dh-xiaomi-watchs4#032` · sao `*` · `Xiaomi Smart Hub⟦*⟧⏎Kết nối không gián đoạn⏎Chụp …`
- `dh-xiaomi-watchs4#032` · sao `*` · `…khiển các thiết bị Xiaomi Home⟦*⟧, giúp bạn dễ dàng kết nối và …`

## 4. Nghi xóa nhầm (19 chỗ)

Chỗ xóa có ít nhất một dấu hiệu: ký tự liền trước là chữ HOA hoặc chữ số (kiểu `IP68`, `Buds3`, `A2305`); liền sau (cách nhiều nhất một dấu cách) là chữ đơn vị (giờ, phút, mAh, W, Hz, nit, %, m, mm, x...); số đã xóa không có chú thích tương ứng trong bảng chú thích của trang; hoặc dấu `*` ngay sau một con số đứng riêng. Người kiểm xem từng chỗ có đúng là ký hiệu không (ví dụ `MIMO8`, `25W6` là ký hiệu thật).

- `dt-apple-iphone17#017` · `8` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…z)⏎5G (sub-6 GHz) với 4x4 MIMO⟦8⟧⏎LTE Gigabit với 4x4 MIMO8⏎Chi…`
- `dt-apple-iphone17#017` · `8` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…MIMO8⏎LTE Gigabit với 4x4 MIMO⟦8⟧⏎Chip mạng không dây Apple N1`
- `dt-apple-iphone17#018` · `9` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…i-Fi 7 (802.11be) với 2x2 MIMO⟦9⟧⏎Bluetooth 6⏎Công nghệ mạng Th…`
- `dt-apple-iphone17#018` · `10` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…le Ultra Wideband thế hệ thứ 2⟦10⟧⏎NFC có chế độ đọc⏎Thẻ Truy Cậ…`
- `dt-apple-iphone17#021` · `6` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `… không dây MagSafe lên đến 25W⟦6⟧⏎Sạc không dây Qi2 lên đến 25W…`
- `dt-apple-iphone17#021` · `6` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…⏎Sạc không dây Qi2 lên đến 25W⟦6⟧⏎Dãy nam châm⏎Nam châm căn chỉ…`
- `dt-xiaomi-15t#041` · `10` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…thống.9⏎Nhận dạng giọng nói AI⟦10⟧⏎Phiên dịch AI10⏎Tìm kiếm AI10…`
- `dt-xiaomi-15t#047` · `15` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…ục14⏎Sạc nhanh HyperCharge 67W⟦15⟧⏎50 phút sạc đầy 100%14⏎Hệ thố…`
- `dt-xiaomi-15t#048` · `16` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…ịnh.⏎+13%⏎Diện tích bề mặt LHP⟦16⟧⏎+11%⏎Tấm than chì trên khung …`
- `dt-xiaomi-15t#048` · `17, 18` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…kép chuẩn Dolby Atmos®⏎Wi-Fi 6⟦17, 18⟧⏎Bluetooth 6.0⏎NFC đa chức năn…`
- `dh-apple-watchse3#016` · `16` · liền trước là chữ hoa hoặc chữ số (có thể là mã như IP68, Buds3, A2305) · `…và A3328⏎Hỗ trợ RedCap cho LTE⟦16⟧⏎FDD-LTE (Băng tần 1, 2, 3, 4,…`
- `dt-samsung-galaxys25ultra#128` · `21,24` · trang không có chú thích mang số này · `…n điều chỉnh cài đặt màn hình.⟦21,24⟧⏎Tuổi thọ pin vượt trội⏎Công n…`
- `dh-samsung-galaxywatch8#038` · `2,12` · trang không có chú thích mang số này · `…mốc, giúp bạn phá vỡ rào cản. ⟦2,12⟧`
- `dh-samsung-galaxywatch8#058` · `13` · trang không có chú thích mang số này · `…để đạt được mục tiêu chạy bộ. ⟦13⟧⏎view more`
- `dh-samsung-galaxywatch8#060` · `14,15,16,17` · trang không có chú thích mang số này · `…n đều được ghi lại chính xác. ⟦14,15,16,17⟧⏎view more⏎Sức ép lên mạch máu…`
- `dh-samsung-galaxywatch8#084` · `11,14,30` · trang không có chú thích mang số này · `…n tới mục tiêu bạn đã đặt ra. ⟦11,14,30⟧⏎view more⏎Giúp tâm trí của bạ…`
- `dh-samsung-galaxywatch8#090` · `34` · trang không có chú thích mang số này · `…ngày mới một cách tự tin hơn. ⟦34⟧⏎view more`
- `dh-samsung-galaxywatch8#091` · `35,36` · trang không có chú thích mang số này · `…bạn cần ngay trên cổ tay bạn. ⟦35,36⟧⏎One UI 8 Watch hoàn toàn mới`
- `dh-samsung-galaxywatch8#116` · `14` · trang không có chú thích mang số này · `… minh chạy Android 12 trở lên.⟦14⟧⏎Galaxy Watch8 có GPS băng tần…`

## 5. Có thể còn sót (299 chỗ theo regex, thêm mã chữ hoa ở 5.2)

### 5.1 Chữ thường, `)` hoặc `%` liền ngay sau là 1-2 chữ số

Trong `noi_dung` mới: chữ thường, dấu đóng ngoặc hoặc dấu % liền ngay sau là 1-2 chữ số rồi tới khoảng trắng, xuống dòng hoặc hết chuỗi (regex `[a-zà-ỹđ%)]\d{1,2}(?=\s|$)`), thêm danh sách số dính chữ không cách (`bơi14,15`). Nhiều chỗ là tên máy hoặc số liệu (`Buds3`, `Watch8`, `4x4`) hoặc tên người dùng trong đánh giá. **Không tự xóa**: người kiểm xem có phải ký hiệu bị sót không. Các ký hiệu thật từng bị sót (`30 phút6`, `AI10`, `xong1`, `nhất2,3`, `Samsung34`...) đã bỏ bằng bảng ghi tay ở mục 7; mục 5.3 đối chiếu lại với thẻ `<sup>` của `page.html` để chắc không còn ký hiệu thật nào trong `noi_dung`.

#### dt-apple-iphone17 (4 chỗ)

Hay gặp: `x4` ×2, `x2` ×1, `i2` ×1

- `dt-apple-iphone17#017` · `x4` · `…900 MHz)⏎5G (sub-6 GHz) với 4x⟦4⟧ MIMO⏎LTE Gigabit với 4x4 MIMO…`
- `dt-apple-iphone17#017` · `x4` · `…ới 4x4 MIMO⏎LTE Gigabit với 4x⟦4⟧ MIMO⏎Chip mạng không dây Appl…`
- `dt-apple-iphone17#018` · `x2` · `…e ID⏎Wi-Fi 7 (802.11be) với 2x⟦2⟧ MIMO⏎Bluetooth 6⏎Công nghệ mạ…`
- `dt-apple-iphone17#021` · `i2` · `…e lên đến 25W⏎Sạc không dây Qi⟦2⟧ lên đến 25W⏎Dãy nam châm⏎Nam …`

#### tn-samsung-buds3pro (54 chỗ)

Hay gặp: `s3` ×46, `s4` ×4, `d6` ×2, `t72` ×1, `h16` ×1

- `tn-samsung-buds3pro#002` · `s3` · `…⏎Đăng nhập/Đăng ký⏎Galaxy Buds⟦3⟧ Pro⏎Bạc⏎Xếp hạng sản phẩm :⏎4…`
- `tn-samsung-buds3pro#002` · `s3` · `…ật⏎Đánh giá⏎Hỗ trợ⏎Galaxy Buds⟦3⟧ Pro⏎+6 xem thêm⏎Bạn đang tìm …`
- `tn-samsung-buds3pro#003` · `s4` · `Galaxy Buds⟦4⟧⏎Product Ratings :⏎4.6⏎Number …`
- `tn-samsung-buds3pro#003` · `s4` · `…s:⏎3⏎1.190.000 VND⏎Galaxy Buds⟦4⟧ Pro (chỉ có tại Samsung.com)⏎…`
- `tn-samsung-buds3pro#003` · `s4` · `…4615⏎6.790.000 VND⏎Galaxy Buds⟦4⟧ Pro⏎Product Ratings :⏎4.8⏎Num…`
- `tn-samsung-buds3pro#003` · `s3` · `… VND⏎Chọn thiết bị⏎Galaxy Buds⟦3⟧⏎Galaxy Buds3 Pro`
- `tn-samsung-buds3pro#003` · `s3` · `…ết bị⏎Galaxy Buds3⏎Galaxy Buds⟦3⟧ Pro`
- `tn-samsung-buds3pro#004` · `s3` · `…ắc : Bạc⏎Bạc⏎Trắng⏎Galaxy Buds⟦3⟧ Pro⏎Galaxy Buds3 Pro Bạc⏎Điểm…`
- `tn-samsung-buds3pro#004` · `s3` · `…g⏎Galaxy Buds3 Pro⏎Galaxy Buds⟦3⟧ Pro Bạc⏎Điểm Samsung Reward ư…`
- `tn-samsung-buds3pro#004` · `s3` · `…hỏng. Màu tai nghe Galaxy Buds⟦3⟧ Pro có sẵn có thể thay đổi th…`
- `tn-samsung-buds3pro#004` · `s3` · `…gia hoặc nhà mạng. Galaxy Buds⟦3⟧ Pro hỗ trợ các tính năng của …`
- `tn-samsung-buds3pro#005` · `s3` · `… sàng cho tai nghe Galaxy Buds⟦3⟧ Pro mới tinh của bạn`
- `tn-samsung-buds3pro#007` · `s3` · `…ights⏎Cặp tai nghe Galaxy Buds⟦3⟧ Pro trong hộp sạc đang mở.⏎Ch…`
- `tn-samsung-buds3pro#007` · `s3` · `… Light và hiển thị Galaxy Buds⟦3⟧ Pro.`
- `tn-samsung-buds3pro#008` · `s3` · `…Một chiếc tai nghe Galaxy Buds⟦3⟧ Pro màu bạc. Các hạt lớn tượn…`
- `tn-samsung-buds3pro#009` · `s3` · `…& Personal Audio – Galaxy Buds⟦3⟧ Pro"`
- `tn-samsung-buds3pro#011` · `s3` · `… kế hoàn toàn mới. Galaxy Buds⟦3⟧ Pro được thiết kế có đầu nhỏ,…`
- `tn-samsung-buds3pro#012` · `s3` · `…i⏎A pair of silver Galaxy Buds⟦3⟧ Pro appear in a closed case w…`
- `tn-samsung-buds3pro#013` · `s3` · `… tâm rằng tai nghe Galaxy Buds⟦3⟧ Pro của bạn luôn chắc chắn kh…`
- `tn-samsung-buds3pro#014` · `s3` · `…một chiếc tai nghe Galaxy Buds⟦3⟧ Pro.⏎Nội dung điều khiển chạm…`
- `tn-samsung-buds3pro#014` · `s3` · `…một chiếc tai nghe Galaxy Buds⟦3⟧ Pro.`
- `tn-samsung-buds3pro#015` · `s3` · `… Light và hiển thị Galaxy Buds⟦3⟧ Pro.`
- `tn-samsung-buds3pro#017` · `s3` · `…iên của chúng tôi, Galaxy Buds⟦3⟧ Pro giảm nhiễu giữa các loa –…`
- `tn-samsung-buds3pro#018` · `s3` · `…uẩn phòng thu trên Galaxy Buds⟦3⟧ Pro của bạn. Công nghệ Samsun…`
- `tn-samsung-buds3pro#018` · `s3` · `…u đó, giải mã trên Galaxy Buds⟦3⟧ Pro, giúp duy trì chất lượng …`
- `tn-samsung-buds3pro#020` · `s3` · `…Tận hưởng tai nghe Galaxy Buds⟦3⟧ Pro nhưng vẫn dễ dàng tương t…`
- `tn-samsung-buds3pro#020` · `s3` · `…nh. Nhờ Galaxy AI, Galaxy Buds⟦3⟧ Pro tự động nhận diện và ngăn…`
- `tn-samsung-buds3pro#020` · `s3` · `…Một chiếc tai nghe Galaxy Buds⟦3⟧ Pro màu bạc có dòng chữ "`
- `tn-samsung-buds3pro#023` · `s3` · `…hông cần phải tháo Galaxy Buds⟦3⟧ Pro ra.`
- `tn-samsung-buds3pro#024` · `s3` · `…ng hoặc tiếng còi, Galaxy Buds⟦3⟧ Pro sẽ tự động chuyển sang ch…`
- `tn-samsung-buds3pro#025` · `s3` · `…ian thực thông qua Galaxy Buds⟦3⟧ Pro. Khám phá ý nghĩa của việ…`
- `tn-samsung-buds3pro#026` · `s3` · `…và giữ tai nghe và Galaxy Buds⟦3⟧ Pro sẽ tiếp tục phiên dịch kh…`
- `tn-samsung-buds3pro#026` · `s3` · `…ía loa, nhấn nhanh Galaxy Buds⟦3⟧ Pro và nghe cuộc trò chuyện đ…`
- `tn-samsung-buds3pro#027` · `s3` · `…y, chất lượng cao? Galaxy Buds⟦3⟧ Pro mang đến chất lượng cuộc …`
- `tn-samsung-buds3pro#029` · `s3` · `…C Auto Switch trên Galaxy Buds⟦3⟧ Pro phát hiện hoạt động âm th…`
- `tn-samsung-buds3pro#030` · `s3` · `…axy Book, tai nghe Galaxy Buds⟦3⟧ Pro và điện thoại Galaxy Z Fo…`
- `tn-samsung-buds3pro#030` · `d6` · `…ọi từ điện thoại Galaxy Z Fold⟦6⟧ xuất hiện trên máy tính xách …`
- `tn-samsung-buds3pro#030` · `s3` · `…thanh của tai nghe Galaxy Buds⟦3⟧ Pro từ máy tính xách tay sang…`
- `tn-samsung-buds3pro#034` · `s3` · `… "volume up" và để Galaxy Buds⟦3⟧ pro thực hiện phần còn lại.⏎T…`
- `tn-samsung-buds3pro#036` · `d6` · `…ast⏎Màn hình lớn Galaxy Z Fold⟦6⟧ mở ra với tai nghe Galaxy Bud…`
- `tn-samsung-buds3pro#036` · `s3` · `…mở ra với tai nghe Galaxy Buds⟦3⟧ Pro ở bên phải và Samsung Hea…`
- `tn-samsung-buds3pro#036` · `s3` · `…Bằng cách nhấn vào Galaxy Buds⟦3⟧ Pro, ứng dụng sẽ kích hoạt và…`
- `tn-samsung-buds3pro#039` · `s3` · `…ắng Chanh Sả⏎BUY NOW⏎Spec⏎Buds⟦3⟧ Pro⏎Buds3⏎Buds FE`
- `tn-samsung-buds3pro#039` · `s3` · `…Sả⏎BUY NOW⏎Spec⏎Buds3 Pro⏎Buds⟦3⟧⏎Buds FE`
- `tn-samsung-buds3pro#042` · `s3` · `…GALAXY WATCH ULTRA⏎Galaxy Buds⟦3⟧⏎CHUYỂN ĐẾN GALAXY BUDS3⏎Galax…`
- `tn-samsung-buds3pro#045` · `s3` · `Chuẩn IP⏎Đánh giá⏎Galaxy Buds⟦3⟧ Pro⏎Product rating :⏎4.4⏎(15,…`
- `tn-samsung-buds3pro#046` · `t72` · `…đánh giá⏎Vị trí địa lý⏎Goodcat⟦72⟧⏎2024-07-26⏎Mobile Alabama⏎Màu…`
- `tn-samsung-buds3pro#052` · `h16` · `…ần đầu trên Samsung US⏎Drsmith⟦16⟧⏎2025-03-12⏎if am not in Miami…`
- `tn-samsung-buds3pro#062` · `s3` · `…dẫn đeo và sử dụng Galaxy Buds⟦3⟧ và Buds3 Pro⏎Cách thay đổi đệ…`
- `tn-samsung-buds3pro#062` · `s3` · `…à sử dụng Galaxy Buds3 và Buds⟦3⟧ Pro⏎Cách thay đổi đệm tai ngh…`
- `tn-samsung-buds3pro#062` · `s3` · `…m tai nghe Samsung Galaxy Buds⟦3⟧ Pro và Buds4 Pro⏎Tại sao Gala…`
- `tn-samsung-buds3pro#062` · `s4` · `…msung Galaxy Buds3 Pro và Buds⟦4⟧ Pro⏎Tại sao Galaxy Buds3/Buds…`
- `tn-samsung-buds3pro#062` · `s3` · `… Pro⏎Tại sao Galaxy Buds3/Buds⟦3⟧ Pro của bạn lại phát ra tiếng…`
- `tn-samsung-buds3pro#063` · `s3` · `… Sound⏎Galaxy Buds⏎Galaxy Buds⟦3⟧ Pro⏎Footer Navigation`

#### dt-oppo-findx8 (19 chỗ)

Hay gặp: `o16` ×6, `o15` ×4, `r5` ×4, `p2` ×2, `s3` ×2, `n78` ×1

- `dt-oppo-findx8#009` · `n78` · `…/n20/n28/n38/n40/n41/n66/n77/n⟦78⟧⏎triển khai dịch vụ.⏎Kết Nối`
- `dt-oppo-findx8#014` · `o16` · `… X9 Pro⏎OPPO Find X9⏎OPPO Reno⟦16⟧ Pro 5G⏎OPPO Reno16 5G⏎OPPO Re…`
- `dt-oppo-findx8#014` · `o16` · `…9⏎OPPO Reno16 Pro 5G⏎OPPO Reno⟦16⟧ 5G⏎OPPO Reno16 F 5G⏎OPPO Reno…`
- `dt-oppo-findx8#014` · `o16` · `…ro 5G⏎OPPO Reno16 5G⏎OPPO Reno⟦16⟧ F 5G⏎OPPO Reno15 5G⏎OPPO Reno…`
- `dt-oppo-findx8#014` · `o15` · `… 5G⏎OPPO Reno16 F 5G⏎OPPO Reno⟦15⟧ 5G⏎OPPO Reno15 F 5G⏎OPPO A7 P…`
- `dt-oppo-findx8#014` · `o15` · `… F 5G⏎OPPO Reno15 5G⏎OPPO Reno⟦15⟧ F 5G⏎OPPO A7 Pro 5G⏎OPPO A6 P…`
- `dt-oppo-findx8#015` · `p2` · `…O Watch X2 Mini⏎OPPO Enco Clip⟦2⟧ Open Earbuds⏎OPPO Enco Buds3s…`
- `dt-oppo-findx8#015` · `r5` · `…3s⏎OPPO Enco X3i⏎OPPO Enco Air⟦5⟧ Pro⏎OPPO Enco Air5⏎OPPO Enco …`
- `dt-oppo-findx8#015` · `r5` · `…PO Enco Air5 Pro⏎OPPO Enco Air⟦5⟧⏎OPPO Enco Air5s`
- `dt-oppo-findx8#016` · `s3` · `OPPO Enco Buds⟦3⟧⏎Mua ở đâu⏎Thế Giới Di Động⏎Đi…`
- `dt-oppo-findx8#065` · `o16` · `… X9 Pro⏎OPPO Find X9⏎OPPO Reno⟦16⟧ Pro 5G⏎OPPO Reno16 5G⏎OPPO Re…`
- `dt-oppo-findx8#065` · `o16` · `…9⏎OPPO Reno16 Pro 5G⏎OPPO Reno⟦16⟧ 5G⏎OPPO Reno16 F 5G⏎OPPO Reno…`
- `dt-oppo-findx8#065` · `o16` · `…ro 5G⏎OPPO Reno16 5G⏎OPPO Reno⟦16⟧ F 5G⏎OPPO Reno15 5G⏎OPPO Reno…`
- `dt-oppo-findx8#065` · `o15` · `… 5G⏎OPPO Reno16 F 5G⏎OPPO Reno⟦15⟧ 5G⏎OPPO Reno15 F 5G⏎OPPO A7 P…`
- `dt-oppo-findx8#065` · `o15` · `… F 5G⏎OPPO Reno15 5G⏎OPPO Reno⟦15⟧ F 5G⏎OPPO A7 Pro 5G⏎OPPO A6 P…`
- `dt-oppo-findx8#066` · `p2` · `…O Watch X2 Mini⏎OPPO Enco Clip⟦2⟧ Open Earbuds⏎OPPO Enco Buds3s…`
- `dt-oppo-findx8#066` · `r5` · `…3s⏎OPPO Enco X3i⏎OPPO Enco Air⟦5⟧ Pro⏎OPPO Enco Air5⏎OPPO Enco …`
- `dt-oppo-findx8#066` · `r5` · `…PO Enco Air5 Pro⏎OPPO Enco Air⟦5⟧⏎OPPO Enco Air5s`
- `dt-oppo-findx8#067` · `s3` · `OPPO Enco Buds⟦3⟧⏎Mua ở đâu⏎Thế Giới Di Động⏎Đi…`

#### dt-samsung-galaxys25ultra (10 chỗ)

Hay gặp: `b6` ×4, `s3` ×2, `s2` ×1, `e20` ×1, `d3` ×1, `h7` ×1

- `dt-samsung-galaxys25ultra#009` · `b6` · `…4G LTE FDD, 4G LTE TDD, 5G Sub⟦6⟧ FDD, 5G Sub6 TDD⏎2G GSM⏎GSM85…`
- `dt-samsung-galaxys25ultra#009` · `b6` · `…G LTE TDD, 5G Sub6 FDD, 5G Sub⟦6⟧ TDD⏎2G GSM⏎GSM850, GSM900, DC…`
- `dt-samsung-galaxys25ultra#011` · `b6` · `…40(2300), B41(2500)⏎5G FDD Sub⟦6⟧⏎N1(2100), N2(1900), N3(1800),…`
- `dt-samsung-galaxys25ultra#011` · `b6` · `…28(700), N66(AWS-3)⏎5G TDD Sub⟦6⟧⏎N38(2600), N40(2300), N41(250…`
- `dt-samsung-galaxys25ultra#015` · `s3` · `… Gear⏎Galaxy Ring, Galaxy Buds⟦3⟧ Pro, Galaxy Buds2 Pro, Galaxy…`
- `dt-samsung-galaxys25ultra#015` · `s2` · `… Galaxy Buds3 Pro, Galaxy Buds⟦2⟧ Pro, Galaxy Buds Pro, Galaxy …`
- `dt-samsung-galaxys25ultra#122` · `e20` · `…es, S21 Ultra, S20 Ultra, Note⟦20⟧ Ultra, Z Fold6, Z Flip6, Z Fo…`
- `dt-samsung-galaxys25ultra#122` · `d3` · `…lip6, Z Fold5, Z Fold4, Z Fold⟦3⟧ và Z Fold2.`
- `dt-samsung-galaxys25ultra#137` · `h7` · `Galaxy Watch⟦7⟧⏎Tìm hiểu thêm⏎Galaxy Buds3 Pr…`
- `dt-samsung-galaxys25ultra#137` · `s3` · `…tch7⏎Tìm hiểu thêm⏎Galaxy Buds⟦3⟧ Pro⏎Tìm hiểu thêm⏎Cách tiếp c…`

#### dt-xiaomi-redminote14proplus5g (1 chỗ)

Hay gặp: `x2` ×1

- `dt-xiaomi-redminote14proplus5g#008` · `x2` · `… 2.4GHz | Wi-Fi 5GHz⏎Hỗ trợ 2x⟦2⟧ MIMO, Wi-Fi Direct⏎Chống nước…`

#### tn-xiaomi-redmibuds6pro (8 chỗ)

Hay gặp: `x1` ×5, `x2` ×3

- `tn-xiaomi-redmibuds6pro#004` · `x1` · `…ản phẩm gồm⏎Redmi Buds 6 Pro x⟦1⟧⏎Hộp sạc x1⏎Cáp sạc Type-C x1⏎…`
- `tn-xiaomi-redmibuds6pro#004` · `x1` · `…⏎Redmi Buds 6 Pro x1⏎Hộp sạc x⟦1⟧⏎Cáp sạc Type-C x1⏎Hướng dẫn s…`
- `tn-xiaomi-redmibuds6pro#004` · `x1` · `…x1⏎Hộp sạc x1⏎Cáp sạc Type-C x⟦1⟧⏎Hướng dẫn sử dụng x1⏎Nút tai …`
- `tn-xiaomi-redmibuds6pro#004` · `x1` · `… Type-C x1⏎Hướng dẫn sử dụng x⟦1⟧⏎Nút tai cỡ S x2⏎Nút tai cỡ L …`
- `tn-xiaomi-redmibuds6pro#004` · `x2` · `… dẫn sử dụng x1⏎Nút tai cỡ S x⟦2⟧⏎Nút tai cỡ L x2⏎Xuất xứ: Trun…`
- `tn-xiaomi-redmibuds6pro#004` · `x2` · `…Nút tai cỡ S x2⏎Nút tai cỡ L x⟦2⟧⏎Xuất xứ: Trung Quốc`
- `tn-xiaomi-redmibuds6pro#013` · `x2` · `…7 mm⏎Củ loa bằng gốm áp điện x⟦2⟧⏎11 mm⏎Củ loa động với màng ng…`
- `tn-xiaomi-redmibuds6pro#013` · `x1` · `…ộng với màng ngăn bằng titan x⟦1⟧`

#### dh-samsung-galaxywatch8 (203 chỗ)

Hay gặp: `h8` ×173, `h7` ×13, `h6` ×13, `p7` ×1, `s3` ×1, `s25` ×1, `k26` ×1

- `dh-samsung-galaxywatch8#002` · `h8` · `…Đăng nhập/Đăng ký⏎Galaxy Watch⟦8⟧ (Bluetooth, 44 mm)⏎Xếp hạng s…`
- `dh-samsung-galaxywatch8#003` · `h8` · `…t⏎Đánh giá⏎Hỗ trợ⏎Galaxy Watch⟦8⟧⏎Thoải mái tối ưu,⏎từ giấc ngủ…`
- `dh-samsung-galaxywatch8#004` · `h8` · `…từ trước đến nay, Galaxy Watch⟦8⟧ đã sẵn sàng để tạo ra tác độn…`
- `dh-samsung-galaxywatch8#004` · `h8` · `…đẳng cấp mới⏎trên Galaxy Watch⟦8⟧`
- `dh-samsung-galaxywatch8#005` · `h8` · `… tôi.⏎Một góc của Galaxy Watch⟦8⟧ được phóng to, làm nổi bật th…`
- `dh-samsung-galaxywatch8#007` · `h8` · `…uyện viên cá nhân⏎Galaxy Watch⟦8⟧ hiển thị dòng chữ Kiểm tra cấ…`
- `dh-samsung-galaxywatch8#008` · `h8` · `…g khi Gemini trên Galaxy Watch⟦8⟧ có thể xử lý mượt mà những câ…`
- `dh-samsung-galaxywatch8#009` · `h8` · `… đổi – giới thiệu Galaxy Watch⟦8⟧ với diện mạo mới táo bạo, đượ…`
- `dh-samsung-galaxywatch8#010` · `h8` · `… hơn bao giờ hết, Galaxy Watch⟦8⟧ là chiếc Galaxy Watch mỏng nh…`
- `dh-samsung-galaxywatch8#010` · `h8` · `…g thanh thoát của Galaxy Watch⟦8⟧ mang đến cảm giác liền mạch h…`
- `dh-samsung-galaxywatch8#011` · `h8` · `…a thành một vòng. Galaxy Watch⟦8⟧ sau đó xoay nhẹ, để lộ mặt đồ…`
- `dh-samsung-galaxywatch8#012` · `h8` · `…namic Lug System, Galaxy Watch⟦8⟧ nằm thoải mái hơn trên cổ tay…`
- `dh-samsung-galaxywatch8#013` · `h8` · `…, thanh thoát của Galaxy Watch⟦8⟧ là bộ vi xử lý 3 nm mạnh mẽ. …`
- `dh-samsung-galaxywatch8#014` · `h8` · `…ó độ sáng cao của Galaxy Watch⟦8⟧ đảm bảo những thông tin quan …`
- `dh-samsung-galaxywatch8#015` · `h8` · `…ho mọi phong cách⏎Galaxy Watch⟦8⟧ màu Bạc nhìn từ phía trước, h…`
- `dh-samsung-galaxywatch8#015` · `h8` · `… và nút Back.⏎Bạc⏎Galaxy Watch⟦8⟧ Xám Graphite nhìn từ phía trư…`
- `dh-samsung-galaxywatch8#016` · `h8` · `…Bedtime guidance. Galaxy Watch⟦8⟧ sử dụng dữ liệu giấc ngủ tron…`
- `dh-samsung-galaxywatch8#017` · `h8` · `…ồ với điện thoại. Galaxy Watch⟦8⟧ và điện thoại thông minh xuất…`
- `dh-samsung-galaxywatch8#017` · `h8` · `…ết nối'. Màn hình Galaxy Watch⟦8⟧ hiển thị câu "`
- `dh-samsung-galaxywatch8#018` · `h8` · `…ửa sổ bật lên với Galaxy Watch⟦8⟧ xoay 360 độ. Văn bản: Galaxy …`
- `dh-samsung-galaxywatch8#018` · `h8` · `… 360 độ. Văn bản: Galaxy Watch⟦8⟧ đã phát hiện thiết bị mới. Dư…`
- `dh-samsung-galaxywatch8#018` · `h8` · `…hác. Chuyển cảnh. Galaxy Watch⟦8⟧ Classic phía bên phải. Ở bên …`
- `dh-samsung-galaxywatch8#018` · `h8` · `…uất hiện. Yêu cầu Galaxy Watch⟦8⟧ Series trở lên, ghép nối với …`
- `dh-samsung-galaxywatch8#020` · `h8` · `… bạn. Bên phải là Galaxy Watch⟦8⟧ hiển thị tính năng Hướng dẫn …`
- `dh-samsung-galaxywatch8#024` · `h8` · `… chuẩn bị đi ngủ. Galaxy Watch⟦8⟧ và điện thoại đặt cạnh nhau ở…`
- `dh-samsung-galaxywatch8#028` · `h8` · `… cụt! Bên phải là Galaxy Watch⟦8⟧ hiển thị thông báo tính năng …`
- `dh-samsung-galaxywatch8#028` · `h8` · `…t. Thông báo trên Galaxy Watch⟦8⟧ được nhấn.`
- `dh-samsung-galaxywatch8#029` · `h8` · `… xuống dưới cùng. Galaxy Watch⟦8⟧ hiển thị hình chim cánh cụt, …`
- `dh-samsung-galaxywatch8#029` · `h8` · `…uen ngủ. Nút trên Galaxy Watch⟦8⟧ được nhấn. Tính năng huấn luy…`
- `dh-samsung-galaxywatch8#029` · `h8` · `… xuống dưới cùng. Galaxy Watch⟦8⟧ hiển thị nút Hiển thị trên đi…`
- `dh-samsung-galaxywatch8#029` · `h8` · `… thoại’. Nút trên Galaxy Watch⟦8⟧ được nhấn.`
- `dh-samsung-galaxywatch8#032` · `h8` · `…tch. Chuyển cảnh. Galaxy Watch⟦8⟧ Classic nằm nghiêng một bên v…`
- `dh-samsung-galaxywatch8#032` · `h8` · `… và hơi xoay nhẹ. Galaxy Watch⟦8⟧ xuất hiện với góc nhìn trước …`
- `dh-samsung-galaxywatch8#032` · `h8` · `…g nhẹ và đặt cạnh Galaxy Watch⟦8⟧ Classic. Chữ: Galaxy Watch8 W…`
- `dh-samsung-galaxywatch8#032` · `h8` · `…ch8 Classic. Chữ: Galaxy Watch⟦8⟧ Watch8 Classic.`
- `dh-samsung-galaxywatch8#032` · `h8` · `…ssic. Chữ: Galaxy Watch8 Watch⟦8⟧ Classic.`
- `dh-samsung-galaxywatch8#033` · `h8` · `…ùng logo Samsung.⏎Galaxy Watch⟦8⟧ được nhìn từ góc nghiêng phía…`
- `dh-samsung-galaxywatch8#033` · `h8` · `… giờ, mặt đồng hồ Galaxy Watch⟦8⟧ sẽ hiển thị biểu tượng Samsun…`
- `dh-samsung-galaxywatch8#034` · `h8` · `…i thông minh hơn. Galaxy Watch⟦8⟧ phân tích quá trình tập luyện…`
- `dh-samsung-galaxywatch8#035` · `h8` · `…n⏎Mặt đồng hồ của Galaxy Watch⟦8⟧ hiển thị màn hình Energy Scor…`
- `dh-samsung-galaxywatch8#035` · `h8` · `…à từ 'Excellent'. Galaxy Watch⟦8⟧ biến mất và điện thoại thông …`
- `dh-samsung-galaxywatch8#036` · `h8` · `…u hơn⏎Chỉ cần đeo Galaxy Watch⟦8⟧ khi đi ngủ và thức dậy để biế…`
- `dh-samsung-galaxywatch8#040` · `h8` · `…ện thoại của bạn. Galaxy Watch⟦8⟧ và điện thoại thông minh xuất…`
- `dh-samsung-galaxywatch8#040` · `h8` · `…ết nối'. Màn hình Galaxy Watch⟦8⟧ hiển thị dòng chữ “Chào mừng”…`
- `dh-samsung-galaxywatch8#040` · `h8` · `…a sổ với hình ảnh Galaxy Watch⟦8⟧ đang xoay 360 độ.`
- `dh-samsung-galaxywatch8#041` · `h8` · `… Chạy bộ⏎Văn bản: Galaxy Watch⟦8⟧ đã phát hiện thiết bị mới. Ph…`
- `dh-samsung-galaxywatch8#041` · `h8` · `…c tế có thể khác. Galaxy Watch⟦8⟧ Series hoặc các dòng sau cần …`
- `dh-samsung-galaxywatch8#042` · `h8` · `…ủa bạn,. Màn hình Galaxy Watch⟦8⟧ được vuốt sang phải. Tính năn…`
- `dh-samsung-galaxywatch8#042` · `h8` · `…ủa bạn’. Màn hình Galaxy Watch⟦8⟧ được chạm vào. Giao diện Tìm …`
- `dh-samsung-galaxywatch8#043` · `h8` · `…ảo sát’. Màn hình Galaxy Watch⟦8⟧ được cuộn xuống và hai nút xu…`
- `dh-samsung-galaxywatch8#044` · `h8` · `…c tế có thể khác. Galaxy Watch⟦8⟧ Series hoặc các dòng sau cần …`
- `dh-samsung-galaxywatch8#044` · `h8` · `…nh. Ở bên phải là Galaxy Watch⟦8⟧ với bài kiểm tra cấp độ chạy …`
- `dh-samsung-galaxywatch8#044` · `h8` · `…ớng dẫn. Màn hình Galaxy Watch⟦8⟧ được cuộn xuống. Hai nút xuất…`
- `dh-samsung-galaxywatch8#045` · `h8` · `… Nút Bắt đầu trên Galaxy Watch⟦8⟧ được chạm. Màn hình thay đổi …`
- `dh-samsung-galaxywatch8#045` · `h8` · `…iểm tra. Màn hình Galaxy Watch⟦8⟧ hiển thị 12 phút, 100% mục ti…`
- `dh-samsung-galaxywatch8#046` · `h8` · `…ng thông tin trên Galaxy Watch⟦8⟧ được chạm. Giao diện Giới thi…`
- `dh-samsung-galaxywatch8#046` · `h8` · `…ổi chạy. Màn hình Galaxy Watch⟦8⟧ được cuộn xuống. Ở bên trái, …`
- `dh-samsung-galaxywatch8#046` · `h8` · `…dưới bên cạnh của Galaxy Watch⟦8⟧ được nhấn và màn hình hiển th…`
- `dh-samsung-galaxywatch8#047` · `h8` · `… độ chạy của bạn. Galaxy Watch⟦8⟧ hiển thị dòng chữ Cấp độ chạy…`
- `dh-samsung-galaxywatch8#047` · `h8` · `…i tiết’. Màn hình Galaxy Watch⟦8⟧ được cuộn xuống và nút Xem ch…`
- `dh-samsung-galaxywatch8#048` · `h8` · `… trên điện thoại. Galaxy Watch⟦8⟧ và điện thoại thông minh xuất…`
- `dh-samsung-galaxywatch8#049` · `h8` · `… bộ'. Bên phải là Galaxy Watch⟦8⟧ hiển thị thông báo Huấn luyện…`
- `dh-samsung-galaxywatch8#050` · `h8` · `…Nút dưới bên cạnh Galaxy Watch⟦8⟧ được nhấn và màn hình hiển th…`
- `dh-samsung-galaxywatch8#050` · `h8` · `…ủa thông báo trên Galaxy Watch⟦8⟧ được chạm vào. Văn bản hiển t…`
- `dh-samsung-galaxywatch8#051` · `h8` · `… bộ⏎Màn hình trên Galaxy Watch⟦8⟧ được cuộn xuống và xuất hiện …`
- `dh-samsung-galaxywatch8#051` · `h8` · `…đầu hiển thị trên Galaxy Watch⟦8⟧ được chạm vào. Màn hình thay …`
- `dh-samsung-galaxywatch8#051` · `h8` · `…ành, làm tốt lắm! Galaxy Watch⟦8⟧ hiển thị biểu tượng dấu kiểm,…`
- `dh-samsung-galaxywatch8#052` · `h8` · `…uấn luyện Chạy bộ⏎Galaxy Watch⟦8⟧ hiển thị biểu tượng người chạ…`
- `dh-samsung-galaxywatch8#052` · `h8` · `…iết hiển thị trên Galaxy Watch⟦8⟧ được chạm vào. Các phân cảnh …`
- `dh-samsung-galaxywatch8#054` · `h8` · `…ện tập? Bên phải, Galaxy Watch⟦8⟧ hiển thị danh sách các buổi l…`
- `dh-samsung-galaxywatch8#054` · `h8` · `…cấp rồi! Màn hình Galaxy Watch⟦8⟧ được cuộn xuống và mục Bài ki…`
- `dh-samsung-galaxywatch8#055` · `h8` · `…iếp tục chạy nhé. Galaxy Watch⟦8⟧ hiển thị biểu tượng số 4, dòn…`
- `dh-samsung-galaxywatch8#056` · `h8` · `…tch. Cảnh chuyển. Galaxy Watch⟦8⟧ Classic được đặt nghiêng sang…`
- `dh-samsung-galaxywatch8#056` · `h8` · `…êng sang một bên. Galaxy Watch⟦8⟧ được đặt phía trước và hơi ng…`
- `dh-samsung-galaxywatch8#056` · `h8` · `… phía trước, cạnh Galaxy Watch⟦8⟧ Classic. Dòng chữ Galaxy Watc…`
- `dh-samsung-galaxywatch8#056` · `h8` · `…Classic. Dòng chữ Galaxy Watch⟦8⟧ Watch8 Classic. Cảnh chuyển. …`
- `dh-samsung-galaxywatch8#056` · `h8` · `…. Dòng chữ Galaxy Watch8 Watch⟦8⟧ Classic. Cảnh chuyển. Xuất hi…`
- `dh-samsung-galaxywatch8#057` · `h8` · `…uyện Chạy bộ trên Galaxy Watch⟦8⟧ với dòng chữ 2. Lặp lại. 1,80…`
- `dh-samsung-galaxywatch8#059` · `h8` · `…ộng được bao lâu. Galaxy Watch⟦8⟧ tự động đo đếm số bước chân, …`
- `dh-samsung-galaxywatch8#061` · `h8` · `… khi bạn ngủ. Đeo Galaxy Watch⟦8⟧ ít nhất 4 giờ mỗi đêm trong h…`
- `dh-samsung-galaxywatch8#062` · `h8` · `…ện thoại của bạn. Galaxy Watch⟦8⟧ Classic và điện thoại thông m…`
- `dh-samsung-galaxywatch8#062` · `h8` · `…ết nối’. Màn hình Galaxy Watch⟦8⟧ hiển thị dòng chữ Chào mừng, …`
- `dh-samsung-galaxywatch8#062` · `h8` · `… lên với hình ảnh Galaxy Watch⟦8⟧ Classic xoay 360 độ.`
- `dh-samsung-galaxywatch8#063` · `h8` · `…uyện tập⏎Dòng chữ Galaxy Watch⟦8⟧ Classic, Một thiết bị mới vừa…`
- `dh-samsung-galaxywatch8#063` · `h8` · `…hác. Cảnh chuyển. Galaxy Watch⟦8⟧ Classic ở bên phải. Bên trái …`
- `dh-samsung-galaxywatch8#063` · `h8` · `…iện ích. Màn hình Galaxy Watch⟦8⟧ Classic được vuốt sang trái v…`
- `dh-samsung-galaxywatch8#063` · `h8` · `…ện ích’. Màn hình Galaxy Watch⟦8⟧ Classic được chạm vào.`
- `dh-samsung-galaxywatch8#064` · `h8` · `…c khỏe’. Màn hình Galaxy Watch⟦8⟧ Classic được cuộn xuống. Chỉ …`
- `dh-samsung-galaxywatch8#065` · `h8` · `…g mạch máu’. Trên Galaxy Watch⟦8⟧ Classic, Tải trọng mạch máu đ…`
- `dh-samsung-galaxywatch8#065` · `h8` · `… thoại’. Màn hình Galaxy Watch⟦8⟧ Classic được cuộn xuống và nú…`
- `dh-samsung-galaxywatch8#066` · `h8` · `…tch (Galaxy Watch Ultra, Watch⟦8⟧ hoặc các mẫu Galaxy Watch thế…`
- `dh-samsung-galaxywatch8#068` · `h8` · `…tch (Galaxy Watch Ultra, Watch⟦8⟧ hoặc các dòng Galaxy Watch đư…`
- `dh-samsung-galaxywatch8#070` · `h8` · `…tch (Galaxy Watch Ultra, Watch⟦8⟧ hoặc các dòng Galaxy Watch đư…`
- `dh-samsung-galaxywatch8#071` · `h8` · `…cảnh. Bên phải là Galaxy Watch⟦8⟧ Classic đang hiển thị tính nă…`
- `dh-samsung-galaxywatch8#072` · `h8` · `…ái cân bằng. Trên Galaxy Watch⟦8⟧ Classic, biểu tượng Tải trọng…`
- `dh-samsung-galaxywatch8#072` · `h8` · `… ở mức cao,. Trên Galaxy Watch⟦8⟧ Classic, biểu tượng Tải trọng…`
- `dh-samsung-galaxywatch8#073` · `h8` · `…uyện tập⏎Màn hình Galaxy Watch⟦8⟧ Classic được cuộn xuống và nú…`
- `dh-samsung-galaxywatch8#073` · `h8` · `…tch (Galaxy Watch Ultra, Watch⟦8⟧ hoặc các dòng Galaxy Watch đư…`
- `dh-samsung-galaxywatch8#075` · `h8` · `…tch (Galaxy Watch Ultra, Watch⟦8⟧ hoặc các dòng Galaxy Watch đư…`
- `dh-samsung-galaxywatch8#076` · `h8` · `…Cảnh chuyển tiếp. Galaxy Watch⟦8⟧ Classic đặt nghiêng sang một …`
- `dh-samsung-galaxywatch8#076` · `h8` · `…êng sang một bên. Galaxy Watch⟦8⟧ xuất hiện ở góc nhìn nghiêng …`
- `dh-samsung-galaxywatch8#076` · `h8` · `… và được đặt cạnh Galaxy Watch⟦8⟧ Classic.`
- `dh-samsung-galaxywatch8#077` · `h8` · `…uyện tập⏎Dòng chữ Galaxy Watch⟦8⟧ Watch8 Classic. Chuyển cảnh. …`
- `dh-samsung-galaxywatch8#077` · `h8` · `…p⏎Dòng chữ Galaxy Watch8 Watch⟦8⟧ Classic. Chuyển cảnh. Ở giữa …`
- `dh-samsung-galaxywatch8#077` · `h8` · `…iến quang học của Galaxy Watch⟦8⟧ đo Sức ép lên mạch máu. Sau đ…`
- `dh-samsung-galaxywatch8#077` · `h8` · `…mạch máu. Sau đó, Galaxy Watch⟦8⟧ xuất hiện, với các dòng chữ '…`
- `dh-samsung-galaxywatch8#078` · `h8` · `…a bạn. Hiệu chỉnh Galaxy Watch⟦8⟧ và bắt đầu đo bằng ứng dụng S…`
- `dh-samsung-galaxywatch8#081` · `h8` · `…iến ở mặt sau của Galaxy Watch⟦8⟧ và màn hình sẽ hiển thị chỉ s…`
- `dh-samsung-galaxywatch8#082` · `h8` · `…, AGEs) của mình. Galaxy Watch⟦8⟧ theo dõi chỉ số AGEs theo bốn…`
- `dh-samsung-galaxywatch8#085` · `h8` · `… giác thanh thản. Galaxy Watch⟦8⟧ mang đến các công cụ nhẹ nhàn…`
- `dh-samsung-galaxywatch8#086` · `h8` · `…i tâm trí của bạn⏎Galaxy Watch⟦8⟧ hiển thị thông báo kiểm tra t…`
- `dh-samsung-galaxywatch8#088` · `h8` · `…t cứ lúc nào trên Galaxy Watch⟦8⟧ của bạn. Chọn một trong ba kỹ…`
- `dh-samsung-galaxywatch8#089` · `h8` · `…lường nâng cao để Galaxy Watch⟦8⟧ có thể theo dõi những thay đổ…`
- `dh-samsung-galaxywatch8#090` · `h8` · `…a Natural Cycles. Galaxy Watch⟦8⟧ giúp dự báo chu kỳ kinh nguyệ…`
- `dh-samsung-galaxywatch8#091` · `h8` · `…ẵn sàng trợ giúp. Galaxy Watch⟦8⟧ tích hợp Gemini giúp bạn hoàn…`
- `dh-samsung-galaxywatch8#092` · `h8` · `…ới thanh Now Bar.⏎Galaxy Watch⟦8⟧ hiển thị các màn hình khác nh…`
- `dh-samsung-galaxywatch8#098` · `p7` · `Galaxy Z Flip⟦7⟧⏎Tìm hiểu thêm⏎Galaxy S25 Ultr…`
- `dh-samsung-galaxywatch8#098` · `s3` · `…ltra⏎Tìm hiểu thêm⏎Galaxy Buds⟦3⟧ Pro⏎Tìm hiểu thêm⏎So sánh Đồn…`
- `dh-samsung-galaxywatch8#098` · `h8` · `… hợp nhất cho bạn⏎Galaxy Watch⟦8⟧⏎44 mm⏎40 mm⏎Màu sắc⏎Xám⏎Bạc⏎G…`
- `dh-samsung-galaxywatch8#098` · `h7` · `…m⏎Màu sắc⏎Xám⏎Bạc⏎Galaxy Watch⟦7⟧⏎44 mm⏎40 mm⏎Màu sắc⏎Kem⏎Xanh⏎…`
- `dh-samsung-galaxywatch8#098` · `h6` · `…⏎Màu sắc⏎Kem⏎Xanh⏎Galaxy Watch⟦6⟧⏎44 mm⏎40 mm⏎Màu sắc⏎Xám⏎Vàng …`
- `dh-samsung-galaxywatch8#099` · `h8` · `Galaxy Watch⟦8⟧⏎Vật liệu⏎Armor Aluminium⏎Gala…`
- `dh-samsung-galaxywatch8#099` · `h7` · `…u⏎Armor Aluminium⏎Galaxy Watch⟦7⟧⏎Vật liệu⏎Armor Aluminium⏎Gala…`
- `dh-samsung-galaxywatch8#099` · `h6` · `…u⏎Armor Aluminium⏎Galaxy Watch⟦6⟧⏎Vật liệu⏎Armor Aluminium⏎Gala…`
- `dh-samsung-galaxywatch8#099` · `h8` · `…u⏎Armor Aluminium⏎Galaxy Watch⟦8⟧⏎Bộ vi xử lý⏎Bộ xử lý 3 nm, 5 …`
- `dh-samsung-galaxywatch8#100` · `h7` · `Galaxy Watch⟦7⟧⏎Bộ vi xử lý⏎Bộ xử lý 3 nm, 5 …`
- `dh-samsung-galaxywatch8#100` · `h6` · `…xử lý 3 nm, 5 Lõi⏎Galaxy Watch⟦6⟧⏎Bộ vi xử lý⏎Bộ xử lý 5 nm, 2 …`
- `dh-samsung-galaxywatch8#100` · `h8` · `…xử lý 5 nm, 2 Lõi⏎Galaxy Watch⟦8⟧⏎GPS⏎L1+L5 Kép-⏎Tần số GPS⏎Gal…`
- `dh-samsung-galaxywatch8#100` · `h7` · `…5 Kép-⏎Tần số GPS⏎Galaxy Watch⟦7⟧⏎GPS⏎L1+L5 Kép-⏎Tần số GPS`
- `dh-samsung-galaxywatch8#101` · `h6` · `Galaxy Watch⟦6⟧⏎GPS⏎L1 GPS⏎Galaxy Watch8⏎Kết …`
- `dh-samsung-galaxywatch8#101` · `h8` · `…Watch6⏎GPS⏎L1 GPS⏎Galaxy Watch⟦8⟧⏎Kết nối⏎Bluetooth / Bluetooth…`
- `dh-samsung-galaxywatch8#101` · `h7` · `…/ Bluetooth + LTE⏎Galaxy Watch⟦7⟧⏎Kết nối⏎Bluetooth / Bluetooth…`
- `dh-samsung-galaxywatch8#101` · `h6` · `…/ Bluetooth + LTE⏎Galaxy Watch⟦6⟧⏎Kết nối⏎Bluetooth / Bluetooth…`
- `dh-samsung-galaxywatch8#102` · `h8` · `Galaxy Watch⟦8⟧⏎Bộ nhớ / Lưu trữ⏎2 GB / 32 GB…`
- `dh-samsung-galaxywatch8#102` · `h7` · `… trữ⏎2 GB / 32 GB⏎Galaxy Watch⟦7⟧⏎Bộ nhớ / Lưu trữ⏎2 GB / 32 GB…`
- `dh-samsung-galaxywatch8#102` · `h6` · `… trữ⏎2 GB / 32 GB⏎Galaxy Watch⟦6⟧⏎Bộ nhớ / Lưu trữ⏎2 GB / 16 GB…`
- `dh-samsung-galaxywatch8#102` · `h8` · `… trữ⏎2 GB / 16 GB⏎Galaxy Watch⟦8⟧⏎Độ sáng hiển thị⏎Lên đến 3000…`
- `dh-samsung-galaxywatch8#103` · `h7` · `Galaxy Watch⟦7⟧⏎Độ sáng hiển thị⏎Lên đến 2000…`
- `dh-samsung-galaxywatch8#103` · `h6` · `…Lên đến 2000 nits⏎Galaxy Watch⟦6⟧⏎Độ sáng hiển thị⏎Lên đến 2000…`
- `dh-samsung-galaxywatch8#103` · `h8` · `…Lên đến 2000 nits⏎Galaxy Watch⟦8⟧⏎Độ bền⏎5ATM + IP68 / MIL-STD-…`
- `dh-samsung-galaxywatch8#103` · `h7` · `…68 / MIL-STD-810H⏎Galaxy Watch⟦7⟧⏎Độ bền⏎5ATM + IP68 / MIL-STD-…`
- `dh-samsung-galaxywatch8#104` · `h6` · `Galaxy Watch⟦6⟧⏎Độ bền⏎5ATM + IP68 / MIL-STD-…`
- `dh-samsung-galaxywatch8#104` · `h8` · `…68 / MIL-STD-810H⏎Galaxy Watch⟦8⟧⏎Pin⏎325 mAh⏎Lên đến 30 giờ (*…`
- `dh-samsung-galaxywatch8#104` · `h7` · `…30 giờ (*Bật AOD)⏎Galaxy Watch⟦7⟧⏎Pin⏎300 mAh⏎Lên đến 30 giờ (*…`
- `dh-samsung-galaxywatch8#105` · `h6` · `Galaxy Watch⟦6⟧⏎Pin⏎300 mAh⏎Lên đến 30 giờ (*…`
- `dh-samsung-galaxywatch8#105` · `h8` · `…30 giờ (*Bật AOD)⏎Galaxy Watch⟦8⟧⏎An toàn và Khẩn cấp⏎SOS / Phá…`
- `dh-samsung-galaxywatch8#105` · `h7` · `… Phát hiện té ngã⏎Galaxy Watch⟦7⟧⏎An toàn và Khẩn cấp⏎SOS / Phá…`
- `dh-samsung-galaxywatch8#106` · `h6` · `Galaxy Watch⟦6⟧⏎An toàn và Khẩn cấp⏎SOS / Phá…`
- `dh-samsung-galaxywatch8#106` · `h8` · `… Phát hiện té ngã⏎Galaxy Watch⟦8⟧⏎Sức khỏe⏎Energy Score⏎Ngưng t…`
- `dh-samsung-galaxywatch8#107` · `h7` · `Galaxy Watch⟦7⟧⏎Sức khỏe⏎Energy Score⏎Ngưng t…`
- `dh-samsung-galaxywatch8#108` · `h6` · `Galaxy Watch⟦6⟧⏎Sức khỏe⏎Energy Score⏎Ngưng t…`
- `dh-samsung-galaxywatch8#108` · `h8` · `…ể⏎Theo dõi chu kỳ⏎Galaxy Watch⟦8⟧`
- `dh-samsung-galaxywatch8#109` · `h7` · `…emini⏎O⏎available⏎Galaxy Watch⟦7⟧⏎Google Gemini⏎not available⏎G…`
- `dh-samsung-galaxywatch8#109` · `h6` · `…ini⏎not available⏎Galaxy Watch⟦6⟧⏎Google Gemini⏎not available⏎G…`
- `dh-samsung-galaxywatch8#109` · `h8` · `…ini⏎not available⏎Galaxy Watch⟦8⟧⏎Nút xử lý nhanh⏎not available`
- `dh-samsung-galaxywatch8#110` · `h7` · `Galaxy Watch⟦7⟧⏎Nút xử lý nhanh⏎not available…`
- `dh-samsung-galaxywatch8#110` · `h6` · `…anh⏎not available⏎Galaxy Watch⟦6⟧⏎Nút xử lý nhanh⏎not available…`
- `dh-samsung-galaxywatch8#110` · `h8` · `… gặp⏎Thiết kế của Galaxy Watch⟦8⟧ có gì thay đổi?⏎Thiết kế đệm …`
- `dh-samsung-galaxywatch8#110` · `h8` · `… mái hơn.⏎Tại sao Galaxy Watch⟦8⟧ lại tốt cho các hoạt động ngo…`
- `dh-samsung-galaxywatch8#111` · `h8` · `Galaxy Watch⟦8⟧ có màn hình độ sáng 3.000 nit…`
- `dh-samsung-galaxywatch8#112` · `h8` · `Galaxy Watch⟦8⟧ có những màu sắc và kích thướ…`
- `dh-samsung-galaxywatch8#112` · `h8` · `…hước nào?⏎Đồng hồ Galaxy Watch⟦8⟧ có màu Bạc và Xám. Sản phẩm c…`
- `dh-samsung-galaxywatch8#112` · `h8` · `…) và Lớn (44 mm).⏎Galaxy Watch⟦8⟧ có thể theo dõi mức độ căng t…`
- `dh-samsung-galaxywatch8#112` · `h8` · `…ủa tôi không?⏎Có, Galaxy Watch⟦8⟧ có thể theo dõi mức độ căng t…`
- `dh-samsung-galaxywatch8#112` · `h8` · `… có thể thiết lập Galaxy Watch⟦8⟧ để tự động theo dõi mức độ că…`
- `dh-samsung-galaxywatch8#113` · `h8` · `Galaxy Watch⟦8⟧ có những màu sắc và kích thướ…`
- `dh-samsung-galaxywatch8#113` · `h8` · `…o?⏎Dung lượng pin Galaxy Watch⟦8⟧ là bao nhiêu?⏎Thời gian dùng …`
- `dh-samsung-galaxywatch8#113` · `h8` · `…hời gian dùng pin Galaxy Watch⟦8⟧ thay đổi tùy thuộc vào mức sử…`
- `dh-samsung-galaxywatch8#114` · `h8` · `Galaxy Watch⟦8⟧ có hỗ trợ cả LTE và Bluetooth…`
- `dh-samsung-galaxywatch8#115` · `h8` · `Galaxy Watch⟦8⟧ có hỗ trợ cả LTE và Bluetooth…`
- `dh-samsung-galaxywatch8#115` · `h8` · `… Bluetooth không?⏎Galaxy Watch⟦8⟧ có cả phiên bản LTE và Blueto…`
- `dh-samsung-galaxywatch8#116` · `h8` · `…ới Galaxy Watch8?⏎Galaxy Watch⟦8⟧ hoạt động với điện thoại thôn…`
- `dh-samsung-galaxywatch8#116` · `h8` · `…droid 12 trở lên.⏎Galaxy Watch⟦8⟧ có GPS băng tần kép không?⏎Có…`
- `dh-samsung-galaxywatch8#116` · `h8` · `…ần kép không?⏎Có, Galaxy Watch⟦8⟧ có GPS băng tần kép. Đồng hồ …`
- `dh-samsung-galaxywatch8#116` · `h8` · `…độ chính xác.⏎Sạc Galaxy Watch⟦8⟧ như thế nào?⏎Bạn có thể sạc G…`
- `dh-samsung-galaxywatch8#116` · `h8` · `…o?⏎Bạn có thể sạc Galaxy Watch⟦8⟧ bằng Sạc không dây đi kèm. Ch…`
- `dh-samsung-galaxywatch8#117` · `h8` · `… chỉ khả dụng với Galaxy Watch⟦8⟧ Series hoặc Galaxy Watch Seri…`
- `dh-samsung-galaxywatch8#124` · `h8` · `… tin SAR⏎Đánh giá⏎Galaxy Watch⟦8⟧ (Bluetooth, 44 mm)⏎Product ra…`
- `dh-samsung-galaxywatch8#127` · `s25` · `…it on number sharing with my s⟦25⟧ ultra.`
- `dh-samsung-galaxywatch8#130` · `k26` · `…ng lần đầu trên Samsung UK⏎Mak⟦26⟧⏎2025-08-18⏎Wallington⏎Màu Sắc…`
- `dh-samsung-galaxywatch8#135` · `h8` · `Dịch⏎I bought the watch⟦8⟧ about six months ago, replaci…`
- `dh-samsung-galaxywatch8#139` · `h8` · `… cá nhân hóa trên Galaxy Watch⟦8⟧ và Watch8 Classic⏎Cách gắn dâ…`
- `dh-samsung-galaxywatch8#139` · `h8` · `…óa trên Galaxy Watch8 và Watch⟦8⟧ Classic⏎Cách gắn dây đeo vào …`
- `dh-samsung-galaxywatch8#139` · `h8` · `…h gắn dây đeo vào Galaxy Watch⟦8⟧ và Watch8 Classic⏎Galaxy Watc…`
- `dh-samsung-galaxywatch8#139` · `h8` · `…đeo vào Galaxy Watch8 và Watch⟦8⟧ Classic⏎Galaxy Watch không th…`
- `dh-samsung-galaxywatch8#140` · `h8` · `…ches⏎Galaxy Watch⏎Galaxy Watch⟦8⟧ (Bluetooth, 44 mm)⏎Footer Nav…`
- `dh-samsung-galaxywatch8#148` · `h8` · `… về Galaxy Watch8/Galaxy Watch⟦8⟧ Classic⏎7 Bố trí và các chức …`
- `dh-samsung-galaxywatch8#157` · `h8` · `… về Galaxy Watch8/Galaxy Watch⟦8⟧ Classic⏎Galaxy Watch8/Galaxy …`
- `dh-samsung-galaxywatch8#157` · `h8` · `…sic⏎Galaxy Watch8/Galaxy Watch⟦8⟧ Classic (sau đây gọi là Đồng …`
- `dh-samsung-galaxywatch8#160` · `h8` · `Bắt đầu⏎▶ Galaxy Watch⟦8⟧ Classic: SM-L500: ◀ Anten GPS…`
- `dh-samsung-galaxywatch8#166` · `h8` · `… hướng dẫn này là Galaxy Watch⟦8⟧ Classic.⏎Các phím⏎Phím`
- `dh-samsung-galaxywatch8#169` · `h8` · `… dụng phím Nhanh (Galaxy Watch⟦8⟧ Classic)⏎Phím Nhanh là phím t…`
- `dh-samsung-galaxywatch8#178` · `h8` · `…n khi đang sạc. • Galaxy Watch⟦8⟧ Classic và Galaxy Watch8 khôn…`
- `dh-samsung-galaxywatch8#178` · `h8` · `…Watch8 Classic và Galaxy Watch⟦8⟧ không hỗ trợ tính năng Chia s…`
- `dh-samsung-galaxywatch8#185` · `h8` · `Bắt đầu ▶ Galaxy Watch⟦8⟧ Classic: Đặt mặt sau của Đồng…`
- `dh-samsung-galaxywatch8#211` · `h8` · `…atch8)⏎Vòng xoay (Galaxy Watch⟦8⟧ Classic)⏎• Cuộn qua các màn h…`
- `dh-samsung-galaxywatch8#220` · `h8` · `… màn hình để bật (Galaxy Watch⟦8⟧ Classic).`
- `dh-samsung-galaxywatch8#313` · `h8` · `… trình tập luyện (Galaxy Watch⟦8⟧ Classic)`
- `dh-samsung-galaxywatch8#379` · `h8` · `…và bệnh mãn tính. Galaxy Watch⟦8⟧ Classic và Galaxy Watch8 có t…`
- `dh-samsung-galaxywatch8#379` · `h8` · `…Watch8 Classic và Galaxy Watch⟦8⟧ có thể đo chỉ số AGE tích lũy…`
- `dh-samsung-galaxywatch8#458` · `h8` · `… gian vòng chạy. (Galaxy Watch⟦8⟧ Classic)⏎Bộ sưu tập`
- `dh-samsung-galaxywatch8#519` · `h8` · `… dụng phím Nhanh (Galaxy Watch⟦8⟧ Classic) để biết thêm thông t…`
- `dh-samsung-galaxywatch8#519` · `h8` · `… thêm thông tin. (Galaxy Watch⟦8⟧ Classic)⏎• Phím Trang chính: …`

### 5.2 Mã chữ hoa + số, số đó cũng đã bị bỏ như ký hiệu ở chỗ khác của mẫu

Regex ở 5.1 không thấy chữ hoa. Bảng này gom mã chữ hoa + 1-2 chữ số còn trong `noi_dung` (ví dụ `AI10`, `X8`, `S25`) mà số đó cũng đã bị bỏ như ký hiệu trong cùng mẫu. Phần còn lại là tên máy hoặc tên chuẩn (`AV1`, `HDR10`). `AI10` của Xiaomi 15T trước đây nằm ở đây nay đã bỏ bằng bảng ghi tay.

| Mẫu | Mã | Số lần | Ví dụ |
|---|---|---:|---|
| dt-apple-iphone17 | `A19` | 1 | `dt-apple-iphone17#008` |
| dt-apple-iphone17 | `N1` | 1 | `dt-apple-iphone17#017` |
| dt-apple-iphone17 | `AV1` | 1 | `dt-apple-iphone17#027` |
| dt-xiaomi-15t | `DCI-P3` | 1 | `dt-xiaomi-15t#004` |
| dt-xiaomi-15t | `L1+L5` | 1 | `dt-xiaomi-15t#012` |
| dt-xiaomi-15t | `L5` | 1 | `dt-xiaomi-15t#012` |
| tn-samsung-buds3pro | `IP57` | 4 | `tn-samsung-buds3pro#039` |
| tn-samsung-buds3pro | `S25` | 2 | `tn-samsung-buds3pro#042` |
| tn-samsung-buds3pro | `IPX2` | 1 | `tn-samsung-buds3pro#041` |
| tn-samsung-buds3pro | `BUDS3` | 1 | `tn-samsung-buds3pro#042` |
| dh-apple-watchse3 | `S10` | 1 | `dh-apple-watchse3#004` |
| dh-apple-watchse3 | `VO2` | 1 | `dh-apple-watchse3#011` |
| dh-apple-watchse3 | `L1` | 1 | `dh-apple-watchse3#016` |
| dt-oppo-findx8 | `X8` | 17 | `dt-oppo-findx8#002` |
| dt-oppo-findx8 | `X9` | 6 | `dt-oppo-findx8#014` |
| dt-oppo-findx8 | `A6` | 4 | `dt-oppo-findx8#014` |
| dt-oppo-findx8 | `DCI-P3` | 3 | `dt-oppo-findx8#003` |
| dt-oppo-findx8 | `(L1` | 2 | `dt-oppo-findx8#013` |
| dt-oppo-findx8 | `N6` | 2 | `dt-oppo-findx8#014` |
| dt-oppo-findx8 | `A7` | 2 | `dt-oppo-findx8#014` |
| dt-oppo-findx8 | `X3` | 2 | `dt-oppo-findx8#015` |
| dt-oppo-findx8 | `X2` | 2 | `dt-oppo-findx8#015` |
| dt-oppo-findx8 | `(E1` | 1 | `dt-oppo-findx8#013` |
| dt-samsung-galaxys25ultra | `S25` | 193 | `dt-samsung-galaxys25ultra#002` |
| dt-samsung-galaxys25ultra | `S21` | 4 | `dt-samsung-galaxys25ultra#037` |
| dt-samsung-galaxys25ultra | `S24` | 3 | `dt-samsung-galaxys25ultra#122` |
| dt-samsung-galaxys25ultra | `S23` | 1 | `dt-samsung-galaxys25ultra#122` |
| dt-samsung-galaxys25ultra | `S22` | 1 | `dt-samsung-galaxys25ultra#122` |
| dt-samsung-galaxys25ultra | `S20` | 1 | `dt-samsung-galaxys25ultra#122` |
| dt-samsung-galaxys25ultra | `S10` | 1 | `dt-samsung-galaxys25ultra#136` |
| tn-apple-airpodspro3 | `H2` | 1 | `tn-apple-airpodspro3#004` |
| tn-apple-airpods4 | `H2` | 1 | `tn-apple-airpods4#003` |
| dh-samsung-galaxywatch8 | `S25` | 12 | `dh-samsung-galaxywatch8#018` |
| dh-samsung-galaxywatch8 | `L1+L5` | 2 | `dh-samsung-galaxywatch8#100` |
| dh-samsung-galaxywatch8 | `L1` | 2 | `dh-samsung-galaxywatch8#101` |
| dh-samsung-galaxywatch8 | `VO2` | 1 | `dh-samsung-galaxywatch8#060` |
| dh-samsung-galaxywatch8 | `L5` | 1 | `dh-samsung-galaxywatch8#116` |

### 5.3 Đối chiếu với thẻ `<sup>` của page.html

Mỗi số trong thẻ `<sup>` hoặc liên kết ký hiệu (`data-sup`, `click_sup`) của `page.html`, ghép với 14 ký tự chữ đứng trước nó, được tìm trong `noi_dung_goc` (ký hiệu có trong văn bản) và trong `noi_dung` (ký hiệu còn sót), bỏ qua khoảng trắng. Con số là số cặp (đoạn, chữ + số) tìm được; 0 nghĩa là mục này không đối chiếu được (OPPO, AirPods 4 dùng thẻ khác; các trang Xiaomi dùng dấu `*`), các mẫu đó chỉ có 5.1 và 5.2.

| Mẫu | Có trong noi_dung_goc | Còn trong noi_dung |
|---|---:|---:|
| dt-apple-iphone17 | 29 | 0 |
| dt-xiaomi-15t | 15 | 0 |
| tn-samsung-buds3pro | 76 | 0 |
| dh-apple-watchse3 | 27 | 0 |
| dt-oppo-findx8 | 0 | 0 |
| dt-samsung-galaxys25ultra | 70 | 0 |
| dt-xiaomi-redminote14proplus5g | 0 | 0 |
| tn-apple-airpodspro3 | 29 | 0 |
| tn-apple-airpods4 | 0 | 0 |
| tn-xiaomi-redmibuds6pro | 0 | 0 |
| dh-samsung-galaxywatch8 | 59 | 0 |
| dh-xiaomi-watchs4 | 0 | 0 |

Còn lại trong `noi_dung`: không có.

## 6. Dấu `*` còn lại trong noi_dung (5 chỗ)

Dấu `*` chưa bị bỏ: không được `chia_doan` nhận là ký hiệu (ví dụ `(*Bật AOD)`), hoặc được nhận nhưng thuộc ba ngoại lệ nói ở đầu báo cáo.

- `dt-apple-iphone17#002` · `*` · `…th. trong 24 tháng.⏎Chú thích ⟦*⟧ biểu tượng⏎Mua⏎Tổng Quan⏎Thôn…`
- `dh-samsung-galaxywatch8#104` · `*` · `…8⏎Pin⏎325 mAh⏎Lên đến 30 giờ (⟦*⟧Bật AOD)⏎Galaxy Watch7⏎Pin⏎300…`
- `dh-samsung-galaxywatch8#104` · `*` · `…7⏎Pin⏎300 mAh⏎Lên đến 30 giờ (⟦*⟧Bật AOD)`
- `dh-samsung-galaxywatch8#105` · `*` · `…6⏎Pin⏎300 mAh⏎Lên đến 30 giờ (⟦*⟧Bật AOD)⏎Galaxy Watch8⏎An toàn…`
- `dh-samsung-galaxywatch8#129` · `*` · `…that I'll fall in love with. 5⟦*⟧ product that I would recommen…`

## 7. Bảng ghi tay (21 mục bỏ thêm, 1 mục giữ lại)

Hai hằng trong `src/kiemchung/chia_doan.py`, mỗi mục gồm mã đoạn, ngữ cảnh trong `noi_dung_goc` (chứa ký hiệu đúng một lần) và ký hiệu. Chỉ đổi `noi_dung`; `chu_thich` và cách gắn chú thích không đổi. Mục không tìm thấy ngữ cảnh, hoặc đã được bỏ rồi, là lỗi (`ValueError`) chứ không bị bỏ qua. Mỗi mục đã đối chiếu thẻ `<sup>` của `page.html`.

### 7.1 Ký hiệu bỏ thêm (`KY_HIEU_BO_THEM`): 21 mục, 29 chỗ

| Mẫu | Số mục | Số chỗ đã bỏ |
|---|---:|---:|
| dt-apple-iphone17 | 1 | 1 |
| dt-xiaomi-15t | 6 | 14 |
| dh-apple-watchse3 | 1 | 1 |
| dt-samsung-galaxys25ultra | 12 | 12 |
| dh-samsung-galaxywatch8 | 1 | 1 |

Từng chỗ (mã đoạn, ký hiệu, ngữ cảnh trước khi bỏ; `⟦…⟧` là chỗ bỏ):

- `dt-apple-iphone17#016` · `6` · `…⏎Sạc lên đến 50% trong 30 phút⟦6⟧ với bộ tiếp hợp 30W trở lên s…`
- `dt-xiaomi-15t#035` · `5` · `…n.⏎Bộ sưu tập Gold Collection ⟦5⟧`
- `dt-xiaomi-15t#041` · `10` · `…g giọng nói AI10⏎Phiên dịch AI⟦10⟧⏎Tìm kiếm AI10⏎Hình nền động A…`
- `dt-xiaomi-15t#041` · `10` · `…10⏎Phiên dịch AI10⏎Tìm kiếm AI⟦10⟧⏎Hình nền động AI10⏎Viết AI10⏎…`
- `dt-xiaomi-15t#041` · `10` · `…Tìm kiếm AI10⏎Hình nền động AI⟦10⟧⏎Viết AI10⏎Nhận dạng giọng nói…`
- `dt-xiaomi-15t#041` · `10` · `…I10⏎Hình nền động AI10⏎Viết AI⟦10⟧⏎Nhận dạng giọng nói AI10⏎Phiê…`
- `dt-xiaomi-15t#041` · `10` · `…ết AI10⏎Nhận dạng giọng nói AI⟦10⟧⏎Phiên dịch AI10⏎Tìm kiếm AI10…`
- `dt-xiaomi-15t#041` · `10` · `…g giọng nói AI10⏎Phiên dịch AI⟦10⟧⏎Tìm kiếm AI10⏎Hình nền động A…`
- `dt-xiaomi-15t#041` · `10` · `…10⏎Phiên dịch AI10⏎Tìm kiếm AI⟦10⟧⏎Hình nền động AI10⏎Viết AI10⏎…`
- `dt-xiaomi-15t#041` · `10` · `…Tìm kiếm AI10⏎Hình nền động AI⟦10⟧⏎Viết AI10⏎Nhận dạng giọng nói…`
- `dt-xiaomi-15t#041` · `10` · `…I10⏎Hình nền động AI10⏎Viết AI⟦10⟧⏎Nhận dạng giọng nói AI10⏎Phiê…`
- `dt-xiaomi-15t#041` · `10` · `…ết AI10⏎Nhận dạng giọng nói AI⟦10⟧⏎Phiên dịch AI10⏎Tìm kiếm AI10…`
- `dt-xiaomi-15t#041` · `10` · `…g giọng nói AI10⏎Phiên dịch AI⟦10⟧⏎Tìm kiếm AI10⏎Hình nền động A…`
- `dt-xiaomi-15t#041` · `10` · `…10⏎Phiên dịch AI10⏎Tìm kiếm AI⟦10⟧⏎Hình nền động AI10`
- `dt-xiaomi-15t#041` · `10` · `…Tìm kiếm AI10⏎Hình nền động AI⟦10⟧`
- `dh-apple-watchse3#004` · `1` · `…⏎Apple Intelligence và Siri AI⟦1⟧⏎Apple Intelligence thế hệ mới…`
- `dt-samsung-galaxys25ultra#034` · `1` · `…hỉ cần nhấn và ra lệnh là xong⟦1⟧⏎phát⏎Galaxy S25 Ultra nhìn th…`
- `dt-samsung-galaxys25ultra#034` · `2,3` · `…roVisual Engine tiên tiến nhất⟦2,3⟧⏎phát`
- `dt-samsung-galaxys25ultra#035` · `4` · `…chơi.⏎Thời lượng pin vượt trội⟦4⟧⏎phát⏎Cảnh quan thành phố thay…`
- `dt-samsung-galaxys25ultra#036` · `6` · `…hẩm đầy ấn tượng của chúng tôi⟦6⟧⏎360° loading⏎Xanh Titan⏎Đen T…`
- `dt-samsung-galaxys25ultra#037` · `33` · `… dày⏎8.2 mm⏎Trọng lượng⏎218 g ⟦33⟧⏎Galaxy S21 Ultra 5G⏎Độ dày⏎8.…`
- `dt-samsung-galaxys25ultra#037` · `33` · `… dày⏎8.9 mm⏎Trọng lượng⏎227 g ⟦33⟧⏎Thiết kế mượt mà, cấu trúc bề…`
- `dt-samsung-galaxys25ultra#038` · `34` · `…bởi các chuyên gia của Samsung⟦34⟧⏎Tìm hiểu thêm`
- `dt-samsung-galaxys25ultra#039` · `1` · `…hỉ cần nhấn và ra lệnh là xong⟦1⟧⏎phát`
- `dt-samsung-galaxys25ultra#111` · `3` · `…roVisual Engine tiên tiến nhất⟦3⟧⏎Công nghệ ProVisual Engine th…`
- `dt-samsung-galaxys25ultra#114` · `3` · `…Tele và thậm chí là Ultra Wide⟦3⟧⏎UW Macro⏎UW⏎Chụp bởi Galaxy S…`
- `dt-samsung-galaxys25ultra#128` · `4,35` · `…5 Ultra⏎Phát lại Video⏎31 giờ ⟦4,35⟧⏎Galaxy S21 Ultra 5G`
- `dt-samsung-galaxys25ultra#129` · `4,35` · `…ân chia⏎Phát lại Video⏎22 giờ ⟦4,35⟧⏎Dung lượng lưu trữ lên đến 1 …`
- `dh-samsung-galaxywatch8#015` · `1` · `…y đeo phù hợp với ngày của bạn⟦1⟧⏎view more⏎Dây đeo Thể thao⏎vi…`

### 7.2 Ngoại lệ giữ lại (`KY_HIEU_GIU_LAI`): 1 mục

Ký hiệu mà nhận diện đã nhận nhưng không phải ký hiệu chú thích, giữ nguyên trong `noi_dung` (ngữ cảnh lấy từ `noi_dung`):

- `dh-samsung-galaxywatch8#129` · `*` · `…that I'll fall in love with. 5⟦*⟧ product that I would recommen…`
