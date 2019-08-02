# -*- coding: utf-8 -*-
#
#       ramstk.tests.test_ramstk.py is part of The RAMSTK Project
#
# All rights reserved.
"""This is the test class for the RAMSTK module algorithms and models."""

# Standard Library Imports
import logging
import os
import tempfile

# Third Party Imports
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.Configuration import Configuration
from ramstk.dao.DAO import DAO
from ramstk.gui.gtk.mwi.ListBook import ListBook
from ramstk.gui.gtk.mwi.ModuleBook import ModuleBook
from ramstk.gui.gtk.mwi.WorkBook import WorkBook
from ramstk.RAMSTK import RAMSTK, Model, _initialize_loggers

TEMPDIR = tempfile.gettempdir()


@pytest.mark.integration
def test_initialize_logger(test_configuration):
    """ _initialize_loggers() should return a tuple of logging.Logger instances. """
    _configuration = test_configuration

    (
        _configuration.RAMSTK_DEBUG_LOG,
        _configuration.RAMSTK_USER_LOG,
        _configuration.RAMSTK_IMPORT_LOG,
    ) = _initialize_loggers(_configuration)

    assert isinstance(_configuration.RAMSTK_DEBUG_LOG, logging.Logger)
    assert isinstance(_configuration.RAMSTK_USER_LOG, logging.Logger)
    assert isinstance(_configuration.RAMSTK_IMPORT_LOG, logging.Logger)
    assert os.path.isfile(_configuration.RAMSTK_LOG_DIR + '/RAMSTK_debug.log')
    assert os.path.isfile(_configuration.RAMSTK_LOG_DIR + '/RAMSTK_user.log')
    assert os.path.isfile(_configuration.RAMSTK_LOG_DIR + '/RAMSTK_import.log')


@pytest.mark.integration
def test_initialize_model(test_common_dao, test_dao):
    """ __init__() should create an instance of the RAMSTK.Model object. """
    DUT = Model(test_common_dao, test_dao)

    assert isinstance(DUT, Model)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.site_dao, DAO)
    assert isinstance(DUT.program_dao, DAO)
    assert DUT.program_session is None


@pytest.mark.integration
def test_do_create_new_program(test_common_dao, test_dao, test_configuration):
    """ do_create_program() should return a zero error code on success. """
    DUT = Model(test_common_dao, test_dao)
    print(TEMPDIR)
    _configuration = test_configuration
    _database = (
        _configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_test_db.ramstk'
    )
    _error_code, _msg = DUT.do_create_program(_database)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Creating RAMSTK Program database {0:s}.'.
        format(_database)
    )


@pytest.mark.integration
def test_do_create_new_program_failed(test_common_dao, test_dao):
    """ do_create_program() should return a non-zero error code on failure. """
    DUT = Model(test_common_dao, test_dao)

    _database = 'sqlite:/' + TEMPDIR + '/BigAssTestDB.ramstk'
    _error_code, _msg = DUT.do_create_program(_database)

    assert _error_code == 1
    assert _msg == (
        'RAMSTK ERROR: Failed to create RAMSTK Program database '
        'sqlite:/' + TEMPDIR + '/BigAssTestDB.ramstk.'
    )


@pytest.mark.integration
def test_do_open_program(test_common_dao, test_dao, test_configuration):
    """ do_open_program() should return a zero error code on success. """
    DUT = Model(test_common_dao, test_dao)

    _configuration = test_configuration
    _database = _configuration.RAMSTK_BACKEND + ':///' + \
                _configuration.RAMSTK_PROG_INFO['database']
    _error_code, _msg = DUT.do_open_program(_database)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Opening RAMSTK Program database {0:s}.'.
        format(_database)
    )


