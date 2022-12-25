import matplotlib.pyplot as plt

base_mortality = 0.05

def mortality(age):
    return base_mortality

class Organism:
    def __init__(self, age, immunity, infectivity, mask_reduction, x_position, y_position, infected):
        self.__age = age  # age in unit time (0-infinity)
        self.__mortality = mortality(age)  # likelihood of death for each unit time infected (0-1)
        self.__immunity = immunity  # immunity to death from each unit time infected (0-1)
        self.__infectivity = infectivity  # coefficient of infectivity (0-1)
        self.__mask_reduction = mask_reduction  # coefficient of mask reduction (0-1)
        
        self.__x_position = x_position  # x position (0-infinity)
        self.__y_position = y_position  # y position (0-infinity)
        
        self.__infected = infected  # infected (True/False)
    
    def change_position(self,)