import streamlit as st

def setup_page():
    """ページの初期設定"""
    st.set_page_config(
        page_title="NBA選手・チーム分析ダッシュボード",
        page_icon="🏀",
        layout="wide"
    )
    
def sort_dataframe(df, col_name):
    """DataFrameのソート処理"""
    if 'sort_column' not in st.session_state:
        st.session_state.sort_column = None
        st.session_state.sort_ascending = False
        
    if col_name:
        if st.session_state.sort_column == col_name:
            st.session_state.sort_ascending = not st.session_state.sort_ascending
        else:
            st.session_state.sort_column = col_name
            st.session_state.sort_ascending = False
            
        return df.sort_values(
            by=st.session_state.sort_column,
            ascending=st.session_state.sort_ascending
        )
    return df
