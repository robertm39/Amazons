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
        boards: The boards, in standard format [N, X, Y, P, O, F]
        moves: The moves, in standard format [N, X_S, Y_S, X_M, Y_M, X_F, Y_F]
    """
    pass

def cant_move_indices(boards, mover):
    """
    Return the indices of the boards where the given player can't move.
    
    Parameters:
        boards: The boards, in standard format [N, X, Y, P, O, F]
        mover: The moving player
    """
    pass

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
#        num_boards = boards.shape[0]
        
        opponent_loses_indices = cant_move_indices(boards, Mover.OPPONENT)
        boards = remove_finished_games(boards, opponent_loses_indices)
#        keep_indices = [i for i in range(0, num_boards) if not i in opponent_loses_indices]
#        keep_indices_tensor = torch.tensor(keep_indices)
#        
#        #Only keep the boards the opponent hasn't lost in yet
#        boards = torch.index_select(boards, dim=0, index=keep_indices_tensor)
        
        for i in range(0, len(opponent_loses_indices)):
            outcomes.append((moves, 1))
        
        moves = opponent(boards)
        boards = apply_moves(boards, moves)
        moves += 1
    
    for (p1, p1_mover, p2, p2_mover, lose_num) in ((player, Mover.PLAYER, opponent, Mover.OPPONENT, 0),
                                                   (opponent, Mover.OPPONENT, player, Mover.PLAYER, 1)):
        p1_loses_indices = cant_move_indices(boards, p1_mover)
        moves = player(boards)
        boards = apply_moves(boards, moves)