@pytest.mark.integration
def test_load_globals(test_common_dao, test_dao):
    """ load_globals() should return False on success. """
    DUT = Model(test_common_dao, test_dao)
    _configuration = Configuration()

    assert not DUT.do_load_globals(_configuration)

    assert isinstance(DUT.tree, Tree)

    assert _configuration.RAMSTK_ACTION_CATEGORY == {
        38: ('ENGD', 'Engineering, Design', 'action', 1),
        39: ('ENGR', 'Engineering, Reliability', 'action', 1),
        40: ('ENGS', 'Engineering, Systems', 'action', 1),
        41: ('MAN', 'Manufacturing', 'action', 1),
        42: ('TEST', 'Test', 'action', 1),
        43: ('VANDV', 'Verification & Validation', 'action', 1),
    }
    assert _configuration.RAMSTK_INCIDENT_CATEGORY == {
        35: ('HW', 'Hardware', 'incident', 1),
        36: ('SW', 'Software', 'incident', 1),
        37: ('PROC', 'Process', 'incident', 1),
    }
    assert _configuration.RAMSTK_SEVERITY == {
        11: ('INS', 'Insignificant', 'risk', 1),
        12: ('SLT', 'Slight', 'risk', 2),
        13: ('LOW', 'Low', 'risk', 3),
        14: ('MED', 'Medium', 'risk', 4),
        15: ('HI', 'High', 'risk', 5),
        16: ('MAJ', 'Major', 'risk', 6),
    }

    assert _configuration.RAMSTK_AFFINITY_GROUPS == {
        8: ('Durability', 'affinity'),
        9: ('Cost', 'affinity'),
        7: ('Reliability', 'affinity'),
    }
    assert _configuration.RAMSTK_WORKGROUPS == {
        1: ('Engineering, Design', 'workgroup'),
        2: ('Engineering, Logistics Support', 'workgroup'),
        3: ('Engineering, Maintainability', 'workgroup'),
        4: ('Engineering, Reliability', 'workgroup'),
        5: ('Engineering, Safety', 'workgroup'),
        6: ('Engineering, Software', 'workgroup'),
    }

    assert _configuration.RAMSTK_DETECTION_METHODS == {
        1: ('Code Reviews', '', 'detection'),
        2: ('Error/Anomaly Detection', '', 'detection'),
        3: ('Structure Analysis', '', 'detection'),
        4: ('Random Testing', '', 'detection'),
        5: ('Functional Testing', '', 'detection'),
        6: ('Branch Testing', '', 'detection'),
    }

    assert _configuration.RAMSTK_DAMAGE_MODELS == {
        1: ('Adhesion Wear Model for Bearings', ),
        2: ('Arrhenius', ),
        3: ('Coffin-Manson', ),
        4: ('Empirical/DOE', ),
        5: ('Eyring', ),
        6: ('Inverse Power Law (IPL)', ),
        7: ('IPL - Arrhenius', ),
        8: ('Time Fraction of Damaging Operating Conditions', ),
    }

    assert _configuration.RAMSTK_ACTION_STATUS == {
        11: ('Initiated', 'Action has been initiated.', 'action'),
        12: ('Reviewed', 'Action has been reviewed.', 'action'),
        13: ('Approved', 'Action has been approved.', 'action'),
        14: (
            'Ready for Closure',
            'Action is ready to be closed.',
            'action',
        ),
        15: ('Closed', 'Action has been closed.', 'action'),
    }
    assert _configuration.RAMSTK_INCIDENT_STATUS == {
        1: ('Initiated', 'Incident has been initiated.', 'incident'),
        2: ('Reviewed', 'Incident has been reviewed.', 'incident'),
        3: (
            'Analysis',
            'Incident has been assigned and is being analyzed.',
            'incident',
        ),
        4: (
            'Solution Identified',
            'A solution to the reported problem has been identified.',
            'incident',
        ),
        5: (
            'Solution Implemented',
            'A solution to the reported problem has been implemented.',
            'incident',
        ),
        6: (
            'Solution Verified',
            'A solution to the reported problem has been verified.',
            'incident',
        ),
        7: (
            'Ready for Approval',
            'Incident analysis is ready to be approved.',
            'incident',
        ),
        8: ('Approved', 'Incident analysis has been approved.', 'incident'),
        9: (
            'Ready for Closure',
            'Incident is ready to be closed.',
            'incident',
        ),
        10: ('Closed', 'Incident has been closed.', 'incident'),
    }
    assert _configuration.RAMSTK_INCIDENT_TYPE == {
        1: ('PLN', 'Planning', 'incident'),
        2: ('CON', 'Concept', 'incident'),
        3: ('RQMT', 'Requirement', 'incident'),
        4: ('DES', 'Design', 'incident'),
        5: ('COD', 'Coding', 'incident'),
        6: ('DB', 'Database', 'incident'),
        7: ('TI', 'Test Information', 'incident'),
        8: ('MAN', 'Manuals', 'incident'),
        9: ('OTH', 'Other', 'incident'),
    }
    assert _configuration.RAMSTK_REQUIREMENT_TYPE == {
        10: ('FUN', 'Functional', 'requirement'),
        11: ('PRF', 'Performance', 'requirement'),
        12: ('REG', 'Regulatory', 'requirement'),
        13: ('REL', 'Reliability', 'requirement'),
        14: ('SAF', 'Safety', 'requirement'),
        15: ('SVC', 'Serviceability', 'requirement'),
        16: ('USE', 'Useability', 'requirement'),
    }
    assert _configuration.RAMSTK_VALIDATION_TYPE == {
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
        33: (
            'EMA',
            'System Engineering, Electromagnetic Analysis',
            'validation',
        ),
        34: ('FEA', 'System Engineering, FEA', 'validation'),
        35: ('2DM', 'System Engineering, 2D Model', 'validation'),
        36: ('3DM', 'System Engineering, 3D Model', 'validation'),
        37: ('SRD', 'System Engineering, Robust Design', 'validation'),
        38: (
            'SCA',
            'System Engineering, Sneak Circuit Analysis',
            'validation',
        ),
        39: ('THA', 'System Engineering, Thermal Analysis', 'validation'),
        40: ('TOL', 'System Engineering, Tolerance Analysis', 'validation'),
        41: ('WCA', 'System Engineering, Worst Case Analysis', 'validation'),
    }

    assert _configuration.RAMSTK_CATEGORIES == {
        1: 'Integrated Circuit',
        2: 'Semiconductor',
        3: 'Resistor',
        4: 'Capacitor',
        5: 'Inductive Device',
        6: 'Relay',
        7: 'Switching Device',
        8: 'Connection',
        9: 'Meter',
        10: 'Miscellaneous',
    }
    assert _configuration.RAMSTK_FAILURE_MODES == {
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
            10: {},
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
            23: {},
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
                3: ['Parameter Change', 0.2, 'FMD-97'],
            },
            25: {},
            26: {},
            27: {},
            28: {},
            29: {},
            30: {},
            31: {},
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
            57: {},
        },
        5: {
            58: {},
            59: {},
        },
        6: {
            60: {},
            61: {},
        },
        7: {
            64: {},
            65: {},
            66: {},
            62: {},
            63: {},
        },
        8: {
            67: {},
            68: {},
            69: {},
            70: {},
            71: {},
        },
        9: {
            72: {},
            73: {},
        },
        10: {
            74: {},
            75: {},
            76: {},
            77: {},
        },
    }
    assert _configuration.RAMSTK_HAZARDS == {
        1: ('Acceleration/Gravity', 'Falls'),
        2: ('Acceleration/Gravity', 'Falling Objects'),
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
        168: (
            'Thermal',
            'Altered Structural Properties (e.g., Embrittlement)',
        ),
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
        186: ('Unannunciated Utility Outages', 'Ventilation'),
    }
    assert _configuration.RAMSTK_MANUFACTURERS == {
        1: ('Sprague', 'New Hampshire', '13606'),
        2: ('Xilinx', '', ''),
        3: ('National Semiconductor', 'California', '27014'),
    }
    assert _configuration.RAMSTK_MEASUREMENT_UNITS == {
        1: ('lbf', 'Pounds Force', 'unit'),
        2: ('lbm', 'Pounds Mass', 'unit'),
        3: ('hrs', 'hours', 'unit'),
        4: ('N', 'Newtons', 'unit'),
        5: ('mins', 'minutes', 'unit'),
        6: ('secs', 'seconds', 'unit'),
        7: ('g', 'grams', 'unit'),
        8: ('oz', 'ounces', 'unit'),
        9: ('A', 'Amperes', 'unit'),
        10: ('V', 'Volts', 'unit'),
    }
    assert _configuration.RAMSTK_STAKEHOLDERS == {
        1: ('Customer', ),
        2: ('Service', ),
        3: ('Manufacturing', ),
        4: ('Management', ),
    }
    assert _configuration.RAMSTK_STRESS_LIMITS == {
        1: (
            0.8,
            0.9,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        ),
        2: (
            1.0,
            1.0,
            0.7,
            0.9,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        ),
        3: (
            1.0,
            1.0,
            0.5,
            0.9,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        ),
        4: (
            1.0,
            1.0,
            1.0,
            1.0,
            0.6,
            0.9,
            10.0,
            0.0,
            125.0,
            125.0,
        ),
        5: (
            .6,
            0.9,
            1.0,
            1.0,
            0.5,
            0.9,
            15.0,
            0.0,
            125.0,
            125.0,
        ),
        6: (
            0.75,
            0.9,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        ),
        7: (
            0.75,
            0.9,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        ),
        8: (
            0.7,
            0.9,
            1.0,
            1.0,
            0.7,
            0.9,
            25.0,
            0.0,
            125.0,
            125.0,
        ),
        9: (
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        ),
        10: (
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        ),
    }
    assert _configuration.RAMSTK_SUBCATEGORIES == {
        1: {
            1: 'Linear',
            2: 'Logic',
            3: 'PAL, PLA',
            4: 'Microprocessor, Microcontroller',
            5: 'Memory, ROM',
            6: 'Memory, EEPROM',
            7: 'Memory, DRAM',
            8: 'Memory, SRAM',
            9: 'GaAs',
            10: 'VHSIC, VLSI',
        },
        2: {
            11: 'Diode, Low Frequency',
            12: 'Diode, High Frequency',
            13: 'Transistor, Low Frequency, Bipolar',
            14: 'Transistor, Low Frequency, Si FET',
            15: 'Transistor, Unijunction',
            16: 'Transistor, High Frequency, Low Noise, Bipolar',
            17: 'Transistor, High Frequency, High Power, Bipolar',
            18: 'Transistor, High Frequency, GaAs FET',
            19: 'Transistor, High Frequency, Si FET',
            20: 'Thyristor, SCR',
            21: 'Optoelectronic, Detector, Isolator, Emitter',
            22: 'Optoelectronic, Alphanumeric Display',
            23: 'Optoelectronic, Laser Diode',
        },
        3: {
            32: 'Variable, Wirewound (RT, RTR)',
            33: 'Variable, Wirewound, Precision (RR)',
            34: 'Variable, Wirewound, Semiprecision (RA, RK)',
            35: 'Variable, Wirewound, Power (RP)',
            36: 'Variable, Non-Wirewound (RJ, RJR)',
            37: 'Variable, Composition (RV)',
            38: 'Variable, Non-Wirewound, Film and Precision (RQ, RVC)',
            24: 'Fixed, Composition (RC, RCR)',
            25: 'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)',
            26: 'Fixed, Film, Power (RD)',
            27: 'Fixed, Film, Network (RZ)',
            28: 'Fixed, Wirewound (RB, RBR)',
            29: 'Fixed, Wirewound, Power (RW, RWR)',
            30: 'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)',
            31: 'Thermistor (RTH)',
        },
        4: {
            39: 'Fixed, Paper, Bypass (CA, CP)',
            40: 'Fixed, Feed-Through (CZ, CZR)',
            41: 'Fixed, Paper and Plastic Film (CPV, CQ, CQR)',
            42: 'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)',
            43: 'Fixed, Plastic and Metallized Plastic',
            44: 'Fixed, Super-Metallized Plastic (CRH)',
            45: 'Fixed, Mica (CM, CMR)',
            46: 'Fixed, Mica, Button (CB)',
            47: 'Fixed, Glass (CY, CYR)',
            48: 'Fixed, Ceramic, General Purpose (CK, CKR)',
            49:
            'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)',
            50: 'Fixed, Electrolytic, Tantalum, Solid (CSR)',
            51: 'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)',
            52: 'Fixed, Electrolytic, Aluminum (CU, CUR)',
            53: 'Fixed, Electrolytic (Dry), Aluminum (CE)',
            54: 'Variable, Ceramic (CV)',
            55: 'Variable, Piston Type (PC)',
            56: 'Variable, Air Trimmer (CT)',
            57: 'Variable and Fixed, Gas or Vacuum (CG)',
        },
        5: {
            58: 'Transformer',
            59: 'Coil',
        },
        6: {
            60: 'Mechanical',
            61: 'Solid State',
        },
        7: {
            64: 'Rotary',
            65: 'Thumbwheel',
            66: 'Circuit Breaker',
            62: 'Toggle or Pushbutton',
            63: 'Sensitive',
        },
        8: {
            67: 'Multi-Pin',
            68: 'PCB Edge',
            69: 'IC Socket',
            70: 'Plated Through Hole (PTH)',
            71: 'Connection, Non-PTH',
        },
        9: {
            72: 'Elapsed Time',
            73: 'Panel',
        },
        10: {
            74: 'Crystal',
            75: 'Filter, Non-Tunable Electronic',
            76: 'Fuse',
            77: 'Lamp',
        },
    }
    assert _configuration.RAMSTK_USERS == {
        1: (
            'Tester',
            'Johnny',
            'tester.johnny@reliaqual.com',
            '+1.269.867.5309',
            '1',
        ),
    }


