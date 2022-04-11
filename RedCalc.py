#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:24:36 2020

@author: Corbett Redden
"""

from math import pi
import warnings


def factorial(n):
    prod = 1
    for i in range(1, n+1):
        prod *= i
    return prod


def sign(x):
    """
    Return plus/minus/0 sign of a real number
    
    Returns
        -1 if x < 0
        0 if x == 0
        1 if x > 0
    """
    if x==0:
        return 0
    elif x < 0:
        return -1
    elif x > 0:
        return 1


def mod2pi(theta):
    """ Return representative of theta in [-pi,pi) """
    return (theta+pi)%(2*pi) - pi


def binomial(alpha, n):
    """ 
    Return binomial coefficient 'alpha choose n' (float).
    Uses multiplicative formula, so alpha doesn't have to
    be an integer; eg can be used for Taylor series of sqrt
    """
    product = 1
    for k in range(1, n+1):
        product *= (alpha-k+1)/k
    return product
    

def sqrt_taylor(x, n):
    """
    Uses a degree n Taylor series, centered at x=1, to 
    approximates sqrt(x).
    Warnings/Questions: Does this always give good answer?
    If it doesn't, what is happening?
    """
    total=0
    for k in range(n+1):
        total += binomial(.5,k)*(x-1)**k
    return total


def trig_deg_given_tolerance(tol):
    """
    Given desired maximal error of sine or cosine, returns smallest 
    order for the Taylor series that will guarantee such accuracy.
    
    Example: accuracy of 1e-8 uses 19th order polynomial
    """        
    k=0
    while (pi**(k+1))/factorial(k+1) >= tol:
        k += 1
    return k


def cos(x, degrees=False, tolerance=1e-11):
    """
    Return cosine(x), using Taylor series of (x modulo 2pi)
    
    Parameters
    ----------
    x : float, int
        input for cos(x).
    deg : bool or string, optional
        If using degrees, use True. The default is False (using radians).
    tolerance : float, optional
        Required accuracy of output. The default is 1e-11.
        Disclaimer - smaller tolerances may not necessarily be more accurate
        due to floating point errors.

    Returns
    -------
    cosx : float
        output cos(x)
    """    
    # Convert to radian if needed
    if degrees==True or degrees=="deg":    
        x = x*pi/180
    
    # Determine degree of Taylor polynomial
    if tolerance==1e-11:  #default tolerance
        poly_deg = 23
    else:
        poly_deg = trig_deg_given_tolerance(tolerance)
    
    # # Obtain representative of x in [0,2pi]
    # x = x%(2*pi)
    # Obtain representative in [-pi,pi]
    x = mod2pi(x)
    
    # Evaluate Taylor series
    cosx = 0
    for i in range(poly_deg//2+1):
        cosx +=  (-1)**i * (1/factorial(2*i))* x**(2*i)
    return cosx


def sin(x, degrees=False, tolerance=1e-11):
    """ 
    Return sine(x), using Taylor series of (x modulo 2pi)
    
    Parameters
    ----------
    x : float, int
        input for cos(x).
    deg : bool or string, optional
        If using degrees, use True. The default is False (using radians).
    tolerance : float, optional
        Required accuracy of output. The default is 1e-11.
        Disclaimer - smaller tolerances may not necessarily be more accurate
        due to floating point errors.

    Return sin(x) as float
    """
    # Convert to radian if needed
    if degrees==True or degrees=="deg":    
        x = x*pi/180
    
    # Determine degree of Taylor polynomial
    if tolerance==1e-11:  #default tolerance
        poly_deg = 23
    else:
        poly_deg = trig_deg_given_tolerance(tolerance)
    
    # # Obtain representative of x in [0,2pi]
    # x = x%(2*pi)
    # Obtain representative in [-pi,pi]
    x = mod2pi(x)
    
    # Evaluate Taylor series
    sinx = 0
    for i in range(poly_deg//2+1):
        sinx +=  (-1)**i * (1/factorial(2*i+1))* x**(2*i+1)
    return sinx


def nDeriv(f, a, h=.001):
    """ Numerically compute f'(a) by central method """
    return (f(a+h)-f(a-h))/(2*h)


def bisect_solve(f, rhs, a, b, x_tol=1e-10):
    """ Solve f(x)=rhs using bisection method """

    # Check lower<upper, and f(x)-rhs changes +/- sign
    if a >= b:
        print("upper bound must be > lower bound")
        return float("nan")
    if sign(f(a)-rhs) == sign(f(b)-rhs):
        print("f(x)-rhs has same sign at endpoints")
        return float("nan")
    
    x = .5*(a + b)
    y = f(x)

    while .5*(b-a) >= x_tol:
        if sign(y-rhs) == sign(f(a)-rhs):
            a = x
        elif sign(y-rhs) == sign(f(b)-rhs):
            b = x
        elif sign(y-rhs) == 0:
            return x
        x = .5*(a+b)
        y = f(x)
    return x


