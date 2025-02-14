import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import scipy.stats as stats
from numpy import mean, std
import scipy.stats as stats

# 日本語の項目名と英語の対応表
column_translation = {
    "論理": "Logical thinking",
    "制御フロー": "Flow control",
    "同期": "Synchronization",
    "抽象化": "Abstraction and problem decomposition",
    "データ表現": "Data Representation",
    "ユーザとの対話性": "User Interactivity",
    "並列処理": "Parallelism",
    "CTスコア": "CT Score"
}

def translate_columns(data, translation_dict):
    # 列名の翻訳
    data = data.rename(columns=translation_dict)
    return data

def count_rows_in_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        return len(rows)

def RQ11(data_csv, output_dir):## リミックス前，リミックス，リミックス後のCSV作成
    # データの読み込み
    data = pd.read_csv(data_csv)

    # リミックス作品（リミックス元IDがあるもの）
    remix_data = data[data["リミックス元ID"].notna()]

    # リミックス前、リミックス、リミックス後を格納するリスト
    complete_pairs = []

    for _, remix_row in remix_data.iterrows():
        author_id = remix_row["作者ID"]
        remix_id = remix_row["作品ID"]

        # リミックス前作品の選定 (リミックス元IDがない同じ作者の作品で、リミックスIDより小さいもの)
        before_candidates = data[(data["作者ID"] == author_id) & 
                                  (data["リミックス元ID"].isna()) & 
                                  (data["作品ID"] < remix_id)]
        if not before_candidates.empty:
            before_best = before_candidates.loc[before_candidates["CTスコア"].idxmax()].copy()
            before_best["カテゴリ"] = "リミックス前"
        else:
            continue  # リミックス前が見つからない場合はスキップ

        # リミックス後作品の選定 (リミックスIDより大きい作品で、リミックス元IDがないもののうち直近3つ)
        after_candidates = data[(data["作者ID"] == author_id) & 
                                 (data["リミックス元ID"].isna()) & 
                                 (data["作品ID"] > remix_id)]
        if not after_candidates.empty:
            after_sorted = after_candidates.sort_values(by="作品ID").head(3)
            if not after_sorted.empty:
                after_best = after_sorted.loc[after_sorted["CTスコア"].idxmax()].copy()
                after_best["カテゴリ"] = "リミックス後"
            else:
                continue  # リミックス後が見つからない場合はスキップ
        else:
            continue  # リミックス後が見つからない場合はスキップ

        # リミックス作品にカテゴリを追加
        remix_row_copy = remix_row.copy()
        remix_row_copy["カテゴリ"] = "リミックス"

        # ペアが揃ったらリストに追加
        complete_pairs.extend([before_best, remix_row_copy, after_best])

    # 最終的なデータフレームを作成
    final_data = pd.DataFrame(complete_pairs)

    # 出力ディレクトリにCSVファイルとして保存
    output_file = f"{output_dir}/remix_data_complete_pairs.csv"
    final_data.to_csv(output_file, index=False)

    print(f"リミックス前、リミックス、リミックス後のペアが揃ったデータを保存しました: {output_file}")

