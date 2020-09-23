from core.sink import Sink
from core.sink import ElectricalSink
from core.power import AlternatingCurrent
from core.transmission import Transformer
from core.transmission import Cable

test = Sink(1, 2)

print(test.location)
print(test.power_in)

test2 = ElectricalSink(1, 2, 3, 4)

# power, location, voltage, phase
test_array = [test2.location, test2.power_in, test2.voltage_level, test2.phase]
assert test_array == [1, 2, 3, 4]
print(', '.join(map(str, test_array)))

power = AlternatingCurrent(1000, 2, 3, 4)
print(power.power, power.voltage, power.frequency, power.power_factor)

transformer = Transformer(1, 2)
transformer.get_power_in()
print(transformer.power_in.power)
print(transformer.power_in.voltage)




# if __name__ == "__main__":
#     test_component = Component()
#     print(test_component.get_children())
#     print(test_component)
