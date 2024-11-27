from nba_api.stats.endpoints import leaguedashteamstats, leaguedashplayerstats
from cache_manager import cache_data
import pandas as pd

class NBADataManager:
    def __init__(self):
        self.season = "2023-24"
        
    @cache_data(expire_time=3600)  # 1時間キャッシュ
    def get_team_ratings(self):
        """チームのレーティングデータを取得"""
        team_stats = leaguedashteamstats.LeagueDashTeamStats(
            season=self.season,
            measure_type_detailed_defense='Advanced'
        ).get_data_frames()[0]
        
        return team_stats[['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']]
    
    @cache_data(expire_time=3600)
    def get_player_ratings(self, team_id=None, min_games=5):
        """選手のレーティングデータを取得"""
        player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=self.season,
            measure_type_detailed_defense='Advanced'
        ).get_data_frames()[0]
        
        # 5試合以上出場選手でフィルター
        filtered_stats = player_stats[player_stats['GP'] >= min_games]
        
        if team_id:
            filtered_stats = filtered_stats[filtered_stats['TEAM_ID'] == team_id]
            
        return filtered_stats[['PLAYER_NAME', 'TEAM_ABBREVIATION', 
                             'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'GP']]
    
    def search_players(self, player_names):
        """選手名で検索"""
        all_players = self.get_player_ratings()
        result = pd.DataFrame()
        
        for name in player_names:
            if name:
                matched = all_players[all_players['PLAYER_NAME'].str.contains(name, case=False)]
                result = pd.concat([result, matched])
                
        return result
