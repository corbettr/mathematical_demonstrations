#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick code to determine palindrome sequence of a given starting number.
See "Lychrel process" https://en.wikipedia.org/wiki/Lychrel_number
Example: palindrome_sequence(13) returns [13, 44] 
         13 not palindrome, so take 13+31=44, which is a palindrome.
Example: palindrome_sequence(22, b=2, stop_length=1000) returns sequence
         of length 1000, of palindrome process for 22 in base 2 (binary);
         numbers in sequence are written in decimal form.
Comment: Code is very not-optimized for longer sequences.
Created on Wed Oct 28 11:02:08 2020
@author: Corbett Redden
"""

default_base = 10

def num_to_base(n, b=default_base):
    """Return base-b representation of natural number n as list"""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n%b)
        n //= b
    return digits[::-1]

def base_to_num(l, b=default_base):
    """Return integer represented by list l in base b"""
    reverse_l = l[::-1]
    return sum([ reverse_l[i]*b**i for i in range(len(l)) ])

def num_is_palindrome(n, b=default_base):
    """Determine if number n is palindrome"""
    digits = num_to_base(n, b)
    return digits == digits[::-1]
    
def mirror_number(n, b=default_base):
    """Return integer given by reversing digits (base b) of integer n"""
    return base_to_num(num_to_base(n,b)[::-1], b)
    
def iterate(n, b=default_base):
    """Return sum of n and its mirror image, base b"""
    return n + mirror_number(n, b)

def palindrome_sequence(n, b=default_base, stop_length = 100):
    """Return palindrome sequence with starting n, stopping if seq length = stop_length"""
    seq = [n]
    length = 1
    while length < stop_length and not num_is_palindrome(n,b):
        n = iterate(n,b)
        seq.append(n)
        length += 1
    return seq