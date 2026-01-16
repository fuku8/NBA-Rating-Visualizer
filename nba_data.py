from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.endpoints import leaguedashteamstats, leaguedashplayerstats
from nba_api.stats.static import teams
import pandas as pd
import streamlit as st
import time

# stats.nba.comへのアクセス用ヘッダー設定（タイムアウト/ブロック回避）
custom_headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://stats.nba.com/',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
}
NBAStatsHTTP.get_headers = lambda self: custom_headers

# データ取得処理を関数として分離し、Streamlitのキャッシュを適用
@st.cache_data(ttl=3600)
def fetch_team_ratings(season):
    """チームのレーティングデータを取得（キャッシュ対応・リトライ付き）"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # measure_type_detailed_defense='Advanced'を指定してOffRtg/DefRtgを取得
            stats = leaguedashteamstats.LeagueDashTeamStats(
                season=season,
                measure_type_detailed_defense='Advanced',
                league_id_nullable='00'
            )
            return stats.get_data_frames()[0]
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2) # 待機時間を設けてリトライ
                continue
            st.error(f"データ取得エラー (Team): {str(e)}")
            return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def fetch_player_ratings(season, min_games):
    """選手のレーティングデータを取得（キャッシュ対応・リトライ付き）"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                measure_type_detailed_defense='Advanced',
                league_id_nullable='00'
            )
            df = stats.get_data_frames()[0]
            # 試合数フィルター
            return df[df['GP'] >= min_games]
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            st.error(f"データ取得エラー (Player): {str(e)}")
            return pd.DataFrame()
    return pd.DataFrame()

class NBADataManager:
    def __init__(self):
        self.season = "2025-26" # 今シーズンの想定（必要に応じて変更）
        self._teams = teams.get_teams()
        
    def get_team_id(self, team_name):
        """チーム名からチームIDを取得"""
        team = next((team for team in self._teams if team['full_name'] == team_name), None)
        return team['id'] if team else None
        
    def get_team_ratings(self):
        """チームのレーティングデータを取得"""
        df = fetch_team_ratings(self.season)
        
        if df.empty:
            return pd.DataFrame(columns=['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING'])
            
        # 必要なカラムが存在するか確認
        cols = ['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
        available_cols = [c for c in cols if c in df.columns]
        return df[available_cols]
    
    def get_player_ratings(self, team_name=None, min_games=20):
        """選手のレーティングデータを取得"""
        df = fetch_player_ratings(self.season, min_games)
        
        if df.empty:
            return pd.DataFrame()
            
        if team_name:
            team_id = self.get_team_id(team_name)
            if team_id:
                df = df[df['TEAM_ID'] == team_id]
            else:
                st.warning(f"チーム '{team_name}' が見つかりませんでした。")
                return pd.DataFrame()
        
        cols = ['PLAYER_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'GP']
        available_cols = [c for c in cols if c in df.columns]
        return df[available_cols]
    
    def search_players(self, player_names):
        """選手名で検索"""
        all_players = self.get_player_ratings(min_games=1) # 検索時は全選手対象にするためmin_gamesを下げる
        if all_players.empty:
            return pd.DataFrame()

        matched_dfs = []
        # 空の検索語を除外
        valid_names = [name for name in player_names if name]
        
        for name in valid_names:
            matched = all_players[all_players['PLAYER_NAME'].str.contains(name, case=False, na=False)]
            matched_dfs.append(matched)
                
        if not matched_dfs:
            return pd.DataFrame()
            
        # 結合して重複を排除
        return pd.concat(matched_dfs).drop_duplicates()
