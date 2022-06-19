import copy
import random
import datetime

import numpy as np
import tensorflow as tf
import pandas as pd

from .mutate import mutate_normal

"""
Hyper-parameters need to be explained:
    - params: search_range (explained below)
    - objective: objective function
    - generation [int]: generation size (default: 30)
    - population [int]: population size (population: 100)
    - p_m [float]: mutation rate (default: 0.1=10%)
    - p_c [float]: crossover rate (default: 0.7=70%)
    - history [1 or 0]: outputs the detail or less (default: 0)
        - 1: all generation
        - 0: last generation only
    - seed [int]: seed at randomizing

Params range should be specified as follows.

    from gaopt import search_space
    params = {
        'x1': search_space.categorical(['relu', 'tanh']), # list(candidates)
        'x2': search_space.discrete(-1.0, 1.0, 0.2), # min, max, step
        'x3': search_space.discrete_int(-4, 2), # min, max
        'x4': search_space.fixed(1) # a fixed value
    }

Hiroya MAKINO
Grad. School of Informatics, Nagoya University

ver1.0, Jun. 19 2022 (inherited from https://github.com/macky168/gaopt)
"""


class params_comb:
    pass


class GAOpt:
    
    def __init__(
            self, 
            params, objective, generation=30, population=100,
            p_m=0.10, p_c=0.7, 
            history=0, seed=168):
        if params is None:
            TypeError("You must specify the params range")
        self.params = params
        self.keys = [key for key in params.keys()]
        for key in self.keys:
            setattr(params_comb, key, "")
            
        if objective is None:
            TypeError("You must specify the objective function")
        self.objective = objective
        
        self.num_of_gens = generation
        if population % 2 == 1:
            TypeError("Population must be set in even number")
        self.population = population
        
        self.rate_of_mutation = p_m
        self.rate_of_crossover = p_c
        if (not history == 1) and (not history ==0):
            TypeError("History parameter must be set in 0 or 1")
        self.history = history

        random.seed(seed)
        np.random.seed(seed)
        tf.random.set_seed(seed)
        
    def fit(self):
        current_lst = [[] for pop in range(self.population)]

        # ---------------------
        # initial population
        # ---------------------
        for i in range(self.population):
            temp_params_comb = params_comb()
            for key in self.keys:
                setattr(temp_params_comb, key, self.params[key].select())
            current_lst[i] = temp_params_comb
        next_lst = copy.deepcopy(current_lst)
        
        # keep all history or not
        if self.history == 1:
            all_list = [next_lst]

        # ---------------------
        # generation update
        # ---------------------
        for gen in range(self.num_of_gens):
            print('\n')
            print('*** generation', gen, "/", self.num_of_gens, " *************")

            current_lst = copy.deepcopy(next_lst)
            next_lst = [0] * self.population

            # ---------------------
            # crossover / copy
            # ---------------------
            j = 0
            while j < self.population:
                
                index_lst = [i for i in range(self.population)]

                candidate1_index = np.random.choice(index_lst)
                candidate1 = current_lst[candidate1_index]
                candidate2_index = np.random.choice(index_lst)
                candidate2 = current_lst[candidate2_index]
                parent1 = self.tournament_func(candidate1, candidate2)
                
                candidate3_index = np.random.choice(index_lst)
                candidate3 = current_lst[candidate3_index]
                candidate4_index = np.random.choice(index_lst)
                candidate4 = current_lst[candidate4_index]    
                parent2 = self.tournament_func(candidate3, candidate4)
                
                key1 = random.random()

                # ---------------------
                # crossover
                # ---------------------
                if key1 < self.rate_of_crossover and j+1 < self.population:
                    next_lst[j], next_lst[j+1] \
                        = copy.deepcopy(self.crossover(parent1, parent2))
                    j += 2

                # ---------------------
                # copy
                # ---------------------
                else:
                    next_lst[j], next_lst[j+1] \
                        = copy.deepcopy(self.copy_parent(parent1, parent2))
                    j += 2
                        
            # ---------------------
            # mutation
            # ---------------------
            for i in range(self.population):
                next_lst[i] = copy.deepcopy(
                    mutate_normal(next_lst[i], self.params, self.keys, self.rate_of_mutation))
                    
        if self.history == 1:
            return next_lst, all_list
        elif self.history == 0:
            return next_lst
        
    def tournament_func(self, candidate1, candidate2):
        out = self.objective(candidate1, candidate2)
        return out
                
    def crossover(self, parent1, parent2):
        chromosome_length = len(self.keys)

        child1 = params_comb()
        child2 = params_comb()

        point_a = random.randint(0, chromosome_length-1)
        point_b = random.randint(0, chromosome_length-1)
        point1 = min(point_a, point_b)
        point2 = max(point_a, point_b)
        
        i = 0
        while i < chromosome_length:
            if i <= point1 or i > point2:
                setattr(child1, self.keys[i], getattr(parent1, self.keys[i]))
                setattr(child2, self.keys[i], getattr(parent2, self.keys[i]))
            else:
                setattr(child1, self.keys[i], getattr(parent2, self.keys[i]))
                setattr(child2, self.keys[i], getattr(parent1, self.keys[i]))
            i += 1
        
        return child1, child2
    
    def copy_parent(self, parent1, parent2):
        child1 = parent1
        child2 = parent2

        return child1, child2