@pytest.mark.integration
def test_do_validate_license(test_common_dao, test_dao):
    """ do_validate_license() should return a zero error code on success. """
    DUT = Model(test_common_dao, test_dao)

    (_error_code, _msg) = DUT.do_validate_license('0000')

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Validating RAMSTK License.')


@pytest.mark.integration
def test_do_validate_license_wrong_key(test_common_dao, test_dao):
    """ do_validate_license() should return a 1 error code when the license key is wrong. """
    DUT = Model(test_common_dao, test_dao)

    _error_code, _msg = DUT.do_validate_license('')

    assert _error_code == 1
    assert _msg == (
        'RAMSTK ERROR: Invalid license (Invalid key).  Your license '
        'key is incorrect.  Closing the RAMSTK application.'
    )


@pytest.mark.broken_test
def test_initialize_controller():
    """ __init__() should create an instance of the ramstk.RAMSTK object. """
    DUT = RAMSTK(test=True)

    assert isinstance(DUT, RAMSTK)
    assert isinstance(DUT.ramstk_model, Model)
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
def test_request_do_validate_license():
    """ do_request_validate_license() should return False on success. """
    DUT = RAMSTK(test=True)

    assert not DUT.request_do_validate_license()


@pytest.mark.broken_test
def test_request_do_load_globals(test_configuration):
    """ request_load_globals() should return False on success. """
    _configuration = test_configuration
    DUT = RAMSTK(test=True)

    _database = _configuration.RAMSTK_COM_BACKEND + ':///' + \
                _configuration.RAMSTK_COM_INFO['database']
    DUT.ramstk_model.program_dao.db_connect(_database)

    assert not DUT.request_do_load_globals()


