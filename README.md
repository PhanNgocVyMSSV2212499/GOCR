# Nhận diện ký tự quang học GOCR

## 1. Tổng quan về GOCR
- **GOCR** là một phần mềm **OCR mã nguồn mở**, viết bằng ngôn ngữ **C**.
- Ra đời từ khoảng năm 2000, phát triển chủ yếu cho hệ thống Linux, nhưng có thể chạy trên Windows, macOS thông qua bản biên dịch.
- **Nguyên lý hoạt động**:
  1. Tiền xử lý ảnh: chuyển về đen–trắng, loại bỏ nhiễu.
  2. Phân đoạn ký tự: tách ảnh thành từng ký tự riêng.
  3. So khớp mẫu (**Pattern Matching**): so sánh hình dạng ký tự với bộ mẫu ký tự có sẵn trong chương trình.
  4. Xuất kết quả thành chuỗi văn bản.

## 2. Hành trình thực hiện
1. **Chuẩn bị dữ liệu**  
   - Sử dụng 5 ảnh bìa sách tiếng Việt (jpg/png) đặt trong thư mục `MauBiaSach`.
2. **Cài đặt môi trường Docker**  
   - Dùng `python:3.10-slim`, cài GOCR và OpenCV.
   - Mount thư mục ảnh từ Windows vào `/data` trong container.
3. **Xây dựng script Python**  
   - Tiền xử lý ảnh bằng OpenCV (grayscale + threshold).
   - Gọi GOCR qua `subprocess` để OCR từng ảnh.
   - Lưu kết quả OCR từng ảnh + gộp vào file `all_books.txt`.
4. **Chạy thử & kết quả**  
   - GOCR xuất ra file `all_books.txt` chứa nhiều ký tự sai, loạn, dấu tiếng Việt bị mất hoặc thay bằng ký tự khác.

## 3. Nguyên nhân kết quả không chính xác
- **Hạn chế do thiết kế và ngôn ngữ C**  
  - GOCR dùng so khớp mẫu ký tự tĩnh, không có khả năng học từ dữ liệu mới.
  - Không thích nghi với font chữ lạ hoặc ảnh nền phức tạp.
- **Không nhận diện tốt tiếng Việt**  
  - Bộ mẫu ký tự không chứa chữ tiếng Việt có dấu (`ă, â, ê, ô, ơ, ư, đ`).
  - Dấu bị bỏ hoặc nhận sai thành ký tự khác.
- **Mỗi bìa mỗi kiểu chữ**  
  - Font chữ khác nhau, có hiệu ứng đồ họa, nghiêng, uốn cong → GOCR khó khớp mẫu.
- **Nền ảnh phức tạp**  
  - Bìa sách nhiều màu, hoa văn → làm thuật toán segmentation và matching bị sai.

## 4. So sánh GOCR với Keras OCR và Tesseract

| Tiêu chí            | GOCR (Pattern Matching)             | Tesseract OCR (LSTM)            | Keras OCR (Deep Learning)         |
|---------------------|--------------------------------------|----------------------------------|------------------------------------|
| **Ngôn ngữ**        | Ít (không hỗ trợ tiếng Việt mặc định) | >100 ngôn ngữ, có tiếng Việt     | Tùy huấn luyện, hỗ trợ tiếng Việt |
| **Công nghệ**       | So khớp mẫu ký tự (C)                 | Machine Learning (LSTM)         | CNN + RNN (CRNN) + EAST detector  |
| **Độ chính xác**    | Thấp với ảnh phức tạp                 | Cao với ảnh rõ, hỗ trợ tiếng Việt | Rất cao, đặc biệt với ảnh phức tạp |
| **Tốc độ**          | Rất nhanh, nhẹ                       | Trung bình                      | Chậm hơn, cần GPU để nhanh        |
| **Khả năng học**    | Không học được mẫu mới                | Có thể train thêm               | Dễ train lại trên dữ liệu mới     |
| **Kích thước**      | Rất nhỏ (~1MB)                       | Trung bình (~50–100MB)          | Lớn (>100MB)                      |
| **Phù hợp**         | Ảnh chữ đen trên nền trắng, font chuẩn| OCR tài liệu, in rõ ràng        | OCR ảnh đời thường, biển hiệu, bìa sách |

## 5. Kết luận
- **GOCR** phù hợp cho các trường hợp đơn giản: chữ in rõ, không dấu, nền đơn giản.
- Với **bìa sách tiếng Việt**, GOCR cho kết quả rất kém do:
  1. **Thuật toán pattern matching** hạn chế.
  2. **Không hỗ trợ tiếng Việt** mặc định.
  3. **Font chữ và nền ảnh phức tạp**.
- Nếu muốn OCR bìa sách tiếng Việt, **Tesseract OCR** hoặc **Keras OCR** là lựa chọn tốt hơn:
  - **Tesseract**: Dễ dùng, miễn phí, hỗ trợ tiếng Việt, chính xác cao với ảnh scan.
  - **Keras OCR**: Nhận tốt ảnh đời thực, hỗ trợ tuỳ biến, nhưng nặng và chậm hơn.