def riemann_sum(f, a, b, N=100, method=.5):
    """
    Calculate and return Riemann sum of f(x) from x=a to x=b
    
    Uses N rectangles (default N=1000)
    Method: 0 - left endpoint; .5 - midpoint; 1 - right endpoints
    """
    dx = (b-a)/N
    x_start = a + method*dx
    x_pts = [ x_start + i*dx for i in range(N) ]
    return sum([ f(x) for x in x_pts ])*dx


def trap_rule(f, a, b, N=100):
    """ Use trapezoid rule to estimate \int_a^b f(x)dx with N trapezoids """
    dx = (b-a)/N
    x_interior = [ a + i*dx for i in range(1,N) ]
    total = ( .5*f(a) + sum([ f(x) for x in x_interior ]) + .5*f(b) )*dx
    return total
    # total = .5*f(a)*dx + sum([ f(x)*dx for x in x_interior ]) + .5*f(b)*dx


def simpson_rule(f, a, b, N=50):
    """
    Approximate the integral of f(x) from a to b by Simpson's rule.

    Simpson's rule approximates the integral \int_a^b f(x) dx by the sum:
    (dx/3) ( f(x_0) + 4 \sum_{1< i odd <N} f(x_i) + 
            2 \sum_{1<i even<N} f(x_i) + f(x_N)  )
    where N even, x_i = a + i*dx, and dx = (b - a)/N.
    """
    
    if N%2 != 0:
        raise ValueError("N must be an even integer.")
    dx = (b-a)/N    
    x = [ a + i*dx for i in range(N+1) ]
    y_odd = [f(x[i]) for i in range(1, N, 2)]
    y_even = [f(x[i]) for i in range(2, N, 2)]
    return dx/3 * ( f(x[0]) + 4*sum(y_odd) + 2*sum(y_even) + f(x[N]) )
    ## Other variants of above commands include:
    # y_odd = [ f(x_odd) for x_odd in x[1:-1:2]]
    # y_even = [f(x_even) for x_even in x[2:-1:2]]
    # return sum([f(x[2*k-2]) + 4*f(x[2*k-1]) + f(x[2*k]) 
    #             for k in range(1, int(N/2)+1)])*dx/3


def fnInt(f, a, b, N=None, dx=1e-2, method="simpson"):
    """
    Numerically calculate \int_a^b f(x)dx
    
    Parameters
    ----------
    f : function
        function of single variable to be integrated
    a, b : numbers
        left, right bounds of integration; forms interval [a,b]
    N : integer, optional
        number of rectangles, i.e. n+1 x-values. 
        Default=None, which calculates based on dx        
    dx : float, optional
        Approximate desired dx. The default is 1e-3.
        input dx will be overriden if N is specified
    method : string, optional
        Integration method. The default is "simpson". Possible values:
            "left" : left endpoints
            "right" : right endpoints
            "mid" : midpoint rule
            "trap" : trapezoid rule
            "simpson" or "simp" : Simpsons's Rule (default)
        
    Returns
    -------
    float
        Approximation of integral f(x)dx on [a,b] using specified integration
        method with subintervals of equal length
        
    Examples
    --------
    fnInt(cos, 0, 2)
    fnInt(lambda x:x**2, -1, 14.5, N=10)
    fnInt(lambda x: x**5-1, 2.1, 3.1, dx=.1, method="left")
    """

    # Exception handling
    if not callable(f):
        raise TypeError("f must be a function")
    try:
        a = float(a)
        b = float(b)
    except:
        raise TypeError("a,b must be numbers")
    if N != None and type(N) != int:
        raise TypeError("N must be an integer")        
    try:
        dx = float(dx)    
    except:
        raise TypeError("dx must be a number")
    
    # Determine N
    if N == None:
        N = int( abs( (b-a)/dx ) )

    # Call specific integration function based on method
    if method in {"simp", "simpson", "Simp", "Simpson", "simpsons", "Simpsons",
                  "simpsons_rule","simpson_rule"}:
        if N%2 == 1:  
            warnings.warn("N was odd, so using N+1 for Simpson's Rule")
            N += 1
        return simpson_rule(f, a, b, N)
    if method in {"trap", "trapezoid", "trapz", "trapezoid_rule"}:
        return trap_rule(f, a, b, N)
    elif method in {"left", "l", "L"}:
        return riemann_sum(f, a, b, N, 0)
    elif method in {"mid", "midpoint"}:
        return riemann_sum(f, a, b, N, .5)
    elif method in {"right", "r", "R"}:
        return riemann_sum(f, a, b, N, 1)
    else:
        raise ValueError("method is unrecognized")

