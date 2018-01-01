--
-- File generated with SQLiteStudio v3.1.1 on Mon Jan 1 11:33:15 2018
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: rtk_application
DROP TABLE IF EXISTS rtk_application;

CREATE TABLE rtk_application (
    fld_application_id       INTEGER       NOT NULL,
    fld_description          VARCHAR (512),
    fld_fault_density        FLOAT,
    fld_transformation_ratio FLOAT,
    PRIMARY KEY (
        fld_application_id
    )
);

INSERT INTO rtk_application (
                                fld_application_id,
                                fld_description,
                                fld_fault_density,
                                fld_transformation_ratio
                            )
                            VALUES (
                                1,
                                'Application Description',
                                1,
                                1
                            );


-- Table: rtk_category
DROP TABLE IF EXISTS rtk_category;

CREATE TABLE rtk_category (
    fld_category_id INTEGER       NOT NULL,
    fld_name        VARCHAR (256),
    fld_description VARCHAR (512),
    fld_type        VARCHAR (256),
    fld_value       INTEGER,
    PRIMARY KEY (
        fld_category_id
    )
);

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             1,
                             'IC',
                             'Integrated Circuit',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             2,
                             'SEMI',
                             'Semiconductor',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             3,
                             'RES',
                             'Resistor',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             4,
                             'CAP',
                             'Capacitor',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             5,
                             'IND',
                             'Inductive Device',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             6,
                             'REL',
                             'Relay',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             7,
                             'SW',
                             'Switching Device',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             8,
                             'CONN',
                             'Connection',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             9,
                             'MET',
                             'Meter',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             10,
                             'MISC',
                             'Miscellaneous',
                             'hardware',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             11,
                             'INS',
                             'Insignificant',
                             'risk',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             12,
                             'SLT',
                             'Slight',
                             'risk',
                             2
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             13,
                             'LOW',
                             'Low',
                             'risk',
                             3
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             14,
                             'MED',
                             'Medium',
                             'risk',
                             4
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             15,
                             'HI',
                             'High',
                             'risk',
                             5
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             16,
                             'MAJ',
                             'Major',
                             'risk',
                             6
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             17,
                             'Batch (General)',
                             'Can be run as a normal batch job and makes no unusual hardware or input-output actions (e.g., payroll program and wind tunnel data analysis program).  Small, throwaway programs for preliminary analysis also fit in this category.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             18,
                             'Event Control',
                             'Does realtime processing of data resulting from external events. An example might be a computer program that processes telemetry data.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             19,
                             'Process Control',
                             'Receives data from an external source and issues commands to that source to control its actions based on the received data.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             20,
                             'Procedure Control',
                             'Controls other software; for example, an operating system that controls execution of time-shared and batch computer programs.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             21,
                             'Navigation',
                             'Does computation and modeling to computer information required to guide an airplane from point of origin to destination.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             22,
                             'Flight Dynamics',
                             'Uses the functions computed by navigation software and augmented by control theory to control the entire flight of an aircraft.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             23,
                             'Orbital Dynamics',
                             'Resembles navigation and flight dynamics software, but has the additional complexity required by orbital navigation, such as a more complex reference system and the inclusion of gravitational effects of other heavenly bodies.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             24,
                             'Message Processing',
                             'Handles input and output mnessages. processing the text or information contained therein.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             25,
                             'Diagnostic Software',
                             'Used to detect and isolate hardware errors in the computer in which it resides or in other hardware that can communicate with the computer.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             26,
                             'Sensor and Signal Processing',
                             'Similar to that of message processing, except that it required greater processing, analyzing, and transforming the input into a usable data processing format.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             27,
                             'Simulation',
                             'Used to simulate and environment ieseion situation. other heavradlwuaatrieo,n aonfd a icnopmutps uftreo mpr otghreasme nt o enable a more realistic or a piece of hardware.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             28,
                             'Database Management',
                             'Manages the storage and access of (typically large) groups of data. Such software can also often prepare reports in user-defined formats, based on the contents of the database.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             29,
                             'Data Acquisition',
                             'Receives information in real-time and stores it in some form suitable format for later processing, for example, software that receives data from a space probe ,and files.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             30,
                             'Data Presentation',
                             'Formats and transforms data, as necessary, for convenient and understandable displays for humans.  Typically, such displays would be for some screen presentation.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             31,
                             'Decision and Planning Aids',
                             'Uses artificial intelligence techniques to provide an expert system to evaluate data and provide additional information and consideration for decision and policy makers.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             32,
                             'Pattern and Image Processing',
                             'Used for computer image generation and processing.  Such software may analyze terrain data and generate images based on stored data.',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             33,
                             'Computer System Software',
                             'Provides services to operational computer programs (i.e., problem oriented).',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             34,
                             'Software Development Tools',
                             'Provides services to aid in the development of software (e.g., compilers, assemblers, static and dynamic analyzers).',
                             'software',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             35,
                             'HW',
                             'Hardware',
                             'incident',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             36,
                             'SW',
                             'Software',
                             'incident',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             37,
                             'PROC',
                             'Process',
                             'incident',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             38,
                             'ENGD',
                             'Engineering, Design',
                             'action',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             39,
                             'ENGR',
                             'Engineering, Reliability',
                             'action',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             40,
                             'ENGS',
                             'Engineering, Systems',
                             'action',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             41,
                             'MAN',
                             'Manufacturing',
                             'action',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             42,
                             'TEST',
                             'Test',
                             'action',
                             1
                         );

