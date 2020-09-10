from core.component import Component
from core.power import Power


class Transmission(Component):
    def __init__(self):
        super.__init__()


class Transformer(Transmission):
    def __init__(self, efficiency):
        super.__init__()
        self.efficiency = efficiency
