from math import *

def get_immunity(time_last_infected):
    calculated_immunity = (time_last_infected*(2.0/3.0)-0.12)/exp(time_last_infected/2.0-0.5)+0.2
    
    return calculated_immunity

print(get_immunity(10))

def binary_search_value(x_lower, x_upper, y, error, f):
    x_mid = (x_lower+x_upper)/2.0
    
    if f(x_lower) == f(x_upper):
        return x_mid
    
    f_incr = f(x_upper) > f(x_lower)

    while abs(f(x_mid)-y) > error:
        if f(x_mid) < y:
            temp_x_lower = x_mid if f_incr else x_lower
            temp_x_upper = x_upper if f_incr else x_mid
            x_mid = (x_mid+x_upper)/2.0 if f_incr else (x_lower+x_mid)/2.0
        else:
            temp_x_lower = x_lower if f_incr else x_mid
            temp_x_upper = x_mid if f_incr else x_upper
            x_mid = (x_lower+x_mid)/2.0 if f_incr else (x_mid+x_upper)/2.0
        
        x_lower = temp_x_lower
        x_upper = temp_x_upper
        
    return x_mid

print(binary_search_value(0, 2.18, 0.8, 0.02, get_immunity))