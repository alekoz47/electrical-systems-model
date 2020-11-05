import csv
import numpy

from core.component import Component
from core.power import Power


class Source(Component):
    def __init__(self, location, power):
        super().__init__(location)
        self.power_in = power

    def get_power_in(self):  # TODO Check that this is correct
        pass


# TODO: implement electrical-mechanical power transfer
#   this means we need both a Diesel and a Generator
class DieselGenerator(Source):
    def __init__(self, location, rated_power_electric, gen_efficiency=0.965):
        super().__init__(location, rated_power_electric)
        self.rated_power = rated_power_electric
        self.MCR = rated_power_electric / gen_efficiency
        self.percent_load = None
        self.SFOC = None
        self.nox_rate = None
        self.sox_rate = None
        self.co2_rate = None

    def SFOC_curve(self, percent_load):
        '''
        This SFOC curve is for Man D&T L21/31 Diesel Generator at 1000rpm
        The data for the SFOC points can be found on page 139 of the L21/31 project guide
        '''

        loads = [0.25, 0.50, 0.75, 0.85, 1]
        fuel_consumption = [216, 196, 192, 191, 193]
        coefs = numpy.polyfit(loads, fuel_consumption, len(loads) - 1)
        SFOC = numpy.polyval(coefs, percent_load)
        return SFOC

    def get_SFOC(self, power_wanted):
        self.percent_load = power_wanted / self.rated_power
        if self.percent_load > 1:
            print('Generator is overloaded: ' + str(self.percent_load * 100) + '%')
        self.SFOC = self.SFOC_curve(self.percent_load)

    def get_nox(self, power_wanted):
        nox_specific_rate = 10  # Using standard NOX generation rate of 10g/kWh from L21/31 Project Guide
        self.nox_rate = power_wanted * nox_specific_rate  # This gives the nox generation rate in g/hr
        return self.nox_rate

    def get_sox(self, power_wanted):
        sox_specific_rate = 10  # Using standard SOX generation rate of 10g/kWh from L21/31 Project Guide
        self.sox_rate = power_wanted * sox_specific_rate  # This gives the sox generation rate in g/hr
        return self.sox_rate

    def get_co2(self, power_wanted):
        co2_specific_rate = 590  # Using standard CO2 generation rate of 10g/kWh from L21/31 Project Guide
        self.co2_rate = power_wanted * co2_specific_rate  # This gives the co2 generation rate in g/hr
        return self.co2_rate

class LowSpeedDiesel(Source):
    _ENGINE_DATABASE = []

    def __init__(self, location, needed_ehp, design_rpm, design_speed, vessel_speeds, propulsive_coef = 0.68, shafting_loss = 0.01, sea_margin = 1.15, engine_margin = 0.9):
        super().__init__(location, 0) # TODO Figure out what power in needs to be (not zero)
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
            fuel_consumption = self.load_case_powers[load_case_num] * engine['Load Case SFOC'] / (1000*1000)
            # fuel consumption is given in MT/hr
            list_of_fuel_consumptions.append(fuel_consumption)
        self.potential_engine = self.append_od(self.potential_engine, list_of_fuel_consumptions, 'Load Case Fuel Consumption')



    def find_mcr(self, needed_ehp, propulsive_coef, shafting_loss, sea_margin, engine_margin):
        needed_dhp = needed_ehp / propulsive_coef
        needed_MCR = needed_dhp * sea_margin / engine_margin / (1 - shafting_loss)
        print(needed_MCR)
        return needed_MCR

    def find_mcr_rpm(self, design_rpm, sea_margin, engine_margin):
        heavy_running_rpm_dp = 0.95 * design_rpm
        rpm_sp = heavy_running_rpm_dp * sea_margin ** (1/3)
        rpm_mp = rpm_sp * (1/engine_margin) ** (1/3)
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
                min_MCR = num_cylinder * (engine['L2'] - engine['L4']) / (engine['nmax'] - engine['nmin']) * self.MCR_rpm + engine['L4']
                max_MCR = num_cylinder * (engine['L1'] - engine['L3']) / (engine['nmax'] - engine['nmin']) * self.MCR_rpm + engine['L3']
                if self.MCR_rpm > engine['nmin'] and self.MCR_rpm < engine['nmax'] and self.MCR > min_MCR and self.MCR < max_MCR:
                    self.potential_engine.append(engine)
                    list_of_cylinder.append(num_cylinder)
        self.potential_engine = self.append_od(self.potential_engine, list_of_cylinder, 'Cylinders')

    def calculate_mep(self, engine, power, rpm):
        calculated_mep = 60/100 * power / (engine['Stroke'] * numpy.pi * engine['Bore']**2/4 * rpm * engine['Cylinders'])
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













