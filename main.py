import streamlit as st
from nba_data_static import NBADataManager
from components import (
    display_team_ratings,
    display_team_players,
    display_player_search,
    display_all_players
)
from utils import setup_page

def main():
    # ページの初期設定
    setup_page()
    
    # NBA データマネージャーのインスタンス化（静的データを使用）
    nba_manager = NBADataManager(use_static_data=True)
    
    # データ更新日時を表示
    st.sidebar.info(f"📅 データ更新日時: {nba_manager.get_last_updated()}")
    
    # ページ選択を上部に移動
    page = st.selectbox(
        "ページを選択",
        ["チームレーティング", "チーム別選手", "選手検索", "全選手レーティング"]
    )
    
    # ページ表示
    if page == "チームレーティング":
        st.header("チームレーティング一覧")
        display_team_ratings(nba_manager)
        
    elif page == "チーム別選手":
        st.header("チーム別選手レーティング")
        display_team_players(nba_manager)
        
    elif page == "選手検索":
        st.header("選手検索")
        display_player_search(nba_manager)
        
    else:
        st.header("全選手レーティング")
        display_all_players(nba_manager)

if __name__ == "__main__":
    main()
