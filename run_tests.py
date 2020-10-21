# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Geolearn
# https://github.com/GeolearnAI/CAES
#
# This file is part of CAES.
# Licensed under the terms and conditions defined in file 'LICENSE.txt',
# which is distributed along with this program.
# -----------------------------------------------------------------------------

from params import config
from caes.core import CAES
import matplotlib.pyplot as plt

test = CAES(config)
test.plot_injection_extraction()
plt.plot(test.calculate_air_density())
plt.show()
plt.plot(test.calculate_temperature())
plt.show()
plt.plot(test.calculate_pressure())
plt.show()
plt.plot(test.calculate_leakage())
plt.show()
test.start_workflow()

