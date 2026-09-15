"""Short public import name for the LearnEnergy package.

The implementation remains in :mod:`learning_energy_model` for compatibility
with existing code. New projects can simply use ``import learnenergy``.
"""

import learning_energy_model as _legacy
from learning_energy_model import *

__version__ = _legacy.__version__
