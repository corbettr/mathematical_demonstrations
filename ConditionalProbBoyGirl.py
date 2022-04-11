#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:51:32 2020

@author: Corbett Redden
"""

# Girl/boy conditional probability problem

import random

n = int(1e5)
children = [random.choices(["B","G"], k=2) for i in range(n)]

num_at_least_one_girl=0
num_eldest_girl=0
num_two_girls=0

#raw calculations
for i in range(n):    
    if "G" in children[i]:
        num_at_least_one_girl += 1
        if children[i][1] == "G":
            num_eldest_girl += 1
            if children[i][0]=="G":
                num_two_girls += 1
                
#conditional probabilities
both_girls_if_eldest_girl = 0
both_girls_if_at_least_one_girl = 0
youngest_girl_if_at_least_one_girl = 0

for i in range(n):
    if children[i][1] == "G":
        if children[i][0] == "G":
            both_girls_if_eldest_girl += 1
    
    if "G" in children[i]:
        if children[i][0] == "G":
            youngest_girl_if_at_least_one_girl += 1
            if children[i][1] == "G":    
                both_girls_if_at_least_one_girl += 1
            
        
print("Probability that both are girls if the eldest is a girl:", 
      both_girls_if_eldest_girl/num_eldest_girl)
print("Probability that the youngest is a girl if there is at least one girl:", 
      youngest_girl_if_at_least_one_girl/num_at_least_one_girl)
print("Probability that both are girls if there is at least one girl:",
      both_girls_if_at_least_one_girl/num_at_least_one_girl)    
