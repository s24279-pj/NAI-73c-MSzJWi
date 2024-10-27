import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

temperature = ctrl.Antecedent(np.arange(10, 35, 1), 'temperature')
humidity_air = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity air')
humidity_soil = ctrl.Antecedent(np.arange(0, 100, 1), 'humidity soil')

humidity_soil.automf(3)
humidity_air.automf(3)

temperature['cold'] = fuzz.trapmf(temperature.universe, [10,10,16,20])
temperature['optimal'] = fuzz.trapmf(temperature.universe, [18,21,24,27])
temperature['hot'] = fuzz.trapmf(temperature.universe, [25,30,35,35])

time = ctrl.Consequent(np.arange(0, 30, 1), 'time')

time['short'] = fuzz.trimf(time.universe, [0,0,10])
time['medium'] = fuzz.trimf(time.universe, [0,10,20])
time['long'] = fuzz.trimf(time.universe, [10,20,30])


time.view()
humidity_air.view()
temperature.view()

rule1 = ctrl.Rule(humidity_soil['poor'] | humidity_air['poor'] | temperature['hot'], time['long'])
rule2 = ctrl.Rule(humidity_soil['average'] | humidity_air['poor'] | temperature['cold'], time['medium'])
rule3 = ctrl.Rule(humidity_soil['average'] | humidity_air['average'] | temperature['cold'], time['short'])

watering_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

watering = ctrl.ControlSystemSimulation(watering_ctrl)

watering.input['humidity air'] = 26
watering.input['humidity soil'] = 9.8
watering.input['temperature'] = 27

# Crunch the numbers
watering.compute()

print (watering.output['time'])
time.view(sim=watering)


plt.show()