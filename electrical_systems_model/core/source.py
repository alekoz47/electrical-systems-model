import csv
import numpy
import pandas as pd
import numpy as np
from core.component import Component
from abc import abstractmethod
from core.power import PowerInterface


class Source(Component):
    def __init__(self, location, power):
        super().__init__(location)
        self.power_in = power

    def get_power_in(self):  # TODO Check that this is correct
        pass

    @abstractmethod
    def constraint(self):
        pass

    @abstractmethod
    def type_name(self):
        pass




class HighSpeedDiesel(Source):
    engine_row = 0 # This is currently #####
    engine_data = None

    def __init__(self, location, power):
        super().__init__(location, power)
        self.power_brake = power
        self.percent_load = None
        self.SFOC = None
        self.NOX_rate = None
        self.SOX_rate = None
        self.CO2_rate = None
        self.power = None
        self.fuel_consumption = None
        if not self.engine_data:
            self.emission_curves()

    def emission_curves(self):
        data = '../data/Cat_engine_data.csv' # Need to add back slashes!!!
        self.engine_data = pd.read_csv(data)
        self.engine_data.head()
        self.engine_data.set_index('Engine', inplace=True)

    @abstractmethod
    def set_power_level(self, mechanical_power, electrical_power):
        pass

    def get_emissions(self):
        self.solve_emissions()
        return self.CO2_eq_rate

    def solve_emissions(self):
        self.solve_fuel_consumption()
        self.solve_NOX()
        self.solve_CO()
        self.solve_HC()
        self.solve_CO2()
        self.solve_PM()
        self.solve_CO2_eq()

    def solve_fuel_consumption(self):
        self.SFOC_data = pd.DataFrame(data={'engine_load': [1, 0.9, 0.8, 0.75, 0.7, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.1],
                                       'SFOC': 608.3 * self.engine_data.iloc[self.engine_row][
                                           ['100% BSFC', '90% BSFC', '80% BSFC', '75% BSFC', '70% BSFC', '60% BSFC',
                                            '50% BSFC', '40% BSFC', '30% BSFC', '25% BSFC', '20% BSFC', '10% BSFC']]})
        SFOC_data_fit = np.polyfit(self.SFOC_data['engine_load'], self.SFOC_data['SFOC'], 2)
        self.SFOC = numpy.polyval(SFOC_data_fit, self.percent_load) # in g/kWh

        # self.SFOC = np.interp(self.percent_load, np.flip(self.SFOC_data['engine_load']), np.flip(self.SFOC_data['SFOC']))

        self.fuel_consumption = self.SFOC * self.power / (10**6) # in MT/hr

    def solve_NOX(self):
        self.NOX_data = pd.DataFrame(data={'engine_load': [1, 0.75, 0.5, 0.25, 0.1],
                                      'NOX': self.engine_data.iloc[self.engine_row][
                                                 ['100% NOX', '75% NOX', '50% NOX', '25% NOX', '10% NOX']]
                                             / np.multiply([1, 0.75, 0.5, 0.25, 0.1], 0.7457*self.engine_data.iloc[self.engine_row]['BHP'])})
        # 0.7457 converts BHP to BkW
        self.specific_NOX_rate = np.interp(self.percent_load, np.flip(self.NOX_data['engine_load']), np.flip(self.NOX_data['NOX'])) # in g/kWh
        self.NOX_rate = self.specific_NOX_rate * self.power # in g/hr

    def get_sox(self, power_wanted):
        # TODO Fix or remove this
        sox_specific_rate = 10  # Using standard SOX generation rate of 10g/kWh from L21/31 Project Guide
        self.sox_rate = power_wanted * sox_specific_rate  # This gives the sox generation rate in g/hr
        return self.sox_rate

    def solve_CO(self):
        CO_data = pd.DataFrame(data={'engine_load': [1, 0.75, 0.5, 0.25, 0.1],
                                     'CO': self.engine_data.iloc[self.engine_row][['100% CO', '75% CO', '50% CO', '25% CO', '10% CO']]
                                           / np.multiply([1, 0.75, 0.5, 0.25, 0.1],
                                                         0.7457*self.engine_data.iloc[self.engine_row]['BHP'])})
        self.CO_specific_rate = np.interp(self.percent_load, np.flip(CO_data['engine_load']), np.flip(CO_data['CO'])) # in g/kWh
        self.CO_rate = self.CO_specific_rate * self.power # in g/hr

    def solve_HC(self):
        self.HC_data = pd.DataFrame(data={'engine_load': [1, 0.75, 0.5, 0.25, 0.1],
                                     'HC': self.engine_data.iloc[self.engine_row][['100% HC', '75% HC', '50% HC', '25% HC', '10% HC']]
                                           / np.multiply([1, 0.75, 0.5, 0.25, 0.1], 0.7457*self.engine_data.iloc[self.engine_row]['BHP'])})
        self.HC_specific_rate = np.interp(self.percent_load, np.flip(self.HC_data['engine_load']), np.flip(self.HC_data['HC'])) # in g/kWh
        self.HC_rate = self.HC_specific_rate * self.power # in g/hr

    def solve_CO2(self):
        self.CO2_data = pd.DataFrame(data={'engine_load': [1, 0.75, 0.5, 0.25, 0.1],
                                      'CO2': self.engine_data.iloc[self.engine_row][
                                                 ['100% CO2', '75% CO2', '50% CO2', '25% CO2', '10% CO2']]
                                             / np.multiply([1, 0.75, 0.5, 0.25, 0.1], 0.7457*self.engine_data.iloc[self.engine_row]['BHP'])})
        CO2_data_fit = np.polyfit(self.CO2_data['engine_load'], self.CO2_data['CO2'], 4)
        self.CO2_specific_rate = np.polyval(CO2_data_fit, self.percent_load) # in kg/kWh
        self.CO2_rate = self.CO2_specific_rate * self.power # in kg/hr

    def solve_PM(self):
        PM_data = pd.DataFrame(data={'engine_load': [1, 0.75, 0.5, 0.25, 0.1],
                                     'PM': self.engine_data.iloc[self.engine_row][['100% PM', '75% PM', '50% PM', '25% PM', '10% PM']]
                                           / np.multiply([1, 0.75, 0.5, 0.25, 0.1], 0.7457*self.engine_data.iloc[self.engine_row]['BHP'])})
        self.PM_specific_rate = np.interp(self.percent_load, np.flip(PM_data['engine_load']), np.flip(PM_data['PM'])) # in g/kWh
        self.PM_rate = self.PM_specific_rate * self.power # in g/hr

    def solve_CO2_eq(self):
        # GWP come from Table ES-1 from Inventory of US Greenhouse Gas Emissions and Sinks: 1990-2019

        GWP_CH4 = 25
        GWP_N2O = 298

        CO2_eq = self.CO2_data['CO2'].reset_index(drop=True) + GWP_CH4 * self.HC_data['HC'].reset_index(
            drop=True) / 1000 + GWP_N2O * self.NOX_data['NOX'].reset_index(drop=True) / 1000
        CO2_eq_data = pd.DataFrame(data={'engine_load': [1, 0.75, 0.5, 0.25, 0.1], 'CO2_eq': CO2_eq})

        self.CO2_eq_specific_rate = np.interp(self.percent_load, np.flip(CO2_eq_data['engine_load']), np.flip(CO2_eq_data['CO2_eq'])) # in kg/kWh
        self.CO2_eq_rate = self.CO2_eq_specific_rate * self.power # kg/hr

    @abstractmethod
    def constraint(self, constraints, index):
        pass

    def type_name(self):
        pass

