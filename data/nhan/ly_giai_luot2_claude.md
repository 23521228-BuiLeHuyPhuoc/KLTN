# Giải thích nhãn lượt 2 (Claude gán, chờ người thực hiện duyệt)

Hai agent architect gán theo hướng dẫn bản 2, chỉ đọc hướng dẫn, chữ của tuyên bố, đoạn tài liệu, cấu hình và chữ trên trang; không đọc nhãn lượt 1, câu hỏi nhãn hay kết quả B0. Ngày 02/11/2026.


Claude gán theo hướng dẫn bản 2, người thực hiện duyệt. Nguồn: `dt-apple-iphone17/doan.jsonl` (51 đoạn, chỉ trang chính). Mỗi con số then chốt chỉ nằm ở một đoạn: 120Hz `#004`; 1000 / 1600 / 3000 nit `#005`; IP68 `#007`; zoom 2x `#009`; 30 và 27 giờ, 20 phút, mốc 50% `#016`; 25W ở chú thích `#016` và ở `#021`; hộp chỉ có cáp `#040`. Chữ "2x" ở `#003`, `#018` là độ phân giải và MIMO, không phải zoom.

Tổng: DUNG 19 (D3), LECH 14 (D4: 13, D2: 1), SAI 2 (D5), CHUA_DU 0. PHÂN VÂN: tb-00009, tb-00019, tb-00022, tb-00026.

- **tb-00001 · LECH D4 `doi_dieu_kien`.** "màn hình 3000 nit với mọi điều kiện ánh sáng". Điều kiện: cụm phủ "mọi điều kiện ánh sáng" (mục 6.8) là nêu rõ chế độ hiển thị, lấy chế độ kém thuận lợi nhất được phủ là tiêu chuẩn (1000 nit); diện tích đo như hãng. D3 không khớp (3000 > 1000); D4: 3000 là số của chế độ ngoài trời. Như V49.
- **tb-00002 · LECH D4 `bo_dieu_kien`.** "thời gian xem video liên tục lên đến 30 giờ". Không nêu gì: "xem video" không kèm tải sẵn hay trực tuyến, "liên tục" không nêu hoạt động; "lên đến" là kiểu tối đa như hãng. Mặc định: hoạt động kém thuận lợi nhất, xem video trực tuyến 27 giờ. D4: 30 là số của xem video tải sẵn. Như V03.
- **tb-00003 · DUNG D3.** "chống nước IP68". Điều kiện thử như hãng công bố (không ghi `mac_dinh`). IP68 bằng IP68.
- **tb-00004 · LECH D4 `bo_dieu_kien`.** "sạc nhanh 50% chỉ trong 20 phút". Nêu rõ mốc 50%. Mặc định: không mua thêm bộ sạc, sạc bằng cáp. 20 phút chỉ đạt với bộ tiếp hợp 40W trở lên, bán riêng; hộp chỉ có cáp (`#040`). "Chỉ" không phải từ khẳng định. Như V21.
- **tb-00005 · DUNG D3.** "công nghệ ProMotion 120Hz". Mặc định kiểu tần số là tối đa; 120Hz khớp "thích ứng lên đến 120Hz".
- **tb-00006 · LECH D2 `doi_kieu_gia_tri`.** "thời lượng pin kéo dài hơn 24 giờ liên tục". "Liên tục" là chưa nêu hoạt động, mặc định 27 giờ. "Hơn 24 giờ" đứng liền con số là từ khẳng định nhóm mức sàn (QĐ4); 24 không cao hơn 27 nên dừng ở D2, ghi `khang_dinh=hơn`. Như V50; bỏ chữ "hơn" thì D3 Đúng.
- **tb-00007 · DUNG D3.** "màn hình ProMotion 120Hz". Như tb-00005.
- **tb-00008 · LECH D4 `bo_dieu_kien`.** "thời lượng pin lên đến 30 giờ". Không nêu hoạt động nên so ở 27 giờ; 30 là số xem video tải sẵn. Như V24.
- **tb-00009 · DUNG D3 · PHÂN VÂN.** "độ sáng màn hình tối đa ngoài trời lên đến 3000 nit giúp hiển thị rõ ràng dưới mọi điều kiện ánh sáng". Nêu rõ chế độ ngoài trời: chữ chỉ chế độ quyết định, "tối đa" chỉ là kiểu giá trị (mục 6.5 ý 4). Vế "giúp … dưới mọi điều kiện ánh sáng" nói tác dụng; con số đã có điều kiện trực tiếp cùng loại nên điều kiện trực tiếp thắng (mục 2, tiêu chí 2). 3000 bằng 3000.
  Phương án còn lại: coi cụm phủ ở vế tác dụng là điều kiện của con số, lấy chế độ kém nhất là tiêu chuẩn, ra LECH D4 `doi_dieu_kien` như tb-00001. Tôi nghiêng về Đúng vì "ngoài trời" gắn trực tiếp với 3000 nit. Ca này ra Đúng nên ảnh hưởng FAR, người duyệt cần chốt.
