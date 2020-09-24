from core.model import Model
from core.sink import ElectricalSink
from core.transmission import Cable


def main():
    # test run of Motor -> Transformer -> Generator (root)
    # create data model
    # import data (this function currently uses test setup, no actual input implemented)
    # solve model
    model = Model()
    model.import_data("")
    print("Test 1 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " kW")
    model.print_tree()

    # test adding some components and resolving
    motor2 = ElectricalSink([0, 0, 0], 10, 120, 0.8)
    motor2.name = "Motor 2"
    cable3 = Cable([0, 0, 0])
    cable3.name = "Cable 3"
    model.add_sink(cable3, 2)
    model.add_sink(motor2, 5)
    print("Test 2 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " kW")
    model.print_tree()

    motor3 = ElectricalSink([0, 0, 0], 10, 120, 0.8)
    motor3.name = "Motor 3"
    cable4 = Cable([0, 0, 0])
    cable4.name = "Cable 4"
    model.add_sink(cable4, 2)
    model.add_sink(motor3, 7)
    print("Test 3 Power Output: " + str("%.1f" % abs(model.solve_model().power)) + " kW")
    model.print_tree()


if __name__ == "__main__":
    main()


test = Cable([0,0,0])
# print(test._CABLE_SIZE)

print(test._CABLE_SIZE[0]['area'])

# for i, v in enumerate(test._CABLE_SIZE):
#     print(i, v['area'])
