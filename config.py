
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Geolearn
# https://github.com/GeolearnAI/CAES
#
# This file is part of CAES.
# Licensed under the terms and conditions defined in file 'LICENSE.txt',
# which is distributed along with this program.
# -----------------------------------------------------------------------------



import numpy as np
#Path to files with extraction and injection schedule
INJECTION_FILE = 'injection_schedule.csv'
EXTRACTION_FILE = 'extraction_schedule.csv'

#From Table 2 of Zhou's article - Parameters for Pilot CAES test in Kamioka

CAVERN_LENGTH = 9 #(H) m
CAVERN_SURFACE_AREA = 211.5 #(Ac) m2
CAVERN_VOLUME = 222.75 #(V) m3
EQUIVALENT_CAVERN_RADIUS = 2.8068 #(r0) 
TEMP_INJECTION = 30.82 + 273#(Ti) °K
HEAT_TRANSFER_COEFF  = 30 #(hc) W/m2K
INITIAL_TEMP =  20 + 273#(T0, TRw) °K
ROCK_PERMEABILITY = 5e-14 #(k) m2 
ROCK_POROSITY = 0.1
AIR_VISCOSITY = 1.79e-5 #Pa.s
RESERVOIR_EDGE_AIR_PRESSURE = 1.0133e5 #(pe) Pa

#other test site parameters
INITIAL_AIR_DENSITY = 1.2754 #rho0 kg/m3
AIR_PRESSURE_SPECIFIC_HEAT = 1004 #(cp) J/(kg*K)
AIR_VOLUME_SPECIFIC_HEAT = 717 #(cv) J/(kg*K)
CAVERN_WALL_TEMPERATURE = 20 + 273 #(Trw) °K
SPECIFIC_AIR_CONSTANT = 286.7 #(R) J/(kg*K)
GAS_COMPRESSIBILITY_FACTOR = 1 #Z


#Other experiment variables

RESERVOIR_RADIUS = np.sqrt((ROCK_PERMEABILITY * 
                            RESERVOIR_EDGE_AIR_PRESSURE * 5000000)/(
                                ROCK_POROSITY * AIR_VISCOSITY))
# RESERVOIR_RADIUS = 500
#CALCULATION PARAMETERS
TIME_STEP = 1 #sec.
TIME_END = 720*60 #sec

