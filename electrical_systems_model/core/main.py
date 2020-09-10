from core.sink import ElectricalSink

test = ElectricalSink('parents', 'children', 'power', 'location', 'voltage', 'phase')
print(ElectricalSink)
print(test.voltage_level)
print(test.location)
print(test.power_out)

#if __name__ == "__main__":
    #test_component = Component()
    #print(test_component.get_children())
    #print(test_component)