INSERT INTO rtk_category (
                             fld_category_id,
                             fld_name,
                             fld_description,
                             fld_type,
                             fld_value
                         )
                         VALUES (
                             43,
                             'VANDV',
                             'Verification & Validation',
                             'action',
                             1
                         );


-- Table: rtk_condition
DROP TABLE IF EXISTS rtk_condition;

CREATE TABLE rtk_condition (
    fld_condition_id INTEGER       NOT NULL,
    fld_description  VARCHAR (512),
    fld_type         VARCHAR (256),
    PRIMARY KEY (
        fld_condition_id
    )
);

INSERT INTO rtk_condition (
                              fld_condition_id,
                              fld_description,
                              fld_type
                          )
                          VALUES (
                              1,
                              'Condition Decription',
                              ''
                          );


-- Table: rtk_criticality
DROP TABLE IF EXISTS rtk_criticality;

CREATE TABLE rtk_criticality (
    fld_criticality_id INTEGER       NOT NULL,
    fld_name           VARCHAR (256),
    fld_description    VARCHAR (512),
    fld_category       VARCHAR (256),
    fld_value          INTEGER,
    PRIMARY KEY (
        fld_criticality_id
    )
);

INSERT INTO rtk_criticality (
                                fld_criticality_id,
                                fld_name,
                                fld_description,
                                fld_category,
                                fld_value
                            )
                            VALUES (
                                1,
                                'Criticality Name',
                                'Criticality Description',
                                '',
                                0
                            );


-- Table: rtk_distribution
DROP TABLE IF EXISTS rtk_distribution;

CREATE TABLE rtk_distribution (
    fld_distribution_id INTEGER       NOT NULL,
    fld_description     VARCHAR (512),
    fld_type            INTEGER,
    PRIMARY KEY (
        fld_distribution_id
    )
);

INSERT INTO rtk_distribution (
                                 fld_distribution_id,
                                 fld_description,
                                 fld_type
                             )
                             VALUES (
                                 1,
                                 'Distribution Description',
                                 'unknown'
                             );


-- Table: rtk_environ
DROP TABLE IF EXISTS rtk_environ;

CREATE TABLE rtk_environ (
    fld_environ_id  INTEGER       NOT NULL,
    fld_code        VARCHAR (256),
    fld_description VARCHAR (512),
    fld_type        INTEGER,
    fld_pi_e        FLOAT,
    fld_do          FLOAT,
    PRIMARY KEY (
        fld_environ_id
    )
);

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            1,
                            'GB',
                            'Ground, Benign',
                            'active',
                            1,
                            1
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            2,
                            'GF',
                            'Ground, Fixed',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            3,
                            'GM',
                            'Ground, Mobile',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            4,
                            'NS',
                            'Naval, Sheltered',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            5,
                            'NU',
                            'Naval, Unsheltered',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            6,
                            'AIC',
                            'Airborne, Inhabited, Cargo',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            7,
                            'AIF',
                            'Airborne, Inhabited, Fighter',
                            'actvie',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            8,
                            'AUC',
                            'Airborne, Uninhabited, Cargo',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            9,
                            'AUF',
                            'Airborne, Uninhabited, Fighter',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            10,
                            'ARW',
                            'Airborne, Rotary Wing',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            11,
                            'SF',
                            'Space, Flight',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            12,
                            'MF',
                            'Missile, Flight',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            13,
                            'ML',
                            'Missile, Launch',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            14,
                            'CL',
                            'Cannon, Launch',
                            'active',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            15,
                            'AIR',
                            'Airborne',
                            'dormant',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            16,
                            'GND',
                            'Ground',
                            'dormant',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            17,
                            'NVL',
                            'Naval',
                            'dormant',
                            NULL,
                            NULL
                        );

