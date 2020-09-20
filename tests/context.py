import os
import sys
sys.path.insert(0, os.path.abspath("../electrical_systems_model/"))

from core.power import Power, ElectricPower, AlternatingCurrent, ThreePhase

from core.component import Component
from core.sink import Sink, ElectricalSink
from core.transmission import Transmission, Transformer, Cable

from core.model import Model

# import <module>

# use the following syntax for tests:
# from context import <module>
