# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.db.test_common.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for common database methods and operations."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mock import patch
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.db.common import (
    _do_load_action_variables, _do_load_hardware_variables,
    _do_load_incident_variables, _do_load_miscellaneous_variables,
    _do_load_pof_variables, _do_load_rpn_variables, _do_load_severity,
    _do_load_user_workgroups, _load_fmea_tables, _load_hazard_analysis_tables,
    _load_incident_report_tables, _load_miscellaneous_tables,
    _load_pof_tables, _load_site_info, do_add_administrator,
    do_create_common_db, do_load_variables, do_make_commondb_tables
)
from ramstk.models.commondb import RAMSTKSiteInfo, RAMSTKUser

TEST_COMMON_DB = BaseDatabase()
TEST_COMMON_DB.do_connect({
    "dialect": "sqlite",
    "host": "localhost",
    "port": "3306",
    "database": ":memory:",
    "user": "johnny.tester",
    "password": "clear.text.password"})


def on_fail_read_license(error_message):
    assert error_message == ('Unable to read license key file.  Defaulting '
                             'to a 30-day demo license.')
    print("\033[35m\nfail_read_license topic was broadcast.")


def test_create_common_db_tables():
    """do_make_commondb_tables() should return None when successfully creating the tables in the RAMSTK common database."""
    assert do_make_commondb_tables(TEST_COMMON_DB.engine) is None
    assert TEST_COMMON_DB.do_insert(RAMSTKSiteInfo()) is None
    assert TEST_COMMON_DB.get_last_id('ramstk_site_info', 'fld_site_id') == 1


@pytest.mark.usefixtures('test_license_file')
def test_load_site_info_with_license(test_license_file):
    """_load_site_info() should return None and load the license key information when a license key file can be read."""
    assert _load_site_info(TEST_COMMON_DB.session) is None

    # Retrieve the newly create site info record (note this is site ID=2 as the
    # _load_site_info() function creates a new record).  Generally we won't be
    # inserting a record before calling the _load_site_info() function, it just
    # so happens we do here because of the ordering of tests.
    _record = TEST_COMMON_DB.session.query(RAMSTKSiteInfo).filter(
        RAMSTKSiteInfo.site_id == 2).first()
    assert _record.product_key == 'apowdigfb3rh9214839qu'
    assert _record.expire_on == date(2019, 8, 7)


def test_load_site_info_no_license():
    """_load_site_info() should return None and load the default 30-day license when the license key file can't be read."""
    pub.subscribe(on_fail_read_license, 'fail_read_license')

    assert _load_site_info(TEST_COMMON_DB.session) is None

    # Retrieve the newly create site info record (note this is site ID=3 as the
    # _load_site_info() function creates a new record).  Generally we won't be
    # inserting records before calling the _load_site_info() function, it just
    # so happens we do here because of the ordering of tests.
    _record = TEST_COMMON_DB.session.query(RAMSTKSiteInfo).filter(
        RAMSTKSiteInfo.site_id == 3).first()
    assert _record.product_key == '0000'
    assert _record.expire_on == date.today() + timedelta(days=30)

    pub.unsubscribe(on_fail_read_license, 'fail_read_license')


def test_load_miscellaneous_tables():
    """_load_miscellaneous_tables() should return None when successfully populating the miscellaneous tables."""
    assert _load_miscellaneous_tables(TEST_COMMON_DB.session) is None


def test_load_fmea_tables():
    """_load_fmea_tables() should return None when successfully populating the FMEA-related tables."""
    assert _load_fmea_tables(TEST_COMMON_DB.session) is None


def test_load_hazard_analysis_tables():
    """_load_hazard_analysis_tables() should return None when successfully populating the FHA-related tables."""
    assert _load_hazard_analysis_tables(TEST_COMMON_DB.session) is None


def test_load_incident_report_tables():
    """_load_incident_report_tables() should return None when successfully populating the incident report related tables."""
    assert _load_incident_report_tables(TEST_COMMON_DB.session) is None


def test_load_pof_tables():
    """_load_pof_tables() should return None when successfully populating the PoF-related tables."""
    assert _load_pof_tables(TEST_COMMON_DB.session) is None


@patch('builtins.input',
       side_effect=[
           'y', 'tester', 'johnny', 'johnny.tester@reliaqual.com',
           '+1.269.867.5309'
       ])
