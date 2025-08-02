# ポケモンの素早さクイズ生成器

「[暗記メーカー](https://ankimaker.com/)」で使えるCSVファイルを出力する。

現在のところ、素早さ種族値を4択で聞くだけ。

## 生成ファイル例

CSVファイルのインポート機能を用いて暗記メーカーに読ませることができる。 https://ankimaker.com/howto/edit_csv

```csv
question,answers,wrongChoices,explanation,ordered,generatedWrongChoices
メタモンの素早さ種族値,48,30;148;60,,,
カイリューの素早さ種族値,80,120;97;101,,,
ドーブルの素早さ種族値,75,80;128;35,,,
ホウオウの素早さ種族値,90,100;138;101,,,
```

## 生成コマンド

```bash
uv run python generate_quiz.py OUTPUT INPUT... [--rank-limit LIMIT]
```

`--rank-limit`: ランキングの`LIMIT`位までを対象とする。

実行例

```bash
uv run python generate_quiz.py quiz.csv dataset/ranking/ranking_33_*.csv
```

使用率ランキングは毎シーズン更新されるため、使用したいファイルをワイルドカードで指定する。
