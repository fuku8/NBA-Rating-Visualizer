import streamlit as st

def display_team_ratings(nba_manager):
    """チームレーティングの表示"""
    team_ratings = nba_manager.get_team_ratings()

    if not team_ratings.empty:
        # ソート機能
        col1, col2 = st.columns([3, 1])
        with col1:
            sort_column = st.selectbox(
                "並び替え",
                options=team_ratings.columns.tolist(),
                key="team_ratings_sort_col"
            )
        with col2:
            sort_order = st.radio("順序", ["降順", "昇順"], horizontal=True, key="team_ratings_sort_order")

        # ソート実行
        ascending = (sort_order == "昇順")
        team_ratings_sorted = team_ratings.sort_values(by=sort_column, ascending=ascending)

        # ソート後に行数番号列を追加
        team_ratings_sorted.insert(0, 'No.', range(1, len(team_ratings_sorted) + 1))

        st.dataframe(
            team_ratings_sorted,
            use_container_width=True,
            hide_index=True,
            column_config={
                "No.": st.column_config.NumberColumn("No.", width="small"),
                "OFF_RATING": st.column_config.NumberColumn("Off Rtg", format="%.1f"),
                "DEF_RATING": st.column_config.NumberColumn("Def Rtg", format="%.1f"),
                "NET_RATING": st.column_config.NumberColumn("Net Rtg", format="%.1f"),
            }
        )
    else:
        st.warning("表示できるチームデータがありません。")

def display_team_players(nba_manager):
    """チーム別選手レーティングの表示"""
    try:
        teams = [team['full_name'] for team in nba_manager._teams]
        selected_team = st.selectbox("チームを選択", teams)

        if selected_team:
            team_players = nba_manager.get_player_ratings(team_name=selected_team)

            if not team_players.empty:
                # ソート機能
                col1, col2 = st.columns([3, 1])
                with col1:
                    sort_column = st.selectbox(
                        "並び替え",
                        options=team_players.columns.tolist(),
                        key="team_players_sort_col"
                    )
                with col2:
                    sort_order = st.radio("順序", ["降順", "昇順"], horizontal=True, key="team_players_sort_order")

                # ソート実行
                ascending = (sort_order == "昇順")
                team_players_sorted = team_players.sort_values(by=sort_column, ascending=ascending)

                # ソート後に行数番号列を追加
                team_players_sorted.insert(0, 'No.', range(1, len(team_players_sorted) + 1))

                st.dataframe(
                    team_players_sorted,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "No.": st.column_config.NumberColumn("No.", width="small"),
                        "OFF_RATING": st.column_config.NumberColumn("Off Rtg", format="%.1f"),
                        "DEF_RATING": st.column_config.NumberColumn("Def Rtg", format="%.1f"),
                        "NET_RATING": st.column_config.NumberColumn("Net Rtg", format="%.1f"),
                    }
                )
            else:
                st.warning(f"{selected_team}の選手データが見つかりませんでした。")
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def display_player_search(nba_manager):
    """選手検索機能の表示"""
    st.info("選手名の一部を入力してください（複数入力可）")

    # UI改善: 検索フォームをまとめる
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        name1 = col1.text_input("選手名 1")
        name2 = col2.text_input("選手名 2")
        submit = st.form_submit_button("検索")

    search_names = [name1, name2]

    if submit and any(search_names):
        results = nba_manager.search_players(search_names)

        if not results.empty:
            # ソート機能
            col1, col2 = st.columns([3, 1])
            with col1:
                sort_column = st.selectbox(
                    "並び替え",
                    options=results.columns.tolist(),
                    key="player_search_sort_col"
                )
            with col2:
                sort_order = st.radio("順序", ["降順", "昇順"], horizontal=True, key="player_search_sort_order")

            # ソート実行
            ascending = (sort_order == "昇順")
            results_sorted = results.sort_values(by=sort_column, ascending=ascending)

            # ソート後に行数番号列を追加
            results_sorted.insert(0, 'No.', range(1, len(results_sorted) + 1))

            st.dataframe(
                results_sorted,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "No.": st.column_config.NumberColumn("No.", width="small"),
                }
            )
        else:
            st.warning("該当する選手が見つかりませんでした。")

def display_all_players(nba_manager):
    """全選手レーティングの表示"""
    # 全選手表示は重いため、注意書きを入れるか、ページネーション的な工夫があると良いが、一旦そのまま表示
    st.warning("注: 全選手のデータを取得・表示するため時間がかかる場合があります。")
    all_players = nba_manager.get_player_ratings(min_games=20)

    if not all_players.empty:
        # ソート機能
        col1, col2 = st.columns([3, 1])
        with col1:
            sort_column = st.selectbox(
                "並び替え",
                options=all_players.columns.tolist(),
                key="all_players_sort_col"
            )
        with col2:
            sort_order = st.radio("順序", ["降順", "昇順"], horizontal=True, key="all_players_sort_order")

        # ソート実行
        ascending = (sort_order == "昇順")
        all_players_sorted = all_players.sort_values(by=sort_column, ascending=ascending)

        # ソート後に行数番号列を追加
        all_players_sorted.insert(0, 'No.', range(1, len(all_players_sorted) + 1))

        st.dataframe(
            all_players_sorted,
            use_container_width=True,
            hide_index=True,
            column_config={
                "No.": st.column_config.NumberColumn("No.", width="small"),
                "OFF_RATING": st.column_config.NumberColumn("Off Rtg", format="%.1f"),
                "DEF_RATING": st.column_config.NumberColumn("Def Rtg", format="%.1f"),
                "NET_RATING": st.column_config.NumberColumn("Net Rtg", format="%.1f"),
            }
        )