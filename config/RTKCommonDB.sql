PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

--
-- Active environments.
--
CREATE TABLE "tbl_active_environs" (
  "fld_subcategory_id" INTEGER NOT NULL,                            -- Component sub-category ID.
  "fld_calculation_model_id" INTEGER NOT NULL,                      -- Calculation model ID.
  "fld_active_environ_id" INTEGER NOT NULL,                         -- Active environment ID.
  "fld_active_environ_code" VARCHAR(4) NOT NULL,                    -- Active environment code.
  "fld_active_environ_noun" VARCHAR(64) NOT NULL,                   -- Active environment name.
  "fld_pi_e" FLOAT NOT NULL DEFAULT (1),                            -- Environmental adjustment factor for reliability model.
  PRIMARY KEY ("fld_subcategory_id","fld_calculation_model_id","fld_active_environ_id"),
  CONSTRAINT "tbl_active_environs_ibfk_1" FOREIGN KEY ("fld_calculation_model_id") REFERENCES "tbl_calculation_model" ("fld_model_id") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "tbl_active_environs_ibfk_2" FOREIGN KEY ("fld_subcategory_id") REFERENCES "tbl_subcategory" ("fld_subcategory_id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "tbl_active_environs" VALUES(1,1,1,'GB','Ground, Benign',0.5);
INSERT INTO "tbl_active_environs" VALUES(1,1,2,'GF','Ground, Fixed',2.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,3,'GM','Ground, Mobile',4.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,4,'NS','Naval, Sheltered',4.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,5,'NU','Naval, Unsheltered',6.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,6,'AIC','Airborne, Inhabited, Cargo',4.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,7,'AIF','Airborne, Inhabited, Fighter',5.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,8,'AUC','Airborne, Uninhabited, Cargo',5.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,9,'AUF','Airborne, Uninhabited, Fighter',8.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,10,'ARW','Airborne, Rotary Wing',8.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,11,'SF','Space, Flight',0.5);
INSERT INTO "tbl_active_environs" VALUES(1,1,12,'MF','Missile, Flight',5.0);
INSERT INTO "tbl_active_environs" VALUES(1,1,13,'ML','Missile, Launch',12.0);

--
-- Dormant environments.
--
CREATE TABLE "tbl_dormant_environs" (
  "fld_model_id" INTEGER NOT NULL,                                  -- Reliability model ID.
  "fld_dormant_environ_id" INTEGER NOT NULL,                        -- ID of the dormant environment.
  "fld_dormant_environ_noun" VARCHAR(64) NOT NULL,                  -- Name of the dormant environment.
  PRIMARY KEY ("fld_model_id","fld_dormant_environ_id"),
  CONSTRAINT "tbl_dormant_environs_ibfk_1" FOREIGN KEY ("fld_model_id") REFERENCES "tbl_calculation_model" ("fld_model_id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "tbl_dormant_environs" VALUES(1,1,'Ground');
INSERT INTO "tbl_dormant_environs" VALUES(1,2,'Naval');
INSERT INTO "tbl_dormant_environs" VALUES(1,3,'Airborne');

--
-- Available reliability allocation models.
--
CREATE TABLE "tbl_allocation_models" (
  "fld_allocation_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- Allocation model ID.
  "fld_allocation_noun" VARCHAR(64) NOT NULL                        -- Allocation model name.
);
INSERT INTO "tbl_allocation_models" VALUES(1,'Equal Apportionment');
INSERT INTO "tbl_allocation_models" VALUES(2,'AGREE Apportionment');
INSERT INTO "tbl_allocation_models" VALUES(3,'ARINC Apportionment');
INSERT INTO "tbl_allocation_models" VALUES(4,'Feasibility of Objectives');
INSERT INTO "tbl_allocation_models" VALUES(5,'Repairable Systems Apportionment');

--
-- Available reliability calculation models.
--
CREATE TABLE "tbl_calculation_model" (
  "fld_model_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,        -- Reliability calculation model ID.
  "fld_model_noun" VARCHAR(50) DEFAULT NULL                         -- Reliability calculation model name.
);
INSERT INTO "tbl_calculation_model" VALUES(1,'MIL-HDBK-217F Stress');
INSERT INTO "tbl_calculation_model" VALUES(2,'MIL-HDBK-217F Parts Count');
INSERT INTO "tbl_calculation_model" VALUES(3,'MIL-HDBK-217FN1 Stress');
INSERT INTO "tbl_calculation_model" VALUES(4,'MIL-HDBK-217FN1 Parts Count');
INSERT INTO "tbl_calculation_model" VALUES(5,'MIL-HDBK-217FN2 Stress');
INSERT INTO "tbl_calculation_model" VALUES(6,'MIL-HDBK-217FN2 Parts Count');
INSERT INTO "tbl_calculation_model" VALUES(7,'Mechanical');

--
-- Component categories.
--
CREATE TABLE "tbl_category" (
  "fld_category_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,     -- Component category ID.
  "fld_category_noun" VARCHAR(64) DEFAULT NULL                      -- Component category name.
);
INSERT INTO "tbl_category" VALUES(1,'Integrated Circuit');
INSERT INTO "tbl_category" VALUES(2,'Semiconductor');
INSERT INTO "tbl_category" VALUES(3,'Resistor');
INSERT INTO "tbl_category" VALUES(4,'Capacitor');
INSERT INTO "tbl_category" VALUES(5,'Inductive Device');
INSERT INTO "tbl_category" VALUES(6,'Relay');
INSERT INTO "tbl_category" VALUES(7,'Switching Device');
INSERT INTO "tbl_category" VALUES(8,'Connection');
INSERT INTO "tbl_category" VALUES(9,'Meter');
INSERT INTO "tbl_category" VALUES(10,'Miscellaneous');

--
-- Component sub-categories.
--
CREATE TABLE "tbl_subcategory" (
  "fld_category_id" INTEGER NOT NULL,
  "fld_subcategory_id" INTEGER NOT NULL,
  "fld_subcategory_noun" VARCHAR(64) DEFAULT NULL,
  PRIMARY KEY ("fld_category_id","fld_subcategory_id"),
  CONSTRAINT "tbl_subcategory_ibfk_1" FOREIGN KEY ("fld_category_id") REFERENCES "tbl_category" ("fld_category_id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "tbl_subcategory" VALUES(1,1,'Linear');
INSERT INTO "tbl_subcategory" VALUES(1,2,'Logic');
INSERT INTO "tbl_subcategory" VALUES(1,3,'PAL, PLA');
INSERT INTO "tbl_subcategory" VALUES(1,4,'Microprocessor, Microcontroller');
INSERT INTO "tbl_subcategory" VALUES(1,5,'Memory, ROM');
INSERT INTO "tbl_subcategory" VALUES(1,6,'Memory, EEPROM');
INSERT INTO "tbl_subcategory" VALUES(1,7,'Memory, DRAM');
INSERT INTO "tbl_subcategory" VALUES(1,8,'Memory, SRAM');
INSERT INTO "tbl_subcategory" VALUES(1,9,'GaAs');
INSERT INTO "tbl_subcategory" VALUES(1,10,'VHSIC, VLSI');
INSERT INTO "tbl_subcategory" VALUES(2,12,'Diode, Low Frequency');
INSERT INTO "tbl_subcategory" VALUES(2,13,'Diode, High Frequency');
INSERT INTO "tbl_subcategory" VALUES(2,14,'Transistor, Low Frequency, Bipolar');
INSERT INTO "tbl_subcategory" VALUES(2,15,'Transistor, Low Frequency, Si FET');
INSERT INTO "tbl_subcategory" VALUES(2,16,'Transistor, Unijunction');
INSERT INTO "tbl_subcategory" VALUES(2,17,'Transistor, High Frequency, Low Noise, Bipolar');
INSERT INTO "tbl_subcategory" VALUES(2,18,'Transistor, High Frequency, High Power, Bipolar');
INSERT INTO "tbl_subcategory" VALUES(2,19,'Transistor, High Frequency, GaAs FET');
INSERT INTO "tbl_subcategory" VALUES(2,20,'Transistor, High Frequency, Si FET');
INSERT INTO "tbl_subcategory" VALUES(2,21,'Thyristor, SCR');
INSERT INTO "tbl_subcategory" VALUES(2,22,'Optoelectronic, Detector, Isolator, Emitter');
INSERT INTO "tbl_subcategory" VALUES(2,23,'Optoelectronic, Alphanumeric Display');
INSERT INTO "tbl_subcategory" VALUES(2,24,'Optoelectronic, Laser Diode');
INSERT INTO "tbl_subcategory" VALUES(3,25,'Fixed, Composition (RC, RCR)');
INSERT INTO "tbl_subcategory" VALUES(3,26,'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)');
INSERT INTO "tbl_subcategory" VALUES(3,27,'Fixed, Film, Power (RD)');
INSERT INTO "tbl_subcategory" VALUES(3,28,'Fixed, Film, Network (RZ)');
INSERT INTO "tbl_subcategory" VALUES(3,29,'Fixed, Wirewound (RB, RBR)');
INSERT INTO "tbl_subcategory" VALUES(3,30,'Fixed, Wirewound, Power (RW, RWR)');
INSERT INTO "tbl_subcategory" VALUES(3,31,'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)');
INSERT INTO "tbl_subcategory" VALUES(3,32,'Thermistor (RTH)');
INSERT INTO "tbl_subcategory" VALUES(3,33,'Variable, Wirewound (RT, RTR)');
INSERT INTO "tbl_subcategory" VALUES(3,34,'Variable, Wirewound, Precision (RR)');
INSERT INTO "tbl_subcategory" VALUES(3,35,'Variable, Wirewound, Semiprecision (RA, RK)');
INSERT INTO "tbl_subcategory" VALUES(3,36,'Variable, Wirewound, Power (RP)');
INSERT INTO "tbl_subcategory" VALUES(3,37,'Variable, Non-Wirewound (RJ, RJR)');
INSERT INTO "tbl_subcategory" VALUES(3,38,'Variable, Composition (RV)');
INSERT INTO "tbl_subcategory" VALUES(3,39,'Variable, Non-Wirewound, Film and Precision (RQ, RVC)');
INSERT INTO "tbl_subcategory" VALUES(4,40,'Fixed, Paper, Bypass (CA, CP)');
INSERT INTO "tbl_subcategory" VALUES(4,41,'Fixed, Feed-Through (CZ, CZR)');
INSERT INTO "tbl_subcategory" VALUES(4,42,'Fixed, Paper and Plastic Film (CPV, CQ, CQR)');
INSERT INTO "tbl_subcategory" VALUES(4,43,'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)');
INSERT INTO "tbl_subcategory" VALUES(4,44,'Fixed, Plastic and Metallized Plastic');
INSERT INTO "tbl_subcategory" VALUES(4,45,'Fixed, Super-Metallized Plastic (CRH)');
INSERT INTO "tbl_subcategory" VALUES(4,46,'Fixed, Mica (CM, CMR)');
INSERT INTO "tbl_subcategory" VALUES(4,47,'Fixed, Mica, Button (CB)');
INSERT INTO "tbl_subcategory" VALUES(4,48,'Fixed, Glass (CY, CYR)');
INSERT INTO "tbl_subcategory" VALUES(4,49,'Fixed, Ceramic, General Purpose (CK, CKR)');
INSERT INTO "tbl_subcategory" VALUES(4,50,'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)');
INSERT INTO "tbl_subcategory" VALUES(4,51,'Fixed, Electrolytic, Tantalum, Solid (CSR)');
INSERT INTO "tbl_subcategory" VALUES(4,52,'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)');
INSERT INTO "tbl_subcategory" VALUES(4,53,'Fixed, Electrolytic, Aluminum (CU, CUR)');
INSERT INTO "tbl_subcategory" VALUES(4,54,'Fixed, Electrolytic (Dry), Aluminum (CE)');
INSERT INTO "tbl_subcategory" VALUES(4,55,'Variable, Ceramic (CV)');
INSERT INTO "tbl_subcategory" VALUES(4,56,'Variable, Piston Type (PC)');
INSERT INTO "tbl_subcategory" VALUES(4,57,'Variable, Air Trimmer (CT)');
INSERT INTO "tbl_subcategory" VALUES(4,58,'Variable and Fixed, Gas or Vacuum (CG)');
INSERT INTO "tbl_subcategory" VALUES(5,62,'Transformer');
INSERT INTO "tbl_subcategory" VALUES(5,63,'Coil');
INSERT INTO "tbl_subcategory" VALUES(6,64,'Mechanical');
INSERT INTO "tbl_subcategory" VALUES(6,65,'Solid State');
INSERT INTO "tbl_subcategory" VALUES(7,67,'Toggle or Pushbutton');
INSERT INTO "tbl_subcategory" VALUES(7,68,'Sensitive');
INSERT INTO "tbl_subcategory" VALUES(7,69,'Rotary');
INSERT INTO "tbl_subcategory" VALUES(7,70,'Thumbwheel');
INSERT INTO "tbl_subcategory" VALUES(7,71,'Circuit Breaker');
INSERT INTO "tbl_subcategory" VALUES(8,72,'Multi-Pin');
INSERT INTO "tbl_subcategory" VALUES(8,73,'PCB Edge');
INSERT INTO "tbl_subcategory" VALUES(8,74,'IC Socket');
INSERT INTO "tbl_subcategory" VALUES(8,75,'Plated Through Hole (PTH)');
INSERT INTO "tbl_subcategory" VALUES(8,76,'Connection, Non-PTH');
INSERT INTO "tbl_subcategory" VALUES(9,77,'Elapsed Time');
INSERT INTO "tbl_subcategory" VALUES(9,78,'Panel');
INSERT INTO "tbl_subcategory" VALUES(10,80,'Crystal');
INSERT INTO "tbl_subcategory" VALUES(10,81,'Filter, Non-Tunable Electronic');
INSERT INTO "tbl_subcategory" VALUES(10,82,'Fuse');
INSERT INTO "tbl_subcategory" VALUES(10,83,'Lamp');

--
-- Program cost estimation methods.
--
CREATE TABLE "tbl_cost_type" (
  "fld_cost_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Cost calculation method ID.
  "fld_cost_type_noun" VARCHAR(64) NOT NULL                         -- Cost calculation name.
);
INSERT INTO "tbl_cost_type" VALUES(1,'Calculated');
INSERT INTO "tbl_cost_type" VALUES(2,'Specified');

--
-- Software development environments.
--
CREATE TABLE "tbl_development_environment" (
  "fld_development_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  -- Software development environment ID.
  "fld_development_desc" VARCHAR(32) DEFAULT NULL,                  -- Software development environment name.
  "fld_do" FLOAT DEFAULT NULL                                       -- Software development environment adjustment factor.
);
INSERT INTO "tbl_development_environment" VALUES(0,'Organic',0.76);
INSERT INTO "tbl_development_environment" VALUES(1,'Semi-Detached',1.0);
INSERT INTO "tbl_development_environment" VALUES(2,'Embedded',1.3);

CREATE TABLE "tbl_development_phase" (
  "fld_phase_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_phase_desc" VARCHAR(64) DEFAULT NULL
);
INSERT INTO "tbl_development_phase" VALUES(0,'Concept/Planning (PCP)');
INSERT INTO "tbl_development_phase" VALUES(1,'Requirements Analysis (SRA)');
INSERT INTO "tbl_development_phase" VALUES(2,'Preliminary Design Review (PDR)');
INSERT INTO "tbl_development_phase" VALUES(3,'Critical Design Review (CDR)');
INSERT INTO "tbl_development_phase" VALUES(4,'Test Readiness Review (TRR)');
INSERT INTO "tbl_development_phase" VALUES(5,'Released');

--
-- Statistical distributions.
--
CREATE TABLE "tbl_distributions" (
  "fld_distribution_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_distribution_noun" VARCHAR(64) NOT NULL
);
INSERT INTO "tbl_distributions" VALUES(1,'Constant Probability');
INSERT INTO "tbl_distributions" VALUES(2,'Exponential');
INSERT INTO "tbl_distributions" VALUES(3,'LogNormal');
INSERT INTO "tbl_distributions" VALUES(4,'Uniform');
INSERT INTO "tbl_distributions" VALUES(5,'Weibull');

CREATE TABLE "tbl_hr_type" (
  "fld_hr_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_hr_type_noun" VARCHAR(64) NOT NULL
);
INSERT INTO "tbl_hr_type" VALUES(1,'Assessed');
INSERT INTO "tbl_hr_type" VALUES(2,'Specified, Hazard Rate');
INSERT INTO "tbl_hr_type" VALUES(3,'Specified, MTBF');

CREATE TABLE "tbl_manufacturers" (
  "fld_manufacturers_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Manufacturer ID.
  "fld_manufacturers_noun" VARCHAR(128) DEFAULT '',                 -- Manufacturer name.
  "fld_location" VARCHAR(45) DEFAULT '',                            -- Manufacturer geographical location.
  "fld_cage_code" VARCHAR(45) DEFAULT ''                            -- Manufacturer C And Government Entity (CAGE) code.
);
INSERT INTO "tbl_manufacturers" VALUES(1,'Sprague','New Hampshire','13606');
INSERT INTO "tbl_manufacturers" VALUES(2,'Xilinx','','');
INSERT INTO "tbl_manufacturers" VALUES(3,'National Semiconductor','California','27014');

CREATE TABLE "tbl_measurement_units" (
  "fld_measurement_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_measurement_code" varchar(64) DEFAULT NULL
);
INSERT INTO "tbl_measurement_units" VALUES(1,'lbf');
INSERT INTO "tbl_measurement_units" VALUES(2,'hours');
INSERT INTO "tbl_measurement_units" VALUES(3,'N');
INSERT INTO "tbl_measurement_units" VALUES(4,'minutes');
INSERT INTO "tbl_measurement_units" VALUES(5,'seconds');
INSERT INTO "tbl_measurement_units" VALUES(6,'grams');
INSERT INTO "tbl_measurement_units" VALUES(7,'oz');
INSERT INTO "tbl_measurement_units" VALUES(8,'Amperes');
INSERT INTO "tbl_measurement_units" VALUES(9,'Volts');

CREATE TABLE "tbl_mttr_type" (
  "fld_mttr_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_mttr_type_noun" varchar(64) NOT NULL
);
INSERT INTO "tbl_mttr_type" VALUES(1,'Assessed');
INSERT INTO "tbl_mttr_type" VALUES(2,'Specified');

CREATE TABLE "tbl_risk_category" (
  "fld_category_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_category_noun" VARCHAR(64) NOT NULL,
  "fld_category_value" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_risk_category" VALUES(0,'Insignificant',1);
INSERT INTO "tbl_risk_category" VALUES(1,'Slight',2);
INSERT INTO "tbl_risk_category" VALUES(2,'Low',3);
INSERT INTO "tbl_risk_category" VALUES(3,'Medium',4);
INSERT INTO "tbl_risk_category" VALUES(4,'High',5);
INSERT INTO "tbl_risk_category" VALUES(5,'Major',6);

CREATE TABLE "tbl_software_application" (
  "fld_application_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_application_desc" VARCHAR(32) DEFAULT NULL,
  "fld_fault_density" FLOAT DEFAULT NULL,
  "fld_transformation_ratio" FLOAT DEFAULT NULL
);
INSERT INTO "tbl_software_application" VALUES(0,'Airborne',0.0128,6.28);
INSERT INTO "tbl_software_application" VALUES(1,'Strategic',0.0092,1.2);
INSERT INTO "tbl_software_application" VALUES(2,'Tactical',0.0078,13.8);
INSERT INTO "tbl_software_application" VALUES(3,'Process Control',0.0018,3.8);
INSERT INTO "tbl_software_application" VALUES(4,'Production Center',0.0085,23.0);
INSERT INTO "tbl_software_application" VALUES(5,'Developmental',0.0123,132.6);

CREATE TABLE "tbl_software_level" (
  "fld_level_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_level_desc" VARCHAR(64) DEFAULT NULL
);
INSERT INTO "tbl_software_level" VALUES(0,'Software System');
INSERT INTO "tbl_software_level" VALUES(1,'Software Module');
INSERT INTO "tbl_software_level" VALUES(2,'Software Unit');

--
-- Software application categories.
--
CREATE TABLE "tbl_software_category"(
    "fld_category_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_category_name" VARCHAR(128),
    "fld_category_description" BLOB
);
INSERT INTO "tbl_software_category" VALUES(0,'Batch (General)','Can be run as a normal batch job and makes no unusual hardware or input-output actions (e.g., payroll program and wind tunnel data analysis program). Small, throwaway programs for preliminary analysis also fit in this category.');
INSERT INTO "tbl_software_category" VALUES(1,'Event Control','Does realtime processing of data resulting from external events. An example might be a computer program that processes telemetry data.');
INSERT INTO "tbl_software_category" VALUES(2,'Process Control','Receives data from an external source and issues commands to that source to control its actions based on the received data.');
INSERT INTO "tbl_software_category" VALUES(3,'Procedure Control','Controls other software; for example, an operrting system that controls execution of time-shared and batch computer programs.');
INSERT INTO "tbl_software_category" VALUES(4,'Navigation','Does computation and modeling to computer information required to guide an airplane from point of origin to destination.');
INSERT INTO "tbl_software_category" VALUES(5,'Flight Dynamics','Uses the functions computed by naviga-ion software and augmented by control theory to control the entire flight of an aircraft.');
INSERT INTO "tbl_software_category" VALUES(6,'Orbital Dynamics','Resembles navigation and flight dynamics software,-but has the additional complexity required by orbital navigation, such as a more complex reference system and the inclusion of gravitational effects of other heavenly bodies.');
INSERT INTO "tbl_software_category" VALUES(7,'Message Processing','Handles input and output mnessages. processing the text or information contained therein.');
INSERT INTO "tbl_software_category" VALUES(8,'Diagnostic Software','Used to detect and isolate hardware errors in the computer in which it resides or in other hardware that can communicate with the computer.');
INSERT INTO "tbl_software_category" VALUES(9,'Sensor and Signal Processing','Similar to that of message processing, except that it required greater processing, analyzing, and transforming the input into a usable data processing format.');
INSERT INTO "tbl_software_category" VALUES(10,'Simulation','Used to simulate and environmentmr ieseion situation. other heavradlwuaatrieo,n aonfd a icnopmutps uftreo mpr otghreasme nt o enable a more realistic or a piece of hardware.');
INSERT INTO "tbl_software_category" VALUES(11,'Database Management','Manages the storage and access of (typically large) groups of data. Such software can also often prepare reports in user-defined formats, based on the contents of the database.');
INSERT INTO "tbl_software_category" VALUES(12,'Data Acquisition','Receives information in real-time and stores ''it in some form suitable for later processing, for example, software that receives data from a space probe ,and files.');
INSERT INTO "tbl_software_category" VALUES(13,'Data Presentation','Formats and transforms data, as necessary, for convenienit and understandable displays for humans. Typically, such _displays would bi- for some screen presentation.');
INSERT INTO "tbl_software_category" VALUES(14,'Decision and Planning Aids','Uses arcial intelligence techniques to provide an expert system to evaluate data and provide additional information and consideration for decision and policy makers.');
INSERT INTO "tbl_software_category" VALUES(15,'Pattern and Image Processing','Used for computer image generation and processing. Such software may analyze terrain data and generate images based on stored data.');
INSERT INTO "tbl_software_category" VALUES(16,'Computer System Software','Provides services to operational computer programs (i.e., problem oriented).');
INSERT INTO "tbl_software_category" VALUES(17,'Software Development Tools','Provides services to aid in the development of software (e.g., compilers, assemblers, static and dynamic analyzers).');

--
-- Software test techniques.
--
CREATE TABLE "tbl_test_techniques" (
    "fld_technique_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_technique_name" VARCHAR(64),
    "fld_technique_type" INTEGER,
    "fld_technique_description" BLOB
);
INSERT INTO "tbl_test_techniques" VALUES(0,'Code Reviews',0,'Code review is a systematic examination (often known as peer review) of computer source code.');
INSERT INTO "tbl_test_techniques" VALUES(1,'Error/Anomaly Detection',0,'');
INSERT INTO "tbl_test_techniques" VALUES(2,'Structure Analysis',0,'');
INSERT INTO "tbl_test_techniques" VALUES(3,'Random Testing',0,'');
INSERT INTO "tbl_test_techniques" VALUES(4,'Functional Testing',0,'');
INSERT INTO "tbl_test_techniques" VALUES(5,'Branch Testing',0,'');

--
-- List of RTK users.
--
CREATE TABLE "tbl_users" (
    "fld_user_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_user_lname" VARCHAR(256),
    "fld_user_fname" VARCHAR(256),
    "fld_user_email" VARCHAR(256),
    "fld_user_phone" VARCHAR(256),
    "fld_user_group" VARCHAR(256)
);

CREATE TABLE "tbl_lifecycles" (
  "fld_lifecycle_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_lifecycle_name" VARCHAR(128)
);
INSERT INTO "tbl_lifecycles" VALUES(1,'Design');
INSERT INTO "tbl_lifecycles" VALUES(2,'Reliability Growth');
INSERT INTO "tbl_lifecycles" VALUES(3,'Reliability Qualification');
INSERT INTO "tbl_lifecycles" VALUES(4,'Production');
INSERT INTO "tbl_lifecycles" VALUES(5,'Storage');
INSERT INTO "tbl_lifecycles" VALUES(6,'Operation');
INSERT INTO "tbl_lifecycles" VALUES(7,'Disposal');

CREATE TABLE "tbl_incident_category" (
  "fld_incident_cat_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_incident_cat_name" VARCHAR(256)
);
INSERT INTO "tbl_incident_category" VALUES(1,'Hardware');
INSERT INTO "tbl_incident_category" VALUES(2,'Software');
INSERT INTO "tbl_incident_category" VALUES(3,'Process');

CREATE TABLE "tbl_incident_type" (
  "fld_incident_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_incident_type_name" VARCHAR(256)
);
INSERT INTO "tbl_incident_type" VALUES(1,'Planning');
INSERT INTO "tbl_incident_type" VALUES(2,'Concept');
INSERT INTO "tbl_incident_type" VALUES(3,'Requirement');
INSERT INTO "tbl_incident_type" VALUES(4,'Design');
INSERT INTO "tbl_incident_type" VALUES(5,'Coding');
INSERT INTO "tbl_incident_type" VALUES(6,'Database');
INSERT INTO "tbl_incident_type" VALUES(7,'Test Information');
INSERT INTO "tbl_incident_type" VALUES(8,'Manuals');
INSERT INTO "tbl_incident_type" VALUES(9,'Other');

CREATE TABLE "tbl_incident_relevency" (
  "fld_relevency_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_relevency_q" VARCHAR(512),
  "fld_y_status" INTEGER DEFAULT (1)
);
INSERT INTO "tbl_incident_relevency" VALUES(1,'This failure occurred on equipment or a component part that is production intent.',-1);
INSERT INTO "tbl_incident_relevency" VALUES(2,'This failure is independent of any other failure.',-1);
INSERT INTO "tbl_incident_relevency" VALUES(3,'This failure is due to design deficiencies or poor workmanship of the equipment or component part.',1);
INSERT INTO "tbl_incident_relevency" VALUES(4,'This failure is due to a defective component part.',1);
INSERT INTO "tbl_incident_relevency" VALUES(5,'This failure is due to a component part that wore out prior to it''s stipulated life.',1);
INSERT INTO "tbl_incident_relevency" VALUES(6,'This failure is the first occurrence of an intermittent failure on this equipment.',1);
INSERT INTO "tbl_incident_relevency" VALUES(7,'This failure is a malfunction (including false alarm) of the built-in test features.',1);
INSERT INTO "tbl_incident_relevency" VALUES(8,'This failure is due to misadjustment of operator controls AND the information necessary to properly adjust these controls is not available from indicators which are integral to the equipment under test.',1);
INSERT INTO "tbl_incident_relevency" VALUES(9,'This failure is dependent on another, relevent, failure.',0);
INSERT INTO "tbl_incident_relevency" VALUES(10,'This failure is directly attributable to improper test setup.',0);
INSERT INTO "tbl_incident_relevency" VALUES(11,'This failure is the failure of test insrumentation or monitoring equipment (other than built-in test equipment).',0);
INSERT INTO "tbl_incident_relevency" VALUES(12,'This failure is the result of test operator error.',0);
INSERT INTO "tbl_incident_relevency" VALUES(13,'This failure is attributable to an error in the test procedure.',0);
INSERT INTO "tbl_incident_relevency" VALUES(14,'This failure is the second or subsequent intermittent failure on this equipment.',0);
INSERT INTO "tbl_incident_relevency" VALUES(15,'This failure occurred during burn-in, troubleshooting, repair verification, or setup.',0);
INSERT INTO "tbl_incident_relevency" VALUES(16,'This failure is clearly attributable to an overstress condition in excess of the design requirements.',0);

CREATE TABLE "tbl_rpn_severity" (
    "fld_severity_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_severity_name" VARCHAR(512),
    "fld_severity_description" VARCHAR(512),
    "fld_fmeca_type" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_rpn_severity" VALUES(1,'None','No effect.',0);
INSERT INTO "tbl_rpn_severity" VALUES(2,'Very Minor','System operable with minimal interference.',0);
INSERT INTO "tbl_rpn_severity" VALUES(3,'Minor','System operable with some degradation of performance.',0);
INSERT INTO "tbl_rpn_severity" VALUES(4,'Very Low','System operable with significant degradation of performance.',0);
INSERT INTO "tbl_rpn_severity" VALUES(5,'Low','System inoperable without damage.',0);
INSERT INTO "tbl_rpn_severity" VALUES(6,'Moderate','System inoperable with minor damage.',0);
INSERT INTO "tbl_rpn_severity" VALUES(7,'High','System inoperable with system damage.',0);
INSERT INTO "tbl_rpn_severity" VALUES(8,'Very High','System inoperable with destructive failure without compromising safety.',0);
INSERT INTO "tbl_rpn_severity" VALUES(9,'Hazardous, with warning','Failure effects safe system operation with warning.',0);
INSERT INTO "tbl_rpn_severity" VALUES(10,'Hazardous, without warning','Failure effects safe system operation without warning.',0);

CREATE TABLE "tbl_rpn_occurrence" (
    "fld_occurrence_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_occurrence_name" VARCHAR(512),
    "fld_occurrence_description" VARCHAR(512),
    "fld_fmeca_type" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_rpn_occurrence" VALUES(1,'Remote','Failure rate is 1 in 1,500,000.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(2,'Very Low','Failure rate is 1 in 150,000.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(3,'Low','Failure rate is 1 in 15,000',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(4,'Moderately Low','Failure rate is 1 in 2000.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(5,'Moderate','Failure rate is 1 in 400.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(6,'Moderately High','Failure rate is 1 in 80.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(7,'High','Failure rate is 1 in 20.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(8,'Very High','Failure rate is 1 in 8.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(9,'Extremely High','Failure rate is 1 in 3.',0);
INSERT INTO "tbl_rpn_occurrence" VALUES(10,'Dangerously High','Failure rate is > 1 in 2.',0);

CREATE TABLE "tbl_rpn_detection" (
    "fld_detection_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_detection_name" VARCHAR(512),
    "fld_detection_description" VARCHAR(512),
    "fld_fmeca_type" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_rpn_detection" VALUES(1,'Almost Certain','Design control will almost certainly detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(2,'Very High','Very high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(3,'High','High chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(4,'Moderately High','Moderately high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(5,'Moderate','Moderate chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(6,'Low','Low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(7,'Very Low','Very low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(8,'Remote','Remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(9,'Very Remote','Very remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.',0);
INSERT INTO "tbl_rpn_detection" VALUES(10,'Absolute Uncertainty','Existing design controls will not or cannot detect a potential mechanism/cause and subsequent failure mode; there is no design control.',0);

CREATE TABLE "tbl_action_category" (
    "fld_action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_action_name" VARCHAR(128)
);
INSERT INTO "tbl_action_category" VALUES(0,'Engineering, Design');
INSERT INTO "tbl_action_category" VALUES(1,'Engineering, Reliability');
INSERT INTO "tbl_action_category" VALUES(2,'Engineering, Systems');
INSERT INTO "tbl_action_category" VALUES(3,'Manufacturing');
INSERT INTO "tbl_action_category" VALUES(4,'Test');
INSERT INTO "tbl_action_category" VALUES(5,'Verification & Validation');

CREATE TABLE "tbl_site_info" (
    "fld_product_key" VARCHAR(64) NOT NULL,
    "fld_expire_date" INTEGER NOT NULL DEFAULT (719163)
);
INSERT INTO "tbl_site_info" VALUES('9490059723f3a743fb961d092d3283422f4f2d13',735599);

CREATE TABLE "tbl_hazards" (
    "fld_hazard_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_category" VARCHAR(256),
    "fld_subcategory" VARCHAR(256)
);
INSERT INTO "tbl_hazards" VALUES(1,'Acceleration/Gravity','Falls');
INSERT INTO "tbl_hazards" VALUES(2,'Acceleration/Gravity','Falling Objects');
INSERT INTO "tbl_hazards" VALUES(3,'Acceleration/Gravity','Fragments/Missiles');
INSERT INTO "tbl_hazards" VALUES(4,'Acceleration/Gravity','Impacts');
INSERT INTO "tbl_hazards" VALUES(5,'Acceleration/Gravity','Inadvertent Motion');
INSERT INTO "tbl_hazards" VALUES(6,'Acceleration/Gravity','Loose Object Translation');
INSERT INTO "tbl_hazards" VALUES(7,'Acceleration/Gravity','Slip/Trip');
INSERT INTO "tbl_hazards" VALUES(8,'Acceleration/Gravity','Sloshing Liquids');
INSERT INTO "tbl_hazards" VALUES(9,'Chemical/Water Contamination','Backflow/Siphon Effect');
INSERT INTO "tbl_hazards" VALUES(10,'Chemical/Water Contamination','Leaks/Spills');
INSERT INTO "tbl_hazards" VALUES(11,'Chemical/Water Contamination','System-Cross Connection');
INSERT INTO "tbl_hazards" VALUES(12,'Chemical/Water Contamination','Vessel/Pipe/Conduit Rupture');
INSERT INTO "tbl_hazards" VALUES(13,'Common Causes','Dust/Dirt');
INSERT INTO "tbl_hazards" VALUES(14,'Common Causes','Faulty Calibration');
INSERT INTO "tbl_hazards" VALUES(15,'Common Causes','Fire');
INSERT INTO "tbl_hazards" VALUES(16,'Common Causes','Flooding');
INSERT INTO "tbl_hazards" VALUES(17,'Common Causes','Location');
INSERT INTO "tbl_hazards" VALUES(18,'Common Causes','Maintenance Error');
INSERT INTO "tbl_hazards" VALUES(19,'Common Causes','Moisture/Humidity');
INSERT INTO "tbl_hazards" VALUES(20,'Common Causes','Radiation');
INSERT INTO "tbl_hazards" VALUES(21,'Common Causes','Seismic Disturbance/Impact');
INSERT INTO "tbl_hazards" VALUES(22,'Common Causes','Single-Operator Coupling');
INSERT INTO "tbl_hazards" VALUES(23,'Common Causes','Temperature Extremes');
INSERT INTO "tbl_hazards" VALUES(24,'Common Causes','Utility Outages');
INSERT INTO "tbl_hazards" VALUES(25,'Common Causes','Vibration');
INSERT INTO "tbl_hazards" VALUES(26,'Common Causes','Wear-Out');
INSERT INTO "tbl_hazards" VALUES(27,'Common Causes','Vermin/Insects');
INSERT INTO "tbl_hazards" VALUES(28,'Contingencies','Earthquake');
INSERT INTO "tbl_hazards" VALUES(29,'Contingencies','Fire');
INSERT INTO "tbl_hazards" VALUES(30,'Contingencies','Flooding');
INSERT INTO "tbl_hazards" VALUES(31,'Contingencies','Freezing');
INSERT INTO "tbl_hazards" VALUES(32,'Contingencies','Hailstorm');
INSERT INTO "tbl_hazards" VALUES(33,'Contingencies','Shutdowns/Failures');
INSERT INTO "tbl_hazards" VALUES(34,'Contingencies','Snow/Ice Load');
INSERT INTO "tbl_hazards" VALUES(35,'Contingencies','Utility Outages');
INSERT INTO "tbl_hazards" VALUES(36,'Contingencies','Windstorm');
INSERT INTO "tbl_hazards" VALUES(37,'Control Systems','Grounding Failure');
INSERT INTO "tbl_hazards" VALUES(38,'Control Systems','Inadvertent Activation');
INSERT INTO "tbl_hazards" VALUES(39,'Control Systems','Interferences (EMI/ESI)');
INSERT INTO "tbl_hazards" VALUES(40,'Control Systems','Lightning Strike');
INSERT INTO "tbl_hazards" VALUES(41,'Control Systems','Moisture');
INSERT INTO "tbl_hazards" VALUES(42,'Control Systems','Power Outage');
INSERT INTO "tbl_hazards" VALUES(43,'Control Systems','Sneak Circuit');
INSERT INTO "tbl_hazards" VALUES(44,'Control Systems','Sneak Software');
INSERT INTO "tbl_hazards" VALUES(45,'Electrical','Burns');
INSERT INTO "tbl_hazards" VALUES(46,'Electrical','Distribution Feedback');
INSERT INTO "tbl_hazards" VALUES(47,'Electrical','Explosion (Arc)');
INSERT INTO "tbl_hazards" VALUES(48,'Electrical','Explosion (Electrostatic)');
INSERT INTO "tbl_hazards" VALUES(49,'Electrical','Overheating');
INSERT INTO "tbl_hazards" VALUES(50,'Electrical','Power Outage');
INSERT INTO "tbl_hazards" VALUES(51,'Electrical','Shock');
INSERT INTO "tbl_hazards" VALUES(52,'Ergonomics','Fatigue');
INSERT INTO "tbl_hazards" VALUES(53,'Ergonomics','Faulty/Inadequate Control/Readout Labeling');
INSERT INTO "tbl_hazards" VALUES(54,'Ergonomics','Faulty Work Station Design');
INSERT INTO "tbl_hazards" VALUES(55,'Ergonomics','Glare');
INSERT INTO "tbl_hazards" VALUES(56,'Ergonomics','Inaccessibility');
INSERT INTO "tbl_hazards" VALUES(57,'Ergonomics','Inadequate Control/Readout Differentiation');
INSERT INTO "tbl_hazards" VALUES(58,'Ergonomics','Inadequate/Improper Illumination');
INSERT INTO "tbl_hazards" VALUES(59,'Ergonomics','Inappropriate Control/Readout Location');
INSERT INTO "tbl_hazards" VALUES(60,'Ergonomics','Nonexistent/Inadequate ''Kill'' Switches');
INSERT INTO "tbl_hazards" VALUES(61,'Explosive Conditions','Explosive Dust Present');
INSERT INTO "tbl_hazards" VALUES(62,'Explosive Conditions','Explosive Gas Present');
INSERT INTO "tbl_hazards" VALUES(63,'Explosive Conditions','Explosive Liquid Present');
INSERT INTO "tbl_hazards" VALUES(64,'Explosive Conditions','Explosive Propellant Present');
INSERT INTO "tbl_hazards" VALUES(65,'Explosive Conditions','Explosive Vapor Present');
INSERT INTO "tbl_hazards" VALUES(66,'Explosive Effects','Blast Overpressure');
INSERT INTO "tbl_hazards" VALUES(67,'Explosive Effects','Mass Fire');
INSERT INTO "tbl_hazards" VALUES(68,'Explosive Effects','Seismic Ground Wave');
INSERT INTO "tbl_hazards" VALUES(69,'Explosive Effects','Thrown Fragments');
INSERT INTO "tbl_hazards" VALUES(70,'Explosive Initiator','Chemical Contamination');
INSERT INTO "tbl_hazards" VALUES(71,'Explosive Initiator','Electrostatic Discharge');
INSERT INTO "tbl_hazards" VALUES(72,'Explosive Initiator','Friction');
INSERT INTO "tbl_hazards" VALUES(73,'Explosive Initiator','Heat');
INSERT INTO "tbl_hazards" VALUES(74,'Explosive Initiator','Impact/Shock');
INSERT INTO "tbl_hazards" VALUES(75,'Explosive Initiator','Lightning');
INSERT INTO "tbl_hazards" VALUES(76,'Explosive Initiator','Vibration');
INSERT INTO "tbl_hazards" VALUES(77,'Explosive Initiator','Welding (Stray Current/Sparks)');
INSERT INTO "tbl_hazards" VALUES(78,'Fire/Flammability','Fuel');
INSERT INTO "tbl_hazards" VALUES(79,'Fire/Flammability','Ignition Source');
INSERT INTO "tbl_hazards" VALUES(80,'Fire/Flammability','Oxidizer');
INSERT INTO "tbl_hazards" VALUES(81,'Fire/Flammability','Propellant');
INSERT INTO "tbl_hazards" VALUES(82,'Human Factors','Failure to Operate');
INSERT INTO "tbl_hazards" VALUES(83,'Human Factors','Inadvertent Operation');
INSERT INTO "tbl_hazards" VALUES(84,'Human Factors','Operated Too Long');
INSERT INTO "tbl_hazards" VALUES(85,'Human Factors','Operated Too Briefly');
INSERT INTO "tbl_hazards" VALUES(86,'Human Factors','Operation Early/Late');
INSERT INTO "tbl_hazards" VALUES(87,'Human Factors','Operation Out of Sequence');
INSERT INTO "tbl_hazards" VALUES(88,'Human Factors','Operator Error');
INSERT INTO "tbl_hazards" VALUES(89,'Human Factors','Right Operation/Wrong Control');
INSERT INTO "tbl_hazards" VALUES(90,'Ionizing Radiation','Alpha');
INSERT INTO "tbl_hazards" VALUES(91,'Ionizing Radiation','Beta');
INSERT INTO "tbl_hazards" VALUES(92,'Ionizing Radiation','Gamma');
INSERT INTO "tbl_hazards" VALUES(93,'Ionizing Radiation','Neutron');
INSERT INTO "tbl_hazards" VALUES(94,'Ionizing Radiation','X-Ray');
INSERT INTO "tbl_hazards" VALUES(95,'Leaks/Spills','Asphyxiating');
INSERT INTO "tbl_hazards" VALUES(96,'Leaks/Spills','Corrosive');
INSERT INTO "tbl_hazards" VALUES(97,'Leaks/Spills','Flammable');
INSERT INTO "tbl_hazards" VALUES(98,'Leaks/Spills','Flooding');
INSERT INTO "tbl_hazards" VALUES(99,'Leaks/Spills','Gases/Vapors');
INSERT INTO "tbl_hazards" VALUES(100,'Leaks/Spills','Irritating Dusts');
INSERT INTO "tbl_hazards" VALUES(101,'Leaks/Spills','Liquids/Cryogens');
INSERT INTO "tbl_hazards" VALUES(102,'Leaks/Spills','Odorous');
INSERT INTO "tbl_hazards" VALUES(103,'Leaks/Spills','Pathogenic');
INSERT INTO "tbl_hazards" VALUES(104,'Leaks/Spills','Radiation Sources');
INSERT INTO "tbl_hazards" VALUES(105,'Leaks/Spills','Reactive');
INSERT INTO "tbl_hazards" VALUES(106,'Leaks/Spills','Run Off');
INSERT INTO "tbl_hazards" VALUES(107,'Leaks/Spills','Slippery');
INSERT INTO "tbl_hazards" VALUES(108,'Leaks/Spills','Toxic');
INSERT INTO "tbl_hazards" VALUES(109,'Leaks/Spills','Vapor Propagation');
INSERT INTO "tbl_hazards" VALUES(110,'Mechanical','Crushing Surfaces');
INSERT INTO "tbl_hazards" VALUES(111,'Mechanical','Ejected Parts/Fragments');
INSERT INTO "tbl_hazards" VALUES(112,'Mechanical','Lifting Weights');
INSERT INTO "tbl_hazards" VALUES(113,'Mechanical','Pinch Points');
INSERT INTO "tbl_hazards" VALUES(114,'Mechanical','Reciprocating Equipment');
INSERT INTO "tbl_hazards" VALUES(115,'Mechanical','Rotating Equipment');
INSERT INTO "tbl_hazards" VALUES(116,'Mechanical','Sharp Edges/Points');
INSERT INTO "tbl_hazards" VALUES(117,'Mechanical','Stability/Topping Potential');
INSERT INTO "tbl_hazards" VALUES(118,'Mission Phasing','Activation');
INSERT INTO "tbl_hazards" VALUES(119,'Mission Phasing','Calibration');
INSERT INTO "tbl_hazards" VALUES(120,'Mission Phasing','Checkout');
INSERT INTO "tbl_hazards" VALUES(121,'Mission Phasing','Coupling/Uncoupling');
INSERT INTO "tbl_hazards" VALUES(122,'Mission Phasing','Delivery');
INSERT INTO "tbl_hazards" VALUES(123,'Mission Phasing','Diagnosis/Trouble Shooting');
INSERT INTO "tbl_hazards" VALUES(124,'Mission Phasing','Emergency Start');
INSERT INTO "tbl_hazards" VALUES(125,'Mission Phasing','Installation');
INSERT INTO "tbl_hazards" VALUES(126,'Mission Phasing','Load Change');
INSERT INTO "tbl_hazards" VALUES(127,'Mission Phasing','Maintenance');
INSERT INTO "tbl_hazards" VALUES(128,'Mission Phasing','Normal Operation');
INSERT INTO "tbl_hazards" VALUES(129,'Mission Phasing','Shake Down');
INSERT INTO "tbl_hazards" VALUES(130,'Mission Phasing','Shutdown Emergency');
INSERT INTO "tbl_hazards" VALUES(131,'Mission Phasing','Standard Shutdown');
INSERT INTO "tbl_hazards" VALUES(132,'Mission Phasing','Standard Start');
INSERT INTO "tbl_hazards" VALUES(133,'Mission Phasing','Stressed Operation');
INSERT INTO "tbl_hazards" VALUES(134,'Mission Phasing','Transport');
INSERT INTO "tbl_hazards" VALUES(135,'Nonionizing Radiation','Infrared');
INSERT INTO "tbl_hazards" VALUES(136,'Nonionizing Radiation','Laser');
INSERT INTO "tbl_hazards" VALUES(137,'Nonionizing Radiation','Microwave');
INSERT INTO "tbl_hazards" VALUES(138,'Nonionizing Radiation','Ultraviolet');
INSERT INTO "tbl_hazards" VALUES(139,'Physiological','Allergens');
INSERT INTO "tbl_hazards" VALUES(140,'Physiological','Asphyxiants');
INSERT INTO "tbl_hazards" VALUES(141,'Physiological','Baropressure Extremes');
INSERT INTO "tbl_hazards" VALUES(142,'Physiological','Carcinogens');
INSERT INTO "tbl_hazards" VALUES(143,'Physiological','Cryogens');
INSERT INTO "tbl_hazards" VALUES(144,'Physiological','Fatigue');
INSERT INTO "tbl_hazards" VALUES(145,'Physiological','Irritants');
INSERT INTO "tbl_hazards" VALUES(146,'Physiological','Lifted Weights');
INSERT INTO "tbl_hazards" VALUES(147,'Physiological','Mutagens');
INSERT INTO "tbl_hazards" VALUES(148,'Physiological','Noise');
INSERT INTO "tbl_hazards" VALUES(149,'Physiological','Nuisance Dust/Odors');
INSERT INTO "tbl_hazards" VALUES(150,'Physiological','Pathogens');
INSERT INTO "tbl_hazards" VALUES(151,'Physiological','Temperature Extremes');
INSERT INTO "tbl_hazards" VALUES(152,'Physiological','Teratogens');
INSERT INTO "tbl_hazards" VALUES(153,'Physiological','Toxins');
INSERT INTO "tbl_hazards" VALUES(154,'Physiological','Vibration (Raynaud’s Syndrome)');
INSERT INTO "tbl_hazards" VALUES(155,'Pneumatic/Hydraulic','Backflow');
INSERT INTO "tbl_hazards" VALUES(156,'Pneumatic/Hydraulic','Blown Objects');
INSERT INTO "tbl_hazards" VALUES(157,'Pneumatic/Hydraulic','Crossflow');
INSERT INTO "tbl_hazards" VALUES(158,'Pneumatic/Hydraulic','Dynamic Pressure Loading');
INSERT INTO "tbl_hazards" VALUES(159,'Pneumatic/Hydraulic','Hydraulic Ram');
INSERT INTO "tbl_hazards" VALUES(160,'Pneumatic/Hydraulic','Implosion');
INSERT INTO "tbl_hazards" VALUES(161,'Pneumatic/Hydraulic','Inadvertent Release');
INSERT INTO "tbl_hazards" VALUES(162,'Pneumatic/Hydraulic','Miscalibrated Relief Device');
INSERT INTO "tbl_hazards" VALUES(163,'Pneumatic/Hydraulic','Mislocated Relief Device');
INSERT INTO "tbl_hazards" VALUES(164,'Pneumatic/Hydraulic','Overpressurization');
INSERT INTO "tbl_hazards" VALUES(165,'Pneumatic/Hydraulic','Pipe/Hose Whip');
INSERT INTO "tbl_hazards" VALUES(166,'Pneumatic/Hydraulic','Pipe/Vessel/Duct Rupture');
INSERT INTO "tbl_hazards" VALUES(167,'Pneumatic/Hydraulic','Relief Pressure Improperly Set');
INSERT INTO "tbl_hazards" VALUES(168,'Thermal','Altered Structural Properties (e.g., Embrittlement)');
INSERT INTO "tbl_hazards" VALUES(169,'Thermal','Confined Gas/Liquid');
INSERT INTO "tbl_hazards" VALUES(170,'Thermal','Elevated Flammability');
INSERT INTO "tbl_hazards" VALUES(171,'Thermal','Elevated Reactivity');
INSERT INTO "tbl_hazards" VALUES(172,'Thermal','Elevated Volatility');
INSERT INTO "tbl_hazards" VALUES(173,'Thermal','Freezing');
INSERT INTO "tbl_hazards" VALUES(174,'Thermal','Heat Source/Sink');
INSERT INTO "tbl_hazards" VALUES(175,'Thermal','Hot/Cold Surface Burns');
INSERT INTO "tbl_hazards" VALUES(176,'Thermal','Humidity/Moisture');
INSERT INTO "tbl_hazards" VALUES(177,'Thermal','Pressure Evaluation');
INSERT INTO "tbl_hazards" VALUES(178,'Unannunciated Utility Outages','Air Conditioning');
INSERT INTO "tbl_hazards" VALUES(179,'Unannunciated Utility Outages','Compressed Air/Gas');
INSERT INTO "tbl_hazards" VALUES(180,'Unannunciated Utility Outages','Electricity');
INSERT INTO "tbl_hazards" VALUES(181,'Unannunciated Utility Outages','Exhaust');
INSERT INTO "tbl_hazards" VALUES(182,'Unannunciated Utility Outages','Fuel');
INSERT INTO "tbl_hazards" VALUES(183,'Unannunciated Utility Outages','Heating/Cooling');
INSERT INTO "tbl_hazards" VALUES(184,'Unannunciated Utility Outages','Lubrication Drains/Sumps');
INSERT INTO "tbl_hazards" VALUES(185,'Unannunciated Utility Outages','Steam');
INSERT INTO "tbl_hazards" VALUES(186,'Unannunciated Utility Outages','Ventilation');

CREATE TABLE "tbl_failure_probability" (
    "fld_probability_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "fld_name" VARCHAR(256),
    "fld_value" INTEGER);
INSERT INTO "tbl_failure_probability" VALUES('Level A - Frequent', 5);
INSERT INTO "tbl_failure_probability" VALUES('Level B - Reasonably Probable', 4);
INSERT INTO "tbl_failure_probability" VALUES('Level C - Occasional', 3);
INSERT INTO "tbl_failure_probability" VALUES('Level D - Remote', 2);
INSERT INTO "tbl_failure_probability" VALUES('Level E - Extremely Unlikely', 1);

DROP TABLE IF EXISTS "tbl_severity";
CREATE TABLE "tbl_severity" (
    "fld_severity_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "fld_name" VARCHAR(256),
    "fld_category" VARCHAR(218),
    "fld_description" BLOB,
    "fld_value" INTEGER);
INSERT INTO "tbl_severity" VALUES('Catastrophic','I','Could result in death, permanent total disability, loss exceeding $1M, or irreversible severe environmental damage that violates law or regulation.', 4);
INSERT INTO "tbl_severity" VALUES('Critical','II','Could result in permanent partial disability, injuries or occupational illness that may result in hospitalization of at least three personnel, loss exceeding $200K but less than $1M, or reversible environmental damage causing a violation of law or regulation.', 3);
INSERT INTO "tbl_severity" VALUES('Marginal','III','Could result in injury or occupational illness resulting in one or more lost work days(s), loss exceeding $10K but less than $200K, or mitigatible environmental damage without violation of law or regulation where restoration activities can be accomplished.', 2);
INSERT INTO "tbl_severity" VALUES('Negligble','IV','Could result in injury or illness not resulting in a lost work day, loss exceeding $2K but less than $10K, or minimal environmental damage not violating law or regulation.', 1);

CREATE TABLE "tbl_environmental_conditions" (
    "fld_condition_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_condition_name" VARCHAR(128)
);
INSERT INTO "tbl_environmental_conditions" VALUES(0,'Abrasion');
INSERT INTO "tbl_environmental_conditions" VALUES(1,'Acceleration');
INSERT INTO "tbl_environmental_conditions" VALUES(2,'Corona');
INSERT INTO "tbl_environmental_conditions" VALUES(3,'Contamination, Chemicals');
INSERT INTO "tbl_environmental_conditions" VALUES(4,'Contamination, Dirt/Dust');
INSERT INTO "tbl_environmental_conditions" VALUES(5,'Contamination, Salt Spray');
INSERT INTO "tbl_environmental_conditions" VALUES(6,'Electrostatic Discharge');
INSERT INTO "tbl_environmental_conditions" VALUES(7,'Fungus');
INSERT INTO "tbl_environmental_conditions" VALUES(8,'Gas, Ionized');
INSERT INTO "tbl_environmental_conditions" VALUES(9,'Geomagnetics');
INSERT INTO "tbl_environmental_conditions" VALUES(10,'Humidity');
INSERT INTO "tbl_environmental_conditions" VALUES(11,'Ozone');
INSERT INTO "tbl_environmental_conditions" VALUES(12,'Pressure, Atmospheric');
INSERT INTO "tbl_environmental_conditions" VALUES(13,'Pressure');
INSERT INTO "tbl_environmental_conditions" VALUES(14,'Radiation, Alpha');
INSERT INTO "tbl_environmental_conditions" VALUES(15,'Radiation, Electromagnetic');
INSERT INTO "tbl_environmental_conditions" VALUES(16,'Radiation, Gamma');
INSERT INTO "tbl_environmental_conditions" VALUES(17,'Radiation, Neutron');
INSERT INTO "tbl_environmental_conditions" VALUES(18,'Radiation, Solar');
INSERT INTO "tbl_environmental_conditions" VALUES(19,'Shock, Mechnical');
INSERT INTO "tbl_environmental_conditions" VALUES(20,'Shock, Thermal');
INSERT INTO "tbl_environmental_conditions" VALUES(21,'Temperature');
INSERT INTO "tbl_environmental_conditions" VALUES(22,'Thermal Cycles');
INSERT INTO "tbl_environmental_conditions" VALUES(23,'Vibration, Acoustic');
INSERT INTO "tbl_environmental_conditions" VALUES(24,'Vibration, Mechanical');
INSERT INTO "tbl_environmental_conditions" VALUES(25,'Weather, Fog');
INSERT INTO "tbl_environmental_conditions" VALUES(26,'Weather, Freezing Rain');
INSERT INTO "tbl_environmental_conditions" VALUES(27,'Weather, Frost');
INSERT INTO "tbl_environmental_conditions" VALUES(28,'Weather, Hail');
INSERT INTO "tbl_environmental_conditions" VALUES(29,'Weather, Ice');
INSERT INTO "tbl_environmental_conditions" VALUES(30,'Weather, Rain');
INSERT INTO "tbl_environmental_conditions" VALUES(31,'Weather, Sleet');
INSERT INTO "tbl_environmental_conditions" VALUES(32,'Weather, Snow');
INSERT INTO "tbl_environmental_conditions" VALUES(33,'Weather, Wind');

CREATE TABLE "tbl_requirement_type" (
  "fld_requirement_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_requirement_type_desc" VARCHAR(32) DEFAULT NULL,
  "fld_requirement_type_code" VARCHAR(4) DEFAULT NULL
);
INSERT INTO "tbl_requirement_type" VALUES(1,'Functional','FUN');
INSERT INTO "tbl_requirement_type" VALUES(2,'Performance','PRF');
INSERT INTO "tbl_requirement_type" VALUES(3,'Regulatory','REG');
INSERT INTO "tbl_requirement_type" VALUES(4,'Reliability','REL');
INSERT INTO "tbl_requirement_type" VALUES(5,'Safety','SAF');
INSERT INTO "tbl_requirement_type" VALUES(6,'Serviceability','SVC');
INSERT INTO "tbl_requirement_type" VALUES(7,'Usability','USE');

CREATE TABLE "tbl_stakeholders" (
    "fld_stakeholder_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_stakeholder" VARCHAR(128)
);
INSERT INTO "tbl_stakeholders" VALUES(1,'Customer');

CREATE TABLE "tbl_status" (
  "fld_status_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_status_name" VARCHAR(256),
  "fld_status_description" BLOB
);
INSERT INTO "tbl_status" VALUES(1,'Initiated','Incident or action has been initiated.');
INSERT INTO "tbl_status" VALUES(2,'Reviewed','Incident or action has been reviewed.');
INSERT INTO "tbl_status" VALUES(3,'Analysis','Incident or action has been assigned and is being analyzed.');
INSERT INTO "tbl_status" VALUES(4,'Solution Identified','A solution to the reported problem has been identified.');
INSERT INTO "tbl_status" VALUES(5,'Solution Implemented','A solution to the reported problem has been implemented.');
INSERT INTO "tbl_status" VALUES(6,'Solution Verified','A solution to the reported problem has been verified.');
INSERT INTO "tbl_status" VALUES(7,'Ready for Approval','Incident analysis or action is ready to be approved.');
INSERT INTO "tbl_status" VALUES(8,'Approved','Incident or action has been approved.');
INSERT INTO "tbl_status" VALUES(9,'Ready for Closure','Incident or action is ready to be closed.');
INSERT INTO "tbl_status" VALUES(10,'Closed','Incident or action has been closed.');

CREATE TABLE "tbl_groups" (
    "fld_group_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  -- Identifier for the group.
    "fld_group_name" VARCHAR (256)
);
INSERT INTO "tbl_groups" VALUES(1,'Engineering, Design');
INSERT INTO "tbl_groups" VALUES(2,'Engineering, Logistics Support');
INSERT INTO "tbl_groups" VALUES(3,'Engineering, Maintainability');
INSERT INTO "tbl_groups" VALUES(4,'Engineering, Reliability');
INSERT INTO "tbl_groups" VALUES(5,'Engineering, Safety');
INSERT INTO "tbl_groups" VALUES(6,'Engineering, Software');

CREATE TABLE "tbl_validation_type" (
  "fld_validation_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_validation_type_desc" VARCHAR(128) DEFAULT NULL,
  "fld_validation_type_code" VARCHAR(16) DEFAULT NULL
);
INSERT INTO "tbl_validation_type" VALUES(1,'Manufacturing Test, DOE','DOE');
INSERT INTO "tbl_validation_type" VALUES(2,'Manufacturing Test, ESS','ESS');
INSERT INTO "tbl_validation_type" VALUES(3,'Manufacturing Test, HASS','HSS');
INSERT INTO "tbl_validation_type" VALUES(4,'Manufacturing Test, PRAT','PRT');
INSERT INTO "tbl_validation_type" VALUES(5,'Reliability, Assessment','RAA');
INSERT INTO "tbl_validation_type" VALUES(6,'Reliability, Durability Analysis','RDA');
INSERT INTO "tbl_validation_type" VALUES(7,'Reliability, FFMEA','RFF');
INSERT INTO "tbl_validation_type" VALUES(8,'Reliability, (D)FMEA','RDF');
INSERT INTO "tbl_validation_type" VALUES(9,'Reliability, Root Cause Analysis','RCA');
INSERT INTO "tbl_validation_type" VALUES(10,'Reliability, Survival Analysis','RSA');
INSERT INTO "tbl_validation_type" VALUES(11,'Reliability Test, ALT','ALT');
INSERT INTO "tbl_validation_type" VALUES(12,'Reliability Test, Demonstration','RDT');
INSERT INTO "tbl_validation_type" VALUES(13,'Reliability Test, HALT','HLT');
INSERT INTO "tbl_validation_type" VALUES(14,'Reliability Test, Growth','RGT');
INSERT INTO "tbl_validation_type" VALUES(15,'Safety, Fault Tree Analysis','FTA');
INSERT INTO "tbl_validation_type" VALUES(16,'Safety, Hazards Analysis','PHA');
INSERT INTO "tbl_validation_type" VALUES(17,'System Engineering, Electromagnetic Analysis','EMA');
INSERT INTO "tbl_validation_type" VALUES(18,'System Engineering, FEA','FEA');
INSERT INTO "tbl_validation_type" VALUES(19,'System Engineering, 2D Model','2DM');
INSERT INTO "tbl_validation_type" VALUES(20,'System Engineering, 3D Model','3DM');
INSERT INTO "tbl_validation_type" VALUES(21,'System Engineering, Robust Design','SRD');
INSERT INTO "tbl_validation_type" VALUES(22,'System Engineering, Sneak Circuit Analysis','SCA');
INSERT INTO "tbl_validation_type" VALUES(23,'System Engineering, Thermal Analysis','THA');
INSERT INTO "tbl_validation_type" VALUES(24,'System Engineering, Tolerance Analysis','TOL');
INSERT INTO "tbl_validation_type" VALUES(25,'System Engineering, Worst Case Analysis','WCA');

CREATE TABLE "tbl_gateways" (
    "fld_gateway_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "fld_gateway_name" VARCHAR(256),
    "fld_gateway_description" BLOB
);
INSERT INTO "tbl_gateways" VALUES(1,'Requirements Review','Requirements review is required before design and development can commence.');
INSERT INTO "tbl_gateways" VALUES(2,'Preliminary Design Review','Preliminary design review (PDR) is required to ensure competing concepts have been thoroughly studied and the best concept has been selected for detailed design.  No prototypes should be created or ordered until PDR has been satisfied.');
INSERT INTO "tbl_gateways" VALUES(3,'Critical Design Review','Critical design review (CDR) is required to ensure the selected concept has been thoroughly modeled and analyzed or plans have been developed and scheduled to complete modelling and analysis.');
INSERT INTO "tbl_gateways" VALUES(4,'Test Readiness Review',NULL);
INSERT INTO "tbl_gateways" VALUES(5,'Manufacturing Review',NULL);

CREATE TABLE "tbl_reviews" (
    "fld_gateway_id" INTEGER DEFAULT (1),
    "fld_concern_id" INTEGER NOT NULL,
    "fld_concern" BLOB,
    "fld_rationale" BLOB,
    "fld_action" BLOB,
    "fld_remarks" BLOB,
    "fld_parent_id" VARCHAR(16) NOT NULL DEFAULT ('-')
);
INSERT INTO "tbl_reviews" VALUES(1,1,'
Avenues of technical interchange between R & M experts and other engineering groups (e.g., Design Engineering, Systems Engineering, Test and Evaluation, etc.) have been established.
','
R & M engineering should participate at all engineering group meetings where R & M is effected. Easy avenues of technical interchange between the design groups and other groups must exist.
','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,2,'
High quality devices are being used wherever possible and procurement lead times for these devices are adequate.
','
Use established vendors with good quality track records.
','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,3,'
An up-to-date preferred parts list has been established for use by designers.
',NULL,'fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,4,'Reliability assessment procedures are in accordance with requirements.',NULL,'fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,5,'Tradeoff studies have been performed.','
Typical tradeoffs might include better cooling, parts, redundancy levels, weight, power, speed, user features, volume, complexity, life cycles costs, etc.
','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,6,'
Methods have been established to ensure that equipment operating temperatures are within rated limits in the end use environment.
',NULL,'fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,7,'
There is a clearly established derating criteria for all part types used in the design.
','
Part derating levels should be a function of system type, use environment, reliability requirements, etc.
','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,8,'
There is a failure reporting and corrective action system (FRACAS) in place.
','FRACAS should include data from inspection and testing and should emphasize corrective action. FRACAS should be started as early as possible.','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,9,'There is a failure analysis capability and will failures be subjected to a detailed analysis.
','
Criteria used to determine which failures will be analyzed should be identified.
','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,10,'
The maintainability/testability evaluation techniques and data used are clearly described.
','
Data should be used for identifying maintainability, testability and diagnostics design problems, errors and for initiating corrective action.
','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,11,'
Reliability growth testing (RGT) has been planned where the product challenges state-of-the-art, operates in a severe use environment, will be produced in large quantities, has critical performance requirements, or has design flexibility.
',NULL,'fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(1,12,'
Reliability qualification testing (RQT) been planned where the product challenges state-of-the-art, operates in a severe use environment, will be produced in large quantities, has critical performance requirements, or has design flexibility.
',NULL,'fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(2,13,'
Avenues of technical interchange between R & M experts and other engineering groups (e.g., Design Engineering, Systems Engineering, Test and Evaluation, etc.) have been established.
','
R & M engineering should participate at all engineering group meetings where R & M is effected. Easy avenues of technical interchange between the design groups and other groups must exist.','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(2,14,'
High quality devices are being used wherever possible and procurement lead times for these devices is adequate.','
Use established vendors with good quality track records.','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(2,15,'
An up-to-date preferred parts list has been established for use by designers.
','','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(2,16,'
Reliability models accurately reflect the configuration, its modes of operation, duty cycles, and implementation of fault tolerance.
','','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(2,17,'Estimates meet or exceed numerical R & M requirements.','If not, better cooling, part quality, and/or redundancy should be considered.','fld_action',NULL,'-');
INSERT INTO "tbl_reviews" VALUES(2,18,'All functional elements are included in the reliability block diagram/model.','Design drawings/diagrams should be reviewed to be sure that the reliability model/diagram agrees with the hardware.','fld_action',NULL,'3');
INSERT INTO "tbl_reviews" VALUES(2,19,'All modes of operation are considered in the reliability model.','Duty cycles, alternate paths, degraded conditions and redundant units should be defined and modeled.','fld_action',NULL,'3');
INSERT INTO "tbl_reviews" VALUES(2,22,'Reliability assessment procedures are in accordance with requirements.','','fld_action',NULL,'3');
INSERT INTO "tbl_reviews" VALUES(2,23,'The sum of the part failure rates equals the module or assembly failure intensity.','Assessments may neglect to include all the parts, producing optimistic results.  Check for solder connections, connectors, circuit boards, fittings, gaskets, etc.','fld_action',NULL,'4');

CREATE TABLE "tbl_failure_modes" (
    "fld_category_id" INTEGER NOT NULL DEFAULT(0),                  -- The component the failure mode belongs to category ID.
    "fld_subcategory_id" INTEGER NOT NULL DEFAULT(0),               -- The component the failure mode belongs to subcategory ID.
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),                      -- The failure mode ID.
    "fld_mode_description" VARCHAR(256),                            -- The description of the failure mode.
    "fld_mode_ratio" REAL,                                          -- The failure mode ratio (0.0 - 100.0).
    "fld_source" INTEGER DEFAULT(0)                                 -- The source of the failure mode information.  (1=FMD-97, 2=MIL-HDBK-338B, 3=
);
INSERT INTO "tbl_failure_modes" VALUES(1,1,1,'Improper Output',0.77,2);
INSERT INTO "tbl_failure_modes" VALUES(1,1,2,'No Output',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,2,1,'Output Stuck High',0.28,2);
INSERT INTO "tbl_failure_modes" VALUES(1,2,2,'Output Stuck Low',0.28,2);
INSERT INTO "tbl_failure_modes" VALUES(1,2,3,'Input Open',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(1,2,4,'Output Open',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(1,3,1,'Improper Output',0.77,2);
INSERT INTO "tbl_failure_modes" VALUES(1,3,2,'No Output',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,4,1,'Improper Output',0.77,2);
INSERT INTO "tbl_failure_modes" VALUES(1,4,2,'No Output',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,5,1,'Data Bit Loss',0.34,2);
INSERT INTO "tbl_failure_modes" VALUES(1,5,2,'Short',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(1,5,3,'Open',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,5,4,'Slow Transfer of Data',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(1,6,1,'Data Bit Loss',0.34,2);
INSERT INTO "tbl_failure_modes" VALUES(1,6,2,'Short',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(1,6,3,'Open',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,6,4,'Slow Transfer of Data',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(1,7,1,'Data Bit Loss',0.34,2);
INSERT INTO "tbl_failure_modes" VALUES(1,7,2,'Short',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(1,7,3,'Open',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,7,4,'Slow Transfer of Data',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(1,8,1,'Data Bit Loss',0.34,2);
INSERT INTO "tbl_failure_modes" VALUES(1,8,2,'Short',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(1,8,3,'Open',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,8,4,'Slow Transfer of Data',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(1,9,1,'Output Stuck High',0.28,2);
INSERT INTO "tbl_failure_modes" VALUES(1,9,2,'Output Stuck Low',0.28,2);
INSERT INTO "tbl_failure_modes" VALUES(1,9,3,'Input Open',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(1,9,4,'Output Open',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(1,10,1,'Improper Output',0.77,2);
INSERT INTO "tbl_failure_modes" VALUES(1,10,2,'No Output',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(1,11,1,'Open Circuit',0.51,2);
INSERT INTO "tbl_failure_modes" VALUES(1,11,2,'Degraded Output',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(1,11,3,'Short Circuit',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(1,11,4,'No Output',0.06,2);
INSERT INTO "tbl_failure_modes" VALUES(2,12,1,'Short',0.49,2);
INSERT INTO "tbl_failure_modes" VALUES(2,12,2,'Open',0.36,2);
INSERT INTO "tbl_failure_modes" VALUES(2,12,3,'Parameter Change',0.15,2);
INSERT INTO "tbl_failure_modes" VALUES(2,13,1,'Short',0.49,2);
INSERT INTO "tbl_failure_modes" VALUES(2,13,2,'Open',0.36,2);
INSERT INTO "tbl_failure_modes" VALUES(2,13,3,'Parameter Change',0.15,2);
INSERT INTO "tbl_failure_modes" VALUES(2,14,1,'Short',0.73,2);
INSERT INTO "tbl_failure_modes" VALUES(2,14,2,'Open',0.27,2);
INSERT INTO "tbl_failure_modes" VALUES(2,15,1,'Short',0.51,2);
INSERT INTO "tbl_failure_modes" VALUES(2,15,2,'Output Low',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(2,15,3,'Parameter Change',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(2,15,4,'Open',0.05,2);
INSERT INTO "tbl_failure_modes" VALUES(2,15,5,'Output High',0.05,2);
INSERT INTO "tbl_failure_modes" VALUES(2,17,1,'Short',0.73,2);
INSERT INTO "tbl_failure_modes" VALUES(2,17,2,'Open',0.27,2);
INSERT INTO "tbl_failure_modes" VALUES(2,18,1,'Short',0.73,2);
INSERT INTO "tbl_failure_modes" VALUES(2,18,2,'Open',0.27,2);
INSERT INTO "tbl_failure_modes" VALUES(2,19,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(2,19,2,'Short',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(2,19,3,'Parameter Change',0.13,2);
INSERT INTO "tbl_failure_modes" VALUES(2,20,1,'Short',0.73,2);
INSERT INTO "tbl_failure_modes" VALUES(2,20,2,'Open',0.27,2);
INSERT INTO "tbl_failure_modes" VALUES(2,21,1,'Short',0.5,2);
INSERT INTO "tbl_failure_modes" VALUES(2,21,2,'Open',0.5,2);
INSERT INTO "tbl_failure_modes" VALUES(2,22,1,'Open',0.7,2);
INSERT INTO "tbl_failure_modes" VALUES(2,22,2,'Short',0.3,2);
INSERT INTO "tbl_failure_modes" VALUES(3,25,1,'Parameter Change',0.66,2);
INSERT INTO "tbl_failure_modes" VALUES(3,25,2,'Open',0.31,2);
INSERT INTO "tbl_failure_modes" VALUES(3,25,3,'Short',0.03,2);
INSERT INTO "tbl_failure_modes" VALUES(3,26,1,'Open',0.59,2);
INSERT INTO "tbl_failure_modes" VALUES(3,26,2,'Parameter Change',0.36,2);
INSERT INTO "tbl_failure_modes" VALUES(3,26,3,'Short',0.05,2);
INSERT INTO "tbl_failure_modes" VALUES(3,27,1,'Open',0.59,2);
INSERT INTO "tbl_failure_modes" VALUES(3,27,2,'Parameter Change',0.36,2);
INSERT INTO "tbl_failure_modes" VALUES(3,27,3,'Short',0.05,2);
INSERT INTO "tbl_failure_modes" VALUES(3,28,1,'Open',0.92,2);
INSERT INTO "tbl_failure_modes" VALUES(3,28,2,'Short',0.08,2);
INSERT INTO "tbl_failure_modes" VALUES(3,29,1,'Open',0.65,2);
INSERT INTO "tbl_failure_modes" VALUES(3,29,2,'Parameter Change',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(3,29,3,'Short',0.09,2);
INSERT INTO "tbl_failure_modes" VALUES(3,30,1,'Open',0.65,2);
INSERT INTO "tbl_failure_modes" VALUES(3,30,2,'Parameter Change',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(3,30,3,'Short',0.09,2);
INSERT INTO "tbl_failure_modes" VALUES(3,31,1,'Open',0.65,2);
INSERT INTO "tbl_failure_modes" VALUES(3,31,2,'Parameter Change',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(3,31,3,'Short',0.09,2);
INSERT INTO "tbl_failure_modes" VALUES(3,33,1,'Open',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(3,33,2,'Erratic Output',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(3,33,3,'Short',0.07,2);
INSERT INTO "tbl_failure_modes" VALUES(3,34,1,'Open',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(3,34,2,'Erratic Output',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(3,34,3,'Short',0.07,2);
INSERT INTO "tbl_failure_modes" VALUES(3,35,1,'Open',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(3,35,2,'Erratic Output',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(3,35,3,'Short',0.07,2);
INSERT INTO "tbl_failure_modes" VALUES(3,36,1,'Open',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(3,36,2,'Erratic Output',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(3,36,3,'Short',0.07,2);
INSERT INTO "tbl_failure_modes" VALUES(3,37,1,'Open',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(3,37,2,'Erratic Output',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(3,37,3,'Short',0.07,2);
INSERT INTO "tbl_failure_modes" VALUES(3,38,1,'Open',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(3,38,2,'Erratic Output',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(3,38,3,'Short',0.07,2);
INSERT INTO "tbl_failure_modes" VALUES(3,39,1,'Open',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(3,39,2,'Erratic Output',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(3,39,3,'Short',0.07,2);
INSERT INTO "tbl_failure_modes" VALUES(4,40,1,'Short',0.63,2);
INSERT INTO "tbl_failure_modes" VALUES(4,40,2,'Open',0.37,2);
INSERT INTO "tbl_failure_modes" VALUES(4,41,1,'Short',0.63,2);
INSERT INTO "tbl_failure_modes" VALUES(4,41,2,'Open',0.37,2);
INSERT INTO "tbl_failure_modes" VALUES(4,42,1,'Short',0.63,2);
INSERT INTO "tbl_failure_modes" VALUES(4,42,2,'Open',0.37,2);
INSERT INTO "tbl_failure_modes" VALUES(4,43,1,'Short',0.63,2);
INSERT INTO "tbl_failure_modes" VALUES(4,43,2,'Open',0.37,2);
INSERT INTO "tbl_failure_modes" VALUES(4,44,1,'Open',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(4,44,2,'Short',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(4,44,3,'Change in Value',0.18,2);
INSERT INTO "tbl_failure_modes" VALUES(4,45,1,'Open',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(4,45,2,'Short',0.4,2);
INSERT INTO "tbl_failure_modes" VALUES(4,45,3,'Change in Value',0.18,2);
INSERT INTO "tbl_failure_modes" VALUES(4,46,1,'Short',0.72,2);
INSERT INTO "tbl_failure_modes" VALUES(4,46,2,'Change in Value',0.15,2);
INSERT INTO "tbl_failure_modes" VALUES(4,46,3,'Open',0.13,2);
INSERT INTO "tbl_failure_modes" VALUES(4,47,1,'Short',0.72,2);
INSERT INTO "tbl_failure_modes" VALUES(4,47,2,'Change in Value',0.15,2);
INSERT INTO "tbl_failure_modes" VALUES(4,47,3,'Open',0.13,2);
INSERT INTO "tbl_failure_modes" VALUES(4,48,1,'Short',0.72,2);
INSERT INTO "tbl_failure_modes" VALUES(4,48,2,'Change in Value',0.15,2);
INSERT INTO "tbl_failure_modes" VALUES(4,48,3,'Open',0.13,2);
INSERT INTO "tbl_failure_modes" VALUES(4,49,1,'Short',0.49,2);
INSERT INTO "tbl_failure_modes" VALUES(4,49,2,'Change in Value',0.29,2);
INSERT INTO "tbl_failure_modes" VALUES(4,49,3,'Open',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(4,50,1,'Short',0.49,2);
INSERT INTO "tbl_failure_modes" VALUES(4,50,2,'Change in Value',0.29,2);
INSERT INTO "tbl_failure_modes" VALUES(4,50,3,'Open',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(4,51,1,'Short',0.69,2);
INSERT INTO "tbl_failure_modes" VALUES(4,51,2,'Open',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(4,51,3,'Change in Value',0.14,2);
INSERT INTO "tbl_failure_modes" VALUES(4,52,1,'Short',0.69,2);
INSERT INTO "tbl_failure_modes" VALUES(4,52,2,'Open',0.17,2);
INSERT INTO "tbl_failure_modes" VALUES(4,52,3,'Change in Value',0.14,2);
INSERT INTO "tbl_failure_modes" VALUES(4,53,1,'Short',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(4,53,2,'Open',0.35,2);
INSERT INTO "tbl_failure_modes" VALUES(4,53,3,'Electrolytic Leak',0.1,2);
INSERT INTO "tbl_failure_modes" VALUES(4,53,4,'Change in Value',0.02,2);
INSERT INTO "tbl_failure_modes" VALUES(4,54,1,'Short',0.53,2);
INSERT INTO "tbl_failure_modes" VALUES(4,54,2,'Open',0.35,2);
INSERT INTO "tbl_failure_modes" VALUES(4,54,3,'Electrolytic Leak',0.1,2);
INSERT INTO "tbl_failure_modes" VALUES(4,54,4,'Change in Value',0.02,2);
INSERT INTO "tbl_failure_modes" VALUES(4,55,1,'Short',0.49,2);
INSERT INTO "tbl_failure_modes" VALUES(4,55,2,'Change in Value',0.29,2);
INSERT INTO "tbl_failure_modes" VALUES(4,55,3,'Open',0.22,2);
INSERT INTO "tbl_failure_modes" VALUES(4,56,1,'Change in Value',0.6,2);
INSERT INTO "tbl_failure_modes" VALUES(4,56,2,'Short',0.3,2);
INSERT INTO "tbl_failure_modes" VALUES(4,56,3,'Open',0.1,2);
INSERT INTO "tbl_failure_modes" VALUES(5,59,1,'Open',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,59,2,'Short',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,59,3,'Parameter Change',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(5,60,1,'Open',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,60,2,'Short',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,60,3,'Parameter Change',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(5,61,1,'Open',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,61,2,'Short',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,61,3,'Parameter Change',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(5,62,1,'Open',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,62,2,'Short',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,62,3,'Parameter Change',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(5,63,1,'Short',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,63,2,'Open',0.42,2);
INSERT INTO "tbl_failure_modes" VALUES(5,63,3,'Change in Value',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(6,64,1,'Fails to Trip',0.55,2);
INSERT INTO "tbl_failure_modes" VALUES(6,64,2,'Spurious Trip',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(6,64,3,'Short',0.19,2);
INSERT INTO "tbl_failure_modes" VALUES(6,65,1,'Fails to Trip',0.55,2);
INSERT INTO "tbl_failure_modes" VALUES(6,65,2,'Spurious Trip',0.26,2);
INSERT INTO "tbl_failure_modes" VALUES(6,65,3,'Short',0.19,2);
INSERT INTO "tbl_failure_modes" VALUES(7,67,1,'Open',0.65,2);
INSERT INTO "tbl_failure_modes" VALUES(7,67,2,'Sticking',0.19,2);
INSERT INTO "tbl_failure_modes" VALUES(7,67,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(8,72,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(8,72,2,'Poor Contact/Intermittent',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(8,72,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(8,73,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(8,73,2,'Poor Contact/Intermittent',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(8,73,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(8,74,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(8,74,2,'Poor Contact/Intermittent',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(8,74,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(8,75,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(8,75,2,'Poor Contact/Intermittent',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(8,75,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(8,76,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(8,76,2,'Poor Contact/Intermittent',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(8,76,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(8,83,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(8,83,2,'Poor Contact/Intermittent',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(8,83,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(8,87,1,'Open',0.61,2);
INSERT INTO "tbl_failure_modes" VALUES(8,87,2,'Poor Contact/Intermittent',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(8,87,3,'Short',0.16,2);
INSERT INTO "tbl_failure_modes" VALUES(9,77,1,'Faulty Indication',0.51,2);
INSERT INTO "tbl_failure_modes" VALUES(9,77,2,'Unable to Adjust',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(9,77,3,'Open',0.14,2);
INSERT INTO "tbl_failure_modes" VALUES(9,77,4,'No Indication',0.12,2);
INSERT INTO "tbl_failure_modes" VALUES(9,78,1,'Faulty Indication',0.51,2);
INSERT INTO "tbl_failure_modes" VALUES(9,78,2,'Unable to Adjust',0.23,2);
INSERT INTO "tbl_failure_modes" VALUES(9,78,3,'Open',0.14,2);
INSERT INTO "tbl_failure_modes" VALUES(9,78,4,'No Indication',0.12,2);
INSERT INTO "tbl_failure_modes" VALUES(10,81,1,'No Illumination',0.67,2);
INSERT INTO "tbl_failure_modes" VALUES(10,81,2,'Reduced Illumination',0.33,2);
INSERT INTO "tbl_failure_modes" VALUES(10,82,1,'Fail to Open',0.49,2);
INSERT INTO "tbl_failure_modes" VALUES(10,82,2,'Slow to Open',0.43,2);
INSERT INTO "tbl_failure_modes" VALUES(10,82,3,'Premature Open',0.08,2);

--
-- Damaging operating conditions.
--
CREATE TABLE "tbl_op_condition" (
    "fld_condition_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  -- The operationg condition ID.
    "fld_condition_name" VARCHAR(256)                               -- The operating condition name.
);
INSERT INTO "tbl_op_condition" VALUES(0, "Cavitation");
INSERT INTO "tbl_op_condition" VALUES(1, "Cold Start");
INSERT INTO "tbl_op_condition" VALUES(2, "Contaminated Oil");
INSERT INTO "tbl_op_condition" VALUES(3, "Cyclic Loading, Low Cycle");
INSERT INTO "tbl_op_condition" VALUES(4, "Cyclic Loading, High Cycle");
INSERT INTO "tbl_op_condition" VALUES(5, "Emergency Stop");
INSERT INTO "tbl_op_condition" VALUES(6, "Full Load");
INSERT INTO "tbl_op_condition" VALUES(7, "High Idle");
INSERT INTO "tbl_op_condition" VALUES(8, "Hot Shutdown");
INSERT INTO "tbl_op_condition" VALUES(9, "Idle");
INSERT INTO "tbl_op_condition" VALUES(10, "Low End Torque");
INSERT INTO "tbl_op_condition" VALUES(11, "Mechanical Shock");
INSERT INTO "tbl_op_condition" VALUES(12, "Oil Pressure Fluctuations");
INSERT INTO "tbl_op_condition" VALUES(13, "Overload");
INSERT INTO "tbl_op_condition" VALUES(14, "Overspeed");
INSERT INTO "tbl_op_condition" VALUES(15, "Pressure Pulsations");
INSERT INTO "tbl_op_condition" VALUES(16, "Short Term Overload");
INSERT INTO "tbl_op_condition" VALUES(17, "Start-Stop");
INSERT INTO "tbl_op_condition" VALUES(18, "System Cool Down");
INSERT INTO "tbl_op_condition" VALUES(19, "System Warm Up");
INSERT INTO "tbl_op_condition" VALUES(20, "Thermal Cycling");
INSERT INTO "tbl_op_condition" VALUES(21, "Vibration");

--
-- Operating conditions that are measureable.
--
CREATE TABLE "tbl_measurements" (
    "fld_measurement_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,    -- Measurement parameter ID.
    "fld_measurement_name" VARCHAR(256)                             -- Parameter measurement name.
);
INSERT INTO "tbl_measurements" VALUES(0, "Contamination, Concentration");
INSERT INTO "tbl_measurements" VALUES(1, "Contamination, Particle Size");
INSERT INTO "tbl_measurements" VALUES(2, "Dynamic Load");
INSERT INTO "tbl_measurements" VALUES(3, "Load, Maximum");
INSERT INTO "tbl_measurements" VALUES(4, "Load, Minimum-Maximum");
INSERT INTO "tbl_measurements" VALUES(5, "Number of Braking Events");
INSERT INTO "tbl_measurements" VALUES(6, "Number of Cycles");
INSERT INTO "tbl_measurements" VALUES(7, "Number of Overload Events");
INSERT INTO "tbl_measurements" VALUES(8, "Number of Shifts");
INSERT INTO "tbl_measurements" VALUES(9, "Operating Time at Condition");
INSERT INTO "tbl_measurements" VALUES(10, "Pressure, Average");
INSERT INTO "tbl_measurements" VALUES(11, "Pressure, Differential");
INSERT INTO "tbl_measurements" VALUES(12, "Pressure, Peak");
INSERT INTO "tbl_measurements" VALUES(13, "RPM");
INSERT INTO "tbl_measurements" VALUES(14, "Temperature, Ambient");
INSERT INTO "tbl_measurements" VALUES(15, "Temperature, Average");
INSERT INTO "tbl_measurements" VALUES(16, "Temperature, Differential");
INSERT INTO "tbl_measurements" VALUES(17, "Temperature, Peak");
INSERT INTO "tbl_measurements" VALUES(18, "Temperature = f(Time)");
INSERT INTO "tbl_measurements" VALUES(19, "Torque");

--
-- Methods of summarizing load histories.
--
CREATE TABLE "tbl_load_history" (
    "fld_history_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,    -- Load history ID.
    "fld_history_name" VARCHAR(256)                                 -- Load history name.
);
INSERT INTO "tbl_load_history" VALUES(0, "Cycle Counts");
INSERT INTO "tbl_load_history" VALUES(1, "Histogram");
INSERT INTO "tbl_load_history" VALUES(2, "Histogram, Bivariate");
INSERT INTO "tbl_load_history" VALUES(3, "Level Crossing");
INSERT INTO "tbl_load_history" VALUES(4, "Rain Flow Count");
INSERT INTO "tbl_load_history" VALUES(5, "Time at Level");
INSERT INTO "tbl_load_history" VALUES(6, "Time at Load");
INSERT INTO "tbl_load_history" VALUES(7, "Time at Maximum");
INSERT INTO "tbl_load_history" VALUES(8, "Time at Minimum");

DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('tbl_allocation_models',5);
INSERT INTO "sqlite_sequence" VALUES('tbl_calculation_model',7);
INSERT INTO "sqlite_sequence" VALUES('tbl_category',10);
INSERT INTO "sqlite_sequence" VALUES('tbl_cost_type',2);
INSERT INTO "sqlite_sequence" VALUES('tbl_development_environment',2);
INSERT INTO "sqlite_sequence" VALUES('tbl_development_phase',5);
INSERT INTO "sqlite_sequence" VALUES('tbl_distributions',5);
INSERT INTO "sqlite_sequence" VALUES('tbl_hr_type',3);
INSERT INTO "sqlite_sequence" VALUES('tbl_manufacturers',3);
INSERT INTO "sqlite_sequence" VALUES('tbl_measurement_units',8);
INSERT INTO "sqlite_sequence" VALUES('tbl_mttr_type',2);
INSERT INTO "sqlite_sequence" VALUES('tbl_risk_category',5);
INSERT INTO "sqlite_sequence" VALUES('tbl_software_application',5);
INSERT INTO "sqlite_sequence" VALUES('tbl_software_level',2);
INSERT INTO "sqlite_sequence" VALUES('tbl_software_category',17);
INSERT INTO "sqlite_sequence" VALUES('tbl_test_techniques',5);
INSERT INTO "sqlite_sequence" VALUES('tbl_users',2);
INSERT INTO "sqlite_sequence" VALUES('tbl_lifecycles',7);
INSERT INTO "sqlite_sequence" VALUES('tbl_incident_category',3);
INSERT INTO "sqlite_sequence" VALUES('tbl_incident_type',9);
INSERT INTO "sqlite_sequence" VALUES('tbl_incident_relevency',16);
INSERT INTO "sqlite_sequence" VALUES('tbl_rpn_severity',10);
INSERT INTO "sqlite_sequence" VALUES('tbl_rpn_occurrence',10);
INSERT INTO "sqlite_sequence" VALUES('tbl_rpn_detection',10);
INSERT INTO "sqlite_sequence" VALUES('tbl_action_category',5);
INSERT INTO "sqlite_sequence" VALUES('tbl_hazards',186);
INSERT INTO "sqlite_sequence" VALUES('tbl_environmental_conditions',33);
INSERT INTO "sqlite_sequence" VALUES('tbl_requirement_type',16);
INSERT INTO "sqlite_sequence" VALUES('tbl_stakeholders',1);
INSERT INTO "sqlite_sequence" VALUES('tbl_status',10);
INSERT INTO "sqlite_sequence" VALUES('tbl_groups',6);
INSERT INTO "sqlite_sequence" VALUES('tbl_validation_type',25);
INSERT INTO "sqlite_sequence" VALUES('tbl_gateways',7);
COMMIT;
