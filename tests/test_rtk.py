#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.TestRTK.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""This is the test class for testing the RTK module algorithms and models."""

import os

import logging
from treelib import Tree

import pytest

from rtk.Configuration import Configuration
from rtk.RTK import Model, RTK, _initialize_loggers
from rtk.dao.DAO import DAO
from rtk.gui.gtk.mwi.ListBook import ListBook
from rtk.gui.gtk.mwi.ModuleBook import ModuleBook
from rtk.gui.gtk.mwi.WorkBook import WorkBook

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2018 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_initialize_logger(test_configuration):
    """ _initialize_loggers() should return a tuple of logging.Logger instances. """
    _configuration = test_configuration

    (_configuration.RTK_DEBUG_LOG, _configuration.RTK_USER_LOG,
     _configuration.RTK_IMPORT_LOG) = _initialize_loggers(_configuration)

    assert isinstance(_configuration.RTK_DEBUG_LOG, logging.Logger)
    assert isinstance(_configuration.RTK_USER_LOG, logging.Logger)
    assert isinstance(_configuration.RTK_IMPORT_LOG, logging.Logger)
    assert os.path.isfile(_configuration.RTK_LOG_DIR + '/RTK_debug.log')
    assert os.path.isfile(_configuration.RTK_LOG_DIR + '/RTK_user.log')
    assert os.path.isfile(_configuration.RTK_LOG_DIR + '/RTK_import.log')


@pytest.mark.integration
def test_initialize_model(test_common_dao, test_dao):
    """ __init__() should create an instance of the RTK.Model object. """
    DUT = Model(test_common_dao, test_dao)

    assert isinstance(DUT, Model)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.site_dao, DAO)
    assert isinstance(DUT.program_dao, DAO)
    assert DUT.program_session is None


@pytest.mark.integration
def test_create_new_program(test_common_dao, test_dao, test_configuration):
    """ create_program() should return a zero error code on success. """
    DUT = Model(test_common_dao, test_dao)

    _configuration = test_configuration
    _database = _configuration.RTK_BACKEND + ':///' + '/tmp/_rtk_test_db.rtk'
    _error_code, _msg = DUT.create_program(_database)

    assert _error_code == 0
    assert _msg == (
        'RTK SUCCESS: Creating RTK Program database {0:s}.'.format(_database))


@pytest.mark.integration
def test_create_new_program_failed(test_common_dao, test_dao):
    """ create_program() should return a non-zero error code on failure. """
    DUT = Model(test_common_dao, test_dao)

    _database = 'sqlite:///tmp/BigAssTestDB.rtk'
    _error_code, _msg = DUT.create_program(_database)

    assert _error_code == 1
    assert _msg == ('RTK ERROR: Failed to create RTK Program database '
                    'sqlite:///tmp/BigAssTestDB.rtk.')


@pytest.mark.integration
def test_open_program(test_common_dao, test_dao, test_configuration):
    """ open_program() should return a zero error code on success. """
    DUT = Model(test_common_dao, test_dao)

    _configuration = test_configuration
    _database = _configuration.RTK_BACKEND + ':///' + \
                _configuration.RTK_PROG_INFO['database']
    _error_code, _msg = DUT.open_program(_database)

    assert _error_code == 0
    assert _msg == (
        'RTK SUCCESS: Opening RTK Program database {0:s}.'.format(_database))


