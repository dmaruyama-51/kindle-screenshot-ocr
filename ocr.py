import argparse
import io
import logging
import os

from google.cloud import vision

logger = logging.getLogger(__name__)


def detect_text(image_path: str) -> str:
    """Google Cloud Vision APIを使用して画像からテキストを検出"""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # 最初の要素が画像全体のテキスト
        return texts[0].description

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return ""


def create_output_path(input_folder: str) -> str:
    """入力フォルダのパスから出力ファイルのパスを生成する"""
    # input_files/book_title/chapter# から output_files/book_title/book_title__chapter#.txt を生成
    parts = input_folder.split(os.sep)
    if len(parts) >= 3 and parts[0] == "input_files":
        book_title = parts[1]
        chapter = parts[2]

        # output_files/book_titleディレクトリが存在しない場合は作成
        output_dir = os.path.join("output_files", book_title)
        os.makedirs(output_dir, exist_ok=True)

        # 出力ファイル名を生成
        output_filename = f"{book_title}__{chapter}.txt"
        return os.path.join(output_dir, output_filename)
    else:
        raise ValueError(
            "入力フォルダは 'input_files/book_title/chapter#' の形式である必要があります"
        )


def postprocess_text(text: str) -> str:
    """OCRで検出されたテキストの改行と余分な空白を処理"""
    # 行を分割して処理
    lines = text.split("\n")
    # 空行を削除し、各行の余分な空白を完全に削除して結合
    processed_lines = ["".join(line.split()) for line in lines if line.strip()]
    return "".join(processed_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Google Cloud Vision APIを使用して画像からテキストを抽出します"
    )
    parser.add_argument(
        "--input_folder", required=True, help="画像が保存されているフォルダのパス"
    )
    parser.add_argument(
        "--output_file",
        required=False,
        help="テキストを保存するファイルのパス（省略可能）",
    )
    args = parser.parse_args()

    # output_fileが指定されていない場合は自動生成
    output_file = args.output_file or create_output_path(args.input_folder)

    with open(output_file, "w", encoding="utf-8") as f:
        for filename in sorted(os.listdir(args.input_folder)):
            logger.info("filename: %s", filename)
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(args.input_folder, filename)
                logger.info("処理中: %s", filename)

                try:
                    text = detect_text(image_path)
                    processed_text = postprocess_text(text)
                    # テキストを保存（改行なしで連結）
                    f.write(processed_text)

                    logger.info("成功: %s", filename)
                except Exception as e:
                    logger.error("エラー (%s): %s", filename, str(e))


if __name__ == "__main__":
    main()