- **tb-00010 · DUNG D3.** "kháng nước chuẩn IP68". Như tb-00003.
- **tb-00011 · LECH D4 `bo_dieu_kien`.** "thời lượng xem video lên đến 30 giờ". Như V03.
- **tb-00012 · LECH D4 `bo_dieu_kien`.** Như tb-00004.
- **tb-00013 · DUNG D3.** "IP68 ở độ sâu 6 mét trong 30 phút". 6 m không quá 6 m, 30 phút không quá 30 phút nên cùng điều kiện thử; loại nước, hoạt động bị cấm như hãng. Như V06.
- **tb-00014 · DUNG D3.** Như tb-00005.
- **tb-00015 · DUNG D3.** "độ sáng đỉnh 3000 nit ngay cả dưới ánh nắng gay gắt". "Dưới ánh nắng" (phụ lục: `ngoai_troi`) là chữ chỉ chế độ rõ, nên "đỉnh" chỉ là kiểu giá trị, không rơi vào lối 2 của D1a như V47. "Ngay cả" chỉ mở đầu điều kiện (bảng mục 6.2). "Gay gắt" chỉ là mức độ; phụ lục đã có "dưới ánh nắng" nên không ghi `ngoai_cau_hinh`.
- **tb-00016 · LECH D4 `bo_dieu_kien`.** Như tb-00008.
- **tb-00017 · LECH D4 `bo_dieu_kien`.** "sạc nhanh 50% trong 20 phút". Như tb-00004 (không có chữ "chỉ").
- **tb-00018 · DUNG D3.** "tần số làm mới 120Hz". Như tb-00005.
- **tb-00019 · SAI D5 `doi_gia_tri` · PHÂN VÂN.** "công nghệ sạc nhanh 30 W" (thuộc tính công suất sạc). Mặc định: không mua thêm bộ sạc, sạc có dây (cách sạc áp dụng vì máy có cả sạc cáp lẫn không dây). Tài liệu chỉ có công suất 25W khi sạc không dây (MagSafe, Qi2), không có số cho sạc có dây. 30W trong tài liệu chỉ là mức tối thiểu của bộ tiếp hợp ("30W trở lên"), không phải giá trị (mục 6.9), nên ghi `nham_vai=30W`. D1 không thỏa (có số 25W); D3 không có số có dây; D4: 30 khác 25; D5: 30 thuận lợi hơn mọi giá trị công bố, nên Sai.
  Phương án còn lại: D6 Chưa đủ, nếu "mọi giá trị" ở D5 không tính giá trị của một cách sạc khác khi tài liệu không công bố công suất có dây. Theo chữ của mục 7 (chỉ loại trừ bộ phận, phiên bản) và định nghĩa Sai của đề cương thì là Sai.
