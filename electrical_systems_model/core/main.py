from core.model import Model
from core.sink import ElectricalSink
from core.transmission import Cable


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
    print('\n')


def format_power(power):
    return "%.1f" % abs(power.power / 1000) + " kW"


def main():

    load_cases = ["0", "1", "2", "3", "4"]
    model = Model()
    model.build()
    model.print_tree()

    root_powers = model.solve(load_cases)

    for case in load_cases:
        print("Load Case " + case + ": " + format_power(root_powers.pop()))
    print('\n')

    components = model.export_components()
    for comp in components:
        print_component_info(comp)


if __name__ == "__main__":
    main()
