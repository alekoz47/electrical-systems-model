from core.component import Component
from core.power import Power


class Source(Component):
    def __init__(self, location, power):
        super().__init__(location)
        self.power_in = power

    def get_power_in(self):
        pass


# TODO: implement electrical-mechanical power transfer
#   this means we need both a Diesel and a Generator
class Generator(Source):
    def __init__(self, location, power):
        super().__init__(location, power)