@pytest.mark.integration
def test_load_globals(test_common_dao, test_dao):
    """ load_globals() should return False on success. """
    DUT = Model(test_common_dao, test_dao)
    _configuration = Configuration()

    assert not DUT.load_globals(_configuration)

    assert isinstance(DUT.tree, Tree)

    assert _configuration.RTK_ACTION_CATEGORY == {}
    assert _configuration.RTK_INCIDENT_CATEGORY == {
        35: (u'HW', u'Hardware', u'incident', 1),
        36: (u'SW', u'Software', u'incident', 1),
        37: (u'PROC', u'Process', u'incident', 1)
    }
    assert _configuration.RTK_SEVERITY == {
        11: (u'INS', u'Insignificant', u'risk', 1),
        12: (u'SLT', u'Slight', u'risk', 2),
        13: (u'LOW', u'Low', u'risk', 3),
        14: (u'MED', u'Medium', u'risk', 4),
        15: (u'HI', u'High', u'risk', 5),
        16: (u'MAJ', u'Major', u'risk', 6)
    }

    assert _configuration.RTK_AFFINITY_GROUPS == {
        8: (u'Durability', u'affinity'),
        9: (u'Cost', u'affinity'),
        7: (u'Reliability', u'affinity')
    }
    assert _configuration.RTK_WORKGROUPS == {
        1: (u'Engineering, Design', u'workgroup'),
        2: (u'Engineering, Logistics Support', u'workgroup'),
        3: (u'Engineering, Maintainability', u'workgroup'),
        4: (u'Engineering, Reliability', u'workgroup'),
        5: (u'Engineering, Safety', u'workgroup'),
        6: (u'Engineering, Software', u'workgroup')
    }

    assert _configuration.RTK_DETECTION_METHODS == {
        1: (u'Code Reviews', u'', u'detection'),
        2: (u'Error/Anomaly Detection', u'', u'detection'),
        3: (u'Structure Analysis', u'', u'detection'),
        4: (u'Random Testing', u'', u'detection'),
        5: (u'Functional Testing', u'', u'detection'),
        6: (u'Branch Testing', u'', u'detection')
    }

    assert _configuration.RTK_DAMAGE_MODELS == {
        1: (u'Adhesion Wear Model for Bearings', ),
        2: (u'Arrhenius', ),
        3: (u'Coffin-Manson', ),
        4: (u'Empirical/DOE', ),
        5: (u'Eyring', ),
        6: (u'Inverse Power Law (IPL)', ),
        7: (u'IPL - Arrhenius', ),
        8: (u'Time Fraction of Damaging Operating Conditions', )
    }

    assert _configuration.RTK_RPN_DETECTION == {
        1:
        (21, u'Almost Certain',
         u'Design control will almost certainly detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 1),
        2:
        (22, u'Very High',
         u'Very high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 2),
        3:
        (23, u'High',
         u'High chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 3),
        4:
        (24, u'Moderately High',
         u'Moderately high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 4),
        5:
        (25, u'Moderate',
         u'Moderate chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 5),
        6:
        (26, u'Low',
         u'Low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 6),
        7:
        (27, u'Very Low',
         u'Very low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 7),
        8:
        (28, u'Remote',
         u'Remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 8),
        9:
        (29, u'Very Remote',
         u'Very remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
         u'detection', 9),
        10:
        (30, u'Absolute Uncertainty',
         u'Existing design controls will not or cannot detect a potential mechanism/cause and subsequent failure mode; there is no design control.',
         u'detection', 10)
    }
    assert _configuration.RTK_RPN_OCCURRENCE == {
        1: (11, u'Remote', u'Failure rate is 1 in 1,500,000.', u'occurrence',
            1),
        2: (12, u'Very Low', u'Failure rate is 1 in 150,000.', u'occurrence',
            2),
        3: (13, u'Low', u'Failure rate is 1 in 15,000', u'occurrence', 3),
        4: (14, u'Moderately Low', u'Failure rate is 1 in 2000.',
            u'occurrence', 4),
        5: (15, u'Moderate', u'Failure rate is 1 in 400.', u'occurrence', 5),
        6: (16, u'Moderately High', u'Failure rate is 1 in 80.', u'occurrence',
            6),
        7: (17, u'High', u'Failure rate is 1 in 20.', u'occurrence', 7),
        8: (18, u'Very High', u'Failure rate is 1 in 8.', u'occurrence', 8),
        9: (19, u'Extremely High', u'Failure rate is 1 in 3.', u'occurrence',
            9),
        10: (20, u'Dangerously High', u'Failure rate is > 1 in 2.',
             u'occurrence', 10)
    }
    assert _configuration.RTK_RPN_SEVERITY == {
        1: (1, u'None', u'No effect.', u'severity', 1),
        2: (2, u'Very Minor', u'System operable with minimal interference.',
            u'severity', 2),
        3:
        (3, u'Minor', u'System operable with some degradation of performance.',
         u'severity', 3),
        4: (4, u'Very Low',
            u'System operable with significant degradation of performance.',
            u'severity', 4),
        5: (5, u'Low', u'System inoperable without damage.', u'severity', 5),
        6: (6, u'Moderate', u'System inoperable with minor damage.',
            u'severity', 6),
        7: (7, u'High', u'System inoperable with system damage.', u'severity',
            7),
        8:
        (8, u'Very High',
         u'System inoperable with destructive failure without compromising safety.',
         u'severity', 8),
        9: (9, u'Hazardous, with warning',
            u'Failure effects safe system operation with warning.',
            u'severity', 9),
        10: (10, u'Hazardous, without warning',
             u'Failure effects safe system operation without warning.',
             u'severity', 10)
    }

    assert _configuration.RTK_ACTION_STATUS == {
        11: (u'Initiated', u'Action has been initiated.', u'action'),
        12: (u'Reviewed', u'Action has been reviewed.', u'action'),
        13: (u'Approved', u'Action has been approved.', u'action'),
        14: (u'Ready for Closure', u'Action is ready to be closed.',
             u'action'),
        15: (u'Closed', u'Action has been closed.', u'action')
    }
    assert _configuration.RTK_INCIDENT_STATUS == {
        1: (u'Initiated', u'Incident has been initiated.', u'incident'),
        2: (u'Reviewed', u'Incident has been reviewed.', u'incident'),
        3: (u'Analysis', u'Incident has been assigned and is being analyzed.',
            u'incident'),
        4: (u'Solution Identified',
            u'A solution to the reported problem has been identified.',
            u'incident'),
        5: (u'Solution Implemented',
            u'A solution to the reported problem has been implemented.',
            u'incident'),
        6: (u'Solution Verified',
            u'A solution to the reported problem has been verified.',
            u'incident'),
        7: (u'Ready for Approval',
            u'Incident analysis is ready to be approved.', u'incident'),
        8: (u'Approved', u'Incident analysis has been approved.', u'incident'),
        9: (u'Ready for Closure', u'Incident is ready to be closed.',
            u'incident'),
        10: (u'Closed', u'Incident has been closed.', u'incident')
    }

    assert _configuration.RTK_INCIDENT_TYPE == {}
    assert _configuration.RTK_REQUIREMENT_TYPE == {}
    assert _configuration.RTK_VALIDATION_TYPE == {}

    assert _configuration.RTK_CATEGORIES == {
        1: u'Integrated Circuit',
        2: u'Semiconductor',
        3: u'Resistor',
        4: u'Capacitor',
        5: u'Inductive Device',
        6: u'Relay',
        7: u'Switching Device',
        8: u'Connection',
        9: u'Meter',
        10: u'Miscellaneous'
    }
    assert _configuration.RTK_FAILURE_MODES == {
        1: {
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
            7: {},
            8: {},
            9: {},
            10: {}
        },
        2: {
            11: {},
            12: {},
            13: {},
            14: {},
            15: {},
            16: {},
            17: {},
            18: {},
            19: {},
            20: {},
            21: {},
            22: {},
            23: {}
        },
        3: {
            32: {},
            33: {},
            34: {},
            35: {},
            36: {},
            37: {},
            38: {},
            24: {
                3: [u'Parameter Change', 0.2, u'FMD-97']
            },
            25: {},
            26: {},
            27: {},
            28: {},
            29: {},
            30: {},
            31: {}
        },
        4: {
            39: {},
            40: {},
            41: {},
            42: {},
            43: {},
            44: {},
            45: {},
            46: {},
            47: {},
            48: {},
            49: {},
            50: {},
            51: {},
            52: {},
            53: {},
            54: {},
            55: {},
            56: {},
            57: {}
        },
        5: {
            58: {},
            59: {}
        },
        6: {
            60: {},
            61: {}
        },
        7: {
            64: {},
            65: {},
            66: {},
            62: {},
            63: {}
        },
        8: {
            67: {},
            68: {},
            69: {},
            70: {},
            71: {}
        },
        9: {
            72: {},
            73: {}
        },
        10: {
            74: {},
            75: {},
            76: {},
            77: {}
        }
    }
    assert _configuration.RTK_HAZARDS == {
        1: (u'Acceleration/Gravity', u'Falls'),
        2: (u'Acceleration/Gravity', u'Falling Objects'),
        3: (u'Acceleration/Gravity', u'Fragments/Missiles'),
        4: (u'Acceleration/Gravity', u'Impacts'),
        5: (u'Acceleration/Gravity', u'Inadvertent Motion'),
        6: (u'Acceleration/Gravity', u'Loose Object Translation'),
        7: (u'Acceleration/Gravity', u'Slip/Trip'),
        8: (u'Acceleration/Gravity', u'Sloshing Liquids'),
        9: (u'Chemical/Water Contamination', u'Backflow/Siphon Effect'),
        10: (u'Chemical/Water Contamination', u'Leaks/Spills'),
        11: (u'Chemical/Water Contamination', u'System-Cross Connection'),
        12: (u'Chemical/Water Contamination', u'Vessel/Pipe/Conduit Rupture'),
        13: (u'Common Causes', u'Dust/Dirt'),
        14: (u'Common Causes', u'Faulty Calibration'),
        15: (u'Common Causes', u'Fire'),
        16: (u'Common Causes', u'Flooding'),
        17: (u'Common Causes', u'Location'),
        18: (u'Common Causes', u'Maintenance Error'),
        19: (u'Common Causes', u'Moisture/Humidity'),
        20: (u'Common Causes', u'Radiation'),
        21: (u'Common Causes', u'Seismic Disturbance/Impact'),
        22: (u'Common Causes', u'Single-Operator Coupling'),
        23: (u'Common Causes', u'Temperature Extremes'),
        24: (u'Common Causes', u'Utility Outages'),
        25: (u'Common Causes', u'Vibration'),
        26: (u'Common Causes', u'Wear-Out'),
        27: (u'Common Causes', u'Vermin/Insects'),
        28: (u'Contingencies', u'Earthquake'),
        29: (u'Contingencies', u'Fire'),
        30: (u'Contingencies', u'Flooding'),
        31: (u'Contingencies', u'Freezing'),
        32: (u'Contingencies', u'Hailstorm'),
        33: (u'Contingencies', u'Shutdowns/Failures'),
        34: (u'Contingencies', u'Snow/Ice Load'),
        35: (u'Contingencies', u'Utility Outages'),
        36: (u'Contingencies', u'Windstorm'),
        37: (u'Control Systems', u'Grounding Failure'),
        38: (u'Control Systems', u'Inadvertent Activation'),
        39: (u'Control Systems', u'Interferences (EMI/ESI)'),
        40: (u'Control Systems', u'Lightning Strike'),
        41: (u'Control Systems', u'Moisture'),
        42: (u'Control Systems', u'Power Outage'),
        43: (u'Control Systems', u'Sneak Circuit'),
        44: (u'Control Systems', u'Sneak Software'),
        45: (u'Electrical', u'Burns'),
        46: (u'Electrical', u'Distribution Feedback'),
        47: (u'Electrical', u'Explosion (Arc)'),
        48: (u'Electrical', u'Explosion (Electrostatic)'),
        49: (u'Electrical', u'Overheating'),
        50: (u'Electrical', u'Power Outage'),
        51: (u'Electrical', u'Shock'),
        52: (u'Ergonomics', u'Fatigue'),
        53: (u'Ergonomics', u'Faulty/Inadequate Control/Readout Labeling'),
        54: (u'Ergonomics', u'Faulty Work Station Design'),
        55: (u'Ergonomics', u'Glare'),
        56: (u'Ergonomics', u'Inaccessibility'),
        57: (u'Ergonomics', u'Inadequate Control/Readout Differentiation'),
        58: (u'Ergonomics', u'Inadequate/Improper Illumination'),
        59: (u'Ergonomics', u'Inappropriate Control/Readout Location'),
        60: (u'Ergonomics', u'Nonexistent/Inadequate Kill Switches'),
        61: (u'Explosive Conditions', u'Explosive Dust Present'),
        62: (u'Explosive Conditions', u'Explosive Gas Present'),
        63: (u'Explosive Conditions', u'Explosive Liquid Present'),
        64: (u'Explosive Conditions', u'Explosive Propellant Present'),
        65: (u'Explosive Conditions', u'Explosive Vapor Present'),
        66: (u'Explosive Effects', u'Blast Overpressure'),
        67: (u'Explosive Effects', u'Mass Fire'),
        68: (u'Explosive Effects', u'Seismic Ground Wave'),
        69: (u'Explosive Effects', u'Thrown Fragments'),
        70: (u'Explosive Initiator', u'Chemical Contamination'),
        71: (u'Explosive Initiator', u'Electrostatic Discharge'),
        72: (u'Explosive Initiator', u'Friction'),
        73: (u'Explosive Initiator', u'Heat'),
        74: (u'Explosive Initiator', u'Impact/Shock'),
        75: (u'Explosive Initiator', u'Lightning'),
        76: (u'Explosive Initiator', u'Vibration'),
        77: (u'Explosive Initiator', u'Welding (Stray Current/Sparks)'),
        78: (u'Fire/Flammability', u'Fuel'),
        79: (u'Fire/Flammability', u'Ignition Source'),
        80: (u'Fire/Flammability', u'Oxidizer'),
        81: (u'Fire/Flammability', u'Propellant'),
        82: (u'Human Factors', u'Failure to Operate'),
        83: (u'Human Factors', u'Inadvertent Operation'),
        84: (u'Human Factors', u'Operated Too Long'),
        85: (u'Human Factors', u'Operated Too Briefly'),
        86: (u'Human Factors', u'Operation Early/Late'),
        87: (u'Human Factors', u'Operation Out of Sequence'),
        88: (u'Human Factors', u'Operator Error'),
        89: (u'Human Factors', u'Right Operation/Wrong Control'),
        90: (u'Ionizing Radiation', u'Alpha'),
        91: (u'Ionizing Radiation', u'Beta'),
        92: (u'Ionizing Radiation', u'Gamma'),
        93: (u'Ionizing Radiation', u'Neutron'),
        94: (u'Ionizing Radiation', u'X-Ray'),
        95: (u'Leaks/Spills', u'Asphyxiating'),
        96: (u'Leaks/Spills', u'Corrosive'),
        97: (u'Leaks/Spills', u'Flammable'),
        98: (u'Leaks/Spills', u'Flooding'),
        99: (u'Leaks/Spills', u'Gases/Vapors'),
        100: (u'Leaks/Spills', u'Irritating Dusts'),
        101: (u'Leaks/Spills', u'Liquids/Cryogens'),
        102: (u'Leaks/Spills', u'Odorous'),
        103: (u'Leaks/Spills', u'Pathogenic'),
        104: (u'Leaks/Spills', u'Radiation Sources'),
        105: (u'Leaks/Spills', u'Reactive'),
        106: (u'Leaks/Spills', u'Run Off'),
        107: (u'Leaks/Spills', u'Slippery'),
        108: (u'Leaks/Spills', u'Toxic'),
        109: (u'Leaks/Spills', u'Vapor Propagation'),
        110: (u'Mechanical', u'Crushing Surfaces'),
        111: (u'Mechanical', u'Ejected Parts/Fragments'),
        112: (u'Mechanical', u'Lifting Weights'),
        113: (u'Mechanical', u'Pinch Points'),
        114: (u'Mechanical', u'Reciprocating Equipment'),
        115: (u'Mechanical', u'Rotating Equipment'),
        116: (u'Mechanical', u'Sharp Edges/Points'),
        117: (u'Mechanical', u'Stability/Topping Potential'),
        118: (u'Mission Phasing', u'Activation'),
        119: (u'Mission Phasing', u'Calibration'),
        120: (u'Mission Phasing', u'Checkout'),
        121: (u'Mission Phasing', u'Coupling/Uncoupling'),
        122: (u'Mission Phasing', u'Delivery'),
        123: (u'Mission Phasing', u'Diagnosis/Trouble Shooting'),
        124: (u'Mission Phasing', u'Emergency Start'),
        125: (u'Mission Phasing', u'Installation'),
        126: (u'Mission Phasing', u'Load Change'),
        127: (u'Mission Phasing', u'Maintenance'),
        128: (u'Mission Phasing', u'Normal Operation'),
        129: (u'Mission Phasing', u'Shake Down'),
        130: (u'Mission Phasing', u'Shutdown Emergency'),
        131: (u'Mission Phasing', u'Standard Shutdown'),
        132: (u'Mission Phasing', u'Standard Start'),
        133: (u'Mission Phasing', u'Stressed Operation'),
        134: (u'Mission Phasing', u'Transport'),
        135: (u'Nonionizing Radiation', u'Infrared'),
        136: (u'Nonionizing Radiation', u'Laser'),
        137: (u'Nonionizing Radiation', u'Microwave'),
        138: (u'Nonionizing Radiation', u'Ultraviolet'),
        139: (u'Physiological', u'Allergens'),
        140: (u'Physiological', u'Asphyxiants'),
        141: (u'Physiological', u'Baropressure Extremes'),
        142: (u'Physiological', u'Carcinogens'),
        143: (u'Physiological', u'Cryogens'),
        144: (u'Physiological', u'Fatigue'),
        145: (u'Physiological', u'Irritants'),
        146: (u'Physiological', u'Lifted Weights'),
        147: (u'Physiological', u'Mutagens'),
        148: (u'Physiological', u'Noise'),
        149: (u'Physiological', u'Nuisance Dust/Odors'),
        150: (u'Physiological', u'Pathogens'),
        151: (u'Physiological', u'Temperature Extremes'),
        152: (u'Physiological', u'Teratogens'),
        153: (u'Physiological', u'Toxins'),
        154: (u'Physiological', u"Vibration (Raynaud's Syndrome)"),
        155: (u'Pneumatic/Hydraulic', u'Backflow'),
        156: (u'Pneumatic/Hydraulic', u'Blown Objects'),
        157: (u'Pneumatic/Hydraulic', u'Crossflow'),
        158: (u'Pneumatic/Hydraulic', u'Dynamic Pressure Loading'),
        159: (u'Pneumatic/Hydraulic', u'Hydraulic Ram'),
        160: (u'Pneumatic/Hydraulic', u'Implosion'),
        161: (u'Pneumatic/Hydraulic', u'Inadvertent Release'),
        162: (u'Pneumatic/Hydraulic', u'Miscalibrated Relief Device'),
        163: (u'Pneumatic/Hydraulic', u'Mislocated Relief Device'),
        164: (u'Pneumatic/Hydraulic', u'Overpressurization'),
        165: (u'Pneumatic/Hydraulic', u'Pipe/Hose Whip'),
        166: (u'Pneumatic/Hydraulic', u'Pipe/Vessel/Duct Rupture'),
        167: (u'Pneumatic/Hydraulic', u'Relief Pressure Improperly Set'),
        168: (u'Thermal',
              u'Altered Structural Properties (e.g., Embrittlement)'),
        169: (u'Thermal', u'Confined Gas/Liquid'),
        170: (u'Thermal', u'Elevated Flammability'),
        171: (u'Thermal', u'Elevated Reactivity'),
        172: (u'Thermal', u'Elevated Volatility'),
        173: (u'Thermal', u'Freezing'),
        174: (u'Thermal', u'Heat Source/Sink'),
        175: (u'Thermal', u'Hot/Cold Surface Burns'),
        176: (u'Thermal', u'Humidity/Moisture'),
        177: (u'Thermal', u'Pressure Evaluation'),
        178: (u'Unannunciated Utility Outages', u'Air Conditioning'),
        179: (u'Unannunciated Utility Outages', u'Compressed Air/Gas'),
        180: (u'Unannunciated Utility Outages', u'Electricity'),
        181: (u'Unannunciated Utility Outages', u'Exhaust'),
        182: (u'Unannunciated Utility Outages', u'Fuel'),
        183: (u'Unannunciated Utility Outages', u'Heating/Cooling'),
        184: (u'Unannunciated Utility Outages', u'Lubrication Drains/Sumps'),
        185: (u'Unannunciated Utility Outages', u'Steam'),
        186: (u'Unannunciated Utility Outages', u'Ventilation')
    }
    assert _configuration.RTK_MANUFACTURERS == {
        1: ('Sprague', 'New Hampshire', '13606'),
        2: ('Xilinx', '', ''),
        3: ('National Semiconductor', 'California', '27014')
    }
    assert _configuration.RTK_MEASUREMENT_UNITS == {
        1: (u'lbf', u'Pounds Force', u'unit'),
        2: (u'lbm', u'Pounds Mass', u'unit'),
        3: (u'hrs', u'hours', u'unit'),
        4: (u'N', u'Newtons', u'unit'),
        5: (u'mins', u'minutes', u'unit'),
        6: (u'secs', u'seconds', u'unit'),
        7: (u'g', u'grams', u'unit'),
        8: (u'oz', u'ounces', u'unit'),
        9: (u'A', u'Amperes', u'unit'),
        10: (u'V', u'Volts', u'unit')
    }
    assert _configuration.RTK_STAKEHOLDERS == {
        1: ('Customer', ),
        2: ('Service', ),
        3: ('Manufacturing', ),
        4: ('Management', )
    }
    assert _configuration.RTK_SUBCATEGORIES == {
        1: {
            1: u'Linear',
            2: u'Logic',
            3: u'PAL, PLA',
            4: u'Microprocessor, Microcontroller',
            5: u'Memory, ROM',
            6: u'Memory, EEPROM',
            7: u'Memory, DRAM',
            8: u'Memory, SRAM',
            9: u'GaAs',
            10: u'VHSIC, VLSI'
        },
        2: {
            11: u'Diode, Low Frequency',
            12: u'Diode, High Frequency',
            13: u'Transistor, Low Frequency, Bipolar',
            14: u'Transistor, Low Frequency, Si FET',
            15: u'Transistor, Unijunction',
            16: u'Transistor, High Frequency, Low Noise, Bipolar',
            17: u'Transistor, High Frequency, High Power, Bipolar',
            18: u'Transistor, High Frequency, GaAs FET',
            19: u'Transistor, High Frequency, Si FET',
            20: u'Thyristor, SCR',
            21: u'Optoelectronic, Detector, Isolator, Emitter',
            22: u'Optoelectronic, Alphanumeric Display',
            23: u'Optoelectronic, Laser Diode'
        },
        3: {
            32: u'Variable, Wirewound (RT, RTR)',
            33: u'Variable, Wirewound, Precision (RR)',
            34: u'Variable, Wirewound, Semiprecision (RA, RK)',
            35: u'Variable, Wirewound, Power (RP)',
            36: u'Variable, Non-Wirewound (RJ, RJR)',
            37: u'Variable, Composition (RV)',
            38: u'Variable, Non-Wirewound, Film and Precision (RQ, RVC)',
            24: u'Fixed, Composition (RC, RCR)',
            25: u'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)',
            26: u'Fixed, Film, Power (RD)',
            27: u'Fixed, Film, Network (RZ)',
            28: u'Fixed, Wirewound (RB, RBR)',
            29: u'Fixed, Wirewound, Power (RW, RWR)',
            30: u'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)',
            31: u'Thermistor (RTH)'
        },
        4: {
            39:
            u'Fixed, Paper, Bypass (CA, CP)',
            40:
            u'Fixed, Feed-Through (CZ, CZR)',
            41:
            u'Fixed, Paper and Plastic Film (CPV, CQ, CQR)',
            42:
            u'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)',
            43:
            u'Fixed, Plastic and Metallized Plastic',
            44:
            u'Fixed, Super-Metallized Plastic (CRH)',
            45:
            u'Fixed, Mica (CM, CMR)',
            46:
            u'Fixed, Mica, Button (CB)',
            47:
            u'Fixed, Glass (CY, CYR)',
            48:
            u'Fixed, Ceramic, General Purpose (CK, CKR)',
            49:
            u'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)',
            50:
            u'Fixed, Electrolytic, Tantalum, Solid (CSR)',
            51:
            u'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)',
            52:
            u'Fixed, Electrolytic, Aluminum (CU, CUR)',
            53:
            u'Fixed, Electrolytic (Dry), Aluminum (CE)',
            54:
            u'Variable, Ceramic (CV)',
            55:
            u'Variable, Piston Type (PC)',
            56:
            u'Variable, Air Trimmer (CT)',
            57:
            u'Variable and Fixed, Gas or Vacuum (CG)'
        },
        5: {
            58: u'Transformer',
            59: u'Coil'
        },
        6: {
            60: u'Mechanical',
            61: u'Solid State'
        },
        7: {
            64: u'Rotary',
            65: u'Thumbwheel',
            66: u'Circuit Breaker',
            62: u'Toggle or Pushbutton',
            63: u'Sensitive'
        },
        8: {
            67: u'Multi-Pin',
            68: u'PCB Edge',
            69: u'IC Socket',
            70: u'Plated Through Hole (PTH)',
            71: u'Connection, Non-PTH'
        },
        9: {
            72: u'Elapsed Time',
            73: u'Panel'
        },
        10: {
            74: u'Crystal',
            75: u'Filter, Non-Tunable Electronic',
            76: u'Fuse',
            77: u'Lamp'
        }
    }
    assert _configuration.RTK_USERS == {
        1: (u'Tester', u'Johnny', u'tester.johnny@reliaqual.com',
            u'+1.269.867.5309', '1')
    }


@pytest.mark.integration
def test_validate_license(test_common_dao, test_dao):
    """ validate_license() should return a zero error code on success. """
    DUT = Model(test_common_dao, test_dao)

    (_error_code, _msg) = DUT.validate_license('0000')

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Validating RTK License.')


@pytest.mark.integration
def test_validate_license_wrong_key(test_common_dao, test_dao):
    """ validate_license() should return a 1 error code when the license key is wrong. """
    DUT = Model(test_common_dao, test_dao)

    _error_code, _msg = DUT.validate_license('')

    assert _error_code == 1
    assert _msg == ('RTK ERROR: Invalid license (Invalid key).  Your license '
                    'key is incorrect.  Closing the RTK application.')


@pytest.mark.broken_test
def test_initialize_controller():
    """ __init__() should create an instance of the rtk.RTK object. """
    DUT = RTK(test=True)

    assert isinstance(DUT, RTK)
    assert isinstance(DUT.rtk_model, Model)
    assert isinstance(DUT.dic_books['listbook'], ListBook)
    assert isinstance(DUT.dic_books['modulebook'], ModuleBook)
    assert isinstance(DUT.dic_books['workbook'], WorkBook)
    assert DUT.dic_controllers['revision'] is None
    assert DUT.dic_controllers['function'] is None
    assert DUT.dic_controllers['requirement'] is None
    assert DUT.dic_controllers['hardware'] is None
    assert DUT.dic_controllers['software'] is None
    assert DUT.dic_controllers['testing'] is None
    assert DUT.dic_controllers['validation'] is None
    assert DUT.dic_controllers['incident'] is None
    assert DUT.dic_controllers['survival'] is None
    assert DUT.dic_controllers['matrices'] is None
    assert DUT.dic_controllers['profile'] is None
    assert DUT.dic_controllers['definition'] is None
    assert DUT.dic_controllers['fmea'] is None
    assert DUT.dic_controllers['stakeholder'] is None
    assert DUT.dic_controllers['allocation'] is None
    assert DUT.dic_controllers['hazard'] is None
    assert DUT.dic_controllers['similaritem'] is None
    assert DUT.dic_controllers['pof'] is None
    assert DUT.dic_controllers['growth'] is None
    assert DUT.dic_controllers['action'] is None
    assert DUT.dic_controllers['component'] is None


@pytest.mark.broken_test
def test_request_validate_license():
    """ request_validate_license() should return False on success. """
    DUT = RTK(test=True)

    assert not DUT.request_validate_license()


@pytest.mark.broken_test
def test_request_load_globals(test_configuration):
    """ request_load_globals() should return False on success. """
    _configuration = test_configuration
    DUT = RTK(test=True)

    _database = _configuration.RTK_COM_BACKEND + ':///' + \
                _configuration.RTK_COM_INFO['database']
    DUT.rtk_model.program_dao.db_connect(_database)

    assert not DUT.request_load_globals()


@pytest.mark.broken_test
def test_request_create_program(test_configuration):
    """ request_create_program() should return False on success. """
    DUT = RTK(test=True)
    DUT.RTK_CONFIGURATION = test_configuration

    assert not DUT.request_create_program()


@pytest.mark.broken_test
def test_request_open_program(test_configuration):
    """ request_open_program() should return False on success. """
    DUT = RTK(test=True)
    DUT.RTK_CONFIGURATION = test_configuration

    assert not DUT.request_open_program()
    assert DUT.RTK_CONFIGURATION.RTK_PREFIX == {
        'function': [u'FUNC', 0],
        'requirement': [u'RQMT', 0],
        'assembly': [u'ASSY', 0],
        'fmeca': [u'FMECA', 0],
        'effect': [u'EFFECT', 0],
        'part': [u'PART', 0],
        'mode': [u'MODE', 0],
        'software': [u'MODULE', 0],
        'cause': [u'CAUSE', 0],
        'revision': [u'REV', 0]
    }
    assert DUT.RTK_CONFIGURATION.RTK_MODULES == {
        'function': 1,
        'fta': 0,
        'requirement': 1,
        'validation': 1,
        'survival': 1,
        'testing': 1,
        'rbd': 0,
        'hardware': 1,
        'rcm': 0,
        'incident': 1,
        'revision': 1,
        'software': 1
    }


@pytest.mark.broken_test
def test_request_save_program():
    """ request_save_program() should return False on success. """
    DUT = RTK(test=True)
    DUT.RTK_CONFIGURATION.RTK_BACKEND = 'sqlite'
    DUT.RTK_CONFIGURATION.RTK_PROG_INFO = {
        'host': 'localhost',
        'socket': 3306,
        'database': '/tmp/TestDB.rtk',
        'user': '',
        'password': ''
    }
    DUT.request_open_program()

    assert not DUT.request_save_program()


@pytest.mark.broken_test
def test_request_close_program():
    """ request_close_program() should return False on success. """
    DUT = RTK(test=True)
    DUT.RTK_CONFIGURATION.RTK_BACKEND = 'sqlite'
    DUT.RTK_CONFIGURATION.RTK_PROG_INFO = {
        'host': 'localhost',
        'socket': 3306,
        'database': '/tmp/TestDB.rtk',
        'user': '',
        'password': ''
    }
    DUT.request_open_program()

    assert not DUT.request_close_program()