@pytest.mark.broken_test
def test_request_do_create_program(test_configuration):
    """ request_create_program() should return False on success. """
    DUT = RAMSTK(test=True)
    DUT.RAMSTK_CONFIGURATION = test_configuration

    assert not DUT.request_do_create_program()


@pytest.mark.broken_test
def test_request_do_open_program(test_configuration):
    """ request_open_program() should return False on success. """
    DUT = RAMSTK(test=True)
    DUT.RAMSTK_CONFIGURATION = test_configuration

    assert not DUT.request_do_open_program()
    assert DUT.RAMSTK_CONFIGURATION.RAMSTK_PREFIX == {
        'function': ['FUNC', 0],
        'requirement': ['RQMT', 0],
        'assembly': ['ASSY', 0],
        'fmeca': ['FMECA', 0],
        'effect': ['EFFECT', 0],
        'part': ['PART', 0],
        'mode': ['MODE', 0],
        'software': ['MODULE', 0],
        'cause': ['CAUSE', 0],
        'revision': ['REV', 0],
    }
    assert DUT.RAMSTK_CONFIGURATION.RAMSTK_MODULES == {
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
        'software': 1,
    }


@pytest.mark.broken_test
def test_request_do_save_program():
    """ request_save_program() should return False on success. """
    DUT = RAMSTK(test=True)
    DUT.RAMSTK_CONFIGURATION.RAMSTK_BACKEND = 'sqlite'
    DUT.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO = {
        'host': 'localhost',
        'socket': 3306,
        'database': TEMPDIR + '/TestDB.ramstk',
        'user': '',
        'password': '',
    }
    DUT.request_do_open_program()

    assert not DUT.request_do_save_program()


@pytest.mark.broken_test
def test_request_do_close_program():
    """ request_close_program() should return False on success. """
    DUT = RAMSTK(test=True)
    DUT.RAMSTK_CONFIGURATION.RAMSTK_BACKEND = 'sqlite'
    DUT.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO = {
        'host': 'localhost',
        'socket': 3306,
        'database': TEMPDIR + '/TestDB.ramstk',
        'user': '',
        'password': '',
    }
    DUT.request_do_open_program()

    assert not DUT.request_do_close_program()
