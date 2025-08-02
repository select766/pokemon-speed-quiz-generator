#!/usr/bin/env python3
import csv
import random
import sys
import argparse
from pathlib import Path


def load_base_stats(csv_path):
    """基本種族値CSVファイルを読み込み、ポケモンの情報を辞書のリストで返す"""
    pokemon_list = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # ポケモン名の処理：改行がある場合は改行前と後の部分を組み合わせる
            original_name = row['ポケモン']
            if '\n' in original_name:
                # 改行がある場合、改行前の基本名と改行後のフォーム名を結合
                name_parts = original_name.split('\n')
                pokemon_name = name_parts[0] + name_parts[1] if len(name_parts) > 1 else name_parts[0]
                base_name = name_parts[0]  # 改行前の基本名（マッチング用）
            else:
                pokemon_name = original_name
                base_name = original_name
            
            pokemon_list.append({
                'no': row['No.'],
                'name': pokemon_name,
                'base_name': base_name,  # マッチング用の基本名
                'original_name': original_name,  # 改行文字を含む元の名前
                'type1': row['タイプ1'],
                'type2': row['タイプ2'],
                'hp': int(row['HP']),
                'attack': int(row['攻撃']),
                'defense': int(row['防御']),
                'sp_attack': int(row['特攻']),
                'sp_defense': int(row['特防']),
                'speed': int(row['素早さ']),
                'total': int(row['合計'])
            })
    
    return pokemon_list


def load_ranking_pokemon(ranking_files, rank_limit=None):
    """ランキングファイルからポケモン名のセットを作成"""
    ranking_pokemon = set()
    
    for ranking_file in ranking_files:
        with open(ranking_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    rank = int(row[0])
                    pokemon_name = row[1].strip()
                    
                    # rank_limitが指定されている場合は、その順位以下のみを対象とする
                    if rank_limit is None or rank <= rank_limit:
                        ranking_pokemon.add(pokemon_name)
    
    return ranking_pokemon


def filter_pokemon_by_ranking(pokemon_list, ranking_pokemon):
    """ランキングに含まれるポケモンのみを抽出"""
    filtered_pokemon = []
    
    for pokemon in pokemon_list:
        # 基本名でマッチング（オーガポンなどの対応）
        if pokemon['base_name'] in ranking_pokemon:
            filtered_pokemon.append(pokemon)
    
    return filtered_pokemon


def generate_wrong_choices(correct_speed, all_speeds, num_choices=3):
    """正解以外の選択肢を生成"""
    # 正解以外の素早さ値を取得
    wrong_speeds = [speed for speed in all_speeds if speed != correct_speed]
    
    # ランダムに選択肢を選ぶ
    if len(wrong_speeds) >= num_choices:
        return random.sample(wrong_speeds, num_choices)
    else:
        # 選択肢が足りない場合は、可能な分だけ返す
        return wrong_speeds


def generate_quiz_data(pokemon_list):
    """クイズデータを生成"""
    quiz_data = []
    
    # 全ポケモンの素早さ値のリストを作成（重複除去）
    all_speeds = list(set(pokemon['speed'] for pokemon in pokemon_list))
    
    for pokemon in pokemon_list:
        # 問題文
        question = f"{pokemon['name']}の素早さ種族値"
        
        # 正解
        correct_answer = str(pokemon['speed'])
        
        # 不正解の選択肢を生成
        wrong_choices = generate_wrong_choices(pokemon['speed'], all_speeds)
        wrong_choices_str = ';'.join(map(str, wrong_choices))
        
        quiz_data.append({
            'question': question,
            'answers': correct_answer,
            'wrongChoices': wrong_choices_str,
            'explanation': '',
            'ordered': '',
            'generatedWrongChoices': ''
        })
    
    return quiz_data


def save_quiz_csv(quiz_data, output_file):
    """クイズデータを暗記メーカー形式のCSVファイルとして保存"""
    fieldnames = ['question', 'answers', 'wrongChoices', 'explanation', 'ordered', 'generatedWrongChoices']
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(quiz_data)


def main():
    parser = argparse.ArgumentParser(description='ポケモン素早さクイズジェネレーター')
    parser.add_argument('output', help='出力CSVファイル名')
    parser.add_argument('ranking_files', nargs='+', help='ランキングCSVファイル（複数可）')
    parser.add_argument('--base-stats', default='dataset/basic/base_stats.csv', 
                       help='基本種族値CSVファイル（デフォルト: dataset/basic/base_stats.csv）')
    parser.add_argument('--rank-limit', type=int, 
                       help='ランキングの指定順位までを対象とする')
    
    args = parser.parse_args()
    
    # 基本種族値データを読み込み
    print(f"基本種族値データを読み込み中: {args.base_stats}")
    pokemon_list = load_base_stats(args.base_stats)
    print(f"読み込んだポケモン数: {len(pokemon_list)}")
    
    # ランキングデータを読み込み
    print(f"ランキングデータを読み込み中: {args.ranking_files}")
    if args.rank_limit:
        print(f"ランキング制限: {args.rank_limit}位まで")
    ranking_pokemon = load_ranking_pokemon(args.ranking_files, args.rank_limit)
    print(f"ランキングに含まれるポケモン数: {len(ranking_pokemon)}")
    
    # ランキングに含まれるポケモンのみを抽出
    filtered_pokemon = filter_pokemon_by_ranking(pokemon_list, ranking_pokemon)
    print(f"クイズ対象ポケモン数: {len(filtered_pokemon)}")
    
    if not filtered_pokemon:
        print("エラー: クイズ対象となるポケモンが見つかりませんでした。")
        return 1
    
    # クイズデータを生成
    print("クイズデータを生成中...")
    quiz_data = generate_quiz_data(filtered_pokemon)
    
    # CSVファイルに保存
    print(f"クイズデータを保存中: {args.output}")
    save_quiz_csv(quiz_data, args.output)
    
    print(f"完了！{len(quiz_data)}問のクイズを生成しました。")
    return 0


if __name__ == '__main__':
    sys.exit(main())