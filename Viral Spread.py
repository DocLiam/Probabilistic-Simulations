import matplotlib.pyplot as plt
from random import *

min_position = 0
max_position = 20

base_mortality = 0.05

def mortality(age):
    return base_mortality

class Organism:
    def __init__(self, age, immunity, infectivity, mask_reduction, x_position, y_position):
        self.__age = age  # age in unit time (0-infinity)
        self.__mortality = mortality(age)  # likelihood of death for each unit time infected (0-1)
        self.immunity = immunity  # immunity to death from each unit time infected (0-1)
        self.infectivity = infectivity  # coefficient of infectivity (0-1)
        self.mask_reduction = mask_reduction  # coefficient of mask reduction (0-1)
        
        self.__x_position = x_position  # x position (0-infinity)
        self.__y_position = y_position  # y position (0-infinity)
    
    def change_position(self):
        self.__x_position = min(max_position, max(min_position, self.__x_position+2-randint(0,4)))
        self.__y_position = min(max_position, max(min_position, self.__y_position+2-randint(0,4)))

    def change_age(self):
        self.__age += 1
        
    def change_mortality(self):
        self.__mortality = mortality(self.__age)
    
    def change_immunity
    
organisms = [Organism(age=randint(0,10), immunity=0, infectivity=0, mask_reduction=0, x_position=random(0,20), y_position=random(0,20)) for i in range(50)]
organisms.append(Organism(age=randint(0,10), immunity=0, infectivity=0.5, mask_reduction=0, x_position=random(0,20), y_position=random(0,20)))

x_values = []

for i in range(100):
    x_values.append(i)
    
    for organism in organisms