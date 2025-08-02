# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pokémon speed quiz generator written in Python. The project is managed with `uv` and contains datasets for Pokémon base stats and competitive rankings.

## Development Commands

- **Run the main application**: `uv run main.py` or `python main.py`
- **Install dependencies**: `uv sync` (if dependencies are added to pyproject.toml)
- **Run with uv**: `uv run python main.py`

## Project Structure

- **main.py**: Entry point with basic "Hello World" implementation (currently minimal)
- **dataset/**: Contains Pokémon data in CSV format
  - **basic/base_stats.csv**: Complete Pokémon base stats (No., Name, Types, HP, Attack, Defense, Special Attack, Special Defense, Speed, Total)
  - **ranking/**: Competitive usage rankings by season (e.g., ranking_33_0.csv for season 33)
- **pyproject.toml**: Project configuration using uv package manager, requires Python >=3.12

## Data Format

The base stats CSV contains Japanese Pokémon names and uses the following columns:
- No., ポケモン (Pokémon name), タイプ1/タイプ2 (Types), HP, 攻撃 (Attack), 防御 (Defense), 特攻 (Special Attack), 特防 (Special Defense), 素早さ (Speed), 合計 (Total)

Ranking files contain popularity/usage data with Pokémon names in Japanese.

## Development Notes

- Project is in early development stage - main.py contains only a placeholder
- Uses uv for Python package management
- All data files use Japanese Pokémon names
- No external dependencies currently defined in pyproject.toml

# 目標

ポケモンの素早さクイズファイルを作成する。

## 成果物の例

「[暗記メーカー](https://ankimaker.com/)」で使えるCSVファイルを出力する。

```
question,answers,wrongChoices,explanation,ordered,generatedWrongChoices
ミライドンの素早さ種族値,135,80;140;102,,,
ライチュウの素早さ種族値,110,90;160;35,,,
ライチュウ(アローラのすがた)の素早さ種族値,110,80;20;35,,,
```

## クイズの内容

ポケモン種族名ごとの素早さ種族値を4択で答えさせる。

1つの数値が正解で、残り3つが不正解。不正解は、他のポケモンの種族値のうち、正解でないものをランダムに抽出。

## 生成元データ

`dataset/basic/base_stats.csv` が種族値を含むCSVファイル。

注意点として、ポケモン名に改行が含まれる場合がある。「コレクレー」について問題を作る場合、1行目の文字列に完全一致するエントリをすべて抽出する。そして、問題にする際は改行文字を削除する。問題「コレクレーはこフォルムの素早さ種族値」解答「10」問題「コレクレーとほフォルムの素早さ種族値」解答「80」のように、各エントリに対して別々のクイズを生成する。

```
No.,ポケモン,タイプ1,タイプ2,HP,攻撃,防御,特攻,特防,素早さ,合計
999,"コレクレー
はこフォルム",ゴースト,,45,30,70,75,70,10,300
999,"コレクレー
とほフォルム",ゴースト,,45,30,25,75,45,80,300
1000,サーフゴー,はがね,ゴースト,87,60,95,133,91,84,550
```

`dataset/ranking/ranking_*.csv` が、よく使用されるポケモンのリストで、この中に含まれるポケモンすべてを抽出する。ヘッダ行がなく、各行は `順位,ポケモン` を表す。

## 生成コマンド

```bash
uv run python generate_quiz.py OUTPUT INPUT...
```

実行例

```bash
uv run python generate_quiz.py quiz.csv dataset/ranking/ranking_33_*.csv
```

使用率ランキングは毎シーズン更新されるため、使用したいファイルをワイルドカードで指定する。
