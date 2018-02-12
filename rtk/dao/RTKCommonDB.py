# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCommonDB.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKCommonDB File
===============================================================================
"""

from sqlalchemy.ext.declarative import declarative_base

RTK_BASE = declarative_base()

# This file contains all the dictionaries defining the default fields for each
# of the tables in the RTK Common database.
RTK_CATEGORIES = {
    0: ('IC', 'Integrated Circuit', 'hardware', 1),
    1: ('SEMI', 'Semiconductor', 'hardware', 1),
    2: ('RES', 'Resistor', 'hardware', 1),
    3: ('CAP', 'Capacitor', 'hardware', 1),
    4: ('IND', 'Inductive Device', 'hardware', 1),
    5: ('REL', 'Relay', 'hardware', 1),
    6: ('SW', 'Switching Device', 'hardware', 1),
    7: ('CONN', 'Connection', 'hardware', 1),
    8: ('MET', 'Meter', 'hardware', 1),
    9: ('MISC', 'Miscellaneous', 'hardware', 1),
    10: ('INS', 'Insignificant', 'risk', 1),
    11: ('SLT', 'Slight', 'risk', 2),
    12: ('LOW', 'Low', 'risk', 3),
    13: ('MED', 'Medium', 'risk', 4),
    14: ('HI', 'High', 'risk', 5),
    15: ('MAJ', 'Major', 'risk', 6),
    16: ('Batch (General)',
         'Can be run as a normal batch job and makes no unusual '
         'hardware or input-output actions (e.g., payroll '
         'program and wind tunnel data analysis program).  '
         'Small, throwaway programs for preliminary analysis '
         'also fit in this category.', 'software', 1),
    17: ('Event Control', 'Does realtime processing of data resulting from '
         'external events. An example might be a computer '
         'program that processes telemetry data.', 'software', 1),
    18: ('Process Control', 'Receives data from an external source and issues '
         'commands to that source to control its actions '
         'based on the received data.', 'software', 1),
    19: ('Procedure Control',
         'Controls other software; for example, an operating '
         'system that controls execution of time-shared and '
         'batch computer programs.', 'software', 1),
    20: ('Navigation', 'Does computation and modeling to computer '
         'information required to guide an airplane from '
         'point of origin to destination.', 'software', 1),
    21: ('Flight Dynamics',
         'Uses the functions computed by navigation software '
         'and augmented by control theory to control the '
         'entire flight of an aircraft.', 'software', 1),
    22: ('Orbital Dynamics',
         'Resembles navigation and flight dynamics software, '
         'but has the additional complexity required by '
         'orbital navigation, such as a more complex '
         'reference system and the inclusion of '
         'gravitational effects of other heavenly bodies.', 'software', 1),
    23: ('Message Processing',
         'Handles input and output mnessages. processing the '
         'text or information contained therein.', 'software', 1),
    24: ('Diagnostic Software',
         'Used to detect and isolate hardware errors in the '
         'computer in which it resides or in other hardware '
         'that can communicate with the computer.', 'software', 1),
    25: ('Sensor and Signal Processing',
         'Similar to that of message processing, except that '
         'it required greater processing, analyzing, and '
         'transforming the input into a usable data '
         'processing format.', 'software', 1),
    26: ('Simulation', 'Used to simulate and environment ieseion '
         'situation. other heavradlwuaatrieo,n aonfd a '
         'icnopmutps uftreo mpr otghreasme nt o enable a '
         'more realistic or a piece of hardware.', 'software', 1),
    27: ('Database Management', 'Manages the storage and access of (typically '
         'large) groups of data. Such software can also '
         'often prepare reports in user-defined formats, '
         'based on the contents of the database.', 'software', 1),
    28: ('Data Acquisition',
         'Receives information in real-time and stores it in '
         'some form suitable format for later processing, '
         'for example, software that receives data from a '
         'space probe ,and files.', 'software', 1),
    29: ('Data Presentation', 'Formats and transforms data, as necessary, for '
         'convenient and understandable displays for '
         'humans.  Typically, such displays would be for '
         'some screen presentation.', 'software', 1),
    30: ('Decision and Planning Aids',
         'Uses artificial intelligence techniques to provide '
         'an expert system to evaluate data and provide '
         'additional information and consideration for '
         'decision and policy makers.', 'software', 1),
    31: ('Pattern and Image Processing',
         'Used for computer image generation and '
         'processing.  Such software may analyze terrain '
         'data and generate images based on stored data.', 'software', 1),
    32: ('Computer System Software',
         'Provides services to operational computer '
         'programs (i.e., problem oriented).', 'software', 1),
    33: ('Software Development Tools',
         'Provides services to aid in the development of '
         'software (e.g., compilers, assemblers, static and '
         'dynamic analyzers).', 'software', 1),
    34: ('HW', 'Hardware', 'incident', 1),
    35: ('SW', 'Software', 'incident', 1),
    36: ('PROC', 'Process', 'incident', 1),
    37: ('ENGD', 'Engineering, Design', 'action', 1),
    38: ('ENGR', 'Engineering, Reliability', 'action', 1),
    39: ('ENGS', 'Engineering, Systems', 'action', 1),
    40: ('MAN', 'Manufacturing', 'action', 1),
    41: ('TEST', 'Test', 'action', 1),
    42: ('VANDV', 'Verification & Validation', 'action', 1)
}

RTK_ENVIRONS = {
    0: ('GB', 'Ground, Benign', 'active', 0.5, 1.0),
    1: ('GF', 'Ground, Fixed', 'active', 2.0, 1.0),
    2: ('GM', 'Ground, Mobile', 'active', 4.0, 1.0),
    3: ('NS', 'Naval, Sheltered', 'active', 4.0, 1.0),
    4: ('NU', 'Naval, Unsheltered', 'active', 6.0, 1.0),
    5: ('AIC', 'Airborne, Inhabited, Cargo', 'active', 4.0, 1.0),
    6: ('AIF', 'Airborne, Inhabited, Fighter', 'active', 5.0, 1.0),
    7: ('AUC', 'Airborne, Uninhabited, Cargo', 'active', 5.0, 1.0),
    8: ('AUF', 'Airborne, Uninhabited, Fighter', 'active', 8.0, 1.0),
    9: ('ARW', 'Airborne, Rotary Wing', 'active', 8.0, 1.0),
    10: ('SF', 'Space, Flight', 'active', 0.5, 1.0),
    11: ('MF', 'Missile, Flight', 'active', 5.0, 1.0),
    12: ('ML', 'Missile, Launch', 'active', 12.0, 1.0),
    13: ('GND', 'Ground', 'dormant', 1.0, 1.0),
    14: ('NVL', 'Naval', 'dormant', 1.0, 1.0),
    15: ('AIR', 'Airborne', 'dormant', 1.0, 1.0),
    16: ('ORG', 'Organic', 'development', 1.0, 0.76),
    17: ('SD', 'Semi-Detached', 'development', 1.0, 1.0),
    18: ('EMB', 'Embedded', 'development', 1.0, 1.3)
}

RTK_GROUPS = {
    0: ('Engineering, Design', 'workgroup'),
    1: ('Engineering, Logistics Support', 'workgroup'),
    2: ('Engineering, Maintainability', 'workgroup'),
    3: ('Engineering, Reliability', 'workgroup'),
    4: ('Engineering, Safety', 'workgroup'),
    5: ('Engineering, Software', 'workgroup'),
    6: ('Reliability', 'affinity'),
    7: ('Durability', 'affinity'),
    8: ('Cost', 'affinity')
}

RTK_LEVELS = {
    0: ('Software System', 'software', 0),
    1: ('Software Module', 'software', 0),
    2: ('Software Unit', 'software', 0),
    3: ('Level A - Frequent', 'probability', 5),
    4: ('Level B - Reasonably Probable', 'probability', 4),
    5: ('Level C - Occasional', 'probability', 3),
    6: ('Level D - Remote', 'probability', 2),
    7: ('Level E - Extremely Unlikely', 'probability', 1)
}

RTK_METHODS = {
    0: ('Code Reviews',
        'Code review is a systematic examination (often known as '
        'peer review) of computer source code.', 'test'),
    1: ('Error/Anomaly Detection', '', 'test'),
    2: ('Structure Analysis', '', 'test'),
    3: ('Random Testing', '', 'test'),
    4: ('Functional Testing', '', 'test'),
    5: ('Branch Testing', '', 'test'),
    6: ('Code Reviews', '', 'detection'),
    7: ('Error/Anomaly Detection', '', 'detection'),
    8: ('Structure Analysis', '', 'detection'),
    9: ('Random Testing', '', 'detection'),
    10: ('Functional Testing', '', 'detection'),
    11: ('Branch Testing', '', 'detection')
}

RTK_MODELS = {
    0: ('Equal Apportionment', 'allocation'),
    1: ('ARINC Apportionment', 'allocation'),
    2: ('AGREE Apportionment', 'allocation'),
    3: ('Feasibility of Objectives', 'allocation'),
    4: ('Repairable Systems Apportionment', 'allocation'),
    5: ('MIL-HDBK-217F Parts Count', 'rprediction'),
    6: ('MIL-HDBK-217F Parts Stress', 'rprediction'),
    7: ('NSWC-11', 'rprediction')
}

RTK_PHASES = {
    0: ('Concept/Planning (PCP)', 'development'),
    1: ('Requirements Analysis (SRA)', 'development'),
    2: ('Preliminary Design Review (PDR)', 'development'),
    3: ('Critical Design Review (CDR)', 'development'),
    4: ('Test Readiness Review (TRR)', 'development'),
    5: ('Released', 'development'),
    6: ('Design', 'lifecycle'),
    7: ('Reliability Growth', 'lifecycle'),
    8: ('Reliability Qualification', 'lifecycle'),
    9: ('Production', 'lifecycle'),
    10: ('Storage', 'lifecycle'),
    11: ('Operation', 'lifecycle'),
    12: ('Disposal', 'lifecycle')
}

RTK_RPNS = {
    0: ('None', 'No effect.', 'severity', 1),
    1: ('Very Minor', 'System operable with minimal interference.', 'severity',
        2),
    2: ('Minor', 'System operable with some degradation of '
        'performance.', 'severity', 3),
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

RTK_STATUSES = {
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

RTK_TYPES = {
    0: ('CALC', 'Calculated', 'cost'),
    1: ('DEF', 'Defined', 'cost'),
    2: ('ASS', 'Assessed', 'mtbf'),
    3: ('DHR', 'Defined, Hazard Rate', 'mtbf'),
    4: ('DMT', 'Defined, MTBF', 'mtbf'),
    5: ('ASS', 'Assessed', 'mttr'),
    6: ('DEF', 'Defined', 'mttr'),
    7: ('PLN', 'Planning', 'incident'),
    8: ('CON', 'Concept', 'incident'),
    9: ('RQMT', 'Requirement', 'incident'),
    10: ('DES', 'Design', 'incident'),
    11: ('COD', 'Coding', 'incident'),
    12: ('DB', 'Database', 'incident'),
    13: ('TI', 'Test Information', 'incident'),
    14: ('MAN', 'Manuals', 'incident'),
    15: ('OTH', 'Other', 'incident'),
    16: ('FUN', 'Functional', 'requirement'),
    17: ('PRF', 'Performance', 'requirement'),
    18: ('REG', 'Regulatory', 'requirement'),
    19: ('REL', 'Reliability', 'requirement'),
    20: ('SAF', 'Safety', 'requirement'),
    21: ('SVC', 'Serviceability', 'requirement'),
    22: ('USE', 'Useability', 'requirement'),
    23: ('DOE', 'Manufacturing Test, DOE', 'validation'),
    24: ('ESS', 'Manufacturing Test, ESS', 'validation'),
    25: ('HSS', 'Manufacturing Test, HASS', 'validation'),
    26: ('PRT', 'Manufacturing Test, PRAT', 'validation'),
    27: ('RAA', 'Reliability, Assessment', 'validation'),
    28: ('RDA', 'Reliability, Durability Analysis', 'validation'),
    29: ('RFF', 'Reliability, FFMEA', 'validation'),
    30: ('RDF', 'Reliability, (D)FMEA', 'validation'),
    31: ('RCA', 'Reliability, Root Cause Analysis', 'validation'),
    32: ('RSA', 'Reliability, Survival Analysis', 'validation'),
    33: ('ALT', 'Reliability Test, ALT', 'validation'),
    34: ('RDT', 'Reliability Test, Demonstration', 'validation'),
    35: ('HLT', 'Reliability Test, HALT', 'validation'),
    36: ('RGT', 'Reliability Test, Growth', 'validation'),
    37: ('FTA', 'Safety, Fault Tree Analysis', 'validation'),
    38: ('PHA', 'Safety, Hazards Analysis', 'validation'),
    39: ('EMA', 'System Engineering, Electromagnetic Analysis', 'validation'),
    40: ('FEA', 'System Engineering, FEA', 'validation'),
    41: ('2DM', 'System Engineering, 2D Model', 'validation'),
    42: ('3DM', 'System Engineering, 3D Model', 'validation'),
    43: ('SRD', 'System Engineering, Robust Design', 'validation'),
    44: ('SCA', 'System Engineering, Sneak Circuit Analysis', 'validation'),
    45: ('THA', 'System Engineering, Thermal Analysis', 'validation'),
    46: ('TOL', 'System Engineering, Tolerance Analysis', 'validation'),
    47: ('WCA', 'System Engineering, Worst Case Analysis', 'validation')
}

RTK_APPLICATIONS = {
    0: ('Airborne', 0.0128, 6.28),
    1: ('Strategic', 0.0092, 1.2),
    2: ('Tactical', 0.0078, 13.8),
    3: ('Process Control', 0.0018, 3.8),
    4: ('Production Center', 0.0085, 23.0),
    5: ('Developmental', 0.0123, 132.6)
}

RTK_CRITICALITIES = {
    0: ('Catastrophic', 'Could result in death, permanent total disability, '
        'loss exceeding $1M, or irreversible severe '
        'environmental damage that violates law or '
        'regulation.', 'I', 4),
    1: ('Critical', 'Could result in permanent partial disability, '
        'injuries or occupational illness that may result in '
        'hospitalization of at least three personnel, loss '
        'exceeding $200K but less than $1M, or reversible '
        'environmental damage causing a violation of law or '
        'regulation.', 'II', 3),
    2: ('Marginal', 'Could result in injury or occupational illness '
        'resulting in one or more lost work days(s), loss '
        'exceeding $10K but less than $200K, or mitigatible '
        'environmental damage without violation of law or '
        'regulation where restoration activities can be '
        'accomplished.', 'III', 2),
    3: ('Negligble', 'Could result in injury or illness not resulting in a '
        'lost work day, loss exceeding $2K but less than '
        '$10K, or minimal environmental damage not violating '
        'law or regulation.', 'IV', 1)
}

RTK_DISTRIBUTIONS = {
    0: ('Constant Probability', 'statistical'),
    1: ('Exponential', 'statistical'),
    2: ('Gaussian', 'statistical'),
    3: ('LogNormal', 'statistical'),
    4: ('Uniform', 'statistical'),
    5: ('Weibull', 'statistical')
}

RTK_HAZARDS = {
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
    60: ('Ergonomics', 'Nonexistent/Inadequate '
         'Kill'
         ' Switches'),
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

RTK_MANUFACTURERS = {
    0: ('Sprague', 'New Hampshire', '13606'),
    1: ('Xilinx', '', ''),
    2: ('National Semiconductor', 'California', '27014')
}

RTK_UNITS = {
    0: ('lbf', 'Pounds Force', 'measurement'),
    1: ('hrs', 'hours', 'measurement'),
    2: ('N', 'Newtons', 'measurement'),
    3: ('mins', 'minutes', 'measurement'),
    4: ('secs', 'seconds', 'measurement'),
    5: ('g', 'grams', 'measurement'),
    6: ('oz', 'ounces', 'measurement'),
    7: ('A', 'Amperes', 'measurement'),
    8: ('V', 'Volts', 'measurement')
}

RTK_STAKEHOLDERS = {0: ('Customer', )}

RTK_CONDITIONS = {
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
    41: ('Shock, Mechnical', 'environmental'),
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

RTK_MEASUREMENTS = {
    0: ('Contamination, Concentration', ),
    1: ('Contamination, Particle Size', ),
    2: ('Dynamic Load', ),
    3: ('Load, Maximum', ),
    4: ('Load, Minimum-Maximum', ),
    5: ('Number of Braking Events', ),
    6: ('Number of Cycles', ),
    7: ('Number of Overload Events', ),
    8: ('Number of Shifts', ),
    9: ('Operating Time at Condition', ),
    10: ('Pressure, Average', ),
    11: ('Pressure, Differential', ),
    12: ('Pressure, Peak', ),
    13: ('RPM', ),
    14: ('Temperature, Ambient', ),
    15: ('Temperature, Average', ),
    16: ('Temperature, Differential', ),
    17: ('Temperature, Peak', ),
    18: ('Temperature = f(Time)', ),
    19: ('Torque', )
}

RTK_HISTORIES = {
    0: ('Cycle Counts', ),
    1: ('Histogram', ),
    2: ('Histogram, Bivariate', ),
    3: ('Level Crossing', ),
    4: ('Rain Flow Count', ),
    5: ('Time at Level', ),
    6: ('Time at Load', ),
    7: ('Time at Maximum', ),
    8: ('Time at Minimum', )
}
