from random import randrange

def stochastic_duration(lower_bound, upper_bound):
    if lower_bound == upper_bound:
        return lower_bound

    return randrange(lower_bound, upper_bound)

