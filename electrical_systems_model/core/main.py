from core.sink import Sink
from core.sink import ElectricalSink

test = Sink(1,2,3,4)

print(test._parents)
print(test._children)
print(test.location)
print(test.power_in)

test2 = ElectricalSink(1,2,3,4,5,6)

#parents, children, power, location, voltage, phase

print(test2.location, test2._parents, test2._children, test2.power_in, test2.voltage_level, test2.phase)



#if __name__ == "__main__":
    #test_component = Component()
    #print(test_component.get_children())
    #print(test_component)