def RQ121(data_csv, output_dir):## リミックス前，リミックス，リミックス後のヒートマップ
    # データの読み込み
    data = pd.read_csv(data_csv)

    # 列名を英語に変換
    data = translate_columns(data, column_translation)

    # リミックス前、リミックス、リミックス後にデータを分類
    remix_before = data[data["カテゴリ"] == "リミックス前"]
    remix = data[data["カテゴリ"] == "リミックス"]
    remix_after = data[data["カテゴリ"] == "リミックス後"]

    # 各項目名 (英語に変更)
    columns_to_compare = ["Logical thinking", "Flow control", "Synchronization", "Abstraction and problem decomposition", "Data Representation", 
                          "User Interactivity", "Parallelism", "CT Score"]

    # 上がった、下がった、変わらなかった場合を格納する辞書
    score_changes = {column: {'up': [], 'down': [], 'unchange': []} for column in columns_to_compare}

    # データをペアリングし、スコア変化を計算
    for i in range(len(remix_before)):
        before = remix_before.iloc[i]
        rem = remix.iloc[i]
        after = remix_after.iloc[i]
        
        if before["作者ID"] == rem["作者ID"] == after["作者ID"]:
            for column in columns_to_compare:
                score_before = before[column]
                score_remix = rem[column]
                score_after = after[column]
                
                # スコアの変化を判定
                if score_after > score_before:
                    score_changes[column]['up'].append((score_before, score_remix, score_after))
                elif score_after < score_before:
                    score_changes[column]['down'].append((score_before, score_remix, score_after))
                else:
                    score_changes[column]['unchange'].append((score_before, score_remix, score_after))

    # 各項目ごとに上がった、下がった、変わらなかった数を出力
    for column in columns_to_compare:
        print(f"Summary for {column}:")
        print(f"  Up: {len(score_changes[column]['up'])}")
        print(f"  Down: {len(score_changes[column]['down'])}")
        print(f"  Unchanged: {len(score_changes[column]['unchange'])}")
        print("="*50)

    # ヒートマップを描画する関数
    def plot_heatmap(data, title, output_dir, filename):
        data = data.astype(int)
        plt.figure(figsize=(10, 8))
        sns.heatmap(data, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title(title, fontsize=16)
        plt.xlabel("Remix Score", fontsize=12)  # 横軸のラベルを英語に変更
        plt.ylabel("Pre Original Score", fontsize=12)  # 縦軸のラベルを英語に変更
        
        # 出力先ディレクトリが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)
        
        # 出力ファイルパスを指定して保存
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path)
        plt.close()

    # 各項目ごとにヒートマップを作成
    for column in columns_to_compare:
        for change_type in ['up', 'down', 'unchange']:
            # スコアのペアを取り出し、ヒートマップデータを作成
            score_pairs = score_changes[column][change_type]
            if score_pairs:
                if column == "CT Score":
                    heatmap_data = np.zeros((22, 22))  # CTスコアは0-21の範囲
                else:
                    heatmap_data = np.zeros((4, 4))  # 他の項目は0-3の範囲

                for before_score, remix_score, after_score in score_pairs:
                    # スコアをインデックスに変換
                    if column == "CT Score":
                        before_index = int(before_score) if 0 <= before_score <= 21 else 21
                        remix_index = int(remix_score) if 0 <= remix_score <= 21 else 21
                    else:
                        before_index = int(before_score) if 0 <= before_score <= 3 else 3
                        remix_index = int(remix_score) if 0 <= remix_score <= 3 else 3

                    heatmap_data[before_index, remix_index] += 1

                # ヒートマップのファイル名を作成
                filename = f"{column}_{change_type}.png"
                plot_heatmap(heatmap_data, f"{column} - {change_type}", output_dir, filename)