def test_do_add_administrator(inputs):
    """do_add_administrator() should return None when successfully adding an administrative user to the RAMSTKUser table."""
    assert do_add_administrator(TEST_COMMON_DB.session) is None


@patch('builtins.input', return_value='n')
def test_do_add_administrator_choose_no(inputs):
    """do_add_administrator() should return None when choosing not to add an administrative user to the RAMSTKUser table."""
    assert do_add_administrator(TEST_COMMON_DB.session) is None


@patch('builtins.input',
       side_effect=[
           'y', 'tester', 'johnny', 'johnny.tester@reliaqual.com',
           '+1.269.867.5309'
       ])
def test_do_create_common_db(monkeypatch):
    """do_create_common_db() should return None when successfully creating a RAMSTK common database."""
    TEST_COMMON_DB.do_disconnect()
    TEST_COMMON_DB.do_connect({
        "dialect": "sqlite",
        "host": "localhost",
        "port": "3306",
        "database": ":memory:",
        "user": "johnny.tester",
        "password": "clear.text.password"})

    assert do_create_common_db(TEST_COMMON_DB.engine,
                               TEST_COMMON_DB.session) is None
    _record = TEST_COMMON_DB.session.query(RAMSTKUser).filter(
        RAMSTKUser.user_id == 1).first()
    assert _record.user_lname == 'tester'
    assert _record.user_fname == 'johnny'
    assert _record.user_email == 'johnny.tester@reliaqual.com'
    assert _record.user_phone == '+1.269.867.5309'


