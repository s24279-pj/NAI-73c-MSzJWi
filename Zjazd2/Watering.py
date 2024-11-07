import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#tworzenie zmiennych wejściowych
temperature = ctrl.Antecedent(np.arange(10, 35, 1), 'temperature')
humidity_air = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity air')
humidity_soil = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity soil')

humidity_soil.automf(3)
humidity_air.automf(3)

# Definicja funkcji przynależności dla temperatury
temperature['cold'] = fuzz.trapmf(temperature.universe, [10,10,16,20])
temperature['optimal'] = fuzz.trapmf(temperature.universe, [18,21,24,27])
temperature['hot'] = fuzz.trapmf(temperature.universe, [25,30,35,35])

#Definicja zmiennej wyjściowej - czas podlewania
time = ctrl.Consequent(np.arange(0, 30, 1), 'time')

# Definicja funkcji przynależności dla czasu podlewania
time['short'] = fuzz.trimf(time.universe, [0,0,10])
time['medium'] = fuzz.trimf(time.universe, [5,15,25])
time['long'] = fuzz.trimf(time.universe, [20,30,30])

# Wizualizacja funkcji przynależności
time.view()
humidity_air.view()
temperature.view()

# Definiowanie reguł sterujących
rule1 = ctrl.Rule(humidity_soil['poor'] | humidity_air['poor'], time['long'])
rule2 = ctrl.Rule(humidity_air['good'] & temperature['optimal'], time['short'])
rule3 = ctrl.Rule(humidity_soil['poor'] | humidity_air['good'] | temperature['optimal'], time['medium'])
rule4 = ctrl.Rule(humidity_soil['good'] & humidity_air['good'], time['short'])
rule5 = ctrl.Rule(humidity_soil['average'] & humidity_air['average'] & temperature['optimal'], time['short'])
rule6 = ctrl.Rule(humidity_soil['poor'] & temperature['hot'], time['long'])
rule7 = ctrl.Rule(humidity_soil['good'] & temperature['cold'], time['short'])
rule8 = ctrl.Rule(humidity_air['poor'] & (temperature['optimal'] | temperature['hot']), time['medium'])
rule9 = ctrl.Rule(humidity_air['good'] & temperature['optimal'] & humidity_soil['good'], time['short'])
rule10 = ctrl.Rule(humidity_soil['poor'] & humidity_air['average'] & temperature['cold'], time['medium'])
rule11 = ctrl.Rule(humidity_soil['average'] & humidity_air['average'] & temperature['hot'], time['medium'])
rule12 = ctrl.Rule(humidity_soil['good'] & humidity_air['poor'] & temperature['hot'], time['medium'])
rule13 = ctrl.Rule(humidity_soil['poor'] & humidity_air['poor'] & temperature['hot'], time['long'])
rule14 = ctrl.Rule((humidity_soil['poor'] | humidity_air['poor']) & temperature['hot'], time['long'])

# Tworzenie systemu sterowania i symulacji
watering_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11,
                                    rule12, rule13, rule14])

watering = ctrl.ControlSystemSimulation(watering_ctrl)

#Przykładowe dane wejściowe
watering.input['humidity air'] = 0
watering.input['humidity soil'] = 0
watering.input['temperature'] = 35

# Przeprowadzenie obliczeń
watering.compute()

# Wynik i wykres
print(f"Czas podlewania roślin: {watering.output['time']}")
time.view(sim=watering)

plt.show()