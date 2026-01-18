import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

def display_team_ratings(nba_manager):
    """チームレーティングの表示"""
    team_ratings = nba_manager.get_team_ratings()

    if not team_ratings.empty:
        # 行番号列を先頭に追加
        team_ratings.insert(0, 'No.', range(1, len(team_ratings) + 1))

        # AG Grid設定
        gb = GridOptionsBuilder.from_dataframe(team_ratings)

        # 行番号列の設定（ソート後も1から順に表示）
        row_number_jscode = JsCode("""
        function(params) {
            return params.node.rowIndex + 1;
        }
        """)

        gb.configure_column(
            "No.",
            headerName="No.",
            valueGetter=row_number_jscode,
            lockPosition=True,
            sortable=False,
            width=80,
            suppressMovable=True
        )

        # 他の列の設定
        gb.configure_default_column(sortable=True, filterable=True)

        # 数値フォーマット設定
        gb.configure_column("OFF_RATING", header_name="Off Rtg", type=["numericColumn"], precision=1)
        gb.configure_column("DEF_RATING", header_name="Def Rtg", type=["numericColumn"], precision=1)
        gb.configure_column("NET_RATING", header_name="Net Rtg", type=["numericColumn"], precision=1)

        gridOptions = gb.build()

        AgGrid(
            team_ratings,
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.NO_UPDATE,
            fit_columns_on_grid_load=True,
            height=500,
            enable_enterprise_modules=False,
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
                # 行番号列を先頭に追加
                team_players.insert(0, 'No.', range(1, len(team_players) + 1))

                # AG Grid設定
                gb = GridOptionsBuilder.from_dataframe(team_players)

                # 行番号列の設定（ソート後も1から順に表示）
                row_number_jscode = JsCode("""
                function(params) {
                    return params.node.rowIndex + 1;
                }
                """)

                gb.configure_column(
                    "No.",
                    headerName="No.",
                    valueGetter=row_number_jscode,
                    lockPosition=True,
                    sortable=False,
                    width=80,
                    suppressMovable=True
                )

                # 他の列の設定
                gb.configure_default_column(sortable=True, filterable=True)

                # 数値フォーマット設定
                gb.configure_column("OFF_RATING", header_name="Off Rtg", type=["numericColumn"], precision=1)
                gb.configure_column("DEF_RATING", header_name="Def Rtg", type=["numericColumn"], precision=1)
                gb.configure_column("NET_RATING", header_name="Net Rtg", type=["numericColumn"], precision=1)

                gridOptions = gb.build()

                AgGrid(
                    team_players,
                    gridOptions=gridOptions,
                    update_mode=GridUpdateMode.NO_UPDATE,
                    fit_columns_on_grid_load=True,
                    height=500,
                    enable_enterprise_modules=False,
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
            # 行番号列を先頭に追加
            results.insert(0, 'No.', range(1, len(results) + 1))

            # AG Grid設定
            gb = GridOptionsBuilder.from_dataframe(results)

            # 行番号列の設定（ソート後も1から順に表示）
            row_number_jscode = JsCode("""
            function(params) {
                return params.node.rowIndex + 1;
            }
            """)

            gb.configure_column(
                "No.",
                headerName="No.",
                valueGetter=row_number_jscode,
                lockPosition=True,
                sortable=False,
                width=80,
                suppressMovable=True
            )

            # 他の列の設定
            gb.configure_default_column(sortable=True, filterable=True)

            gridOptions = gb.build()

            AgGrid(
                results,
                gridOptions=gridOptions,
                update_mode=GridUpdateMode.NO_UPDATE,
                fit_columns_on_grid_load=True,
                height=500,
                enable_enterprise_modules=False,
            )
        else:
            st.warning("該当する選手が見つかりませんでした。")

def display_all_players(nba_manager):
    """全選手レーティングの表示"""
    # 全選手表示は重いため、注意書きを入れるか、ページネーション的な工夫があると良いが、一旦そのまま表示
    st.warning("注: 全選手のデータを取得・表示するため時間がかかる場合があります。")
    all_players = nba_manager.get_player_ratings(min_games=20)

    if not all_players.empty:
        # 行番号列を先頭に追加
        all_players.insert(0, 'No.', range(1, len(all_players) + 1))

        # AG Grid設定
        gb = GridOptionsBuilder.from_dataframe(all_players)

        # 行番号列の設定（ソート後も1から順に表示）
        row_number_jscode = JsCode("""
        function(params) {
            return params.node.rowIndex + 1;
        }
        """)

        gb.configure_column(
            "No.",
            headerName="No.",
            valueGetter=row_number_jscode,
            lockPosition=True,
            sortable=False,
            width=80,
            suppressMovable=True
        )

        # 他の列の設定
        gb.configure_default_column(sortable=True, filterable=True)

        # 数値フォーマット設定
        gb.configure_column("OFF_RATING", header_name="Off Rtg", type=["numericColumn"], precision=1)
        gb.configure_column("DEF_RATING", header_name="Def Rtg", type=["numericColumn"], precision=1)
        gb.configure_column("NET_RATING", header_name="Net Rtg", type=["numericColumn"], precision=1)

        gridOptions = gb.build()

        AgGrid(
            all_players,
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.NO_UPDATE,
            fit_columns_on_grid_load=True,
            height=500,
            enable_enterprise_modules=False,
        )