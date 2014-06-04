-- MySQL dump 10.13  Distrib 5.1.56, for slackware-linux-gnu (x86_64)
--
-- Host: frodo    Database: example1
-- ------------------------------------------------------
-- Server version	5.1.56-log

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

--
-- Current Database: `example1`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `example1` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `example1`;

--
-- Table structure for table `tbl_allocation`
--

DROP TABLE IF EXISTS `tbl_allocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_allocation` (
  `fld_revision_id` int(11) NOT NULL,
  `fld_assembly_id` int(11) NOT NULL,
  `fld_included` tinyint(4) NOT NULL DEFAULT '1',
  `fld_n_sub_systems` int(11) NOT NULL DEFAULT '1',
  `fld_n_sub_elements` int(11) NOT NULL DEFAULT '1',
  `fld_weight_factor` float NOT NULL DEFAULT '1',
  `fld_percent_wt_factor` float NOT NULL DEFAULT '1',
  `fld_int_factor` int(11) NOT NULL DEFAULT '1',
  `fld_soa_factor` int(11) NOT NULL DEFAULT '1',
  `fld_op_time_factor` int(11) NOT NULL DEFAULT '1',
  `fld_env_factor` int(11) NOT NULL DEFAULT '1',
  `fld_availability_alloc` float NOT NULL DEFAULT '0',
  `fld_reliability_alloc` float NOT NULL DEFAULT '0',
  `fld_failure_rate_alloc` float NOT NULL DEFAULT '0',
  `fld_mtbf_alloc` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`fld_revision_id`,`fld_assembly_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_allocation`
--

LOCK TABLES `tbl_allocation` WRITE;
/*!40000 ALTER TABLE `tbl_allocation` DISABLE KEYS */;
INSERT INTO `tbl_allocation` VALUES (1,1,1,1,1,1,1,1,1,1,1,0,0,0,0),(1,2,1,1,1,1,1,1,1,1,1,0,0,0,0),(1,6,1,1,1,1,1,1,1,1,1,0,0,0,0),(1,8,1,1,1,1,1,1,1,1,1,0,0,0,0);
/*!40000 ALTER TABLE `tbl_allocation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_functional_matrix`
--

DROP TABLE IF EXISTS `tbl_functional_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_functional_matrix` (
  `fld_assembly_id` int(11) NOT NULL DEFAULT '0' COMMENT 'The index of the assembly in tbl_system.',
  `fld_function_id` int(11) NOT NULL DEFAULT '0' COMMENT 'The index of the function in tbl_functions.',
  `fld_revision_id` int(11) NOT NULL DEFAULT '0' COMMENT 'The index of the revision in tbl_revisions.',
  PRIMARY KEY (`fld_function_id`,`fld_assembly_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='This table holds component to function relationships.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_functional_matrix`
--

LOCK TABLES `tbl_functional_matrix` WRITE;
/*!40000 ALTER TABLE `tbl_functional_matrix` DISABLE KEYS */;
INSERT INTO `tbl_functional_matrix` VALUES (51,7,1),(52,7,1),(54,7,1),(56,7,1),(57,7,1),(58,7,1),(59,7,1),(60,7,1),(61,7,1),(62,7,1),(64,7,1),(66,7,1),(68,7,1),(69,7,1),(70,7,1),(71,7,1),(72,7,1),(73,7,1),(74,7,1),(75,7,1),(76,7,1),(77,7,1),(78,7,1),(79,7,1),(81,7,1),(83,7,1),(84,7,1),(85,7,1),(86,7,1),(87,7,1),(88,7,1),(89,7,1),(90,7,1),(92,7,1),(93,7,1),(94,7,1),(95,7,1),(100,7,1),(101,7,1),(55,8,1),(82,8,1),(55,10,1),(80,10,1),(82,10,1),(80,16,1);
/*!40000 ALTER TABLE `tbl_functional_matrix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_functions`
--

DROP TABLE IF EXISTS `tbl_functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_functions` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '1' COMMENT 'System revision identifier that this function belongs to.',
  `fld_function_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique function or functional failure identifier.',
  `fld_availability` float NOT NULL DEFAULT '1' COMMENT 'Predicted availability of the function; calculated from predicted failure rate.',
  `fld_availability_mission` float NOT NULL DEFAULT '1' COMMENT 'Mission availability of function; calculated from mission failure rate and mission time.',
  `fld_code` varchar(16) NOT NULL DEFAULT 'Function Code' COMMENT 'Alphanumeric code for the function.',
  `fld_cost` float NOT NULL DEFAULT '0' COMMENT 'Total cost of the function; sum of the unit cost of parts comprising the function.',
  `fld_failure_rate_mission` float NOT NULL DEFAULT '0',
  `fld_failure_rate_predicted` float NOT NULL DEFAULT '0',
  `fld_mmt` float NOT NULL DEFAULT '0',
  `fld_mcmt` float NOT NULL DEFAULT '0',
  `fld_mpmt` float NOT NULL DEFAULT '0',
  `fld_mtbf_mission` float NOT NULL DEFAULT '0',
  `fld_mtbf_predicted` float NOT NULL DEFAULT '0',
  `fld_mttr` float NOT NULL DEFAULT '0',
  `fld_name` varchar(255) DEFAULT 'Function Name' COMMENT 'Noun name of the function.',
  `fld_remarks` longblob,
  `fld_total_mode_quantity` int(11) NOT NULL DEFAULT '0',
  `fld_total_part_quantity` int(11) NOT NULL DEFAULT '0',
  `fld_type` int(11) NOT NULL DEFAULT '0',
  `fld_parent_id` varchar(16) NOT NULL DEFAULT '-',
  `fld_level` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`fld_revision_id`,`fld_function_id`) USING BTREE,
  KEY `lk_function` (`fld_function_id`),
  CONSTRAINT `tbl_functions_ibfk_1` FOREIGN KEY (`fld_revision_id`) REFERENCES `tbl_revisions` (`fld_revision_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COMMENT='Table containing system functions.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_functions`
--

LOCK TABLES `tbl_functions` WRITE;
/*!40000 ALTER TABLE `tbl_functions` DISABLE KEYS */;
INSERT INTO `tbl_functions` VALUES (1,6,1,1,'F_CAP_01',1.59,0,10.0378,0,0,0,0,99623.7,0,'Demonstrate Fixed Capacitance','',0,5,0,'0',1),(1,7,1,1,'F_CAP',0.09,0,10.7929,0,0,0,0,92653.6,0,'Demonstrate Capacitance','',0,44,0,'-',0),(1,8,1,1,'F_CAP_02',7.51,0,1.80786,0,0,0,0,553140,0,'Demonstrate Variable Capacitance','',0,8,0,'0',1),(1,9,1,1,'F_CON',0,0,10.9753,0,0,0,0,91113.4,0,'Demonstrate Connections','This function is used to demonstrate how The RTK Project handles electrical connections.',0,4,0,'-',0),(1,10,1,1,'F_CON_01',0,0,1.49267,0,0,0,0,669940,0,'New Function','',0,3,0,'1',0),(1,11,1,1,'F_CON_01_A',0,0,0,0,0,0,0,0,0,'New Function','',0,0,0,'1:0',0),(1,12,1,1,'F_CON_01_B',0,0,0,0,0,0,0,0,0,'New Function','',0,0,0,'1:0',0),(1,13,1,1,'FUNCTION 3',0,0,0,0,0,0,0,0,0,'New Function','',0,0,0,'1:0',0),(1,14,1,1,'F_CAP_03',1.61,0,1.70114,0,0,0,0,587840,0,'Demonstrate Electrolytic Capacitance','',0,3,0,'0',0),(1,15,1,1,'FUNCTION 4',0,0,0.890259,0,0,0,0,1.12327e+06,0,'New Function','',0,1,0,'1',0),(1,16,1,1,'FUNCTION 5',0,0,9.82767,0,0,0,0,101754,0,'New Function','',0,2,0,'1',0),(1,17,1,1,'FUNCTION 6',0,0,10.7717,0,0,0,0,92836,0,'New Function','',0,4,0,'1',0),(1,18,1,1,'FUNCTION 7',0,0,0.890259,0,0,0,0,1.12327e+06,0,'New Function','',0,1,0,'1',0),(1,19,1,1,'FUNCTION 8',0,0,0.890259,0,0,0,0,1.12327e+06,0,'Sub Function 8','',0,1,0,'1',0),(1,20,1,1,'FUNCTION 9',0,0,0,0,0,0,0,0,0,'New Function','',0,0,0,'1',0),(1,21,1,1,'FUNCTION 10',0,0,0,0,0,0,0,0,0,'Sub Sub Function 1','',0,0,0,'1:5',0),(1,22,1,1,'FUNCTION 11',0,0,0,0,0,0,0,0,0,'New Function','',0,0,0,'1:5',0),(1,23,1,1,'FUNCTION 12',0,0,0,0,0,0,0,0,0,'New Function','',0,0,0,'1:5',0),(1,24,0,1,'Unassigned',0,0,0,0,0,0,0,0,0,'Function Name','None',0,0,0,'-',0);
/*!40000 ALTER TABLE `tbl_functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_prediction`
--

DROP TABLE IF EXISTS `tbl_prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_prediction` (
  `fld_revision_id` int(11) NOT NULL,
  `fld_assembly_id` int(11) NOT NULL,
  `fld_function_id` int(11) NOT NULL DEFAULT '0',
  `fld_a1` float NOT NULL DEFAULT '0',
  `fld_a2` float NOT NULL DEFAULT '0',
  `fld_application_id` int(11) NOT NULL DEFAULT '0',
  `fld_burnin_temperature` float NOT NULL DEFAULT '30',
  `fld_burnin_time` float NOT NULL DEFAULT '0',
  `fld_c1` float NOT NULL DEFAULT '0',
  `fld_c2` float NOT NULL DEFAULT '0',
  `fld_c3` float NOT NULL DEFAULT '0',
  `fld_c4` float NOT NULL DEFAULT '0',
  `fld_c5` float NOT NULL DEFAULT '0',
  `fld_c6` float NOT NULL DEFAULT '0',
  `fld_c7` float NOT NULL DEFAULT '0',
  `fld_capacitance` float NOT NULL DEFAULT '0',
  `fld_construction_id` int(11) NOT NULL DEFAULT '0',
  `fld_current_ratio` float NOT NULL DEFAULT '1',
  `fld_cycles_id` int(11) NOT NULL DEFAULT '0',
  `fld_cycling_rate` float NOT NULL DEFAULT '0',
  `fld_devices_lab` int(11) NOT NULL DEFAULT '0',
  `fld_die_area` float NOT NULL DEFAULT '0',
  `fld_ea` float NOT NULL DEFAULT '0',
  `fld_ecc_id` int(11) NOT NULL DEFAULT '0',
  `fld_element_id` int(11) NOT NULL DEFAULT '0',
  `fld_esd_voltage` float NOT NULL DEFAULT '0',
  `fld_failures_field` int(11) NOT NULL DEFAULT '0',
  `fld_failures_lab` int(11) NOT NULL DEFAULT '0',
  `fld_family_id` int(11) NOT NULL DEFAULT '0',
  `fld_feature_size` float NOT NULL DEFAULT '1' COMMENT 'Default value is 1 to prevent division by zero errors.',
  `fld_func_id` int(11) NOT NULL DEFAULT '0',
  `fld_i1` float NOT NULL DEFAULT '0',
  `fld_i2` float NOT NULL DEFAULT '0',
  `fld_i3` float NOT NULL DEFAULT '0',
  `fld_i4` float NOT NULL DEFAULT '0',
  `fld_i5` float NOT NULL DEFAULT '0',
  `fld_i6` float NOT NULL DEFAULT '0',
  `fld_initial_temperature` float NOT NULL DEFAULT '30',
  `fld_insulation_id` int(11) NOT NULL DEFAULT '0',
  `fld_junction_temperature` float NOT NULL DEFAULT '30',
  `fld_k1` float NOT NULL DEFAULT '0',
  `fld_k2` float NOT NULL DEFAULT '0',
  `fld_k3` float NOT NULL DEFAULT '0',
  `fld_knee_temperature` float NOT NULL DEFAULT '0',
  `fld_l1` float NOT NULL DEFAULT '0',
  `fld_l2` float NOT NULL DEFAULT '0',
  `fld_lambda_b` float NOT NULL DEFAULT '0',
  `fld_lambda_b0` float NOT NULL DEFAULT '0',
  `fld_lambda_b1` float NOT NULL DEFAULT '0',
  `fld_lambda_b2` float NOT NULL DEFAULT '0',
  `fld_lambda_bd` float NOT NULL DEFAULT '0',
  `fld_lambda_eos` float NOT NULL DEFAULT '0',
  `fld_lambda_g` float NOT NULL DEFAULT '0',
  `fld_lambda_o` float NOT NULL DEFAULT '0',
  `fld_manufacturing_id` int(11) NOT NULL DEFAULT '0',
  `fld_max_rated_temperature` float NOT NULL DEFAULT '0',
  `fld_min_rated_temperature` float NOT NULL DEFAULT '0',
  `fld_number_contacts` int(11) NOT NULL DEFAULT '0',
  `fld_number_elements` int(11) NOT NULL DEFAULT '0',
  `fld_number_hand` int(11) NOT NULL DEFAULT '0',
  `fld_number_pins` int(11) NOT NULL DEFAULT '0',
  `fld_number_wave` int(11) NOT NULL DEFAULT '0',
  `fld_operating_current` float NOT NULL DEFAULT '0',
  `fld_operating_freq` float NOT NULL DEFAULT '0',
  `fld_operating_power` float NOT NULL DEFAULT '0',
  `fld_operating_time_field` float NOT NULL DEFAULT '0',
  `fld_operating_voltage` float NOT NULL DEFAULT '0',
  `fld_package_id` int(11) NOT NULL DEFAULT '0',
  `fld_pi_a` float NOT NULL DEFAULT '1',
  `fld_pi_c` float NOT NULL DEFAULT '1',
  `fld_pi_cf` float NOT NULL DEFAULT '1',
  `fld_pi_cyc` float NOT NULL DEFAULT '1',
  `fld_pi_e` float NOT NULL DEFAULT '1',
  `fld_pi_ecc` float NOT NULL DEFAULT '1',
  `fld_pi_f` float NOT NULL DEFAULT '1',
  `fld_pi_k` float NOT NULL DEFAULT '1',
  `fld_pi_m` float NOT NULL DEFAULT '1',
  `fld_pi_mfg` float NOT NULL DEFAULT '1',
  `fld_pi_pt` float NOT NULL DEFAULT '1',
  `fld_pi_q` float NOT NULL DEFAULT '1',
  `fld_pi_r` float NOT NULL DEFAULT '1',
  `fld_pi_sr` float NOT NULL DEFAULT '1',
  `fld_pi_u` float NOT NULL DEFAULT '1',
  `fld_pi_v` float NOT NULL DEFAULT '1',
  `fld_power_ratio` float NOT NULL DEFAULT '1',
  `fld_quality_id` int(11) NOT NULL DEFAULT '0',
  `fld_r1` float NOT NULL DEFAULT '0',
  `fld_r2` float NOT NULL DEFAULT '0',
  `fld_r3` float NOT NULL DEFAULT '0',
  `fld_r4` float NOT NULL DEFAULT '0',
  `fld_r5` float NOT NULL DEFAULT '0',
  `fld_r6` float NOT NULL DEFAULT '0',
  `fld_rated_current` float NOT NULL DEFAULT '1',
  `fld_rated_power` float NOT NULL DEFAULT '1',
  `fld_rated_voltage` float NOT NULL DEFAULT '1',
  `fld_resistance` float NOT NULL DEFAULT '1',
  `fld_resistance_id` int(11) NOT NULL DEFAULT '0',
  `fld_s1` float NOT NULL DEFAULT '0',
  `fld_s2` float NOT NULL DEFAULT '0',
  `fld_s3` float NOT NULL DEFAULT '0',
  `fld_s4` float NOT NULL DEFAULT '0',
  `fld_specification_id` int(11) NOT NULL DEFAULT '0',
  `fld_specsheet_id` int(11) NOT NULL DEFAULT '0',
  `fld_tbase` float NOT NULL DEFAULT '0',
  `fld_technology_id` int(11) NOT NULL DEFAULT '0',
  `fld_temperature` float NOT NULL DEFAULT '30',
  `fld_temperature_lab` float NOT NULL DEFAULT '30',
  `fld_temperature_rise` float NOT NULL DEFAULT '0',
  `fld_test_time_lab` float NOT NULL DEFAULT '0',
  `fld_thermal_resistance` float NOT NULL DEFAULT '0',
  `fld_tref` float NOT NULL DEFAULT '0',
  `fld_voltage_ratio` float NOT NULL DEFAULT '1',
  `fld_years` float NOT NULL DEFAULT '1',
  PRIMARY KEY (`fld_revision_id`,`fld_assembly_id`),
  KEY `fld_assembly_id` (`fld_assembly_id`),
  CONSTRAINT `tbl_prediction_ibfk_2` FOREIGN KEY (`fld_assembly_id`) REFERENCES `tbl_system` (`fld_assembly_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_prediction`
--

LOCK TABLES `tbl_prediction` WRITE;
/*!40000 ALTER TABLE `tbl_prediction` DISABLE KEYS */;
INSERT INTO `tbl_prediction` VALUES (1,26,6,0,0,0,30,0,51,0.016462,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0,0,0,3e-05,1.82,30,0,30,0,0,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,0,0,0,0,5,3,1,1,1,1,2,1,1,1,1,1,1,10,1.48413,1,0,1,0,4,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,2,30,30,0,0,20,0,1,1),(1,27,6,0,0,0,30,0,0.06,0.008665,0,0,0,0,0,0,0,1,0,0,0,0,0.35,0,4,0,0,0,0,1,0,0,0,0,0,0.00028,1.08,30,0,33,0,0,0,50,0,0,0,0,0,0,0,0,0,0,0,125,-55,0,4,0,24,0,0.004,0,0.15,0,24,3,1,1,1,1,2,1,1,1,1,1,1,2,0.519354,1,0.193823,1,0.220588,3,0,0,0,0,0,0,0.004,0.68,40,0,0,0,0,0,0,0,0,30,2,30,30,0,0,20,0,0.6,4),(1,28,6,0,0,0,30,0,0.08,0.011823,0,0,0,0,0,0,0,0.14,0,0,0,0,0.35,0,4,0,0,0,11,1,0,0,0,0,0,0.00028,1.08,30,0,36.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,0.0007,0,0.05,0,5,1,1,1,1,1,2,1,1,1,1,1,1,2,0.257903,1,0.164187,1,0.4,3,0,0,0,0,0,0,0.005,0.125,5,0,0,0,0,0,0,0,0,0,2,30,30,0,0,125,0,1,6),(1,29,6,0,0,1,30,0,7.2,0.024994,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,1,1,0,0,0,0,0,0.00028,1.08,30,0,30,0,0,0,0,0,0,0.09,0,0,0,0,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,5,1,1,1,1,1,2,1,1,1,1,1,1,10,1.48413,1,0,1,0,4,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,30,2,30,30,0,0,28,0,1,1),(1,30,6,0,0,2,30,0,1.12,0.455131,0,0,0,0,0,0,0,0.716667,0,0,0,0.25,0,0,4,2000,0,0,0,1,0,0,0,0,0,0.00028,1.08,30,0,50.15,0,0,0,70,0,0,0,0,0,0,0.24,0.043625,0,0,2,70,-25,0,0,0,940,0,43,0,65,0,1.5,1,1,1,3.40762,1,2,1,1,1,1,2,1,1,0.257903,1,0.717096,1,0.730337,2,0,0,0,0,0,0,60,89,1.5,0,0,0,0,0,0,0,0,30,2,30,30,0,0,0.31,0,1,6),(1,37,6,0.68,0,0,30,0,0.0068,0.011823,0,0,0,0,0,0,0,0,10,0,0,0,0.35,3,4,0,0,0,0,1,0,0,0,0,0,0.00028,1.08,30,0,31.032,64000,0.25,0.12,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,1024000,0,32,0,0,0,0.043,0,3.3,1,1,1,1,1,2,0.68,1,1,1,1,1,1,0.365982,1,0.158975,1,0,2,0,0,0,0,0,0,0,0,3.3,0,0,0,0,0,0,0,0,333,2,30,30,0,0,24,0,1,5),(1,39,6,0,0,0,30,0,0.0025,0.005593,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0,0,0,0.00028,1.08,30,0,46.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,70,0,0,0,0,16,0,0,0,0.3,0,3.3,1,1,1,1,1,2,1,1,1,1,1,1,2,0.257903,1,0.549242,1,0.6,3,0,0,0,0,0,0,0,0.5,3.3,0,0,0,0,0,0,0,0,0,2,30,30,0,0,55,0,1,6),(1,40,6,0,0,0,30,0,0.00085,0.011823,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0.00028,1.08,30,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,32,0,0,0,0,0,3.3,1,1,1,1,1,2,1,1,1,1,1,1,2,1.04585,1,0.151847,1,0,3,0,0,0,0,0,0,0,0,3.3,0,0,0,0,0,0,0,0,0,2,30,30,0,0,28,0,1,2),(1,41,6,0,0,0,30,0,0.011,0.005593,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0,0,0,0.00028,1.08,30,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,3.3,1,1,1,1,1,2,1,1,1,1,1,1,10,0.181741,1,0.151847,1,0,4,0,0,0,0,0,0,0,0,3.3,0,0,0,0,0,0,0,0,0,2,30,30,0,0,28,0,1,7),(1,42,6,0,0,3,30,0,1.12,0,0,0,0,0,0,0,1,0.4,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,5260,0,0,30,0,33.75,0,0,0,125,0,0,0.22,0,0,0,0,0,0,0,0,125,-55,0,0,0,0,0,0.04,0,0.25,0,5,37,1,1,1,1,2,1,1,1,1,1,1,5,1,1,1.65449,1,0.071429,3,0,0,0,0,0,0,0.1,3.5,35,0,0,0,0,0,0,0,0,0,0,30,30,0,0,15,0,0.142857,1),(1,43,6,0,0,2,30,0,0,0,0,0,0,0,0,0,2,0.465116,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,3091,0,0,30,0,78.372,0,0,0,150,0,0,0.001,0,0,0,0,0,0,0,0,150,-65,0,0,0,0,0,0.1,0,0.087,0,24,22,1,2,1,1,6,1,1,1,1,1,1,2.4,1,0.074187,4.83334,1,0.386667,3,0,0,0,0,0,0,0.215,0.225,70,0,0,0,0,0,0,0,0,0,0,30,30,0,0,556,0,0.342857,1),(1,44,6,0,0,1,30,0,0.06,0,0,0,0,0,0,0,2,0.666667,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2100,0,0,30,0,45.4,0,0,0,45,0,0,0.00301,0,0,0,0,0,0,0,0,75,-25,0,7,0,0,0,0.01,0,0.22,0,5,44,0.5,1,1,1,2,1,1,1,1,1,1,5.5,1,0.54,1.82185,1,0.6875,4,0,0,0,0,0,0,0.015,0.32,5,0,0,0,0,0,0,0,0,0,0,30,30,0,0,70,0,1,1),(1,45,6,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.0022,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,2,43,1,1,1,1,6,1,1,1,1,1,1,2.4,1.90365,0.175353,1.18609,1,0,3,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,30,30,0,0,10,0,0.4,1),(1,47,0,0,0,3,30,0,1.12,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.00023,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,40,1,1,1,1,2,1,1,1,1,1,1,2.4,1.48413,1,1.16707,1,0,3,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,30,30,0,0,5,0,1,1),(1,48,0,0,0,2,30,0,0,0,0,0,0,0,0,0,1,0,0,65,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,3.23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.025,0.5,0,0,1,41,8.06226,1,1,1,2,1,1,0.081395,1,1,0.833333,1,1,1,1.29261,1,0,2,0,0,0,0,0,0,0,0.2,1,0,0,0,0,0,0,0,0,0,0,30,30,0,0,10,0,1,1),(1,49,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,6e-05,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0.05,0,3.3,0,1,1,1,1,2,1,1,1,1,1,1,3,1,1,2e-06,1,0.2,2,0,0,0,0,0,0,0,0.25,1,0,1,0,0,0,0,0,0,30,0,30,30,0,0,0,0,3.3,1),(1,50,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,125,0,0,0.014139,0,0,0,0,0,0,0,0,175,0,0,0,0,0,0,0,0,0.125,0,1,0,1,1,1,1,2,1,1,1,1,1,1,1,1.2,1,2e-06,1,0.125,1,0,0,0,0,0,0,0,1,1,0,2,0,0,0,0,0,0,0,0,30,30,0,0,0,0,1,1),(1,53,0,0,0,2,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,31.53,0,0,0,0,0,0,0.237108,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,2.25,0,1,6,4,1,1,1,2,1,1,1,4,1,1,2,0,1,1.38088,1,0,3,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,30,3,30,30,0,0,0.68,0,1,1),(1,54,0,0,0,2,30,0,0,0,0,0,0,0,0,0,1,0,0,0.35,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,82.5,0,0,0,0,0,0,0.237483,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,42,0,50,2,7.6,1,1,1,2,1,1,1,4,1,1,2,1,1,0.068173,1,0,3,0,0,0,0,0,0,0,0,140,0,0,0,0,0,0,0,0,0,3,30,30,0,0,1.25,0,0.357143,1),(1,55,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,32.5,0,0,0,0,0,0,0.18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25,0,0.38,3,0,1,1,1,2,1,1,1,1,1,1,2,0.773782,2.16443,1.19024,1,0.5,3,0,0,0,0,0,0,0,0.5,0.75,0,0,0,0,0,0,0,0,0,0,30,30,0,0,10,0,0.506667,1),(1,56,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30.15,0,0,0,25,0,0,0.06,0,0,0,0,0,0,0,0,150,0,0,0,0,0,0,0,0,0.03,0,1,17,1,1,1,1,2,1,1,1,1,1,1,1,0.43,9.98908,1.11599,1,0.15,2,0,0,0,0,0,0,0,0.2,5,0,0,0,0,0,0,0,0,0,1,30,30,0,0,5,0,0.2,1),(1,57,0,0,0,1,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,42.5,0,0,0,0,0,0,0.00074,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25,0,0.36,8,1.5,1,1,1,6,1,1,1,1,1,1,1,6,0.137368,1.48214,1,0.5,2,0,0,0,0,0,0,1,0.5,1,1,0,0,0,0,0,0,0,0,0,30,30,0,0,50,0,0.36,1),(1,58,0,0,0,3,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,80,0,0,0,0,0,0,0.012,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,31,4,1,1,1,6,1,1,1,1,1,1,2.4,1.81392,0.045,2.73594,1,0.4,3,0,0,0,0,0,0,1,5,1,1,0,0,0,0,0,0,0,0,1,30,30,0,0,25,0,0,1),(1,59,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.000181,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1.5,1,1,1,6,1,1,1,1,1,1,8,1,0.045,1.1474,1,0,5,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,30,30,0,0,70,0,0,1),(1,60,0,0,0,0,30,0,0.06,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,38.75,0,0,0,0,0,0,0.000287,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.125,0,3.3,0,1,4,1,1,3,1,1,1,1,1,1,5,1.6,1,1.44412,1,0.25,5,0,0,0,0,0,0,1,0.5,1,1,3,0,0,0,0,0,0,0,0,30,30,0,0,0,0,3.3,1),(1,61,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.001251,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.5,0,3.3,0,1,1,1,1,2,1,1,1,1,1,1,5,1.6,1,1,1,0.5,5,0,0,0,0,0,0,1,1,1,1,3,0,0,0,0,3,0,0,0,30,30,0,0,0,0,3.3,1),(1,62,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,70,0,0,0.00383,0,0,0,0,0,0,0,0,175,-65,0,0,0,0,0,0,0,0.125,0,0,0,1,1,1,1,2,1,1,1,1,1,1,0.3,1,1,1,1,0.25,3,0,0,0,0,0,0,1,0.5,1,1,1,0,0,0,0,0,0,0,0,30,30,0,0,0,0,0,1),(1,64,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.0081,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.075,0,0,0,1,1,1,1,2,1,1,1,1,1,1,0.1,1,1,1,1,0.3,2,0,0,0,0,0,0,1,0.25,1,1,-1,0,0,0,0,1,6,0,0,30,30,0,0,0,0,0,1),(1,66,0,0,0,0,30,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.002197,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,1,1,1,1,1,1,0.1,1,1,1,1,0,2,0,0,0,0,0,0,1,1,1,1,4,0,0,0,0,1,4,0,0,30,30,0,0,0,0,0,1),(1,68,0,0,0,0,30,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.021,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.05,0,1.5,0,1,1,1,1,5,1,1,1,1,1,1,15,1,1,1,1,0.4,2,0,0,0,0,0,0,1,0.125,1,1,4,0,0,0,0,0,0,0,0,30,30,0,0,0,0,1.5,1),(1,69,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.037236,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0.18,0,24,0,1,1,1,1,2,1,1,1,1,1,1,2.5,1,1,0.905137,1,0.36,1,0,0,0,0,0,0,1,0.5,350,1,1,0,0,0,0,0,6,0,0,30,30,0,0,0,0,0.068571,1),(1,70,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.021674,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,24,0,1,1,1,1,3,1,1,1,1,1,1,3,1.1,1,0.905137,1,0,5,0,0,0,0,0,0,1,5,200,56000,2,0,0,0,0,0,3,0,0,30,30,0,0,0,0,0.12,1),(1,71,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.030955,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0.25,0,24,0,1,1,1,1,3,1,1,1,1,1,1,2,1.2,1,0.905137,1,0.25,1,0,0,0,0,0,0,1,1,500,1,3,0,0,0,0,1,7,0,0,30,30,0,0,0,0,0.048,1),(1,72,0,0,0,0,30,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.024259,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0.25,0,24,0,1,1,1,1,2,1,1,1,1,1,1,3,1.4,1,0.905137,1,0.25,5,0,0,0,0,0,0,1,1,90,1,2,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.266667,1),(1,73,0,0,0,0,30,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.086717,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0.25,0,24,0,1,2,1,1,3,1,1,1,1,1,1,2,1.4,1,0.999846,1,0.25,1,0,0,0,0,0,0,1,1,100,2700,2,0,0,0,0,2,30,0,0,30,30,0,0,0,0,0.24,1),(1,74,0,0,0,0,30,0,1.12,0,0,0,0,0,0,3e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,31,0,0,0,0,0,0,0.021004,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.05,0,2.2,0,1,1,0.304357,1,2,1,1,1,1,1,1,10,1.48413,1,0.164805,1,0.05,3,0,0,0,0,0,0,1,1,5,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.44,1),(1,75,0,0,0,0,30,0,0,0,0,0,0,0,0,2e-06,-1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,65,0,0,0,0,0,0,0.111243,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.5,0,4.5,0,1,1.5,0.344968,1,2,1,1,1,1,1,1,3,1,1,3.02823,2,0.5,1,0,0,0,0,0,0,1,1,10,1,0,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.45,1),(1,76,0,0,0,0,30,0,0,0,0,0,0,0,0,3e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.009929,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0,15,0,1,1,0.488294,1,2,1,1,1,1,1,1,1,1,1,1,1,0.1,4,0,0,0,0,0,0,1,1,33,1,0,0,0,0,0,2,4,0,0,30,30,0,0,0,0,0.454545,1),(1,77,0,0,0,0,30,0,0,0,0,0,0,0,0,3e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.075088,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,10,0,1,1,0.372457,1,2,1,1,1,1,1,1,1,1,1,1,1,1,4,0,0,0,0,0,0,1,1,22,1,0,0,0,0,0,2,2,0,0,30,30,0,0,0,0,0.454545,1),(1,78,0,0,0,0,30,0,0,0,0,0,0,0,0,3e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.020098,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.05,0,2.2,0,1,1,0.36849,1,2,1,1,1,1,1,1,1,1,0.33,1,1,0.05,4,0,0,0,0,0,0,1,1,5,0.05,0,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.44,1),(1,79,0,0,0,0,30,0,0,0,0,0,0,0,0,2e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.01013,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,1,1,0.358819,1,4,1,1,1,1,1,1,1,1,1,1,1,0,4,0,0,0,0,0,0,1,1,22,1,0,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.454545,1),(1,80,0,0,0,0,30,0,0,0,0,0,0,0,0,1e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.000672,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,5,0,1,1,0.065045,1,2,1,1,1,1,1,1,0.1,1,1,1,1,1,3,0,0,0,0,0,0,1,1,22,1,0,0,0,0,0,1,3,0,0,30,30,0,0,0,0,0.227273,1),(1,81,0,0,0,0,30,0,0,0,0,0,0,0,0,3e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.036981,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.5,0,3,0,1,1,0.016638,1,2,1,1,1,1,1,1,5,1,1,1,1,0.5,1,0,0,0,0,0,0,1,1,10,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.3,1),(1,82,0,0,0,0,30,0,0,0,0,0,0,0,0,1e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.00032,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,190,0,1,1,0.123706,1,2,1,1,1,1,1,1,3,1,1,1,1,10,5,0,0,0,0,0,0,1,1,220,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.863636,1),(1,83,0,0,0,0,30,0,0,0,0,0,0,0,0,1e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.141561,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,3.5,0,1,1,0.115554,1,2,1,1,1,1,1,1,1,1,1,1,1,1,4,0,0,0,0,0,0,1,1,10,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.35,1),(1,84,0,0,0,0,30,0,0,0,0,0,0,0,0,2.2e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,1,1,0.162908,1,2,1,1,1,1,1,1,1,1,1,1,1,0,4,0,0,0,0,0,0,1,1,22,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.227273,1),(1,85,0,0,0,0,30,0,0.06,0,0,0,0,0,0,0.001,4,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,35,0,0,0,0,0,0,0.095744,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25,0,4.7,0,1,2.5,0.519773,1,2,1,1,1,1,1,1,1.5,1.48413,1,0.227469,1,0.25,5,0,0,0,0,0,0,1,1,10,0.5,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.47,1),(1,86,0,0,0,0,30,0,0,0,0,0,0,0,0,0.001,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.127588,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,50,0,1,1,0.436516,1,2,1,1,1,1,1,1,1.5,1,0.33,1,1,2,8,0,0,0,0,0,0,1,1,100,0.5,0,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.5,1),(1,87,0,0,0,0,30,0,0,0,0,0,0,0,0,1e-06,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.231226,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,20,0,1,1,0.1,1,3,1,1,1,1,1,1,3,1,1,1,1,1,1,0,0,0,0,0,0,1,1,50,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.4,1),(1,88,0,0,0,0,30,0,0,0,0,0,0,0,0,2.2e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.049805,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,1,1,1,1,3,1,1,1,1,1,1,5,1,1,1,1,0,1,0,0,0,0,0,0,1,1,10,1,0,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.4,1),(1,89,0,0,0,0,30,0,0,0,0,0,0,0,0,1e-06,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.034766,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,1,1,1,1,3,1,1,1,1,1,1,4,1,1,1,1,0,1,0,0,0,0,0,0,1,1,50,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.4,1),(1,90,0,0,0,0,30,0,0,0,0,0,0,0,0,3.3e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.155613,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,1,1,1,1,3,1,1,1,1,1,1,3,1,1,1,1,0,1,0,0,0,0,0,0,1,1,10,1,0,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.9,1),(1,92,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,4,47.1875,0,0,0,0,6,0.5,0.002228,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.75,0,4,0,1,1,1,1,6,1,1,1,1,1,0,3,1,1,1,1,0.75,1,0,0,0,0,0,0,1,1,10,1,0,0,0,0,0,1,1,0,0,30,30,15.625,0,0,0,0.4,1),(1,93,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,4,68.5,0,0,0,0,6.5,0,0.002457,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,6,1,1,1,1,1,1,3,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,30,30,35,0,0,0,0,1),(1,94,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,5,49.2103,0,0,0,0,0,0.75,0.001957,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1.25,0,0,0,1,1,1,1,6,1,1,1,1,1,1,3,1,1,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,30,30,17.4639,0,0,0,0,1),(1,95,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,2,46.9714,0,0,0,0,0,0.6,0.002602,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,6,1,1,1,1,1,1,7.5,1,1,1,1,0,2,0,0,0,0,0,0,1,5.2,1,1,0,0,0,0,0,0,0,30,0,30,30,15.4286,0,0,0,0,1),(1,96,0,0,0,0,30,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,2,38.5938,0,0,0,0,2,0.1,0.004857,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.125,0,0,0,1,1,1,1,4,1,1,1,1,1,1,3,1,1,1,1,0.125,-1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,30,30,7.8125,0,0,0,0,1),(1,98,0,0,0,1,30,0,0,0,0,0,0,0,0,0,1,0.4,0,1,0,0,0,0,0,0,0,0,6,1,1,0,0,0,2100,0,0,30,1,68.5,0,0,0,0,0,0,0.006103,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0.5,3,1,0.1,2,1,7,1,2.71828,1,1,1.5,-0.25,1,1.12332,1,0,6,0,0,0,0,0,0,10,1,1,1,4,0,0,0,0,0,0,30,0,30,30,35,0,0,0,0,1),(1,99,0,0,0,0,30,0,0.06,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1925,0,0,30,0,30,0,0,0,0,0,0,0.4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,3,1,1,1,1,1,1,1,1.48413,0.54,0.151847,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,30,30,0,0,0,0,0,1),(1,100,0,0,0,0,30,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,34,0,0,0,0,0,0,0.053537,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,4,0,1,1,0.800717,1,2,1,1,1,1,1,1,1,1.48413,1,0.210028,1,0.2,4,0,0,0,0,0,0,1,1,12,1,0,0,0,0,0,1,2,0,0,30,30,0,0,0,0,0.333333,1),(1,101,0,0,0,0,30,0,0.06,0,0,0,0,0,0,25,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.042057,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4,0,12,0,1,1,0.618722,1,2,1,1,1,1,1,0,3,1.48413,1,0.151847,1,0.4,1,0,0,0,0,0,0,1,1,35,1,0,0,0,0,0,1,1,0,0,30,30,0,0,0,0,0.342857,1),(1,102,0,0,0,0,30,0,0.06,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,9,30,0,0,0,0,0,0,0.00042,0,0,0,0,0,0,0,0,0,0,32,0,0,60,0,0,0,0,0,0,0,1,1,0,1,3,1,1,1.5,1,1,5.76852,1,1.48413,1,0.151847,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0.025,0.5,0,0,0,0,0,30,30,0.000696,0,0,0,0,1),(1,103,0,0,0,0,30,0,0,0,0,0,0,0,0,0,2,0,3,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,6,30,0,0,0,0,0,0,0.000247,0,0,0,0,0,0,0,0,0,0,24,0,0,32,0,0,0,0,0,24,0,1,1,0,1,1,1,1,2,1,1,5.76852,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,600,1,0,0,0.05,0.8,0,0,0,0,0,30,30,0.001074,0,0,0,0.04,1),(1,104,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.000124,0,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,1,1,1,1,3,1,1,1.5,1,1,12.1416,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0.025,0.08,0,0,0,0,0,30,30,0.001075,0,0,0,0,1),(1,106,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,0.00041,0,0,0,0,0,0,0,0,0,0,64,4,1,0,3,0,0,0,0,0,0,1,1.55672,1,1,2,1,1,1.5,1,1,12.1416,1,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0.03,0.08,0,0,0,0,1,30,30,0.001506,0,0,0,0,1),(1,108,0,0,0,0,30,0,0,0,0,0,0,0,0,0,0,0.4,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,30,0,30,0,0,0,0,0,0,6.9e-05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0,0.05,0,5,0,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,0.4,1,0,0,0,0,0,0,0.025,0.125,25,1,1,0,0,0,0,0,0,0,0,30,30,0,0,0,0,0.2,1);
/*!40000 ALTER TABLE `tbl_prediction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_program_info`
--

DROP TABLE IF EXISTS `tbl_program_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_program_info` (
  `fld_program_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_revision_prefix` varchar(16) NOT NULL DEFAULT 'REVISION',
  `fld_revision_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_function_prefix` varchar(16) NOT NULL DEFAULT 'FUNCTION',
  `fld_function_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_assembly_prefix` varchar(16) NOT NULL DEFAULT 'ASSEMBLY',
  `fld_assembly_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_part_prefix` varchar(16) NOT NULL DEFAULT 'PART',
  `fld_part_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_fmeca_prefix` varchar(16) NOT NULL DEFAULT 'FMEA',
  `fld_fmeca_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_mode_prefix` varchar(16) NOT NULL DEFAULT 'MODE',
  `fld_mode_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_effect_prefix` varchar(16) NOT NULL DEFAULT 'EFFECT',
  `fld_effect_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_cause_prefix` varchar(16) NOT NULL DEFAULT 'CAUSE',
  `fld_cause_next_id` int(11) NOT NULL DEFAULT '1',
  `fld_revision_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_function_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_fmeca_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_maintainability_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_rcm_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_rbd_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_fta_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_fraca_active` tinyint(4) NOT NULL DEFAULT '1',
  `fld_created_on` datetime DEFAULT NULL,
  `fld_created_by` varchar(45) DEFAULT '',
  `fld_last_saved` datetime DEFAULT NULL,
  `fld_last_saved_by` varchar(45) DEFAULT '',
  PRIMARY KEY (`fld_program_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_program_info`
--

LOCK TABLES `tbl_program_info` WRITE;
/*!40000 ALTER TABLE `tbl_program_info` DISABLE KEYS */;
INSERT INTO `tbl_program_info` VALUES (1,'REVISION',1,'FUNCTION',13,'ASSEMBLY',3,'PART',61,'FMEA',1,'MODE',1,'EFFECT',1,'CAUSE',1,1,1,1,1,1,1,1,1,'0000-00-00 00:00:00','',NULL,NULL);
/*!40000 ALTER TABLE `tbl_program_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_requirements`
--

DROP TABLE IF EXISTS `tbl_requirements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_requirements` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '1',
  `fld_requirement_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_assembly_id` int(11) NOT NULL DEFAULT '1',
  `fld_requirement_desc` blob,
  `fld_requirement_type` int(11) NOT NULL DEFAULT '0',
  `fld_requirement_code` varchar(16) DEFAULT NULL,
  `fld_derived` tinyint(1) DEFAULT '0',
  `fld_parent_requirement` varchar(45) NOT NULL DEFAULT '-',
  `fld_validated` tinyint(1) DEFAULT '0',
  `fld_validated_date` varchar(45) DEFAULT NULL,
  `fld_owner` varchar(64) DEFAULT NULL,
  `fld_specification` varchar(128) DEFAULT NULL,
  `fld_page_number` varchar(32) DEFAULT NULL,
  `fld_figure_number` varchar(32) DEFAULT NULL,
  `fld_parent_id` int(11) DEFAULT '0',
  PRIMARY KEY (`fld_requirement_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_requirements`
--

LOCK TABLES `tbl_requirements` WRITE;
/*!40000 ALTER TABLE `tbl_requirements` DISABLE KEYS */;
INSERT INTO `tbl_requirements` VALUES (1,1,1,'Example system 1 shall operate within all specified parameters at temperatures in the military temperature range (-55C to 155C).',4,'PRF-0001',0,'-',0,'None','Systems Engineering','','None','None',-1),(1,2,1,'Example system 1 shall have an MTBF >= 5000 hours under the stated worst-case environmental and mission profile.',5,'REL-0002',0,'-',0,'None','Design Assurance','','None','None',0),(1,3,1,'The Integrated Circuit Subsystem shall have an MTBF >= 15,000 hours under the stated worst-case environmental and mission profile.',5,'REL-0003',1,'1',0,'None','Design Assurance','','None','None',2),(1,5,2,'The Integrated Circuit & Semiconductor Subsystem shall have an MTBF >= 10,000 hours under the stated worst-case environmental and mission profile.',5,'REL-0005',1,'1',0,'None','Design Assurance','','','',3),(1,6,1,'No single failure shall result in the loss of Example system 1.',5,'REL-0006',0,'-',0,'None','Design Assurance','None','None','None',0);
/*!40000 ALTER TABLE `tbl_requirements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_revisions`
--

DROP TABLE IF EXISTS `tbl_revisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_revisions` (
  `fld_revision_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_availability` float NOT NULL DEFAULT '1',
  `fld_availability_mission` float NOT NULL DEFAULT '1',
  `fld_cost` float NOT NULL DEFAULT '0',
  `fld_cost_failure` float NOT NULL DEFAULT '0',
  `fld_cost_hour` float NOT NULL DEFAULT '0',
  `fld_failure_rate_active` float NOT NULL DEFAULT '0',
  `fld_failure_rate_dormant` float NOT NULL DEFAULT '0',
  `fld_failure_rate_mission` float NOT NULL DEFAULT '0',
  `fld_failure_rate_predicted` float NOT NULL DEFAULT '0',
  `fld_failure_rate_software` float NOT NULL DEFAULT '0',
  `fld_mmt` float NOT NULL DEFAULT '0',
  `fld_mcmt` float NOT NULL DEFAULT '0',
  `fld_mpmt` float NOT NULL DEFAULT '0',
  `fld_mtbf_mission` float NOT NULL DEFAULT '0',
  `fld_mtbf_predicted` float NOT NULL DEFAULT '0',
  `fld_mttr` float NOT NULL DEFAULT '0',
  `fld_name` varchar(128) NOT NULL DEFAULT '',
  `fld_reliability_mission` float NOT NULL DEFAULT '1',
  `fld_reliability_predicted` float NOT NULL DEFAULT '1',
  `fld_remarks` longblob NOT NULL,
  `fld_total_part_quantity` int(11) NOT NULL DEFAULT '1',
  `fld_revision_code` varchar(8) DEFAULT '',
  PRIMARY KEY (`fld_revision_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='Table containing configuration information.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_revisions`
--

LOCK TABLES `tbl_revisions` WRITE;
/*!40000 ALTER TABLE `tbl_revisions` DISABLE KEYS */;
INSERT INTO `tbl_revisions` VALUES (1,1,1,9.21,44,0,33.409,2.07637,0,35.4854,0,0,0,0,0,28180.6,0,'Original',1,1,'This is the original revision of example system #1.',66,''),(3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'New Revision',1,1,'',0,'A');
/*!40000 ALTER TABLE `tbl_revisions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_similar_item`
--

DROP TABLE IF EXISTS `tbl_similar_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_similar_item` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '1',
  `fld_assembly_id` int(11) NOT NULL DEFAULT '1',
  `fld_sia_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_change_desc_1` blob NOT NULL,
  `fld_change_category_1` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_1` float DEFAULT '1',
  `fld_change_effort_1` int(11) DEFAULT '0',
  `fld_change_cost_1` float DEFAULT '0',
  `fld_change_desc_2` blob NOT NULL,
  `fld_change_category_2` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_2` float DEFAULT '1',
  `fld_change_effort_2` int(11) DEFAULT '0',
  `fld_change_cost_2` float DEFAULT '0',
  `fld_change_desc_3` blob,
  `fld_change_category_3` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_3` float DEFAULT '1',
  `fld_change_effort_3` int(11) DEFAULT '0',
  `fld_change_cost_3` float DEFAULT '0',
  `fld_change_desc_4` blob NOT NULL,
  `fld_change_category_4` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_4` float DEFAULT '1',
  `fld_change_effort_4` int(11) DEFAULT '0',
  `fld_change_cost_4` float DEFAULT '0',
  `fld_change_desc_5` blob NOT NULL,
  `fld_change_category_5` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_5` float DEFAULT '1',
  `fld_change_effort_5` int(11) DEFAULT '0',
  `fld_change_cost_5` float DEFAULT '0',
  `fld_change_desc_6` blob NOT NULL,
  `fld_change_category_6` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_6` float DEFAULT '1',
  `fld_change_effort_6` int(11) DEFAULT '0',
  `fld_change_cost_6` float DEFAULT '0',
  `fld_change_desc_7` blob NOT NULL,
  `fld_change_category_7` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_7` float DEFAULT '1',
  `fld_change_effort_7` int(11) DEFAULT '0',
  `fld_change_cost_7` float DEFAULT '0',
  `fld_change_desc_8` blob NOT NULL,
  `fld_change_category_8` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_8` float DEFAULT '1',
  `fld_change_effort_8` int(11) DEFAULT '0',
  `fld_change_cost_8` float DEFAULT '0',
  `fld_function_1` varchar(128) NOT NULL,
  `fld_function_2` varchar(128) NOT NULL,
  `fld_function_3` varchar(128) NOT NULL,
  `fld_function_4` varchar(128) NOT NULL,
  `fld_function_5` varchar(128) NOT NULL,
  `fld_result_1` float DEFAULT '0',
  `fld_result_2` float DEFAULT '0',
  `fld_result_3` float DEFAULT '0',
  `fld_result_4` float DEFAULT '0',
  `fld_result_5` float DEFAULT '0',
  `fld_user_blob_1` blob NOT NULL,
  `fld_user_blob_2` blob NOT NULL,
  `fld_user_blob_3` blob NOT NULL,
  `fld_user_float_1` float DEFAULT '0',
  `fld_user_float_2` float DEFAULT '0',
  `fld_user_float_3` float DEFAULT '0',
  `fld_user_int_1` int(11) DEFAULT '0',
  `fld_user_int_2` int(11) DEFAULT '0',
  `fld_user_int_3` int(11) DEFAULT '0',
  `fld_category_value_1` int(11) DEFAULT '0',
  `fld_category_value_2` int(11) DEFAULT '0',
  `fld_category_value_3` int(11) DEFAULT '0',
  `fld_category_value_4` int(11) DEFAULT '0',
  `fld_category_value_5` int(11) DEFAULT '0',
  `fld_category_value_6` int(11) DEFAULT '0',
  `fld_category_value_7` int(11) DEFAULT '0',
  `fld_category_value_8` int(11) DEFAULT '0',
  PRIMARY KEY (`fld_sia_id`,`fld_revision_id`,`fld_assembly_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_similar_item`
--

LOCK TABLES `tbl_similar_item` WRITE;
/*!40000 ALTER TABLE `tbl_similar_item` DISABLE KEYS */;
INSERT INTO `tbl_similar_item` VALUES (1,2,1,'Changing all TTL devices to CMOS devices.  Changing all logic devices from +5VDC to +2.7VDC.','Medium',1.25,68,42000,'Will be required to use Pb free solder.','High',1.5,0,0,'No change in usage.','None',1,0,0,'Voltage and current stresses being reduced with reduction in operating voltage from +5VDC to +2.7VDC.','Low',0.8,0,0,'No changes to serviceability.','None',1,0,0,'Same suppliers for all components.','None',1,0,0,'','0',1,0,0,'','0',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',25,0.693164,0,0,0,'None','Reliability assessment, FMEA, thermal analysis','None',0.34,0,0,0,0,0,4,5,0,3,0,0,0,0),(1,6,2,'Changing all TTL devices to CMOS devices.','Low',1,21,22000,'Will be required to use Pb free solder.','High',1.5,0,0,'No change in usage.','None',1,0,0,'No change to stresses.','None',1,0,0,'No changes to serviceability.','None',1,0,0,'Same suppliers for all components.','None',1,0,0,'','0',1,0,0,'','0',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',22.2222,57.6287,0,0,0,'None','Reliability assessment, FMEA, thermal analysis','None',0.33,0,0,0,0,0,3,5,0,0,0,0,0,0),(1,7,3,'Changing all TTL devices to CMOS devices.  Changing all logic devices from +5VDC to +2.7VDC.','High',1.5,0,0,'','None',1,0,0,'None','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',0,0,0,0,0,'','','',1,0,0,0,0,0,0,0,0,0,0,0,0,0),(1,8,4,'Changing all resistors to metal film.  Changing all capacitors to SMT chip types.','Low',1.1,14,12000,'Will be required to use Pb free solder.','High',1.5,0,0,'No change in usage.','None',1,0,0,'No change to stresses.','None',1,0,0,'No changes to serviceability.','None',1,0,0,'Same suppliers for all components.','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',22.2222,17.0409,0,0,0,'','Reliability assessment, FMEA, thermal analysis','',0.33,0,0,0,0,0,3,5,0,0,0,0,0,0),(1,10,5,'','None',1,0,0,'','None',1,0,0,NULL,'None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',0,0,0,0,0,'','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0),(1,11,6,'','None',1,0,0,'','None',1,0,0,NULL,'None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',0,0,0,0,0,'','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0),(1,12,7,'','None',1,0,0,'','None',1,0,0,NULL,'None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',0,0,0,0,0,'','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0),(1,13,8,'','None',1,0,0,'','None',1,0,0,NULL,'None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',0,0,0,0,0,'','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0),(1,14,9,'','None',1,0,0,'','None',1,0,0,NULL,'None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'','None',1,0,0,'((cat1/36.0)+(cat2/36.0)+(cat3/36.0)+(cat4/36.0)+(cat5/36.0)+(cat6/36.0))*100','hr*pi1*pi2*pi3*pi4*pi5*pi6','','','',0,0,0,0,0,'','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `tbl_similar_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_system`
--

DROP TABLE IF EXISTS `tbl_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_system` (
  `fld_revision_id` int(11) NOT NULL,
  `fld_assembly_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_add_adj_factor` float NOT NULL DEFAULT '0',
  `fld_allocation_wt_factor` float NOT NULL DEFAULT '0',
  `fld_alt_part_number` varchar(128) DEFAULT '',
  `fld_assembly_criticality` float NOT NULL DEFAULT '0',
  `fld_attachments` varchar(256) DEFAULT '',
  `fld_availability` float NOT NULL DEFAULT '1',
  `fld_availability_mission` float NOT NULL DEFAULT '1',
  `fld_cage_code` varchar(64) DEFAULT '',
  `fld_calculation_model` int(11) NOT NULL DEFAULT '1',
  `fld_category_id` int(11) NOT NULL DEFAULT '0',
  `fld_comp_ref_des` varchar(128) DEFAULT '',
  `fld_cost` float NOT NULL DEFAULT '0',
  `fld_cost_failure` float NOT NULL DEFAULT '0',
  `fld_cost_hour` float NOT NULL DEFAULT '0',
  `fld_cost_type` int(11) NOT NULL DEFAULT '1',
  `fld_description` varchar(256) DEFAULT '',
  `fld_detection_fr` float NOT NULL DEFAULT '0',
  `fld_detection_percent` float NOT NULL DEFAULT '100',
  `fld_duty_cycle` float NOT NULL DEFAULT '100',
  `fld_entered_by` varchar(64) DEFAULT '',
  `fld_environment_active` int(11) NOT NULL DEFAULT '0',
  `fld_environment_dormant` int(11) NOT NULL DEFAULT '0',
  `fld_failure_dist` int(11) NOT NULL DEFAULT '0',
  `fld_failure_parameter_1` float NOT NULL DEFAULT '0',
  `fld_failure_parameter_2` float NOT NULL DEFAULT '0',
  `fld_failure_parameter_3` float NOT NULL DEFAULT '0',
  `fld_failure_rate_active` float NOT NULL DEFAULT '0',
  `fld_failure_rate_dormant` float NOT NULL DEFAULT '0',
  `fld_failure_rate_mission` float NOT NULL DEFAULT '0',
  `fld_failure_rate_percent` float NOT NULL DEFAULT '0',
  `fld_failure_rate_predicted` float NOT NULL DEFAULT '0',
  `fld_failure_rate_software` float NOT NULL DEFAULT '0',
  `fld_failure_rate_specified` float NOT NULL DEFAULT '0',
  `fld_failure_rate_type` int(11) NOT NULL DEFAULT '2' COMMENT 'How failure rates are assigned:  1=Allocated; 2=Assessed; 3=Specified, Hazard Rate; 4=Specified, MTBF',
  `fld_figure_number` varchar(32) DEFAULT '',
  `fld_humidity` float NOT NULL DEFAULT '50',
  `fld_image_file` varchar(128) DEFAULT '',
  `fld_isolation_fr` float NOT NULL DEFAULT '0',
  `fld_isolation_percent` float NOT NULL DEFAULT '0',
  `fld_lcn` varchar(128) DEFAULT '',
  `fld_level` int(11) NOT NULL DEFAULT '1',
  `fld_manufacturer` int(11) NOT NULL DEFAULT '0',
  `fld_mcmt` float NOT NULL DEFAULT '0',
  `fld_mission_time` float NOT NULL DEFAULT '100',
  `fld_mmt` float NOT NULL DEFAULT '0',
  `fld_modified_by` varchar(64) DEFAULT '',
  `fld_mpmt` float NOT NULL DEFAULT '0',
  `fld_mtbf_mission` float NOT NULL DEFAULT '0',
  `fld_mtbf_predicted` float NOT NULL DEFAULT '0',
  `fld_mtbf_specified` float NOT NULL DEFAULT '0',
  `fld_mttr` float NOT NULL DEFAULT '0',
  `fld_mttr_add_adj_factor` float NOT NULL DEFAULT '1',
  `fld_mttr_mult_adj_factor` float NOT NULL DEFAULT '0',
  `fld_mttr_specified` float NOT NULL DEFAULT '0',
  `fld_mttr_type` int(11) NOT NULL DEFAULT '1',
  `fld_mult_adj_factor` float NOT NULL DEFAULT '1',
  `fld_name` varchar(256) DEFAULT '',
  `fld_nsn` varchar(32) DEFAULT '',
  `fld_overstress` tinyint(4) NOT NULL DEFAULT '0',
  `fld_page_number` varchar(32) DEFAULT '',
  `fld_parent_assembly` varchar(16) NOT NULL DEFAULT '0',
  `fld_part` tinyint(4) NOT NULL DEFAULT '0',
  `fld_part_number` varchar(128) DEFAULT '',
  `fld_percent_isolation_group_ri` float NOT NULL DEFAULT '0',
  `fld_percent_isolation_single_ri` float NOT NULL DEFAULT '0',
  `fld_quantity` int(11) NOT NULL DEFAULT '1',
  `fld_ref_des` varchar(128) DEFAULT '',
  `fld_reliability_mission` float NOT NULL DEFAULT '1',
  `fld_reliability_predicted` float NOT NULL DEFAULT '1',
  `fld_remarks` longblob,
  `fld_repair_dist` int(11) NOT NULL DEFAULT '0',
  `fld_repair_parameter_1` float NOT NULL DEFAULT '0',
  `fld_repair_parameter_2` float NOT NULL DEFAULT '0',
  `fld_repairable` tinyint(4) NOT NULL DEFAULT '0',
  `fld_rpm` float NOT NULL DEFAULT '0',
  `fld_specification_number` varchar(64) DEFAULT '',
  `fld_subcategory_id` int(11) NOT NULL DEFAULT '0',
  `fld_tagged_part` tinyint(4) NOT NULL DEFAULT '0',
  `fld_temperature_active` float NOT NULL DEFAULT '30',
  `fld_temperature_dormant` float NOT NULL DEFAULT '30',
  `fld_total_part_quantity` int(11) NOT NULL DEFAULT '0',
  `fld_total_power_dissipation` float NOT NULL DEFAULT '0',
  `fld_vibration` float NOT NULL DEFAULT '0',
  `fld_weibull_data_set` int(11) NOT NULL DEFAULT '1',
  `fld_weibull_file` varchar(128) DEFAULT '',
  `fld_year_of_manufacture` int(11) NOT NULL DEFAULT '2010',
  `fld_ht_model` varchar(512) DEFAULT 'None',
  PRIMARY KEY (`fld_revision_id`,`fld_assembly_id`),
  KEY `fld_assembly_id` (`fld_assembly_id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_system`
--

LOCK TABLES `tbl_system` WRITE;
/*!40000 ALTER TABLE `tbl_system` DISABLE KEYS */;
INSERT INTO `tbl_system` VALUES (1,1,0,0,'',0,'',1,1,'34335',1,0,'S1',21.71,0.004463,0.001056,1,'Example System #1',0,100,100,'',2,1,0,0,0,0,45.4075,3.23556,33.6766,0.000993,48.6431,0,0,2,'',50,'',0,0,'',0,-1,0,100,0,'',0,22022.8,20557.9,0,0,1,0,48,2,1,'','',0,'','-',0,'EXS1',0,0,1,'S1',0.99547,0.995148,'',0,0,0,1,0,'',0,0,30,25,181,138.435,0,0,'',2010,''),(1,2,0,0,'',0,'',1,1,'01295',1,0,'S1:SS1',7.51,0.162516,3e-06,1,'Integrated Circuit Subsystem',0,100,100,'',2,1,0,0,0,0,0.365037,0.097072,0.351465,0.000273,0.462109,0,0,2,'',50,'',0,0,'',1,-1,0,100,0,'',0,2.73945e+06,2.16399e+06,0,0,1,0,48,2,1,'','',0,'','0',0,'EXSSS1',0,0,1,'SS1',0.999964,0.999954,'',0,0,0,1,0,'',0,0,30,25,10,1.143,0,1,'',2010,'None'),(1,6,0,0,'None',0,'None',1,1,'',1,0,'S1:SS2',14.11,0.003673,0.000542,1,'Integrated Circuit & Semiconductor Subsystem',0,100,100,'root',2,1,0,0,0,0,36.3644,2.05461,26.8757,0.73639,38.4191,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,27499.4,26028.7,0,0,1,0,0,1,1,'','None',0,'None','0',0,'EXSSS2',0,0,1,'SS2',0.99637,0.996165,'',0,0,0,1,0,'None',0,0,30,25,18,112.762,0,1,'None',2010,'None'),(1,7,0,0,'None',0,'None',1,1,'34335',1,0,'S1:SS1:A11',7.51,0.162516,3e-06,1,'Carrier Board for Integrated Circuits',0,100,100,'root',2,1,0,0,0,0,0.365037,0.097072,0.351465,0.000273,0.462109,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,2.73945e+06,2.16399e+06,0,0,1,0,0,1,1,'IC Carrier 1','None',0,'None','0:0',0,'EXS1A11',0,0,1,'A11',0.999964,0.999954,'',0,0,0,1,0,'None',0,0,30,28,10,1.143,0,1,'None',2010,'None'),(1,8,0,0,'None',0,'None',1,1,'',1,0,'S1:SS3',0.09,8.7e-05,1e-06,1,'Passive Component Subsystem',0,100,100,'root',2,1,0,0,0,0,9.19213,1.13568,6.18819,0.174954,10.3278,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,108789,96825.9,0,0,1,0,0,1,1,'','None',0,'None','0',0,'EXSSS3',0,0,1,'SS3',0.999081,0.998968,'',0,0,0,1,0,'None',0,0,30,25,153,24.33,0,1,'None',2010,'None'),(1,10,0,0,'None',0,'None',1,1,'34335',1,0,'S1:SS3:A31',0,0,0,1,'Resistor Assembly',0,100,90,'root',2,1,0,0,0,0,3.85486,0.373973,1.99048,0.056706,4.22883,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,259413,236472,0,0,1,0,0,1,1,'Resistor Carrier','None',0,'None','0:2',0,'EXSSS3A1',0,0,1,'A31',0.999615,0.999577,'',0,0,0,1,0,'None',0,0,30,30,12,1.855,0,1,'None',2010,'None'),(1,11,0,0,'None',0,'None',1,1,'34335',1,0,'S1:SS3:A32',0.09,0.000247,0,1,'Capacitor Assembly',0,100,100,'root',2,1,0,0,0,0,3.46321,0.173161,3.46321,0.093946,3.63637,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,288749,274999,0,0,1,0,0,1,1,'Capacitor Carrier','None',0,'None','0:2',0,'EXSSS3A32',0,0,1,'A32',0.999654,0.999636,'',0,0,0,1,0,'None',0,0,30,30,16,16.95,0,1,'None',2010,'None'),(1,12,0,0,'None',0,'None',1,1,'',1,0,'S1:SS2:A21',12.5,0.062284,2.5e-05,1,'Carrier Board for Integrated Circuits, Special Duty',0,100,100,'root',2,1,0,0,0,0,1.67244,0.334489,0.12536,0.00661,2.00693,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,597927,498273,0,0,1,0,0,1,1,'IC Carrier 2','None',0,'None','0:1',0,'EXS1A21',0,0,1,'A21',0.999833,0.999799,'',0,0,0,0,0,'None',0,0,30,30,3,65,0,1,'None',2010,'None'),(1,13,0,0,'None',0,'None',1,1,'34335',1,0,'S1:SS2:A22',1.61,0.001805,1.4e-05,1,'Diode Carrier Board',0,100,100,'root',2,1,0,0,0,0,8.2582,0.660656,10.6785,0.000226,8.91886,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,121092,112122,0,0,1,0,0,1,1,'Diode Carrier','None',0,'None','0:1',0,'EXS1A22',0,0,1,'A22',0.999175,0.999108,'',0,0,0,1,0,'None',0,0,30,30,5,0.357,0,1,'None',2010,'None'),(1,14,0,0,'None',0,'None',1,1,'',1,0,'S1:SS2:A23',0,0,0,1,'Semiconductor Carrier Board',0,100,100,'root',2,1,0,0,0,0,26.4338,1.05947,16.0718,0.431828,27.4933,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,37830.4,36372.5,0,0,1,0,0,1,1,'Transistor Carrier','None',0,'None','0:1',0,'EXS1A23',0,0,1,'A23',0.99736,0.997254,'',0,0,0,1,0,'None',0,0,30,30,10,47.405,0,1,'None',2010,'None'),(1,26,0,0,'None',0,'None',1,1,'',1,4,'S1:SS2:A21:U211',0,0,0,1,'Digital GaAs',0,100,100,'root',2,1,0,0,0,0,0.488667,0.097733,1.9e-05,0.012055,0.586401,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,2.04638e+06,1.70532e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:1:0',1,'None',0,0,1,'U211',0.999951,0.999941,'',0,0,0,0,0,'None',1,0,30,30,1,0,0,1,'None',2010,'[(\'piL\', 1.484131591025766), (\'piA\', 1.0), (\'equation\', \'(C1 * piT * piA + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.016462440384557468), (\'piQ\', 10.0), (\'C1\', 51.0), (\'piT\', 2.4760397501677523e-08)]'),(1,27,0,0,'',0,'None',1,1,'27014',1,4,'S1:SS1:A11:U111',2.95,2.45171,1e-06,1,'Amplifier, Operational, High Voltage',0,100,100,'root',2,1,0,0,0,0,0.030081,0.030081,0.216884,0.001237,0.060162,0,0,2,'None',50,'None',0,0,'None',1,1,0,100,0,'None',0,3.32435e+07,1.66218e+07,0,0,1,0,0,1,1,'','None',1,'None','0:0:0',1,'LM143H',0,0,5,'U111',0.999997,0.999994,'',0,0,0,0,0,'None',3,0,30,30,5,0.75,0,1,'None',2007,'[(\'piL\', 0.5193536683483142), (\'equation\', \'(C1 * piT + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.008665352680402862), (\'piQ\', 2.0), (\'C1\', 0.059999998658895493), (\'piT\', 0.19382273064597905)]'),(1,28,0,0,'None',0,'30.0',1,1,'0GD60',1,4,'S1:SS1:A11:U112',0.38,0.166916,0,1,'Inverter. Hex',0,100,100,'root',2,1,0,0,0,0,0.018972,0.003794,0.018972,0.000468,0.022766,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,5.27102e+07,4.39252e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:0:0',1,'SN74LS04N',0,0,1,'U112',0.999998,0.999998,'',0,0,0,0,0,'None',4,0,30,30,1,0.05,0,1,'None',2010,'[(\'piL\', 0.25790339917193061), (\'equation\', \'(C1 * piT + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.011822792954742348), (\'piQ\', 2.0), (\'C1\', 0.079999998211860657), (\'piT\', 0.16418710978699974)]'),(1,29,0,0,'None',0,'None',1,1,'34335',1,4,'S1:SS2:A21:U212',0,0,0,1,'MMIC GaAs',0,100,100,'root',2,1,0,0,0,0,0.741883,0.148377,1e-06,0.018302,0.890259,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.34792e+06,1.12327e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:1:0',1,'None',0,0,1,'U212',0.999926,0.999911,'',0,0,0,0,0,'None',2,0,30,30,1,0,0,1,'None',2010,'[(\'piL\', 1.484131591025766), (\'piA\', 1.0), (\'equation\', \'(C1 * piT * piA + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'piQ\', 10.0), (\'C2\', 0.02499380650099927), (\'C1\', 7.1999998092651367), (\'piT\', 8.3537823567415923e-09)]'),(1,30,0,0,'None',0,'None',1,1,'',1,4,'S1:SS2:A21:U213',12.5,0.235728,7e-06,1,'Microprocessor, 64-Bit, Single Core',0,100,100,'root',2,1,0,0,0,0,0.441894,0.088379,0.12534,0.010901,0.530273,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,2.26299e+06,1.88582e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:1:0',1,'ADA3200AEP5AP',0,0,1,'U213',0.999956,0.999947,'',0,0,0,0,0,'None',9,0,30,30,1,65,0,1,'None',2008,'[(\'piL\', 0.25790339917193061), (\'equation\', \'(C1 * piT + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.45513068135022555), (\'piQ\', 1.0), (\'C1\', 1.1200000047683716), (\'piT\', 0.71709563921185171)]'),(1,37,0,0,'None',0,'30.0',1,1,'0AX86',1,4,'S1:SS1:A11:U113',2.59,0.091295,1e-06,1,'512 Kbit Serial SPI Bus EEPROM with High Speed Clock',0,100,100,'andrew',2,1,0,0,0,0,0.236413,0.047283,0.170578,0.005832,0.283696,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,4.22988e+06,3.5249e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:0:0',1,'M95512-DR',0,0,1,'U113',0.999976,0.999972,'',0,0,0,0,0,'None',6,0,30,30,1,0.043,0,1,'None',2010,'[(\'piL\', 0.36598234443677974), (\'lambdaCYC\', 0.62124278107911612), (\'equation\', \'(C1 * piT + C2 * piE + lambdaCYC) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.011822792954742348), (\'piQ\', 1.0), (\'C1\', 0.0068000000901520252), (\'piT\', 0.15897487544666097), (\'piECC\', 0.68000000000000005)]'),(1,39,0,0,'None',0,'None',1,1,'01295',1,4,'S1:SS1:A11:U114',0,0,0,1,'Memory, Dynamic RAM',0,100,100,'andrew',2,1,0,0,0,0,0.006478,0.001296,0.000708,0.00016,0.007773,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,1.54379e+08,1.28649e+08,0,0,1,0,0,1,1,'None','None',0,'None','0:0:0',1,'MM5290',0,0,1,'U114',0.999999,0.999999,'',0,0,0,0,0,'None',5,0,30,30,1,0.3,0,1,'None',2010,'[(\'piL\', 0.25790339917193061), (\'equation\', \'(C1 * piT + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.005592520859079222), (\'piQ\', 2.0), (\'C1\', 0.0024999999441206455), (\'piT\', 0.54924174251440661)]'),(1,40,0,0,'None',0,'30.0',1,1,'01295',1,4,'S1:SS1:A11:U115',1.59,0.266442,0,1,'Memory, ROM',0,100,100,'andrew',2,1,0,0,0,0,0.049729,0.009946,0.049729,0.001227,0.059675,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,2.01088e+07,1.67573e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:0:0',1,'MM5211',0,0,1,'U115',0.999995,0.999994,'',0,0,0,0,0,'None',7,0,30,30,1,0,0,1,'None',2010,'[(\'piL\', 1.0458498557711413), (\'equation\', \'(C1 * piT + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.011822792954742348), (\'piQ\', 2.0), (\'C1\', 0.0008500000112690032), (\'piT\', 0.1518470762590093)]'),(1,41,0,0,'None',0,'None',1,1,'01295',1,4,'S1:SS1:A11:U116',0,0,0,1,'Memory, Static RAM',0,100,100,'andrew',2,1,0,0,0,0,0.023364,0.004673,0.003036,0.000576,0.028036,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,4.28018e+07,3.56681e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:0:0',1,'MM5290',0,0,1,'U116',0.999998,0.999997,'',0,0,0,0,0,'None',8,0,30,30,1,0,0,1,'None',2010,'[(\'piL\', 0.1817414536944306), (\'equation\', \'(C1 * piT + C2 * piE) * piQ * piL\'), (\'piE\', 2.0), (\'C2\', 0.005592520859079222), (\'piQ\', 10.0), (\'C1\', 0.010999999940395355), (\'piT\', 0.1518470762590093)]'),(1,42,0,0,'None',0,'None',1,1,'81978',1,9,'S1:SS2:A22:CR221',0,0,0,1,'Band Switching Diode',0,100,100,'andrew',2,1,0,0,0,0,3.63988,0.29119,9.09969,0.080815,3.93107,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,274735,254384,0,0,1,0,0,1,1,'Diode, High Frequency','None',0,'None','0:1:1',1,'1SS356',0,0,1,'CR221',0.999636,0.999607,'',0,0,0,0,0,'None',1,0,30,30,1,0.25,0,1,'None',2010,'[(\'piA\', 1.0), (\'equation\', \'lambdab * piT * piA * piR * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 0.2199999988079071), (\'piQ\', 5.0), (\'piR\', 1.0), (\'piT\', 1.6544894122285279)]'),(1,43,0,0,'None',0,'None',1,1,'01295',1,9,'S1:SS2:A22:CR222',0,0,0,1,'Dual Series Switching Diode',0,100,100,'andrew',2,1,0,0,0,0,0.010327,0.000826,0.003688,0.000229,0.011153,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,9.68355e+07,8.96625e+07,0,0,1,0,0,1,1,'Diode, Small Signal, Silicon','None',0,'None','0:1:1',1,'BAV99LTG',0,0,1,'CR222',0.999999,0.999999,'',0,0,0,0,0,'None',2,0,30,30,1,0.087,0,1,'None',2010,'[(\'equation\', \'lambdab * piT * piS * piC * piQ * piE\'), (\'piC\', 2.0), (\'piE\', 6.0), (\'lambdab\', 0.0010000000474974513), (\'piQ\', 2.4000000953674316), (\'piS\', 0.074186533801483504), (\'piT\', 4.8333443392012301)]'),(1,44,0,0,'None',0,'None',1,1,'81978',1,9,'S1:SS2:A22:U223',1.61,0.369789,0,1,'Single Digit LED Numeric Display',0,100,100,'andrew',2,1,0,0,0,0,0.060322,0.003225,0.040313,0.000895,0.043538,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,2.48057e+07,2.29683e+07,0,0,1,0,0,1,1,'Display, Ones Position','None',1,'None','0:1:1',1,'LF-301VA',0,0,1,'U223',0.999996,0.999996,'',0,0,0,0,0,'None',3,0,30,30,1,0.22,0,1,'None',2010,'[(\'piQ\', 5.5), (\'equation\', \'lambdab * piT * piQ * piE\'), (\'piT\', 1.8218514988002814), (\'piE\', 2.0), (\'lambdab\', 0.0030100000000000001)]'),(1,45,0,0,'None',0,'None',1,1,'',1,9,'S1:SS2:A23:CR231',0,0,0,1,'Rectifier, Silicon Controlled',0,100,100,'andrew',2,1,0,0,0,0,0.012543,0.001003,0.012543,0.000278,0.013547,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,7.97249e+07,7.38194e+07,0,0,1,0,0,1,1,'None','None',1,'None','0:1:2',1,'None',0,0,1,'CR231',0.999999,0.999999,'',0,0,0,0,0,'None',6,0,30,30,1,0,0,1,'None',2010,'[(\'equation\', \'lambdab * piT * piR * piS * piQ * piE\'), (\'piE\', 6.0), (\'lambdab\', 0.0022000000000000001), (\'piQ\', 2.4000000953674316), (\'piR\', 1.9036539387158786), (\'piS\', 0.1753533162216348), (\'piT\', 1.1860930060934465)]'),(1,47,0,0,'None',0,'None',1,1,'0AX86',1,9,'S1:SS2:A22:CR224',0,0,0,1,'Diode, LED, Yellow',0,100,100,'andrew',2,1,0,0,0,0,0.001288,0.000103,0.001288,2.9e-05,0.001392,0,0,2,'None',50,'None',0,0,'None',1,-1,0,100,0,'None',0,7.7613e+08,7.18639e+08,0,0,1,0,0,1,1,'None','None',1,'None','0:1:1',1,'None',0,0,1,'CR224',1,1,'',0,0,0,0,0,'None',4,0,30,30,1,0,0,1,'None',2010,'[(\'piQ\', 2.4000000953674316), (\'equation\', \'lambdab * piT * piQ * piE\'), (\'piT\', 1.1670688106813309), (\'piE\', 2.0), (\'lambdab\', 0.00023000000510364771)]'),(1,48,0,0,'None',0,'None',1,1,'',1,9,'S1:SS2:A22:CR225',0,0,0,1,'Diode, Laser, 1024MHz',0,100,100,'andrew',2,1,0,0,0,0,4.5664,0.365312,1.53353,0.101386,4.93171,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,218991,202769,0,0,1,0,0,1,1,'None','None',1,'None','0:1:1',1,'None',0,0,1,'CR225',0.999543,0.999507,'',0,0,0,0,0,'None',5,0,30,30,1,0,0,1,'None',2010,'[(\'piI\', 0.081395277903921023), (\'piA\', 8.0622577482985491), (\'equation\', \'lambdab * piT * piI * piA * piP * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 3.2300000190734863), (\'piP\', 0.83333334161175632), (\'piQ\', 1.0), (\'piT\', 1.2926075983786154)]'),(1,49,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R311',0,0,0,1,'Conformal, Single In-Line Resistor, Through Hole Network (Standard)',0,100,90,'andrew',2,1,0,0,0,0,0,0,0,0,0,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,2.26013e+14,2.05466e+14,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'VTF366BX',0,0,1,'R311',1,1,'',0,0,0,0,0,'None',3,0,30,30,1,0.05,0,1,'None',2010,'[(\'equation\', \'lambdab * piT * piNR * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 6.0000000000000002e-05), (\'piQ\', 3.0), (\'piNR\', 8), (\'piR\', 1.0), (\'piT\', 1.5362923430206255e-06)]'),(1,50,0,0,'RNR75',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R312',0,0,0,1,'Metal Film Resistors, Military/Established Reliability, Hermetically-Sealed',0,100,90,'andrew',2,1,0,0,0,0,0.033934,0.003393,0.030541,0.000767,0.037328,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,2.94688e+07,2.67898e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'HDN75',0,0,1,'R312',0.999997,0.999996,'',0,0,0,0,0,'None',4,0,30,30,1,0.125,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piR * piQ * piE\'), (\'piR\', 1.2000000476837158), (\'lambdab\', 0.014139233556023399), (\'piE\', 2.0)]'),(1,53,0,0,'None',0,'None',1,1,'34335',1,9,'S1:SS2:A23:Q232',0,0,0,1,'Microwave Power MES FET',0,100,100,'andrew',2,1,0,0,0,0,20.9547,0.838189,10.4774,0.448016,21.7929,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,47721.9,45886.4,0,0,1,0,0,1,1,'None','None',1,'None','0:1:2',1,'MGF1954A',0,0,1,'Q232',0.997907,0.997823,'',0,0,0,0,0,'None',7,0,30,30,1,2.25,0,1,'None',2005,'[(\'piM\', 4.0), (\'piA\', 4.0), (\'equation\', \'lambdab * piT * piA * piM * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 0.2371076838450342), (\'piQ\', 2.0), (\'piT\', 1.3808821418871904)]'),(1,54,0,0,'None',0,'None',1,1,'34335',1,9,'S1:SS2:A23:Q233',0,0,0,1,'High Power NPN Epitaxial Planar Bipolar Transistor',0,100,100,'andrew',2,1,0,0,0,0,1.9687,0.078748,1.9687,0.042091,2.04744,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,507951,488414,0,0,1,0,0,1,1,'None','None',1,'None','0:1:2',1,'2STC4468',0,0,1,'Q233',0.999803,0.999795,'',0,0,0,0,0,'None',8,0,30,30,1,42,0,1,'None',2010,'[(\'piM\', 4.0), (\'piA\', 7.5999999999999996), (\'equation\', \'lambdab * piT * piA * piM * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 0.23748296695051302), (\'piQ\', 2.0), (\'piT\', 0.06817299899266209)]'),(1,55,0,0,'None',0,'None',1,1,'None',1,9,'S1:SS2:A23:Q234',0,0,0,1,'Low Noise Silicon Bipolar Transistor',0,100,100,'andrew',2,1,0,0,0,0,1.43526,0.05741,1.43526,0.030686,1.49267,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,696738,669940,0,0,1,0,0,1,1,'None','None',0,'None','0:1:2',1,'AT-41535',0,0,1,'Q234',0.999856,0.999851,'',0,0,0,0,0,'None',9,0,30,30,1,0.25,0,1,'None',2010,'[(\'equation\', \'lambdab * piT * piR * piS * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 0.17999999999999999), (\'piQ\', 2.0), (\'piR\', 0.77378249677119493), (\'piS\', 2.1644341197691994), (\'piT\', 1.1902413847594255)]'),(1,56,0,0,'None',0,'None',1,1,'34335',1,9,'S1:SS2:A23:Q235',0,0,0,1,'N-Channel Junction Silicon FET',0,100,100,'andrew',2,1,0,0,0,0,0.133919,0.005357,0.266996,0.002863,0.139275,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,7.46723e+06,7.18003e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:1:2',1,'2SK932',0,0,1,'Q235',0.999987,0.999986,'',0,0,0,0,0,'None',10,0,30,30,1,0.03,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piT * piQ * piE\'), (\'piT\', 1.1159876418609065), (\'piE\', 2.0), (\'lambdab\', 0.059999998658895493)]'),(1,57,0,0,'None',0,'None',1,1,'None',1,9,'S1:SS2:A23:Q236',0,0,0,1,'Low Frequency NPN Bipolar Transistor',0,100,100,'andrew',2,1,0,0,0,0,0.000699,2.8e-05,0.000699,1.5e-05,0.000727,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.42963e+09,1.37465e+09,0,0,1,0,0,1,1,'None','None',0,'None','0:1:2',1,'2N2222A',0,0,1,'Q236',1,1,'',0,0,0,0,0,'None',11,0,30,30,1,0.25,0,1,'None',2010,'[(\'piA\', 1.5), (\'equation\', \'lambdab * piT * piR * piS * piQ * piE\'), (\'piE\', 6.0), (\'lambdab\', 0.00073999999999999999), (\'piQ\', 1.0), (\'piR\', 0.77378249677119493), (\'piS\', 0.13736787336114123), (\'piT\', 1.4821360076815207)]'),(1,58,0,0,'None',0,'None',1,1,'None',1,9,'S1:SS2:A23:Q237',0,0,0,1,'Low Frequency Silicon FET',0,100,100,'andrew',2,1,0,0,0,0,1.89108,0.075643,1.89108,0.040432,1.96672,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,528799,508460,0,0,1,0,0,1,1,'None','None',0,'None','0:1:2',1,'None',0,0,1,'Q237',0.999811,0.999803,'',0,0,0,0,0,'None',12,0,30,30,1,2,0,1,'None',2010,'[(\'piA\', 4.0), (\'equation\', \'lambdab * piT * piA * piQ * piE\'), (\'piE\', 6.0), (\'lambdab\', 0.012000000104308128), (\'piQ\', 2.4000000953674316), (\'piT\', 2.7359363983031812)]'),(1,59,0,0,'None',0,'None',1,1,'34335',1,9,'S1:SS2:A23:Q238',0,0,0,1,'Transisitor, Unijunctions',0,100,100,'andrew',2,1,0,0,0,0,0.009969,0.000399,0.009969,0.000213,0.010367,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.00315e+08,9.64569e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:1:2',1,'None',0,0,1,'Q238',0.999999,0.999999,'',0,0,0,0,0,'None',13,0,30,30,1,0,0,1,'None',2010,'[(\'piQ\', 8.0), (\'equation\', \'lambdab * piT * piQ * piE\'), (\'piT\', 1.147396305341051), (\'piE\', 6.0), (\'lambdab\', 0.00018099999579135329)]'),(1,60,0,0,'None',0,'None',1,1,'',1,8,'S1:SS2:A23:R231',0,0,0,1,'Fixed Composition Resistor',0,100,100,'andrew',2,1,0,0,0,0,0.006887,0.000689,0.006887,0.000156,0.007576,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.45198e+08,1.31998e+08,0,0,1,0,0,1,1,'None','None',0,'None','0:1:2',1,'None',0,0,1,'R231',0.999999,0.999999,'',0,0,0,0,0,'None',1,0,30,30,1,0.125,0,1,'None',2010,'[(\'piQ\', 5.0), (\'equation\', \'lambdab * piR * piQ * piE\'), (\'piR\', 1.6000000238418579), (\'lambdab\', 0.00028696475996073715), (\'piE\', 3.0)]'),(1,61,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS2:A23:R232',0,0,0,1,'Fixed Film Resistor',0,100,100,'andrew',2,1,0,0,0,0,0.020013,0.002001,0.011489,0.000453,0.022014,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,4.99679e+07,4.54254e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:1:2',1,'None',0,0,1,'R232',0.999998,0.999998,'',0,0,0,0,0,'None',2,0,30,30,1,0.5,0,1,'None',2010,'[(\'piQ\', 5.0), (\'equation\', \'lambdab * piR * piQ * piE\'), (\'piR\', 1.6000000238418579), (\'lambdab\', 0.0012508028757314985), (\'piE\', 2.0)]'),(1,62,0,0,'None',0,'None',1,1,'13606',1,8,'S1:SS3:A31:R313',0,0,0,1,'Wirewound Resistor, Precision Power, Surface Mount',0,100,90,'andrew',2,1,0,0,0,0,0.002298,0.00023,0.006895,5.2e-05,0.002528,0,0,2,'None',50,'None',0,0,'None',1,2,0,100,0,'None',0,4.35117e+08,3.95561e+08,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'WSC01/2',0,0,1,'R313',1,1,'',0,0,0,0,0,'None',5,0,30,30,1,0.125,0,1,'None',2010,'[(\'piQ\', 0.30000001192092896), (\'equation\', \'lambdab * piR * piQ * piE\'), (\'piR\', 1.0), (\'lambdab\', 0.0038303848559076508), (\'piE\', 2.0)]'),(1,64,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R314',0,0,0,1,'Wirewound Resistor, Power',0,100,90,'andrew',2,1,0,0,0,0,0.00162,0.000162,0.001458,3.6e-05,0.001782,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,6.17314e+08,5.61195e+08,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R314',1,1,'',0,0,0,0,0,'None',6,0,30,30,1,0.075,0,1,'None',2010,'[(\'piQ\', 0.10000000149011612), (\'equation\', \'lambdab * piR * piQ * piE\'), (\'piR\', 1.0), (\'lambdab\', 0.00809960055287323), (\'piE\', 2.0)]'),(1,66,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R315',0,0,0,1,'Chassis Mount Wirewound Resistor',0,100,90,'andrew',2,1,0,0,0,0,0.000439,4.4e-05,0.000395,1e-05,0.000483,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,2.27564e+09,2.06877e+09,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R315',1,1,'',0,0,0,0,0,'None',7,0,30,30,1,0,0,1,'None',2010,'[(\'piQ\', 0.10000000149011612), (\'equation\', \'lambdab * piR * piQ * piE\'), (\'piR\', 1.0), (\'lambdab\', 0.002197181312105147), (\'piE\', 2.0)]'),(1,68,0,0,'None',0,'None',1,1,'6V793',1,8,'S1:SS3:A31:R316',0,0,0,1,'Thermistor',0,100,90,'andrew',2,1,0,0,0,0,1.575,0.1575,1.4175,0.035207,1.7325,0,0,2,'None',50,'None',0,0,'None',1,2,0,100,0,'None',0,634921,577201,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R316',0.999843,0.999827,'',0,0,0,0,0,'None',8,0,30,30,1,0.05,0,1,'None',2010,'[(\'piQ\', 15.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piR\', 1.0), (\'lambdab\', 0.020999999716877937), (\'piE\', 5.0)]'),(1,69,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R317',0,0,0,1,'Variable Resistor, Composition',0,100,90,'andrew',2,1,0,0,0,0,0.168517,0.016852,0.151666,0.003767,0.185369,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,5.9341e+06,5.39464e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R317',0.999983,0.999981,'',0,0,0,0,0,'None',9,0,30,30,1,0.18,0,1,'None',2010,'[(\'equation\', \'lambdab * piTAPS * piR * piV * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 0.03723578753607105), (\'piTAPS\', 0.9051370849898477), (\'piQ\', 2.5), (\'piR\', 1.0), (\'piV\', 1.0)]'),(1,70,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R318',0,0,0,1,'Variable Resistor, Non-Wirewound',0,100,90,'andrew',2,1,0,0,0,0,0.19422,0,0.209758,0,0,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,0,0,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R318',1,1,'',0,0,0,0,0,'None',10,0,30,30,1,0,0,1,'None',2010,'[(\'equation\', \'lambdab * piTAPS * piR * piV * piQ * piE\'), (\'piE\', 3.0), (\'lambdab\', 0.021674287419116), (\'piTAPS\', 0.9051370849898477), (\'piQ\', 3.0), (\'piR\', 1.100000023841858), (\'piV\', 1.0)]'),(1,71,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R319',0,0,0,1,'Variable Resistor, Film',0,100,90,'andrew',2,1,0,0,0,0,0.201736,0.020174,0,0.00451,0.22191,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,4.95696e+06,4.50633e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R319',0.99998,0.999978,'',0,0,0,0,0,'None',11,0,30,30,1,0.25,0,1,'None',2010,'[(\'equation\', \'lambdab * piTAPS * piR * piV * piQ * piE\'), (\'piE\', 3.0), (\'lambdab\', 0.030955479846161614), (\'piTAPS\', 0.9051370849898477), (\'piQ\', 2.0), (\'piR\', 1.2000000476837158), (\'piV\', 1.0)]'),(1,72,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R320',0,0,0,1,'Variable Resistor, Wirewound',0,100,90,'andrew',2,1,0,0,0,0,0.184443,0.018444,0,0.004123,0.202887,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,5.42173e+06,4.92885e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R320',0.999982,0.99998,'',0,0,0,0,0,'q',12,0,30,30,1,0.25,0,1,'None',2010,'[(\'equation\', \'lambdab * piTAPS * piR * piV * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 0.024258747106771002), (\'piTAPS\', 0.9051370849898477), (\'piQ\', 3.0), (\'piR\', 1.399999976158142), (\'piV\', 1.0)]'),(1,73,0,0,'None',0,'None',1,1,'34335',1,8,'S1:SS3:A31:R321',0,0,0,1,'Variable Resistor, Wirewound, Power',0,100,90,'andrew',2,1,0,0,0,0,0.728309,0.145662,0,0.032561,1.60228,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,686522,624111,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'R321',0.999854,0.99984,'',0,0,0,0,0,'None',13,0,30,30,1,0.25,0,1,'None',2010,'[(\'equation\', \'lambdab * piTAPS * piR * piV * piQ * piE\'), (\'piC\', 2.0), (\'piE\', 3.0), (\'lambdab\', 0.08671674913514311), (\'piTAPS\', 0.9998460969082653), (\'piQ\', 2.0), (\'piR\', 1.399999976158142), (\'piV\', 1.0)]'),(1,74,0,0,'None',0,'None',1,1,'34335',1,1,'S1:SS3:A32:C321',0.09,0.006704,0,1,'Capacitor, Fixed, Paper, Feedthrough',0,100,100,'andrew',2,1,0,0,0,0,0.127855,0.006393,0.127855,0.002414,0.134248,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,7.82134e+06,7.4489e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C321',0.999987,0.999987,'',0,0,0,0,0,'None',13,0,30,30,1,0.05,0,1,'None',2010,'[(\'piQ\', 10.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.3043565048180028), (\'lambdab\', 0.02100420105474339), (\'piE\', 2.0)]'),(1,75,0,0,'None',0,'None',1,1,'34335',1,1,'S1:SS3:A31:C310',0,0,0,1,'Capacitor, Fixed, Paper, Bypass',0,100,90,'andrew',2,1,0,0,0,0,0.230252,0.011513,0.207227,0.004913,0.241765,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,4.34307e+06,4.13626e+06,0,0,1,0,0,1,1,'None','None',0,'None','0:2:0',1,'None',0,0,1,'C310',0.999977,0.999976,'',0,0,0,0,0,'None',12,0,30,30,1,0.5,0,1,'None',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.34496822615300216), (\'lambdab\', 0.11124306212740259), (\'piE\', 2.0)]'),(1,76,0,0,'None',0,'None',1,1,'None',1,1,'S1:SS3:A32:C322',0,0,0,1,'Capacitor, Fixed, Plastic Film',0,100,100,'andrew',2,1,0,0,0,0,0.009697,0.000485,0.009697,0.000183,0.010181,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.03129e+08,9.82181e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C322',0.999999,0.999999,'',0,0,0,0,0,'None',11,0,30,30,1,0.1,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.4882943398397614), (\'lambdab\', 0.009929044658337402), (\'piE\', 2.0)]'),(1,77,0,0,'None',0,'None',1,1,'None',1,1,'S1:SS3:A32:C323',0,0,0,1,'Capacitor, Fixed, Metallized Paper',0,100,100,'andrew',2,1,0,0,0,0,0.055934,0.002797,0.055934,0.001056,0.058731,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.78782e+07,1.70269e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C323',0.999994,0.999994,'',0,0,0,0,0,'None',8,0,30,30,1,1,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.37245722471836185), (\'lambdab\', 0.07508789675584462), (\'piE\', 2.0)]'),(1,78,0,0,'None',0,'None',1,1,'None',1,1,'S1:SS3:A32:C324',0,0,0,1,'Capacitor, Fixed, Metallized Plastic',0,100,100,'andrew',2,1,0,0,0,0,0.014812,0.000741,0.014812,0.00028,0.015553,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,6.75132e+07,6.42983e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C324',0.999999,0.999998,'',0,0,0,0,0,'None',14,0,30,30,1,0.05,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.3684894975457193), (\'lambdab\', 0.0200981631852614), (\'piE\', 2.0)]'),(1,79,0,0,'None',0,'None',1,1,'34335',1,1,'S1:SS3:A32:C325',0,0,0,1,'Capacitor, Fixed, Super-Metallized Plastic',0,100,100,'andrew',2,1,0,0,0,0,0.01454,0.000727,0.01454,0.000275,0.015267,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,6.87778e+07,6.55027e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C325',0.999999,0.999998,'',0,0,0,0,0,'None',15,0,30,30,1,0,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.35881947426857996), (\'lambdab\', 0.010130140246859055), (\'piE\', 4.0)]'),(1,80,0,0,'None',0,'None',1,1,'None',1,1,'S1:SS3:A32:C326',0,0,0,1,'Capacitor, Fixed, Mica',0,100,100,'andrew',2,1,2,0,0,0,9e-06,0,9e-06,0,9e-06,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.14469e+11,1.09018e+11,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C326',1,1,'',0,0,0,0,0,'None',9,0,30,30,1,1,0,1,'None',2010,'[(\'piQ\', 0.10000000149011612), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.0650447896605756), (\'lambdab\', 0.0006715363549738058), (\'piE\', 2.0)]'),(1,81,0,0,'None',0,'None',1,1,'None',1,1,'S1:SS3:A32:C327',0,0,0,1,'Capacitor, Fixed, Mica, Button',0,100,100,'andrew',2,1,0,0,0,0,0.006153,0.000308,0.006153,0.000116,0.00646,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,1.62527e+08,1.54788e+08,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C327',0.999999,0.999999,'',0,0,0,0,0,'None',10,0,30,30,1,0.5,0,1,'None',2010,'[(\'piQ\', 5.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.016637941231604347), (\'lambdab\', 0.036980617699742306), (\'piE\', 2.0)]'),(1,82,0,0,'None',0,'None',1,1,'None',1,1,'S1:SS3:A32:C328',0,0,0,1,'Capacitor, Fixed, Glass',0,100,100,'andrew',2,1,0,0,0,0,0.000237,1.2e-05,0.000237,4e-06,0.000249,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,4.21494e+09,4.01423e+09,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C328',1,1,'',0,0,0,0,0,'None',7,0,30,30,1,10,0,1,'None',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.12370626309055888), (\'lambdab\', 0.00031964328838167394), (\'piE\', 2.0)]'),(1,83,0,0,'None',0,'None',1,1,'None',1,1,'S1:SS3:A32:C329',0,0,0,1,'Capacitor, Fixed, Ceramic, General Purpose',0,100,100,'andrew',2,1,0,0,0,0,0.032716,0.001636,0.032716,0.000618,0.034352,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,3.05662e+07,2.91107e+07,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C329',0.999997,0.999997,'',0,0,0,0,0,'None',1,0,30,30,1,1,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.11555369986073809), (\'lambdab\', 0.1415612976874148), (\'piE\', 2.0)]'),(1,84,0,0,'None',0,'None',1,1,'34335',1,1,'S1:SS3:A32:C330',0,0,0,1,'Capacitor, Fixed, Ceramic, Chip',0,100,100,'andrew',2,1,0,0,0,0,0,0,0,0,0,0,0,2,'None',50,'None',0,0,'None',1,0,0,100,0,'None',0,9.68388e+13,9.22274e+13,0,0,1,0,0,1,1,'None','None',0,'None','0:2:1',1,'None',0,0,1,'C330',1,1,'',0,0,0,0,0,'None',2,0,30,30,1,0,0,1,'None',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.16290812071467506), (\'lambdab\', 3.16940589561122e-08), (\'piE\', 2.0)]'),(1,85,0,0,'',0,'',1,1,'34335',1,1,'S1:SS3:A32:C331',0,0,0,1,'Capacitor, Electrolytic, Tantalum, Non-Solid',0,100,100,'andrew',2,1,0,0,0,0,0.373238,0.018662,0.373238,0.007047,0.3919,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,2.67926e+06,2.55167e+06,0,0,1,0,0,1,1,'None','',0,'','0:2:1',1,'',0,0,1,'C331',0.999963,0.999961,'',0,0,0,0,0,'',5,0,30,30,1,0.25,0,1,'',2010,'[(\'equation\', \'lambdab * piCV * piC * piQ * piE\'), (\'piC\', 2.5), (\'piE\', 2.0), (\'lambdab\', 0.09574372633046183), (\'piQ\', 1.5), (\'piCV\', 0.5197731648600814)]'),(1,86,0,0,'',0,'',1,1,'09969',1,1,'S1:SS3:A32:C332',0,0,0,1,'Capacitor, Electrolytic, Tantalum, Solid',0,100,100,'andrew',2,1,0,0,0,0,0.055137,0.002757,0.055137,0.001176,0.057894,0,0,2,'',50,'',0,0,'',1,11,0,100,0,'',0,1.81366e+07,1.7273e+07,0,0,1,0,0,1,1,'','',0,'','0:2:1',1,'',0,0,1,'C332',0.999994,0.999994,'',0,0,0,0,0,'',6,0,30,30,1,2,0,1,'',2010,'[(\'equation\', \'lambdab * piCV * piSR * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 0.1275875417661124), (\'piQ\', 1.5), (\'piCV\', 0.4365158347281727), (\'piSR\', 0.33)]'),(1,87,0,0,'',0,'',1,1,'34335',1,1,'S1:SS3:A32:C333',0,0,0,1,'Capacitor, Variable, Gas or Vacuum',0,100,100,'andrew',2,1,0,0,0,0,0.208103,0.010405,0.208103,0.003929,0.218508,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,4.80531e+06,4.57648e+06,0,0,1,0,0,1,1,'','',0,'','0:2:1',1,'',0,0,1,'C333',0.999979,0.999978,'',0,0,0,0,0,'',16,0,30,30,1,1,0,1,'',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piCF * piQ * piE\'), (\'piCF\', 0.1), (\'lambdab\', 0.23122582209335835), (\'piE\', 3.0)]'),(1,88,0,0,'',0,'',1,1,'',1,1,'S1:SS3:A32:C334',0,0,0,1,'Capacitor, Variable, Air Trimmer',0,100,100,'andrew',2,1,0,0,0,0,0.747082,0.037354,0.747082,0.014106,0.784436,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,1.33854e+06,1.2748e+06,0,0,1,0,0,1,1,'','',0,'','0:2:1',1,'',0,0,1,'C334',0.999925,0.999922,'',0,0,0,0,0,'',17,0,30,30,1,0,0,1,'',2010,'[(\'piQ\', 5.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 3.0), (\'lambdab\', 0.04980545977214119)]'),(1,89,0,0,'',0,'',1,1,'',1,1,'S1:SS3:A32:C335',0,0,0,1,'Capacitor, Variable Ceramic',0,100,100,'andrew',2,1,0,0,0,0,0.417187,0.020859,0.417187,0.007877,0.438047,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,2.39701e+06,2.28286e+06,0,0,1,0,0,1,1,'','',0,'','0:2:1',1,'',0,0,1,'C335',0.999958,0.999956,'',0,0,0,0,0,'',18,0,30,30,1,0,0,1,'',2010,'[(\'piQ\', 4.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 3.0), (\'lambdab\', 0.03476560466863235)]'),(1,90,0,0,'',0,'',1,1,'',1,1,'S1:SS3:A32:C336',0,0,0,1,'Capacitor, Variable, Piston Type',0,100,100,'andrew',2,1,0,0,0,0,1.40051,0.070026,1.40051,0.026444,1.47054,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,714024,680023,0,0,1,0,0,1,1,'','',0,'','0:2:1',1,'',0,0,1,'C336',0.99986,0.999853,'',0,0,0,0,0,'',19,0,30,30,1,0,0,1,'',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 3.0), (\'lambdab\', 0.15561252346220467)]'),(1,91,0,0,'',0,'',1,1,'34335',1,0,'S1:SS3:A33',0,0,0,1,'Inductor Assembly',0,100,100,'andrew',2,1,0,0,0,0,0.294905,0.009465,1.47452,0.035406,0.30437,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,3.39093e+06,3.28548e+06,0,0,1,0,0,1,1,'Inductor Carrier','',0,'','0:2',0,'EXSSS3A33',0,0,1,'A33',0.99997,0.99997,'',0,0,0,1,0,'',0,0,30,30,5,2.125,0,1,'',2010,'None'),(1,92,0,0,'',0,'',1,1,'34335',1,3,'S1:SS3:A33:T331',0,0,0,1,'Transformer, Audio',0,100,100,'andrew',2,1,0,0,0,0,0.040106,0.001604,0.040106,0.00075,0.04171,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,2.4934e+07,2.3975e+07,0,0,1,0,0,1,1,'','',0,'','0:2:2',1,'',0,0,1,'T331',0.999996,0.999996,'',0,0,0,0,0,'',2,0,30,30,1,0.75,0,1,'',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 6.0), (\'lambdab\', 0.0022281066078266598)]'),(1,93,0,0,'',0,'',1,1,'',1,3,'S1:SS3:A33:T332',0,0,0,1,'Transformer, Power',0,100,100,'andrew',2,1,0,0,0,0,0.044223,0.001769,0.044223,0.000827,0.045992,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,2.26125e+07,2.17428e+07,0,0,1,0,0,1,1,'','',0,'','0:2:2',1,'',0,0,1,'T332',0.999996,0.999995,'',0,0,0,0,0,'',3,0,30,30,1,0,0,1,'',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 6.0), (\'lambdab\', 0.002456854074885161)]'),(1,94,0,0,'',0,'',1,1,'',1,3,'S1:SS3:A33:T333',0,0,0,1,'Transformer, Pulse',0,100,100,'andrew',2,1,0,0,0,0,0.03522,0.001409,0.03522,0.000659,0.036629,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,2.83929e+07,2.73009e+07,0,0,1,0,0,1,1,'','',0,'','0:2:2',1,'',0,0,1,'T333',0.999996,0.999996,'',0,0,0,0,0,'',4,0,30,30,1,1.25,0,1,'',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 6.0), (\'lambdab\', 0.0019566673347924633)]'),(1,95,0,0,'',0,'',1,1,'',1,3,'S1:SS3:A33:T334',0,0,0,1,'Transformer, Radio Frequency',0,100,100,'andrew',2,1,0,0,0,0,0.117075,0.004683,0.117075,0.00219,0.121758,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,8.54156e+06,8.21304e+06,0,0,1,0,0,1,1,'','',0,'','0:2:2',1,'',0,0,1,'T334',0.999988,0.999988,'',0,0,0,0,0,'',5,0,30,30,1,0,0,1,'',2010,'[(\'piQ\', 7.5), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 6.0), (\'lambdab\', 0.002601659091183416)]'),(1,96,0,0,'',0,'',1,1,'',1,3,'S1:SS3:A33:L335',0,0,0,1,'Inductor, Coil',0,100,100,'andrew',2,1,0,0,0,0,0.058281,0,0.058281,0.001048,0.058281,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,1.71584e+07,1.71584e+07,0,0,1,0,0,1,1,'','',0,'','0:2:2',1,'',0,0,1,'L335',0.999994,0.999994,'',0,0,0,0,0,'',1,0,30,30,1,0.125,0,1,'',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piC * piQ * piE\'), (\'piC\', 1.0), (\'piE\', 4.0), (\'lambdab\', 0.004856716852883175)]'),(1,97,0,0,'',0,'',1,1,'34335',1,0,'S1:SS3:A34',0,0,0,1,'Relays, Switches, and Connections',0,100,100,'andrew',2,1,0,0,0,0,1.57916,0.579084,0.479699,0.017106,2.15824,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,633248,463340,0,0,1,0,0,1,1,'Mechanical Device Carrier','',0,'','0:2',0,'EXSSS3A34',0,0,1,'A34',0.999842,0.999784,'',0,0,0,1,0,'',0,0,30,30,120,3.4,0,1,'',2010,'None'),(1,98,0,0,'',0,'',1,1,'34335',1,7,'S1:SS3:A34:K341',0,0,0,1,'Relay, Mechanical',0,100,100,'andrew',2,1,0,0,0,0,0.104521,0.083617,0.209043,0.003383,0.188139,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,9.56741e+06,5.31523e+06,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,2,'K341',0.99999,0.999981,'',0,0,0,0,0,'',1,0,30,30,2,0,0,1,'',2010,'[(\'piL\', 2.7182818284590455), (\'piCYC\', 0.1), (\'equation\', \'lambdab * piL * piC * piCYC * piF * piQ * piE\'), (\'piC\', 3.0), (\'piE\', 2.0), (\'lambdab\', 0.006103381526827279), (\'piF\', 7.0), (\'piQ\', 1.5)]'),(1,99,0,0,'',0,'',1,1,'34335',1,7,'S1:SS3:A34:K342',0,0,0,1,'Relay, Solid State',0,100,100,'andrew',2,1,0,0,0,0,1.2,0.48,0.001221,0.030211,1.68,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,833333,595238,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,1,'K342',0.99988,0.999832,'',0,0,0,0,0,'',2,0,30,30,1,0,0,1,'',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 3.0), (\'lambdab\', 0.4)]'),(1,100,0,0,'',0,'',1,1,'34335',1,1,'S1:SS3:A34:C341',0,0,0,1,'Capacitor, Electrolytic, Fixed, Aluminum',0,100,100,'andrew',2,1,0,0,0,0,0.085735,0.004287,0.085735,0.001619,0.090022,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,1.16638e+07,1.11084e+07,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,1,'C341',0.999991,0.999991,'',0,0,0,0,0,'',4,0,30,30,1,0.2,0,1,'',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.8007167565246432), (\'lambdab\', 0.05353668107161735), (\'piE\', 2.0)]'),(1,101,0,0,'',0,'',1,1,'34335',1,1,'S1:SS3:A34:C342',0,0,0,1,'Capacitor, Dry Electrolytic, Fixed, Aluminum',0,100,100,'andrew',2,1,0,0,0,0,0.156128,0.007806,0.156128,0.002948,0.163934,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,6.405e+06,6.1e+06,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,1,'C342',0.999984,0.999984,'',0,0,0,0,0,'',3,0,30,30,1,0.4,0,1,'',2010,'[(\'piQ\', 3.0), (\'equation\', \'lambdab * piCV * piQ * piE\'), (\'piCV\', 0.6187222850465108), (\'lambdab\', 0.042056561643852866), (\'piE\', 2.0)]'),(1,102,0,0,'',0,'',1,1,'34335',1,2,'S1:SS3:A34:J341',0,0,0,1,'Socket, IC, 16-Pin',0,100,100,'andrew',2,1,0,0,0,0,0.007268,0.001454,0.003425,7.4e-05,0.008722,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,1.37583e+08,1.14653e+08,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,1,'J341',0.999999,0.999999,'',0,0,0,0,0,'',4,0,30,30,1,0,0,1,'',2010,'[(\'piP\', 5.768522319848014), (\'equation\', \'lambdab * piP * piE\'), (\'piE\', 3.0), (\'lambdab\', 0.00042)]'),(1,103,0,0,'',0,'',1,1,'34335',1,2,'S1:SS3:A34:J342',0,0,0,1,'Connector, Round, Power',0,100,100,'andrew',2,1,0,0,0,0,0.002846,0.000569,0.002847,6.1e-05,0.003416,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,3.51324e+08,2.9277e+08,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,1,'J342',1,1,'',0,0,0,0,0,'',5,0,30,30,1,0,0,1,'',2010,'[(\'piP\', 5.768522319848014), (\'equation\', \'lambdab * piK * piP * piE\'), (\'piK\', 2.0), (\'piE\', 1.0), (\'lambdab\', 0.0002467164967019012)]'),(1,104,0,0,'',0,'',1,1,'',1,2,'S1:SS3:A34:J343',0,0,0,1,'Connector, PCB Edge',0,100,100,'andrew',2,1,0,0,0,0,0.006756,0.001351,0.006755,0.000146,0.008107,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,1.48026e+08,1.23355e+08,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,1,'J343',0.999999,0.999999,'',0,0,0,0,0,'',6,0,30,30,1,0,0,1,'',2010,'[(\'piP\', 12.141575740769989), (\'equation\', \'lambdab * piK * piP * piE\'), (\'piK\', 1.5), (\'piE\', 3.0), (\'lambdab\', 0.00012364446734788393)]'),(1,106,0,0,'',0,'',1,1,'34335',1,2,'S1:SS3:A34:J344',0,0,0,1,'Connection, PTH',0,100,100,'andrew',2,0,0,0,0,0,0.015766,0,0.015766,0.000284,0.015766,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,6.34274e+07,6.34274e+07,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,56,'J344',0.999998,0.999998,'',0,0,0,0,0,'',7,0,30,30,56,0,0,1,'',2010,'[(\'equation\', \'lambdab * (N1 * piC + N2 * (piC + 13.0)) * piQ * piE\'), (\'piC\', 1.5567223160046073), (\'piE\', 2.0), (\'lambdab\', 0.00041), (\'piQ\', 1.0), (\'N1\', 3), (\'N2\', 1)]'),(1,108,0,0,'',0,'',1,1,'34335',1,2,'S1:SS3:A34:R341',0,0,0,1,'Connection, Solder, Component to PCB',0,100,100,'andrew',2,0,0,0,0,0,0.000138,0,0,2e-06,0.000138,0,0,2,'',50,'',0,0,'',1,0,0,100,0,'',0,7.24638e+09,7.24638e+09,0,0,1,0,0,1,1,'','',0,'','0:2:3',1,'',0,0,56,'R341',1,1,'',0,0,0,0,0,'',8,0,30,30,56,2.8,0,1,'',2010,'[(\'piQ\', 1.0), (\'equation\', \'lambdab * piQ * piE\'), (\'piE\', 2.0), (\'lambdab\', 6.9e-05)]');
/*!40000 ALTER TABLE `tbl_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_validation`
--

DROP TABLE IF EXISTS `tbl_validation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_validation` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '1',
  `fld_validation_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_task_desc` blob,
  `fld_task_type` int(11) DEFAULT '0',
  `fld_task_specification` varchar(128) NOT NULL DEFAULT '',
  `fld_measurement_unit` int(11) DEFAULT '0',
  `fld_min_acceptable` float DEFAULT '0',
  `fld_mean_acceptable` float DEFAULT '0',
  `fld_max_acceptable` float DEFAULT '0',
  `fld_variance_acceptable` float DEFAULT '0',
  `fld_start_date` varchar(45) DEFAULT '',
  `fld_end_date` varchar(45) DEFAULT '',
  `fld_status` float DEFAULT '0',
  `fld_effectiveness` float DEFAULT '0',
  PRIMARY KEY (`fld_validation_id`,`fld_revision_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_validation`
--

LOCK TABLES `tbl_validation` WRITE;
/*!40000 ALTER TABLE `tbl_validation` DISABLE KEYS */;
INSERT INTO `tbl_validation` VALUES (1,1,'Perform similar item analysis using Example System 0a as the baseline.',2,'',2,7500,0,0,0,'4/15/2012','6/15/2012',5,0),(1,2,'Perform MIL-HDBK-217FN2 stress analysis of design.',2,'MIL-HDBK-217FN2',2,5000,0,0,0,'7/1/2012','6/30/2013',0,0),(1,3,'Perform reliability demonstration testing.',2,'',2,5500,0,0,0,'3/1/2014','8/31/3014',0,0),(1,4,'Perform functional FMEA.',2,'MIL-STD-1629A',0,0,0,0,0,'4/15/2012','8/31/2012',0,0),(1,6,'Perform hardware FMEA.',2,'MIL-STD-1629A',0,0,0,0,0,'9/1/2012','8/31/2013',0,0);
/*!40000 ALTER TABLE `tbl_validation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_validation_matrix`
--

DROP TABLE IF EXISTS `tbl_validation_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_validation_matrix` (
  `fld_validation_id` int(11) NOT NULL,
  `fld_requirement_id` int(11) NOT NULL,
  `fld_revision_id` int(11) DEFAULT '1',
  PRIMARY KEY (`fld_validation_id`,`fld_requirement_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_validation_matrix`
--

LOCK TABLES `tbl_validation_matrix` WRITE;
/*!40000 ALTER TABLE `tbl_validation_matrix` DISABLE KEYS */;
INSERT INTO `tbl_validation_matrix` VALUES (1,2,1),(2,2,1),(3,2,1),(3,3,1),(2,3,1),(1,3,1),(1,5,1),(4,6,1),(6,6,1);
/*!40000 ALTER TABLE `tbl_validation_matrix` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-04-13 12:30:18
