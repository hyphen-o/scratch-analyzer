import os

def count_files(dir_path):
    file_count = 0

    # ディレクトリ内のファイルとディレクトリのリストを取得
    items = os.listdir(dir_path)

    for item in items:
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):  # ファイルであればカウント
            file_count += 1

    return file_count
