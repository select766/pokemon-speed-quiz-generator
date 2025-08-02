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