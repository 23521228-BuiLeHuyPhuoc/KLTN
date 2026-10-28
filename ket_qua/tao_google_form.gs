// Tạo Google Form cho khảo sát Bước 10. Sinh tự động từ mục 4 của ket_qua/khao_sat_cach_hieu.md,
// đừng sửa tay: sửa phiếu trong tệp .md rồi sinh lại.
// Cách dùng: script.google.com > dán toàn bộ tệp này > Lưu > chọn hàm > Chạy.
//   taoPhieu: tạo form mới.
//   capNhatPhieu: ghi đè câu hỏi của form đã tạo (FORM_ID), giữ nguyên đường dẫn và tên form;
//   dừng nếu form đã có câu trả lời.
// Đường dẫn để sửa và để gửi form hiện trong Nhật ký thực thi.

var FORM_ID = "1cbbwG710d5oH6j6qZgKqUhCl7Ab2l2MUa9T6GPejOYk";
var TIEU_DE = "Bạn hiểu quảng cáo điện thoại, tai nghe, đồng hồ như thế nào?";
var MO_TA = "Phiếu này phục vụ khóa luận tốt nghiệp về quảng cáo thiết bị điện tử. Bạn sẽ đọc 10 đoạn trích ngắn từ quảng cáo, mỗi đoạn có 1 đến 3 câu hỏi. Hãy chọn theo cảm nhận đầu tiên khi đọc, không cần tra cứu. Không có đáp án đúng hay sai. Nếu không phương án nào giống ý bạn, hãy ghi vào ô \"Khác\". Phiếu ẩn danh, không thu tên hay email, mất khoảng 6 phút. Phiếu dành cho người từ 18 tuổi.";
var MUC = [
  {loai: 'khung', tieuDe: "Đoạn 1: điện thoại iPhone 17", moTa: "\"Luôn sẵn sàng cho mọi hành trình với thời lượng pin ấn tượng, lên đến 30 giờ.\""},
  {loai: 'cau', tieuDe: "Câu 1. Theo bạn, 30 giờ pin này là khi dùng điện thoại vào việc gì?", luaChon: ["Xem video đã tải sẵn trong máy", "Xem video trực tuyến (YouTube, Netflix...)", "Chơi game, dùng nặng", "Dùng hằng ngày, nhiều việc lẫn lộn (nhắn tin, lướt web, gọi điện...)", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 2: tai nghe Galaxy Buds3 Pro", moTa: "\"Tận hưởng thời gian sử dụng vượt trội: lên đến 6 giờ.\"\nThông tin thêm: tai nghe này có tính năng chống ồn (tự lọc bớt tiếng ồn xung quanh, gọi tắt là ANC), người dùng tự bật hoặc tắt. Tai nghe đi kèm một hộp sạc: cất tai nghe vào hộp thì tai nghe được sạc lại."},
  {loai: 'cau', tieuDe: "Câu 2. Theo bạn, 6 giờ này là khi dùng tai nghe vào việc gì?", luaChon: ["Nghe nhạc, xem phim", "Gọi điện", "Dùng lẫn lộn, lúc nghe nhạc lúc gọi điện", "Không biết / không chắc"], khac: true},
  {loai: 'cau', tieuDe: "Câu 3. Theo bạn, trong 6 giờ đó tính năng chống ồn đang bật hay tắt?", luaChon: ["Bật suốt", "Tắt suốt", "Lúc bật lúc tắt", "Không biết / không chắc"], khac: true},
  {loai: 'cau', tieuDe: "Câu 4. Theo bạn, 6 giờ này được tính thế nào?", luaChon: ["Chỉ tính tai nghe: sạc đầy tai nghe một lần, nghe liên tục được 6 giờ", "Tính cả hộp sạc: hết pin thì cất tai nghe vào hộp sạc lại rồi nghe tiếp, cộng lại được 6 giờ", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 3: đồng hồ Apple Watch SE 3", moTa: "\"Tận hưởng trải nghiệm liền mạch với thời lượng pin ấn tượng: 18 giờ.\"\nThông tin thêm: đồng hồ này có chế độ tiết kiệm pin (tắt bớt một số tính năng để pin dùng lâu hơn), người dùng tự bật hoặc tắt."},
  {loai: 'cau', tieuDe: "Câu 5. Theo bạn, 18 giờ này là khi dùng đồng hồ thế nào?", luaChon: ["Dùng bình thường hằng ngày: xem giờ, nhận thông báo, đo nhịp tim", "Dùng bình thường, có lúc tập thể dục một chút", "Tập thể thao liên tục suốt 18 giờ (ví dụ chạy bộ có bật định vị GPS)", "Không biết / không chắc"], khac: true},
  {loai: 'cau', tieuDe: "Câu 6. Theo bạn, trong 18 giờ đó đồng hồ đang ở chế độ nào?", luaChon: ["Chế độ bình thường, đủ tính năng", "Chế độ tiết kiệm pin", "Lúc bình thường, lúc tiết kiệm pin", "Không biết / không chắc"], khac: true},
  {loai: 'cau', tieuDe: "Câu 7. Theo bạn, con số 18 giờ nghĩa là gì?", luaChon: ["Dùng thường xuyên sẽ được khoảng 18 giờ", "18 giờ là mức tốt nhất, dùng thực tế thường ít hơn", "Chắc chắn dùng được ít nhất 18 giờ, có khi còn hơn", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 4: điện thoại iPhone 17", moTa: "\"Luôn sẵn sàng cho mọi hành trình với thời lượng pin ấn tượng, xem video lên đến 30 giờ và khả năng sạc nhanh 50% chỉ trong 20 phút.\""},
  {loai: 'cau', tieuDe: "Câu 8. Theo bạn, cần gì để sạc được 50% pin trong 20 phút?", luaChon: ["Dùng đồ đi kèm khi mua máy là đủ, không phải mua thêm gì", "Dùng củ sạc nào cũng được, kể cả củ sạc cũ ở nhà", "Phải có củ sạc loại mạnh (công suất cao), thường phải mua riêng", "Không biết / không chắc"], khac: true},
  {loai: 'cau', tieuDe: "Câu 9. Theo bạn, \"xem video\" ở đây là xem thế nào?", luaChon: ["Xem video đã tải sẵn trong máy", "Xem video trực tuyến (YouTube, Netflix...)", "Cả hai, không phân biệt", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 5: điện thoại iPhone 17", moTa: "\"Với độ sáng 3000 nit, mọi nội dung từ phim ảnh đến ảnh chụp đều rực rỡ và sắc nét.\"\nThông tin thêm: nit là đơn vị đo độ sáng màn hình, số càng lớn màn hình càng sáng."},
  {loai: 'cau', tieuDe: "Câu 10. Theo bạn, màn hình sáng được 3000 nit khi nào?", luaChon: ["Khi dùng bình thường, lúc nào cũng sáng được như vậy", "Khi ra ngoài trời nắng (máy tự tăng độ sáng)", "Khi xem phim hoặc ảnh loại HDR (loại hình ảnh có vùng sáng rất sáng)", "Đây là mức sáng nhất máy có thể đạt, không rõ lúc nào", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 6: đồng hồ Apple Watch SE 3", moTa: "\"Tận hưởng trải nghiệm liền mạch với thời lượng pin ấn tượng: kéo dài tới 32 giờ.\"\nThông tin thêm: đồng hồ này có chế độ tiết kiệm pin (tắt bớt một số tính năng để pin dùng lâu hơn), người dùng tự bật hoặc tắt."},
  {loai: 'cau', tieuDe: "Câu 11. Theo bạn, trong 32 giờ đó đồng hồ đang ở chế độ nào?", luaChon: ["Chế độ bình thường, đủ tính năng", "Chế độ tiết kiệm pin", "Lúc bình thường, lúc tiết kiệm pin", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 7: điện thoại iPhone 17", moTa: "\"Ghi lại mọi khoảnh khắc đáng giá với hệ thống camera đa năng, cho phép bạn thu phóng lên đến 10x, đảm bảo mọi chi tiết đều được nắm bắt hoàn hảo.\"\nThông tin thêm: thu phóng (zoom) là phóng to cảnh ở xa khi chụp ảnh."},
  {loai: 'cau', tieuDe: "Câu 12. Theo bạn, thu phóng 10x ở đây là gì?", luaChon: ["Phóng to 10 lần bằng ống kính, ảnh vẫn nét như chụp thường", "Phóng to 10 lần bằng phần mềm, ảnh có thể mờ hoặc vỡ hạt", "Kết hợp: một phần bằng ống kính, phần còn lại bằng phần mềm", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 8: tai nghe Galaxy Buds3 Pro", moTa: "\"Các cuộc trò chuyện cũng trở nên rõ ràng hơn bao giờ hết với thời lượng đàm thoại lên đến 5 giờ.\"\nThông tin thêm: tai nghe này có tính năng chống ồn (tự lọc bớt tiếng ồn xung quanh, gọi tắt là ANC), người dùng tự bật hoặc tắt."},
  {loai: 'cau', tieuDe: "Câu 13. Theo bạn, trong 5 giờ gọi điện đó tính năng chống ồn đang bật hay tắt?", luaChon: ["Bật suốt", "Tắt suốt", "Lúc bật lúc tắt", "Không biết / không chắc"], khac: true},
  {loai: 'khung', tieuDe: "Đoạn 9: đồng hồ Apple Watch SE 3", moTa: "\"Khả năng sạc nhanh vượt trội giúp bạn quay lại hoạt động chỉ trong tích tắc, với 80% pin chỉ trong khoảng 45 phút, hoặc 15 phút sạc cho 8 giờ sử dụng.\""},
  {loai: 'cau', tieuDe: "Câu 14. Theo bạn, cần gì để sạc được 80% pin trong khoảng 45 phút?", luaChon: ["Dùng đồ đi kèm khi mua đồng hồ là đủ, không phải mua thêm gì", "Dùng củ sạc nào cũng được, kể cả củ sạc cũ ở nhà", "Phải có củ sạc loại mạnh (công suất cao), thường phải mua riêng", "Không biết / không chắc"], khac: true},
  {loai: 'trang', tieuDe: "Phần 2"},
  {loai: 'khung', tieuDe: "Đoạn 10: đồng hồ Apple Watch SE 3", moTa: "\"Tận hưởng trải nghiệm liền mạch với thời lượng pin ấn tượng: lên đến 18 giờ.\""},
  {loai: 'cau', tieuDe: "Câu 15. Theo bạn, con số 18 giờ nghĩa là gì?", luaChon: ["Dùng thường xuyên sẽ được khoảng 18 giờ", "18 giờ là mức tốt nhất, dùng thực tế thường ít hơn", "Chắc chắn dùng được ít nhất 18 giờ, có khi còn hơn", "Không biết / không chắc"], khac: true},
  {loai: 'trang', tieuDe: "Về bạn"},
  {loai: 'cau', tieuDe: "Câu 16. Bạn bao nhiêu tuổi?", luaChon: ["18–24", "25–34", "35–49", "Từ 50 trở lên"], khac: false},
  {loai: 'cau', tieuDe: "Câu 17. Bạn có học hoặc làm trong ngành công nghệ thông tin không?", luaChon: ["Có", "Không"], khac: false},
  {loai: 'cau', tieuDe: "Câu 18. Trong 2 năm qua, bạn có mua điện thoại, tai nghe không dây hoặc đồng hồ thông minh không?", luaChon: ["Có", "Không"], khac: false}
];

function taoPhieu() {
  dungPhieu(FormApp.create(TIEU_DE));
}

function capNhatPhieu() {
  var form = FormApp.openById(FORM_ID);
  if (form.getResponses().length > 0) {
    throw new Error('Form đã có ' + form.getResponses().length + ' câu trả lời, không ghi đè. Dùng taoPhieu để tạo form mới.');
  }
  form.getItems().forEach(function (muc) {
    form.deleteItem(muc);
  });
  dungPhieu(form);  // giữ nguyên tên form người thực hiện đã đặt
}

function dungPhieu(form) {
  form.setDescription(MO_TA);
  form.setCollectEmail(false);
  form.setShuffleQuestions(false);
  form.setProgressBar(true);
  form.setAllowResponseEdits(false);
  form.setConfirmationMessage('Cảm ơn bạn đã dành thời gian trả lời!');

  MUC.forEach(function (m) {
    if (m.loai === 'trang') {
      form.addPageBreakItem().setTitle(m.tieuDe);
    } else if (m.loai === 'khung') {
      form.addSectionHeaderItem().setTitle(m.tieuDe).setHelpText(m.moTa);
    } else {
      var cau = form.addMultipleChoiceItem()
        .setTitle(m.tieuDe)
        .setChoiceValues(m.luaChon)
        .setRequired(true);
      if (m.khac) {
        cau.showOtherOption(true);
      }
    }
  });

  Logger.log('Số câu: ' + form.getItems(FormApp.ItemType.MULTIPLE_CHOICE).length);
  Logger.log('Đường dẫn để SỬA form: ' + form.getEditUrl());
  Logger.log('Đường dẫn để GỬI cho người trả lời: ' + form.getPublishedUrl());
}