- **tb-00020 · DUNG D3.** "ProMotion 120Hz". Như tb-00005.
- **tb-00021 · DUNG D3.** "độ sáng màn hình lên tới 3000 nit ngay cả trong ánh sáng mạnh". "Ánh sáng mạnh" (phụ lục: `ngoai_troi`) nêu chế độ; "lên tới" là kiểu tối đa. 3000 bằng 3000.
- **tb-00022 · LECH D4 `bo_dieu_kien` · PHÂN VÂN (chỉ ở loại).** "năng suất làm việc và giải trí kéo dài lên đến 30 giờ video". "30 giờ video" đọc theo nghĩa là xem video chưa rõ loại, tức chưa nêu hoạt động. Phụ lục chỉ có "xem video", "xem phim", nên ghi `ngoai_cau_hinh=giờ video`. "Làm việc và giải trí" tôi coi là cụm chung chung (mục 6.8 ý 2). Mặc định 27 giờ; 30 là số xem video tải sẵn.
  Phương án còn lại: coi "làm việc và giải trí" là cụm phủ kiểu "cho cả A và B", tức điều kiện nêu rõ, thì loại là `doi_dieu_kien`. Nhãn LECH D4 không đổi.
- **tb-00023 · LECH D4 `bo_dieu_kien`.** Như tb-00004.
- **tb-00024 · DUNG D3.** "zoom quang học 2x". Nêu rõ quang học. Mặc định: độ phóng đại (áp dụng vì hãng ghi cả độ phóng đại 2x lẫn phạm vi 4x) và chụp ảnh (áp dụng vì hãng tách zoom ảnh 10x, video 6x; như V28). 2x khớp "Độ phóng đại quang học 2x".
- **tb-00025 · DUNG D3.** "pin siêu bền 24 giờ sử dụng liên tục". "Siêu bền" là cụm khen; "sử dụng liên tục" là chưa nêu hoạt động, so ở 27 giờ; 24 kém thuận lợi hơn nên khớp. Không có từ khẳng định. Như ví dụ tự đặt ở mục 6.8 ý 3.
- **tb-00026 · SAI D5 `doi_gia_tri` · PHÂN VÂN.** "sạc nhanh 30 W". Như tb-00019.
- **tb-00027 · DUNG D3.** "chống nước, bụi chuẩn IP68". Như tb-00003.
- **tb-00028 · LECH D4 `bo_dieu_kien`.** Như tb-00004.
- **tb-00029 · DUNG D3.** Như tb-00005.
- **tb-00030 · DUNG D3.** "độ sáng lên tới 3000 nit ngay cả dưới ánh nắng mạnh". "Dưới ánh nắng" nêu chế độ ngoài trời. Như tb-00021.
- **tb-00031 · LECH D4 `bo_dieu_kien`.** "pin kéo dài tới 30 giờ". "Tới" là kiểu tối đa. Như tb-00008.
- **tb-00032 · DUNG D3.** "màn hình luôn bật siêu mượt với ProMotion 120Hz". "Luôn" đi với "bật": đó là tên tính năng Màn hình Luôn Bật (`#004`), không gắn với 120Hz (mục 6.2, V40), nên không dừng ở D2. "Siêu mượt" là cụm khen. Mặc định kiểu tối đa, khớp.
- **tb-00033 · DUNG D3.** "hỗ trợ telephoto 2x". "Telephoto" (phụ lục: `quang_hoc`). Mặc định độ phóng đại, chụp ảnh. 2x khớp "Telephoto 2x chất lượng quang học".
- **tb-00034 · LECH D4 `bo_dieu_kien`.** "pin bền tới 30 giờ xem video". Như tb-00011.
- **tb-00035 · DUNG D3.** "sạc nhanh 50% chỉ trong 20 phút qua USB-C 40 W". Mục 6.8 ý 5: W đi cùng cổng sạc là công suất bộ tiếp hợp, 40W thỏa "40W trở lên". "Qua USB-C" là sạc bằng cáp, nêu rõ, nên không ghi `mac_dinh=cach_sac`; mốc 50% nêu rõ. Cấu hình chưa có cụm cho W đi cùng cổng sạc: ghi `ngoai_cau_hinh=qua USB-C 40 W`. Như V01.

**Lưu ý cho mục 11.2.** 7 trong 13 ca D4 (tb-00002, 00008, 00011, 00016, 00022, 00031, 00034) trùng số 30 giờ của xem video tải sẵn, trong khi hoạt động mặc định là xem video trực tuyến. Theo chữ của mục 11.2, đó là "trùng số khác hoạt động", nên riêng iPhone 17 đã vượt 1/4. Đây là ca `bo_dieu_kien` cốt lõi như V03, V24, không phải trùng số ngẫu nhiên như V42. Xem câu hỏi cuối trong `iphone17_cau_hoi.md`.


