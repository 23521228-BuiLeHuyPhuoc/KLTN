# Bước 27: thiết kế bộ quyết định A–D và sinh lý do

Opus viết ngày 08/11/2026, trước khi cài. Đặc tả cho `src/kiemchung/quyet_dinh.py`, `src/kiemchung/ly_do.py`, `tests/test_quyet_dinh.py`. Căn cứ: T5.5, T5.6, T5.8, T5.9 của kế hoạch; hướng dẫn gán nhãn bản 2 (mục 3–8, ví dụ mục 9); `chung.yaml` (`dieu_kien_la`, `chon_gia_tri_khi_khong_neu`, `cum_phu`, `hieu_thong_thuong_dac_biet`); đầu ra Bước 22 (`luan_van/buoc22_thiet_ke_trich_xuat.md`, mục 8).

Nguyên tắc: bộ quyết định là **bản cài của hướng dẫn mục 5–7**, không thêm quy tắc mới. Chỗ hướng dẫn nói bằng lời mà máy cần luật cụ thể thì luật đó được ghi ở đây và đánh dấu **[luật cài]**; mỗi luật cài có ví dụ của hướng dẫn làm kiểm thử.

## 1. Đầu vào, đầu ra

`quyet_dinh(ban_ghi, cau_hinh, doi_chieu=True, luat_chung_cho_nhieu_gia_tri=None)`:

- `ban_ghi`: bản ghi trích xuất của một tuyên bố (Bước 22): `ma_mau`, `tuyen_bo` (mục), `bang_chung` (các mục tài liệu đã qua neo nguồn), `loi`.
- `cau_hinh`: `doc_cau_hinh(nhom)` của nhóm theo tiền tố mã mẫu; `hang` của mẫu lấy từ `data/mau_san_pham.csv` (cho `cach_goi_theo_hang`).
- `doi_chieu=False` là P−ĐK (T5.9). `luat_chung_cho_nhieu_gia_tri=None` đọc từ `chung.yaml` (hiện `tat`).

Trả về:

```json
{"nhan": "LECH", "dong_d": "D4", "loai": "bo_dieu_kien",
 "bang_chung": ["dt-apple-iphone17#016"], "trich": "Thời gian xem video: Lên đến 30 giờ",
 "ly_do": "Giá trị 30 giờ chỉ đạt khi xem video; tuyên bố được hiểu là xem video trực tuyến. Nguồn: “Thời gian xem video: Lên đến 30 giờ”.",
 "ghi_chu": ["mac_dinh=hoat_dong"], "tai_lieu_mau_thuan": false,
 "vet": {"dieu_kien_tuyen_bo": {...}, "nguon_dieu_kien": {...}, "cung_dk": [...], "khac_dk": [...], "so_sanh": [...]}}
```

Trường giống bản ghi nhãn chuẩn (hướng dẫn mục 8) để so trực tiếp ở Bước 28, 37: `nhan`, `dong_d`, `loai`, `bang_chung`, `trich`, `ly_do`, `ghi_chu`, `tai_lieu_mau_thuan`. `vet` là dấu vết đầy đủ để sinh lý do và phân tích lỗi (Bước 38).

## 2. Bước A: thông số cùng sản phẩm và thuộc tính

1. Bản ghi có `loi`, hoặc tuyên bố không có `thuoc_tinh` hay `gia_tri`: `CHUA_DU`, `D1a`, ghi chú `chua_xac_dinh=trich_xuat_that_bai` **[luật cài]**. Bước 38 xếp các ca này vào lỗi trích xuất.
2. Tuyên bố gọi sản phẩm khác mẫu (`san_pham_ma` khác `ma_mau`, hoặc tên khớp `khong_nham_voi`): `CHUA_DU`, `D1` (tài liệu của sản phẩm tuyên bố nói không có trong kho).
3. `cung_tt` = các mục tài liệu cùng `thuoc_tinh`, có `gia_tri`, không `khac_san_pham`. Rỗng: `D1`, không ghi `mac_dinh`.
4. **Dạng của sạc nhanh đồng hồ** (`don_vi: phut_hoac_gio`) **[luật cài]**: giá trị tính bằng phút là dạng 1 (thời gian sạc tới mốc), bằng giờ là dạng 2 (số giờ dùng sau X phút sạc). Chỉ so trong cùng dạng; `cung_tt` chỉ giữ mục cùng dạng với tuyên bố; điều kiện có `pham_vi_ap_dung` "dạng 1" hay "dạng 2" chỉ áp cho dạng đó. Thuộc tính khác quy về đơn vị của thuộc tính (`quy_doi` giờ ↔ phút).

