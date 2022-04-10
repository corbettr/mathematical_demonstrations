#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:51:32 2020

@author: Corbett Redden
"""

import random


def airplane_seat_simulation(num_passengers, num_seats=None):
    """Simulate seat assignment from classic probability problem.

    Input: num_passengers (int), num_seats (int, optional-will default
                                               to num_passengers)
    Output: list of tuples (passenger, seat)
    
    Passengers 1,...,num_passengers are each assigned the airplane seat
    corresponding to their number (eg person 2 has seat 2). Passengers board one
    at a time in their numbered order. Passenger 1 chooses a seat randomly. 
    Each subsequent passsenger sits in their assigned seat if it is still
    available. If it is not available, he/she randomly chooses a seat that
    has not yet been taken.
    """    
    if num_seats == None:
        num_seats = num_passengers
    if num_seats < num_passengers:
        return None
    
    passengers = list(range(1,num_passengers+1))
    seats = list(range(1, num_seats+1))
        
    pass_seat_pairings = [(passengers.pop(0), random_pop(seats))]
    
    while len(passengers) > 0:
        curr_person = passengers.pop(0)
        if curr_person in seats:
            pass_seat_pairings.append((curr_person, curr_person))
            seats.remove(curr_person)
        else:
            random_seat = random_pop(seats)
            pass_seat_pairings.append((curr_person, random_seat))
    return pass_seat_pairings
        

def airplane_simulation_statistics(num_trials, num_passengers=100, num_seats=100):
    """Repeatedly run airplane_seat_simulation, return correct seat frequency.
    
    Return: list - (i-1)st entry = frequency ith passenger gets assigned seat.
    For frequency of last passenger getting correct seat, append [-1], ie
    airplane_simulation_statistics(num_trials)[-1]
    """
    results = [ airplane_seat_simulation(num_passengers, num_seats) 
               for n in range(num_trials) ]
    num_correct_seat = [ sum([ results[trial][person][0]==results[trial][person][1] 
                              for trial in range(num_trials)]) 
                        for person in range(num_passengers) ]
    return [ num_correct_seat[i]/num_trials for i in range(num_passengers)]
    

def random_pop(l):
    """Input list l. Removes and returns a random item from l."""
    selection_num = random.choice(range(len(l)))
    return l.pop(selection_num)