class DieselGenerator(HighSpeedDiesel):
    def __init__(self, location, power, generator_efficiency=0.95):
        super().__init__(location, power)
        self.generator_efficiency = generator_efficiency

    def set_power_level(self, mechanical_power_wanted, electric_power_wanted):
        self.power = electric_power_wanted / self.generator_efficiency
        self.percent_load = self.power / self.power_brake
        self.solve_emissions()

    def constraint(self, constraints, index):
        def electrical_overload_constraint(engine_loading):
            # Need to think of a way to pass the index of the current engine to this function
            mechanical_power_wanted = 0
            electrical_power_wanted = engine_loading[2*index + 1] # need to check this
            self.set_power_level(mechanical_power_wanted, electrical_power_wanted)
            return self.power_brake - self.power

        def electrical_zero_load_constraint(engine_loading):
            mechanical_power_wanted = 0
            electrical_power_wanted = engine_loading[2*index + 1]  # need to check this
            self.set_power_level(mechanical_power_wanted, electrical_power_wanted)
            return self.power

        def mechanical_load_constraint_1(engine_loading):
            mechanical_power_wanted = engine_loading[2*index] # need to check
            return 1-mechanical_power_wanted

        def mechanical_load_constraint_2(engine_loading):
            mechanical_power_wanted = engine_loading[2*index] # need to check
            return 1+mechanical_power_wanted



        constraints.append({
            'type': 'ineq',
            'fun': electrical_overload_constraint
        })

        constraints.append({
            'type': 'ineq',
            'fun': electrical_zero_load_constraint
        })

        constraints.append({
            'type': 'ineq',
            'fun': mechanical_load_constraint_1
        })

        constraints.append({
            'type': 'ineq',
            'fun': mechanical_load_constraint_2
        })

        return constraints

    def type_name(self):
        return 'Diesel Generator'

