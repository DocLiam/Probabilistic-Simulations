from math import *

def get_immunity(time_last_infected):
    calculated_immunity = (time_last_infected*(2.0/3.0)-0.12)/exp(time_last_infected/2.0-0.5)+0.2
    
    return calculated_immunity

print(get_immunity(10))