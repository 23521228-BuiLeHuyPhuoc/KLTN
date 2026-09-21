#!/bin/bash
set -e

VENV="/home/phuocblh/.gemini/antigravity-ide/brain/60ad82b3-6386-48cb-bc66-8653fc854671/scratch/venv312"
PDF2ZH="$VENV/bin/pdf2zh_next"
INPUT_DIR="/home/phuocblh/KLTN/báo"
OUTPUT_DIR="/home/phuocblh/KLTN/dịch"
LOG_FILE="/home/phuocblh/KLTN/translate_batch.log"

echo "=== Batch Translation (BING - FAST NO API KEY) Started: $(date) ===" | tee -a "$LOG_FILE"

for num in 2 3 4 5 6; do
    file="$INPUT_DIR/[$num].pdf"
    echo "----------------------------------------" | tee -a "$LOG_FILE"
    echo ">> [$(date +'%Y-%m-%d %H:%M:%S')] Starting [$num].pdf with Bing..." | tee -a "$LOG_FILE"
    
    if [ ! -f "$file" ]; then
        echo "Error: File $file not found!" | tee -a "$LOG_FILE"
        continue
    fi

    "$PDF2ZH" "$file" \
        --bing \
        --lang-in en \
        --lang-out vi \
        --watermark-output-mode no_watermark \
        --no-auto-extract-glossary \
        --output "$OUTPUT_DIR" 2>&1 | tee -a "$LOG_FILE"

    echo ">> [$(date +'%Y-%m-%d %H:%M:%S')] Finished [$num].pdf successfully" | tee -a "$LOG_FILE"
done

echo "=== All files [2] to [6] completed: $(date) ===" | tee -a "$LOG_FILE"
