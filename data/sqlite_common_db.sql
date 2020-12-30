BEGIN TRANSACTION;
DROP TABLE IF EXISTS `ramstk_user`;
CREATE TABLE IF NOT EXISTS `ramstk_user` (
	`fld_user_id`	INTEGER NOT NULL,
	`fld_user_lname`	VARCHAR ( 256 ),
	`fld_user_fname`	VARCHAR ( 256 ),
	`fld_user_email`	VARCHAR ( 256 ),
	`fld_user_phone`	VARCHAR ( 256 ),
	`fld_user_group_id`	VARCHAR ( 256 ),
	PRIMARY KEY(`fld_user_id`)
);
INSERT INTO `ramstk_user` VALUES (1,'Tester','Johnny','tester.johnny@reliaqual.com','+1.269.867.5309','1');
DROP TABLE IF EXISTS `ramstk_type`;
CREATE TABLE IF NOT EXISTS `ramstk_type` (
	`fld_type_id`	INTEGER NOT NULL,
	`fld_code`	VARCHAR ( 256 ),
	`fld_description`	VARCHAR ( 512 ),
	`fld_type`	VARCHAR ( 256 ),
	PRIMARY KEY(`fld_type_id`)
);
INSERT INTO `ramstk_type` VALUES (1,'PLN','Planning','incident');
INSERT INTO `ramstk_type` VALUES (2,'CON','Concept','incident');
INSERT INTO `ramstk_type` VALUES (3,'RQMT','Requirement','incident');
INSERT INTO `ramstk_type` VALUES (4,'DES','Design','incident');
INSERT INTO `ramstk_type` VALUES (5,'COD','Coding','incident');
INSERT INTO `ramstk_type` VALUES (6,'DB','Database','incident');
INSERT INTO `ramstk_type` VALUES (7,'TI','Test Information','incident');
INSERT INTO `ramstk_type` VALUES (8,'MAN','Manuals','incident');
INSERT INTO `ramstk_type` VALUES (9,'OTH','Other','incident');
INSERT INTO `ramstk_type` VALUES (10,'FUN','Functional','requirement');
INSERT INTO `ramstk_type` VALUES (11,'PRF','Performance','requirement');
INSERT INTO `ramstk_type` VALUES (12,'REG','Regulatory','requirement');
INSERT INTO `ramstk_type` VALUES (13,'REL','Reliability','requirement');
INSERT INTO `ramstk_type` VALUES (14,'SAF','Safety','requirement');
INSERT INTO `ramstk_type` VALUES (15,'SVC','Serviceability','requirement');
INSERT INTO `ramstk_type` VALUES (16,'USE','Useability','requirement');
INSERT INTO `ramstk_type` VALUES (17,'DOE','Manufacturing Test, DOE','validation');
INSERT INTO `ramstk_type` VALUES (18,'ESS','Manufacturing Test, ESS','validation');
INSERT INTO `ramstk_type` VALUES (19,'HSS','Manufacturing Test, HASS','validation');
INSERT INTO `ramstk_type` VALUES (20,'PRT','Manufacturing Test, PRAT','validation');
INSERT INTO `ramstk_type` VALUES (21,'RAA','Reliability, Assessment','validation');
INSERT INTO `ramstk_type` VALUES (22,'RDA','Reliability, Durability Analysis','validation');
INSERT INTO `ramstk_type` VALUES (23,'RFF','Reliability, FFMEA','validation');
INSERT INTO `ramstk_type` VALUES (24,'RDF','Reliability, (D)FMEA','validation');
INSERT INTO `ramstk_type` VALUES (25,'RCA','Reliability, Root Cause Analysis','validation');
INSERT INTO `ramstk_type` VALUES (26,'RSA','Reliability, Survival Analysis','validation');
INSERT INTO `ramstk_type` VALUES (27,'ALT','Reliability Test, ALT','validation');
INSERT INTO `ramstk_type` VALUES (28,'RDT','Reliability Test, Demonstration','validation');
INSERT INTO `ramstk_type` VALUES (29,'HLT','Reliability Test, HALT','validation');
INSERT INTO `ramstk_type` VALUES (30,'RGT','Reliability Test, Growth','validation');
INSERT INTO `ramstk_type` VALUES (31,'FTA','Safety, Fault Tree Analysis','validation');
INSERT INTO `ramstk_type` VALUES (32,'PHA','Safety, Hazards Analysis','validation');
INSERT INTO `ramstk_type` VALUES (33,'EMA','System Engineering, Electromagnetic Analysis','validation');
INSERT INTO `ramstk_type` VALUES (34,'FEA','System Engineering, FEA','validation');
INSERT INTO `ramstk_type` VALUES (35,'2DM','System Engineering, 2D Model','validation');
INSERT INTO `ramstk_type` VALUES (36,'3DM','System Engineering, 3D Model','validation');
INSERT INTO `ramstk_type` VALUES (37,'SRD','System Engineering, Robust Design','validation');
INSERT INTO `ramstk_type` VALUES (38,'SCA','System Engineering, Sneak Circuit Analysis','validation');
INSERT INTO `ramstk_type` VALUES (39,'THA','System Engineering, Thermal Analysis','validation');
INSERT INTO `ramstk_type` VALUES (40,'TOL','System Engineering, Tolerance Analysis','validation');
INSERT INTO `ramstk_type` VALUES (41,'WCA','System Engineering, Worst Case Analysis','validation');
DROP TABLE IF EXISTS `ramstk_subcategory`;
CREATE TABLE IF NOT EXISTS `ramstk_subcategory` (
	`fld_category_id`	INTEGER NOT NULL,
	`fld_subcategory_id`	INTEGER NOT NULL,
	`fld_description`	VARCHAR ( 512 ),
	PRIMARY KEY(`fld_subcategory_id`),
	FOREIGN KEY(`fld_category_id`) REFERENCES `ramstk_category`(`fld_category_id`)
);
INSERT INTO `ramstk_subcategory` VALUES (1,1,'Linear');
INSERT INTO `ramstk_subcategory` VALUES (1,2,'Logic');
INSERT INTO `ramstk_subcategory` VALUES (1,3,'PAL, PLA');
INSERT INTO `ramstk_subcategory` VALUES (1,4,'Microprocessor, Microcontroller');
INSERT INTO `ramstk_subcategory` VALUES (1,5,'Memory, ROM');
INSERT INTO `ramstk_subcategory` VALUES (1,6,'Memory, EEPROM');
INSERT INTO `ramstk_subcategory` VALUES (1,7,'Memory, DRAM');
INSERT INTO `ramstk_subcategory` VALUES (1,8,'Memory, SRAM');
INSERT INTO `ramstk_subcategory` VALUES (1,9,'GaAs');
INSERT INTO `ramstk_subcategory` VALUES (1,10,'VHSIC, VLSI');
INSERT INTO `ramstk_subcategory` VALUES (2,11,'Diode, Low Frequency');
INSERT INTO `ramstk_subcategory` VALUES (2,12,'Diode, High Frequency');
INSERT INTO `ramstk_subcategory` VALUES (2,13,'Transistor, Low Frequency, Bipolar');
INSERT INTO `ramstk_subcategory` VALUES (2,14,'Transistor, Low Frequency, Si FET');
INSERT INTO `ramstk_subcategory` VALUES (2,15,'Transistor, Unijunction');
INSERT INTO `ramstk_subcategory` VALUES (2,16,'Transistor, High Frequency, Low Noise, Bipolar');
INSERT INTO `ramstk_subcategory` VALUES (2,17,'Transistor, High Frequency, High Power, Bipolar');
INSERT INTO `ramstk_subcategory` VALUES (2,18,'Transistor, High Frequency, GaAs FET');
INSERT INTO `ramstk_subcategory` VALUES (2,19,'Transistor, High Frequency, Si FET');
INSERT INTO `ramstk_subcategory` VALUES (2,20,'Thyristor, SCR');
INSERT INTO `ramstk_subcategory` VALUES (2,21,'Optoelectronic, Detector, Isolator, Emitter');
INSERT INTO `ramstk_subcategory` VALUES (2,22,'Optoelectronic, Alphanumeric Display');
INSERT INTO `ramstk_subcategory` VALUES (2,23,'Optoelectronic, Laser Diode');
INSERT INTO `ramstk_subcategory` VALUES (3,24,'Fixed, Composition (RC, RCR)');
INSERT INTO `ramstk_subcategory` VALUES (3,25,'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)');
INSERT INTO `ramstk_subcategory` VALUES (3,26,'Fixed, Film, Power (RD)');
INSERT INTO `ramstk_subcategory` VALUES (3,27,'Fixed, Film, Network (RZ)');
INSERT INTO `ramstk_subcategory` VALUES (3,28,'Fixed, Wirewound (RB, RBR)');
INSERT INTO `ramstk_subcategory` VALUES (3,29,'Fixed, Wirewound, Power (RW, RWR)');
INSERT INTO `ramstk_subcategory` VALUES (3,30,'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)');
INSERT INTO `ramstk_subcategory` VALUES (3,31,'Thermistor (RTH)');
INSERT INTO `ramstk_subcategory` VALUES (3,32,'Variable, Wirewound (RT, RTR)');
INSERT INTO `ramstk_subcategory` VALUES (3,33,'Variable, Wirewound, Precision (RR)');
INSERT INTO `ramstk_subcategory` VALUES (3,34,'Variable, Wirewound, Semiprecision (RA, RK)');
INSERT INTO `ramstk_subcategory` VALUES (3,35,'Variable, Wirewound, Power (RP)');
INSERT INTO `ramstk_subcategory` VALUES (3,36,'Variable, Non-Wirewound (RJ, RJR)');
INSERT INTO `ramstk_subcategory` VALUES (3,37,'Variable, Composition (RV)');
INSERT INTO `ramstk_subcategory` VALUES (3,38,'Variable, Non-Wirewound, Film and Precision (RQ, RVC)');
INSERT INTO `ramstk_subcategory` VALUES (4,39,'Fixed, Paper, Bypass (CA, CP)');
INSERT INTO `ramstk_subcategory` VALUES (4,40,'Fixed, Feed-Through (CZ, CZR)');
INSERT INTO `ramstk_subcategory` VALUES (4,41,'Fixed, Paper and Plastic Film (CPV, CQ, CQR)');
INSERT INTO `ramstk_subcategory` VALUES (4,42,'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)');
INSERT INTO `ramstk_subcategory` VALUES (4,43,'Fixed, Plastic and Metallized Plastic');
INSERT INTO `ramstk_subcategory` VALUES (4,44,'Fixed, Super-Metallized Plastic (CRH)');
INSERT INTO `ramstk_subcategory` VALUES (4,45,'Fixed, Mica (CM, CMR)');
INSERT INTO `ramstk_subcategory` VALUES (4,46,'Fixed, Mica, Button (CB)');
INSERT INTO `ramstk_subcategory` VALUES (4,47,'Fixed, Glass (CY, CYR)');
INSERT INTO `ramstk_subcategory` VALUES (4,48,'Fixed, Ceramic, General Purpose (CK, CKR)');
INSERT INTO `ramstk_subcategory` VALUES (4,49,'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)');
INSERT INTO `ramstk_subcategory` VALUES (4,50,'Fixed, Electrolytic, Tantalum, Solid (CSR)');
INSERT INTO `ramstk_subcategory` VALUES (4,51,'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)');
INSERT INTO `ramstk_subcategory` VALUES (4,52,'Fixed, Electrolytic, Aluminum (CU, CUR)');
INSERT INTO `ramstk_subcategory` VALUES (4,53,'Fixed, Electrolytic (Dry), Aluminum (CE)');
INSERT INTO `ramstk_subcategory` VALUES (4,54,'Variable, Ceramic (CV)');
INSERT INTO `ramstk_subcategory` VALUES (4,55,'Variable, Piston Type (PC)');
INSERT INTO `ramstk_subcategory` VALUES (4,56,'Variable, Air Trimmer (CT)');
INSERT INTO `ramstk_subcategory` VALUES (4,57,'Variable and Fixed, Gas or Vacuum (CG)');
INSERT INTO `ramstk_subcategory` VALUES (5,58,'Transformer');
INSERT INTO `ramstk_subcategory` VALUES (5,59,'Coil');
INSERT INTO `ramstk_subcategory` VALUES (6,60,'Mechanical');
INSERT INTO `ramstk_subcategory` VALUES (6,61,'Solid State');
INSERT INTO `ramstk_subcategory` VALUES (7,62,'Toggle or Pushbutton');
INSERT INTO `ramstk_subcategory` VALUES (7,63,'Sensitive');
INSERT INTO `ramstk_subcategory` VALUES (7,64,'Rotary');
INSERT INTO `ramstk_subcategory` VALUES (7,65,'Thumbwheel');
INSERT INTO `ramstk_subcategory` VALUES (7,66,'Circuit Breaker');
INSERT INTO `ramstk_subcategory` VALUES (8,67,'Multi-Pin');
INSERT INTO `ramstk_subcategory` VALUES (8,68,'PCB Edge');
INSERT INTO `ramstk_subcategory` VALUES (8,69,'IC Socket');
INSERT INTO `ramstk_subcategory` VALUES (8,70,'Plated Through Hole (PTH)');
INSERT INTO `ramstk_subcategory` VALUES (8,71,'Connection, Non-PTH');
INSERT INTO `ramstk_subcategory` VALUES (9,72,'Elapsed Time');
INSERT INTO `ramstk_subcategory` VALUES (9,73,'Panel');
INSERT INTO `ramstk_subcategory` VALUES (10,74,'Crystal');
INSERT INTO `ramstk_subcategory` VALUES (10,75,'Filter, Non-Tunable Electronic');
INSERT INTO `ramstk_subcategory` VALUES (10,76,'Fuse');
INSERT INTO `ramstk_subcategory` VALUES (10,77,'Lamp');
DROP TABLE IF EXISTS `ramstk_status`;
CREATE TABLE IF NOT EXISTS `ramstk_status` (
	`fld_status_id`	INTEGER NOT NULL,
	`fld_name`	VARCHAR ( 256 ),
	`fld_description`	VARCHAR ( 512 ),
	`fld_status_type`	VARCHAR ( 256 ),
	PRIMARY KEY(`fld_status_id`)
);
INSERT INTO `ramstk_status` VALUES (1,'Initiated','Incident has been initiated.','incident');
INSERT INTO `ramstk_status` VALUES (2,'Reviewed','Incident has been reviewed.','incident');
INSERT INTO `ramstk_status` VALUES (3,'Analysis','Incident has been assigned and is being analyzed.','incident');
INSERT INTO `ramstk_status` VALUES (4,'Solution Identified','A solution to the reported problem has been identified.','incident');
INSERT INTO `ramstk_status` VALUES (5,'Solution Implemented','A solution to the reported problem has been implemented.','incident');
INSERT INTO `ramstk_status` VALUES (6,'Solution Verified','A solution to the reported problem has been verified.','incident');
INSERT INTO `ramstk_status` VALUES (7,'Ready for Approval','Incident analysis is ready to be approved.','incident');
INSERT INTO `ramstk_status` VALUES (8,'Approved','Incident analysis has been approved.','incident');
INSERT INTO `ramstk_status` VALUES (9,'Ready for Closure','Incident is ready to be closed.','incident');
INSERT INTO `ramstk_status` VALUES (10,'Closed','Incident has been closed.','incident');
INSERT INTO `ramstk_status` VALUES (11,'Initiated','Action has been initiated.','action');
INSERT INTO `ramstk_status` VALUES (12,'Reviewed','Action has been reviewed.','action');
INSERT INTO `ramstk_status` VALUES (13,'Approved','Action has been approved.','action');
INSERT INTO `ramstk_status` VALUES (14,'Ready for Closure','Action is ready to be closed.','action');
INSERT INTO `ramstk_status` VALUES (15,'Closed','Action has been closed.','action');
DROP TABLE IF EXISTS `ramstk_stakeholders`;
CREATE TABLE IF NOT EXISTS `ramstk_stakeholders` (
	`fld_stakeholders_id`	INTEGER NOT NULL,
	`fld_stakeholder`	VARCHAR ( 512 ),
	PRIMARY KEY(`fld_stakeholders_id`)
);
INSERT INTO `ramstk_stakeholders` VALUES (1,'Customer');
INSERT INTO `ramstk_stakeholders` VALUES (2,'Service');
INSERT INTO `ramstk_stakeholders` VALUES (3,'Manufacturing');
INSERT INTO `ramstk_stakeholders` VALUES (4,'Management');
DROP TABLE IF EXISTS `ramstk_site_info`;
CREATE TABLE IF NOT EXISTS `ramstk_site_info` (
	`fld_site_id`	INTEGER NOT NULL,
	`fld_product_key`	VARCHAR ( 512 ),
	`fld_expire_on`	DATE,
	`fld_function_enabled`	INTEGER,
	`fld_requirement_enabled`	INTEGER,
	`fld_hardware_enabled`	INTEGER,
	`fld_vandv_enabled`	INTEGER,
	`fld_fmea_enabled`	INTEGER,
	PRIMARY KEY(`fld_site_id`)
);
INSERT INTO `ramstk_site_info` VALUES (1,'0000','2019-08-20',0,0,0,0,0);
DROP TABLE IF EXISTS `ramstk_rpn`;
CREATE TABLE IF NOT EXISTS `ramstk_rpn` (
	`fld_rpn_id`	INTEGER NOT NULL,
	`fld_name`	VARCHAR ( 512 ),
	`fld_description`	VARCHAR ( 512 ),
	`fld_rpn_type`	VARCHAR ( 256 ),
	`fld_value`	INTEGER,
	PRIMARY KEY(`fld_rpn_id`)
);
INSERT INTO `ramstk_rpn` VALUES (1,'None','No effect.','severity',1);
INSERT INTO `ramstk_rpn` VALUES (2,'Very Minor','System operable with minimal interference.','severity',2);
INSERT INTO `ramstk_rpn` VALUES (3,'Minor','System operable with some degradation of performance.','severity',3);
INSERT INTO `ramstk_rpn` VALUES (4,'Very Low','System operable with significant degradation of performance.','severity',4);
INSERT INTO `ramstk_rpn` VALUES (5,'Low','System inoperable without damage.','severity',5);
INSERT INTO `ramstk_rpn` VALUES (6,'Moderate','System inoperable with minor damage.','severity',6);
INSERT INTO `ramstk_rpn` VALUES (7,'High','System inoperable with system damage.','severity',7);
INSERT INTO `ramstk_rpn` VALUES (8,'Very High','System inoperable with destructive failure without compromising safety.','severity',8);
INSERT INTO `ramstk_rpn` VALUES (9,'Hazardous, with warning','Failure effects safe system operation with warning.','severity',9);
INSERT INTO `ramstk_rpn` VALUES (10,'Hazardous, without warning','Failure effects safe system operation without warning.','severity',10);
INSERT INTO `ramstk_rpn` VALUES (11,'Remote','Failure rate is 1 in 1,500,000.','occurrence',1);
INSERT INTO `ramstk_rpn` VALUES (12,'Very Low','Failure rate is 1 in 150,000.','occurrence',2);
INSERT INTO `ramstk_rpn` VALUES (13,'Low','Failure rate is 1 in 15,000','occurrence',3);
INSERT INTO `ramstk_rpn` VALUES (14,'Moderately Low','Failure rate is 1 in 2000.','occurrence',4);
INSERT INTO `ramstk_rpn` VALUES (15,'Moderate','Failure rate is 1 in 400.','occurrence',5);
INSERT INTO `ramstk_rpn` VALUES (16,'Moderately High','Failure rate is 1 in 80.','occurrence',6);
INSERT INTO `ramstk_rpn` VALUES (17,'High','Failure rate is 1 in 20.','occurrence',7);
INSERT INTO `ramstk_rpn` VALUES (18,'Very High','Failure rate is 1 in 8.','occurrence',8);
INSERT INTO `ramstk_rpn` VALUES (19,'Extremely High','Failure rate is 1 in 3.','occurrence',9);
INSERT INTO `ramstk_rpn` VALUES (20,'Dangerously High','Failure rate is > 1 in 2.','occurrence',10);
INSERT INTO `ramstk_rpn` VALUES (21,'Almost Certain','Design control will almost certainly detect a potential mechanism/cause and subsequent failure mode.','detection',1);
INSERT INTO `ramstk_rpn` VALUES (22,'Very High','Very high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',2);
INSERT INTO `ramstk_rpn` VALUES (23,'High','High chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',3);
INSERT INTO `ramstk_rpn` VALUES (24,'Moderately High','Moderately high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',4);
INSERT INTO `ramstk_rpn` VALUES (25,'Moderate','Moderate chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',5);
INSERT INTO `ramstk_rpn` VALUES (26,'Low','Low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',6);
INSERT INTO `ramstk_rpn` VALUES (27,'Very Low','Very low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',7);
INSERT INTO `ramstk_rpn` VALUES (28,'Remote','Remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',8);
INSERT INTO `ramstk_rpn` VALUES (29,'Very Remote','Very remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.','detection',9);
INSERT INTO `ramstk_rpn` VALUES (30,'Absolute Uncertainty','Existing design controls will not or cannot detect a potential mechanism/cause and subsequent failure mode; there is no design control.','detection',10);
DROP TABLE IF EXISTS `ramstk_model`;
CREATE TABLE IF NOT EXISTS `ramstk_model` (
	`fld_model_id`	INTEGER NOT NULL,
	`fld_description`	VARCHAR ( 512 ),
	`fld_model_type`	INTEGER,
	PRIMARY KEY(`fld_model_id`)
);
INSERT INTO `ramstk_model` VALUES (1,'Adhesion Wear Model for Bearings','damage');
INSERT INTO `ramstk_model` VALUES (2,'Arrhenius','damage');
INSERT INTO `ramstk_model` VALUES (3,'Coffin-Manson','damage');
INSERT INTO `ramstk_model` VALUES (4,'Empirical/DOE','damage');
INSERT INTO `ramstk_model` VALUES (5,'Eyring','damage');
INSERT INTO `ramstk_model` VALUES (6,'Inverse Power Law (IPL)','damage');
INSERT INTO `ramstk_model` VALUES (7,'IPL - Arrhenius','damage');
INSERT INTO `ramstk_model` VALUES (8,'Time Fraction of Damaging Operating Conditions','damage');
DROP TABLE IF EXISTS `ramstk_method`;
CREATE TABLE IF NOT EXISTS `ramstk_method` (
	`fld_method_id`	INTEGER NOT NULL,
	`fld_name`	VARCHAR ( 256 ),
	`fld_description`	VARCHAR ( 512 ),
	`fld_method_type`	VARCHAR ( 256 ),
	PRIMARY KEY(`fld_method_id`)
);
INSERT INTO `ramstk_method` VALUES (1,'Code Reviews','','detection');
INSERT INTO `ramstk_method` VALUES (2,'Error/Anomaly Detection','','detection');
INSERT INTO `ramstk_method` VALUES (3,'Structure Analysis','','detection');
INSERT INTO `ramstk_method` VALUES (4,'Random Testing','','detection');
INSERT INTO `ramstk_method` VALUES (5,'Functional Testing','','detection');
INSERT INTO `ramstk_method` VALUES (6,'Branch Testing','','detection');
DROP TABLE IF EXISTS `ramstk_measurement`;
CREATE TABLE IF NOT EXISTS `ramstk_measurement` (
	`fld_measurement_id`	INTEGER NOT NULL,
	`fld_code`	VARCHAR ( 128 ),
	`fld_description`	VARCHAR ( 512 ),
	`fld_type`	VARCHAR ( 128 ),
	PRIMARY KEY(`fld_measurement_id`)
);
INSERT INTO `ramstk_measurement` VALUES (1,'lbf','Pounds Force','unit');
INSERT INTO `ramstk_measurement` VALUES (2,'lbm','Pounds Mass','unit');
INSERT INTO `ramstk_measurement` VALUES (3,'hrs','hours','unit');
INSERT INTO `ramstk_measurement` VALUES (4,'N','Newtons','unit');
INSERT INTO `ramstk_measurement` VALUES (5,'mins','minutes','unit');
INSERT INTO `ramstk_measurement` VALUES (6,'secs','seconds','unit');
INSERT INTO `ramstk_measurement` VALUES (7,'g','grams','unit');
INSERT INTO `ramstk_measurement` VALUES (8,'oz','ounces','unit');
INSERT INTO `ramstk_measurement` VALUES (9,'A','Amperes','unit');
INSERT INTO `ramstk_measurement` VALUES (10,'V','Volts','unit');
INSERT INTO `ramstk_measurement` VALUES (11,'CN','Contamination, Concentration','damage');
INSERT INTO `ramstk_measurement` VALUES (12,'CS','Contamination, Particle Size','damage');
INSERT INTO `ramstk_measurement` VALUES (13,'LD','Dynamic Load','damage');
INSERT INTO `ramstk_measurement` VALUES (14,'LM','Load, Maximum','damage');
INSERT INTO `ramstk_measurement` VALUES (15,'LMM','Load, Minimum-Maximum','damage');
INSERT INTO `ramstk_measurement` VALUES (16,'NBC','Number of Braking Events','damage');
INSERT INTO `ramstk_measurement` VALUES (17,'NC','Number of Cycles','damage');
INSERT INTO `ramstk_measurement` VALUES (18,'NOE','Number of Overload Events','damage');
INSERT INTO `ramstk_measurement` VALUES (19,'NS','Number of Shifts','damage');
INSERT INTO `ramstk_measurement` VALUES (20,'TIME','Operating Time at Condition','damage');
INSERT INTO `ramstk_measurement` VALUES (21,'PAVG','Pressure, Average','damage');
INSERT INTO `ramstk_measurement` VALUES (22,'DELTAP','Pressure, Differential','damage');
INSERT INTO `ramstk_measurement` VALUES (23,'PPEAK','Pressure, Peak','damage');
INSERT INTO `ramstk_measurement` VALUES (24,'RPM','Revolutions per Time','damage');
INSERT INTO `ramstk_measurement` VALUES (25,'TAMB','Temperature, Ambient','damage');
INSERT INTO `ramstk_measurement` VALUES (26,'TAVG','Temperature, Average','damage');
INSERT INTO `ramstk_measurement` VALUES (27,'DELTAT','Temperature, Differential','damage');
INSERT INTO `ramstk_measurement` VALUES (28,'TPEAK','Temperature, Peak','damage');
INSERT INTO `ramstk_measurement` VALUES (29,'TEMP','Temperature = f(Time)','damage');
INSERT INTO `ramstk_measurement` VALUES (30,'T','Torque','damage');
DROP TABLE IF EXISTS `ramstk_manufacturer`;
CREATE TABLE IF NOT EXISTS `ramstk_manufacturer` (
	`fld_manufacturer_id`	INTEGER NOT NULL,
	`fld_description`	VARCHAR ( 512 ),
	`fld_location`	VARCHAR ( 512 ),
	`fld_cage_code`	VARCHAR ( 512 ),
	PRIMARY KEY(`fld_manufacturer_id`)
);
INSERT INTO `ramstk_manufacturer` VALUES (1,'Sprague','New Hampshire','13606');
INSERT INTO `ramstk_manufacturer` VALUES (2,'Xilinx','','');
INSERT INTO `ramstk_manufacturer` VALUES (3,'National Semiconductor','California','27014');
DROP TABLE IF EXISTS `ramstk_load_history`;
CREATE TABLE IF NOT EXISTS `ramstk_load_history` (
	`fld_history_id`	INTEGER NOT NULL,
	`fld_description`	VARCHAR ( 512 ),
	PRIMARY KEY(`fld_history_id`)
);
INSERT INTO `ramstk_load_history` VALUES (1,'Cycle Counts');
INSERT INTO `ramstk_load_history` VALUES (2,'Histogram');
INSERT INTO `ramstk_load_history` VALUES (3,'Histogram, Bivariate');
INSERT INTO `ramstk_load_history` VALUES (4,'Level Crossing');
INSERT INTO `ramstk_load_history` VALUES (5,'Rain Flow Count');
INSERT INTO `ramstk_load_history` VALUES (6,'Time at Level');
INSERT INTO `ramstk_load_history` VALUES (7,'Time at Load');
INSERT INTO `ramstk_load_history` VALUES (8,'Time at Maximum');
INSERT INTO `ramstk_load_history` VALUES (9,'Time at Minimum');
DROP TABLE IF EXISTS `ramstk_hazards`;
CREATE TABLE IF NOT EXISTS `ramstk_hazards` (
	`fld_hazard_id`	INTEGER NOT NULL,
	`fld_hazard_category`	VARCHAR ( 512 ),
	`fld_hazard_subcategory`	VARCHAR ( 512 ),
	PRIMARY KEY(`fld_hazard_id`)
);
INSERT INTO `ramstk_hazards` VALUES (1,'Acceleration/Gravity','Falls');
INSERT INTO `ramstk_hazards` VALUES (2,'Acceleration/Gravity','Falling Objects');
INSERT INTO `ramstk_hazards` VALUES (3,'Acceleration/Gravity','Fragments/Missiles');
INSERT INTO `ramstk_hazards` VALUES (4,'Acceleration/Gravity','Impacts');
INSERT INTO `ramstk_hazards` VALUES (5,'Acceleration/Gravity','Inadvertent Motion');
INSERT INTO `ramstk_hazards` VALUES (6,'Acceleration/Gravity','Loose Object Translation');
INSERT INTO `ramstk_hazards` VALUES (7,'Acceleration/Gravity','Slip/Trip');
INSERT INTO `ramstk_hazards` VALUES (8,'Acceleration/Gravity','Sloshing Liquids');
INSERT INTO `ramstk_hazards` VALUES (9,'Chemical/Water Contamination','Backflow/Siphon Effect');
INSERT INTO `ramstk_hazards` VALUES (10,'Chemical/Water Contamination','Leaks/Spills');
INSERT INTO `ramstk_hazards` VALUES (11,'Chemical/Water Contamination','System-Cross Connection');
INSERT INTO `ramstk_hazards` VALUES (12,'Chemical/Water Contamination','Vessel/Pipe/Conduit Rupture');
INSERT INTO `ramstk_hazards` VALUES (13,'Common Causes','Dust/Dirt');
INSERT INTO `ramstk_hazards` VALUES (14,'Common Causes','Faulty Calibration');
INSERT INTO `ramstk_hazards` VALUES (15,'Common Causes','Fire');
INSERT INTO `ramstk_hazards` VALUES (16,'Common Causes','Flooding');
INSERT INTO `ramstk_hazards` VALUES (17,'Common Causes','Location');
INSERT INTO `ramstk_hazards` VALUES (18,'Common Causes','Maintenance Error');
INSERT INTO `ramstk_hazards` VALUES (19,'Common Causes','Moisture/Humidity');
INSERT INTO `ramstk_hazards` VALUES (20,'Common Causes','Radiation');
INSERT INTO `ramstk_hazards` VALUES (21,'Common Causes','Seismic Disturbance/Impact');
INSERT INTO `ramstk_hazards` VALUES (22,'Common Causes','Single-Operator Coupling');
INSERT INTO `ramstk_hazards` VALUES (23,'Common Causes','Temperature Extremes');
INSERT INTO `ramstk_hazards` VALUES (24,'Common Causes','Utility Outages');
INSERT INTO `ramstk_hazards` VALUES (25,'Common Causes','Vibration');
INSERT INTO `ramstk_hazards` VALUES (26,'Common Causes','Wear-Out');
INSERT INTO `ramstk_hazards` VALUES (27,'Common Causes','Vermin/Insects');
INSERT INTO `ramstk_hazards` VALUES (28,'Contingencies','Earthquake');
INSERT INTO `ramstk_hazards` VALUES (29,'Contingencies','Fire');
INSERT INTO `ramstk_hazards` VALUES (30,'Contingencies','Flooding');
INSERT INTO `ramstk_hazards` VALUES (31,'Contingencies','Freezing');
INSERT INTO `ramstk_hazards` VALUES (32,'Contingencies','Hailstorm');
INSERT INTO `ramstk_hazards` VALUES (33,'Contingencies','Shutdowns/Failures');
INSERT INTO `ramstk_hazards` VALUES (34,'Contingencies','Snow/Ice Load');
INSERT INTO `ramstk_hazards` VALUES (35,'Contingencies','Utility Outages');
INSERT INTO `ramstk_hazards` VALUES (36,'Contingencies','Windstorm');
INSERT INTO `ramstk_hazards` VALUES (37,'Control Systems','Grounding Failure');
INSERT INTO `ramstk_hazards` VALUES (38,'Control Systems','Inadvertent Activation');
INSERT INTO `ramstk_hazards` VALUES (39,'Control Systems','Interferences (EMI/ESI)');
INSERT INTO `ramstk_hazards` VALUES (40,'Control Systems','Lightning Strike');
INSERT INTO `ramstk_hazards` VALUES (41,'Control Systems','Moisture');
INSERT INTO `ramstk_hazards` VALUES (42,'Control Systems','Power Outage');
INSERT INTO `ramstk_hazards` VALUES (43,'Control Systems','Sneak Circuit');
INSERT INTO `ramstk_hazards` VALUES (44,'Control Systems','Sneak Software');
INSERT INTO `ramstk_hazards` VALUES (45,'Electrical','Burns');
INSERT INTO `ramstk_hazards` VALUES (46,'Electrical','Distribution Feedback');
INSERT INTO `ramstk_hazards` VALUES (47,'Electrical','Explosion (Arc)');
INSERT INTO `ramstk_hazards` VALUES (48,'Electrical','Explosion (Electrostatic)');
INSERT INTO `ramstk_hazards` VALUES (49,'Electrical','Overheating');
INSERT INTO `ramstk_hazards` VALUES (50,'Electrical','Power Outage');
INSERT INTO `ramstk_hazards` VALUES (51,'Electrical','Shock');
INSERT INTO `ramstk_hazards` VALUES (52,'Ergonomics','Fatigue');
INSERT INTO `ramstk_hazards` VALUES (53,'Ergonomics','Faulty/Inadequate Control/Readout Labeling');
INSERT INTO `ramstk_hazards` VALUES (54,'Ergonomics','Faulty Work Station Design');
INSERT INTO `ramstk_hazards` VALUES (55,'Ergonomics','Glare');
INSERT INTO `ramstk_hazards` VALUES (56,'Ergonomics','Inaccessibility');
INSERT INTO `ramstk_hazards` VALUES (57,'Ergonomics','Inadequate Control/Readout Differentiation');
INSERT INTO `ramstk_hazards` VALUES (58,'Ergonomics','Inadequate/Improper Illumination');
INSERT INTO `ramstk_hazards` VALUES (59,'Ergonomics','Inappropriate Control/Readout Location');
INSERT INTO `ramstk_hazards` VALUES (60,'Ergonomics','Nonexistent/Inadequate Kill Switches');
INSERT INTO `ramstk_hazards` VALUES (61,'Explosive Conditions','Explosive Dust Present');
INSERT INTO `ramstk_hazards` VALUES (62,'Explosive Conditions','Explosive Gas Present');
INSERT INTO `ramstk_hazards` VALUES (63,'Explosive Conditions','Explosive Liquid Present');
INSERT INTO `ramstk_hazards` VALUES (64,'Explosive Conditions','Explosive Propellant Present');
INSERT INTO `ramstk_hazards` VALUES (65,'Explosive Conditions','Explosive Vapor Present');
INSERT INTO `ramstk_hazards` VALUES (66,'Explosive Effects','Blast Overpressure');
INSERT INTO `ramstk_hazards` VALUES (67,'Explosive Effects','Mass Fire');
INSERT INTO `ramstk_hazards` VALUES (68,'Explosive Effects','Seismic Ground Wave');
INSERT INTO `ramstk_hazards` VALUES (69,'Explosive Effects','Thrown Fragments');
INSERT INTO `ramstk_hazards` VALUES (70,'Explosive Initiator','Chemical Contamination');
INSERT INTO `ramstk_hazards` VALUES (71,'Explosive Initiator','Electrostatic Discharge');
INSERT INTO `ramstk_hazards` VALUES (72,'Explosive Initiator','Friction');
INSERT INTO `ramstk_hazards` VALUES (73,'Explosive Initiator','Heat');
INSERT INTO `ramstk_hazards` VALUES (74,'Explosive Initiator','Impact/Shock');
INSERT INTO `ramstk_hazards` VALUES (75,'Explosive Initiator','Lightning');
INSERT INTO `ramstk_hazards` VALUES (76,'Explosive Initiator','Vibration');
INSERT INTO `ramstk_hazards` VALUES (77,'Explosive Initiator','Welding (Stray Current/Sparks)');
INSERT INTO `ramstk_hazards` VALUES (78,'Fire/Flammability','Fuel');
INSERT INTO `ramstk_hazards` VALUES (79,'Fire/Flammability','Ignition Source');
INSERT INTO `ramstk_hazards` VALUES (80,'Fire/Flammability','Oxidizer');
INSERT INTO `ramstk_hazards` VALUES (81,'Fire/Flammability','Propellant');
INSERT INTO `ramstk_hazards` VALUES (82,'Human Factors','Failure to Operate');
INSERT INTO `ramstk_hazards` VALUES (83,'Human Factors','Inadvertent Operation');
INSERT INTO `ramstk_hazards` VALUES (84,'Human Factors','Operated Too Long');
INSERT INTO `ramstk_hazards` VALUES (85,'Human Factors','Operated Too Briefly');
INSERT INTO `ramstk_hazards` VALUES (86,'Human Factors','Operation Early/Late');
INSERT INTO `ramstk_hazards` VALUES (87,'Human Factors','Operation Out of Sequence');
INSERT INTO `ramstk_hazards` VALUES (88,'Human Factors','Operator Error');
INSERT INTO `ramstk_hazards` VALUES (89,'Human Factors','Right Operation/Wrong Control');
INSERT INTO `ramstk_hazards` VALUES (90,'Ionizing Radiation','Alpha');
INSERT INTO `ramstk_hazards` VALUES (91,'Ionizing Radiation','Beta');
INSERT INTO `ramstk_hazards` VALUES (92,'Ionizing Radiation','Gamma');
INSERT INTO `ramstk_hazards` VALUES (93,'Ionizing Radiation','Neutron');
INSERT INTO `ramstk_hazards` VALUES (94,'Ionizing Radiation','X-Ray');
INSERT INTO `ramstk_hazards` VALUES (95,'Leaks/Spills','Asphyxiating');
INSERT INTO `ramstk_hazards` VALUES (96,'Leaks/Spills','Corrosive');
INSERT INTO `ramstk_hazards` VALUES (97,'Leaks/Spills','Flammable');
INSERT INTO `ramstk_hazards` VALUES (98,'Leaks/Spills','Flooding');
INSERT INTO `ramstk_hazards` VALUES (99,'Leaks/Spills','Gases/Vapors');
INSERT INTO `ramstk_hazards` VALUES (100,'Leaks/Spills','Irritating Dusts');
INSERT INTO `ramstk_hazards` VALUES (101,'Leaks/Spills','Liquids/Cryogens');
INSERT INTO `ramstk_hazards` VALUES (102,'Leaks/Spills','Odorous');
INSERT INTO `ramstk_hazards` VALUES (103,'Leaks/Spills','Pathogenic');
INSERT INTO `ramstk_hazards` VALUES (104,'Leaks/Spills','Radiation Sources');
INSERT INTO `ramstk_hazards` VALUES (105,'Leaks/Spills','Reactive');
INSERT INTO `ramstk_hazards` VALUES (106,'Leaks/Spills','Run Off');
INSERT INTO `ramstk_hazards` VALUES (107,'Leaks/Spills','Slippery');
INSERT INTO `ramstk_hazards` VALUES (108,'Leaks/Spills','Toxic');
INSERT INTO `ramstk_hazards` VALUES (109,'Leaks/Spills','Vapor Propagation');
INSERT INTO `ramstk_hazards` VALUES (110,'Mechanical','Crushing Surfaces');
INSERT INTO `ramstk_hazards` VALUES (111,'Mechanical','Ejected Parts/Fragments');
INSERT INTO `ramstk_hazards` VALUES (112,'Mechanical','Lifting Weights');
INSERT INTO `ramstk_hazards` VALUES (113,'Mechanical','Pinch Points');
INSERT INTO `ramstk_hazards` VALUES (114,'Mechanical','Reciprocating Equipment');
INSERT INTO `ramstk_hazards` VALUES (115,'Mechanical','Rotating Equipment');
INSERT INTO `ramstk_hazards` VALUES (116,'Mechanical','Sharp Edges/Points');
INSERT INTO `ramstk_hazards` VALUES (117,'Mechanical','Stability/Topping Potential');
INSERT INTO `ramstk_hazards` VALUES (118,'Mission Phasing','Activation');
INSERT INTO `ramstk_hazards` VALUES (119,'Mission Phasing','Calibration');
INSERT INTO `ramstk_hazards` VALUES (120,'Mission Phasing','Checkout');
INSERT INTO `ramstk_hazards` VALUES (121,'Mission Phasing','Coupling/Uncoupling');
INSERT INTO `ramstk_hazards` VALUES (122,'Mission Phasing','Delivery');
INSERT INTO `ramstk_hazards` VALUES (123,'Mission Phasing','Diagnosis/Trouble Shooting');
INSERT INTO `ramstk_hazards` VALUES (124,'Mission Phasing','Emergency Start');
INSERT INTO `ramstk_hazards` VALUES (125,'Mission Phasing','Installation');
INSERT INTO `ramstk_hazards` VALUES (126,'Mission Phasing','Load Change');
INSERT INTO `ramstk_hazards` VALUES (127,'Mission Phasing','Maintenance');
INSERT INTO `ramstk_hazards` VALUES (128,'Mission Phasing','Normal Operation');
INSERT INTO `ramstk_hazards` VALUES (129,'Mission Phasing','Shake Down');
INSERT INTO `ramstk_hazards` VALUES (130,'Mission Phasing','Shutdown Emergency');
INSERT INTO `ramstk_hazards` VALUES (131,'Mission Phasing','Standard Shutdown');
INSERT INTO `ramstk_hazards` VALUES (132,'Mission Phasing','Standard Start');
INSERT INTO `ramstk_hazards` VALUES (133,'Mission Phasing','Stressed Operation');
INSERT INTO `ramstk_hazards` VALUES (134,'Mission Phasing','Transport');
INSERT INTO `ramstk_hazards` VALUES (135,'Nonionizing Radiation','Infrared');
INSERT INTO `ramstk_hazards` VALUES (136,'Nonionizing Radiation','Laser');
INSERT INTO `ramstk_hazards` VALUES (137,'Nonionizing Radiation','Microwave');
INSERT INTO `ramstk_hazards` VALUES (138,'Nonionizing Radiation','Ultraviolet');
INSERT INTO `ramstk_hazards` VALUES (139,'Physiological','Allergens');
INSERT INTO `ramstk_hazards` VALUES (140,'Physiological','Asphyxiants');
INSERT INTO `ramstk_hazards` VALUES (141,'Physiological','Baropressure Extremes');
INSERT INTO `ramstk_hazards` VALUES (142,'Physiological','Carcinogens');
INSERT INTO `ramstk_hazards` VALUES (143,'Physiological','Cryogens');
INSERT INTO `ramstk_hazards` VALUES (144,'Physiological','Fatigue');
INSERT INTO `ramstk_hazards` VALUES (145,'Physiological','Irritants');
INSERT INTO `ramstk_hazards` VALUES (146,'Physiological','Lifted Weights');
INSERT INTO `ramstk_hazards` VALUES (147,'Physiological','Mutagens');
INSERT INTO `ramstk_hazards` VALUES (148,'Physiological','Noise');
INSERT INTO `ramstk_hazards` VALUES (149,'Physiological','Nuisance Dust/Odors');
INSERT INTO `ramstk_hazards` VALUES (150,'Physiological','Pathogens');
INSERT INTO `ramstk_hazards` VALUES (151,'Physiological','Temperature Extremes');
INSERT INTO `ramstk_hazards` VALUES (152,'Physiological','Teratogens');
INSERT INTO `ramstk_hazards` VALUES (153,'Physiological','Toxins');
INSERT INTO `ramstk_hazards` VALUES (154,'Physiological','Vibration (Raynaud''s Syndrome)');
INSERT INTO `ramstk_hazards` VALUES (155,'Pneumatic/Hydraulic','Backflow');
INSERT INTO `ramstk_hazards` VALUES (156,'Pneumatic/Hydraulic','Blown Objects');
INSERT INTO `ramstk_hazards` VALUES (157,'Pneumatic/Hydraulic','Crossflow');
INSERT INTO `ramstk_hazards` VALUES (158,'Pneumatic/Hydraulic','Dynamic Pressure Loading');
INSERT INTO `ramstk_hazards` VALUES (159,'Pneumatic/Hydraulic','Hydraulic Ram');
INSERT INTO `ramstk_hazards` VALUES (160,'Pneumatic/Hydraulic','Implosion');
INSERT INTO `ramstk_hazards` VALUES (161,'Pneumatic/Hydraulic','Inadvertent Release');
INSERT INTO `ramstk_hazards` VALUES (162,'Pneumatic/Hydraulic','Miscalibrated Relief Device');
INSERT INTO `ramstk_hazards` VALUES (163,'Pneumatic/Hydraulic','Mislocated Relief Device');
INSERT INTO `ramstk_hazards` VALUES (164,'Pneumatic/Hydraulic','Overpressurization');
INSERT INTO `ramstk_hazards` VALUES (165,'Pneumatic/Hydraulic','Pipe/Hose Whip');
INSERT INTO `ramstk_hazards` VALUES (166,'Pneumatic/Hydraulic','Pipe/Vessel/Duct Rupture');
INSERT INTO `ramstk_hazards` VALUES (167,'Pneumatic/Hydraulic','Relief Pressure Improperly Set');
INSERT INTO `ramstk_hazards` VALUES (168,'Thermal','Altered Structural Properties (e.g., Embrittlement)');
INSERT INTO `ramstk_hazards` VALUES (169,'Thermal','Confined Gas/Liquid');
INSERT INTO `ramstk_hazards` VALUES (170,'Thermal','Elevated Flammability');
INSERT INTO `ramstk_hazards` VALUES (171,'Thermal','Elevated Reactivity');
INSERT INTO `ramstk_hazards` VALUES (172,'Thermal','Elevated Volatility');
INSERT INTO `ramstk_hazards` VALUES (173,'Thermal','Freezing');
INSERT INTO `ramstk_hazards` VALUES (174,'Thermal','Heat Source/Sink');
INSERT INTO `ramstk_hazards` VALUES (175,'Thermal','Hot/Cold Surface Burns');
INSERT INTO `ramstk_hazards` VALUES (176,'Thermal','Humidity/Moisture');
INSERT INTO `ramstk_hazards` VALUES (177,'Thermal','Pressure Evaluation');
INSERT INTO `ramstk_hazards` VALUES (178,'Unannunciated Utility Outages','Air Conditioning');
INSERT INTO `ramstk_hazards` VALUES (179,'Unannunciated Utility Outages','Compressed Air/Gas');
INSERT INTO `ramstk_hazards` VALUES (180,'Unannunciated Utility Outages','Electricity');
INSERT INTO `ramstk_hazards` VALUES (181,'Unannunciated Utility Outages','Exhaust');
INSERT INTO `ramstk_hazards` VALUES (182,'Unannunciated Utility Outages','Fuel');
INSERT INTO `ramstk_hazards` VALUES (183,'Unannunciated Utility Outages','Heating/Cooling');
INSERT INTO `ramstk_hazards` VALUES (184,'Unannunciated Utility Outages','Lubrication Drains/Sumps');
INSERT INTO `ramstk_hazards` VALUES (185,'Unannunciated Utility Outages','Steam');
INSERT INTO `ramstk_hazards` VALUES (186,'Unannunciated Utility Outages','Ventilation');
DROP TABLE IF EXISTS `ramstk_group`;
CREATE TABLE IF NOT EXISTS `ramstk_group` (
	`fld_group_id`	INTEGER NOT NULL,
	`fld_description`	VARCHAR ( 512 ),
	`fld_group_type`	VARCHAR ( 256 ),
	PRIMARY KEY(`fld_group_id`)
);
INSERT INTO `ramstk_group` VALUES (1,'Engineering, Design','workgroup');
INSERT INTO `ramstk_group` VALUES (2,'Engineering, Logistics Support','workgroup');
INSERT INTO `ramstk_group` VALUES (3,'Engineering, Maintainability','workgroup');
INSERT INTO `ramstk_group` VALUES (4,'Engineering, Reliability','workgroup');
INSERT INTO `ramstk_group` VALUES (5,'Engineering, Safety','workgroup');
INSERT INTO `ramstk_group` VALUES (6,'Engineering, Software','workgroup');
INSERT INTO `ramstk_group` VALUES (7,'Reliability','affinity');
INSERT INTO `ramstk_group` VALUES (8,'Durability','affinity');
INSERT INTO `ramstk_group` VALUES (9,'Cost','affinity');
DROP TABLE IF EXISTS `ramstk_failure_mode`;
CREATE TABLE IF NOT EXISTS `ramstk_failure_mode` (
	`fld_category_id`	INTEGER NOT NULL,
	`fld_subcategory_id`	INTEGER NOT NULL,
	`fld_failuremode_id`	INTEGER NOT NULL,
	`fld_description`	VARCHAR ( 512 ),
	`fld_mode_ratio`	FLOAT,
	`fld_source`	VARCHAR ( 128 ),
	FOREIGN KEY(`fld_subcategory_id`) REFERENCES `ramstk_subcategory`(`fld_subcategory_id`),
	PRIMARY KEY(`fld_failuremode_id`),
	FOREIGN KEY(`fld_category_id`) REFERENCES `ramstk_category`(`fld_category_id`)
);
INSERT INTO `ramstk_failure_mode` VALUES (3,24,3,'Parameter Change',0.2,'FMD-97');
DROP TABLE IF EXISTS `ramstk_condition`;
CREATE TABLE IF NOT EXISTS `ramstk_condition` (
	`fld_condition_id`	INTEGER NOT NULL,
	`fld_description`	VARCHAR ( 512 ),
	`fld_condition_type`	VARCHAR ( 256 ),
	PRIMARY KEY(`fld_condition_id`)
);
INSERT INTO `ramstk_condition` VALUES (1,'Cavitation','operating');
INSERT INTO `ramstk_condition` VALUES (2,'Cold Start','operating');
INSERT INTO `ramstk_condition` VALUES (3,'Contaminated Oil','operating');
INSERT INTO `ramstk_condition` VALUES (4,'Cyclic Loading, Low Cycle','operating');
INSERT INTO `ramstk_condition` VALUES (5,'Cyclic Loading, High Cycle','operating');
INSERT INTO `ramstk_condition` VALUES (6,'Emergency Stop','operating');
INSERT INTO `ramstk_condition` VALUES (7,'Full Load','operating');
INSERT INTO `ramstk_condition` VALUES (8,'High Idle','operating');
INSERT INTO `ramstk_condition` VALUES (9,'Hot Shutdown','operating');
INSERT INTO `ramstk_condition` VALUES (10,'Idle','operating');
INSERT INTO `ramstk_condition` VALUES (11,'Low End Torque','operating');
INSERT INTO `ramstk_condition` VALUES (12,'Mechanical Shock','operating');
INSERT INTO `ramstk_condition` VALUES (13,'Oil Pressure Fluctuations','operating');
INSERT INTO `ramstk_condition` VALUES (14,'Overload','operating');
INSERT INTO `ramstk_condition` VALUES (15,'Overspeed','operating');
INSERT INTO `ramstk_condition` VALUES (16,'Pressure Pulsations','operating');
INSERT INTO `ramstk_condition` VALUES (17,'Short Term Overload','operating');
INSERT INTO `ramstk_condition` VALUES (18,'Start-Stop','operating');
INSERT INTO `ramstk_condition` VALUES (19,'System Cool Down','operating');
INSERT INTO `ramstk_condition` VALUES (20,'System Warm Up','operating');
INSERT INTO `ramstk_condition` VALUES (21,'Thermal Cycling','operating');
INSERT INTO `ramstk_condition` VALUES (22,'Vibration','operating');
INSERT INTO `ramstk_condition` VALUES (23,'Abrasion','environmental');
INSERT INTO `ramstk_condition` VALUES (24,'Acceleration','environmental');
INSERT INTO `ramstk_condition` VALUES (25,'Corona','environmental');
INSERT INTO `ramstk_condition` VALUES (26,'Contamination, Chemicals','environmental');
INSERT INTO `ramstk_condition` VALUES (27,'Contamination, Dirt/Dust','environmental');
INSERT INTO `ramstk_condition` VALUES (28,'Contamination, Salt Spray','environmental');
INSERT INTO `ramstk_condition` VALUES (29,'Electrostatic Discharge','environmental');
INSERT INTO `ramstk_condition` VALUES (30,'Fungus','environmental');
INSERT INTO `ramstk_condition` VALUES (31,'Gas, Ionized','environmental');
INSERT INTO `ramstk_condition` VALUES (32,'Geomagnetics','environmental');
INSERT INTO `ramstk_condition` VALUES (33,'Humidity','environmental');
INSERT INTO `ramstk_condition` VALUES (34,'Ozone','environmental');
INSERT INTO `ramstk_condition` VALUES (35,'Pressure, Atmospheric','environmental');
INSERT INTO `ramstk_condition` VALUES (36,'Pressure','environmental');
INSERT INTO `ramstk_condition` VALUES (37,'Radiation, Alpha','environmental');
INSERT INTO `ramstk_condition` VALUES (38,'Radiation, Electromagnetic','environmental');
INSERT INTO `ramstk_condition` VALUES (39,'Radiation, Gamma','environmental');
INSERT INTO `ramstk_condition` VALUES (40,'Radiation, Neutron','environmental');
INSERT INTO `ramstk_condition` VALUES (41,'Radiation, Solar','environmental');
INSERT INTO `ramstk_condition` VALUES (42,'Shock, Mechanical','environmental');
INSERT INTO `ramstk_condition` VALUES (43,'Shock, Thermal','environmental');
INSERT INTO `ramstk_condition` VALUES (44,'Temperature','environmental');
INSERT INTO `ramstk_condition` VALUES (45,'Thermal Cycles','environmental');
INSERT INTO `ramstk_condition` VALUES (46,'Vibration, Acoustic','environmental');
INSERT INTO `ramstk_condition` VALUES (47,'Vibration, Mechanical','environmental');
INSERT INTO `ramstk_condition` VALUES (48,'Weather, Fog','environmental');
INSERT INTO `ramstk_condition` VALUES (49,'Weather, Freezing Rain','environmental');
INSERT INTO `ramstk_condition` VALUES (50,'Weather, Frost','environmental');
INSERT INTO `ramstk_condition` VALUES (51,'Weather, Hail','environmental');
INSERT INTO `ramstk_condition` VALUES (52,'Weather, Ice','environmental');
INSERT INTO `ramstk_condition` VALUES (53,'Weather, Rain','environmental');
INSERT INTO `ramstk_condition` VALUES (54,'Weather, Sleet','environmental');
INSERT INTO `ramstk_condition` VALUES (55,'Weather, Snow','environmental');
INSERT INTO `ramstk_condition` VALUES (56,'Weather, Wind','environmental');
DROP TABLE IF EXISTS `ramstk_category`;
CREATE TABLE IF NOT EXISTS `ramstk_category` (
	`fld_category_id`	INTEGER NOT NULL,
	`fld_name`	VARCHAR ( 256 ),
	`fld_description`	VARCHAR ( 512 ),
	`fld_category_type`	VARCHAR ( 256 ),
	`fld_value`	INTEGER,
	`fld_harsh_ir_limit`	FLOAT,
	`fld_mild_ir_limit`	FLOAT,
	`fld_harsh_pr_limit`	FLOAT,
	`fld_mild_pr_limit`	FLOAT,
	`fld_harsh_vr_limit`	FLOAT,
	`fld_mild_vr_limit`	FLOAT,
	`fld_harsh_deltat_limit`	FLOAT,
	`fld_mild_deltat_limit`	FLOAT,
	`fld_harsh_maxt_limit`	FLOAT,
	`fld_mild_maxt_limit`	FLOAT,
	PRIMARY KEY(`fld_category_id`)
);
INSERT INTO `ramstk_category` VALUES (1,'IC','Integrated Circuit','hardware',1,0.8,0.9,1.0,1.0,1.0,1.0,0.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (2,'SEMI','Semiconductor','hardware',1,1.0,1.0,0.7,0.9,1.0,1.0,0.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (3,'RES','Resistor','hardware',1,1.0,1.0,0.5,0.9,1.0,1.0,0.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (4,'CAP','Capacitor','hardware',1,1.0,1.0,1.0,1.0,0.6,0.9,10.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (5,'IND','Inductive Device','hardware',1,0.6,0.9,1.0,1.0,0.5,0.9,15.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (6,'REL','Relay','hardware',1,0.75,0.9,1.0,1.0,1.0,1.0,0.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (7,'SW','Switching Device','hardware',1,0.75,0.9,1.0,1.0,1.0,1.0,0.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (8,'CONN','Connection','hardware',1,0.7,0.9,1.0,1.0,0.7,0.9,25.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (9,'MET','Meter','hardware',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (10,'MISC','Miscellaneous','hardware',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,125.0,125.0);
INSERT INTO `ramstk_category` VALUES (11,'INS','Insignificant','risk',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (12,'SLT','Slight','risk',2,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (13,'LOW','Low','risk',3,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (14,'MED','Medium','risk',4,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (15,'HI','High','risk',5,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (16,'MAJ','Major','risk',6,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (17,'Batch (General)','Can be run as a normal batch job and makes no unusual hardware or input-output actions (e.g., payroll program and wind tunnel data analysis program).  Small, throwaway programs for preliminary analysis also fit in this category.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (18,'Event Control','Does realtime processing of data resulting from external events. An example might be a computer program that processes telemetry data.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (19,'Process Control','Receives data from an external source and issues commands to that source to control its actions based on the received data.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (20,'Procedure Control','Controls other software; for example, an operating system that controls execution of time-shared and batch computer programs.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (21,'Navigation','Does computation and modeling to computer information required to guide an airplane from point of origin to destination.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (22,'Flight Dynamics','Uses the functions computed by navigation software and augmented by control theory to control the entire flight of an aircraft.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (23,'Orbital Dynamics','Resembles navigation and flight dynamics software, but has the additional complexity required by orbital navigation, such as a more complex reference system and the inclusion of gravitational effects of other heavenly bodies.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (24,'Message Processing','Handles input and output mnessages. processing the text or information contained therein.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (25,'Diagnostic Software','Used to detect and isolate hardware errors in the computer in which it resides or in other hardware that can communicate with the computer.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (26,'Sensor and Signal Processing','Similar to that of message processing, except that it required greater processing, analyzing, and transforming the input into a usable data processing format.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (27,'Simulation','Used to simulate and environment ieseion situation. other heavradlwuaatrieo,n aonfd a icnopmutps uftreo mpr otghreasme nt o enable a more realistic or a piece of hardware.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (28,'Database Management','Manages the storage and access of (typically large) groups of data. Such software can also often prepare reports in user-defined formats, based on the contents of the database.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (29,'Data Acquisition','Receives information in real-time and stores it in some form suitable format for later processing, for example, software that receives data from a space probe ,and files.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (30,'Data Presentation','Formats and transforms data, as necessary, for convenient and understandable displays for humans.  Typically, such displays would be for some screen presentation.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (31,'Decision and Planning Aids','Uses artificial intelligence techniques to provide an expert system to evaluate data and provide additional information and consideration for decision and policy makers.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (32,'Pattern and Image Processing','Used for computer image generation and processing.  Such software may analyze terrain data and generate images based on stored data.','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (33,'Computer System Software','Provides services to operational computer programs (i.e., problem oriented).','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (34,'Software Development Tools','Provides services to aid in the development of software (e.g., compilers, assemblers, static and dynamic analyzers).','software',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (35,'HW','Hardware','incident',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (36,'SW','Software','incident',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (37,'PROC','Process','incident',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (38,'ENGD','Engineering, Design','action',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (39,'ENGR','Engineering, Reliability','action',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (40,'ENGS','Engineering, Systems','action',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (41,'MAN','Manufacturing','action',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (42,'TEST','Test','action',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
INSERT INTO `ramstk_category` VALUES (43,'VANDV','Verification & Validation','action',1,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0);
COMMIT;
