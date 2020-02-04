# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:08:00 2020

@author: rober
"""

from enum import Enum

import torch

class Mover(Enum):
    PLAYER = 'P'
    OPPONENT = 'O'

#Movers:
#O: opponent

def apply_moves(boards, moves):
    """
    Return the boards after the moves have been applied.
    
    Parameters:
        boards: The boards, in standard format [N, X, Y, 3]
        moves: The moves, in standard format [N, 6]
    """
    
    boards = boards.clone().detach() #Use a duplicate to avoid side effects
    
    for i in range(0, boards.shape[0]):#Unloop it later
        board = boards[i, :, :, :,]
        x_s, y_s, x_m, y_m, x_f, y_f = moves[i, :]
        
        #The data for the square the move starts from
        start_square = board[x_s, y_s, :]
        
        #Zero out the square being moved from
        board[x_s, y_s, :] = torch.tensor([0, 0, 0])
        
        #Now the final square will have the same data the start square had
        board[x_m, y_m, :] = start_square
        
        #Now the targeted square will be burning
        board[x_f, y_f, :] = torch.tensor([0, 0, 1])
        boards[i, :, :, :] = board
        
    return boards

def is_square_open(board, x, y):
    if x < 0 or y < 0:
        return False
    
    w, h = board.shape[1], board.shape[2]
    if x >= w or y >= h:
        return False
    
    square_open = True
    for i in (0, 1, 2): #Anything blocks a square
        if board[x, y, i] == 1:
            square_open = False
    return square_open

def is_surrounded(board, x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0  and dy == 0: #Don't check the square we're in
                continue
            if is_square_open(board, x+dx, y+dy):
                return False
    return True

def cant_move_indices(boards, mover):
    """
    Return the indices of the boards where the given player can't move.
    
    Parameters:
        boards: The boards, in standard format [N, X, Y, 3]
        mover: The moving player
    """
    
    boards = boards.clone().detach() #Use a duplicate to avoid side effects
    
    if mover == Mover.PLAYER:
        p_index = 0
    elif mover == Mover.OPPONENT:
        p_index = 1
    else:
        raise AssertionError('mover:', mover)
    
    indices = []
    
    for i in range(0, boards.shape[0]):
        board = boards[i, :, :, :]
        can_move=False
        for x in range(0, board.shape[1]):
            for y in range(0, board.shape[2]):
                if board[x, y, p_index] == 1:
                    if not is_surrounded(board, x, y):
                        can_move = True
                if can_move:
                    break
            if can_move:
                break
        if not can_move:
            indices.append(i)
    
    return indices

def remove_finished_games(boards, loses_indices):
    num_boards = boards.shape[0]
    keep_indices = [i for i in range(0, num_boards) if not i in loses_indices]
    keep_indices_tensor = torch.tensor(keep_indices)
    
    #Only keep the boards the opponent hasn't lost in yet
    boards = torch.index_select(boards, dim=0, index=keep_indices_tensor)

def play_games(player, opponent, boards, player_goes_first=True):
    outcomes = []
    moves = 1
    
    if not player_goes_first:
        
        opponent_loses_indices = cant_move_indices(boards, Mover.OPPONENT)
        boards = remove_finished_games(boards, opponent_loses_indices)
        
        for i in range(0, len(opponent_loses_indices)):
            outcomes.append((moves, 1))
        
        moves = opponent(boards)
        boards = apply_moves(boards, moves)
        moves += 1
    
    while boards.shape[0]:
        for (p1, p1_mover, p2, p2_mover, lose_num) in ((player, Mover.PLAYER, opponent, Mover.OPPONENT, 0),
                                                       (opponent, Mover.OPPONENT, player, Mover.PLAYER, 1)):
            
            p1_loses_indices = cant_move_indices(boards, p1_mover)
            boards = remove_finished_games(boards, p1_loses_indices)
            
            for i in range(0, len(p1_loses_indices)):
                outcomes.append((moves, lose_num))
            
            if boards.shape[0]:
                moves = player(boards)
                boards = apply_moves(boards, moves)
                moves += 1
    
    return outcomes