## 3. Bước B: điều kiện của tuyên bố

Xét từng điều kiện bắt buộc `c` của thuộc tính (`dieu_kien_bat_buoc`), theo thứ tự dưới; xong bước này thì điều kiện của tuyên bố giữ nguyên tới D6 (hướng dẫn mục 7). Không bao giờ dùng con số của tuyên bố để chọn điều kiện.

**B1. Điều kiện chưa xác định → D1a ngay** (điểm 14 ở T10):

- tuyên bố có `dieu_kien_khac` mà không phải cụm phủ (B4): `chua_xac_dinh=<cụm>`;
- `xung_dot` ở một điều kiện: `chua_xac_dinh=<cụm>`;
- chữ gọi mức cao trỏ tới nhiều chế độ (B5): `chua_xac_dinh=<chữ>`;
- điều kiện áp dụng (mục 4) có cách hiểu `khong_co_mac_dinh` mà tuyên bố không nêu, trừ khi "so thẳng" (B6): `mac_dinh=<c>`.

**B2. Luật chép đúng nhãn của tài liệu (QĐ15), xét trước cách hiểu mặc định** **[luật cài]**. Nhãn của một mục tài liệu là câu trích giá trị của mục đó bỏ đi con số, đơn vị, cụm kiểu giá trị, dấu câu, và bỏ các chữ chung đầu nhãn ("thời gian", "thời lượng"). Luật áp khi:

- nhãn còn ít nhất một chữ, và chữ tuyên bố (chuẩn hóa như neo nguồn) chứa **trọn** nhãn đó như một cụm liền;
- trong các nhãn được chứa, chọn nhãn dài nhất (không thiếu chữ điều kiện nào của nhãn). Hai nhãn dài bằng nhau mà điều kiện khác nhau thì không áp.

Áp thì mọi điều kiện mà mục đó có và tuyên bố chưa nêu rõ lấy theo mục đó; ghi `chep_nhan=<nhãn>`; các khóa này không vào `mac_dinh`. Ví dụ V03: nhãn "xem video" của "Thời gian xem video: Lên đến 30 giờ" nằm trọn trong "iPhone 17 xem video được 30 giờ", còn "xem video trực tuyến" thì không, nên điều kiện là `xem_video`. Danh sách chữ chung đầu nhãn để trong `chung.yaml` (khóa mới `chep_nhan.bo_chu_dau`, bổ sung khi cài).

**B3. Điều kiện nêu rõ** (từ bước trích xuất) giữ nguyên. Giá trị `chua_ro_hoat_dong`, `chua_ro_loai_video` (cụm "liên tục", "dùng", "xem video" không kèm loại) nghĩa là **chưa nêu**, chuyển sang B6 (hướng dẫn mục 6.8 ý 3, phụ lục cấu hình).

**B4. Cụm phủ nhiều giá trị** (hướng dẫn mục 6.8, `chung.yaml cum_phu`) **[luật cài]**: một mục `dieu_kien_khac` của tuyên bố khớp mẫu cụm phủ (cùng biểu thức với `scripts/ra_tach.py CUM_PHU`) thì không phải điều kiện lạ. Điều kiện được phủ:

| Mẫu | Điều kiện được phủ |
|---|---|
| "mọi chế độ" | điều kiện loại `che_do_hoat_dong` đầu tiên của thuộc tính không phải hoạt động (`che_do_nguon`, `che_do_chong_on`, `che_do_hien_thi`) |
| "mọi hoạt động" | `hoat_dong`; với kháng nước là `hoat_dong_cho_phep` hoặc `hoat_dong_bi_cam` (phủ cả hoạt động bị cấm) |
| "mọi điều kiện X", "bất kể X" | điều kiện có cụm X trong cấu hình; X là "ánh sáng" thì `che_do_hien_thi` |
| "dù A hay B", "cho cả A và B" | điều kiện mà A và B là hai giá trị của nó (tra `cach_dien_dat`) |

Không xác định được điều kiện được phủ thì vẫn là điều kiện lạ (B1). Điều kiện của tuyên bố là giá trị **kém thuận lợi nhất** trong các giá trị được phủ mà tài liệu công bố; điều kiện này tính là **nêu rõ** (Lệch thì `doi_dieu_kien`). Điều kiện trực tiếp cùng loại đã có ở tuyên bố thì thắng cụm phủ (QĐ11). Kháng nước: "mọi hoạt động" gồm hoạt động bị cấm, nên tuyên bố được coi là nêu hoạt động bị cấm.

**B5. Chữ gọi mức cao của độ sáng** (hướng dẫn mục 6.5): tuyên bố có `goi_muc_cao` và không có chữ chỉ chế độ rõ thì tra `cach_goi_theo_hang[hang][chữ]`, chỉ khi `cung_tt` có từ hai giá trị khác nhau (cùng bộ phận). Trỏ một chế độ: đó là chế độ nêu rõ của tuyên bố (V05 "tối đa" của Apple là tiêu chuẩn). Trỏ nhiều chế độ: D1a (V47 "đỉnh"). Tài liệu chỉ có một giá trị: chữ chỉ là kiểu giá trị tối đa, chế độ coi như chưa nêu (V43).

**B6. Cách hiểu mặc định** (`hieu_thong_thuong`), chỉ cho điều kiện **áp dụng** (mục 4) mà tuyên bố chưa nêu:

| Giá trị trong YAML | Điều kiện của tuyên bố | `mac_dinh` |
|---|---|---|
| giá trị cụ thể (`bat`, `tai_nghe`, `thuong`, `cap`, `quang_hoc`...) | giá trị đó | ghi |
| `kem_thuan_loi_nhat` | giá trị của `c` mà con số tài liệu (cùng bộ phận, phiên bản với tuyên bố) kém thuận lợi nhất | ghi |
| `khong_mua_them` | "chỉ đồ trong hộp": mục tài liệu có `bo_tiep_hop` (điều kiện dạng số về bộ sạc) là khác điều kiện **[luật cài]**, căn cứ hướng dẫn mục 5 (iPhone 17, Xiaomi 15T chỉ kèm cáp; bộ 20W của Watch SE 3 không có trong hộp) | ghi |
| `nhu_hang_cong_bo` | không ràng buộc (khớp mọi giá trị của `c`) | không ghi |
| `khong_co_mac_dinh` | D1a (B1), trừ khi so thẳng | ghi (khi D1a) |

**So thẳng** (`chon_gia_tri_khi_khong_neu.mot_gia_tri_khong_dieu_kien`): mọi mục của `cung_tt` cùng bộ phận chỉ có một giá trị (bằng nhau), và không mục nào có điều kiện nào (kể cả `dieu_kien_khac`, kể cả kiểu giá trị do chữ gọi mức cao) thì tuyên bố không nêu điều kiện so thẳng với giá trị đó (V12); không dừng ở D1a vì `khong_co_mac_dinh`. Lý do ghi "tài liệu không nêu điều kiện".

## 4. Điều kiện "áp dụng" và điều kiện của mục tài liệu