INSERT INTO rtk_environ (
                            fld_environ_id,
                            fld_code,
                            fld_description,
                            fld_type,
                            fld_pi_e,
                            fld_do
                        )
                        VALUES (
                            18,
                            'SPC',
                            'Space',
                            'dormant',
                            NULL,
                            NULL
                        );


-- Table: rtk_failure_mode
DROP TABLE IF EXISTS rtk_failure_mode;

CREATE TABLE rtk_failure_mode (
    fld_category_id    INTEGER       NOT NULL,
    fld_subcategory_id INTEGER       NOT NULL,
    fld_failuremode_id INTEGER       NOT NULL,
    fld_description    VARCHAR (512),
    fld_mode_ratio     FLOAT,
    fld_source         INTEGER,
    PRIMARY KEY (
        fld_failuremode_id
    ),
    FOREIGN KEY (
        fld_category_id
    )
    REFERENCES rtk_category (fld_category_id),
    FOREIGN KEY (
        fld_subcategory_id
    )
    REFERENCES rtk_subcategory (fld_subcategory_id) 
);

INSERT INTO rtk_failure_mode (
                                 fld_category_id,
                                 fld_subcategory_id,
                                 fld_failuremode_id,
                                 fld_description,
                                 fld_mode_ratio,
                                 fld_source
                             )
                             VALUES (
                                 9,
                                 1,
                                 1,
                                 'Failure Mode Decription',
                                 1,
                                 0
                             );


-- Table: rtk_group
DROP TABLE IF EXISTS rtk_group;

CREATE TABLE rtk_group (
    fld_group_id    INTEGER       NOT NULL,
    fld_description VARCHAR (512),
    fld_type        VARCHAR (256),
    PRIMARY KEY (
        fld_group_id
    )
);

INSERT INTO rtk_group (
                          fld_group_id,
                          fld_description,
                          fld_type
                      )
                      VALUES (
                          1,
                          'Engineering, Systems',
                          'workgroup'
                      );

INSERT INTO rtk_group (
                          fld_group_id,
                          fld_description,
                          fld_type
                      )
                      VALUES (
                          2,
                          'Engineering, Reliability',
                          'workgroup'
                      );

INSERT INTO rtk_group (
                          fld_group_id,
                          fld_description,
                          fld_type
                      )
                      VALUES (
                          3,
                          'Engineering, Design Services',
                          'workgroup'
                      );


-- Table: rtk_hazards
DROP TABLE IF EXISTS rtk_hazards;

CREATE TABLE rtk_hazards (
    fld_hazard_id   INTEGER       NOT NULL,
    fld_category    VARCHAR (512),
    fld_subcategory VARCHAR (512),
    PRIMARY KEY (
        fld_hazard_id
    )
);

INSERT INTO rtk_hazards (
                            fld_hazard_id,
                            fld_category,
                            fld_subcategory
                        )
                        VALUES (
                            1,
                            'Hazard Category',
                            'Hazard Subcategory'
                        );


-- Table: rtk_level
DROP TABLE IF EXISTS rtk_level;

CREATE TABLE rtk_level (
    fld_level_id    INTEGER       NOT NULL,
    fld_description VARCHAR (512),
    fld_type        VARCHAR (256),
    fld_value       INTEGER,
    PRIMARY KEY (
        fld_level_id
    )
);

INSERT INTO rtk_level (
                          fld_level_id,
                          fld_description,
                          fld_type,
                          fld_value
                      )
                      VALUES (
                          1,
                          'Level Description',
                          '',
                          0
                      );


-- Table: rtk_load_history
DROP TABLE IF EXISTS rtk_load_history;

CREATE TABLE rtk_load_history (
    fld_load_history_id INTEGER       NOT NULL,
    fld_description     VARCHAR (512),
    PRIMARY KEY (
        fld_load_history_id
    )
);

INSERT INTO rtk_load_history (
                                 fld_load_history_id,
                                 fld_description
                             )
                             VALUES (
                                 1,
                                 'Load History Description'
                             );


-- Table: rtk_manufacturer
DROP TABLE IF EXISTS rtk_manufacturer;

