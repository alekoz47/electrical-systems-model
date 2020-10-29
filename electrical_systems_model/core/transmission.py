import csv

import numpy

from core.component import Component
from core.power import ThreePhase
from core.power import DirectCurrent
from helpers.math_utils import taxicab_ship_distance


class Transmission(Component):

    def __init__(self, location):
        super().__init__(location)

    def get_power_in(self, load_case_num):
        self.power_out = self.get_power_out(load_case_num)
        self.power_in = self.power_out.copy()
        return self.power_in


class Transformer(Transmission):

    def __init__(self, location, voltage_in, efficiency=0.97):
        super().__init__(location)
        self.voltage_in = voltage_in
        self.voltage_out = 0  # so we can track voltage_out in get_power_in
        self.efficiency = efficiency

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        self.voltage_out = self.power_out.voltage
        self.power_in = self.power_out.copy()
        self.power_in.efficiency_loss(self.efficiency)
        self.power_in.voltage = self.voltage_in
        return self.power_in


class Panel(Transmission):

    def __init__(self, location, efficiency=1):
        super().__init__(location)
        self.efficiency = efficiency

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        self.power_in = self.power_out.copy()
        return self.power_in


class Cable(Transmission):
    _CABLE_SIZE = []
    flag = 0
    selected_size = 0

    def __init__(self, location):
        super().__init__(location)
        self.resistance = None
        # if self.flag = 0:
        #     self.load_data()
        #     flag = 1
        self.weight = 0  # TODO Move to parent class????
        self.length = 0
        self.voltage_drop_percent = 0
        if not bool(self._CABLE_SIZE):
            self.load_data()

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        self.power_in = self.power_out.copy()

        if load_case_num == 0:
            # print("solved cable: " + str(self.name))
            self.set_distance()
            self.set_cable_size()
        self.power_in.resistance_loss(
            numpy.sqrt(3) * self.resistance)  # TODO Check EE is correct and move the sqrt(3) to a better spot
        return self.power_in

    def load_data(self):
        data_path = '../data/abs_cable_size.csv'
        with open(data_path) as file:
            data = csv.DictReader(file)
            for line in data:
                self._CABLE_SIZE.append(line)

    def set_cable_size(self):
        self.num_conductors = 1
        selected_size_index = -1

        while selected_size_index == -1:
            selected_size_index = self.find_cable_size()
            if self.num_conductors > 50:
                print("Current is very high in " + self.name)
                # TODO: add behavior to split into branches in this case
                break
            else:
                self.num_conductors += 1
        self.num_conductors -= 1  # subtract one for now

        # This section calculates the resistance per m using the cross sectional area of the conductors
        resistivity_copper_20C = 1.724 * 10 ** (-8)  # Ohm*m TODO Find source for resistivity
        resistivity_temp = 20  # degree C
        rated_temp = 85  # degree C
        alpha_temp_coef = 0.00429  # TODO Find source for Alpha
        resistivity_copper_rated_temp = resistivity_copper_20C * (
                    1 + alpha_temp_coef * (rated_temp - resistivity_temp))  # Ohm*m
        resistance_per_meter = resistivity_copper_rated_temp / (
                    float(self._CABLE_SIZE[selected_size_index]['area']) / (1000 ** 2))  # Ohm/m

        self.resistance = resistance_per_meter * self.length / self.num_conductors  # Check EE

        # TODO write if statement to determine if cable three phase or single phase/DC and do weight correctly
        # This section finds the linear weight of the selected cable on a per core basis
        density_of_copper = 8.95  # mt/m^3
        linear_weight = density_of_copper * float(self._CABLE_SIZE[selected_size_index]['area']) / (1000 ** 2)

        if isinstance(self.power_in, ThreePhase):
            number_of_core = 3
            self.weight = self.num_conductors * number_of_core * linear_weight
        elif isinstance(self.power_in, DirectCurrent):
            number_of_core = 1
            self.weight = self.num_conductors * number_of_core * linear_weight

    def find_cable_size(self):
        for index, cable_size in enumerate(self._CABLE_SIZE):
            self.voltage_drop_percent = (self.power_out.current * float(self._CABLE_SIZE[index]['resistance']) *
                                         self.length / self.num_conductors) / self.power_out.voltage
            if float(cable_size['XLPE']) > self.power_out.current / self.num_conductors and self.voltage_drop_percent <= 0.3:
                selected_size_index = index
                return selected_size_index
        return -1

    def set_distance(self):
        start_location = self.get_parents().location
        end_location = self.get_children()[0].location
        self.length = taxicab_ship_distance(start_location, end_location)


class VFD(Transmission):
    def __init__(self, location, efficiency=0.9):
        super().__init__(location)
        self.efficiency = efficiency

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        self.power_in = self.power_out.copy()
        self.power_in.efficiency_loss(self.efficiency)
        return self.power_in


class Inverter(Transmission):
    def __init__(self, location, efficiency=0.9):
        super().__init__(location)
        self.efficiency = efficiency

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        self.power_in = DirectCurrent(self.power_out.power, self.power_out.voltage)
        self.power_in.efficiency_loss(self.efficiency)
        return self.power_in
