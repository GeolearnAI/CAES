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

test = CAES(config)
test.plot_injection_extraction()
test.plot_pressure(test.calculate_pressure())
test.plot_temperature(test.calculate_temperature())
test.plot_leakage(test.calculate_leakage())
test.start_workflow()