Người gán: Claude, theo hướng dẫn bản 2 (01/11/2026). Chỉ đọc chữ của tuyên bố (`tuyen_bo`, `thuoc_tinh`), tài liệu `data/nguon/tn-samsung-buds3pro/doan.jsonl`, cấu hình và hướng dẫn. Không mở nhãn lượt 1, kết quả B0 hay `cau_goc`.

## Số liệu của tài liệu dùng chung

Cột Buds3 Pro của bảng so sánh `#042` là cột đầu (thứ tự cột "Buds3 Pro, Buds3, Buds FE" ghi ở cuối `#039`; cột đầu ghi 7,0/30 và 6,0/26, khớp `#038`). Số 6,0/30, 5/24 thuộc Buds3; 8,5/30, 6,0/21 thuộc Buds FE: không tính.

| Chống ồn | Hoạt động | Tai nghe | Kèm hộp sạc | Đoạn |
|---|---|---|---|---|
| Bật | Nghe nhạc | 6 | **26 và 30 (mâu thuẫn, V48)** | `#038`, `#042`, `#044`; 30: dòng thứ hai của `#044` và chú thích `#038` |
| Tắt | Nghe nhạc | 7 | 30 | `#038`, `#042`, `#044` |
| Bật | Đàm thoại | 4,5 | 20 | `#044` |
| Tắt | Đàm thoại | 5 | 22 | `#044` |

Hộp sạc riêng: không có số (không tự trừ, mục 6.9). Kháng nước: IP57 cho tai nghe (`#044`, `#039`, `#041` cột Buds3 Pro, chú thích `#038`); hộp sạc không kháng nước. Dung lượng pin: tai nghe 50 mAh, hộp sạc 515 mAh, đều Typical (`#044`). Sạc nhanh: không có số nào.

Mặc định tai nghe (mục 5): chống ồn bật, chỉ tai nghe, nghe nhạc.

## Từng tuyên bố

