"""
ローカル環境でNBAデータを取得してCSVファイルに保存するスクリプト
定期的に実行してデータを更新し、GitHubにプッシュすることでStreamlit Cloudでも最新データを利用可能
"""
from nba_api.stats.endpoints import leaguedashteamstats, leaguedashplayerstats
import pandas as pd
from datetime import datetime

def fetch_and_save_data():
    """データを取得してCSVファイルに保存"""
    season = "2025-26"  # 現在のシーズン
    
    print("チームデータを取得中...")
    try:
        team_stats = leaguedashteamstats.LeagueDashTeamStats(
            season=season,
            measure_type_detailed_defense='Advanced',
            league_id_nullable='00'
        )
        team_df = team_stats.get_data_frames()[0]
        
        # 必要なカラムのみ抽出
        team_cols = ['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
        team_df = team_df[[col for col in team_cols if col in team_df.columns]]
        
        # CSVに保存
        team_df.to_csv('data/team_ratings.csv', index=False)
        print(f"✓ チームデータを保存しました: {len(team_df)}チーム")
        
    except Exception as e:
        print(f"✗ チームデータ取得エラー: {e}")
        return False
    
    print("選手データを取得中...")
    try:
        player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            measure_type_detailed_defense='Advanced',
            league_id_nullable='00'
        )
        player_df = player_stats.get_data_frames()[0]
        
        # 必要なカラムのみ抽出
        player_cols = ['PLAYER_NAME', 'TEAM_ID', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'GP']
        player_df = player_df[[col for col in player_cols if col in player_df.columns]]
        
        # CSVに保存
        player_df.to_csv('data/player_ratings.csv', index=False)
        print(f"✓ 選手データを保存しました: {len(player_df)}選手")
        
    except Exception as e:
        print(f"✗ 選手データ取得エラー: {e}")
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