**Áp dụng** **[luật cài]**: điều kiện `c` áp dụng cho tuyên bố khi ít nhất một mục của `cung_tt` có `c` (nêu rõ hoặc bổ sung), hoặc `pham_vi_ap_dung[c]` là "dạng 1"/"dạng 2" khớp dạng của tuyên bố, hoặc `c` có cách hiểu `khong_co_mac_dinh` mà thuộc tính chỉ có nghĩa khi có `c` (mốc phần trăm của sạc nhanh dạng 1, số phút sạc của dạng 2; chế độ hiển thị của độ sáng điện thoại). Không áp dụng thì không ràng buộc và không ghi `mac_dinh` (hướng dẫn mục 4, mục 8: "Không ghi khóa không áp dụng"). Ví dụ: trang Watch SE 3 ghi chung 18 giờ cho hai phiên bản, nên phiên bản không áp dụng (V14, V15).

**Mục tài liệu không ghi `c`** **[luật cài]**: lấy theo cách hiểu mặc định nếu đó là giá trị cụ thể (bộ phận chính, chế độ thường...), theo hướng dẫn mục 6.7 ý 4 ("bộ phận chính; không mua thêm phụ kiện; ... chế độ mặc định của máy nếu hãng ghi"); `kem_thuan_loi_nhat`, `nhu_hang_cong_bo`, `khong_co_mac_dinh` thì không ràng buộc. `khong_mua_them` ở phía tài liệu: mục không có `bo_tiep_hop` là "chỉ đồ trong hộp".

## 5. So điều kiện: `khop_dieu_kien(dk, u)`

Cùng điều kiện khi mọi điều kiện bắt buộc áp dụng đều khớp:

- một bên không ràng buộc: khớp;
- điều kiện chữ: bằng nhau;
- điều kiện dạng số: `thoa_dieu_kien_so(thoa_khi, số của tuyên bố, số của tài liệu)` sau khi cùng đơn vị; tuyên bố có số mà tài liệu không có thì khớp nếu điều kiện của tài liệu là "như hãng công bố", không khớp nếu là "chỉ đồ trong hộp" của bộ sạc;
- kiểu giá trị: chỉ so khi tuyên bố ghi rõ kiểu khác `khong_neu` và khác `khang_dinh`; kiểu của tài liệu `khong_neu` thì lấy `kieu_gia_tri_mac_dinh` của thuộc tính (V37: "định mức" khác "Typical");
- mục tài liệu có `dieu_kien_khac`: phần điều kiện đã biết vẫn so như trên; cụm lạ xử lý ở luật chặn (mục 6, D1a).

## 6. Bước C và D: thứ tự D1b → D6

Theo đúng mã giả T5.5:

```
cung_dk = [u ∈ cung_tt | khop_dieu_kien(dk, u)];  khac_dk = cung_tt − cung_dk
Luật chặn điều kiện lạ: có u ∈ cung_dk mang dieu_kien_khac mà khop_gia_tri(tb, u) → D1a, chua_xac_dinh=dieu_kien_la:<cụm>
D1b: cung_dk có từ hai giá trị khác nhau (ngoài ngưỡng bằng nhau):
     tb khớp tất cả → ghi mau_thuan_khop_ca_hai=<g1>/<g2>, dò tiếp (QĐ13); ngược lại → CHUA_DU, tai_lieu_mau_thuan=true
D2:  tb.kieu = khang_dinh và có u ∈ cung_dk kiểu toi_da (kể cả mặc định toi_da) mà tb không thuận lợi hơn u → LECH, doi_kieu_gia_tri, khang_dinh=<từ>
D3:  có u ∈ cung_dk với khop_gia_tri(tb, u) → DUNG
D4:  có u ∈ khac_dk với bang(tb, u) → LECH, loai_bien_doi(dk, u)
D5:  cung_dk khác rỗng, hoặc tb thuận lợi hơn mọi giá trị của cung_bp → SAI
D6:  còn lại → CHUA_DU
```