class DieselMechanical(HighSpeedDiesel):
    def __init__(self, location, power, shaftline_efficiency=0.99):
        super().__init__(location, power)
        self.shaftline_efficiency = shaftline_efficiency

    def set_power_level(self, mechanical_power_wanted, electrical_power_wanted):
        self.power = mechanical_power_wanted / self.shaftline_efficiency
        self.percent_load = self.power / self.power_brake
        self.solve_emissions()

    def constraint(self, constraints, index):

        def mechanical_overload_constraint(engine_loading):
            # Need to think of a way to pass the index of the current engine to this function
            mechanical_power_wanted = engine_loading[2 * index]
            electrical_power_wanted = 0
            self.set_power_level(mechanical_power_wanted, electrical_power_wanted)
            return self.power_brake - self.power

        def mechanical_zero_load_constraint(engine_loading):
            mechanical_power_wanted = engine_loading[2 * index]
            electrical_power_wanted = 0 # need to check this
            self.set_power_level(mechanical_power_wanted, electrical_power_wanted)
            return self.power

        def electrical_load_constraint_1(engine_loading):
            electrical_power_wanted = engine_loading[2 * index + 1]
            return 1-electrical_power_wanted

        def electrical_load_constraint_2(engine_loading):
            electrical_power_wanted = engine_loading[2 * index + 1]
            return 1+electrical_power_wanted



        constraints.append({
            'type': 'ineq',
            'fun': mechanical_overload_constraint
        })

        constraints.append({
            'type': 'ineq',
            'fun': mechanical_zero_load_constraint
        })

        constraints.append({
            'type': 'ineq',
            'fun': electrical_load_constraint_1
        })

        constraints.append({
            'type': 'ineq',
            'fun': electrical_load_constraint_2
        })

        return constraints

    def type_name(self):
        return 'Diesel Mechanical'

class DieselShaftGenerator(HighSpeedDiesel):
    def __init__(self, location, power, shaftline_efficiency_before_alternator=0.99, shaftline_efficiency_after_alternator=0.99, generator_efficiency=0.95):
        super().__init__(location, power)
        self.shaftline_efficiency_before_alternator = shaftline_efficiency_before_alternator
        self.shaftline_efficiency_after_alternator = shaftline_efficiency_after_alternator
        self.generator_efficiency = generator_efficiency

    def set_power_level(self, mechanical_power_wanted, electrical_power_wanted):
        self.power = (mechanical_power_wanted/self.shaftline_efficiency_after_alternator + electrical_power_wanted/self.generator_efficiency) / self.shaftline_efficiency_before_alternator
        self.percent_load = self.power / self.power_brake
        self.solve_emissions()

    def bound(self, bounds):
        mechanical_bound = (0, self.power_brake * self.shaftline_efficiency_before_alternator * self.shaftline_efficiency_after_alternator)
        bounds.append(mechanical_bound)
        electrical_bound = (0, self.power_brake * self.shaftline_efficiency_before_alternator * self.generator_efficiency)
        bounds.append(electrical_bound)
        return bounds

    def type_name(self):
        return 'Shaft Generator'


