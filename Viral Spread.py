import matplotlib.pyplot as plt
from random import *
from math import *
from time import sleep

min_position = 0
max_position = 10

time_interval = 1.0

base_mortality = 0.2

def get_mortality(age):
    calculated_mortality = base_mortality/(2.0+exp(4.0-age/10.0))
    
    return calculated_mortality

def get_immunity(time_last_infected):
    calculated_immunity = (1.0-random()/10.0)*((time_last_infected*(2.0/3.0)-0.12)/exp(time_last_infected/2.0-0.5)+0.2)
    
    return calculated_immunity

def get_infectivity(time_last_infected):
    calculated_infectivity = (1.4*time_last_infected-1.4/29.0)/exp(0.5*time_last_infected-0.5/29.0)-0.048
    
    return calculated_infectivity

class Organism:
    def __init__(self, age, immunity, infectivity, mask_reduction, time_last_infected, x_position, y_position):
        self.age = age  # age in unit time (0-infinity)
        self.mortality = get_mortality(age)  # likelihood of death for each unit time infected (0-1)
        self.immunity = immunity  # immunity to death from each unit time infected (0-1)
        self.infectivity = infectivity  # coefficient of infectivity (0-1)
        self.mask_reduction = mask_reduction  # coefficient of mask reduction (0-1)
        self.time_last_infected = time_last_infected  # time since last infection started in unit time (0-infinity)
        
        self.__x_position = x_position  # x position (min position-max position)
        self.__y_position = y_position  # y position (min position-max position)

    def change_age(self):
        self.age += time_interval
        
    def change_mortality(self):
        self.mortality = get_mortality(self.age)
    
    def change_immunity(self):
        if self.time_last_infected > -1:
            calculated_immunity = get_immunity(self.time_last_infected)
            
            self.immunity = (max(self.immunity, calculated_immunity)+self.immunity)/2.0

    def change_infectivity(self):
        if self.time_last_infected > -1:
            self.infectivity = max(0, get_infectivity(self.time_last_infected))
    
    def reset_time_last_infected(self):
        self.time_last_infected = 0
        
    def change_time_last_infected(self):
        if self.time_last_infected > -1:
            self.time_last_infected += time_interval
    
    def get_x_position(self):
        return self.__x_position

    def get_y_position(self):
        return self.__y_position

    def change_position(self):
        self.__x_position = min(max_position, max(min_position, self.__x_position+time_interval*2.0-4.0*random()))
        self.__y_position = min(max_position, max(min_position, self.__y_position+time_interval*2.0-4.0*random()))
    
organisms = [Organism(age=randint(0,50), immunity=0, infectivity=0, mask_reduction=random()/3, time_last_infected=-1, x_position=randint(0,10), y_position=randint(0,10)) for i in range(50)]
organisms.append(Organism(age=randint(0,10), immunity=0, infectivity=1.0, mask_reduction=0, time_last_infected=0, x_position=randint(0,10), y_position=randint(0,10)))

initial_count = len(organisms)

x_values = []
age_values = []
proportion_values = []
immunity_values = []
infectivity_values = []
proportion_infected_values = []

time_total = 100

for k in range(time_total):
    plt.clf()
    
    for organism in organisms:
        plt.scatter(organism.get_x_position(), organism.get_y_position(), color=((organism.infectivity,0,0) if organism.infectivity > 0 else (0,1,0)))
    
    plt.plot(x_values, proportion_values)
    plt.plot(x_values, immunity_values)
    plt.plot(x_values, infectivity_values)
    plt.plot(x_values, proportion_infected_values)
    
    plt.pause(0.05)
    
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

sleep(5)