- `khop_gia_tri`: `so_huong` ra `bang` hoặc `kem_hon` (số); `so_ip` ra `bang` hoặc `kem_hon` (mã IP); ISO 22810 như số; `"co"`/`"khong"` chỉ khớp chính nó.
- `bang`: bằng trong ngưỡng (`nguong_bang`, hiện 1%); mã IP bằng nhau; `"co"`/`"khong"` bằng nhau. Con số của điều kiện không bao giờ ở đây vì bộ thông số đã tách giá trị khỏi điều kiện (Bước 22).
- `cung_bp`: mục của `cung_tt` cùng bộ phận và phiên bản với điều kiện của tuyên bố (điều kiện khác thì bỏ qua). Với P−ĐK là toàn bộ `cung_tt`.
- D5 loại: `doi_gia_tri`; riêng khi tuyên bố nêu rõ bộ phận (hoặc phiên bản) mà `cung_bp` không có giá trị khẳng định nào (chỉ có `"khong"` hay không có gì) thì `doi_bo_phan` (`doi_phien_ban`), như V18.
- **Luật chung cho nhiều giá trị** (`dieu_kien_la.luat_chung_cho_nhieu_gia_tri`, mặc định tắt, chọn ở Bước 33): bật thì từ hai giá trị chỉ khác nhau ở cùng một điều kiện lạ coi như lựa chọn của người dùng, lấy giá trị kém thuận lợi nhất thay cho D1a.
- **P−ĐK** (`doi_chieu=False`): bỏ bước B; `cung_dk = cung_tt`, `khac_dk = ∅`; không có D1a (trừ trích xuất thất bại) và D1b; kiểm thử: "Galaxy Buds3 Pro nghe nhạc 7 giờ khi bật chống ồn" ra Đúng.

## 7. `loai_bien_doi(dk, u)` và chọn giá trị ở D4

Với mỗi điều kiện khác nhau giữa tuyên bố và `u`: nêu rõ (kể cả cụm phủ, chép nhãn) → `doi_dieu_kien`, `doi_bo_phan` (c là `bo_phan`), `doi_phien_ban` (c là `phien_ban`), `doi_kieu_gia_tri` (kiểu giá trị); lấy mặc định → `bo_dieu_kien`. Nhiều `u` bằng giá trị: chọn `u` khác ít điều kiện nhất; hòa thì ưu tiên khác ở điều kiện nêu rõ hơn mặc định, rồi bộ phận, phiên bản, kiểu giá trị, điều kiện còn lại (hướng dẫn mục 8, tạm chốt, chốt ở bước này). Lý do ghi đủ các điều kiện khác nhau.

Bằng chứng ở D3, D4, D5: mọi mục cùng giá trị ở cùng điều kiện mà nhãn dựa vào (hướng dẫn mục 8), sắp theo mã đoạn; `trich` nối bằng " | ", bỏ trùng.

## 8. Ghi chú

- `mac_dinh=<khóa,...>`: mọi khóa lấy mặc định ở B6 (giá trị cụ thể, `kem_thuan_loi_nhat`, `khong_mua_them`, và khóa `khong_co_mac_dinh` khi D1a), ở D1a–D6; không ghi ở D1 và khi trích xuất thất bại. Không ghi khóa `nhu_hang_cong_bo`, khóa không áp dụng, khóa nêu rõ, khóa chép nhãn.
- `chep_nhan=<nhãn>`, `khang_dinh=<từ>`, `chua_xac_dinh=<cụm>`, `mau_thuan_khop_ca_hai=<g1>/<g2>`.
- `ngoai_cau_hinh`, `ngoai_sau_loai`, `nham_vai`: hệ thống không tự ghi (cần người đọc); Bước 38 so với ghi chú của nhãn chuẩn.

## 9. Sinh lý do (T5.6)