CREATE TABLE rtk_manufacturer (
    fld_manufacturer_id INTEGER       NOT NULL,
    fld_description     VARCHAR (512),
    fld_location        VARCHAR (512),
    fld_cage_code       VARCHAR (512),
    PRIMARY KEY (
        fld_manufacturer_id
    )
);

INSERT INTO rtk_manufacturer (
                                 fld_manufacturer_id,
                                 fld_description,
                                 fld_location,
                                 fld_cage_code
                             )
                             VALUES (
                                 1,
                                 'Manufacturer Description',
                                 'unknown',
                                 'CAGE Code'
                             );


-- Table: rtk_measurement
DROP TABLE IF EXISTS rtk_measurement;

CREATE TABLE rtk_measurement (
    fld_measurement_id INTEGER       NOT NULL,
    fld_description    VARCHAR (512),
    PRIMARY KEY (
        fld_measurement_id
    )
);

INSERT INTO rtk_measurement (
                                fld_measurement_id,
                                fld_description
                            )
                            VALUES (
                                1,
                                'Measurement Decription'
                            );


-- Table: rtk_method
DROP TABLE IF EXISTS rtk_method;

CREATE TABLE rtk_method (
    fld_method_id   INTEGER       NOT NULL,
    fld_name        VARCHAR (256),
    fld_description VARCHAR (512),
    fld_type        VARCHAR (256),
    PRIMARY KEY (
        fld_method_id
    )
);

INSERT INTO rtk_method (
                           fld_method_id,
                           fld_name,
                           fld_description,
                           fld_type
                       )
                       VALUES (
                           1,
                           'Method Name',
                           'Method Description',
                           'unknown'
                       );


-- Table: rtk_model
DROP TABLE IF EXISTS rtk_model;

CREATE TABLE rtk_model (
    fld_model_id    INTEGER       NOT NULL,
    fld_description VARCHAR (512),
    fld_type        INTEGER,
    PRIMARY KEY (
        fld_model_id
    )
);

INSERT INTO rtk_model (
                          fld_model_id,
                          fld_description,
                          fld_type
                      )
                      VALUES (
                          1,
                          'MIL-HDBK-217F, Part Count',
                          'rprediction'
                      );

INSERT INTO rtk_model (
                          fld_model_id,
                          fld_description,
                          fld_type
                      )
                      VALUES (
                          2,
                          'MIL-HDBK-217F, Part Stress',
                          'rprediction'
                      );

INSERT INTO rtk_model (
                          fld_model_id,
                          fld_description,
                          fld_type
                      )
                      VALUES (
                          3,
                          'NSWC-11',
                          'rprediction'
                      );


-- Table: rtk_phase
DROP TABLE IF EXISTS rtk_phase;

CREATE TABLE rtk_phase (
    fld_phase_id    INTEGER       NOT NULL,
    fld_description VARCHAR (512),
    fld_type        INTEGER,
    PRIMARY KEY (
        fld_phase_id
    )
);

INSERT INTO rtk_phase (
                          fld_phase_id,
                          fld_description,
                          fld_type
                      )
                      VALUES (
                          1,
                          'Phase Description',
                          'unknown'
                      );


-- Table: rtk_rpn
DROP TABLE IF EXISTS rtk_rpn;

CREATE TABLE rtk_rpn (
    fld_rpn_id      INTEGER       NOT NULL,
    fld_name        VARCHAR (512),
    fld_description VARCHAR (512),
    fld_type        VARCHAR (256),
    fld_value       INTEGER,
    PRIMARY KEY (
        fld_rpn_id
    )
);

INSERT INTO rtk_rpn (
                        fld_rpn_id,
                        fld_name,
                        fld_description,
                        fld_type,
                        fld_value
                    )
                    VALUES (
                        1,
                        'RPN Name',
                        'RPN Description',
                        '',
                        0
                    );


-- Table: rtk_site_info
DROP TABLE IF EXISTS rtk_site_info;

CREATE TABLE rtk_site_info (
    fld_site_id     INTEGER       NOT NULL,
    fld_product_key VARCHAR (512),
    fld_expire_on   DATE,
    PRIMARY KEY (
        fld_site_id
    )
);

INSERT INTO rtk_site_info (
                              fld_site_id,
                              fld_product_key,
                              fld_expire_on
                          )
                          VALUES (
                              1,
                              '9490059723f3a743fb961d092d3283422f4f2d13',
                              '2018-01-31'
                          );


-- Table: rtk_stakeholders
DROP TABLE IF EXISTS rtk_stakeholders;

