# NBA Rating Visualizer

NBAチームと選手のレーティング（オフェンス・ディフェンス・ネット）を可視化するStreamlitアプリケーション。

## 特徴

- **チームレーティング**: 全30チームのオフェンス/ディフェンス/ネットレーティングを表示
- **チーム別選手**: 各チームの選手レーティングを表示
- **選手検索**: 選手名で検索してレーティングを確認
- **全選手レーティング**: 全選手のレーティング一覧（最低出場試合数でフィルタリング可能）

## 統計指標について

このアプリは[Basketball Reference](https://www.basketball-reference.com/)からデータを取得しており、以下の統計指標を使用しています。

### チームデータ
- **ORtg (Offensive Rating)**: オフェンシブ・レーティング - 100ポゼッション当たりの得点。チームの攻撃効率を示す指標
- **DRtg (Defensive Rating)**: ディフェンシブ・レーティング - 100ポゼッション当たりの失点。チームの守備効率を示す指標（低いほど良い）
- **NRtg (Net Rating)**: ネット・レーティング - ORtgとDRtgの差（ORtg - DRtg）。チームの総合力を示す指標

### 選手データ
- **OWS (Offensive Win Shares)**: オフェンス勝利貢献値 - 選手の攻撃面でのチームの勝利への貢献度を数値化したもの
- **DWS (Defensive Win Shares)**: ディフェンス勝利貢献値 - 選手の守備面でのチームの勝利への貢献度を数値化したもの
- **WS (Win Shares)**: 勝利貢献値 - OWSとDWSの合計。選手の総合的な勝利への貢献度を示す指標
- **GP (Games Played)**: 出場試合数

**Win Sharesについて**: 1シーズンで約48のWin Sharesがリーグ全体に分配されます。優秀な選手は10以上のWSを記録し、MVPクラスの選手は15以上になることもあります。

## データ更新

このアプリは静的データ方式を採用しています。データは以下の方法で自動更新されます：

### 自動更新（GitHub Actions）
- **毎日午後4時（日本時間）**に自動的にデータが更新されます
- GitHub Actionsが`fetch_data.py`を実行し、Basketball Referenceから最新データを取得
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
- **Basketball Reference**: NBAデータソース（スクレイピング）
- **Pandas**: データ処理とHTML解析
- **lxml / html5lib**: HTMLパーサー
- **GitHub Actions**: 自動データ更新

## ファイル構成

```
.
├── main.py                 # メインアプリケーション
├── nba_data_static.py      # 静的データマネージャー
├── components.py           # UI コンポーネント
├── utils.py               # ユーティリティ関数
├── fetch_data.py          # データ取得スクリプト（Basketball Reference）
├── data/                  # データディレクトリ
│   ├── team_ratings.csv   # チームレーティングデータ
│   ├── player_ratings.csv # 選手レーティングデータ
│   └── last_updated.txt   # 最終更新日時
└── .github/
    └── workflows/
        └── update_data.yml # 自動更新ワークフロー
```

## データソースの変更履歴

- **2026年1月**: NBA APIからBasketball Referenceに移行
  - 理由: NBA APIへのアクセス制限に対応
  - 変更点: 選手データの指標をRating系からWin Shares系に変更

## ライセンス

MIT License
