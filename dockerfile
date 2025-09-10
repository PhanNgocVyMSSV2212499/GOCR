FROM python:3.10-slim

# Cài GOCR + libglib2.0 (fix lỗi libgthread) + libgl1 (fix lỗi GUI OpenCV)
RUN apt-get update && apt-get install -y \
    gocr \
    libglib2.0-0 \
    libgl1 \
    && apt-get clean

# Cài OpenCV cho Python
RUN pip install opencv-python

# Thư mục làm việc
WORKDIR /app

# Copy file Python vào container
COPY test.py /app/test.py

# Chạy script khi container khởi động
CMD ["python", "test.py"]