`ly_do.py` ghép câu từ `vet` theo đúng tám mẫu câu của T5.6 (bảng trong hướng dẫn mục 8). Tên thuộc tính, điều kiện in bằng chữ tiếng Việt: thêm bảng `ten_hien_thi` (tên điều kiện, giá trị) đọc từ cụm `tu_tai_lieu` hoặc `hieu_biet_chung` đầu tiên của giá trị trong `cach_dien_dat`, và tên thuộc tính từ bảng mô tả của Bước 22. D3 có tuyên bố không ghi kiểu mà tài liệu ghi `toi_da`: thêm "(quảng cáo bỏ "lên đến")" (`chung.yaml ghi_chu_bo_len_den`). So thẳng: thêm "tài liệu không nêu điều kiện". Lý do luôn khớp nhãn vì sinh từ cùng dấu vết.

## 10. Kiểm thử

1. **Mỗi dòng ít nhất 3 ca** (khớp, không khớp, biên) cho D1, D1a (đủ ba lối vào và lối trích xuất thất bại), D1b (kể cả ngoại lệ QĐ13), D2 (kể cả mức sàn "hơn", tên tính năng không tính), D3, D4, D5, D6.
2. **Hồi quy toàn bộ ví dụ của hướng dẫn mục 9** (V01–V51): tệp `tests/du_lieu/vi_du_huong_dan.json`, mỗi ví dụ một bản ghi trích xuất **dựng tay** từ dòng "Bằng chứng" của ví dụ (chỉ các mục tài liệu cùng thuộc tính mà ví dụ nhắc, đúng câu trích của đoạn thật) cùng nhãn, dòng D, loại kỳ vọng. Test đọc lại hướng dẫn để chắc nhãn, dòng, loại trong tệp trùng tiêu đề ví dụ, và mọi câu trích là chuỗi con của `doan.jsonl`. Ví dụ mà P theo thiết kế ra khác nhãn chuẩn (V08 điều kiện lạ trước khi bổ sung cấu hình, V41, V51...) ghi rõ trong tệp: nhãn chuẩn, nhãn P dự kiến, lý do (giới hạn bao phủ); test kiểm nhãn P dự kiến.
3. **Ba trạng thái điều kiện** (T5.7): không áp dụng (phiên bản Watch SE 3), không nêu (mặc định), chưa xác định (D1a), và điều kiện chưa hỗ trợ (`dieu_kien_khac`) tách riêng.
4. **Luật chặn điều kiện lạ**: ba tình huống ở mục 4 của `luan_van/phan_tich_dieu_kien_ngoai_cau_hinh.md`; công tắc luật chung tắt và bật.
5. **QĐ15**: khớp đủ chữ, thiếu chữ điều kiện, số bằng, thấp hơn, cao hơn. **D4 không đổi điều kiện khi chỉ đổi con số** của tuyên bố (tính chất: với mọi ví dụ, đổi con số không đổi `dieu_kien_tuyen_bo` trong `vet`).
6. **P−ĐK**: Buds3 Pro 7 giờ khi bật chống ồn ra Đúng; không bao giờ ra D1a (trừ trích xuất thất bại), D1b, D4.
7. **Ngưỡng QĐ8 ở D4** (hướng dẫn mục 11.2): hàm đếm ca D4 mà tuyên bố nêu rõ hoạt động và giá trị trùng thuộc hoạt động khác, để Bước 27–28 đếm trên tập phát triển (không đổi ngưỡng 1/4 sau khi đếm).

## 11. Điểm 5, 6, 14 ở T10

Hướng dẫn bản 2 (người thực hiện duyệt ngày 01–02/11) đã trả lời cả ba; bộ quyết định cài đúng như vậy:

- Điểm 5: D2 áp khi tuyên bố khẳng định chắc chắn một mức không cao hơn mức "lên đến" ở cùng điều kiện.
- Điểm 6: kiểm "tài liệu mâu thuẫn" ở D1b, sau D1a, trước D2, có ngoại lệ QĐ13.
- Điểm 14: không xác định được điều kiện thì kết luận ngay Chưa đủ thông tin (D1a).

Ghi là "chốt theo hướng dẫn bản 2" khi Bước 27 xong; người thực hiện có thể đổi trước Bước 33.
