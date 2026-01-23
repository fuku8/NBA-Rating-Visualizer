"""
Basketball Referenceから2025-26シーズンのNBAデータを取得してCSVファイルに保存するスクリプト
定期的に実行してデータを更新し、GitHubにプッシュすることでStreamlit Cloudでも最新データを利用可能
"""
import pandas as pd
import requests
from datetime import datetime
import time
import os

def fetch_basketball_reference_data():
    """Basketball ReferenceからデータをスクレイピングしてCSVに保存"""

    # User-Agentを設定（礼儀正しくアクセス）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    season_year = "2026"  # 2025-26シーズンは2026として表記

    # チームデータを取得
    print("Basketball Referenceからチームデータを取得中...")
    try:
        # チームのAdvanced Statsを取得
        team_url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}.html"

        # すべてのテーブルを取得
        all_tables = pd.read_html(team_url)

        # Advanced Statsを含むテーブルを探す（ORtgを含むテーブル）
        team_df = None
        for table in all_tables:
            # マルチインデックスの場合、レベル1のカラム名をチェック
            if isinstance(table.columns, pd.MultiIndex):
                level_0_cols = [col[0] for col in table.columns]
                if 'Unnamed: 10_level_0' in level_0_cols or 'ORtg' in level_0_cols:
                    # マルチインデックスを解除（レベル1を使用）
                    table.columns = [col[1] if col[1] != 'Unnamed: ' + str(i) + '_level_1' else col[0]
                                    for i, col in enumerate(table.columns)]
                    team_df = table
                    break
            else:
                # シングルインデックスの場合
                if 'ORtg' in table.columns:
                    team_df = table
                    break

        if team_df is None:
            print("✗ チームのAdvanced Statsテーブルが見つかりません")
            return False

        # カラム名を確認してマッピング
        # Basketball Referenceでは: Team, ORtg, DRtg, NRtg
        column_mapping = {
            'Team': 'TEAM_NAME',
            'ORtg': 'OFF_RATING',
            'DRtg': 'DEF_RATING',
            'NRtg': 'NET_RATING'
        }

        team_df = team_df.rename(columns=column_mapping)

        # 必要なカラムを抽出
        team_cols = ['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
        team_df = team_df[[col for col in team_cols if col in team_df.columns]]

        # リーグ平均の行を削除（存在する場合）
        team_df = team_df[team_df['TEAM_NAME'] != 'League Average']

        # 欠損値を削除
        team_df = team_df.dropna(subset=['TEAM_NAME'])

        # 数値型に変換
        numeric_cols = ['OFF_RATING', 'DEF_RATING', 'NET_RATING']
        for col in numeric_cols:
            if col in team_df.columns:
                team_df[col] = pd.to_numeric(team_df[col], errors='coerce')

        # CSVに保存
        team_df.to_csv('data/team_ratings.csv', index=False)
        print(f"✓ チームデータを保存しました: {len(team_df)}チーム")

    except Exception as e:
        print(f"✗ チームデータ取得エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 礼儀正しく待機
    print("\n5秒待機中...")
    time.sleep(5)

    # 選手データを取得
    print("Basketball Referenceから選手データを取得中...")
    try:
        # 選手のAdvanced Statsを取得
        player_url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}_advanced.html"

        # pandasでHTMLテーブルを読み込む
        player_tables = pd.read_html(player_url)

        if len(player_tables) == 0:
            print("✗ 選手のAdvanced Statsテーブルが見つかりません")
            return False

        player_df = player_tables[0]

        # カラム名を確認してマッピング
        # Basketball Referenceでは: Player, Team, OWS (Offensive Win Shares), DWS (Defensive Win Shares), WS (Total Win Shares), G
        column_mapping = {
            'Player': 'PLAYER_NAME',
            'Team': 'TEAM_ID',
            'OWS': 'OFF_RATING',      # Offensive Win Shares を OFF_RATING として使用
            'DWS': 'DEF_RATING',      # Defensive Win Shares を DEF_RATING として使用
            'WS': 'NET_RATING',       # Total Win Shares を NET_RATING として使用
            'G': 'GP'
        }

        player_df = player_df.rename(columns=column_mapping)

        # 必要なカラムを抽出
        player_cols = ['PLAYER_NAME', 'TEAM_ID', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'GP']
        player_df = player_df[[col for col in player_cols if col in player_df.columns]]

        # ヘッダー行を削除（存在する場合）
        player_df = player_df[player_df['PLAYER_NAME'] != 'Player']

        # 数値型に変換
        numeric_cols = ['OFF_RATING', 'DEF_RATING', 'NET_RATING', 'GP']
        for col in numeric_cols:
            if col in player_df.columns:
                player_df[col] = pd.to_numeric(player_df[col], errors='coerce')

        # 欠損値を削除
        player_df = player_df.dropna(subset=['PLAYER_NAME'])

        # CSVに保存
        player_df.to_csv('data/player_ratings.csv', index=False)
        print(f"✓ 選手データを保存しました: {len(player_df)}選手")

    except Exception as e:
        print(f"✗ 選手データ取得エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 更新日時を記録
    with open('data/last_updated.txt', 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("\n✓ すべてのデータ取得が完了しました")
    return True

if __name__ == "__main__":
    # dataディレクトリを作成
    os.makedirs('data', exist_ok=True)

    fetch_basketball_reference_data()