class LowSpeedDiesel(Source):
    _ENGINE_DATABASE = []

    def __init__(self, location, needed_ehp, design_rpm, design_speed, vessel_speeds, propulsive_coef=0.68,
                 shafting_loss=0.01, sea_margin=1.15, engine_margin=0.9):
        super().__init__(location, 0)  # TODO Figure out what power in needs to be (not zero)
        if not bool(self._ENGINE_DATABASE):
            self.load_data()
        self.MCR = self.find_mcr(needed_ehp, propulsive_coef, shafting_loss, sea_margin, engine_margin)
        self.NCR = self.MCR * engine_margin
        self.MCR_rpm = self.find_mcr_rpm(design_rpm, sea_margin, engine_margin)
        self.propulsive_coef = propulsive_coef
        self.shafting_loss = shafting_loss
        self.sea_margin = sea_margin
        self.engine_margin = engine_margin

        self.potential_engine = []
        self.select_potential_engines()
        self.get_SFOC_at_SMCR()

        # TODO add in selection from different speeds 4.0 for fast, 3.5 for medium, 3.2 for low
        self.speed_relationship = 3.5
        self.speed_constant = self.NCR / design_speed ** self.speed_relationship

        self.load_case_powers = []
        self.get_required_power(vessel_speeds)
        # TODO add method to solve for emissions and fuel consumption for a given load case

        self.percent_load = None
        self.SFOC = None
        self.nox_rate = None
        self.sox_rate = None
        self.co2_rate = None

    def evaluate_load_case(self, load_case_num):
        # This method should return fuel burn rate, nox rate, sox rate
        self.get_SFOC_at_power(self.load_case_powers[load_case_num])
        list_of_fuel_consumptions = []
        for engine in self.potential_engine:
            fuel_consumption = self.load_case_powers[load_case_num] * engine['Load Case SFOC'] / (1000 * 1000)
            # fuel consumption is given in MT/hr
            list_of_fuel_consumptions.append(fuel_consumption)
        self.potential_engine = self.append_od(self.potential_engine, list_of_fuel_consumptions,
                                               'Load Case Fuel Consumption')

    def find_mcr(self, needed_ehp, propulsive_coef, shafting_loss, sea_margin, engine_margin):
        needed_dhp = needed_ehp / propulsive_coef
        needed_MCR = needed_dhp * sea_margin / engine_margin / (1 - shafting_loss)
        print(needed_MCR)
        return needed_MCR

    def find_mcr_rpm(self, design_rpm, sea_margin, engine_margin):
        heavy_running_rpm_dp = 0.95 * design_rpm
        rpm_sp = heavy_running_rpm_dp * sea_margin ** (1 / 3)
        rpm_mp = rpm_sp * (1 / engine_margin) ** (1 / 3)
        return rpm_mp

    def load_data(self):
        data_path = '../data/MAN_engines.csv'
        with open(data_path) as file:
            data = csv.DictReader(file)
            for row in data:
                for cell in row:
                    try:
                        row[cell] = float(row[cell])
                    except ValueError:
                        pass
                self._ENGINE_DATABASE.append(row)

    def select_potential_engines(self):
        list_of_cylinder = []
        for index, engine in enumerate(self._ENGINE_DATABASE):
            for num_cylinder in range(int(engine['Zmin']), int(engine['Zmax'])):
                min_MCR = num_cylinder * (engine['L2'] - engine['L4']) / (
                        engine['nmax'] - engine['nmin']) * self.MCR_rpm + engine['L4']
                max_MCR = num_cylinder * (engine['L1'] - engine['L3']) / (
                        engine['nmax'] - engine['nmin']) * self.MCR_rpm + engine['L3']
                if self.MCR_rpm > engine['nmin'] and self.MCR_rpm < engine['nmax'] and self.MCR > min_MCR and self.MCR < max_MCR:
                    self.potential_engine.append(engine)
                    list_of_cylinder.append(num_cylinder)
        self.potential_engine = self.append_od(self.potential_engine, list_of_cylinder, 'Cylinders')

    def calculate_mep(self, engine, power, rpm):
        calculated_mep = 60 / 100 * power / (
                engine['Stroke'] * numpy.pi * engine['Bore'] ** 2 / 4 * rpm * engine['Cylinders'])
        return calculated_mep

    def get_SFOC_at_SMCR(self):
        list_SFC_SMCR = []
        for engine in self.potential_engine:
            MEP_SMCR = self.calculate_mep(engine, self.MCR, self.MCR_rpm)
            MEP_NMCR = self.calculate_mep(engine, engine['L1'] * engine['Cylinders'], engine['nmax'])
            MEP_norm = MEP_SMCR / MEP_NMCR
            rpm_norm = self.MCR_rpm / engine['nmax']

            # TODO Add citation for source of equation
            a00 = 0.8342
            a10 = -0.0009009
            a01 = 0.1665

            SFC_N = a00 + a10 * rpm_norm + a01 * MEP_norm
            SFC_SMCR = engine['SFOC NMCR'] * SFC_N
            list_SFC_SMCR.append(SFC_SMCR)
        self.potential_engine = self.append_od(self.potential_engine, list_SFC_SMCR, 'SFOC SMCR')

    def get_SFOC_at_power(self, power):
        list_SFOC_at_power = []

        for engine in self.potential_engine:
            # TODO Cite Source
            P_B = power / self.MCR

            mu = 0.55
            sigma = 0.2739
            x = (P_B - mu) / sigma
            list_of_factors = [0, 5.533, -8.209, -13.29, 20.94, 25.25, -36.64, 986.3]
            SFCs = numpy.polyval([item / 1000 for item in list_of_factors], x)
            SFOC_at_power = engine['SFOC SMCR'] * SFCs
            list_SFOC_at_power.append(SFOC_at_power)
        self.potential_engine = self.append_od(self.potential_engine, list_SFOC_at_power, 'Load Case SFOC')

    def get_required_power(self, vessel_speeds):
        list_of_powers = []
        for speed in vessel_speeds:
            power = self.speed_constant * speed ** self.speed_relationship
            list_of_powers.append(power)
        self.load_case_powers = list_of_powers

    def append_od(self, ordered_dic, added_list, key):
        for index, value in enumerate(ordered_dic):
            value[key] = added_list[index]
        return ordered_dic













