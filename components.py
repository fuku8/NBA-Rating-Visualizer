import streamlit as st
from utils import sort_dataframe

def display_team_ratings(nba_manager):
    """チームレーティングの表示"""
    team_ratings = nba_manager.get_team_ratings()
    
    # データの表示
    if not team_ratings.empty:
        sorted_ratings = sort_dataframe(team_ratings, None)
        st.dataframe(sorted_ratings, use_container_width=True)
    else:
        st.warning("表示できるチームデータがありません。")

def display_team_players(nba_manager):
    """チーム別選手レーティングの表示"""
    try:
        # チーム一覧を取得
        teams = [team['full_name'] for team in nba_manager._teams]
        selected_team = st.selectbox("チームを選択", teams)
        
        if selected_team:
            try:
                team_players = nba_manager.get_player_ratings(team_name=selected_team)
                
                # データの表示
                if not team_players.empty:
                    sorted_players = sort_dataframe(team_players, None)
                    st.dataframe(sorted_players, use_container_width=True)
                else:
                    st.warning(f"{selected_team}の選手データが見つかりませんでした。")
            except Exception as e:
                st.error(f"選手データの取得に失敗しました: {str(e)}")
    except Exception as e:
        st.error(f"チーム一覧の取得に失敗しました: {str(e)}")

def display_player_search(nba_manager):
    """選手検索機能の表示"""
    # 5つの検索フォーム
    search_names = []
    cols = st.columns(5)
    for i in range(5):
        search_names.append(cols[i].text_input(f"選手名 {i+1}"))
        
    # 検索実行
    if any(search_names):
        results = nba_manager.search_players(search_names)
        
        # データの表示
        sorted_results = sort_dataframe(results, None)
        st.dataframe(sorted_results, use_container_width=True)

def display_all_players(nba_manager):
    """全選手レーティングの表示"""
    all_players = nba_manager.get_player_ratings(min_games=20)
    
    # データの表示
    sorted_players = sort_dataframe(all_players, None)
    st.dataframe(sorted_players, use_container_width=True)