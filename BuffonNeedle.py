#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:06:11 2020

@author: Corbett Redden
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos

# np.random.seed(1)  #Comment out when running actual simulations

# Initial Parameters - These can be changed
num_needles = 200
needle_length = 1
board_width = 1
num_middle_boards = 3

# New/Abbreviated variables, determined by above parameters
r = needle_length/2  #radius - distance from needle midpoint
theoretical_avg = (2*needle_length)/(board_width*pi)

# Determine number boards to use
long_needle = (needle_length > board_width)
if not long_needle:  #short needle
    x_board_low = 0
    num_boards = num_middle_boards 
    x_board_high = num_middle_boards * board_width
if long_needle:
    num_left_boards = int(r//board_width)
    x_board_low = -num_left_boards * board_width
    num_right_boards = int(r//board_width)
    num_boards = num_left_boards + num_right_boards + num_middle_boards  
    x_board_high = (num_middle_boards + num_right_boards)*board_width

# Create x-values for lines between strips
x_board = np.linspace(x_board_low, x_board_high, num_boards+1)

# Determine bounds for needle midpoint. y-values could be adjusted
x_needle_low = 0
x_needle_high = num_middle_boards * board_width
y_needle_low = x_needle_low # defaulted to square
y_needle_high = x_needle_high # defaulted to square

# Drop needles. x0 is needle midpoint, theta is angle of rotation in (-pi/2,pi/2)
x0 = np.random.uniform(x_needle_low, x_needle_high, num_needles)
y0 = np.random.uniform(y_needle_low, y_needle_high, num_needles)
theta = np.random.uniform(-pi/2, pi/2, num_needles)

# Left, right endpoints of needles
xL = x0 - r*cos(theta)
xR = x0 + r*cos(theta)
yL = y0 - r*sin(theta)
yR = y0 + r*sin(theta)

# Calculate Intersections - row needle, column line
cond1 = xL.reshape(num_needles,1) <= x_board.reshape(1,num_boards+1)
cond2 = x_board.reshape(1,num_boards+1) <= xR.reshape(num_needles, 1)
intersect = np.logical_and(cond1, cond2)

# Associated calculations
num_intersections = np.sum(intersect)
avg_num_intersections = num_intersections / num_needles
needle_intersect = np.any(intersect, axis=1)
avg_num_needle_intersect = np.sum(needle_intersect) / num_needles

# Graph
# Determine graph bounds
margin = .25*board_width
x_graph_low = x_board_low - margin
x_graph_high = x_board_high + margin
y_graph_low = y_needle_low - margin
y_graph_high = y_needle_high + margin
# Graph boards
for i in range(num_boards+1):
    plt.plot([x_board[i], x_board[i]], [y_graph_low, y_graph_high], 
             color="red")
# Graph needles
for i in range(num_needles):
    needle_color = int(needle_intersect[i])*"blue" + int(not needle_intersect[i])*"grey"
    plt.plot([xL[i], xR[i]], [yL[i], yR[i]], color=needle_color, linewidth=1)
plt.xlim(x_graph_low, x_graph_high)
plt.ylim(y_graph_low, y_graph_high)
plt.axis(False)
title1 = "Board width: "+str(board_width)+"    Needle length: "+str(needle_length)+ "    Needles: "+str(num_needles)
title2 = "Average intersections: "+str(avg_num_intersections)+"     Theoretical: "+str(round(theoretical_avg,6))
title3 = long_needle*("\nPercent of needles that cross line: "+str(avg_num_needle_intersect))
plt.title(title1+"\n"+title2+title3)
# plt.savefig("BuffonNeedlePic")
plt.show()