def RQ122(data_csv, remixp_csv, output_dir):## リミックス前，リミックス元，リミックス後のヒートマップ
    # データの読み込み
    data = pd.read_csv(data_csv)
    remixp_data = pd.read_csv(remixp_csv)

    # 列名を英語に変換
    data = translate_columns(data, column_translation)
    remixp_data = translate_columns(remixp_data, column_translation)

    # リミックス元作品を取得
    remixp_dict = remixp_data.set_index("作品ID").to_dict(orient="index")

    # リミックス前、リミックス、リミックス後のデータを分類
    remix_before = data[data["カテゴリ"] == "リミックス前"]
    remix = data[data["カテゴリ"] == "リミックス"]
    remix_after = data[data["カテゴリ"] == "リミックス後"]

    # 各項目名 (英語に変更)
    columns_to_compare = ["Logical thinking", "Flow control", "Synchronization", "Abstraction and problem decomposition", "Data Representation", 
                          "User Interactivity", "Parallelism", "CT Score"]

    # 上がった、下がった、変わらなかった場合を格納する辞書
    score_changes = {column: {'up': [], 'down': [], 'unchange': []} for column in columns_to_compare}

    # データをペアリングし、スコア変化を計算
    for i in range(len(remix_before)):
        before = remix_before.iloc[i]
        rem = remix.iloc[i]
        after = remix_after.iloc[i]
        
        remix_source_id = rem["リミックス元ID"]

        # リミックス元IDに対応する作品が remixp_data にあるか確認
        if pd.notna(remix_source_id) and remix_source_id in remixp_dict:
            remix_source = remixp_dict[remix_source_id]  # リミックス元作品のデータ

            # 同じ作者で比較
            if before["作者ID"] == rem["作者ID"] == after["作者ID"]:
                for column in columns_to_compare:
                    score_before = before[column]
                    score_remix = rem[column]
                    score_after = after[column]
                    remix_source_score = remix_source[column]  # 横軸のリミックス元作品スコア

                    # スコアの変化を判定
                    if score_after > score_before:
                        score_changes[column]['up'].append((score_before, remix_source_score, score_after))
                    elif score_after < score_before:
                        score_changes[column]['down'].append((score_before, remix_source_score, score_after))
                    else:
                        score_changes[column]['unchange'].append((score_before, remix_source_score, score_after))

    # ヒートマップを描画する関数
    def plot_heatmap(data, title, output_dir, filename):
        # データを整数に変換
        data = np.round(data).astype(int)

        plt.figure(figsize=(10, 8))
        sns.heatmap(data, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title(title, fontsize=16)
        plt.xlabel("Remix Source Score", fontsize=12)
        plt.ylabel("Pre Original Score", fontsize=12)
        
        # 出力先ディレクトリが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)

        # 画像を保存
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path)
        plt.close()
    
    # **ヒートマップを描画する関数（縦軸のデータ数で重み付け）**
    def plot_weighted_heatmap(data, title, output_dir, filename):
        # 縦軸（リミックス前スコア）の出現回数を取得
        row_sums = np.sum(data, axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # 0で割るのを防ぐ

        # 縦軸のデータ数で正規化（重み付け）
        weighted_data = data / row_sums  

        # ヒートマップ描画
        plt.figure(figsize=(10, 8))
        sns.heatmap(weighted_data, annot=True, fmt=".2f", cmap="Blues", cbar=True)
        plt.title(title, fontsize=16)
        plt.xlabel("Remix Source Score", fontsize=12)
        plt.ylabel("Pre Original Score", fontsize=12)
        
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path)
        plt.close()

    for column in columns_to_compare:
        for change_type in ['up', 'down', 'unchange']:
            # スコアのペアを取り出し、ヒートマップデータを作成
            score_pairs = score_changes[column][change_type]
            if score_pairs:
                if column == "CT Score":
                    heatmap_data = np.zeros((22, 22))  # CTスコアは0-21の範囲
                else:
                    heatmap_data = np.zeros((4, 4))  # 他の項目は0-3の範囲

                for before_score, remix_source_score, after_score in score_pairs:
                    # スコアをインデックスに変換
                    if column == "CT Score":
                        before_index = int(before_score) if 0 <= before_score <= 21 else 21
                        remix_source_index = int(remix_source_score) if 0 <= remix_source_score <= 21 else 21
                    else:
                        before_index = int(before_score) if 0 <= before_score <= 3 else 3
                        remix_source_index = int(remix_source_score) if 0 <= remix_source_score <= 3 else 3

                    heatmap_data[before_index, remix_source_index] += 1

                # # ヒートマップのファイル名を作成
                # filename = f"{column}_{change_type}.png"
                # plot_heatmap(heatmap_data, f"{column} - {change_type}", output_dir, filename)

                # **重み付きヒートマップの描画**
                filename = f"{column}_{change_type}_weighted.png"
                plot_weighted_heatmap(heatmap_data, f"{column} - {change_type} (Weighted)", output_dir, filename)

    # 各項目ごとに上がった、下がった、変わらなかった数を出力
    for column in columns_to_compare:
        print(f"Summary for {column}:")
        print(f"  Up: {len(score_changes[column]['up'])}")
        print(f"  Down: {len(score_changes[column]['down'])}")
        print(f"  Unchanged: {len(score_changes[column]['unchange'])}")
        print("="*50)

