/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `reliafreecom` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `reliafreecom`;

--
-- Table structure for table `tbl_active_environs`
--

DROP TABLE IF EXISTS `tbl_active_environs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_active_environs` (
  `fld_subcategory_id` int(11) NOT NULL,
  `fld_calculation_model_id` int(11) NOT NULL COMMENT 'Hazard rate model key value.',
  `fld_active_environ_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Active environment key value.',
  `fld_active_environ_code` varchar(4) NOT NULL COMMENT 'Active environment noun code.',
  `fld_active_environ_noun` varchar(64) NOT NULL COMMENT 'Active environment noun name.',
  `fld_pi_e` float NOT NULL DEFAULT '1',
  PRIMARY KEY (`fld_subcategory_id`,`fld_calculation_model_id`,`fld_active_environ_id`),
  KEY `fld_active_environ_id` (`fld_active_environ_id`),
  KEY `fld_calculation_model_id` (`fld_calculation_model_id`),
  CONSTRAINT `tbl_active_environs_ibfk_1` FOREIGN KEY (`fld_calculation_model_id`) REFERENCES `tbl_calculation_model` (`fld_model_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tbl_active_environs_ibfk_2` FOREIGN KEY (`fld_subcategory_id`) REFERENCES `tbl_subcategory` (`fld_subcategory_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='Table containing active environments for each hazard rate mo';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_active_environs`
--

LOCK TABLES `tbl_active_environs` WRITE;
/*!40000 ALTER TABLE `tbl_active_environs` DISABLE KEYS */;
INSERT INTO `tbl_active_environs` VALUES (1,1,1,'GB','Ground, Benign',0.5),(1,1,2,'GF','Ground, Fixed',2),(1,1,3,'GM','Ground, Mobile',4),(1,1,4,'NS','Naval, Sheltered',4),(1,1,5,'NU','Naval, Unsheltered',6),(1,1,6,'AIC','Airborne, Inhabited, Cargo',4),(1,1,7,'AIF','Airborne, Inhabited, Fighter',5),(1,1,8,'AUC','Airborne, Uninhabited, Cargo',5),(1,1,9,'AUF','Airborne, Uninhabited, Fighter',8),(1,1,10,'ARW','Airborne, Rotary Wing',8),(1,1,11,'SF','Space, Flight',0.5),(1,1,12,'MF','Missile, Flight',5),(1,1,13,'ML','Missile, Launch',12),(1,1,14,'CL','Cannon, Launch',220);
/*!40000 ALTER TABLE `tbl_active_environs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_allocation_models`
--

DROP TABLE IF EXISTS `tbl_allocation_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_allocation_models` (
  `fld_allocation_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_allocation_noun` varchar(64) NOT NULL,
  PRIMARY KEY (`fld_allocation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_allocation_models`
--

LOCK TABLES `tbl_allocation_models` WRITE;
/*!40000 ALTER TABLE `tbl_allocation_models` DISABLE KEYS */;
INSERT INTO `tbl_allocation_models` VALUES (1,'Equal Apportionment'),(2,'AGREE Apportionment'),(3,'ARINC Apportionment'),(4,'Feasibility of Objectives'),(5,'Repairable Systems Apportionment');
/*!40000 ALTER TABLE `tbl_allocation_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_calculation_model`
--

DROP TABLE IF EXISTS `tbl_calculation_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_calculation_model` (
  `fld_model_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_model_noun` char(50) DEFAULT NULL,
  PRIMARY KEY (`fld_model_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_calculation_model`
--

LOCK TABLES `tbl_calculation_model` WRITE;
/*!40000 ALTER TABLE `tbl_calculation_model` DISABLE KEYS */;
INSERT INTO `tbl_calculation_model` VALUES (1,'MIL-HDBK-217F Stress'),(2,'MIL-HDBK-217F Parts Count'),(3,'MIL-HDBK-217FN1 Stress'),(4,'MIL-HDBK-217FN1 Parts Count'),(5,'MIL-HDBK-217FN2 Stress'),(6,'MIL-HDBK-217FN2 Parts Count'),(7,'Mechanical');
/*!40000 ALTER TABLE `tbl_calculation_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_category`
--

DROP TABLE IF EXISTS `tbl_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_category` (
  `fld_category_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identification number for part category.',
  `fld_category_noun` char(64) DEFAULT NULL COMMENT 'Noun name of part category.',
  PRIMARY KEY (`fld_category_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_category`
--

LOCK TABLES `tbl_category` WRITE;
/*!40000 ALTER TABLE `tbl_category` DISABLE KEYS */;
INSERT INTO `tbl_category` VALUES (1,'Integrated Circuit'),(2,'Semiconductor'),(3,'Resistor'),(4,'Capacitor'),(5,'Inductive Device'),(6,'Relay'),(7,'Switching Device'),(8,'Connection'),(9,'Meter'),(10,'Miscellaneous');
/*!40000 ALTER TABLE `tbl_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_chargeability`
--

DROP TABLE IF EXISTS `tbl_chargeability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_chargeability` (
  `fld_chargeability_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_chargeability_q` varchar(512) DEFAULT '',
  `fld_order` int(11) NOT NULL DEFAULT '0',
  `fld_y_next` int(11) NOT NULL DEFAULT '82',
  `fld_n_next` int(11) NOT NULL DEFAULT '82',
  PRIMARY KEY (`fld_chargeability_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_cost_type`
--

DROP TABLE IF EXISTS `tbl_cost_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_cost_type` (
  `fld_cost_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_cost_type_noun` varchar(64) NOT NULL,
  PRIMARY KEY (`fld_cost_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_cost_type`
--

LOCK TABLES `tbl_cost_type` WRITE;
/*!40000 ALTER TABLE `tbl_cost_type` DISABLE KEYS */;
INSERT INTO `tbl_cost_type` VALUES (1,'Calculated'),(2,'Specified');
/*!40000 ALTER TABLE `tbl_cost_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_development_environment`
--

DROP TABLE IF EXISTS `tbl_development_environment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_development_environment` (
  `fld_development_id` int(11) NOT NULL DEFAULT '0',
  `fld_development_desc` varchar(32) DEFAULT NULL,
  `fld_do` float DEFAULT NULL,
  PRIMARY KEY (`fld_development_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_development_environment`
--

LOCK TABLES `tbl_development_environment` WRITE;
/*!40000 ALTER TABLE `tbl_development_environment` DISABLE KEYS */;
INSERT INTO `tbl_development_environment` VALUES (0,'Organic',0.76),(1,'Semi-Detached',1),(2,'Embedded',1.3);
/*!40000 ALTER TABLE `tbl_development_environment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_development_phase`
--

DROP TABLE IF EXISTS `tbl_development_phase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_development_phase` (
  `fld_phase_id` int(11) NOT NULL DEFAULT '0',
  `fld_phase_desc` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`fld_phase_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_development_phase`
--

LOCK TABLES `tbl_development_phase` WRITE;
/*!40000 ALTER TABLE `tbl_development_phase` DISABLE KEYS */;
INSERT INTO `tbl_development_phase` VALUES (0,'Software Requirements Review (SRR)'),(1,'Software Requirements Analysis (SSR)'),(2,'Preliminary Design Review (PDR)'),(3,'Critical Design Review (CDR)'),(4,'Test Readiness Review (TRR)');
/*!40000 ALTER TABLE `tbl_development_phase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_distributions`
--

DROP TABLE IF EXISTS `tbl_distributions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_distributions` (
  `fld_distribution_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_distribution_noun` varchar(64) NOT NULL,
  PRIMARY KEY (`fld_distribution_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_distributions`
--

LOCK TABLES `tbl_distributions` WRITE;
/*!40000 ALTER TABLE `tbl_distributions` DISABLE KEYS */;
INSERT INTO `tbl_distributions` VALUES (1,'Constant Probability'),(2,'Exponential'),(3,'LogNormal'),(4,'Uniform'),(5,'Weibull');
/*!40000 ALTER TABLE `tbl_distributions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_dormant_environs`
--

DROP TABLE IF EXISTS `tbl_dormant_environs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_dormant_environs` (
  `fld_model_id` int(11) NOT NULL,
  `fld_dormant_environ_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_dormant_environ_noun` varchar(64) NOT NULL,
  PRIMARY KEY (`fld_model_id`,`fld_dormant_environ_id`),
  KEY `fld_dormant_environ_id` (`fld_dormant_environ_id`),
  CONSTRAINT `tbl_dormant_environs_ibfk_1` FOREIGN KEY (`fld_model_id`) REFERENCES `tbl_calculation_model` (`fld_model_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_dormant_environs`
--

LOCK TABLES `tbl_dormant_environs` WRITE;
/*!40000 ALTER TABLE `tbl_dormant_environs` DISABLE KEYS */;
INSERT INTO `tbl_dormant_environs` VALUES (1,1,'Ground'),(1,2,'Naval'),(1,3,'Airborne');
/*!40000 ALTER TABLE `tbl_dormant_environs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_hr_type`
--

DROP TABLE IF EXISTS `tbl_hr_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_hr_type` (
  `fld_hr_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_hr_type_noun` varchar(64) NOT NULL,
  PRIMARY KEY (`fld_hr_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_hr_type`
--

LOCK TABLES `tbl_hr_type` WRITE;
/*!40000 ALTER TABLE `tbl_hr_type` DISABLE KEYS */;
INSERT INTO `tbl_hr_type` VALUES (1,'Assessed'),(2,'Specified, Hazard Rate'),(3,'Specified, MTBF');
/*!40000 ALTER TABLE `tbl_hr_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_manufacturers`
--

DROP TABLE IF EXISTS `tbl_manufacturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_manufacturers` (
  `fld_manufacturers_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_manufacturers_noun` varchar(128) DEFAULT '',
  `fld_location` varchar(45) DEFAULT '',
  `fld_cage_code` varchar(45) DEFAULT '',
  PRIMARY KEY (`fld_manufacturers_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_manufacturers`
--

LOCK TABLES `tbl_manufacturers` WRITE;
/*!40000 ALTER TABLE `tbl_manufacturers` DISABLE KEYS */;
INSERT INTO `tbl_manufacturers` VALUES (1,'Sprague','New Hampshire','13606'),(2,'Xilinx','',''),(3,'National Semiconductor','California','27014');
/*!40000 ALTER TABLE `tbl_manufacturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_measurement_units`
--

DROP TABLE IF EXISTS `tbl_measurement_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_measurement_units` (
  `fld_measurement_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_measurement_code` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`fld_measurement_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_measurement_units`
--

LOCK TABLES `tbl_measurement_units` WRITE;
/*!40000 ALTER TABLE `tbl_measurement_units` DISABLE KEYS */;
INSERT INTO `tbl_measurement_units` VALUES (1,'lbf'),(2,'hours');
/*!40000 ALTER TABLE `tbl_measurement_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_mttr_type`
--

DROP TABLE IF EXISTS `tbl_mttr_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_mttr_type` (
  `fld_mttr_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_mttr_type_noun` varchar(64) NOT NULL,
  PRIMARY KEY (`fld_mttr_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_mttr_type`
--

LOCK TABLES `tbl_mttr_type` WRITE;
/*!40000 ALTER TABLE `tbl_mttr_type` DISABLE KEYS */;
INSERT INTO `tbl_mttr_type` VALUES (1,'Assessed'),(2,'Specified');
/*!40000 ALTER TABLE `tbl_mttr_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_relevency`
--

DROP TABLE IF EXISTS `tbl_relevency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_relevency` (
  `fld_relevency_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_relevency_q` varchar(512) DEFAULT '',
  `fld_order` int(11) NOT NULL DEFAULT '0',
  `fld_y_next` int(11) NOT NULL DEFAULT '82',
  `fld_n_next` int(11) NOT NULL DEFAULT '82',
  PRIMARY KEY (`fld_relevency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_requirement_type`
--

DROP TABLE IF EXISTS `tbl_requirement_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_requirement_type` (
  `fld_requirement_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_requirement_type_desc` varchar(32) DEFAULT NULL,
  `fld_requirement_type_code` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`fld_requirement_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_requirement_type`
--

LOCK TABLES `tbl_requirement_type` WRITE;
/*!40000 ALTER TABLE `tbl_requirement_type` DISABLE KEYS */;
INSERT INTO `tbl_requirement_type` VALUES (1,'MARKETING','MKT'),(2,'FINANCIAL','FIN'),(3,'REGULATORY','REG'),(4,'PERFORMANCE','PRF'),(5,'RELIABILITY','REL'),(6,'SAFETY','SAF'),(7,'MAINTAINABILITY','MNT');
/*!40000 ALTER TABLE `tbl_requirement_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_risk_category`
--

DROP TABLE IF EXISTS `tbl_risk_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_risk_category` (
  `fld_category_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_category_noun` varchar(64) NOT NULL,
  `fld_category_value` int(11) DEFAULT '0',
  PRIMARY KEY (`fld_category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_risk_category`
--

LOCK TABLES `tbl_risk_category` WRITE;
/*!40000 ALTER TABLE `tbl_risk_category` DISABLE KEYS */;
INSERT INTO `tbl_risk_category` VALUES (0,'Category I',0),(1,'Category II',1),(2,'Category III',2),(3,'Category IV',3);
/*!40000 ALTER TABLE `tbl_risk_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_software_application`
--

DROP TABLE IF EXISTS `tbl_software_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_software_application` (
  `fld_application_id` int(11) NOT NULL DEFAULT '0',
  `fld_application_desc` varchar(32) DEFAULT NULL,
  `fld_fault_density` float DEFAULT NULL,
  `fld_transformation_ratio` float DEFAULT NULL,
  PRIMARY KEY (`fld_application_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_software_application`
--

LOCK TABLES `tbl_software_application` WRITE;
/*!40000 ALTER TABLE `tbl_software_application` DISABLE KEYS */;
INSERT INTO `tbl_software_application` VALUES (0,'Airborne',0.0128,6.28),(1,'Strategic',0.0092,1.2),(2,'Tactical',0.0078,13.8),(3,'Process Control',0.0018,3.8),(4,'Production Center',0.0085,23),(5,'Developmental',0.0123,132.6);
/*!40000 ALTER TABLE `tbl_software_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_software_level`
--

DROP TABLE IF EXISTS `tbl_software_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_software_level` (
  `fld_level_id` int(11) NOT NULL DEFAULT '0',
  `fld_level_desc` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`fld_level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_software_level`
--

LOCK TABLES `tbl_software_level` WRITE;
/*!40000 ALTER TABLE `tbl_software_level` DISABLE KEYS */;
INSERT INTO `tbl_software_level` VALUES (0,'Software System'),(1,'Computer Software Configuration Item (CSCI)'),(2,'Software Unit');
/*!40000 ALTER TABLE `tbl_software_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_subcategory`
--

DROP TABLE IF EXISTS `tbl_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_subcategory` (
  `fld_category_id` int(11) NOT NULL COMMENT 'Identification number for part category.',
  `fld_subcategory_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identification number for part subcategory.',
  `fld_subcategory_noun` varchar(64) DEFAULT NULL COMMENT 'Noun name of part subcategory.',
  PRIMARY KEY (`fld_category_id`,`fld_subcategory_id`),
  KEY `fld_subcategory_id` (`fld_subcategory_id`),
  CONSTRAINT `tbl_subcategory_ibfk_1` FOREIGN KEY (`fld_category_id`) REFERENCES `tbl_category` (`fld_category_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_subcategory`
--

LOCK TABLES `tbl_subcategory` WRITE;
/*!40000 ALTER TABLE `tbl_subcategory` DISABLE KEYS */;
INSERT INTO `tbl_subcategory` VALUES (1,1,'Linear'),(1,2,'Logic'),(1,3,'PAL, PLA'),(1,4,'Microprocessor, Microcontroller'),(1,5,'Memory, ROM'),(1,6,'Memory, EEPROM'),(1,7,'Memory, DRAM'),(1,8,'Memory, SRAM'),(1,9,'GaAs Digital'),(1,10,'GaAs MMIC'),(1,11,'VHSIC, VLSI'),(2,12,'Diode, Low Frequency'),(2,13,'Diode, High Frequency'),(2,14,'Transistor, Low Frequency, Bipolar'),(2,15,'Transistor, Low Frequency, Si FET'),(2,16,'Transistor, Unijunction'),(2,17,'Transistor, High Frequency, Low Noise, Bipolar'),(2,18,'Transistor, High Frequency, High Power, Bipolar'),(2,19,'Transistor, High Frequency, GaAs FET'),(2,20,'Transistor, High Frequency, Si FET'),(2,21,'Thyristor, SCR'),(2,22,'Optoelectronic, Detector, Isolator, Emitter'),(2,23,'Optoelectronic, Alphanumeric Display'),(2,24,'Optoelectronic, Laser Diode'),(3,25,'Fixed, Composition (RC, RCR)'),(3,26,'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)'),(3,27,'Fixed, Film, Power (RD)'),(3,28,'Fixed, Film, Network (RZ)'),(3,29,'Fixed, Wirewound (RB, RBR)'),(3,30,'Fixed, Wirewound, Power (RW, RWR)'),(3,31,'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)'),(3,32,'Thermistor (RTH)'),(3,33,'Variable, Wirewound (RT, RTR)'),(3,34,'Variable, Wirewound, Precision (RR)'),(3,35,'Variable, Wirewound, Semiprecision (RA, RK)'),(3,36,'Variable, Wirewound, Power (RP)'),(3,37,'Variable, Non-Wirewound (RJ, RJR)'),(3,38,'Variable, Composition (RV)'),(3,39,'Variable, Non-Wirewound, Film and Precision (RQ, RVC)'),(4,40,'Fixed, Paper, Bypass (CA, CP)'),(4,41,'Fixed, Feed-Through (CZ, CZR)'),(4,42,'Fixed, Paper and Plastic Film (CPV, CQ, CQR)'),(4,43,'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)'),(4,44,'Fixed, Plastic and Metallized Plastic'),(4,45,'Fixed, Super-Metallized Plastic (CRH)'),(4,46,'Fixed, Mica (CM, CMR)'),(4,47,'Fixed, Mica, Button (CB)'),(4,48,'Fixed, Glass (CY, CYR)'),(4,49,'Fixed, Ceramic, General Purpose (CK, CKR)'),(4,50,'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)'),(4,51,'Fixed, Electrolytic, Tantalum, Solid (CSR)'),(4,52,'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)'),(4,53,'Fixed, Electrolytic, Aluminum (CU, CUR)'),(4,54,'Fixed, Electrolytic (Dry), Aluminum (CE)'),(4,55,'Variable, Ceramic (CV)'),(4,56,'Variable, Piston Type (PC)'),(4,57,'Variable, Air Trimmer (CT)'),(4,58,'Variable and Fixed, Gas or Vacuum (CG)'),(5,59,'Transformer, Pulse'),(5,60,'Transformer, Audio'),(5,61,'Transformer, Power'),(5,62,'Transformer, RF'),(5,63,'Coil'),(6,64,'Mechanical'),(6,65,'Solid State'),(7,67,'Toggle or Pushbutton'),(7,68,'Sensitive'),(7,69,'Rotary'),(7,70,'Thumbwheel'),(7,71,'Circuit Breaker'),(8,72,'Multi-Pin'),(8,73,'PCB Edge'),(8,74,'IC Socket'),(8,75,'Plated Through Hole'),(8,76,'Clip'),(8,83,'Crimp'),(8,84,'Hand Solder'),(8,85,'Reflow Solder'),(8,86,'Weld'),(8,87,'Wrap'),(9,77,'Elapsed Time'),(9,78,'Panel'),(10,80,'Crystal'),(10,81,'Lamp'),(10,82,'Fuse'),(10,83,'Filter, Non-Tunable Electronic');
/*!40000 ALTER TABLE `tbl_subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_validation_type`
--

DROP TABLE IF EXISTS `tbl_validation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_validation_type` (
  `fld_validation_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_validation_type_desc` varchar(128) DEFAULT NULL,
  `fld_validation_type_code` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`fld_validation_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_validation_type`
--

LOCK TABLES `tbl_validation_type` WRITE;
/*!40000 ALTER TABLE `tbl_validation_type` DISABLE KEYS */;
INSERT INTO `tbl_validation_type` VALUES (1,'System Engineering','SYS'),(2,'Reliability Analysis','REL'),(3,'Design for X','DFX'),(4,'SubSystem Reliability Testing','SRT');
/*!40000 ALTER TABLE `tbl_validation_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
