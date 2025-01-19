# Kindle Screenshot OCR

## Overview

KindleのスクリーンショットをGoogle Cloud Vision APIを使用してOCRし, Chapterごとにテキストファイルに出力するツールです。
テキストファイルを NotebookLM に読み込むことで, Kindle本のRAGを作れます。

## Usage

### 1. Setup

依存ライブラリのインストール
```bash
poetry install
```

gcloudの認証
```bash
gcloud auth login
```

### 2. 書籍のスクリーンショットを配置

kindle本のChapterごとにスクリーンショットを取り、以下の階層に配置してください。
screenshotのファイル名は任意ですが、並び順通りにOCRをしてテキストが結合されるため、ページ順に並ぶようにしてください。

```
input_files/
└── {{ your_book_title }}/
    ├── chapter{{ chapter_number }}/
    │   ├── screenshot1.png
    │   ├── screenshot2.png
    │   └── ...
    ├── chapter{{ chapter_number }}/
    │   ├── screenshot1.png
    │   ├── screenshot2.png
    │   └── ...
    └── ...
```

### 3. OCR処理を実行
次のコマンドでOCRを実行します。`BOOK`には書籍タイトル（2.で配置した`{{ your_book_title }}`ディレクトリに対応）,`CHAPTER`にはChapter番号（`{{ chapter_number }}`に対応）を指定してください。
現状、Chapter事に実行する必要があります。（ToDo: 複数ChapterをまとめてOCRできるようにする）

```bash
 make ocr BOOK={{ your_book_title }} CHAPTER={{ hapter_number }} 

 # example: sample_bookの1章目をOCR
 make ocr BOOK=sample_book CHAPTER=1
```

結果は次の場所に出力されます。
```
output_files/
└── {{ your_book_title }}/
    └── {{ your_book_title }}__chapter{{ chapter }}.txt
```

