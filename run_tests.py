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
test.start_workflow()
ml_config1 = test.ml


config2 = config
config2.RESERVOIR_RADIUS = 20
test = CAES(config2)
test.start_workflow()
ml_config2 = test.ml


fig,ax = plt.subplots()
ax.plot(ml_config1,'r')
ax.plot(ml_config2,'b')

# radius_range = [5,10,20,30]
# for r in radius_range:
#     config.RESERVOIR_RADIUS = r
#     test = CAES(config)
#     test.plot_leakage(test.calculate_leakage())
