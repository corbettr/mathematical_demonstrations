#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Corbett Redden

Suppose you are given an ordered multiset (a, a, b, b, b, c),
which is equivalent to the multiset (0, 0, 1, 1, 1, 2)
and can be represented by the partition_tuple (2, 3, 1).
If you count all possible permutations, you get the multinomial 
coefficient of the partition_tuple, eg 5!/(2!3!)

How many configurations are there if you now count permutations as 
equivalent when they differ by a cyclic permutation (in cyclic group Cn)?
eg aabbb ~ abbba ~ bbbaa ~ etc
What about when they differ by a cyclic permutation and order reversal
(ie permutation in dihedral group Dn)?
eg  abcc ~ cabc ~ ccab ~ bcca ~
   ~ccba ~ cbac ~ bacc ~ accb

An equivalence class of such permutations, modulo cyclic permutations,
is called a "necklace" in combinatorics. The equivalence class,
modulo Dn, is called a "bracelet."
https://en.wikipedia.org/wiki/Necklace_(combinatorics)
The idea is: you are making a necklace or braclet from the beads
(a, a, b, b, b, c), and you want to consider two necklaces as the same
if they differ by rotating it around your neck. Similarly, two "bracelets"
are the same if the physical bracelets are equivalent in 3d space, which
allows you to rotate the bracelet or to turn it over.

The number of such distinct necklaces/bracelets (ie the cardinarily of the
"configuration space of anagrams" modulo cyclic/dihedral group)
is computed by brute force in this code.  The functions return the c
cardinality by default, but they can also return a set of representatives
or the entire cosets.

eg 
>>> partition_tuple = (2, 3, 1)
>>> necklaces(partition_tuple)
10
>>> bracelets(partition_tuple)
6
"""
# Remark: the primary function is really 'configs_count'. The functions 
# 'necklaces' and 'bracelets' only exist for notational ease, as they
# both call 'configs_count'.
    
from sympy.utilities.iterables import multiset_permutations
# import itertools


def necklaces(partition_tuple, output='num'):
    """
    Determine the necklaces of a given partition.
    
    Input:
        partition_tuple : tuple
            eg (2, 2, 1) to represent 2+2+1=5, [a,a,b,b,c]
        output : {'num', 'reps', 'cosets'}, optional

    Output: 
        if output=='num', returns number of necklaces
        if output=='reps', returns a list of necklaces (representatives)
        if output=='cosets', return list of cosets        
    """
    if output=='num':
        return configs_count(partition_tuple, group="Cn", return_cosets=False)
    
    if output=='cosets':
        return configs_count(partition_tuple, group="Cn", return_cosets=True)
    
    if output=='reps':
        cosets = configs_count(partition_tuple, group="Cn", return_cosets=True)
        return [ x.pop() for x in cosets]


def bracelets(partition_tuple, output='num'):
    """
    Determine the bracelets of a given partition.
    
    Input:
        partition_tuple : tuple
            eg (2, 2, 1) to represent 2+2+1=5, [a,a,b,b,c]
        output : {'num', 'reps', 'cosets'}, optional

    Output: 
        if output=='num', returns number of bracelets
        if output=='reps', returns a list of bracelets (representatives)
        if output=='cosets', return list of cosets        
    """
    if output=='num':
        return configs_count(partition_tuple, group="Dn", return_cosets=False)
    
    if output=='cosets':
        return configs_count(partition_tuple, group="Dn", return_cosets=True)
    
    if output=='reps':
        cosets = configs_count(partition_tuple, group="Dn", return_cosets=True)
        return [ x.pop() for x in cosets]


def configs_count(partition_tuple, group="Cn", return_cosets=False):
    """
    Given partition, calculate the number of multiset permutations
    (ie anagrams) modulo cyclic rotations (group="Cn")
    or modulo reversals + cyclic rotations (group="Dn")
    
    Input:
        partition_tuple : tuple
            eg (2, 2, 1) to represent 2+2+1=5, [a,a,b,b,c]
        group : "Cn" or "Dn" for cyclic/dihedral group
        return_cosets : bool
            False : only return cardinality
            True : return list of quotient set elems
    Output: 
        cardinality (or set) of configurations modulo symmetry
    """
    attendees = multiset_tuple(partition_tuple)
    configs_iter = multiset_permutations(attendees)
    configs = { tuple(x) for x in configs_iter }
    # configs = set(itertools.permutations(attendees))
    return mod_group(configs, group, return_cosets)


def multiset_tuple(partition_tuple):
    """
    input partition, output tuple of individual labeled objects
    >>> multiset_tuple((2, 3, 1))
    (0, 0, 1, 1, 1, 2)
    """
    elem_list = list()
    elem = 0
    for n in partition_tuple:
        elem_list += [elem] * n
        elem += 1
    return tuple(elem_list)


def mod_group(orig_set, group, return_cosets=False, inplace=False):
    """ 
    Input:
        orig_set : set, where each element is an iterable
            (assumed to be of same length)
        group : "Cn" or "Dn" for cyclic/dihedral group
        return_cosets : bool
            False : only return cardinality
            True : return list of quotient set elems
        inplace : bool
            False : orig_set is not modified
    Output: 
        cardinality (or set) of orig_set (configs) modulo symmetry
    """
    # sets are mutable, so make a copy if we don't want to eventually delete all elements from input set
    big_set = (orig_set if inplace else orig_set.copy())

    # Determine value of n (this assumes all multisets have the same length; n could be determined for each individual element if we don't want to assume this)
    elem = big_set.pop()
    n = len(elem)
    big_set.add(elem)
        
    quotient_size = 0
    if return_cosets:
        quotient_list = list()  # can't make quotient_set b/c elements are sets which are not hashable (and different orbits may have different size)

    while big_set:
        elem = big_set.pop()
        orbit = group_orbit(elem, group, n)
        quotient_size += 1
        if return_cosets:
            big_set.add(elem)
            quotient_list.append(orbit & big_set)
        big_set -= orbit

    if return_cosets:
        return quotient_list
    else:
        return quotient_size


def group_orbit(x, group, n):
    """
    Input:
        x : iterable (tuple, list)
        group : "Cn" or "Dn"
        n : len(x), parameter for Cn, Dn
    Output:
        orbit : set of tuples g.x for g in group
    """
    if group not in {"Cn", "Dn"}:
        raise Exception("Incorrect 'group' in 'group_orbit' argument")
    orbit = set()
    if group == "Cn":
        for i in range(n):
            orbit.add(tuple(x[(i+_)%n] for _ in range(n)))
    if group == "Dn":
        for i in range(n):
            orbit.add(tuple(x[(i+_)%n] for _ in range(n)))
            orbit.add(tuple(x[(i+_)%n] for _ in range(n-1,-1,-1)))
    return orbit
