import gaopt
from gaopt import search_space

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

params_range={
    'sin': search_space.binary(),
    'cos': search_space.binary(),
    'sin2': search_space.binary(),
    'cos2': search_space.binary(),
}
cal_time_lst = []
date_start = None


def objective1(candidate1, candidate2):  
     
    fig = plt.figure()
    
    ax1 = fig.add_subplot(1, 2, 1)    
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-10, 10)

    x, y = encoding(candidate1)
    ax1.plot(x, y)
    ax1.set_title("#1")
    
    
    ax2 = fig.add_subplot(1, 2, 2)    
    ax2.set_xlim(-5, 5)
    ax2.set_ylim(-10, 10)
    x = np.arange(-5, 5, 0.05)
    y = np.sin(x)
            
    x, y = encoding(candidate2)
    
    ax2.plot(x, y)
    ax2.set_title("#2")
        
    plt.ion()  
    plt.show()
    # You may save the plot to check later.
              
    
    out = input('Which is better? 1 or 2: ')
    if out == str(1):
        out_candidate = candidate1
    elif out == str(2):
        out_candidate = candidate2
    else:
        TypeError("input is unacceptable")
    
    plt.close()
    return out_candidate


def encoding(candidate_params):
    x = np.arange(-5, 5, 0.05)
    y = np.sin(x)
    
    if candidate_params.sin:
        y += np.sin(x)
    if candidate_params.cos:
        y += np.cos(x)
    if candidate_params.sin2:
        y += np.sin(2*x)
    if candidate_params.cos2:
        y += np.cos(2*x)
        
    return x, y


def main():
    p_m = 0.10
    p_c = 0.7

    population = 4
    generation = 4

    instance = gaopt.GAOpt(params_range, objective=objective1, generation=generation, population=population,
                           p_m=p_m, p_c=p_c, history=1)
    last_lst, all_list = instance.fit()
    # You may use encoder.


if __name__ == '__main__':
    main()