def RQ122_boxplot(data_csv, remixp_csv, output_dir):## 縦軸リミックス前とリミックス元のスコア差，横軸リミックス前でリミックス前と後で上がったかどうかの箱ひげ図
    # データの読み込み
    data = pd.read_csv(data_csv)
    remixp_data = pd.read_csv(remixp_csv)

    # 列名を英語に変換
    data = translate_columns(data, column_translation)
    remixp_data = translate_columns(remixp_data, column_translation)

    # リミックス元作品のデータを辞書化
    remixp_dict = remixp_data.set_index("作品ID").to_dict(orient="index")

    # リミックス前、リミックス、リミックス後のデータを分類
    remix_before = data[data["カテゴリ"] == "リミックス前"]
    remix = data[data["カテゴリ"] == "リミックス"]
    remix_after = data[data["カテゴリ"] == "リミックス後"]

    # 比較する項目
    columns_to_compare = ["Logical thinking", "Flow control", "Synchronization", "Abstraction and problem decomposition", 
                          "Data Representation", "User Interactivity", "Parallelism", "CT Score"]

    # 箱ひげ図用のデータリスト
    boxplot_data = []

    # 各項目のスコア変化のカウントを保存する辞書
    score_changes = {column: {"Up": 0, "Down": 0, "Unchanged": 0} for column in columns_to_compare}


    # データをペアリングし、スコア変化を計算
    for i in range(len(remix_before)):
        before = remix_before.iloc[i]
        rem = remix.iloc[i]
        after = remix_after.iloc[i]

        remix_source_id = rem["リミックス元ID"]

        # リミックス元IDに対応する作品が remixp_data にあるか確認
        if pd.notna(remix_source_id) and remix_source_id in remixp_dict:
            remix_source = remixp_dict[remix_source_id]  # リミックス元作品のデータ

            # 同じ作者で比較
            if before["作者ID"] == rem["作者ID"] == after["作者ID"]:
                for column in columns_to_compare:
                    score_before = before[column]  # リミックス前のスコア
                    remix_source_score = remix_source[column]  # リミックス元のスコア
                    score_after = after[column]  # リミックス後のスコア
                    
                    # **縦軸の値（リミックス前とリミックス元のスコア差）**
                    score_diff = remix_source_score  - score_before

                    # **スコアの変化（リミックス前 vs リミックス後）**
                    if score_after > score_before:
                        change_type = "Up"
                    elif score_after < score_before:
                        change_type = "Down"
                    else:
                        change_type = "Unchanged"

                    # 変化のカウントを増やす
                    score_changes[column][change_type] += 1

                    # データ追加
                    boxplot_data.append({
                        "Remix Before Score": score_before,
                        "Score Difference": score_diff,
                        "Change Type": change_type,
                        "Column": column
                    })

    # データフレームに変換
    df_boxplot = pd.DataFrame(boxplot_data)

    palette = {
        "Up": (0.6, 0.8, 1, 0.6),        # **薄い青 (淡い水色, 透明度 60%)**
        "Down": (1, 0.6, 0.6, 0.6),      # **薄い赤 (淡いピンク, 透明度 60%)**
        "Unchanged": (0.8, 0.8, 0.8, 0.6) # **薄いグレー (透明度 60%)**
    }


    # **箱ひげ図を描画する関数**
    def plot_boxplot(df, column, output_dir):
        plt.figure(figsize=(12, 6))
        sns.boxplot(
            data=df[df["Column"] == column], 
            x="Remix Before Score", 
            y="Score Difference", 
            hue="Change Type", 
            palette=palette,
            boxprops={"edgecolor": "black"},     # **箱の枠線を黒に**
            medianprops={"color": "black"},      # **中央値の線を黒に**
            whiskerprops={"color": "black"},     # **ひげ（上下の線）を黒に**
            capprops={"color": "black"}          # **ひげの端（キャップ）を黒に**
        )
        plt.axhline(0, color="black", linestyle="--")  # 基準線
        plt.title(f"Score Difference: Remix Source - Remix Before ({column})", fontsize=14)
        plt.xlabel("Remix Before Score", fontsize=12)
        plt.ylabel("Score Difference (Before - Source)", fontsize=12)
        
        os.makedirs(output_dir, exist_ok=True)
        plt.legend(title="Change Type")
        output_path = os.path.join(output_dir, f"{column}_boxplot.png")
        plt.savefig(output_path)
        plt.close()

    # 各スキル項目ごとに箱ひげ図を作成
    for column in columns_to_compare:
        plot_boxplot(df_boxplot, column, output_dir)
    
    print("Boxplots saved in:", output_dir)

    # **各項目ごとのスコア変化を出力**
    for column in columns_to_compare:
        print(f"Summary for {column}:")
        print(f"  Up: {score_changes[column]['Up']}")
        print(f"  Down: {score_changes[column]['Down']}")
        print(f"  Unchanged: {score_changes[column]['Unchanged']}")
        print("=" * 50)

def analyze_scratch_data(csv_file):## データのユーザ数，リミックス作品数，オリジナル作品数をカウント
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)
    
    # リミックス作品数（リミックス元IDがあるもの）
    remix_count = df[df["リミックス元ID"].notna() & (df["リミックス元ID"] != "")].shape[0]
    
    # ユーザ数（ユニークな作者IDの数）
    user_count = df["作者ID"].nunique()
    
    # オリジナル作品数（リミックス元IDがないものの数）
    original_count = df[df["リミックス元ID"].isna() | (df["リミックス元ID"] == "")].shape[0]
    
    return remix_count, user_count, original_count

