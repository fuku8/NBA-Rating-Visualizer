# NBA Rating Visualizer

NBAチームと選手のレーティング（オフェンス・ディフェンス・ネット）を可視化するStreamlitアプリケーション。

## 特徴

- **チームレーティング**: 全30チームのオフェンス/ディフェンス/ネットレーティングを表示
- **チーム別選手**: 各チームの選手レーティングを表示
- **選手検索**: 選手名で検索してレーティングを確認
- **全選手レーティング**: 全選手のレーティング一覧（最低出場試合数でフィルタリング可能）

## データ更新

このアプリは静的データ方式を採用しています。データは以下の方法で自動更新されます：

### 自動更新（GitHub Actions）
- **毎日午前9時（日本時間）**に自動的にデータが更新されます
- GitHub Actionsが`fetch_data.py`を実行し、最新データを取得
- 更新されたデータは自動的にリポジトリにコミット・プッシュされます
- Streamlit Cloudが変更を検知して自動的に再デプロイします

### 手動更新
必要に応じて手動でデータを更新することも可能です：

```bash
# ローカルで実行
python fetch_data.py

# GitHubにプッシュ
git add data/
git commit -m "Update NBA data"
git push
```

または、GitHubのActionsタブから「Update NBA Data」ワークフローを手動実行できます。

## セットアップ

### ローカル環境

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 初回データ取得
python fetch_data.py

# アプリ起動
streamlit run main.py
```

### Streamlit Cloudへのデプロイ

1. このリポジトリをGitHubにプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス
3. リポジトリを選択してデプロイ
4. 自動的に`data/`ディレクトリのCSVファイルが読み込まれます

## 技術スタック

- **Streamlit**: Webアプリケーションフレームワーク
- **nba_api**: NBA公式データAPI
- **Pandas**: データ処理
- **GitHub Actions**: 自動データ更新

## ファイル構成

```
.
├── main.py                 # メインアプリケーション
├── nba_data_static.py      # 静的データマネージャー
├── components.py           # UI コンポーネント
├── utils.py               # ユーティリティ関数
├── fetch_data.py          # データ取得スクリプト
├── data/                  # データディレクトリ
│   ├── team_ratings.csv   # チームレーティングデータ
│   ├── player_ratings.csv # 選手レーティングデータ
│   └── last_updated.txt   # 最終更新日時
└── .github/
    └── workflows/
        └── update_data.yml # 自動更新ワークフロー
```

## ライセンス

MIT License
