from core.engine_loading import *
from core.source import *

import time

start = time.time()

engine_1 = DieselGenerator([0, 0, 0], 100)
engine_2 = DieselGenerator([0, 0, 0], 200)
engine_3 = DieselGenerator([0, 0, 0], 300)
main_engine = DieselMechanical([0, 0, 0], 4000)
source_list = [engine_1, engine_2, engine_3, main_engine]


mechanical_power = 3000
electrical_power = 550

test_opt = EngineLoadSelector(source_list, mechanical_power, electrical_power)

solve_time = time.time() - start

print(test_opt.result)
print('Engine 1 Power ', engine_1.power)
print('Engine 2 Power ', engine_2.power)
print('Engine 3 Power ', engine_3.power)
print('Main Engine Power ', main_engine.power)


print('Engine 1 Fuel Consumption ', engine_1.fuel_consumption)
print('Engine 2 Fuel Consumption ', engine_2.fuel_consumption)
print('Engine 3 Fuel Consumption ', engine_3.fuel_consumption)


# print(test_opt.constraints)
print(solve_time)
# print(test_opt.source_list)




