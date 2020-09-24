from core.component import Component
from core.power import ThreePhase
import csv


class Transmission(Component):

    def __init__(self, location):
        super().__init__(location)

    def get_power_in(self):
        self.power_out = self.get_power_out()
        self.power_in = self.power_out.copy()
        return self.power_in


class Transformer(Transmission):

    def __init__(self, location, voltage_in, efficiency=0.97):
        super().__init__(location)
        self.voltage_in = voltage_in
        self.voltage_out = 0  # so we can track voltage_out in get_power_in
        self.efficiency = efficiency

    def get_power_in(self):
        super().get_power_in()
        self.voltage_out = self.power_out.voltage
        self.power_in = self.power_out.copy()
        self.power_in.efficiency_loss(self.efficiency)
        self.power_in.voltage = self.voltage_in
        return self.power_in


class Panel(Transmission):

    def __init__(self, location, efficiency=0.97):
        super().__init__(location)
        self.efficiency = efficiency

    def get_power_in(self):
        super().get_power_in()
        voltage_level_in = 0
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
        self.weight = None  #TODO Move to parent class????
        if not bool(self._CABLE_SIZE):
            self.load_data()

    def get_power_in(self):
        super().get_power_in()
        self.power_in = self.power_out.copy()
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
        num_conductors = 1
        selected_size_index = -1
        length = 10  # TODO Test length of 10m, code length finder

        while selected_size_index == -1:
            selected_size_index = self.find_cable_size(num_conductors)
            if num_conductors > 50:
                print("Current is very high in " + self.name)
            else:
                num_conductors += 1
        num_conductors -= 1  # subtract one for now
        print(num_conductors)
        self.resistance = float(self._CABLE_SIZE[selected_size_index]['resistance']) * length / num_conductors  # Check EE
        self.weight = num_conductors * float(self._CABLE_SIZE[selected_size_index]['weight'])

    def find_cable_size(self, num_conductors):
        num_conductors = num_conductors
        for index, cable_size in enumerate(self._CABLE_SIZE):
            if float(cable_size['XLPE']) > self.power_out.current / num_conductors:
                selected_size_index = index
                #
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

        # This find the total length of cable needed
        length = abs(long_distance) + abs(tran_distance) + abs(vert_distance)
        print(length)


