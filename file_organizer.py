import os
import shutil
import time
from datetime import datetime
from pathlib import Path # pathlibをインポート

# --- ユーザー設定エリア（ここを自由に変更してください） ---

# 3. キーワードによる仕分けルール (ファイル名にキーワードが含まれていれば、指定フォルダに移動)
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

# 5. お掃除機能の設定 (指定日数以上更新がないファイルを移動)
ARCHIVE_DAYS = 30
ARCHIVE_FOLDER_NAME = "長期保管（アーカイブ）"

# --- 設定はここまで ---

# --- 自動設定エリア（ここから下は変更不要です） ---

# 1. 整理したいフォルダのパス (ユーザーのダウンロードフォルダを自動取得)
WATCH_FOLDER = Path.home() / "Downloads"

# 2. 整理後のファイルを保存する基本フォルダのパス (ユーザーのドキュメントフォルダを自動取得)
DESTINATION_BASE_FOLDER = Path.home() / "Documents" / "整理済みファイル"

# --- プログラム本体 ---

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
        
        last_modified_time = datetime.fromtimestamp(os.path.getmtime(source_path))
        year_str = f"{last_modified_time.year}年"
        month_str = f"{last_modified_time.month}月"
        moved = False
        for keyword, folder_name in KEYWORD_RULES.items():
            if keyword in filename:
                dest_folder = os.path.join(DESTINATION_BASE_FOLDER, year_str, month_str, folder_name)
                move_file(source_path, dest_folder, filename)
                moved = True
                break
        if moved:
            continue
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension in EXTENSION_RULES:
            folder_name = EXTENSION_RULES[file_extension]
            dest_folder = os.path.join(DESTINATION_BASE_FOLDER, year_str, month_str, folder_name)
            move_file(source_path, dest_folder, filename)
            continue
    print("今回のファイル整理が完了しました。")

def archive_old_files():
    """WATCH_FOLDER内の古いファイルをアーカイブする関数"""
    print(f"\n{ARCHIVE_DAYS}日以上更新されていないファイルの整理を開始します...")
    now = time.time()

    for filename in os.listdir(WATCH_FOLDER):
        source_path = os.path.join(WATCH_FOLDER, filename)
        if not os.path.isfile(source_path):
            continue
        last_modified_time = os.path.getmtime(source_path)
        if (now - last_modified_time) / (60 * 60 * 24) > ARCHIVE_DAYS:
            print(f"古いファイルを検出: {filename}")
            file_datetime = datetime.fromtimestamp(last_modified_time)
            year_str = f"{file_datetime.year}年"
            month_str = f"{file_datetime.month}月"
            dest_folder = os.path.join(DESTINATION_BASE_FOLDER, ARCHIVE_FOLDER_NAME, year_str, month_str)
            move_file(source_path, dest_folder, filename)
    print("古いファイルの整理が完了しました。")

if __name__ == "__main__":
    try:
        archive_old_files()
        organize_files()
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    finally:
        input("\n全ての処理が完了しました。Enterキーを押して終了してください...")
