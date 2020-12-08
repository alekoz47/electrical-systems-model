import time

from core.model import Model
from core.sink import ElectricalSink

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
    start = time.time()
    model.build()
    build_time = time.time() - start
    model.print_tree()
    model.export_tree()

    start = time.time()
    root_powers = model.solve(load_cases)
    solve_time = time.time() - start

    for case in load_cases:
        print("Load Case " + case + ": " + format_power(root_powers.pop()))
    print('\n')

    components = model.export_components()
    for comp in components:
        print_component_info(comp)

    print("Model Evaluation Times")
    print("Build Time: " + str("%.0f" % (build_time * 1000)) + " ms")
    print("Solve Time: " + str("%.0f" % (solve_time * 1000)) + " ms")

    
if __name__ == "__main__":
    main()
