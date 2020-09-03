from core.component import Component
from core.power import Power


class Transmission(Component):
    def __init__(self):
        self.power_out = None
        self.power_in = None
