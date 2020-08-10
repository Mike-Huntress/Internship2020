"""
File: mcmc.py
Author: Jeremy Ephron
---------------------
This file implements a simple Markov Chain Monte Carlo (MCMC) optimizer.

"""

from typing import Callable, Optional, Tuple

import numpy as np


def mcmcOptimizer(
    initial_coef: np.array,
    obj_fn: Callable[[np.array], float],
    change_fn: Callable[[np.array, np.array, int], np.array],
    n_iters: int = 100000,
    initial_T: float = 0.2,
    verbose: bool = False
) -> Tuple[np.array, float]:
    """

    Optimizes an array of coefficients using MCMC.

    Args:
        initial_coef: The initial array of coefficients.
        obj_fn: The objective function to maximize. Takes in the array of 
            current coefficients and returns an objective function value.
        change_fn: The function that takes in the current coefficients, the 
            best coefficients, and the current iteration number and returns
            the new modified coefficients.
        n_iters: The number of iterations to run for.
        initial_T: The base temperature value from which to calculate the new
            temperature.
        verbose: Whether to print info about what's going on.

    Returns:
        best_coef: The best coefficients found.
        best_obj: The objective function value for the best coefficients.

    """

    coef = initial_coef.copy()
    best_coef = None
    best_obj = -np.inf

    for i in range(n_iters):
        if verbose and (i + 1) % np.ceil(n_iters * 0.05) == 0:
            print(f'{i * 100 // n_iters}% done, best_obj={best_obj}, '
                  f'best_coef={best_coef}')

        new_coef = change_fn(coef.copy(), best_coef, i)
        new_obj = obj_fn(new_coef)

        T = initial_T * np.exp(-np.log10(1.00002) * i)
        
        if new_obj > best_obj:
            coef = new_coef
            best_coef = new_coef
            best_obj = new_obj

            if verbose:
                print(f'New best: {best_obj} with coefficients: {best_coef}')

        elif np.random.random() < np.exp((new_obj - best_obj) / T):
            coef = new_coef
    
    print(f'100% done, best_obj={best_obj}, best_coef={best_coef}')
    return best_coef, best_obj

