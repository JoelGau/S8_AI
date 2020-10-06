#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 12:17:33 2020

@author: user
"""

import os
import sys
import time
import logging

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

from skfuzzy import control as ctrl
from gym import spaces, logger
from gym.utils import seeding
import math

def calcVitesse(Vx,Vy):
    return math.sqrt(Vx**2+Vy**2)

def calcCourbe(capteur):
    moygauche = np.mean(capteur[0:9])
    moydroite = np.mean(capteur[9:18])
    return (moydroite-moygauche)/100

def calcGear(Shift,currentGear):
    outGear = currentGear + Shift
    if outGear < 1:
        outGear = 1
    elif outGear > 6:
        outGear = 6
    return outGear

def calcConsignes(sim, observation, action):
    # Calculate variables
    vitesse = calcVitesse(observation["speed"][0], observation["speed"][1])
    courbe = calcCourbe(observation["track"])
    
    # Link inputs
    sim.input['Angle'] = observation["angle"][0]
    #sim.input['Trackpos'] = observation["trackPos"][0]
    sim.input['Vitesse'] = vitesse
    sim.input['RPM'] = observation["rpm"][0]
    sim.input['Courbe'] = courbe
    
    # Magic happens here
    sim.compute()
    
    # Link output
    action['accel'][0] = sim.output['Accel']
    action['brake'][0] = sim.output['Brake']
    action['steer'][0] = sim.output['Steer']
    action['gear'][0] = calcGear(sim.output['Shift'], observation['gear'][0])
    
    return action

def createFuzzyController():
    PI = math.pi
    
    # Input control
    angle = ctrl.Antecedent(np.linspace(-PI, PI, 10000), 'Angle')
    track_pos = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'Trackpos')
    vitesse = ctrl.Antecedent(np.linspace(0, 300, 301), 'Vitesse')
    rpm = ctrl.Antecedent(np.linspace(0, 10000, 10000), 'RPM')
    courbe = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'Courbe')
    
    # Create membership functions
    angle['AngleRealNeg'] = fuzz.trapmf(angle.universe, [-PI, -PI, -PI/2, -PI/4])
    angle['AngleNeg'] = fuzz.trapmf(angle.universe, [-3*PI/8, -PI/4, -PI/8, -PI/32])
    angle['AngleStraight'] = fuzz.trapmf(angle.universe, [-PI/16, 0, 0, PI/16])
    angle['AnglePos'] = fuzz.trapmf(angle.universe, [PI/32, PI/8, PI/4, 3*PI/8])
    angle['AngleRealPos'] = fuzz.trapmf(angle.universe, [PI/4, PI/2, PI, PI])
    
    vitesse['Low'] = fuzz.trapmf(vitesse.universe, [0,0,20,30])
    vitesse['Mid'] = fuzz.trapmf(vitesse.universe, [20,30,60,70])
    vitesse['High'] = fuzz.trapmf(vitesse.universe, [60,70,300,300])
    
    rpm['Low'] = fuzz.trapmf(rpm.universe, [0, 0, 1000, 2000])
    rpm['Mid'] = fuzz.trapmf(rpm.universe, [1000, 2000, 4000, 5000])
    rpm['High'] = fuzz.trapmf(rpm.universe, [4000, 5000, 10000, 10000]) 
    
    courbe['Straight'] = fuzz.trapmf(courbe.universe, [-0.5, -0.25, 0.25, 0.5])
    courbe['KinkedL'] = fuzz.trapmf(courbe.universe, [-1, -1, -0.75, -0.25])
    courbe['KinkedR'] = fuzz.trapmf(courbe.universe, [0.25, 0.75, 1, 1])

    # Output consigne
    shift = ctrl.Consequent(np.linspace(-3, 3, 7), 'Shift', defuzzify_method='centroid')
    steer = ctrl.Consequent(np.linspace(-1, 1, 1000), 'Steer', defuzzify_method='centroid')
    accel = ctrl.Consequent(np.linspace(0, 1, 1000), 'Accel', defuzzify_method='centroid')
    brake = ctrl.Consequent(np.linspace(0, 1, 1000), 'Brake', defuzzify_method='centroid')
    
    # Create membership functions
    shift['DownShift'] = fuzz.trapmf(shift.universe, [-3, -3, -1, -0.5])
    shift['NoShift'] = fuzz.trapmf(shift.universe, [-1, 0, 0, 1])
    shift['UpShift'] = fuzz.trapmf(shift.universe, [0.5, 1, 3, 3])
    
    steer['HardLeft'] = fuzz.trapmf(steer.universe, [-1, -1, -0.75, -0.5])
    steer['SoftLeft'] = fuzz.trapmf(steer.universe, [-0.75, -0.5, -0.25, 0])
    steer['Rest'] = fuzz.trapmf(steer.universe, [-0.25, 0, 0, 0.25])
    steer['SoftRight'] = fuzz.trapmf(steer.universe, [0, 0.25, 0.5, 0.75])
    steer['HardRight'] = fuzz.trapmf(steer.universe, [0.5, 0.75, 1, 1])

    accel['NoAccel'] = fuzz.trapmf(accel.universe, [0, 0, 0.25, 0.5])
    accel['YesAccel'] = fuzz.trapmf(accel.universe, [0.25, 0.5, 1, 1])
    
    brake['NoBrake'] = fuzz.trapmf(brake.universe, [0, 0, 0.25, 0.5])
    brake['YesBrake'] = fuzz.trapmf(brake.universe, [0.25, 0.5, 1, 1])
    
    # Define the rules.
    rules = []
    # rules.append(ctrl.Rule(antecedent=(ant1['AngleNeutre'] & ant2['VitNeutre']), consequent=cons1['ForceNeutre']))
    
    # Gear Shifting Rules
    rules.append(ctrl.Rule(antecedent=(rpm['Low']), consequent=shift['DownShift']))
    rules.append(ctrl.Rule(antecedent=(rpm['Mid']), consequent=shift['NoShift']))
    rules.append(ctrl.Rule(antecedent=(rpm['High']), consequent=shift['UpShift']))
    
    # Steering Rules
    rules.append(ctrl.Rule(antecedent=(angle['AngleRealPos'] & vitesse['Low']), consequent=steer['HardLeft']))
    rules.append(ctrl.Rule(antecedent=(angle['AnglePos'] & vitesse['Low']), consequent=steer['HardLeft']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleStraight'] & vitesse['Low']), consequent=steer['Rest']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleNeg'] & vitesse['Low']), consequent=steer['HardRight']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleRealNeg'] & vitesse['Low']), consequent=steer['HardRight']))

    rules.append(ctrl.Rule(antecedent=(angle['AngleRealPos'] & vitesse['Mid']), consequent=steer['SoftLeft']))
    rules.append(ctrl.Rule(antecedent=(angle['AnglePos'] & vitesse['Mid']), consequent=steer['HardLeft']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleStraight'] & vitesse['Mid']), consequent=steer['Rest']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleNeg'] & vitesse['Mid']), consequent=steer['HardRight']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleRealNeg'] & vitesse['Mid']), consequent=steer['SoftRight']))
    
    rules.append(ctrl.Rule(antecedent=(angle['AngleRealPos'] & vitesse['High']), consequent=steer['SoftLeft']))
    rules.append(ctrl.Rule(antecedent=(angle['AnglePos'] & vitesse['High']), consequent=steer['SoftLeft']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleStraight'] & vitesse['High']), consequent=steer['Rest']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleNeg'] & vitesse['High']), consequent=steer['SoftRight']))
    rules.append(ctrl.Rule(antecedent=(angle['AngleRealNeg'] & vitesse['High']), consequent=steer['SoftRight']))

    # Acceleration Rules
    rules.append(ctrl.Rule(antecedent=(courbe['Straight']), consequent=accel['YesAccel']))
    rules.append(ctrl.Rule(antecedent=((courbe['KinkedR'] | courbe['KinkedL']) & vitesse['Low']), consequent=accel['YesAccel']))
    rules.append(ctrl.Rule(antecedent=((courbe['KinkedR'] | courbe['KinkedL']) & (vitesse['High'] | vitesse['Mid'])), consequent=accel['NoAccel']))
    
    # Braking Rules
    rules.append(ctrl.Rule(antecedent=(courbe['Straight']), consequent=brake['NoBrake']))
    rules.append(ctrl.Rule(antecedent=((courbe['KinkedR'] | courbe['KinkedL']) & vitesse['Low']), consequent=brake['NoBrake']))
    rules.append(ctrl.Rule(antecedent=((courbe['KinkedR'] | courbe['KinkedL']) & (vitesse['High'] | vitesse['Mid'])), consequent=brake['YesBrake']))

    # Conjunction (and_func) and disjunction (or_func) methods for rules:
    #     np.fmin
    #     np.fmax
    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim