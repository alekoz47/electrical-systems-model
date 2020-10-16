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
    transformer = Transformer([100, 12, 20], 440)
    motor = ElectricalSink([125, 3, 5], 10000, [1, 0.5, 0], 220, power_factor=0.8)
    components = [transformer, motor]
    motor.name = "Motor"
    transformer.name = "Transformer"
    model = Model()
    model.import_components(components)  # right now this just adds components in a straight hierarchy
    root_powers = model.solve_model(['Connected', 'At Sea'])
    print("Test 1 Power Output, Connected: " + str("%.1f" % abs(root_powers[0].power) + " W"))
    print("Test 1 Power Output, At Sea: " + str("%.1f" % abs(root_powers[1].power) + " W"))
    model.print_tree()

    print_component_info(transformer)
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


if __name__ == "__main__":
    main()
