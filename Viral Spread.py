import matplotlib.pyplot as plt
from random import *
from math import *
from time import sleep

min_position = 0
max_position = 20

time_interval = 0.5

base_mortality = 0.1

time_max_immunity = 2.18
allowed_error = 0.001

def get_mortality(age):
    calculated_mortality = base_mortality/(2.0+exp(4.0-age/10.0))
    
    return calculated_mortality

def get_immunity(time_last_infected):
    calculated_immunity = ((time_last_infected/2.0-0.3)/exp(time_last_infected/2.0-0.5)+0.5)
    
    return calculated_immunity

def get_infectivity(time_last_infected):
    calculated_infectivity = (1.4*time_last_infected-1.4/29.0)/exp(0.5*time_last_infected-0.5/29.0)-0.048
    
    return calculated_infectivity

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

class Organism:
    def __init__(self, age, can_recover, immunity, infectivity, mask_reduction, time_last_infected, time_first_infected, x_position, y_position):
        self.age = age  # age in unit time (0-infinity)
        self.can_recover = can_recover  # whether the person can recover, or is persistently sick
        self.mortality = get_mortality(age)  # likelihood of death for each unit time infected (0-1)
        self.immunity = immunity  # immunity to death from each unit time infected (0-1)
        self.infectivity = infectivity  # coefficient of infectivity (0-1)
        self.mask_reduction = mask_reduction  # coefficient of mask reduction (0-1)
        self.time_last_infected = time_last_infected  # time since last infection started in unit time (0-infinity)
        self.time_first_infected = time_first_infected  # time since first infection started in unit time (0-infinity)
        
        self.__x_position = x_position  # x position (min position-max position)
        self.__y_position = y_position  # y position (min position-max position)

    def change_age(self):
        self.age += time_interval
        
    def change_mortality(self):
        if self.can_recover:
            self.mortality = get_mortality(self.age)
        else:
            self.mortality = 0
    
    def change_immunity(self):
        if self.time_first_infected > -1 and self.can_recover:
            self.immunity = get_immunity(self.time_first_infected)

    def change_infectivity(self):
        if self.time_last_infected > -1 and self.can_recover:
            self.infectivity = max(0, get_infectivity(self.time_last_infected))
    
    def reset_time_last_infected(self):
        if self.immunity > 0:
            self.time_first_infected = binary_search_value(0, time_max_immunity, self.immunity, allowed_error, get_immunity)
        else:
            self.time_first_infected = 0
            
        self.time_last_infected = 0
        
    def change_time_last_infected(self):
        if self.time_last_infected > -1:
            self.time_last_infected += time_interval
        if self.time_first_infected > -1:
            self.time_first_infected += time_interval
    
    def get_x_position(self):
        return self.__x_position

    def get_y_position(self):
        return self.__y_position

    def change_position(self):
        self.__x_position = min(max_position, max(min_position, self.__x_position+time_interval*(0.5-1.0*random())))
        self.__y_position = min(max_position, max(min_position, self.__y_position+time_interval*(0.5-1.0*random())))
    
organisms = [Organism(age=randint(0,50), can_recover=True, immunity=0, infectivity=0, mask_reduction=0, time_last_infected=-1, time_first_infected=-1, x_position=randint(min_position, max_position), y_position=randint(min_position, max_position)) for i in range(80)]
organisms.append(Organism(age=randint(0,10), can_recover=True, immunity=0, infectivity=1.0, mask_reduction=0, time_last_infected=0, time_first_infected=0, x_position=randint(min_position, max_position), y_position=randint(min_position, max_position)))

initial_count = len(organisms)

x_values = []
age_values = []
proportion_values = []
immunity_values = []
infectivity_values = []
proportion_infected_values = []

time_total = 200

for k in range(time_total):
    plt.clf()
    
    for organism in organisms:
        plt.scatter(organism.get_x_position(), organism.get_y_position(), color=((organism.infectivity,0,0) if organism.infectivity > 0 else (0,1,0)))
    
    plt.plot(x_values, proportion_values)
    plt.plot(x_values, immunity_values)
    plt.plot(x_values, infectivity_values)
    plt.plot(x_values, proportion_infected_values)
    
    plt.pause(0.01)
    
    temp_organisms = organisms.copy()
    
    for i in range(len(temp_organisms)):
        for j in range(i, len(temp_organisms)):
            organism1 = organisms[i]
            organism2 = organisms[j]
            
            temp_organism1 = temp_organisms[i]
            temp_organism2 = temp_organisms[j]
            
            distance = ((organism1.get_x_position()-organism2.get_x_position())**2 + (organism1.get_y_position()-organism2.get_y_position())**2)**0.5
            
            volumetric_probability_coefficient = 1/(1+distance**3)
            
            if organism1.infectivity > 0:
                if organism2.infectivity == 0:
                    threshold = time_interval*volumetric_probability_coefficient*organism1.infectivity*((1.0-organism2.immunity)*((1.0-organism1.mask_reduction)*(1.0-organism2.mask_reduction)))
                    
                    if random() < threshold:
                        temp_organism2.reset_time_last_infected()
            elif organism2.infectivity > 0:
                threshold = time_interval*volumetric_probability_coefficient*organism2.infectivity*((1.0-organism1.immunity)*((1.0-organism1.mask_reduction)*(1.0-organism2.mask_reduction)))
                
                if random() < threshold:
                    temp_organism1.reset_time_last_infected()
    
    mean_age = 0        
    mean_immunity = 0
    mean_infectivity = 0
    proportion_infected = 0
    
    for temp_organism in temp_organisms:
        temp_organism.change_age()
        temp_organism.change_mortality()
        temp_organism.change_immunity()
        temp_organism.change_infectivity()
        temp_organism.change_position()
        temp_organism.change_time_last_infected()

        mortality = time_interval*temp_organism.mortality*temp_organism.infectivity*(1.0-temp_organism.immunity)
        
        if random() < mortality:
            temp_organisms.remove(temp_organism)
        else:
            mean_age += temp_organism.age
            mean_immunity += temp_organism.immunity
            mean_infectivity += temp_organism.infectivity
            proportion_infected += 1 if temp_organism.infectivity > 0 else 0
    
    mean_age /= len(temp_organisms)
    mean_immunity /= len(temp_organisms)
    mean_infectivity /= len(temp_organisms)
    proportion_infected /= len(temp_organisms)
    
    x_values.append(min_position+(max_position-min_position)*(k/time_total))
    age_values.append(min_position+(max_position-min_position)*mean_age)
    proportion_values.append(min_position+(max_position-min_position)*(len(temp_organisms)/initial_count))
    immunity_values.append(min_position+(max_position-min_position)*mean_immunity)
    infectivity_values.append(min_position+(max_position-min_position)*mean_infectivity)
    proportion_infected_values.append(min_position+(max_position-min_position)*proportion_infected)
    
    organisms = temp_organisms.copy()

sleep(10)