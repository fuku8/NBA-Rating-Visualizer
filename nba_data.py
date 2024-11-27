from nba_api.stats.endpoints import leaguedashteamstats, leaguedashplayerstats
from nba_api.stats.static import teams
from cache_manager import cache_data
import pandas as pd
import streamlit as st

class NBADataManager:
    def __init__(self):
        self.season = "2024-25"
        self._teams = teams.get_teams()
        
    def get_team_id(self, team_name):
        """チーム名からチームIDを取得"""
        try:
            team = next((team for team in self._teams if team['full_name'] == team_name), None)
            return team['id'] if team else None
        except Exception as e:
            st.error(f"チームIDの取得に失敗しました: {str(e)}")
            return None
        
    @cache_data(expire_time=3600)  # 1時間キャッシュ
    def get_team_ratings(self):
        """チームのレーティングデータを取得"""
        try:
            team_stats = leaguedashteamstats.LeagueDashTeamStats(
                season=self.season,
                measure_type_detailed_defense='Advanced'
            ).get_data_frames()[0]
            
            if team_stats.empty:
                st.error("チームデータの取得に失敗しました。")
                return pd.DataFrame(columns=['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING'])
            
            return team_stats[['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']]
        except Exception as e:
            st.error(f"チームデータの取得中にエラーが発生しました: {str(e)}")
            return pd.DataFrame(columns=['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING'])
    
    @cache_data(expire_time=3600)
    def get_player_ratings(self, team_name=None, min_games=5):
        """選手のレーティングデータを取得"""
        try:
            player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=self.season,
                measure_type_detailed_defense='Advanced'
            ).get_data_frames()[0]
            
            # 5試合以上出場選手でフィルター
            filtered_stats = player_stats[player_stats['GP'] >= min_games]
            
            if team_name:
                team_id = self.get_team_id(team_name)
                if team_id:
                    filtered_stats = filtered_stats[filtered_stats['TEAM_ID'] == team_id]
                else:
                    raise ValueError(f"チーム '{team_name}' が見つかりませんでした。")
            
            return filtered_stats[['PLAYER_NAME', 'TEAM_ABBREVIATION', 
                                'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'GP']]
                                
        except Exception as e:
            st.error(f"選手データの取得に失敗しました: {str(e)}")
            return pd.DataFrame()
    
    def search_players(self, player_names):
        """選手名で検索"""
        all_players = self.get_player_ratings()
        result = pd.DataFrame()
        
        for name in player_names:
            if name:
                matched = all_players[all_players['PLAYER_NAME'].str.contains(name, case=False)]
                result = pd.concat([result, matched])
                
        return result
