from core.sink import Sink
from core.sink import ElectricalSink
from core.power import AlternatingCurrent
from core.transmission import Transformer

test = Sink(1,2,3,4)

print(test._parents)
print(test._children)
print(test.location)
print(test.power_in)

test2 = ElectricalSink(1,2,3,4,5,6)

#parents, children, power, location, voltage, phase

print(test2.location, test2._parents, test2._children, test2.power_in, test2.voltage_level, test2.phase)

power = AlternatingCurrent(1000,2,3,4)
print(power.power, power.voltage, power.frequency, power.power_factor)

transformer = Transformer(1,2,3)
transformer.get_power_in()
print(transformer.power_in.power)

#if __name__ == "__main__":
    #test_component = Component()
    #print(test_component.get_children())
    #print(test_component)

