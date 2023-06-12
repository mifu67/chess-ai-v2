#!/bin/sh
echo "base-minimax fancy-minimax"
python3 eval-chess.py base-minimax fancy-minimax 3
echo "fancy-minimax base-minimax"
python3 eval-chess.py fancy-minimax base-minimax 5
echo "baseline linear"
python3 eval-chess.py baseline linear-minimax 5
echo "linear baseline"
python3 eval-chess.py linear-minimax baseline 5
echo "baseline deep"
python3 eval-chess.py baseline deep-minimax 5
echo "deep baseline"
python3 eval-chess.py deep-minimax baseline 5
echo "base-minimax deep-only"
python3 eval-chess.py base-minimax deep-only 5
echo "deep-only base-minimax" 
python3 eval-chess.py deep-only base-minimax 5
echo "base-minimax linear"
python3 eval-chess.py base-minimax linear-minimax 5
echo "linear base-minimax"
python3 eval-chess.py linear-minimax base-minimax 5
echo "base-minimax deep"
python3 eval-chess.py base-minimax deep-minimax 5
echo "deep base-minimax"
python3 eval-chess.py deep-minimax base-minimax 5
echo "fancy-minimax linear-only"
python3 eval-chess.py fancy-minimax linear-only 5
echo "linear-only fancy-minimax"
python3 eval-chess.py linear-only fancy-minimax 5
echo "fancy-minimax deep-only"
python3 eval-chess.py fancy-minimax deep-only 5
echo "deep-only fancy-minimax"
python3 eval-chess.py deep-only fancy-minimax 5
echo "linear-only deep-only"
python3 eval-chess.py linear-only deep-only 5
echo "deep-only linear-only"
python3 eval-chess.py deep-only linear-only 5
