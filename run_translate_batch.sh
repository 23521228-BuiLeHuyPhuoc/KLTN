#!/bin/bash

VENV="/home/phuocblh/.gemini/antigravity-ide/brain/60ad82b3-6386-48cb-bc66-8653fc854671/scratch/venv312"
PDF2ZH="$VENV/bin/pdf2zh_next"
INPUT_DIR="/home/phuocblh/KLTN/KLTN/báo"
OUTPUT_DIR="/home/phuocblh/KLTN/KLTN/dịch"
MIRROR_DIR="/home/phuocblh/KLTN/dịch"
LOG_FILE="/home/phuocblh/KLTN/KLTN/translate_batch.log"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$MIRROR_DIR"

echo "==================================================" | tee -a "$LOG_FILE"
echo "=== TIẾP TỤC DỊCH CÁC BÀI BÁO (RESUME): $(date) ===" | tee -a "$LOG_FILE"

FILES=()
for i in $(seq 1 16); do
    FILES+=("$INPUT_DIR/[$i].pdf")
done

# Thêm bài trong thư mục con nếu có
if [ -f "$INPUT_DIR/báo con1/2003.00744v3.pdf" ]; then
    FILES+=("$INPUT_DIR/báo con1/2003.00744v3.pdf")
fi

TOTAL=${#FILES[@]}
CURRENT=0
SUCCESS_COUNT=0
FAIL_COUNT=0

for file in "${FILES[@]}"; do
    CURRENT=$((CURRENT + 1))
    fname=$(basename "$file")
    
    if [ ! -f "$file" ]; then
        echo "Lỗi: Không tìm thấy file $file! Bỏ qua..." | tee -a "$LOG_FILE"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi

    # Kiểm tra nếu file đã dịch xong cả mono và dual thì bỏ qua
    mono_pdf="$OUTPUT_DIR/${fname%.pdf}.no_watermark.vi.mono.pdf"
    dual_pdf="$OUTPUT_DIR/${fname%.pdf}.no_watermark.vi.dual.pdf"
    if [ -f "$mono_pdf" ] && [ -f "$dual_pdf" ]; then
        echo ">> [$(date +'%Y-%m-%d %H:%M:%S')] [$CURRENT/$TOTAL] $fname đã có bản dịch hoàn tất từ trước, bỏ qua." | tee -a "$LOG_FILE"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        continue
    fi

    echo "==================================================" | tee -a "$LOG_FILE"
    echo ">> [$(date +'%Y-%m-%d %H:%M:%S')] [$CURRENT/$TOTAL] Bắt đầu dịch: $fname" | tee -a "$LOG_FILE"

    "$PDF2ZH" "$file" \
        --bing \
        --lang-in en \
        --lang-out vi \
        --watermark-output-mode no_watermark \
        --no-auto-extract-glossary \
        --output "$OUTPUT_DIR" 2>&1 | tee -a "$LOG_FILE"

    STATUS=$?
    if [ $STATUS -eq 0 ]; then
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo ">> [$(date +'%Y-%m-%d %H:%M:%S')] [$CURRENT/$TOTAL] Thành công: $fname" | tee -a "$LOG_FILE"
        # Đồng bộ sang thư mục dịch ở ngoài
        cp -u "$OUTPUT_DIR"/* "$MIRROR_DIR"/ 2>/dev/null || true
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo ">> [$(date +'%Y-%m-%d %H:%M:%S')] [$CURRENT/$TOTAL] Thất bại: $fname (Mã lỗi: $STATUS)" | tee -a "$LOG_FILE"
    fi
done

echo "==================================================" | tee -a "$LOG_FILE"
echo "=== TỔNG KẾT: Hoàn thành $SUCCESS_COUNT/$TOTAL file, Thất bại $FAIL_COUNT file: $(date) ===" | tee -a "$LOG_FILE"
