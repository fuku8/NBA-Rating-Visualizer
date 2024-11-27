import streamlit as st
from utils import sort_dataframe

def display_team_ratings(nba_manager):
    """チームレーティングの表示"""
    team_ratings = nba_manager.get_team_ratings()
    
    # ソート用のボタン
    cols = st.columns(4)
    sort_col = None
    if cols[1].button("OFF RATING"):
        sort_col = "OFF_RATING"
    elif cols[2].button("DEF RATING"):
        sort_col = "DEF_RATING"
    elif cols[3].button("NET RATING"):
        sort_col = "NET_RATING"
        
    # データのソートと表示
    sorted_ratings = sort_dataframe(team_ratings, sort_col)
    st.dataframe(sorted_ratings, use_container_width=True)

def display_team_players(nba_manager):
    """チーム別選手レーティングの表示"""
    teams = nba_manager.get_team_ratings()['TEAM_NAME'].tolist()
    selected_team = st.selectbox("チームを選択", teams)
    
    if selected_team:
        team_players = nba_manager.get_player_ratings(selected_team)
        
        # ソート用のボタン
        cols = st.columns(4)
        sort_col = None
        if cols[1].button("OFF RATING"):
            sort_col = "OFF_RATING"
        elif cols[2].button("DEF RATING"):
            sort_col = "DEF_RATING"
        elif cols[3].button("NET RATING"):
            sort_col = "NET_RATING"
            
        # データのソートと表示
        sorted_players = sort_dataframe(team_players, sort_col)
        st.dataframe(sorted_players, use_container_width=True)

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
        
        # ソート用のボタン
        cols = st.columns(4)
        sort_col = None
        if cols[1].button("OFF RATING"):
            sort_col = "OFF_RATING"
        elif cols[2].button("DEF RATING"):
            sort_col = "DEF_RATING"
        elif cols[3].button("NET RATING"):
            sort_col = "NET_RATING"
            
        # データのソートと表示
        sorted_results = sort_dataframe(results, sort_col)
        st.dataframe(sorted_results, use_container_width=True)

def display_all_players(nba_manager):
    """全選手レーティングの表示"""
    all_players = nba_manager.get_player_ratings(min_games=5)
    
    # ソート用のボタン
    cols = st.columns(4)
    sort_col = None
    if cols[1].button("OFF RATING"):
        sort_col = "OFF_RATING"
    elif cols[2].button("DEF RATING"):
        sort_col = "DEF_RATING"
    elif cols[3].button("NET RATING"):
        sort_col = "NET_RATING"
        
    # データのソートと表示
    sorted_players = sort_dataframe(all_players, sort_col)
    st.dataframe(sorted_players, use_container_width=True)