CREATE TABLE rtk_stakeholders (
    fld_stakeholders_id INTEGER       NOT NULL,
    fld_stakeholder     VARCHAR (512),
    PRIMARY KEY (
        fld_stakeholders_id
    )
);

INSERT INTO rtk_stakeholders (
                                 fld_stakeholders_id,
                                 fld_stakeholder
                             )
                             VALUES (
                                 1,
                                 'Stakeholder'
                             );


-- Table: rtk_status
DROP TABLE IF EXISTS rtk_status;

CREATE TABLE rtk_status (
    fld_status_id   INTEGER       NOT NULL,
    fld_name        VARCHAR (256),
    fld_description VARCHAR (512),
    fld_type        VARCHAR (256),
    PRIMARY KEY (
        fld_status_id
    )
);

INSERT INTO rtk_status (
                           fld_status_id,
                           fld_name,
                           fld_description,
                           fld_type
                       )
                       VALUES (
                           1,
                           'Status Name',
                           'Status Decription',
                           ''
                       );


-- Table: rtk_subcategory
DROP TABLE IF EXISTS rtk_subcategory;

CREATE TABLE rtk_subcategory (
    fld_category_id      INTEGER      NOT NULL,
    fld_subcategory_id   INTEGER      NOT NULL,
    fld_subcategory_noun VARCHAR (64) DEFAULT NULL,
    PRIMARY KEY (
        fld_category_id,
        fld_subcategory_id
    ),
    CONSTRAINT rtk_subcategory_ibfk_1 FOREIGN KEY (
        fld_category_id
    )
    REFERENCES rtk_category (fld_category_id) ON DELETE CASCADE
                                              ON UPDATE CASCADE
);

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                1,
                                'Linear'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                2,
                                'Logic'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                3,
                                'PAL, PLA'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                4,
                                'Microprocessor, Microcontroller'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                5,
                                'Memory, ROM'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                6,
                                'Memory, EEPROM'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                7,
                                'Memory, DRAM'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                8,
                                'Memory, SRAM'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                9,
                                'GaAs'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                1,
                                10,
                                'VHSIC, VLSI'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                12,
                                'Diode, Low Frequency'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                13,
                                'Diode, High Frequency'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                14,
                                'Transistor, Low Frequency, Bipolar'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                15,
                                'Transistor, Low Frequency, Si FET'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                16,
                                'Transistor, Unijunction'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                17,
                                'Transistor, High Frequency, Low Noise, Bipolar'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                18,
                                'Transistor, High Frequency, High Power, Bipolar'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                19,
                                'Transistor, High Frequency, GaAs FET'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                20,
                                'Transistor, High Frequency, Si FET'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                21,
                                'Thyristor, SCR'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                22,
                                'Optoelectronic, Detector, Isolator, Emitter'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                23,
                                'Optoelectronic, Alphanumeric Display'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                2,
                                24,
                                'Optoelectronic, Laser Diode'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                25,
                                'Fixed, Composition (RC, RCR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                26,
                                'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                27,
                                'Fixed, Film, Power (RD)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                28,
                                'Fixed, Film, Network (RZ)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                29,
                                'Fixed, Wirewound (RB, RBR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                30,
                                'Fixed, Wirewound, Power (RW, RWR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                31,
                                'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                32,
                                'Thermistor (RTH)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                33,
                                'Variable, Wirewound (RT, RTR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                34,
                                'Variable, Wirewound, Precision (RR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                35,
                                'Variable, Wirewound, Semiprecision (RA, RK)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                36,
                                'Variable, Wirewound, Power (RP)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                37,
                                'Variable, Non-Wirewound (RJ, RJR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                38,
                                'Variable, Composition (RV)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                3,
                                39,
                                'Variable, Non-Wirewound, Film and Precision (RQ, RVC)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                40,
                                'Fixed, Paper, Bypass (CA, CP)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                41,
                                'Fixed, Feed-Through (CZ, CZR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                42,
                                'Fixed, Paper and Plastic Film (CPV, CQ, CQR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                43,
                                'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                44,
                                'Fixed, Plastic and Metallized Plastic'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                45,
                                'Fixed, Super-Metallized Plastic (CRH)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                46,
                                'Fixed, Mica (CM, CMR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                47,
                                'Fixed, Mica, Button (CB)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                48,
                                'Fixed, Glass (CY, CYR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                49,
                                'Fixed, Ceramic, General Purpose (CK, CKR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                50,
                                'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                51,
                                'Fixed, Electrolytic, Tantalum, Solid (CSR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                52,
                                'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                53,
                                'Fixed, Electrolytic, Aluminum (CU, CUR)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                54,
                                'Fixed, Electrolytic (Dry), Aluminum (CE)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                55,
                                'Variable, Ceramic (CV)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                56,
                                'Variable, Piston Type (PC)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                57,
                                'Variable, Air Trimmer (CT)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                4,
                                58,
                                'Variable and Fixed, Gas or Vacuum (CG)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                5,
                                62,
                                'Transformer'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                5,
                                63,
                                'Coil'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                6,
                                64,
                                'Mechanical'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                6,
                                65,
                                'Solid State'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                7,
                                67,
                                'Toggle or Pushbutton'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                7,
                                68,
                                'Sensitive'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                7,
                                69,
                                'Rotary'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                7,
                                70,
                                'Thumbwheel'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                7,
                                71,
                                'Circuit Breaker'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                8,
                                72,
                                'Multi-Pin'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                8,
                                73,
                                'PCB Edge'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                8,
                                74,
                                'IC Socket'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                8,
                                75,
                                'Plated Through Hole (PTH)'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                8,
                                76,
                                'Connection, Non-PTH'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                9,
                                77,
                                'Elapsed Time'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                9,
                                78,
                                'Panel'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                10,
                                80,
                                'Crystal'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                10,
                                83,
                                'Lamp'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                10,
                                82,
                                'Fuse'
                            );

