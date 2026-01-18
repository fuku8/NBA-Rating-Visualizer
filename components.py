import streamlit as st

def display_team_ratings(nba_manager):
    """チームレーティングの表示"""
    team_ratings = nba_manager.get_team_ratings()

    if not team_ratings.empty:
        # session_stateの初期化
        if 'team_ratings_sort_col' not in st.session_state:
            st.session_state.team_ratings_sort_col = team_ratings.columns[0]
        if 'team_ratings_ascending' not in st.session_state:
            st.session_state.team_ratings_ascending = False

        # ソート機能
        st.write("**並び替え列を選択:**")
        sort_column = st.radio(
            "並び替え列",
            options=team_ratings.columns.tolist(),
            horizontal=True,
            key="team_ratings_radio",
            label_visibility="collapsed"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("降順", key="team_ratings_desc", use_container_width=True):
                st.session_state.team_ratings_sort_col = sort_column
                st.session_state.team_ratings_ascending = False
        with col2:
            if st.button("昇順", key="team_ratings_asc", use_container_width=True):
                st.session_state.team_ratings_sort_col = sort_column
                st.session_state.team_ratings_ascending = True

        # ソート実行
        team_ratings_sorted = team_ratings.sort_values(
            by=st.session_state.team_ratings_sort_col,
            ascending=st.session_state.team_ratings_ascending
        )

        # ソート後に行数番号列を追加
        team_ratings_sorted.insert(0, 'No.', range(1, len(team_ratings_sorted) + 1))

        # 数値フォーマットを適用
        for col in ['OFF_RATING', 'DEF_RATING', 'NET_RATING']:
            if col in team_ratings_sorted.columns:
                team_ratings_sorted[col] = team_ratings_sorted[col].apply(lambda x: f"{x:.1f}")

        # 列名を変更
        team_ratings_sorted = team_ratings_sorted.rename(columns={
            'OFF_RATING': 'Off Rtg',
            'DEF_RATING': 'Def Rtg',
            'NET_RATING': 'Net Rtg'
        })

        st.table(team_ratings_sorted.set_index('No.'))
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
                # session_stateの初期化
                if 'team_players_sort_col' not in st.session_state:
                    st.session_state.team_players_sort_col = team_players.columns[0]
                if 'team_players_ascending' not in st.session_state:
                    st.session_state.team_players_ascending = False

                # ソート機能
                st.write("**並び替え列を選択:**")
                sort_column = st.radio(
                    "並び替え列",
                    options=team_players.columns.tolist(),
                    horizontal=True,
                    key="team_players_radio",
                    label_visibility="collapsed"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("降順", key="team_players_desc", use_container_width=True):
                        st.session_state.team_players_sort_col = sort_column
                        st.session_state.team_players_ascending = False
                with col2:
                    if st.button("昇順", key="team_players_asc", use_container_width=True):
                        st.session_state.team_players_sort_col = sort_column
                        st.session_state.team_players_ascending = True

                # ソート実行
                team_players_sorted = team_players.sort_values(
                    by=st.session_state.team_players_sort_col,
                    ascending=st.session_state.team_players_ascending
                )

                # ソート後に行数番号列を追加
                team_players_sorted.insert(0, 'No.', range(1, len(team_players_sorted) + 1))

                # 数値フォーマットを適用
                for col in ['OFF_RATING', 'DEF_RATING', 'NET_RATING']:
                    if col in team_players_sorted.columns:
                        team_players_sorted[col] = team_players_sorted[col].apply(lambda x: f"{x:.1f}")

                # 列名を変更
                team_players_sorted = team_players_sorted.rename(columns={
                    'OFF_RATING': 'Off Rtg',
                    'DEF_RATING': 'Def Rtg',
                    'NET_RATING': 'Net Rtg'
                })

                st.table(team_players_sorted.set_index('No.'))
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
            # session_stateの初期化
            if 'player_search_sort_col' not in st.session_state:
                st.session_state.player_search_sort_col = results.columns[0]
            if 'player_search_ascending' not in st.session_state:
                st.session_state.player_search_ascending = False

            # ソート機能
            st.write("**並び替え列を選択:**")
            sort_column = st.radio(
                "並び替え列",
                options=results.columns.tolist(),
                horizontal=True,
                key="player_search_radio",
                label_visibility="collapsed"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("降順", key="player_search_desc", use_container_width=True):
                    st.session_state.player_search_sort_col = sort_column
                    st.session_state.player_search_ascending = False
            with col2:
                if st.button("昇順", key="player_search_asc", use_container_width=True):
                    st.session_state.player_search_sort_col = sort_column
                    st.session_state.player_search_ascending = True

            # ソート実行
            results_sorted = results.sort_values(
                by=st.session_state.player_search_sort_col,
                ascending=st.session_state.player_search_ascending
            )

            # ソート後に行数番号列を追加
            results_sorted.insert(0, 'No.', range(1, len(results_sorted) + 1))

            # 数値フォーマットを適用
            for col in ['OFF_RATING', 'DEF_RATING', 'NET_RATING']:
                if col in results_sorted.columns:
                    results_sorted[col] = results_sorted[col].apply(lambda x: f"{x:.1f}")

            # 列名を変更
            results_sorted = results_sorted.rename(columns={
                'OFF_RATING': 'Off Rtg',
                'DEF_RATING': 'Def Rtg',
                'NET_RATING': 'Net Rtg'
            })

            st.table(results_sorted.set_index('No.'))
        else:
            st.warning("該当する選手が見つかりませんでした。")

def display_all_players(nba_manager):
    """全選手レーティングの表示"""
    # 全選手表示は重いため、注意書きを入れるか、ページネーション的な工夫があると良いが、一旦そのまま表示
    st.warning("注: 全選手のデータを取得・表示するため時間がかかる場合があります。")
    all_players = nba_manager.get_player_ratings(min_games=20)

    if not all_players.empty:
        # session_stateの初期化
        if 'all_players_sort_col' not in st.session_state:
            st.session_state.all_players_sort_col = all_players.columns[0]
        if 'all_players_ascending' not in st.session_state:
            st.session_state.all_players_ascending = False

        # ソート機能
        st.write("**並び替え列を選択:**")
        sort_column = st.radio(
            "並び替え列",
            options=all_players.columns.tolist(),
            horizontal=True,
            key="all_players_radio",
            label_visibility="collapsed"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("降順", key="all_players_desc", use_container_width=True):
                st.session_state.all_players_sort_col = sort_column
                st.session_state.all_players_ascending = False
        with col2:
            if st.button("昇順", key="all_players_asc", use_container_width=True):
                st.session_state.all_players_sort_col = sort_column
                st.session_state.all_players_ascending = True

        # ソート実行
        all_players_sorted = all_players.sort_values(
            by=st.session_state.all_players_sort_col,
            ascending=st.session_state.all_players_ascending
        )

        # ソート後に行数番号列を追加
        all_players_sorted.insert(0, 'No.', range(1, len(all_players_sorted) + 1))

        # 数値フォーマットを適用
        for col in ['OFF_RATING', 'DEF_RATING', 'NET_RATING']:
            if col in all_players_sorted.columns:
                all_players_sorted[col] = all_players_sorted[col].apply(lambda x: f"{x:.1f}")

        # 列名を変更
        all_players_sorted = all_players_sorted.rename(columns={
            'OFF_RATING': 'Off Rtg',
            'DEF_RATING': 'Def Rtg',
            'NET_RATING': 'Net Rtg'
        })

        st.table(all_players_sorted.set_index('No.'))
