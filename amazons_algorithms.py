# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 16:33:31 2020

@author: rober
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init

from utils import crelu

full_bias = True

conv = nn.Conv2d

act = crelu
act_mult = 2

piece_first_channels = 32
piece_second_channels = 32
piece_third_channels = 32

piece_fourth_channels = 64
piece_fifth_channels = 64

class AmazonsPlayer(nn.Module):
    def __init__(self):
        super(AmazonsPlayer, self).__init__()
        
        self.piece_conv_1 = conv(in_channels=4,
                           out_channels=piece_first_channels,
                           kernel_size=3,
                           padding=1,
                           bias=full_bias)
        
        self.piece_conv_2 = conv(in_channels=piece_first_channels * act_mult,
                           out_channels=piece_second_channels,
                           kernel_size=3,
                           padding=1,
                           bias=full_bias)
        
        self.piece_conv_3 = conv(in_channels=piece_second_channels * act_mult,
                           out_channels=piece_third_channels,
                           kernel_size=3,
                           padding=1,
                           bias=full_bias)
        
        self.piece_conv_4 = conv(in_channels=piece_third_channels * act_mult,
                           out_channels=piece_fourth_channels,
                           kernel_size=5,
                           padding=2,
                           bias=full_bias)
        
        self.piece_conv_5 = conv(in_channels=piece_fourth_channels * act_mult,
                           out_channels=piece_fifth_channels,
                           kernel_size=5,
                           padding=2,
                           bias=full_bias)