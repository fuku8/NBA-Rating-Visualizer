import streamlit as st

def setup_page():
    """ページの初期設定"""
    st.set_page_config(
        page_title="NBA選手・チーム分析ダッシュボード",
        page_icon="🏀",
        layout="wide"
    )