- **tb-00036** "kháng nước chuẩn IP57 bền bỉ". Nêu: mã IP57; "bền bỉ" là cụm khen, bỏ qua. Mặc định: bộ phận tai nghe; điều kiện thử như hãng công bố. D3 Đúng: IP57 bằng IP57.
- **tb-00037** "tổng thời gian phát nhạc lên đến 30 giờ". Nêu: kèm hộp sạc ("tổng"), nghe nhạc. Mặc định: chống ồn bật. D1b: ở bật chống ồn, kèm hộp sạc, tài liệu ghi 26 và 30 (V48, ca đặc biệt trên trang gán nhãn).
- **tb-00038** "hộp sạc dung lượng 515mAh". Nêu: bộ phận hộp sạc. Kiểu không ghi nên hiểu là điển hình. D3 Đúng.
- **tb-00039** "Galaxy Buds3 Pro và hộp sạc cho tổng thời lượng sử dụng lên đến 30 giờ". Nêu: kèm hộp sạc. Mặc định: chống ồn bật; "thời lượng sử dụng" là mức dùng chung, coi như chưa nêu hoạt động (mục 6.8 ý 3), nên nghe nhạc. D1b như tb-00037 (gần như V48). **PHÂN VÂN**: nếu đọc "sử dụng" như tiêu đề nhóm "Thời gian sử dụng (bật ANC)" của bảng thông số, tức phủ cả đàm thoại và nghe nhạc, thì điều kiện là đàm thoại kèm hộp sạc khi bật chống ồn (20 giờ), 30 trùng tổng phát nhạc khi tắt chống ồn: D4 Lệch, `doi_dieu_kien`. Tôi không chọn vì tuyên bố không có cụm phủ ("cả", "mọi").
- **tb-00040** "thời gian phát tối đa 7 giờ khi nghe nhạc suốt cả ngày trên tai nghe". Nêu: nghe nhạc, tai nghe ("trên tai nghe" không đứng liền con số nên không phải từ mức sàn); "suốt cả ngày" là cụm khen. Mặc định: chống ồn bật (6 giờ). D3 không khớp; D4: 7 là số khi tắt chống ồn. Lệch, `bo_dieu_kien`.
- **tb-00041** "thời lượng pin khi kết nối âm nhạc lên đến 30 giờ". Nêu: nghe nhạc (đọc "kết nối âm nhạc" theo mục 6.8 ý 2, là hoàn cảnh của "Thời gian phát": "kết nối với điện thoại, phát nhạc trực tuyến"; `ngoai_cau_hinh`). Mặc định: chống ồn bật, chỉ tai nghe (6 giờ). D4: 30 là tổng kèm hộp sạc. Lệch, `bo_dieu_kien`. **PHÂN VÂN (chỉ ghi chú)**: coi "kết nối âm nhạc" là chưa nêu hoạt động thì ghi chú thêm `hoat_dong` vào `mac_dinh` và bỏ `ngoai_cau_hinh`; nhãn không đổi.
- **tb-00042** "tổng cộng thời gian phát lên tới 30 giờ khi sử dụng cùng hộp sạc". Nêu: kèm hộp sạc, nghe nhạc ("Thời gian phát"). Mặc định: chống ồn bật. D1b.
- **tb-00043** "chống bụi và kháng nước chuẩn IP57". Như tb-00036: D3 Đúng.
- **tb-00044** "dung lượng pin tai nghe 50 mAh". Nêu: tai nghe. D3 Đúng.
- **tb-00045** "hộp sạc dung lượng 515 mAh". Như tb-00038: D3 Đúng.
- **tb-00046** "thời gian đàm thoại lên tới 20 giờ ở chế độ bật ANC". Nêu: đàm thoại, bật chống ồn. Mặc định: chỉ tai nghe (4,5 giờ). D4: 20 là tổng đàm thoại kèm hộp sạc. Lệch, `bo_dieu_kien`.
- **tb-00047** "thời gian phát nhạc lên tới 26 giờ ở chế độ bật ANC". Nêu: nghe nhạc, bật chống ồn. Mặc định: chỉ tai nghe (6 giờ). D1b không xét vì mâu thuẫn ở điều kiện kèm hộp sạc, khác điều kiện của tuyên bố. D4: 26 là tổng kèm hộp sạc. Lệch, `bo_dieu_kien`.
- **tb-00048** "thời lượng phát nhạc ấn tượng lên đến 30 giờ khi kết hợp hộp sạc". Nêu: kèm hộp sạc, nghe nhạc. Mặc định: chống ồn bật. D1b.
- **tb-00049** "chuẩn kháng nước và bụi IP57 cho khả năng sử dụng bền bỉ". D3 Đúng như tb-00036.
- **tb-00050** "thời lượng pin lên tới 8 giờ liên tục". "Liên tục" không nêu hoạt động (mục 6.8 ý 3), không phải từ khẳng định. Mặc định cả ba (6 giờ). D4: 8 không trùng số nào của Buds3 Pro (8,5 của Buds FE không tính). D5: 8 cao hơn mọi số của tai nghe (cao nhất 7). Sai, `doi_gia_tri`, như V16.
- **tb-00051** "hộp sạc cung cấp thêm 24 giờ". Nêu: bộ phận hộp sạc (chủ ngữ, mục 6.8 ý 6). Mặc định: chống ồn bật, nghe nhạc. Hãng không công bố số riêng của hộp sạc; không trừ 30−7 hay 26−6. 24 không trùng số nào của Buds3 Pro (24 trong `#042` là cột Buds3). D5 không áp vì hộp sạc không có số nào để "thuận lợi hơn mọi giá trị". D6, như ví dụ ở mục 6.9.
- **tb-00052** "chống nước IPX4". Mặc định: tai nghe. IPX4 nhánh tia nước, IP57 nhánh ngâm: khác nhánh, không khớp ở D3; không trùng mã nào (hộp sạc không kháng nước; IPX2 là của Buds FE). D5 Sai, `doi_gia_tri` (mục 6.6).
- **tb-00053** "thời lượng pin lên tới 30 giờ (kèm hộp sạc)". Nêu: kèm hộp sạc. Mặc định: chống ồn bật, nghe nhạc. D1b.
- **tb-00054** "chuẩn kháng nước IP57". D3 Đúng.
- **tb-00055** "thời lượng pin 8 giờ nghe liên tục". "Nghe" không nêu nghe nhạc hay gọi (như "nghe" ở V38); "liên tục" coi như chưa nêu. D5 Sai như tb-00050.
- **tb-00056** (đã đổi ngày 02/11, xem cuối tệp) "tổng thời lượng pin 24 giờ cùng hộp sạc". Nêu: kèm hộp sạc. Mặc định: chống ồn bật, nghe nhạc. D1b dù 24 thấp hơn cả 26 và 30 (bảng D1b: "kém thuận lợi hơn cả hai" vẫn D1b). Nếu tài liệu không mâu thuẫn thì đây là D3 Đúng.
- **tb-00057** "chỉ cần 5 phút sạc để có thêm 2 giờ sử dụng". Sạc nhanh: tài liệu không có số nào. D1, như V45.
- **tb-00058** "lên đến 30 giờ (tắt ANC) cho cả nhạc và cuộc gọi". Nêu: tắt chống ồn; cụm phủ "cho cả A và B" về hoạt động, nên điều kiện là hoạt động kém thuận lợi nhất (đàm thoại). Mặc định: chỉ tai nghe (đàm thoại tắt chống ồn: 5 giờ). D4: 30 là tổng phát nhạc kèm hộp sạc khi tắt chống ồn. Hai điều kiện khác: hoạt động (nêu rõ qua cụm phủ) và bộ phận (mặc định); theo ưu tiên ở mục 8, chọn `doi_dieu_kien`. Phương án còn lại về loại: `bo_dieu_kien` nếu chỉ xét phần "nhạc" của cụm phủ.
- **tb-00059** "lên đến 26 giờ (bật ANC) cho cả nhạc và cuộc gọi". Như tb-00058: điều kiện là đàm thoại, tai nghe, bật chống ồn (4,5 giờ); 26 là tổng phát nhạc kèm hộp sạc. D4 Lệch, `doi_dieu_kien`.
- **tb-00060** "kèm hộp sạc 515 mAh cho lần sạc nhanh chóng". Đọc theo nghĩa: hộp sạc có 515 mAh, nên bộ phận hộp sạc; "sạc nhanh chóng" không có số. D3 Đúng. Chữ "kèm hộp sạc" trong phụ lục là `kem_hop_sac` (tổng), nhưng quy tắc 6.8 ý 6 chỉ nói cho thời lượng pin: ghi ở câu hỏi.
- **tb-00061** "độ bền vượt trội chuẩn IP57". "Vượt trội" là cụm khen. D3 Đúng.
- **tb-00062** "pin siêu bền lên tới 8 giờ nghe liên tục". "Siêu bền" là cụm khen. D5 Sai như tb-00055.
- **tb-00063** "kèm hộp sạc nhanh chỉ cần 5 phút cho 1 giờ sử dụng". Sạc nhanh: D1.
- **tb-00064** "chuẩn IP57 chống nước". D3 Đúng.
- **tb-00065** "lên tới 30 giờ (tắt ANC)". Nêu: tắt chống ồn. Mặc định: nghe nhạc, chỉ tai nghe (7 giờ). D4: 30 là tổng kèm hộp sạc. Lệch, `bo_dieu_kien`.
- **tb-00066** "lên tới 26 giờ (bật ANC)". Nêu: bật chống ồn. Mặc định: nghe nhạc, chỉ tai nghe (6 giờ). D4: 26 là tổng kèm hộp sạc. Lệch, `bo_dieu_kien`.

