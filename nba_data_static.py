from nba_api.stats.static import teams
import pandas as pd
import streamlit as st
import os

class NBADataManager:
    def __init__(self, use_static_data=True):
        """
        Args:
            use_static_data: Trueの場合、CSVファイルからデータを読み込む（Streamlit Cloud用）
                           Falseの場合、APIから直接取得（ローカル開発用）
        """
        self.use_static_data = use_static_data
        self.season = "2025-26"
        self._teams = teams.get_teams()
        
        if use_static_data:
            self._load_static_data()
    
    def _load_static_data(self):
        """CSVファイルからデータを読み込む"""
        try:
            self.team_ratings_cache = pd.read_csv('data/team_ratings.csv')
            self.player_ratings_cache = pd.read_csv('data/player_ratings.csv')
            
            # 更新日時を読み込む
            if os.path.exists('data/last_updated.txt'):
                with open('data/last_updated.txt', 'r') as f:
                    self.last_updated = f.read().strip()
            else:
                self.last_updated = "不明"
        except Exception as e:
            st.error(f"データファイルの読み込みエラー: {e}")
            self.team_ratings_cache = pd.DataFrame()
            self.player_ratings_cache = pd.DataFrame()
            self.last_updated = "エラー"
    
    def get_team_id(self, team_name):
        """チーム名からチームIDを取得"""
        team = next((team for team in self._teams if team['full_name'] == team_name), None)
        return team['id'] if team else None
    
    def get_team_ratings(self):
        """チームのレーティングデータを取得"""
        if self.use_static_data:
            return self.team_ratings_cache.copy()
        else:
            # APIから取得（ローカル開発用）
            from nba_data_api import fetch_team_ratings
            df = fetch_team_ratings(self.season)
            if df.empty:
                return pd.DataFrame(columns=['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING'])
            cols = ['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
            available_cols = [c for c in cols if c in df.columns]
            return df[available_cols]
    
    def get_player_ratings(self, team_name=None, min_games=20):
        """選手のレーティングデータを取得"""
        if self.use_static_data:
            df = self.player_ratings_cache.copy()
        else:
            # APIから取得（ローカル開発用）
            from nba_data_api import fetch_player_ratings
            df = fetch_player_ratings(self.season, min_games)
        
        if df.empty:
            return pd.DataFrame()
        
        # 試合数フィルター
        if 'GP' in df.columns:
            df = df[df['GP'] >= min_games]
        
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
        all_players = self.get_player_ratings(min_games=1)
        if all_players.empty:
            return pd.DataFrame()

        matched_dfs = []
        valid_names = [name for name in player_names if name]
        
        for name in valid_names:
            matched = all_players[all_players['PLAYER_NAME'].str.contains(name, case=False, na=False)]
            matched_dfs.append(matched)
        
        if not matched_dfs:
            return pd.DataFrame()
        
        return pd.concat(matched_dfs).drop_duplicates()
    
    def get_last_updated(self):
        """データの最終更新日時を取得"""
        if self.use_static_data:
            return self.last_updated
        else:
            return "リアルタイム"
