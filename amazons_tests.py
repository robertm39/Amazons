# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:47:14 2020

@author: rober
"""

def print_board(board, fancy_symbols=True):
    if fancy_symbols:
        white = '○'
        black = '●'
        fire = 'X'
    else:
        white = 'W'
        black = 'B'
        fire = 'X'
    empty = ' '
    
    w, h = board.shape[0], board.shape[1]
    
    print(' ' + '#'*w + ' ')
          
    for y in range(0, h):
        print('#', end='')
        for x in range(0, w):
            square = board[x, y, :]
            
            if square[0] == 1: #White is on the square
                print(white, end='')
            elif square[1] == 1: #Black is on the square
                print(black, end='')
            elif square[2] == 1: #The square is on fire
                print(fire, end='')
            elif square[3] == 1: #The square is empty
                print(empty, end='')
            else: #something is wrong
                print('?', end='')
        print('#')
    
    print(' ' + '#'*w + ' ')
                