## Ghi chú về bằng chứng

- Nhãn Lệch có số trùng 30 giờ (tb-00041, 058, 065) ghi cả dòng "Tổng thời gian phát nhạc (Giờ, bật ANC) Lên đến 30" của `#044` vì đoạn này có số trùng (QĐ7); dòng đó nằm dưới nhóm tắt chống ồn nhưng ghi "bật ANC". Lý do không trích dòng này: tb-00058, 065 trích "Tắt Tính năng ANC Đến 7 / 30 giờ" (số tắt chống ồn, không mâu thuẫn); tb-00041 trích chú thích `#038` vì câu đó nói rõ bộ phận ("tai nghe và hộp tai nghe"), là điều kiện tuyên bố bỏ.
- Ca D1b có chống ồn lấy mặc định ghi thêm `#020` (chú thích "ANC … được bật theo mặc định"), như V10, V32.

## Sửa ngày 02/11/2026 sau rà soát (QĐ9–QĐ14 người thực hiện đã duyệt)

Một bản sao của Claude rà lại 66 nhãn: đồng ý 63/66, không nhãn nào phải đổi theo hướng dẫn lúc đó. Sau khi người thực hiện duyệt QĐ9–QĐ14, các nhãn sau đổi (gán lại không đọc nhãn lượt 1):

