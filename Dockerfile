# Dịch vụ kiểm chứng (Bước 34). Chạy: docker run -p 8000:8000 --env-file <tệp biến môi trường> kiemchung
# Khóa API (GEMINI_API_KEY, GROQ_API_KEY) truyền lúc chạy qua --env-file hoặc -e; image không chứa .env, data/nhan/ hay ket_qua/.
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 PYTHONUTF8=1 PYTHONPATH=/app/src
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/nguon/ data/nguon/
COPY data/cau_hinh/ data/cau_hinh/
COPY data/mau_san_pham.csv data/mau_san_pham.csv
COPY data/huong_dan_gan_nhan.md data/huong_dan_gan_nhan.md

# Bộ nhớ đệm LLM của API ghi ở ket_qua/llm_cache_api (đổi bằng KIEMCHUNG_CACHE_DIR); gắn volume nếu cần giữ lại.
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "kiemchung.api:app", "--host", "0.0.0.0", "--port", "8000"]
