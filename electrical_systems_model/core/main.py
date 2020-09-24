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
    transformer = Transformer([0, 0, 0], 440)
    cable2 = Cable([0, 0, 0])
    motor = ElectricalSink([0, 0, 0], 1000000, 220)
    components = [cable1, transformer, cable2, motor]
    cable1.name = "Cable 1"
    cable2.name = "Cable 2"
    transformer.name = "Transformer"
    motor.name = "Motor"
    model = Model()
    model.import_components(components)  # right now this just adds components in a straight hierarchy
    print("Test 1 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " W")
    model.print_tree()

    # # test adding some components and resolving
    # motor2 = ElectricalSink([0, 0, 0], 10000, 220, 0.8)
    # motor2.name = "Motor 2"
    # cable3 = Cable([0, 0, 0])
    # cable3.name = "Cable 3"
    # model.add_sink(cable3, 2)
    # model.add_sink(motor2, 5)
    # print("Test 2 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " W")
    # model.print_tree()
    #
    # motor3 = ElectricalSink([0, 0, 0], 10000, 220, 0.8)
    # motor3.name = "Motor 3"
    # cable4 = Cable([0, 0, 0])
    # cable4.name = "Cable 4"
    # model.add_sink(cable4, 2)
    # model.add_sink(motor3, 7)
    # print("Test 3 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " W")
    # model.print_tree()

    print_component_info(cable1)
    print("Resistance: " + str(cable1.resistance))
    print_component_info(transformer)
    print_component_info(cable2)
    print("Resistance: " + str(cable2.resistance))
    print_component_info(motor)


def print_component_info(comp):
    print(comp.name)
    print("Power in: " + str("%.1f" % abs(comp.power_in.power)) + " W")
    # print("Power out: " + str("%.1f" % abs(comp.power_out.power)) + " W")
    # print("Power drop: " + str("%.1f" % abs(comp.power_out.power - comp.power_in.power)) + " W")
    print("Voltage: " + str("%.1f" % abs(comp.power_in.voltage)) + " V")
    print("Current: " + str("%.1f" % abs(comp.power_in.current)) + " A")
    print(" \n")


if __name__ == "__main__":
    main()


test = Cable([0,0,0])
# print(test._CABLE_SIZE)

print(test._CABLE_SIZE[0]['area'])

# for i, v in enumerate(test._CABLE_SIZE):
#     print(i, v['area'])