- **tb-00056 · CHUA_DU D1b → DUNG D3** (QĐ13). "tổng thời lượng pin 24 giờ cùng hộp sạc": điều kiện kèm hộp sạc, chống ồn bật và nghe nhạc theo mặc định. Tài liệu ghi hai số mâu thuẫn 26 và 30 giờ; 24 giờ kém thuận lợi hơn cả hai nên khớp ở mọi cách đọc, không dừng ở D1b, dò tiếp tới D3. Bỏ tick tài liệu mâu thuẫn, ghi `mau_thuan_khop_ca_hai=26/30`. Năm ca D1b còn lại (tb-00037, 039, 042, 048, 053) đều ghi 30 giờ, trùng một số và thuận lợi hơn số kia, nên vẫn D1b.
- **tb-00021 · ghi chú** (QĐ14). "ánh sáng mạnh" không còn trong phụ lục; đọc theo mục 6.8 ý 2 là hoàn cảnh của chế độ ngoài trời, nhãn giữ DUNG D3, thêm `ngoai_cau_hinh=ánh sáng mạnh`.
- **tb-00022 · ghi chú.** Thêm `ngoai_cau_hinh=giờ video` (giải thích đã nói vậy nhưng nhãn thiếu).
- **tb-00050, tb-00055, tb-00062 · ghi chú** (QĐ12). "liên tục" nay có trong phụ lục tai nghe (`chua_ro_hoat_dong`), bỏ `ngoai_cau_hinh=liên tục`.
- **tb-00039 · không đổi.** "sử dụng" đứng riêng nay có trong phụ lục (`chua_ro_hoat_dong`, QĐ12) nên không cần `ngoai_cau_hinh`; nhãn D1b như cũ (30 giờ).
- **tb-00009 · không đổi** (QĐ11). Điều kiện trực tiếp "ngoài trời" thắng cụm phủ ở vế tác dụng; DUNG D3 như lý do đã ghi.

Sau khi sửa: DUNG 30, LECH 22, SAI 6, CHUA_DU 8 (D1b 5, D1 2, D6 1). `kiem_nhan.py --luot 2` không lỗi.

## Sửa sau khi người thực hiện duyệt (02/11/2026, QĐ15)

Người thực hiện duyệt 66 nhãn. Năm nhóm nhãn người thực hiện không đồng ý lúc đầu được đối chiếu với hướng dẫn, khảo sát và kế hoạch; người thực hiện giữ cả năm nhóm, rồi nêu lại nhóm "xem video 30 giờ": tài liệu ghi nguyên văn "Thời gian xem video: Lên đến 30 giờ", không ghi "ngoại tuyến". Người thực hiện duyệt thêm luật chép đúng nhãn của tài liệu (QĐ15, hướng dẫn mục 6.8). Tệp nhãn sau duyệt là `data/nhan/thu_luot2.jsonl`; tệp này (`thu_luot2_claude.jsonl`) giữ bản Claude gán trước khi duyệt.

- `tb-00002`, `tb-00011`, `tb-00034` (xem video … 30 giờ), `tb-00022` (30 giờ video): LECH D4 `bo_dieu_kien` → DUNG D3, ghi `chep_nhan`. `nguoi_gan` đổi thành `phuoc`.
- `tb-00008`, `tb-00016`, `tb-00031` (pin 30 giờ, không trùng chữ nhãn nào): giữ LECH D4; lý do bỏ câu "chỉ đạt khi xem video tải sẵn (không trực tuyến)" vì tài liệu không ghi chữ đó, thay bằng "số của dòng “Thời gian xem video”". `nguoi_gan` đổi thành `phuoc`.