def RQ_T(data_csv, remixp_csv):## T検定
    # データの読み込み
    data = pd.read_csv(data_csv)
    remixp_data = pd.read_csv(remixp_csv)

    # 列名を英語に変換
    data = translate_columns(data, column_translation)
    remixp_data = translate_columns(remixp_data, column_translation)

    # リミックス元作品のデータを辞書化
    remixp_dict = remixp_data.set_index("作品ID").to_dict(orient="index")

    # リミックス前、リミックス、リミックス後のデータを分類
    remix_before = data[data["カテゴリ"] == "リミックス前"]
    remix = data[data["カテゴリ"] == "リミックス"]
    remix_after = data[data["カテゴリ"] == "リミックス後"]

    # 比較する項目
    columns_to_compare = ["Logical thinking", "Flow control", "Synchronization", "Abstraction and problem decomposition", 
                          "Data Representation", "User Interactivity", "Parallelism", "CT Score"]

    # 箱ひげ図用のデータリスト
    boxplot_data = []

    # 各項目のスコア変化のカウントを保存する辞書
    score_changes = {column: {"Up": 0, "Down": 0, "Unchanged": 0} for column in columns_to_compare}


    # データをペアリングし、スコア変化を計算
    for i in range(len(remix_before)):
        before = remix_before.iloc[i]
        rem = remix.iloc[i]
        after = remix_after.iloc[i]

        remix_source_id = rem["リミックス元ID"]

        # リミックス元IDに対応する作品が remixp_data にあるか確認
        if pd.notna(remix_source_id) and remix_source_id in remixp_dict:
            remix_source = remixp_dict[remix_source_id]  # リミックス元作品のデータ

            # 同じ作者で比較
            if before["作者ID"] == rem["作者ID"] == after["作者ID"]:
                for column in columns_to_compare:
                    score_before = before[column]  # リミックス前のスコア
                    remix_source_score = remix_source[column]  # リミックス元のスコア
                    score_after = after[column]  # リミックス後のスコア
                    
                    # **縦軸の値（リミックス前とリミックス元のスコア差）**
                    score_diff = remix_source_score  - score_before

                    # **スコアの変化（リミックス前 vs リミックス後）**
                    if score_after > score_before:
                        change_type = "Up"
                    elif score_after < score_before:
                        change_type = "Down"
                    else:
                        change_type = "Unchanged"

                    # 変化のカウントを増やす
                    score_changes[column][change_type] += 1

                    # データ追加
                    boxplot_data.append({
                        "Remix Before Score": score_before,
                        "Score Difference": score_diff,
                        "Change Type": change_type,
                        "Column": column
                    })

    # データフレームに変換
    df_boxplot = pd.DataFrame(boxplot_data)


    def perform_t_tests(df, column):
        up_scores = df[(df["Column"] == column) & (df["Change Type"] == "Up")]["Score Difference"]
        down_scores = df[(df["Column"] == column) & (df["Change Type"] == "Down")]["Score Difference"]
        unchanged_scores = df[(df["Column"] == column) & (df["Change Type"] == "Unchanged")]["Score Difference"]

        print(f"\nT-Tests for {column}:")
        
        # Up vs Down
        if len(up_scores) > 1 and len(down_scores) > 1:
            t_stat, p_value = stats.ttest_ind(up_scores, down_scores, equal_var=False)
            print(f"  Up vs Down: t = {t_stat:.3f}, p = {p_value:.5f}")

        # Up vs Unchanged
        if len(up_scores) > 1 and len(unchanged_scores) > 1:
            t_stat, p_value = stats.ttest_ind(up_scores, unchanged_scores, equal_var=False)
            print(f"  Up vs Unchanged: t = {t_stat:.3f}, p = {p_value:.5f}")

        # Down vs Unchanged
        if len(down_scores) > 1 and len(unchanged_scores) > 1:
            t_stat, p_value = stats.ttest_ind(down_scores, unchanged_scores, equal_var=False)
            print(f"  Down vs Unchanged: t = {t_stat:.3f}, p = {p_value:.5f}")

        # ANOVA (3グループ比較)
        f_stat, p_value = stats.f_oneway(up_scores, down_scores)
        print(f"ANOVA結果（Up vs Down）: F = {f_stat:.3f}, p = {p_value:.5f}")
        eta_squared = f_stat / (f_stat + (len(up_scores) + len(down_scores) - 2))
        print(f"効果量 η² (Eta Squared): {eta_squared:.5f}")  # 平均を取らずそのまま出力



        print("Up count:", len(up_scores))
        print("Down count:", len(down_scores))
        print("Unchanged count:", len(unchanged_scores))



    # 各スキル項目ごとに箱ひげ図を作成
    for column in columns_to_compare:
        perform_t_tests(df_boxplot, column)


    # # **各項目ごとのスコア変化を出力**
    # for column in columns_to_compare:
    #     print(f"Summary for {column}:")
    #     print(f"  Up: {score_changes[column]['Up']}")
    #     print(f"  Down: {score_changes[column]['Down']}")
    #     print(f"  Unchanged: {score_changes[column]['Unchanged']}")
    #     print("=" * 50)

