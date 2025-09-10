import os
import subprocess
import cv2

# 📂 Thư mục ảnh trong container
input_dir = "/data/MauBiaSach"
output_dir = "/data/output"

# Tạo thư mục output nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# File tổng hợp kết quả
final_output_file = os.path.join(output_dir, "all_books.txt")

# Lấy danh sách ảnh (chỉ lấy 5 file đầu tiên)
book_covers = [f for f in os.listdir(input_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
book_covers = book_covers[:5]

with open(final_output_file, "w", encoding="utf-8") as fout:
    for cover in book_covers:
        input_path = os.path.join(input_dir, cover)
        clean_path = os.path.join(output_dir, f"clean_{cover}")
        output_txt = os.path.join(output_dir, f"{os.path.splitext(cover)[0]}.txt")

        # 🖼 Tiền xử lý ảnh (grayscale + threshold)
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        cv2.imwrite(clean_path, thresh)

        # 🔍 Chạy GOCR
        subprocess.run(["gocr", "-i", clean_path, "-o", output_txt])

        # Đọc nội dung OCR và ghi vào file tổng hợp
        fout.write(f"===== {cover} =====\n")
        try:
            with open(output_txt, "r", encoding="utf-8") as fin:
                fout.write(fin.read().strip() + "\n\n")
        except:
            fout.write("[Lỗi đọc file OCR]\n\n")

        print(f"✅ Đã OCR: {cover} → {output_txt}")

print(f"🎯 Hoàn thành OCR. File tổng hợp: {final_output_file}")