from core.component import Component
from core.power import ThreePhase
from core.power import DirectCurrent
import csv


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
        voltage_level_in = 0
        # TODO Actually make this correct
        self.power_out = ThreePhase(1, 2, 3, 4)  # for testing purposes
        self.power_in = ThreePhase(self.power_out.power / self.efficiency,
                                   voltage_level_in,
                                   self.power_out.frequency,
                                   self.power_out.power_factor)
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
        self.num_conductors = 0  # so we know it hasn't been calculated yet
        self.voltage_drop_percent = 0
        if not bool(self._CABLE_SIZE):
            self.load_data()

    def get_power_in(self, load_case_num):
        super().get_power_in(load_case_num)
        self.power_in = self.power_out.copy()
        if load_case_num == 0:
            self.set_distance()
            self.set_cable_size()
        self.power_in.resistance_loss(self.resistance)
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
            else:
                self.num_conductors += 1
        self.num_conductors -= 1  # subtract 1 for now -> yields correct answer
        # this while loop could be rewritten for better practices and readability

        # This section calculates the resistance per m using the cross sectional area of the conductors
        resistivity_copper = 1.724 * 10 ** (-8)  # Ohm*m TODO: Find source for resistivity
        core_temp = 20  # degree C
        rated_temp = 85  # degree C
        alpha_temp_coeff = 0.00429  # TODO: Find source for Alpha
        resistivity_copper_rated_temp = resistivity_copper * (
                1 + alpha_temp_coeff * (rated_temp - core_temp))  # Ohm*m
        resistance_per_meter = resistivity_copper_rated_temp / (
                float(self._CABLE_SIZE[selected_size_index]['area']) / (1000 ** 2))  # Ohm/m

        self.resistance = resistance_per_meter * self.length / self.num_conductors  # Check EE

        # TODO: write if statement to determine if cable three phase or single phase/DC and do weight correctly
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
            if float(cable_size['XLPE']) > self.power_out.current / self.num_conductors and \
                    self.voltage_drop_percent <= 0.3:
                selected_size_index = index
                return selected_size_index
        return -1

    def set_distance(self):
        start_location = self.get_parents().location
        end_location = self.get_children()[0].location

        # This finds the longitudinal distance in meters between the parent and child of the cable
        long_distance = end_location[0] - start_location[0]

        # This find the transverse length of cable in meters assuming the
        # cable will run from the child and parent all the way to centerline before running longitudinally
        tran_distance = abs(end_location[1]) + abs(start_location[1])

        # This finds the longitudinal distance in meters between the parent and child of the cable
        vert_distance = end_location[2] - start_location[2]

        # This sets the total length of cable needed
        self.length = abs(long_distance) + abs(tran_distance) + abs(vert_distance)


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