def RQ_U(data_csv, remixp_csv):## U検定
    # データの読み込み
    data = pd.read_csv(data_csv)
    remixp_data = pd.read_csv(remixp_csv)

    # 列名を英語に変換
    data = translate_columns(data, column_translation)
    remixp_data = translate_columns(remixp_data, column_translation)

    # リミックス元作品のデータを辞書化
    remixp_dict = remixp_data.set_index("作品ID").to_dict(orient="index")

    # リミックス前、リミックス、リミックス後のデータを分類
    remix_before = data[data["カテゴリ"] == "リミックス前"]
    remix = data[data["カテゴリ"] == "リミックス"]
    remix_after = data[data["カテゴリ"] == "リミックス後"]

    # 比較する項目
    columns_to_compare = ["Logical thinking", "Flow control", "Synchronization", "Abstraction and problem decomposition", 
                          "Data Representation", "User Interactivity", "Parallelism", "CT Score"]

    # 箱ひげ図用のデータリスト
    boxplot_data = []

    # 各項目のスコア変化のカウントを保存する辞書
    score_changes = {column: {"Up": 0, "Down": 0, "Unchanged": 0} for column in columns_to_compare}


    # データをペアリングし、スコア変化を計算
    for i in range(len(remix_before)):
        before = remix_before.iloc[i]
        rem = remix.iloc[i]
        after = remix_after.iloc[i]

        remix_source_id = rem["リミックス元ID"]

        # リミックス元IDに対応する作品が remixp_data にあるか確認
        if pd.notna(remix_source_id) and remix_source_id in remixp_dict:
            remix_source = remixp_dict[remix_source_id]  # リミックス元作品のデータ

            # 同じ作者で比較
            if before["作者ID"] == rem["作者ID"] == after["作者ID"]:
                for column in columns_to_compare:
                    score_before = before[column]  # リミックス前のスコア
                    remix_source_score = remix_source[column]  # リミックス元のスコア
                    score_after = after[column]  # リミックス後のスコア
                    
                    # **縦軸の値（リミックス前とリミックス元のスコア差）**
                    score_diff = remix_source_score  - score_before

                    # **スコアの変化（リミックス前 vs リミックス後）**
                    if score_after > score_before:
                        change_type = "Up"
                    elif score_after < score_before:
                        change_type = "Down"
                    else:
                        change_type = "Unchanged"

                    # 変化のカウントを増やす
                    score_changes[column][change_type] += 1

                    # データ追加
                    boxplot_data.append({
                        "Remix Before Score": score_before,
                        "Score Difference": score_diff,
                        "Change Type": change_type,
                        "Column": column
                    })

    # データフレームに変換
    df_boxplot = pd.DataFrame(boxplot_data)

    def Ukentei(df, column):
        up_scores = df[(df["Column"] == column) & (df["Change Type"] == "Up")]["Score Difference"]
        down_scores = df[(df["Column"] == column) & (df["Change Type"] == "Down")]["Score Difference"]
        unchanged_scores = df[(df["Column"] == column) & (df["Change Type"] == "Unchanged")]["Score Difference"]
        # Mann-Whitney U検定
        stat, p_value = stats.mannwhitneyu(up_scores, down_scores, alternative='two-sided')
        print(f"\nMann-Whitney-U for {column}:")
        # 結果の表示
        print(f"Mann-Whitney U検定の統計量: {stat}")
        print(f"p値: {p_value}")

        print("Up count:", len(up_scores))
        print("Down count:", len(down_scores))
        print("Unchanged count:", len(unchanged_scores))



    # 各スキル項目ごとに箱ひげ図を作成
    for column in columns_to_compare:
        Ukentei(df_boxplot, column)


    # # **各項目ごとのスコア変化を出力**
    # for column in columns_to_compare:
    #     print(f"Summary for {column}:")
    #     print(f"  Up: {score_changes[column]['Up']}")
    #     print(f"  Down: {score_changes[column]['Down']}")
    #     print(f"  Unchanged: {score_changes[column]['Unchanged']}")
    #     print("=" * 50)

