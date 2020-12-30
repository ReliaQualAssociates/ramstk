# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.db.common.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Common Database Module."""

# Standard Library Imports
import gettext
import os
from datetime import date, datetime, timedelta
from typing import Dict, Tuple

# Third Party Imports
from pubsub import pub
from sqlalchemy import exc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase
from ramstk.models.commondb import (
    RAMSTKRPN, RAMSTKCategory, RAMSTKCondition, RAMSTKFailureMode, RAMSTKGroup,
    RAMSTKHazards, RAMSTKLoadHistory, RAMSTKManufacturer, RAMSTKMeasurement,
    RAMSTKMethod, RAMSTKModel, RAMSTKSiteInfo, RAMSTKStakeholders,
    RAMSTKStatus, RAMSTKSubCategory, RAMSTKType, RAMSTKUser
)

_ = gettext.gettext

RAMSTK_CATEGORIES = {
    0: ('IC', 'Integrated Circuit', 'hardware', 1, 0.8, 0.9, 1.0, 1.0, 1.0,
        1.0, 0.0, 0.0, 125.0, 125.0),
    1: ('SEMI', 'Semiconductor', 'hardware', 1, 1.0, 1.0, 0.7, 0.9, 1.0, 1.0,
        0.0, 0.0, 125.0, 125.0),
    2: ('RES', 'Resistor', 'hardware', 1, 1.0, 1.0, 0.5, 0.9, 1.0, 1.0, 0.0,
        0.0, 125.0, 125.0),
    3: ('CAP', 'Capacitor', 'hardware', 1, 1.0, 1.0, 1.0, 1.0, 0.6, 0.9, 10.0,
        0.0, 125.0, 125.0),
    4: ('IND', 'Inductive Device', 'hardware', 1, 0.6, 0.9, 1.0, 1.0, 0.5, 0.9,
        15.0, 0.0, 125.0, 125.0),
    5: ('REL', 'Relay', 'hardware', 1, 0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
        125.0, 125.0),
    6: ('SW', 'Switching Device', 'hardware', 1, 0.75, 0.9, 1.0, 1.0, 1.0, 1.0,
        0.0, 0.0, 125.0, 125.0),
    7: ('CONN', 'Connection', 'hardware', 1, 0.7, 0.9, 1.0, 1.0, 0.7, 0.9,
        25.0, 0.0, 125.0, 125.0),
    8: ('MET', 'Meter', 'hardware', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
        125.0, 125.0),
    9: ('MISC', 'Miscellaneous', 'hardware', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        0.0, 0.0, 125.0, 125.0),
    10: ('INS', 'Insignificant', 'risk', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
         0.0, 0.0, 0.0),
    11: ('SLT', 'Slight', 'risk', 2, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
         0.0, 0.0),
    12: ('LOW', 'Low', 'risk', 3, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0,
         0.0),
    13: ('MED', 'Medium', 'risk', 4, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
         0.0, 0.0),
    14: ('HI', 'High', 'risk', 5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0,
         0.0),
    15: ('MAJ', 'Major', 'risk', 6, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
         0.0, 0.0),
    16: ('Batch (General)',
         'Can be run as a normal batch job and makes no unusual '
         'hardware or input-output actions (e.g., payroll '
         'program and wind tunnel data analysis program).  '
         'Small, throwaway programs for preliminary analysis '
         'also fit in this category.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0,
         1.0, 0.0, 0.0, 0.0, 0.0),
    17: ('Event Control', 'Does realtime processing of data resulting from '
         'external events. An example might be a computer '
         'program that processes telemetry data.', 'software', 1, 1.0, 1.0,
         1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    18: ('Process Control', 'Receives data from an external source and issues '
         'commands to that source to control its actions '
         'based on the received data.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0,
         1.0, 0.0, 0.0, 0.0, 0.0),
    19:
    ('Procedure Control', 'Controls other software; for example, an operating '
     'system that controls execution of time-shared and '
     'batch computer programs.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
     0.0, 0.0, 0.0, 0.0),
    20: ('Navigation', 'Does computation and modeling to computer '
         'information required to guide an airplane from '
         'point of origin to destination.', 'software', 1, 1.0, 1.0, 1.0, 1.0,
         1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    21:
    ('Flight Dynamics', 'Uses the functions computed by navigation software '
     'and augmented by control theory to control the '
     'entire flight of an aircraft.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0,
     1.0, 0.0, 0.0, 0.0, 0.0),
    22:
    ('Orbital Dynamics', 'Resembles navigation and flight dynamics software, '
     'but has the additional complexity required by '
     'orbital navigation, such as a more complex '
     'reference system and the inclusion of '
     'gravitational effects of other heavenly bodies.', 'software', 1, 1.0,
     1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    23: ('Message Processing',
         'Handles input and output mnessages. processing the '
         'text or information contained therein.', 'software', 1, 1.0, 1.0,
         1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    24: ('Diagnostic Software',
         'Used to detect and isolate hardware errors in the '
         'computer in which it resides or in other hardware '
         'that can communicate with the computer.', 'software', 1, 1.0, 1.0,
         1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    25: ('Sensor and Signal Processing',
         'Similar to that of message processing, except that '
         'it required greater processing, analyzing, and '
         'transforming the input into a usable data '
         'processing format.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
         0.0, 0.0, 0.0, 0.0),
    26: ('Simulation', 'Used to simulate and environment ieseion '
         'situation. other heavradlwuaatrieo,n aonfd a '
         'icnopmutps uftreo mpr otghreasme nt o enable a '
         'more realistic or a piece of hardware.', 'software', 1, 1.0, 1.0,
         1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    27: ('Database Management', 'Manages the storage and access of (typically '
         'large) groups of data. Such software can also '
         'often prepare reports in user-defined formats, '
         'based on the contents of the database.', 'software', 1, 1.0, 1.0,
         1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    28:
    ('Data Acquisition', 'Receives information in real-time and stores it in '
     'some form suitable format for later processing, '
     'for example, software that receives data from a '
     'space probe ,and files.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
     0.0, 0.0, 0.0, 0.0),
    29: ('Data Presentation', 'Formats and transforms data, as necessary, for '
         'convenient and understandable displays for '
         'humans.  Typically, such displays would be for '
         'some screen presentation.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0,
         1.0, 0.0, 0.0, 0.0, 0.0),
    30: ('Decision and Planning Aids',
         'Uses artificial intelligence techniques to provide '
         'an expert system to evaluate data and provide '
         'additional information and consideration for '
         'decision and policy makers.', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0,
         1.0, 0.0, 0.0, 0.0, 0.0),
    31:
    ('Pattern and Image Processing', 'Used for computer image generation and '
     'processing.  Such software may analyze terrain '
     'data and generate images based on stored data.', 'software', 1, 1.0, 1.0,
     1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    32: ('Computer System Software',
         'Provides services to operational computer '
         'programs (i.e., problem oriented).', 'software', 1, 1.0, 1.0, 1.0,
         1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    33: ('Software Development Tools',
         'Provides services to aid in the development of '
         'software (e.g., compilers, assemblers, static and '
         'dynamic analyzers).', 'software', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
         0.0, 0.0, 0.0, 0.0),
    34: ('HW', 'Hardware', 'incident', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
         0.0, 0.0, 0.0),
    35: ('SW', 'Software', 'incident', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
         0.0, 0.0, 0.0),
    36: ('PROC', 'Process', 'incident', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
         0.0, 0.0, 0.0),
    37: ('ENGD', 'Engineering, Design', 'action', 1, 1.0, 1.0, 1.0, 1.0, 1.0,
         1.0, 0.0, 0.0, 0.0, 0.0),
    38: ('ENGR', 'Engineering, Reliability', 'action', 1, 1.0, 1.0, 1.0, 1.0,
         1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    39: ('ENGS', 'Engineering, Systems', 'action', 1, 1.0, 1.0, 1.0, 1.0, 1.0,
         1.0, 0.0, 0.0, 0.0, 0.0),
    40: ('MAN', 'Manufacturing', 'action', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
         0.0, 0.0, 0.0, 0.0),
    41: ('TEST', 'Test', 'action', 1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
         0.0, 0.0),
    42: ('VANDV', 'Verification & Validation', 'action', 1, 1.0, 1.0, 1.0, 1.0,
         1.0, 1.0, 0.0, 0.0, 0.0, 0.0)
}

RAMSTK_CONDITIONS = {
    0: ('Cavitation', 'operating'),
    1: ('Cold Start', 'operating'),
    2: ('Contaminated Oil', 'operating'),
    3: ('Cyclic Loading, Low Cycle', 'operating'),
    4: ('Cyclic Loading, High Cycle', 'operating'),
    5: ('Emergency Stop', 'operating'),
    6: ('Full Load', 'operating'),
    7: ('High Idle', 'operating'),
    8: ('Hot Shutdown', 'operating'),
    9: ('Idle', 'operating'),
    10: ('Low End Torque', 'operating'),
    11: ('Mechanical Shock', 'operating'),
    12: ('Oil Pressure Fluctuations', 'operating'),
    13: ('Overload', 'operating'),
    14: ('Overspeed', 'operating'),
    15: ('Pressure Pulsations', 'operating'),
    16: ('Short Term Overload', 'operating'),
    17: ('Start-Stop', 'operating'),
    18: ('System Cool Down', 'operating'),
    19: ('System Warm Up', 'operating'),
    20: ('Thermal Cycling', 'operating'),
    21: ('Vibration', 'operating'),
    22: ('Abrasion', 'environmental'),
    23: ('Acceleration', 'environmental'),
    24: ('Corona', 'environmental'),
    25: ('Contamination, Chemicals', 'environmental'),
    26: ('Contamination, Dirt/Dust', 'environmental'),
    27: ('Contamination, Salt Spray', 'environmental'),
    28: ('Electrostatic Discharge', 'environmental'),
    29: ('Fungus', 'environmental'),
    30: ('Gas, Ionized', 'environmental'),
    31: ('Geomagnetics', 'environmental'),
    32: ('Humidity', 'environmental'),
    33: ('Ozone', 'environmental'),
    34: ('Pressure, Atmospheric', 'environmental'),
    35: ('Pressure', 'environmental'),
    36: ('Radiation, Alpha', 'environmental'),
    37: ('Radiation, Electromagnetic', 'environmental'),
    38: ('Radiation, Gamma', 'environmental'),
    39: ('Radiation, Neutron', 'environmental'),
    40: ('Radiation, Solar', 'environmental'),
    41: ('Shock, Mechanical', 'environmental'),
    42: ('Shock, Thermal', 'environmental'),
    43: ('Temperature', 'environmental'),
    44: ('Thermal Cycles', 'environmental'),
    45: ('Vibration, Acoustic', 'environmental'),
    46: ('Vibration, Mechanical', 'environmental'),
    47: ('Weather, Fog', 'environmental'),
    48: ('Weather, Freezing Rain', 'environmental'),
    49: ('Weather, Frost', 'environmental'),
    50: ('Weather, Hail', 'environmental'),
    51: ('Weather, Ice', 'environmental'),
    52: ('Weather, Rain', 'environmental'),
    53: ('Weather, Sleet', 'environmental'),
    54: ('Weather, Snow', 'environmental'),
    55: ('Weather, Wind', 'environmental')
}

RAMSTK_GROUPS = {
    1: ('RAMSTK Administrator', 'workgroup'),
    2: ('Engineering, Design', 'workgroup'),
    3: ('Engineering, Logistics Support', 'workgroup'),
    4: ('Engineering, Maintainability', 'workgroup'),
    5: ('Engineering, Reliability', 'workgroup'),
    6: ('Engineering, Safety', 'workgroup'),
    7: ('Engineering, Software', 'workgroup'),
    8: ('Reliability', 'affinity'),
    9: ('Durability', 'affinity'),
    10: ('Cost', 'affinity')
}

RAMSTK_FAILURE_MODES = {
    3: {
        25: {
            1: ['Open', 0.5, 'FMD-97'],
            2: ['Short', 0.3, 'FMD-97'],
            3: ['Parameter Change', 0.2, 'FMD-97']
        }
    }
}

RAMSTK_HAZARDS = {
    0: ('Acceleration/Gravity', 'Falls'),
    1: ('Acceleration/Gravity', 'Falling Objects'),
    3: ('Acceleration/Gravity', 'Fragments/Missiles'),
    4: ('Acceleration/Gravity', 'Impacts'),
    5: ('Acceleration/Gravity', 'Inadvertent Motion'),
    6: ('Acceleration/Gravity', 'Loose Object Translation'),
    7: ('Acceleration/Gravity', 'Slip/Trip'),
    8: ('Acceleration/Gravity', 'Sloshing Liquids'),
    9: ('Chemical/Water Contamination', 'Backflow/Siphon Effect'),
    10: ('Chemical/Water Contamination', 'Leaks/Spills'),
    11: ('Chemical/Water Contamination', 'System-Cross Connection'),
    12: ('Chemical/Water Contamination', 'Vessel/Pipe/Conduit Rupture'),
    13: ('Common Causes', 'Dust/Dirt'),
    14: ('Common Causes', 'Faulty Calibration'),
    15: ('Common Causes', 'Fire'),
    16: ('Common Causes', 'Flooding'),
    17: ('Common Causes', 'Location'),
    18: ('Common Causes', 'Maintenance Error'),
    19: ('Common Causes', 'Moisture/Humidity'),
    20: ('Common Causes', 'Radiation'),
    21: ('Common Causes', 'Seismic Disturbance/Impact'),
    22: ('Common Causes', 'Single-Operator Coupling'),
    23: ('Common Causes', 'Temperature Extremes'),
    24: ('Common Causes', 'Utility Outages'),
    25: ('Common Causes', 'Vibration'),
    26: ('Common Causes', 'Wear-Out'),
    27: ('Common Causes', 'Vermin/Insects'),
    28: ('Contingencies', 'Earthquake'),
    29: ('Contingencies', 'Fire'),
    30: ('Contingencies', 'Flooding'),
    31: ('Contingencies', 'Freezing'),
    32: ('Contingencies', 'Hailstorm'),
    33: ('Contingencies', 'Shutdowns/Failures'),
    34: ('Contingencies', 'Snow/Ice Load'),
    35: ('Contingencies', 'Utility Outages'),
    36: ('Contingencies', 'Windstorm'),
    37: ('Control Systems', 'Grounding Failure'),
    38: ('Control Systems', 'Inadvertent Activation'),
    39: ('Control Systems', 'Interferences (EMI/ESI)'),
    40: ('Control Systems', 'Lightning Strike'),
    41: ('Control Systems', 'Moisture'),
    42: ('Control Systems', 'Power Outage'),
    43: ('Control Systems', 'Sneak Circuit'),
    44: ('Control Systems', 'Sneak Software'),
    45: ('Electrical', 'Burns'),
    46: ('Electrical', 'Distribution Feedback'),
    47: ('Electrical', 'Explosion (Arc)'),
    48: ('Electrical', 'Explosion (Electrostatic)'),
    49: ('Electrical', 'Overheating'),
    50: ('Electrical', 'Power Outage'),
    51: ('Electrical', 'Shock'),
    52: ('Ergonomics', 'Fatigue'),
    53: ('Ergonomics', 'Faulty/Inadequate Control/Readout Labeling'),
    54: ('Ergonomics', 'Faulty Work Station Design'),
    55: ('Ergonomics', 'Glare'),
    56: ('Ergonomics', 'Inaccessibility'),
    57: ('Ergonomics', 'Inadequate Control/Readout Differentiation'),
    58: ('Ergonomics', 'Inadequate/Improper Illumination'),
    59: ('Ergonomics', 'Inappropriate Control/Readout Location'),
    60: ('Ergonomics', 'Nonexistent/Inadequate Kill Switches'),
    61: ('Explosive Conditions', 'Explosive Dust Present'),
    62: ('Explosive Conditions', 'Explosive Gas Present'),
    63: ('Explosive Conditions', 'Explosive Liquid Present'),
    64: ('Explosive Conditions', 'Explosive Propellant Present'),
    65: ('Explosive Conditions', 'Explosive Vapor Present'),
    66: ('Explosive Effects', 'Blast Overpressure'),
    67: ('Explosive Effects', 'Mass Fire'),
    68: ('Explosive Effects', 'Seismic Ground Wave'),
    69: ('Explosive Effects', 'Thrown Fragments'),
    70: ('Explosive Initiator', 'Chemical Contamination'),
    71: ('Explosive Initiator', 'Electrostatic Discharge'),
    72: ('Explosive Initiator', 'Friction'),
    73: ('Explosive Initiator', 'Heat'),
    74: ('Explosive Initiator', 'Impact/Shock'),
    75: ('Explosive Initiator', 'Lightning'),
    76: ('Explosive Initiator', 'Vibration'),
    77: ('Explosive Initiator', 'Welding (Stray Current/Sparks)'),
    78: ('Fire/Flammability', 'Fuel'),
    79: ('Fire/Flammability', 'Ignition Source'),
    80: ('Fire/Flammability', 'Oxidizer'),
    81: ('Fire/Flammability', 'Propellant'),
    82: ('Human Factors', 'Failure to Operate'),
    83: ('Human Factors', 'Inadvertent Operation'),
    84: ('Human Factors', 'Operated Too Long'),
    85: ('Human Factors', 'Operated Too Briefly'),
    86: ('Human Factors', 'Operation Early/Late'),
    87: ('Human Factors', 'Operation Out of Sequence'),
    88: ('Human Factors', 'Operator Error'),
    89: ('Human Factors', 'Right Operation/Wrong Control'),
    90: ('Ionizing Radiation', 'Alpha'),
    91: ('Ionizing Radiation', 'Beta'),
    92: ('Ionizing Radiation', 'Gamma'),
    93: ('Ionizing Radiation', 'Neutron'),
    94: ('Ionizing Radiation', 'X-Ray'),
    95: ('Leaks/Spills', 'Asphyxiating'),
    96: ('Leaks/Spills', 'Corrosive'),
    97: ('Leaks/Spills', 'Flammable'),
    98: ('Leaks/Spills', 'Flooding'),
    99: ('Leaks/Spills', 'Gases/Vapors'),
    100: ('Leaks/Spills', 'Irritating Dusts'),
    101: ('Leaks/Spills', 'Liquids/Cryogens'),
    102: ('Leaks/Spills', 'Odorous'),
    103: ('Leaks/Spills', 'Pathogenic'),
    104: ('Leaks/Spills', 'Radiation Sources'),
    105: ('Leaks/Spills', 'Reactive'),
    106: ('Leaks/Spills', 'Run Off'),
    107: ('Leaks/Spills', 'Slippery'),
    108: ('Leaks/Spills', 'Toxic'),
    109: ('Leaks/Spills', 'Vapor Propagation'),
    110: ('Mechanical', 'Crushing Surfaces'),
    111: ('Mechanical', 'Ejected Parts/Fragments'),
    112: ('Mechanical', 'Lifting Weights'),
    113: ('Mechanical', 'Pinch Points'),
    114: ('Mechanical', 'Reciprocating Equipment'),
    115: ('Mechanical', 'Rotating Equipment'),
    116: ('Mechanical', 'Sharp Edges/Points'),
    117: ('Mechanical', 'Stability/Topping Potential'),
    118: ('Mission Phasing', 'Activation'),
    119: ('Mission Phasing', 'Calibration'),
    120: ('Mission Phasing', 'Checkout'),
    121: ('Mission Phasing', 'Coupling/Uncoupling'),
    122: ('Mission Phasing', 'Delivery'),
    123: ('Mission Phasing', 'Diagnosis/Trouble Shooting'),
    124: ('Mission Phasing', 'Emergency Start'),
    125: ('Mission Phasing', 'Installation'),
    126: ('Mission Phasing', 'Load Change'),
    127: ('Mission Phasing', 'Maintenance'),
    128: ('Mission Phasing', 'Normal Operation'),
    129: ('Mission Phasing', 'Shake Down'),
    130: ('Mission Phasing', 'Shutdown Emergency'),
    131: ('Mission Phasing', 'Standard Shutdown'),
    132: ('Mission Phasing', 'Standard Start'),
    133: ('Mission Phasing', 'Stressed Operation'),
    134: ('Mission Phasing', 'Transport'),
    135: ('Nonionizing Radiation', 'Infrared'),
    136: ('Nonionizing Radiation', 'Laser'),
    137: ('Nonionizing Radiation', 'Microwave'),
    138: ('Nonionizing Radiation', 'Ultraviolet'),
    139: ('Physiological', 'Allergens'),
    140: ('Physiological', 'Asphyxiants'),
    141: ('Physiological', 'Baropressure Extremes'),
    142: ('Physiological', 'Carcinogens'),
    143: ('Physiological', 'Cryogens'),
    144: ('Physiological', 'Fatigue'),
    145: ('Physiological', 'Irritants'),
    146: ('Physiological', 'Lifted Weights'),
    147: ('Physiological', 'Mutagens'),
    148: ('Physiological', 'Noise'),
    149: ('Physiological', 'Nuisance Dust/Odors'),
    150: ('Physiological', 'Pathogens'),
    151: ('Physiological', 'Temperature Extremes'),
    152: ('Physiological', 'Teratogens'),
    153: ('Physiological', 'Toxins'),
    154: ('Physiological', "Vibration (Raynaud's Syndrome)"),
    155: ('Pneumatic/Hydraulic', 'Backflow'),
    156: ('Pneumatic/Hydraulic', 'Blown Objects'),
    157: ('Pneumatic/Hydraulic', 'Crossflow'),
    158: ('Pneumatic/Hydraulic', 'Dynamic Pressure Loading'),
    159: ('Pneumatic/Hydraulic', 'Hydraulic Ram'),
    160: ('Pneumatic/Hydraulic', 'Implosion'),
    161: ('Pneumatic/Hydraulic', 'Inadvertent Release'),
    162: ('Pneumatic/Hydraulic', 'Miscalibrated Relief Device'),
    163: ('Pneumatic/Hydraulic', 'Mislocated Relief Device'),
    164: ('Pneumatic/Hydraulic', 'Overpressurization'),
    165: ('Pneumatic/Hydraulic', 'Pipe/Hose Whip'),
    166: ('Pneumatic/Hydraulic', 'Pipe/Vessel/Duct Rupture'),
    167: ('Pneumatic/Hydraulic', 'Relief Pressure Improperly Set'),
    168: ('Thermal', 'Altered Structural Properties (e.g., '
          'Embrittlement)'),
    169: ('Thermal', 'Confined Gas/Liquid'),
    170: ('Thermal', 'Elevated Flammability'),
    171: ('Thermal', 'Elevated Reactivity'),
    172: ('Thermal', 'Elevated Volatility'),
    173: ('Thermal', 'Freezing'),
    174: ('Thermal', 'Heat Source/Sink'),
    175: ('Thermal', 'Hot/Cold Surface Burns'),
    176: ('Thermal', 'Humidity/Moisture'),
    177: ('Thermal', 'Pressure Evaluation'),
    178: ('Unannunciated Utility Outages', 'Air Conditioning'),
    179: ('Unannunciated Utility Outages', 'Compressed Air/Gas'),
    180: ('Unannunciated Utility Outages', 'Electricity'),
    181: ('Unannunciated Utility Outages', 'Exhaust'),
    182: ('Unannunciated Utility Outages', 'Fuel'),
    183: ('Unannunciated Utility Outages', 'Heating/Cooling'),
    184: ('Unannunciated Utility Outages', 'Lubrication Drains/Sumps'),
    185: ('Unannunciated Utility Outages', 'Steam'),
    186: ('Unannunciated Utility Outages', 'Ventilation')
}

RAMSTK_HISTORIES = {
    0: 'Cycle Counts',
    1: 'Histogram',
    2: 'Histogram, Bivariate',
    3: 'Level Crossing',
    4: 'Rain Flow Count',
    5: 'Time at Level',
    6: 'Time at Load',
    7: 'Time at Maximum',
    8: 'Time at Minimum'
}

RAMSTK_MANUFACTURERS = {
    0: ('Sprague', 'New Hampshire', '13606'),
    1: ('Xilinx', '', ''),
    2: ('National Semiconductor', 'California', '27014')
}

RAMSTK_MEASUREMENTS = {
    0: ('lbf', 'Pounds Force', 'unit'),
    1: ('lbm', 'Pounds Mass', 'unit'),
    2: ('hrs', 'hours', 'unit'),
    3: ('N', 'Newtons', 'unit'),
    4: ('mins', 'minutes', 'unit'),
    5: ('secs', 'seconds', 'unit'),
    6: ('g', 'grams', 'unit'),
    7: ('oz', 'ounces', 'unit'),
    8: ('A', 'Amperes', 'unit'),
    9: ('V', 'Volts', 'unit'),
    10: ('CN', 'Contamination, Concentration', 'damage'),
    11: ('CS', 'Contamination, Particle Size', 'damage'),
    12: ('LD', 'Dynamic Load', 'damage'),
    13: ('LM', 'Load, Maximum', 'damage'),
    14: ('LMM', 'Load, Minimum-Maximum', 'damage'),
    15: ('NBC', 'Number of Braking Events', 'damage'),
    16: ('NC', 'Number of Cycles', 'damage'),
    17: ('NOE', 'Number of Overload Events', 'damage'),
    18: ('NS', 'Number of Shifts', 'damage'),
    19: ('TIME', 'Operating Time at Condition', 'damage'),
    20: ('PAVG', 'Pressure, Average', 'damage'),
    21: ('DELTAP', 'Pressure, Differential', 'damage'),
    22: ('PPEAK', 'Pressure, Peak', 'damage'),
    23: ('RPM', 'Revolutions per Time', 'damage'),
    24: ('TAMB', 'Temperature, Ambient', 'damage'),
    25: ('TAVG', 'Temperature, Average', 'damage'),
    26: ('DELTAT', 'Temperature, Differential', 'damage'),
    27: ('TPEAK', 'Temperature, Peak', 'damage'),
    28: ('TEMP', 'Temperature = f(Time)', 'damage'),
    29: ('T', 'Torque', 'damage')
}

RAMSTK_METHODS = {
    0: ('Code Reviews', '', 'detection'),
    1: ('Error/Anomaly Detection', '', 'detection'),
    2: ('Structure Analysis', '', 'detection'),
    3: ('Random Testing', '', 'detection'),
    4: ('Functional Testing', '', 'detection'),
    5: ('Branch Testing', '', 'detection')
}

RAMSTK_MODELS = {
    0: ('Adhesion Wear Model for Bearings', 1),
    1: ('Arrhenius', 1),
    2: ('Coffin-Manson', 1),
    3: ('Empirical/DOE', 1),
    4: ('Eyring', 1),
    5: ('Inverse Power Law (IPL)', 1),
    6: ('IPL - Arrhenius', 1),
    7: ('Time Fraction of Damaging Operating Conditions', 1)
}

RAMSTK_RPNS = {
    0: ('None', 'No effect.', 'severity', 1),
    1: ('Very Minor', 'System operable with minimal interference.', 'severity',
        2),
    2: ('Minor', 'System operable with some degradation of performance.',
        'severity', 3),
    3: ('Very Low', 'System operable with significant degradation of '
        'performance.', 'severity', 4),
    4: ('Low', 'System inoperable without damage.', 'severity', 5),
    5: ('Moderate', 'System inoperable with minor damage.', 'severity', 6),
    6: ('High', 'System inoperable with system damage.', 'severity', 7),
    7: ('Very High', 'System inoperable with destructive failure '
        'without compromising safety.', 'severity', 8),
    8: ('Hazardous, with warning',
        'Failure effects safe system operation with warning.', 'severity', 9),
    9:
    ('Hazardous, without warning',
     'Failure effects safe system operation without warning.', 'severity', 10),
    10: ('Remote', 'Failure rate is 1 in 1,500,000.', 'occurrence', 1),
    11: ('Very Low', 'Failure rate is 1 in 150,000.', 'occurrence', 2),
    12: ('Low', 'Failure rate is 1 in 15,000', 'occurrence', 3),
    13: ('Moderately Low', 'Failure rate is 1 in 2000.', 'occurrence', 4),
    14: ('Moderate', 'Failure rate is 1 in 400.', 'occurrence', 5),
    15: ('Moderately High', 'Failure rate is 1 in 80.', 'occurrence', 6),
    16: ('High', 'Failure rate is 1 in 20.', 'occurrence', 7),
    17: ('Very High', 'Failure rate is 1 in 8.', 'occurrence', 8),
    18: ('Extremely High', 'Failure rate is 1 in 3.', 'occurrence', 9),
    19: ('Dangerously High', 'Failure rate is > 1 in 2.', 'occurrence', 10),
    20: ('Almost Certain',
         'Design control will almost certainly detect a potential '
         'mechanism/cause and subsequent failure mode.', 'detection', 1),
    21: ('Very High', 'Very high chance the existing design controls '
         'will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 2),
    22: ('High', 'High chance the existing design controls will or '
         'can detect a potential mechanism/cause and subsequent '
         'failure mode.', 'detection', 3),
    23: ('Moderately High', 'Moderately high chance the existing '
         'design controls will or can detect a potential '
         'mechanism/cause and subsequent failure mode.', 'detection', 4),
    24: ('Moderate', 'Moderate chance the existing design controls '
         'will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 5),
    25: ('Low', 'Low chance the existing design controls will or can '
         'detect a potential mechanism/cause and subsequent failure '
         'mode.', 'detection', 6),
    26: ('Very Low', 'Very low chance the existing design controls '
         'will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 7),
    27: ('Remote', 'Remote chance the existing design controls will '
         'or can detect a potential mechanism/cause and subsequent '
         'failure mode.', 'detection', 8),
    28: ('Very Remote', 'Very remote chance the existing design '
         'controls will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 9),
    29: ('Absolute Uncertainty', 'Existing design controls will not '
         'or cannot detect a potential mechanism/cause and subsequent '
         'failure mode; there is no design control.', 'detection', 10)
}

RAMSTK_STAKEHOLDERS = {
    0: 'Customer',
    1: 'Service',
    2: 'Manufacturing',
    3: 'Management'
}

RAMSTK_STATUSES = {
    0: ('Initiated', 'Incident has been initiated.', 'incident'),
    1: ('Reviewed', 'Incident has been reviewed.', 'incident'),
    2: ('Analysis', 'Incident has been assigned and is being analyzed.',
        'incident'),
    3: ('Solution Identified',
        'A solution to the reported problem has been identified.', 'incident'),
    4:
    ('Solution Implemented',
     'A solution to the reported problem has been implemented.', 'incident'),
    5: ('Solution Verified',
        'A solution to the reported problem has been verified.', 'incident'),
    6: ('Ready for Approval', 'Incident analysis is ready to be approved.',
        'incident'),
    7: ('Approved', 'Incident analysis has been approved.', 'incident'),
    8: ('Ready for Closure', 'Incident is ready to be closed.', 'incident'),
    9: ('Closed', 'Incident has been closed.', 'incident'),
    10: ('Initiated', 'Action has been initiated.', 'action'),
    11: ('Reviewed', 'Action has been reviewed.', 'action'),
    12: ('Approved', 'Action has been approved.', 'action'),
    13: ('Ready for Closure', 'Action is ready to be closed.', 'action'),
    14: ('Closed', 'Action has been closed.', 'action')
}

RAMSTK_SUBCATEGORIES = [
    (1, 1, 'Linear'), (1, 2, 'Logic'), (1, 3, 'PAL, PLA'),
    (1, 4, 'Microprocessor, Microcontroller'), (1, 5, 'Memory, ROM'),
    (1, 6, 'Memory, EEPROM'), (1, 7, 'Memory, DRAM'), (1, 8, 'Memory, SRAM'),
    (1, 9, 'GaAs'), (1, 10, 'VHSIC, VLSI'), (2, 12, 'Diode, Low Frequency'),
    (2, 13, 'Diode, High Frequency'),
    (2, 14, 'Transistor, Low Frequency, Bipolar'),
    (2, 15, 'Transistor, Low Frequency, Si FET'),
    (2, 16, 'Transistor, Unijunction'),
    (2, 17, 'Transistor, High Frequency, Low Noise, Bipolar'),
    (2, 18, 'Transistor, High Frequency, High Power, Bipolar'),
    (2, 19, 'Transistor, High Frequency, GaAs FET'),
    (2, 20, 'Transistor, High Frequency, Si FET'), (2, 21, 'Thyristor, SCR'),
    (2, 22, 'Optoelectronic, Detector, Isolator, Emitter'),
    (2, 23, 'Optoelectronic, Alphanumeric Display'),
    (2, 24, 'Optoelectronic, Laser Diode'),
    (3, 25, 'Fixed, Composition (RC, RCR)'),
    (3, 26, 'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)'),
    (3, 27, 'Fixed, Film, Power (RD)'), (3, 28, 'Fixed, Film, Network (RZ)'),
    (3, 29, 'Fixed, Wirewound (RB, RBR)'),
    (3, 30, 'Fixed, Wirewound, Power (RW, RWR)'),
    (3, 31, 'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)'),
    (3, 32, 'Thermistor (RTH)'), (3, 33, 'Variable, Wirewound (RT, RTR)'),
    (3, 34, 'Variable, Wirewound, Precision (RR)'),
    (3, 35, 'Variable, Wirewound, Semiprecision (RA, RK)'),
    (3, 36, 'Variable, Wirewound, Power (RP)'),
    (3, 37, 'Variable, Non-Wirewound (RJ, RJR)'),
    (3, 38, 'Variable, Composition (RV)'),
    (3, 39, 'Variable, Non-Wirewound, Film and Precision (RQ, RVC)'),
    (4, 40, 'Fixed, Paper, Bypass (CA, CP)'),
    (4, 41, 'Fixed, Feed-Through (CZ, CZR)'),
    (4, 42, 'Fixed, Paper and Plastic Film (CPV, CQ, CQR)'),
    (4, 43, 'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)'),
    (4, 44, 'Fixed, Plastic and Metallized Plastic'),
    (4, 45, 'Fixed, Super-Metallized Plastic (CRH)'),
    (4, 46, 'Fixed, Mica (CM, CMR)'), (4, 47, 'Fixed, Mica, Button (CB)'),
    (4, 48, 'Fixed, Glass (CY, CYR)'),
    (4, 49, 'Fixed, Ceramic, General Purpose (CK, CKR)'),
    (4, 50,
     'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)'),
    (4, 51, 'Fixed, Electrolytic, Tantalum, Solid (CSR)'),
    (4, 52, 'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)'),
    (4, 53, 'Fixed, Electrolytic, Aluminum (CU, CUR)'),
    (4, 54, 'Fixed, Electrolytic (Dry), Aluminum (CE)'),
    (4, 55, 'Variable, Ceramic (CV)'), (4, 56, 'Variable, Piston Type (PC)'),
    (4, 57, 'Variable, Air Trimmer (CT)'),
    (4, 58, 'Variable and Fixed, Gas or Vacuum (CG)'), (5, 62, 'Transformer'),
    (5, 63, 'Coil'), (6, 64, 'Mechanical'), (6, 65, 'Solid State'),
    (7, 67, 'Toggle or Pushbutton'), (7, 68, 'Sensitive'), (7, 69, 'Rotary'),
    (7, 70, 'Thumbwheel'), (7, 71, 'Circuit Breaker'), (8, 72, 'Multi-Pin'),
    (8, 73, 'PCB Edge'), (8, 74, 'IC Socket'),
    (8, 75, 'Plated Through Hole (PTH)'), (8, 76, 'Connection, Non-PTH'),
    (9, 77, 'Elapsed Time'), (9, 78, 'Panel'), (10, 80, 'Crystal'),
    (10, 81, 'Filter, Non-Tunable Electronic'), (10, 82, 'Fuse'),
    (10, 83, 'Lamp')
]

RAMSTK_TYPES: Dict[int, Tuple[str, str, str]] = {
    1: ('PLN', 'Planning', 'incident'),
    2: ('CON', 'Concept', 'incident'),
    3: ('RQMT', 'Requirement', 'incident'),
    4: ('DES', 'Design', 'incident'),
    5: ('COD', 'Coding', 'incident'),
    6: ('DB', 'Database', 'incident'),
    7: ('TI', 'Test Information', 'incident'),
    8: ('MAN', 'Manuals', 'incident'),
    9: ('OTH', 'Other', 'incident'),
    10: ('FUN', 'Functional', 'requirement'),
    11: ('PRF', 'Performance', 'requirement'),
    12: ('REG', 'Regulatory', 'requirement'),
    13: ('REL', 'Reliability', 'requirement'),
    14: ('SAF', 'Safety', 'requirement'),
    15: ('SVC', 'Serviceability', 'requirement'),
    16: ('USE', 'Useability', 'requirement'),
    17: ('DOE', 'Manufacturing Test, DOE', 'validation'),
    18: ('ESS', 'Manufacturing Test, ESS', 'validation'),
    19: ('HSS', 'Manufacturing Test, HASS', 'validation'),
    20: ('PRT', 'Manufacturing Test, PRAT', 'validation'),
    21: ('RAA', 'Reliability, Assessment', 'validation'),
    22: ('RDA', 'Reliability, Durability Analysis', 'validation'),
    23: ('RFF', 'Reliability, FFMEA', 'validation'),
    24: ('RDF', 'Reliability, (D)FMEA', 'validation'),
    25: ('RCA', 'Reliability, Root Cause Analysis', 'validation'),
    26: ('RSA', 'Reliability, Survival Analysis', 'validation'),
    27: ('ALT', 'Reliability Test, ALT', 'validation'),
    28: ('RDT', 'Reliability Test, Demonstration', 'validation'),
    29: ('HLT', 'Reliability Test, HALT', 'validation'),
    30: ('RGT', 'Reliability Test, Growth', 'validation'),
    31: ('FTA', 'Safety, Fault Tree Analysis', 'validation'),
    32: ('PHA', 'Safety, Hazards Analysis', 'validation'),
    33: ('EMA', 'System Engineering, Electromagnetic Analysis', 'validation'),
    34: ('FEA', 'System Engineering, FEA', 'validation'),
    35: ('2DM', 'System Engineering, 2D Model', 'validation'),
    36: ('3DM', 'System Engineering, 3D Model', 'validation'),
    37: ('SRD', 'System Engineering, Robust Design', 'validation'),
    38: ('SCA', 'System Engineering, Sneak Circuit Analysis', 'validation'),
    39: ('THA', 'System Engineering, Thermal Analysis', 'validation'),
    40: ('TOL', 'System Engineering, Tolerance Analysis', 'validation'),
    41: ('WCA', 'System Engineering, Worst Case Analysis', 'validation')
}


def _load_fmea_tables(session: scoped_session) -> None:
    """Load RAMSTKFailureMode and RAMSTKRPN."""
    _cat_key: int = 0
    _subcat_key: int = 0
    _mode_key: int = 0
    _rpn = Tuple[str, str, str, int]
    _method = Tuple[str, str, str]

    for _cat_key in RAMSTK_FAILURE_MODES:
        _record = RAMSTKFailureMode()
        _record.category_id = _cat_key
        for _subcat_key in RAMSTK_FAILURE_MODES[_cat_key]:
            _record.subcategory_id = _subcat_key
            for _mode_key in RAMSTK_FAILURE_MODES[_cat_key][_subcat_key]:
                _record.mode_id = _mode_key
                _record.description = RAMSTK_FAILURE_MODES[_cat_key][
                    _subcat_key][_mode_key][0]
                _record.mode_ratio = RAMSTK_FAILURE_MODES[_cat_key][
                    _subcat_key][_mode_key][1]
                _record.source = RAMSTK_FAILURE_MODES[_cat_key][_subcat_key][
                    _mode_key][2]
                session.add(_record)
    # pylint: disable=unused-variable
    for __, _rpn in list(RAMSTK_RPNS.items()):
        _record = RAMSTKRPN()
        _record.name = _rpn[0]
        _record.description = _rpn[1]
        _record.rpn_type = _rpn[2]
        _record.value = _rpn[3]
        session.add(_record)
    # pylint: disable=unused-variable
    for __, _method in list(RAMSTK_METHODS.items()):
        _record = RAMSTKMethod()
        _record.name = _method[0]
        _record.description = _method[1]
        _record.method_type = _method[2]
        session.add(_record)

    try:
        session.commit()
    except exc.IntegrityError as _error:
        print(_error)


def _load_hazard_analysis_tables(session: scoped_session) -> None:
    """Load RAMSTKHazards."""
    _hazard = Tuple[str, str]

    # pylint: disable=unused-variable
    for __, _hazard in list(RAMSTK_HAZARDS.items()):
        _record = RAMSTKHazards()
        _record.category = _hazard[0]
        _record.subcategory = _hazard[1]
        session.add(_record)

    session.commit()


def _load_incident_report_tables(session: scoped_session) -> None:
    """Load RAMSTKStatus and RAMSTKType."""
    _status = Tuple[str, str, str]
    _type = Tuple[str, str, str]

    # pylint: disable=unused-variable
    for __, _status in list(RAMSTK_STATUSES.items()):
        _record = RAMSTKStatus()
        _record.name = _status[0]
        _record.description = _status[1]
        _record.status_type = _status[2]
        session.add(_record)
    # pylint: disable=unused-variable
    for __, _type in list(RAMSTK_TYPES.items()):
        _record = RAMSTKType()
        _record.code = _type[0]
        _record.description = _type[1]
        _record.type_type = _type[2]
        session.add(_record)

    session.commit()


def _load_miscellaneous_tables(session: scoped_session) -> None:
    """Load RAMSTKCategory and RAMSTKSubCategory."""
    _category = Tuple[str, str, str, int, float, float, float, float, float,
                      float, float, float, float, float]
    _subcategory = Tuple[int, int, str]
    _manufacturer = Tuple[str, str, str]
    _measurement = Tuple[str, str, str]

    # pylint: disable=unused-variable
    for __, _category in list(RAMSTK_CATEGORIES.items()):
        _record = RAMSTKCategory()
        _record.name = _category[0]
        _record.description = _category[1]
        _record.cat_type = _category[2]
        _record.value = _category[3]
        _record.harsh_ir_limit = _category[4]
        _record.mild_ir_limit = _category[5]
        _record.harsh_pr_limit = _category[6]
        _record.mild_pr_limit = _category[7]
        _record.harsh_vr_limit = _category[8]
        _record.mild_vr_limit = _category[9]
        _record.harsh_deltat_limit = _category[10]
        _record.mild_deltat_limit = _category[11]
        _record.harsh_maxt_limit = _category[12]
        _record.mild_maxt_limit = _category[13]
        session.add(_record)

    # pylint: disable=unused-variable
    for __, _subcategory in enumerate(RAMSTK_SUBCATEGORIES):
        _record = RAMSTKSubCategory()
        _record.category_id = _subcategory[0]
        _record.subcategory_id = _subcategory[1]
        _record.description = _subcategory[2]
        session.add(_record)

    # pylint: disable=unused-variable
    for __, _manufacturer in list(RAMSTK_MANUFACTURERS.items()):
        _record = RAMSTKManufacturer()
        _record.description = _manufacturer[0]
        _record.location = _manufacturer[1]
        _record.cage_code = _manufacturer[2]
        session.add(_record)

    # pylint: disable=unused-variable
    for __, _measurement in list(RAMSTK_MEASUREMENTS.items()):
        _record = RAMSTKMeasurement()
        _record.code = _measurement[0]
        _record.description = _measurement[1]
        _record.measurement_type = _measurement[2]
        session.add(_record)

    session.commit()


def _load_pof_tables(session: scoped_session) -> None:
    """Load RAMSTKCondition, RAMSTKLoadHistory, and RAMSTKModel."""
    _condition = Tuple[str, str]
    _history: str = ''
    _model = Tuple[str, int]

    # pylint: disable=unused-variable
    for __, _condition in list(RAMSTK_CONDITIONS.items()):
        _record = RAMSTKCondition()
        _record.description = _condition[0]
        _record.cond_type = _condition[1]
        session.add(_record)

    # pylint: disable=unused-variable
    for __, _history in list(RAMSTK_HISTORIES.items()):
        _record = RAMSTKLoadHistory()
        _record.description = _history
        session.add(_record)

    # pylint: disable=unused-variable
    for __, _model in list(RAMSTK_MODELS.items()):
        _record = RAMSTKModel()
        _record.description = _model[0]
        _record.model_type = _model[1]
        session.add(_record)

    session.commit()


def _load_requirements_analysis_tables(session: scoped_session) -> None:
    """Load RAMSTKStakeholders."""
    _group = Tuple[str, str]
    _stakeholder: str = ''

    # pylint: disable=unused-variable
    for __, _group in list(RAMSTK_GROUPS.items()):
        _record = RAMSTKGroup()
        _record.description = _group[0]
        _record.group_type = _group[1]
        session.add(_record)

    # pylint: disable=unused-variable
    for __, _stakeholder in list(RAMSTK_STAKEHOLDERS.items()):
        _record = RAMSTKStakeholders()
        _record.stakeholder = _stakeholder
        session.add(_record)

    session.commit()


def _load_site_info(session: scoped_session) -> None:
    """Load RAMSTKSiteInfo."""
    _cwd = os.getcwd()
    _license_key: str = '0000'
    _expire_date: date = date.today() + timedelta(days=30)

    try:
        license_file = open(_cwd + '/license.key', 'r')
        _contents = license_file.readlines()
        _license_key = _contents[0].strip('\n')
        _expire_date = datetime.strptime(_contents[1], '%Y-%m-%d')
        license_file.close()
    except IOError:
        _error_msg = ("Unable to read license key file.  Defaulting to a "
                      "30-day demo license.")
        pub.sendMessage('fail_read_license', error_message=_error_msg)

    _site_info = RAMSTKSiteInfo()
    _site_info.product_key = _license_key
    _site_info.expire_on = _expire_date
    session.add(_site_info)

    session.commit()


def do_add_administrator(session: scoped_session) -> None:
    """Add a new administrator to the RAMSTK pool."""
    _user = RAMSTKUser()

    _yn = input(  # nosec
        _("Would you like to add a RAMSTK Administrator? ([y]/n): ")) or 'y'

    if _yn.lower() == 'y':
        _user.user_lname = input(  # nosec
            _("Enter the RAMSTK Administrator's last name (surname): "))
        _user.user_fname = input(  # nosec
            _("Enter the RAMSTK Administrator's first name (given name): "))
        _user.user_email = input(  # nosec
            _("Enter the RAMSTK Administrator's e-mail address: "))
        _user.user_phone = input(  # nosec
            _("Enter the RAMSTK Administrator's phone number: "))
        _user.user_group_id = 1

        session.add(_user)
        session.commit()


def do_create_common_db(engine: Engine, session: scoped_session) -> None:
    """Create and populate the RAMSTK Common database.

    :param engine: the SQLAlchemy Engine connected to the database.
    :param session: the SQLAlchemy session to use when creating the database.
    :return: None
    :rtype: None
    """
    do_make_commondb_tables(engine)

    _load_site_info(session)

    _load_miscellaneous_tables(session)
    _load_fmea_tables(session)
    _load_hazard_analysis_tables(session)
    _load_pof_tables(session)
    _load_requirements_analysis_tables(session)
    _load_incident_report_tables(session)

    # Add a new admin user.
    do_add_administrator(session)

    session.commit()


def do_make_commondb_tables(engine: Engine) -> None:
    """Create all the tables in the RAMSTK Common database.

    :param engine: the SQLAlchemy database engine to use to create the common
        database tables.
    :type engine: :class:`sqlalchemy.engine.Engine`
    :return: None
    :rtype: None
    """
    RAMSTKSiteInfo.__table__.create(bind=engine)
    RAMSTKCategory.__table__.create(bind=engine)
    RAMSTKCondition.__table__.create(bind=engine)
    RAMSTKFailureMode.__table__.create(bind=engine)
    RAMSTKGroup.__table__.create(bind=engine)
    RAMSTKHazards.__table__.create(bind=engine)
    RAMSTKLoadHistory.__table__.create(bind=engine)
    RAMSTKManufacturer.__table__.create(bind=engine)
    RAMSTKMeasurement.__table__.create(bind=engine)
    RAMSTKMethod.__table__.create(bind=engine)
    RAMSTKModel.__table__.create(bind=engine)
    RAMSTKRPN.__table__.create(bind=engine)
    RAMSTKStakeholders.__table__.create(bind=engine)
    RAMSTKStatus.__table__.create(bind=engine)
    RAMSTKSubCategory.__table__.create(bind=engine)
    RAMSTKType.__table__.create(bind=engine)
    RAMSTKUser.__table__.create(bind=engine)


def _do_load_action_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load the RAMSTK_ACTION_CATEGORY variable.

    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKCategory).filter(
            RAMSTKCategory.category_type == 'action').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_ACTION_CATEGORY[_record.category_id] = (
            _attributes['name'],
            _attributes['description'],
            _attributes['category_type'],
            _attributes['value'],
        )
    for _record in site_db.session.query(RAMSTKStatus).\
            filter(RAMSTKStatus.status_type == 'action').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_ACTION_STATUS[_record.status_id] = (
            _attributes['name'],
            _attributes['description'],
            _attributes['status_type'],
        )


def _do_load_hardware_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load variables associated with hardware categories and failure modes.

    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKCategory).\
            filter(RAMSTKCategory.category_type == 'hardware').all():

        _subcats = {}
        user_configuration.RAMSTK_FAILURE_MODES[_record.category_id] = {}
        user_configuration.RAMSTK_STRESS_LIMITS[_record.category_id] = (
            _record.harsh_ir_limit, _record.mild_ir_limit,
            _record.harsh_pr_limit, _record.mild_pr_limit,
            _record.harsh_vr_limit, _record.mild_vr_limit,
            _record.harsh_deltat_limit, _record.mild_deltat_limit,
            _record.harsh_maxt_limit, _record.mild_maxt_limit)
        for _subcat in site_db.session.query(RAMSTKSubCategory).\
                filter(RAMSTKSubCategory.category_id == _record.category_id).\
                all():
            _subcats[_subcat.subcategory_id] = _subcat.description

            _modes = {}
            user_configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                _subcat.subcategory_id] = {}
            for _mode in site_db.session.query(RAMSTKFailureMode).filter(
                    RAMSTKFailureMode.category_id == _record.category_id
            ).filter(RAMSTKFailureMode.subcategory_id ==
                     _subcat.subcategory_id).all():
                _modes[_mode.mode_id] = [
                    _mode.description,
                    _mode.mode_ratio,
                    _mode.source,
                ]

            user_configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                _subcat.subcategory_id] = _modes

        user_configuration.RAMSTK_CATEGORIES[
            _record.category_id] = _record.description
        user_configuration.RAMSTK_SUBCATEGORIES[_record.category_id] = _subcats


def _do_load_incident_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load the RAMSTK_INCIDENT_CATEGORY variable.

    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKCategory).\
            filter(RAMSTKCategory.category_type == 'incident').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_INCIDENT_CATEGORY[_record.category_id] = (
            _attributes['name'],
            _attributes['description'],
            _attributes['category_type'],
            _attributes['value'],
        )
    for _record in site_db.session.query(RAMSTKStatus).\
            filter(RAMSTKStatus.status_type == 'incident').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_INCIDENT_STATUS[_record.status_id] = (
            _attributes['name'],
            _attributes['description'],
            _attributes['status_type'],
        )
    for _record in site_db.session.query(RAMSTKType).\
            filter(RAMSTKType.type_type == 'incident').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_INCIDENT_TYPE[_record.type_id] = (
            _attributes['code'],
            _attributes['description'],
            _attributes['type_type'],
        )


def _do_load_miscellaneous_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load miscellaneous variables that don't fit in another grouping.

    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKMethod).\
            filter(RAMSTKMethod.method_type == 'detection').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_DETECTION_METHODS[_record.method_id] = (
            _attributes['name'],
            _attributes['description'],
            _attributes['method_type'],
        )
    for _record in site_db.session.query(RAMSTKHazards).all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_HAZARDS[_record.hazard_id] = (
            _attributes['hazard_category'], _attributes['hazard_subcategory'])
    for _record in site_db.session.query(RAMSTKManufacturer).all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_MANUFACTURERS[_record.manufacturer_id] = (
            _attributes['description'], _attributes['location'],
            _attributes['cage_code'])
    for _record in site_db.session.query(RAMSTKMeasurement).\
            filter(RAMSTKMeasurement.measurement_type == 'unit').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_MEASUREMENT_UNITS[_record.measurement_id] = (
            _attributes['code'], _attributes['description'],
            _attributes['measurement_type'])
    for _record in site_db.session.query(RAMSTKType).\
            filter(RAMSTKType.type_type == 'validation').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_VALIDATION_TYPE[_record.type_id] = (
            _attributes['code'], _attributes['description'],
            _attributes['type_type'])


def _do_load_pof_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load the RAMSTK_DAMAGE_MODELS variable.

    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKModel). \
            filter(RAMSTKModel.model_type == 'damage').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_DAMAGE_MODELS[_record.model_id] = (
            _attributes['description'])
    for _record in site_db.session.query(RAMSTKLoadHistory).all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_LOAD_HISTORY[_record.history_id] = (
            _attributes['description'])
    for _record in site_db.session.query(RAMSTKMeasurement). \
            filter(RAMSTKMeasurement.measurement_type == 'damage').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_MEASURABLE_PARAMETERS[
            _record.measurement_id] = (_attributes['code'],
                                       _attributes['description'],
                                       _attributes['measurement_type'])


def _do_load_requirement_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load variables related to requiremetents and stakeholders.

    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKGroup).\
            filter(RAMSTKGroup.group_type == 'affinity').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_AFFINITY_GROUPS[_record.group_id] = (
            _attributes['description'],
            _attributes['group_type'],
        )
    for _record in site_db.session.query(RAMSTKType).\
            filter(RAMSTKType.type_type == 'requirement').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_REQUIREMENT_TYPE[_record.type_id] = (
            _attributes['code'], _attributes['description'],
            _attributes['type_type'])
    for _record in site_db.session.query(RAMSTKStakeholders).all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_STAKEHOLDERS[_record.stakeholders_id] = (
            _attributes['stakeholder'])


def _do_load_rpn_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load the RPN detection, occurremce, and severity variables.

    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKRPN).\
            filter(RAMSTKRPN.rpn_type == 'detection').all():
        user_configuration.RAMSTK_RPN_DETECTION[_record.value] = \
            _record.get_attributes()

    for _record in site_db.session.query(RAMSTKRPN).\
            filter(RAMSTKRPN.rpn_type == 'occurrence').all():
        user_configuration.RAMSTK_RPN_OCCURRENCE[_record.value] = \
            _record.get_attributes()

    for _record in site_db.session.query(RAMSTKRPN). \
            filter(RAMSTKRPN.rpn_type == 'severity').all():
        user_configuration.RAMSTK_RPN_SEVERITY[_record.value] = \
            _record.get_attributes()


def _do_load_severity(site_db: BaseDatabase,
                      user_configuration: RAMSTKUserConfiguration) -> None:
    """Load the RAMSTK_SEVERITY variable.

    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKCategory).\
            filter(RAMSTKCategory.category_type == 'risk').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_SEVERITY[_record.category_id] = (
            _attributes['name'], _attributes['description'],
            _attributes['category_type'], _attributes['value'])


def _do_load_user_workgroups(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    """Load the RAMSTK_USERS and RAMSTK_WORKGROUPS variables.

    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :return: None
    :rtype: None
    """
    for _record in site_db.session.query(RAMSTKUser).all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_USERS[_record.user_id] = (
            _attributes['user_lname'],
            _attributes['user_fname'],
            _attributes['user_email'],
            _attributes['user_phone'],
            _attributes['user_group_id'],
        )
    for _record in site_db.session.query(RAMSTKGroup).\
            filter(RAMSTKGroup.group_type == 'workgroup').all():
        _attributes = _record.get_attributes()
        user_configuration.RAMSTK_WORKGROUPS[_record.group_id] = (
            _attributes['description'],
            _attributes['group_type'],
        )


def do_load_variables(site_db: BaseDatabase,
                      user_configuration: RAMSTKUserConfiguration) -> None:
    """Load the RAMSTKUserConfiguration global variables from the site db.

    :param site_db: the RAMSTK Site Database to read the values of the
        global variables.
    :param user_configuration: the RAMSTKUserConfiguration instance whose
        variable is to be loaded.
    :return: None
    :rtype: None
    """
    pub.sendMessage('do_log_info_msg',
                    logger_name='INFO',
                    message="Loading global RAMSTK configuration variables.")

    _do_load_action_variables(site_db, user_configuration)
    _do_load_hardware_variables(site_db, user_configuration)
    _do_load_incident_variables(site_db, user_configuration)
    _do_load_miscellaneous_variables(site_db, user_configuration)
    _do_load_pof_variables(site_db, user_configuration)
    _do_load_requirement_variables(site_db, user_configuration)
    _do_load_rpn_variables(site_db, user_configuration)
    _do_load_severity(site_db, user_configuration)
    _do_load_user_workgroups(site_db, user_configuration)

    pub.sendMessage('do_log_info_msg',
                    logger_name='INFO',
                    message="Loaded global RAMSTK configuration variables.")
