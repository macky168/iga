import random
import copy

# ---------------------
# mutate individual
# ---------------------
# normal mutation
def mutate_normal(params_comb_temp, params, keys, rate_of_mutation):
    for key in keys:
        if random.random() < rate_of_mutation:
            setattr(params_comb_temp, key, params[key].mutate(getattr(params_comb_temp, key)))
        else:
            pass
            # no mutation
    return params_comb_temp

# ---------------------
# mutate each bit
# ---------------------
# normal mutation
def mutate_normal_each_key(params_comb_temp, params, key, rate_of_mutation):
    if random.random() < rate_of_mutation:
        setattr(params_comb_temp, key, params[key].mutate(getattr(params_comb_temp, key)))
    else:
        pass
        # no mutation
    return params_comb_temp