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
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

class CAES(object):
    def __init__(self,config):
        self.config = config
        self.time = np.arange(0,self.config.TIME_END+1,
                                    self.config.TIME_STEP)
        self.mi = self.discretize_injection_rate()
        self.me = self.discretize_extraction_rate()

    def discretize_injection_rate(self):
        """
       Change injection function form .csv file to
            array of injection rate at a regular time step       
        """

        data = np.loadtxt(self.config.INJECTION_FILE, delimiter = ';')
        f = interp1d(data[:,0], data[:,1], bounds_error = False,
                                                 fill_value = data[-1,1])
        return f(self.time)
    
    def discretize_extraction_rate(self):
        """
        Change injection function form .csv file to
          array of extraction rate at a regular time step
         """
        data = np.loadtxt(self.config.EXTRACTION_FILE,delimiter = ';')
        f = interp1d(data[:,0], data[:,1] * -1 ,bounds_error = False,
                                         fill_value = data[-1,1])
        return f(self.time)

    
    def plot_injection_extraction(self):
        fig,ax = plt.subplots()
        ax.plot(self.time/3600, self.mi, 'b-')
        ax.plot(self.time/3600, self.me, 'r--')
        ax.set_xlabel('time (h)')
        ax.set_ylabel('mass rate (kg/s)')
        plt.legend(['injection', 'extraction'], loc='best')
        plt.show()
    
    def plot_temperature(self,temperature):
        fig,ax = plt.subplots()
        ax.plot(self.time/3600, temperature, 'b-')
        ax.set_xlabel('time (h)')
        ax.set_ylabel('Temperature (kg/s)')
        plt.show()
        
    def plot_pressure(self,pressure):
        fig,ax = plt.subplots()
        ax.plot(self.time/3600, pressure * 1e-6, 'b-')
        ax.set_xlabel('time (h)')
        ax.set_ylabel('Pressure (Mpa)')
        plt.show()
        
    def plot_leakage(self,leakage):
        fig,ax = plt.subplots()
        ax.plot(self.time/3600, leakage, 'b-')
        ax.set_xlabel('time (h)')
        ax.set_ylabel('Leakage rate (kg/s)')
        plt.show()

    def calculate_air_density(self, leakage_rate = 0):
        """
        from Equation1 of Zhou's article
        """
        temp1 = np.cumsum(self.mi*self.config.TIME_STEP)
        temp2 = np.cumsum(self.me*self.config.TIME_STEP)
        temp3 = np.cumsum(leakage_rate * self.config.TIME_STEP)
        
        rho =  self.config.INITIAL_AIR_DENSITY + (temp1 + temp2 -
                                      temp3) / self.config.CAVERN_VOLUME
        rho[rho < self.config.INITIAL_AIR_DENSITY] = (
                                self.config.INITIAL_AIR_DENSITY)
        
        return rho
    
    def calculate_temperature(self, leakage_rate=0, original_solution = False):
        """
        from Equation 2-4 of Zhou's article
        """
        if original_solution == True:
            ml=0
        else:
            ml = leakage_rate
        
        alpha = (self.mi * self.config.AIR_PRESSURE_SPECIFIC_HEAT * 
                                    self.config.TEMP_INJECTION)
        alpha += (self.config.HEAT_TRANSFER_COEFF * 
                                self.config.CAVERN_SURFACE_AREA * 
                                self.config.CAVERN_WALL_TEMPERATURE)
        alpha /= (self.mi * (self.config.SPECIFIC_AIR_CONSTANT - 
                                    self.config.AIR_PRESSURE_SPECIFIC_HEAT) +    
                         (self.me - ml) * 
                         self.config.SPECIFIC_AIR_CONSTANT - 
                         self.config.HEAT_TRANSFER_COEFF * 
                         self.config.CAVERN_SURFACE_AREA)
        
        beta = self.mi * (self.config.SPECIFIC_AIR_CONSTANT - 
                              self.config.AIR_PRESSURE_SPECIFIC_HEAT)
        beta += (self.me - ml) * self.config.SPECIFIC_AIR_CONSTANT
        beta -= (self.config.HEAT_TRANSFER_COEFF * 
                 self.config.CAVERN_SURFACE_AREA)
        beta /= (self.config.CAVERN_VOLUME * 
                self.calculate_air_density(leakage_rate) *
                                        self.config.AIR_VOLUME_SPECIFIC_HEAT)
        
        return (self.config.INITIAL_TEMP + alpha) * np.exp(beta * 
                                                           self.time) - alpha
    
    def calculate_pressure(self, leakage_rate=0, original_solution = False):
        """
        from Equation 5 of Zhou's article
        """
        p = (self.calculate_air_density(leakage_rate) * 
               self.config.SPECIFIC_AIR_CONSTANT * 
               self.calculate_temperature(leakage_rate, original_solution))
        #add condition from step 9 of Zhou's workflow
        p[p < self.config.RESERVOIR_EDGE_AIR_PRESSURE] = (
                                self.config.RESERVOIR_EDGE_AIR_PRESSURE)
        return p
    
    def calculate_leakage(self, leakage_rate = 0, original_solution = False):
        """
        From equation 8 of Zhou's article
        """

        num = (1.0967e-2 * self.config.ROCK_PERMEABILITY * 
               self.config.CAVERN_LENGTH * 
               (self.calculate_pressure(leakage_rate,original_solution)**2 - 
                                self.config.RESERVOIR_EDGE_AIR_PRESSURE**2))
        return num / (self.config.AIR_VISCOSITY * 
                      self.config.GAS_COMPRESSIBILITY_FACTOR * 
                  self.calculate_temperature(leakage_rate,original_solution) * 
                  np.log(self.config.RESERVOIR_RADIUS /
                                         self.config.EQUIVALENT_CAVERN_RADIUS))
         
        
        
    def start_workflow(self):
        """
        Iterative method from Zhou's article. Details of the workflow is 
        presented in Figure 4

        Returns
        -------
        None.

        """

# =============================================================================
#         Initial estimation
# =============================================================================
        
        ml = self.calculate_leakage()
        
# =============================================================================
#         #Basic iteration
#         #initialize delta to 1
# =============================================================================
        
        delta = 1
        i = 1
        while delta >= 1:
            temp = self.calculate_leakage(ml, original_solution = True)
            plt.plot(temp)
            plt.show()
            plt.plot(self.calculate_temperature(ml, True))
            plt.show()
            plt.plot(self.calculate_pressure(ml, True))
            plt.show()
            delta = np.mean(np.abs(temp - ml)) * 100
            print('Basic iteration no.{}'.format(str(i)))
            print('Error is {}%'.format(str(delta)))
            ml = temp
            i+=1
            
# =============================================================================
#             #Adjustment iteration
# =============================================================================
            
        delta=1
        i=1
        while delta >= 1:
            temp = self.calculate_leakage(ml)
            # plt.plot(temp)
            # plt.show()
            # plt.plot(self.calculate_temperature(ml))
            # plt.show()
            # plt.plot(self.calculate_pressure(ml))
            # plt.show()
            delta = np.mean(np.abs(temp - ml))*100
            print('Adjustment iteration no.{}'.format(str(i)))
            print('Error is {}%'.format(str(delta)))
            ml = temp
            i+=1
        
        
        
    