@pytest.mark.usefixtures('test_common_dao', 'test_toml_user_configuration')
class TestLoadCommonTables():
    """Class for testing functions to load common database tables."""
    def test_do_load_action_variables(self, test_common_dao,
                                      test_toml_user_configuration):
        """_do_load_action_variables() should load global variables related to actions and return None."""
        assert _do_load_action_variables(test_common_dao,
                                         test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_ACTION_CATEGORY == {
            38: ('ENGD', 'Engineering, Design', 'action', 1),
            39: ('ENGR', 'Engineering, Reliability', 'action', 1),
            40: ('ENGS', 'Engineering, Systems', 'action', 1),
            41: ('MAN', 'Manufacturing', 'action', 1),
            42: ('TEST', 'Test', 'action', 1),
            43: ('VANDV', 'Verification & Validation', 'action', 1)
        }
        assert test_toml_user_configuration.RAMSTK_ACTION_STATUS == {
            11: ('Initiated', 'Action has been initiated.', 'action'),
            12: ('Reviewed', 'Action has been reviewed.', 'action'),
            13: ('Approved', 'Action has been approved.', 'action'),
            14:
            ('Ready for Closure', 'Action is ready to be closed.', 'action'),
            15: ('Closed', 'Action has been closed.', 'action')
        }

    def test_do_load_hardware_variables(self, test_common_dao,
                                        test_toml_user_configuration):
        """_do_load_hardware_variables() should load global variables related to hardware and return None."""
        assert _do_load_hardware_variables(
            test_common_dao, test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_FAILURE_MODES == {
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
                24: {
                    3: ['Parameter Change', 0.2, 'FMD-97']
                },
                25: {},
                26: {},
                27: {},
                28: {},
                29: {},
                30: {},
                31: {},
                32: {},
                33: {},
                34: {},
                35: {},
                36: {},
                37: {},
                38: {}
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
                62: {},
                63: {},
                64: {},
                65: {},
                66: {}
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

        assert test_toml_user_configuration.RAMSTK_STRESS_LIMITS == {
            1: (0.8, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0),
            2: (1.0, 1.0, 0.7, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0),
            3: (1.0, 1.0, 0.5, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0),
            4: (1.0, 1.0, 1.0, 1.0, 0.6, 0.9, 10.0, 0.0, 125.0, 125.0),
            5: (0.6, 0.9, 1.0, 1.0, 0.5, 0.9, 15.0, 0.0, 125.0, 125.0),
            6: (0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0),
            7: (0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0),
            8: (0.7, 0.9, 1.0, 1.0, 0.7, 0.9, 25.0, 0.0, 125.0, 125.0),
            9: (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0),
            10: (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0)
        }
        assert test_toml_user_configuration.RAMSTK_CATEGORIES == {
            1: 'Integrated Circuit',
            2: 'Semiconductor',
            3: 'Resistor',
            4: 'Capacitor',
            5: 'Inductive Device',
            6: 'Relay',
            7: 'Switching Device',
            8: 'Connection',
            9: 'Meter',
            10: 'Miscellaneous'
        }
        assert test_toml_user_configuration.RAMSTK_SUBCATEGORIES == {
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
                10: 'VHSIC, VLSI'
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
                23: 'Optoelectronic, Laser Diode'
            },
            3: {
                24: 'Fixed, Composition (RC, RCR)',
                25: 'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)',
                26: 'Fixed, Film, Power (RD)',
                27: 'Fixed, Film, Network (RZ)',
                28: 'Fixed, Wirewound (RB, RBR)',
                29: 'Fixed, Wirewound, Power (RW, RWR)',
                30: 'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)',
                31: 'Thermistor (RTH)',
                32: 'Variable, Wirewound (RT, RTR)',
                33: 'Variable, Wirewound, Precision (RR)',
                34: 'Variable, Wirewound, Semiprecision (RA, RK)',
                35: 'Variable, Wirewound, Power (RP)',
                36: 'Variable, Non-Wirewound (RJ, RJR)',
                37: 'Variable, Composition (RV)',
                38: 'Variable, Non-Wirewound, Film and Precision (RQ, RVC)'
            },
            4: {
                39: 'Fixed, Paper, Bypass (CA, CP)',
                40: 'Fixed, Feed-Through (CZ, CZR)',
                41: 'Fixed, Paper and Plastic Film (CPV, CQ, CQR)',
                42:
                'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)',
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
                57: 'Variable and Fixed, Gas or Vacuum (CG)'
            },
            5: {
                58: 'Transformer',
                59: 'Coil'
            },
            6: {
                60: 'Mechanical',
                61: 'Solid State'
            },
            7: {
                62: 'Toggle or Pushbutton',
                63: 'Sensitive',
                64: 'Rotary',
                65: 'Thumbwheel',
                66: 'Circuit Breaker'
            },
            8: {
                67: 'Multi-Pin',
                68: 'PCB Edge',
                69: 'IC Socket',
                70: 'Plated Through Hole (PTH)',
                71: 'Connection, Non-PTH'
            },
            9: {
                72: 'Elapsed Time',
                73: 'Panel'
            },
            10: {
                74: 'Crystal',
                75: 'Filter, Non-Tunable Electronic',
                76: 'Fuse',
                77: 'Lamp'
            }
        }

    def test_do_load_incident_variables(self, test_common_dao,
                                        test_toml_user_configuration):
        """_do_load_incident_variables() should load global variables related to incidents and return None."""
        assert _do_load_incident_variables(
            test_common_dao, test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_INCIDENT_CATEGORY == {
            35: ('HW', 'Hardware', 'incident', 1),
            36: ('SW', 'Software', 'incident', 1),
            37: ('PROC', 'Process', 'incident', 1)
        }
        assert test_toml_user_configuration.RAMSTK_INCIDENT_STATUS == {
            1: ('Initiated', 'Incident has been initiated.', 'incident'),
            2: ('Reviewed', 'Incident has been reviewed.', 'incident'),
            3:
            ('Analysis', 'Incident has been assigned and is being analyzed.',
             'incident'),
            4: ('Solution Identified',
                'A solution to the reported problem has been identified.',
                'incident'),
            5: ('Solution Implemented',
                'A solution to the reported problem has been implemented.',
                'incident'),
            6: ('Solution Verified',
                'A solution to the reported problem has been verified.',
                'incident'),
            7: ('Ready for Approval',
                'Incident analysis is ready to be approved.', 'incident'),
            8:
            ('Approved', 'Incident analysis has been approved.', 'incident'),
            9: ('Ready for Closure', 'Incident is ready to be closed.',
                'incident'),
            10: ('Closed', 'Incident has been closed.', 'incident')
        }
        assert test_toml_user_configuration.RAMSTK_INCIDENT_TYPE == {
            1: ('PLN', 'Planning', 'incident'),
            2: ('CON', 'Concept', 'incident'),
            3: ('RQMT', 'Requirement', 'incident'),
            4: ('DES', 'Design', 'incident'),
            5: ('COD', 'Coding', 'incident'),
            6: ('DB', 'Database', 'incident'),
            7: ('TI', 'Test Information', 'incident'),
            8: ('MAN', 'Manuals', 'incident'),
            9: ('OTH', 'Other', 'incident')
        }

    def test_do_load_miscellaneous_variables(self, test_common_dao,
                                             test_toml_user_configuration):
        """_do_load_miscellaneous_variables() should load global variables related to uncategorized and return None."""
        assert _do_load_miscellaneous_variables(
            test_common_dao, test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_DETECTION_METHODS == {
            1: ('Code Reviews', '', 'detection'),
            2: ('Error/Anomaly Detection', '', 'detection'),
            3: ('Structure Analysis', '', 'detection'),
            4: ('Random Testing', '', 'detection'),
            5: ('Functional Testing', '', 'detection'),
            6: ('Branch Testing', '', 'detection')
        }
        assert test_toml_user_configuration.RAMSTK_HAZARDS == {
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
            12:
            ('Chemical/Water Contamination', 'Vessel/Pipe/Conduit Rupture'),
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
            168:
            ('Thermal', 'Altered Structural Properties (e.g., Embrittlement)'),
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

        assert test_toml_user_configuration.RAMSTK_MANUFACTURERS == {
            1: ('Sprague', 'New Hampshire', '13606'),
            2: ('Xilinx', '', ''),
            3: ('National Semiconductor', 'California', '27014')
        }
        assert test_toml_user_configuration.RAMSTK_MEASUREMENT_UNITS == {
            1: ('lbf', 'Pounds Force', 'unit'),
            2: ('lbm', 'Pounds Mass', 'unit'),
            3: ('hrs', 'hours', 'unit'),
            4: ('N', 'Newtons', 'unit'),
            5: ('mins', 'minutes', 'unit'),
            6: ('secs', 'seconds', 'unit'),
            7: ('g', 'grams', 'unit'),
            8: ('oz', 'ounces', 'unit'),
            9: ('A', 'Amperes', 'unit'),
            10: ('V', 'Volts', 'unit')
        }
        assert test_toml_user_configuration.RAMSTK_VALIDATION_TYPE == {
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
            33: ('EMA', 'System Engineering, Electromagnetic Analysis',
                 'validation'),
            34: ('FEA', 'System Engineering, FEA', 'validation'),
            35: ('2DM', 'System Engineering, 2D Model', 'validation'),
            36: ('3DM', 'System Engineering, 3D Model', 'validation'),
            37: ('SRD', 'System Engineering, Robust Design', 'validation'),
            38: ('SCA', 'System Engineering, Sneak Circuit Analysis',
                 'validation'),
            39: ('THA', 'System Engineering, Thermal Analysis', 'validation'),
            40:
            ('TOL', 'System Engineering, Tolerance Analysis', 'validation'),
            41:
            ('WCA', 'System Engineering, Worst Case Analysis', 'validation')
        }

    def test_do_load_pof_variables(self, test_common_dao,
                                   test_toml_user_configuration):
        """_do_load_pof_variables() should load global variables related to physics of failure analysis and return None."""
        assert _do_load_pof_variables(test_common_dao,
                                      test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_DAMAGE_MODELS == {
            1: 'Adhesion Wear Model for Bearings',
            2: 'Arrhenius',
            3: 'Coffin-Manson',
            4: 'Empirical/DOE',
            5: 'Eyring',
            6: 'Inverse Power Law (IPL)',
            7: 'IPL - Arrhenius',
            8: 'Time Fraction of Damaging Operating Conditions'
        }
        assert test_toml_user_configuration.RAMSTK_LOAD_HISTORY == {
            1: 'Cycle Counts',
            2: 'Histogram',
            3: 'Histogram, Bivariate',
            4: 'Level Crossing',
            5: 'Rain Flow Count',
            6: 'Time at Level',
            7: 'Time at Load',
            8: 'Time at Maximum',
            9: 'Time at Minimum'
        }
        assert test_toml_user_configuration.RAMSTK_MEASURABLE_PARAMETERS == {
            11: ('CN', 'Contamination, Concentration', 'damage'),
            12: ('CS', 'Contamination, Particle Size', 'damage'),
            13: ('LD', 'Dynamic Load', 'damage'),
            14: ('LM', 'Load, Maximum', 'damage'),
            15: ('LMM', 'Load, Minimum-Maximum', 'damage'),
            16: ('NBC', 'Number of Braking Events', 'damage'),
            17: ('NC', 'Number of Cycles', 'damage'),
            18: ('NOE', 'Number of Overload Events', 'damage'),
            19: ('NS', 'Number of Shifts', 'damage'),
            20: ('TIME', 'Operating Time at Condition', 'damage'),
            21: ('PAVG', 'Pressure, Average', 'damage'),
            22: ('DELTAP', 'Pressure, Differential', 'damage'),
            23: ('PPEAK', 'Pressure, Peak', 'damage'),
            24: ('RPM', 'Revolutions per Time', 'damage'),
            25: ('TAMB', 'Temperature, Ambient', 'damage'),
            26: ('TAVG', 'Temperature, Average', 'damage'),
            27: ('DELTAT', 'Temperature, Differential', 'damage'),
            28: ('TPEAK', 'Temperature, Peak', 'damage'),
            29: ('TEMP', 'Temperature = f(Time)', 'damage'),
            30: ('T', 'Torque', 'damage')
        }

    def test_do_load_rpn_variables(self, test_common_dao,
                                   test_toml_user_configuration):
        """_do_load_rpn_variables() should load global variables related to incidents and return None."""
        assert _do_load_rpn_variables(test_common_dao,
                                      test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_RPN_DETECTION == {
            1: {
                'rpn_id': 21,
                'name': 'Almost Certain',
                'description':
                'Design control will almost certainly detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 1
            },
            2: {
                'rpn_id': 22,
                'name': 'Very High',
                'description':
                'Very high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 2
            },
            3: {
                'rpn_id': 23,
                'name': 'High',
                'description':
                'High chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 3
            },
            4: {
                'rpn_id': 24,
                'name': 'Moderately High',
                'description':
                'Moderately high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 4
            },
            5: {
                'rpn_id': 25,
                'name': 'Moderate',
                'description':
                'Moderate chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 5
            },
            6: {
                'rpn_id': 26,
                'name': 'Low',
                'description':
                'Low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 6
            },
            7: {
                'rpn_id': 27,
                'name': 'Very Low',
                'description':
                'Very low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 7
            },
            8: {
                'rpn_id': 28,
                'name': 'Remote',
                'description':
                'Remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 8
            },
            9: {
                'rpn_id': 29,
                'name': 'Very Remote',
                'description':
                'Very remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',
                'rpn_type': 'detection',
                'value': 9
            },
            10: {
                'rpn_id': 30,
                'name': 'Absolute Uncertainty',
                'description':
                'Existing design controls will not or cannot detect a potential mechanism/cause and subsequent failure mode; there is no design control.',
                'rpn_type': 'detection',
                'value': 10
            }
        }
        assert test_toml_user_configuration.RAMSTK_RPN_OCCURRENCE == {
            1: {
                'rpn_id': 11,
                'name': 'Remote',
                'description': 'Failure rate is 1 in 1,500,000.',
                'rpn_type': 'occurrence',
                'value': 1
            },
            2: {
                'rpn_id': 12,
                'name': 'Very Low',
                'description': 'Failure rate is 1 in 150,000.',
                'rpn_type': 'occurrence',
                'value': 2
            },
            3: {
                'rpn_id': 13,
                'name': 'Low',
                'description': 'Failure rate is 1 in 15,000',
                'rpn_type': 'occurrence',
                'value': 3
            },
            4: {
                'rpn_id': 14,
                'name': 'Moderately Low',
                'description': 'Failure rate is 1 in 2000.',
                'rpn_type': 'occurrence',
                'value': 4
            },
            5: {
                'rpn_id': 15,
                'name': 'Moderate',
                'description': 'Failure rate is 1 in 400.',
                'rpn_type': 'occurrence',
                'value': 5
            },
            6: {
                'rpn_id': 16,
                'name': 'Moderately High',
                'description': 'Failure rate is 1 in 80.',
                'rpn_type': 'occurrence',
                'value': 6
            },
            7: {
                'rpn_id': 17,
                'name': 'High',
                'description': 'Failure rate is 1 in 20.',
                'rpn_type': 'occurrence',
                'value': 7
            },
            8: {
                'rpn_id': 18,
                'name': 'Very High',
                'description': 'Failure rate is 1 in 8.',
                'rpn_type': 'occurrence',
                'value': 8
            },
            9: {
                'rpn_id': 19,
                'name': 'Extremely High',
                'description': 'Failure rate is 1 in 3.',
                'rpn_type': 'occurrence',
                'value': 9
            },
            10: {
                'rpn_id': 20,
                'name': 'Dangerously High',
                'description': 'Failure rate is > 1 in 2.',
                'rpn_type': 'occurrence',
                'value': 10
            }
        }
        assert test_toml_user_configuration.RAMSTK_RPN_SEVERITY == {
            1: {
                'rpn_id': 1,
                'name': 'None',
                'description': 'No effect.',
                'rpn_type': 'severity',
                'value': 1
            },
            2: {
                'rpn_id': 2,
                'name': 'Very Minor',
                'description': 'System operable with minimal interference.',
                'rpn_type': 'severity',
                'value': 2
            },
            3: {
                'rpn_id': 3,
                'name': 'Minor',
                'description':
                'System operable with some degradation of performance.',
                'rpn_type': 'severity',
                'value': 3
            },
            4: {
                'rpn_id': 4,
                'name': 'Very Low',
                'description':
                'System operable with significant degradation of performance.',
                'rpn_type': 'severity',
                'value': 4
            },
            5: {
                'rpn_id': 5,
                'name': 'Low',
                'description': 'System inoperable without damage.',
                'rpn_type': 'severity',
                'value': 5
            },
            6: {
                'rpn_id': 6,
                'name': 'Moderate',
                'description': 'System inoperable with minor damage.',
                'rpn_type': 'severity',
                'value': 6
            },
            7: {
                'rpn_id': 7,
                'name': 'High',
                'description': 'System inoperable with system damage.',
                'rpn_type': 'severity',
                'value': 7
            },
            8: {
                'rpn_id': 8,
                'name': 'Very High',
                'description':
                'System inoperable with destructive failure without compromising safety.',
                'rpn_type': 'severity',
                'value': 8
            },
            9: {
                'rpn_id': 9,
                'name': 'Hazardous, with warning',
                'description':
                'Failure effects safe system operation with warning.',
                'rpn_type': 'severity',
                'value': 9
            },
            10: {
                'rpn_id': 10,
                'name': 'Hazardous, without warning',
                'description':
                'Failure effects safe system operation without warning.',
                'rpn_type': 'severity',
                'value': 10
            }
        }

    def test_do_load_severity(self, test_common_dao,
                              test_toml_user_configuration):
        """_do_load_severity() should load global variables related to severity and return None."""
        assert _do_load_severity(test_common_dao,
                                 test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_SEVERITY == {
            11: ('INS', 'Insignificant', 'risk', 1),
            12: ('SLT', 'Slight', 'risk', 2),
            13: ('LOW', 'Low', 'risk', 3),
            14: ('MED', 'Medium', 'risk', 4),
            15: ('HI', 'High', 'risk', 5),
            16: ('MAJ', 'Major', 'risk', 6)
        }

    def test_do_load_user_workgroups(self, test_common_dao,
                                     test_toml_user_configuration):
        """_do_load_user_workgroups() should load global variables related to users and workgroups and return None."""
        assert _do_load_user_workgroups(test_common_dao,
                                        test_toml_user_configuration) is None
        assert test_toml_user_configuration.RAMSTK_USERS == {
            1: ('Tester', 'Johnny', 'tester.johnny@reliaqual.com',
                '+1.269.867.5309', '1')
        }
        assert test_toml_user_configuration.RAMSTK_WORKGROUPS == {
            1: ('Engineering, Design', 'workgroup'),
            2: ('Engineering, Logistics Support', 'workgroup'),
            3: ('Engineering, Maintainability', 'workgroup'),
            4: ('Engineering, Reliability', 'workgroup'),
            5: ('Engineering, Safety', 'workgroup'),
            6: ('Engineering, Software', 'workgroup')
        }

    def test_do_load_variables(self, test_common_dao,
                               test_toml_user_configuration):
        """_do_load_variables() should return None."""
        assert do_load_variables(test_common_dao,
                                 test_toml_user_configuration) is None
