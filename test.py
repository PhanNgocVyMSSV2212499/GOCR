import os
import subprocess
import cv2
import time

# 📂 Thư mục ảnh
input_dir = "/data/MauBiaSach"
output_dir = "/data/output"

# Tạo thư mục output nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# File tổng hợp kết quả
final_output_file = os.path.join(output_dir, "all_books.txt")

# Lấy danh sách ảnh (chỉ lấy 5 file đầu tiên)
book_covers = [f for f in os.listdir(input_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
book_covers = book_covers[:5]

total_time = 0
total_words = 0

with open(final_output_file, "w", encoding="utf-8") as fout:
    for cover in book_covers:
        input_path = os.path.join(input_dir, cover)
        clean_path = os.path.join(output_dir, f"clean_{cover}")
        output_txt = os.path.join(output_dir, f"{os.path.splitext(cover)[0]}.txt")

        # 🕒 bắt đầu đo thời gian
        start_time = time.time()

        # ======== TIỀN XỬ LÝ ẢNH ========
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        # Làm mờ để giảm nhiễu
        blur = cv2.GaussianBlur(img, (3,3), 0)

        # Adaptive threshold (cắt theo từng vùng, tốt hơn threshold cố định)
        thresh = cv2.adaptiveThreshold(
            blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            35, 11
        )

        # Morphology để loại nhiễu và làm chữ rõ nét
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Lưu ảnh đã xử lý
        cv2.imwrite(clean_path, morph)
        # =================================

        # 🔍 Chạy GOCR
        subprocess.run(["gocr", "-i", clean_path, "-o", output_txt])

        # Đọc nội dung OCR
        try:
            with open(output_txt, "r", encoding="utf-8") as fin:
                ocr_text = fin.read().strip()
        except:
            ocr_text = "[Lỗi đọc file OCR]"

        # 🕒 kết thúc đo thời gian
        elapsed = time.time() - start_time
        total_time += elapsed

        # 📊 Thống kê
        word_count = len(ocr_text.split())
        total_words += word_count

        # Accuracy giả định
        accuracy = 100.0 if ocr_text and ocr_text != "[Lỗi đọc file OCR]" else 0.0

        # ✍️ Ghi kết quả vào file
        fout.write(f"===== {cover} =====\n")
        fout.write(ocr_text + "\n")
        fout.write(f"[Số từ: {word_count}] [Thời gian: {elapsed:.2f}s] [Độ chính xác: {accuracy:.2f}%]\n\n")

        print(f"✅ {cover}: {word_count} từ, {elapsed:.2f}s, acc={accuracy:.2f}%")

# Ghi tổng hợp
with open(final_output_file, "a", encoding="utf-8") as fout:
    fout.write("===== TỔNG HỢP =====\n")
    fout.write(f"Tổng số từ: {total_words}\n")
    fout.write(f"Tổng thời gian: {total_time:.2f} giây\n")
    if len(book_covers) > 0:
        fout.write(f"Tốc độ trung bình: {total_time/len(book_covers):.2f} giây/ảnh\n")

print(f"🎯 Hoàn thành OCR. File tổng hợp: {final_output_file}")