def RQ1_2_boxplot_histgram(data_csv, remixp_csv, output_dir):
    # データの読み込み
    data = pd.read_csv(data_csv)
    remixp_data = pd.read_csv(remixp_csv)

    # 列名を英語に変換
    data = translate_columns(data, column_translation)
    remixp_data = translate_columns(remixp_data, column_translation)

    # リミックス元作品のデータを辞書化
    remixp_dict = remixp_data.set_index("作品ID").to_dict(orient="index")

    # リミックス前、リミックス、リミックス後のデータを分類
    remix_before = data[data["カテゴリ"] == "リミックス前"]
    remix = data[data["カテゴリ"] == "リミックス"]
    remix_after = data[data["カテゴリ"] == "リミックス後"]

    # 比較する項目
    columns_to_compare = ["Logical thinking", "Flow control", "Synchronization", "Abstraction and problem decomposition", 
                          "Data Representation", "User Interactivity", "Parallelism", "CT Score"]

    # データリスト
    boxplot_data = []
    hist_data = []

    # スコア変化のカウント辞書
    score_changes = {column: {} for column in columns_to_compare}

    # データをペアリングし、スコア変化を計算
    for i in range(len(remix_before)):
        before = remix_before.iloc[i]
        rem = remix.iloc[i]
        after = remix_after.iloc[i]

        remix_source_id = rem["リミックス元ID"]

        if pd.notna(remix_source_id) and remix_source_id in remixp_dict:
            remix_source = remixp_dict[remix_source_id]
            if before["作者ID"] == rem["作者ID"] == after["作者ID"]:
                for column in columns_to_compare:
                    score_before = before[column]
                    remix_source_score = remix_source[column]
                    score_after = after[column]
                    
                    score_diff = remix_source_score - score_before
                    change_value = score_after - score_before
                    
                    if change_value > 0:
                        change_type = "Up"
                    elif change_value < 0:
                        change_type = "Down"
                    else:
                        change_type = "Unchanged"
                    
                    if score_before not in score_changes[column]:
                        score_changes[column][score_before] = {"Up": 0, "Down": 0, "Unchanged": 0}
                    score_changes[column][score_before][change_type] += 1
                    
                    boxplot_data.append({
                        "Remix Before Score": score_before,
                        "Score Difference": score_diff,
                        "Change Type": change_type,
                        "Column": column
                    })
                    
                    hist_data.append({
                        "Remix Before Score": score_before,
                        "Change Type": change_type,
                        "Column": column
                    })

    df_boxplot = pd.DataFrame(boxplot_data)
    df_hist = pd.DataFrame(hist_data)

    palette = {
        "Up": (0.6, 0.8, 1, 1.0),
        "Unchanged": (0.8, 0.8, 0.8, 1.0),
        "Down": (1, 0.6, 0.6, 1.0)
    }

    def plot_boxplot(df, column, output_dir):
        plt.figure(figsize=(12, 6))
        sns.boxplot(
            data=df[df["Column"] == column], 
            x="Remix Before Score", 
            y="Score Difference", 
            hue="Change Type", 
            hue_order=["Up", "Unchanged", "Down"],
            palette=palette,
            boxprops={"edgecolor": "black"},
            medianprops={"color": "black"},
            whiskerprops={"color": "black"},
            capprops={"color": "black"}
        )
        plt.axhline(0, color="black", linestyle="--")
        plt.title(f"Score Difference: Remix Source - Remix Before ({column})", fontsize=14)
        plt.xlabel("Remix Before Score", fontsize=12)
        plt.ylabel("Score Difference (Before - Source)", fontsize=12)
        
        os.makedirs(output_dir, exist_ok=True)
        plt.legend(title="Change Type")
        output_path = os.path.join(output_dir, f"{column}_boxplot.png")
        plt.savefig(output_path)
        plt.close()

    def plot_histogram(score_changes, column, output_dir):
        scores = sorted(score_changes[column].keys())
        up_values = [score_changes[column][score]["Up"] for score in scores]
        unchanged_values = [score_changes[column][score]["Unchanged"] for score in scores]
        down_values = [score_changes[column][score]["Down"] for score in scores]
        
        x = np.arange(len(scores))
        width = 0.3
        
        plt.figure(figsize=(12, 6))
        plt.bar(x - width, up_values, width=width, label="Up", color=palette["Up"])
        plt.bar(x, unchanged_values, width=width, label="Unchanged", color=palette["Unchanged"])
        plt.bar(x + width, down_values, width=width, label="Down", color=palette["Down"])
        
        plt.xticks(ticks=x, labels=scores)
        plt.title(f"Distribution of Score Changes ({column})", fontsize=14)
        plt.xlabel("Remix Before Score", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.legend()
        
        output_path = os.path.join(output_dir, f"{column}_histogram.png")
        plt.savefig(output_path)
        plt.close()

    for column in columns_to_compare:
        plot_boxplot(df_boxplot, column, output_dir)
        plot_histogram(score_changes, column, output_dir)
    
    print("Boxplots and histograms saved in:", output_dir)

    for column in columns_to_compare:
        print(f"Summary for {column}:")
        for score in sorted(score_changes[column].keys()):
            print(f"  Score {score}: Up={score_changes[column][score]['Up']}, Down={score_changes[column][score]['Down']}, Unchanged={score_changes[column][score]['Unchanged']}")
        print("=" * 50)

def RQ3_boxplot_histgram(data_csv, remixp_csv, output_dir):
    # データの読み込み
    data = pd.read_csv(data_csv)
    remixp_data = pd.read_csv(remixp_csv)

    data = translate_columns(data, column_translation)
    remixp_data = translate_columns(remixp_data, column_translation)

    # リミックス元作品のデータを辞書化
    remixp_dict = remixp_data.set_index("作品ID").to_dict(orient="index")

    # リミックス前、リミックス、リミックス後のデータを分類
    remix_before = data[data["カテゴリ"] == "リミックス前"]
    remix = data[data["カテゴリ"] == "リミックス"]
    remix_after = data[data["カテゴリ"] == "リミックス後"]
    
    # 比較する項目
    columns_to_compare = ["Logical thinking", "Flow control", "Synchronization", "Abstraction and problem decomposition", 
                          "Data Representation", "User Interactivity", "Parallelism"]

    # カラーパレット
    palette = {
        "Up": (0.6, 0.8, 1, 1.0),
        "Unchanged": (0.8, 0.8, 0.8, 1.0),
        "Down": (1, 0.6, 0.6, 1.0)
    }

    # データリスト
    boxplot_data = []
    hist_data = {column: {score: {"Up": 0, "Unchanged": 0, "Down": 0} for score in range(1, 6)} for column in columns_to_compare}

    # データをペアリングし、スコア変化を計算
    for i in range(len(remix_before)):
        before = remix_before.iloc[i]
        after = remix_after.iloc[i]
        remix_source_id = remix.iloc[i]["リミックス元ID"]
        
        if pd.notna(remix_source_id) and remix_source_id in remixp_dict:
            remix_source = remixp_dict[remix_source_id]
            
            for column in columns_to_compare:
                score_before = before[column]
                score_after = after[column]
                change_type = "Up" if score_after > score_before else "Down" if score_after < score_before else "Unchanged"
                
                ct_score_diff = remix_source["CT Score"] - before["CT Score"]
                
                boxplot_data.append({
                    "Remix Before CT Score": before["CT Score"],
                    "CT Score Difference": ct_score_diff,
                    "Column": column,
                    "Change Type": change_type
                })

                # hist_dataを動的に更新するよう修正
                if before["CT Score"] not in hist_data[column]:
                    hist_data[column][before["CT Score"]] = {"Up": 0, "Unchanged": 0, "Down": 0}
                hist_data[column][before["CT Score"]][change_type] += 1

    df_boxplot = pd.DataFrame(boxplot_data)

    def plot_boxplot(df, column, output_dir):
        plt.figure(figsize=(12, 6))
        sns.boxplot(
            data=df[df["Column"] == column], 
            x="Remix Before CT Score", 
            y="CT Score Difference",
            hue="Change Type",
            hue_order=["Up", "Unchanged", "Down"],
            palette=palette,
            boxprops={"edgecolor": "black"},
            medianprops={"color": "black"},
            whiskerprops={"color": "black"},
            capprops={"color": "black"}
        )
        plt.axhline(0, color="black", linestyle="--")
        plt.title(f"CT Score Difference: Remix Source - Remix Before ({column})", fontsize=14)
        plt.xlabel("Remix Before CT Score", fontsize=12)
        plt.ylabel("CT Score Difference (Source - Before)", fontsize=12)
        
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{column}_ctscore_boxplot.png")
        plt.savefig(output_path)
        plt.close()

    def plot_histogram(hist_data, column, output_dir):
        categories = ["Up", "Unchanged", "Down"]
        scores = sorted(hist_data[column].keys())
        values = [[hist_data[column][score][cat] for cat in categories] for score in scores]
        
        x_labels = [str(score) for score in scores]
        x = range(len(scores))
        width = 0.3
        
        plt.figure(figsize=(10, 6))
        for i, cat in enumerate(categories):
            plt.bar([p + i * width for p in x], [values[j][i] for j in range(len(scores))], width=width, label=cat, color=palette[cat])
        
        plt.xticks([p + width for p in x], x_labels)
        plt.title(f"Change Distribution for {column}", fontsize=14)
        plt.xlabel("Remix Before CT Score", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.legend()
        
        output_path = os.path.join(output_dir, f"{column}_histogram.png")
        plt.savefig(output_path)
        plt.close()

    for column in columns_to_compare:
        plot_boxplot(df_boxplot, column, output_dir)
        plot_histogram(hist_data, column, output_dir)
    
    print("Boxplots and histograms saved in:", output_dir)


# 実行例
data_csv = '../../dataset/plotdata/dataset/data1.csv'
remixp_csv = '../../dataset/plotdata/dataset/remixparent_data.csv'
output_dir = '../../dataset/plotdata/RQ2'
rq1data_csv = '../../dataset/plotdata/RQ1/remix_data_complete_pairs.csv'
# RQ11(data_csv, output_dir)
# RQ122_boxplot(rq1data_csv, remixp_csv, output_dir)
RQ1_2_boxplot_histgram(rq1data_csv, remixp_csv, output_dir)
# print(f"行数: {count_rows_in_csv(data_csv)}")

# 列名を英語に変換
    # data = translate_columns(data, column_translation)
    # remixp_data = translate_columns(remixp_data, column_translation)

# remix_count, user_count, original_count = analyze_scratch_data(data_csv)
# print(f"リミックス作品数: {remix_count}")
# print(f"ユーザ数: {user_count}")
# print(f"オリジナル作品数: {original_count}")
# print(count_rows_in_csv(remixp_csv))

RQ_U(rq1data_csv, remixp_csv)
