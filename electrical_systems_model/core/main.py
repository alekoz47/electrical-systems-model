from core.model import Model
from core.sink import ElectricalSink
from core.transmission import Cable, Transformer


def main():
    # test run of Motor -> Transformer -> Generator (root)
    # and several mutations

    # Steps:
    # create components
    # create data model from components
    # solve model

    # straight hierarchy test
    cable1 = Cable([0, 0, 0])
    transformer = Transformer([100, 12, 20], 440)
    cable2 = Cable([0, 0, 0])
    motor = ElectricalSink([125, 3, 5], 10000, 220)
    components = [cable1, transformer, cable2, motor]
    cable1.name = "Cable 1"
    cable2.name = "Cable 2"
    transformer.name = "Transformer"
    motor.name = "Motor"
    model = Model()
    model.import_components(components)  # right now this just adds components in a straight hierarchy\
    print("Test 1 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " W")
    model.print_tree()

    # test adding some components and resolving
    # we've added call to reset inside solve method to clear up old data
    motor2 = ElectricalSink([125, 3, 5], 10000, 220, 0.8)
    motor2.name = "Motor 2"
    cable3 = Cable([0, 0, 0])
    cable3.name = "Cable 3"
    model.add_sink(cable3, transformer)
    model.add_sink(motor2, cable3)
    print("Test 2 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " W")
    model.print_tree()

    print_component_info(cable1)
    print_component_info(transformer)
    print_component_info(cable2)
    print_component_info(motor)

    print("Transformer children:")
    for comp in transformer.get_children():
        print(comp.name + " -> " + comp.get_children()[0].name)


def print_component_info(comp):
    print(comp.name)
    print("Power in: " + str("%.1f" % abs(comp.power_in.power / 1000)) + " kW")
    if not isinstance(comp, ElectricalSink):
        print("Power out: " + str("%.1f" % abs(comp.power_out.power / 1000)) + " kW")
        print("Power drop: " + str("%.1f" % abs(comp.power_out.power - comp.power_in.power)) + " W")
    print("Voltage: " + str("%.1f" % abs(comp.power_in.voltage)) + " V")
    print("Current: " + str("%.1f" % abs(comp.power_in.current)) + " A")
    if isinstance(comp, Cable):
        print("Resistance: " + str("%.6f" % comp.resistance) + " Ohms")
    print(" \n")

PARENT = Transformer([100, 12, 20], 440)
CHILD = ElectricalSink([125, 3, 5], 10000, 220)
CABLE = Cable([0, 0, 0])
CABLE.set_parents(PARENT)
CABLE.set_children([CHILD])
CABLE.get_power_in()
print('Test Cable Power: '+ str(CABLE.power_in.power))

if __name__ == "__main__":
    main()


# test = Cable([0,0,0])
# # print(test._CABLE_SIZE)
#
# print(test._CABLE_SIZE[0]['area'])

# for i, v in enumerate(test._CABLE_SIZE):
#     print(i, v['area'])

