from core.component import Component
from core.power import Power


class Transmission(Component):
    def __init__(self, parents, children):
        super().__init__(parents, children)


class Transformer(Transmission):
    def __init__(self, efficiency):
        super().__init__(parents, children)
        self.efficiency = efficiency