INSERT INTO rtk_subcategory (
                                fld_category_id,
                                fld_subcategory_id,
                                fld_subcategory_noun
                            )
                            VALUES (
                                10,
                                81,
                                'Filter, Non-Tunable Electronic'
                            );


-- Table: rtk_type
DROP TABLE IF EXISTS rtk_type;

CREATE TABLE rtk_type (
    fld_model_id    INTEGER       NOT NULL,
    fld_code        VARCHAR (256),
    fld_description VARCHAR (512),
    fld_type        INTEGER,
    PRIMARY KEY (
        fld_model_id
    )
);

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         1,
                         'STMD',
                         'State/Mode Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         2,
                         'FUNC',
                         'Functional Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         3,
                         'PERF',
                         'Performance Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         4,
                         'EXIN',
                         'External Interface Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         5,
                         'ENVT',
                         'Environmental Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         6,
                         'RESC',
                         'Resource Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         7,
                         'PHYS',
                         'Physical Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         8,
                         'QUAL',
                         'Quality Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         9,
                         'DSGN',
                         'Design Requirement',
                         'requirement'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         10,
                         'RASS',
                         'Assessed',
                         'mtbf'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         11,
                         'RSHT',
                         'Stated, Failure Rate',
                         'mtbf'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         12,
                         'RSMT',
                         'Stated, MTBF',
                         'mtbf'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         13,
                         'RSSD',
                         'Stated, Distribution',
                         'mtbf'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         14,
                         'CSTD',
                         'Stated',
                         'cost'
                     );

INSERT INTO rtk_type (
                         fld_model_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         15,
                         'CCLC',
                         'Calculated',
                         'cost'
                     );


-- Table: rtk_unit
DROP TABLE IF EXISTS rtk_unit;

CREATE TABLE rtk_unit (
    fld_unit_id     INTEGER       NOT NULL,
    fld_code        VARCHAR (256),
    fld_description VARCHAR (512),
    fld_type        VARCHAR (256),
    PRIMARY KEY (
        fld_unit_id
    )
);

INSERT INTO rtk_unit (
                         fld_unit_id,
                         fld_code,
                         fld_description,
                         fld_type
                     )
                     VALUES (
                         1,
                         'Unit Code',
                         'Unit Description',
                         'unknown'
                     );


-- Table: rtk_user
DROP TABLE IF EXISTS rtk_user;

CREATE TABLE rtk_user (
    fld_user_id    INTEGER       NOT NULL,
    fld_user_lname VARCHAR (256),
    fld_user_fname VARCHAR (256),
    fld_user_email VARCHAR (256),
    fld_user_phone VARCHAR (256),
    fld_user_group VARCHAR (256),
    PRIMARY KEY (
        fld_user_id
    )
);

INSERT INTO rtk_user (
                         fld_user_id,
                         fld_user_lname,
                         fld_user_fname,
                         fld_user_email,
                         fld_user_phone,
                         fld_user_group
                     )
                     VALUES (
                         1,
                         'Last Name',
                         'First Name',
                         'EMail',
                         '867.5309',
                         '0'
                     );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
