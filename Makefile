.PHONY: lint format ocr help

# ================================
# ユーザー向け
# ================================
help:
	@echo "使用可能なコマンド:"
	@echo "  make ocr BOOK=<book_title> CHAPTER=<chapter_number> - 指定した本の章のOCR処理を実行"
	@echo "例:"
	@echo "  make ocr BOOK=sample_book CHAPTER=1"

ocr:
ifndef BOOK
	$(error BOOKが指定されていません。使用例: make ocr BOOK=sample_book CHAPTER=1)
endif
ifndef CHAPTER
	$(error CHAPTERが指定されていません。使用例: make ocr BOOK=sample_book CHAPTER=1)
endif
	@echo "OCR処理を開始: $(BOOK) Chapter $(CHAPTER)"
	poetry run --no-ansi --no-interaction python ocr.py --input_folder=input_files/$(BOOK)/chapter$(CHAPTER)
	@echo "OCR処理が完了しました。出力: output_files/$(BOOK)_chapter$(CHAPTER).txt"

# ================================
# 開発
# ================================
format:
	poetry run ruff format .

lint:
	poetry run ruff check . --fix

all: format lint 