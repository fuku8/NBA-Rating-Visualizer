"""
ローカル環境でNBAデータを取得してCSVファイルに保存するスクリプト
定期的に実行してデータを更新し、GitHubにプッシュすることでStreamlit Cloudでも最新データを利用可能
"""
from nba_api.stats.endpoints import leaguedashteamstats, leaguedashplayerstats
import pandas as pd
from datetime import datetime
import time

def fetch_with_retry(fetch_func, max_retries=3, retry_delay=5):
    """リトライロジック付きでデータ取得を実行"""
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"  リトライ {attempt}/{max_retries-1}...")
                time.sleep(retry_delay)
            return fetch_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"  エラー発生: {e}")
            print(f"  {retry_delay}秒後に再試行します...")
    return None

def fetch_and_save_data():
    """データを取得してCSVファイルに保存"""
    season = "2025-26"  # 現在のシーズン

    print("チームデータを取得中...")
    try:
        def fetch_team_data():
            team_stats = leaguedashteamstats.LeagueDashTeamStats(
                season=season,
                measure_type_detailed_defense='Advanced',
                league_id_nullable='00',
                timeout=60  # タイムアウトを60秒に延長
            )
            return team_stats.get_data_frames()[0]

        team_df = fetch_with_retry(fetch_team_data)

        # 必要なカラムのみ抽出
        team_cols = ['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
        team_df = team_df[[col for col in team_cols if col in team_df.columns]]

        # CSVに保存
        team_df.to_csv('data/team_ratings.csv', index=False)
        print(f"✓ チームデータを保存しました: {len(team_df)}チーム")

    except Exception as e:
        print(f"✗ チームデータ取得エラー（最大試行回数超過）: {e}")
        return False

    print("\n選手データを取得中...")
    try:
        def fetch_player_data():
            player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                measure_type_detailed_defense='Advanced',
                league_id_nullable='00',
                timeout=60  # タイムアウトを60秒に延長
            )
            return player_stats.get_data_frames()[0]

        player_df = fetch_with_retry(fetch_player_data)

        # 必要なカラムのみ抽出
        player_cols = ['PLAYER_NAME', 'TEAM_ID', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'GP']
        player_df = player_df[[col for col in player_cols if col in player_df.columns]]

        # CSVに保存
        player_df.to_csv('data/player_ratings.csv', index=False)
        print(f"✓ 選手データを保存しました: {len(player_df)}選手")

    except Exception as e:
        print(f"✗ 選手データ取得エラー（最大試行回数超過）: {e}")
        return False

    # 更新日時を記録
    with open('data/last_updated.txt', 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("\n✓ すべてのデータ取得が完了しました")
    return True

if __name__ == "__main__":
    import os
    
    # dataディレクトリを作成
    os.makedirs('data', exist_ok=True)
    
    fetch_and_save_data()
