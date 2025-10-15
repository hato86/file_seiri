import os
import shutil
import time
from datetime import datetime

# --- ユーザー設定エリア ---

# 1. 整理したいフォルダのパス (WSL用のパス)
WATCH_FOLDER = "/mnt/c/Users/hayat/Downloads"

# 2. 整理後のファイルを保存する基本フォルダのパス (WSL用のパス)
DESTINATION_BASE_FOLDER = "/mnt/c/Users/hayat/Documents/整理済みファイル"

# 3. キーワードによる仕分けルール
KEYWORD_RULES = {
    "請求書": "01_請求書",
    "見積書": "02_見積書",
    "議事録": "03_会議資料",
    "receipt": "04_領収書"
}

# 4. 拡張子による仕分けルール
EXTENSION_RULES = {
    # 画像
    ".jpg": "画像", ".jpeg": "画像", ".png": "画像", ".gif": "画像", ".bmp": "画像",
    # 書類
    ".pdf": "書類", ".docx": "書類", ".xlsx": "書類", ".pptx": "書類", ".txt": "書類",
    # 圧縮ファイル
    ".zip": "圧縮ファイル", ".rar": "圧縮ファイル",
    # 実行ファイル
    ".exe": "インストーラー", ".msi": "インストーラー"
}

# 5. お掃除機能の設定
ARCHIVE_DAYS = 30
ARCHIVE_FOLDER_NAME = "長期保管（アーカイブ）"

# --- 設定はここまで ---


def organize_files():
    """WATCH_FOLDER内のファイルをルールに従って整理する関数"""
    print("ファイル整理を開始します...")
    script_name = os.path.basename(__file__)

    for filename in os.listdir(WATCH_FOLDER):
        if filename == script_name:
            continue
        source_path = os.path.join(WATCH_FOLDER, filename)
        if not os.path.isfile(source_path):
            continue

        # ファイルの最終更新日時から年月フォルダを決定
        last_modified_time = datetime.fromtimestamp(os.path.getmtime(source_path))
        year_str = f"{last_modified_time.year}年"
        month_str = f"{last_modified_time.month}月"

        moved = False
        # キーワードルールをチェック
        for keyword, folder_name in KEYWORD_RULES.items():
            if keyword in filename:
                dest_folder = os.path.join(DESTINATION_BASE_FOLDER, year_str, month_str, folder_name)
                move_file(source_path, dest_folder, filename)
                moved = True
                break
        if moved:
            continue

        # 拡張子ルールをチェック
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension in EXTENSION_RULES:
            folder_name = EXTENSION_RULES[file_extension]
            dest_folder = os.path.join(DESTINATION_BASE_FOLDER, year_str, month_str, folder_name)
            move_file(source_path, dest_folder, filename)
            continue

    print("今回のファイル整理が完了しました。")


def archive_old_files():
    """WATCH_FOLDER内の古いファイルをアーカイブする関数 (年月フォルダに仕分けるよう改造)"""
    print(f"\n{ARCHIVE_DAYS}日以上更新されていないファイルの整理を開始します...")
    now = time.time()

    for filename in os.listdir(WATCH_FOLDER):
        source_path = os.path.join(WATCH_FOLDER, filename)
        if not os.path.isfile(source_path):
            continue

        last_modified_time = os.path.getmtime(source_path)
        
        # 古いファイルかどうかを判定
        if (now - last_modified_time) / (60 * 60 * 24) > ARCHIVE_DAYS:
            print(f"古いファイルを検出: {filename}")
            
            # ファイルの最終更新日時から年月フォルダを決定
            file_datetime = datetime.fromtimestamp(last_modified_time)
            year_str = f"{file_datetime.year}年"
            month_str = f"{file_datetime.month}月"
            
            # 年月フォルダを含めた保存先パスを作成
            dest_folder = os.path.join(DESTINATION_BASE_FOLDER, ARCHIVE_FOLDER_NAME, year_str, month_str)
            move_file(source_path, dest_folder, filename)

    print("古いファイルの整理が完了しました。")


def move_file(source_path, dest_folder, filename):
    """ファイルを移動させる共通関数"""
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, filename)
    count = 1
    while os.path.exists(dest_path):
        name, ext = os.path.splitext(filename)
        dest_path = os.path.join(dest_folder, f"{name}_{count}{ext}")
        count += 1
    shutil.move(source_path, dest_path)
    print(f"  -> {filename} を {dest_folder} に移動しました。")


# --- メイン処理 ---
if __name__ == "__main__":
    archive_old_files()
    organize_files()
    print("\n全ての処理が完了しました。")