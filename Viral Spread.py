import matplotlib.pyplot as plt

base_mortality = 0.1

def mortality(age):
    return base_mortality

def current_infectivity

class Organism:
    def __init__(self, age, immunity, infectivity, x_position, y_position):
        self.__age__ = age
        self.__mortality__ = mortality(age)
        self.__immunity__ = immunity
        self.__infectivity__ = infectivity
        
        self.__x_position__ = x_position
        self.__y_position__ = y_position