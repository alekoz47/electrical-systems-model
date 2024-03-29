import time

from core.model import Model
from core.sink import ElectricalSink

from core.transmission import Cable, Transformer


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
    print("")


def print_cable_size(cable):
    print(cable.name)
    print(cable.selected_size)
    print(cable.num_conductors)
    print("")


def format_power(power):
    return "%.1f" % abs(power.power / 1000) + " kW"


def main():

    epla_path = "../../tests/inputs/EPLA_example_1.csv"
    load_cases = [0, 1, 2, 3, 4]
    model = Model()
    start = time.time()
    model.load_epla(epla_path)
    model.build()
    build_time = time.time() - start
    model.print_tree()

    start = time.time()
    root_powers = model.solve(load_cases)
    solve_time = time.time() - start

    cables = model.export_cables()
    print(cables)
    for cable in cables:
        print_cable_size(cable)

    model.export_tree(show_cables=True)
    model.export_tree(show_cables=False)

    for case in load_cases:
        print("Load Case " + str(case) + ": " + format_power(root_powers.pop()))
    print('\n')

    components = model.export_components()
    for comp in components:
        print_component_info(comp)

    print("Model Evaluation Times")
    print("Build Time: " + str("%.0f" % (build_time * 1000)) + " ms")
    print("Solve Time: " + str("%.0f" % (solve_time * 1000)) + " ms")


if __name__ == "__main__":
    main()
