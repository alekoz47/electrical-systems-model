from core.component import Component
from core.power import Power
import numpy

class Source(Component):
    def __init__(self, location, power):
        super().__init__(location)
        self.power_in = power

    def get_power_in(self):  # TODO Check that this is correct
        pass


# TODO: implement electrical-mechanical power transfer
#   this means we need both a Diesel and a Generator
class DieselGenerator(Source):
    def __init__(self, location, rated_power_electric, gen_efficiency=0.97):
        super().__init__(location, rated_power_electric)
        self.rated_power = rated_power_electric
        self.MCR = power_electric / gen_efficiency

    def SFOC_curve(self, percent_load):
        '''
        This SFOC curve is for Man D&T L21/31 Diesel Generator at 1000rpm
        The data for the SFOC points can be found on page 139 of the L21/31 project guide
        '''

        loads = [0.25, 0.50, 0.75, 0.85, 1]
        fuel_consumption = [216, 196, 192, 191, 193]
        coefs = numpy.polyfit(loads, fuel_consumption, len(loads) - 1)
        SFOC = coefs[0] * percent_load ** 4 + coefs[1] * percent_load ** 3 + coefs[2] * percent_load ** 2 + coefs[
        3] * percent_load + coefs[4]
        return SFOC

    def get_SFOC(self, power_wanted):
        self.percent_load = power_wanted / self.rated_power
        if self.percent_load > 1:
            print('Generator is overloaded: ' + str(self.percent_load * 100) + '%')
        self.SFOC = self.SFOC_curve(self.percent_load)



class LowSpeedDiesel(Source):








# page 139 for SFOC for L21/31