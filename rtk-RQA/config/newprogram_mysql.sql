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
-- Table structure for table `tbl_actions`
--

DROP TABLE IF EXISTS `tbl_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_actions` (
    `fld_incident_id` int(11) NOT NULL,
    `fld_action_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,,
    `fld_prescribed_action` blob,
    `fld_action_taken` blob,
    `fld_owner` varchar(256),
    `fld_due_date` varchar(45),
    `fld_status` int(11),
    `fld_approved_by` varchar(256),
    `fld_approved_date` varchar(45),
    `fld_approved` tinyint(4) DEFAULT '0',
    `fld_closed_by` varchar(256),
    `fld_closed_date` varchar(45),
    `fld_closed` tinyint(4) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_allocation`
--

DROP TABLE IF EXISTS `tbl_allocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_allocation` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  `fld_assembly_id` int(11) NOT NULL DEFAULT '0',
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
-- Adding data for table `tbl_allocation`
--

LOCK TABLES `tbl_allocation` WRITE;
/*!40000 ALTER TABLE `tbl_allocation` DISABLE KEYS */;
INSERT INTO `tbl_allocation` VALUES (0,0,1,1,1,1,1,1,1,1,1,0,0,0,0);
/*!40000 ALTER TABLE `tbl_allocation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_field_incident`
--

DROP TABLE IF EXISTS `tbl_field_incident`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_field_incident` (
  `fld_revision_id` int(11) DEFAULT '0',
  `fld_incident_id` varchar(32) NOT NULL,
  `fld_incident_type` varchar(16) DEFAULT '0',
  `fld_short_desc` varchar(128) DEFAULT NULL,
  `fld_long_desc` blob,
  `fld_remarks` blob,
  `fld_incident_date` varchar(45) DEFAULT NULL,
  `fld_closure_date` varchar(45) DEFAULT NULL,
  `fld_incident_age` int(11) DEFAULT NULL,
  `fld_status` int(11) DEFAULT NULL,
  `fld_accepted` tinyint(4) DEFAULT NULL,
  `fld_reviewed` tinyint(4) DEFAULT NULL,
  `fld_machine` varchar(32) DEFAULT '',
  `fld_system` varchar(16) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_field_incident_detail`
--

DROP TABLE IF EXISTS `tbl_field_incident_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_field_incident_detail` (
  `fld_incident_id` varchar(32) NOT NULL,
  `fld_part_num` varchar(128) NOT NULL,
  `fld_age_at_incident` float DEFAULT '0',
  `fld_failure` tinyint(4) DEFAULT '0',
  `fld_suspension` tinyint(4) DEFAULT '0',
  `fld_cnd_nff` tinyint(4) DEFAULT '0',
  `fld_ooc_fault` tinyint(4) DEFAULT '0',
  `fld_initial_installation` tinyint(4) DEFAULT '0',
  `fld_interval_censored` tinyint(4) DEFAULT '0',
  `fld_use_op_time` tinyint(4) DEFAULT '0',
  `fld_use_cal_time` tinyint(4) DEFAULT '0',
  `fld_ttf` float DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_functional_matrix`
--

DROP TABLE IF EXISTS `tbl_fmeca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_fmeca` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  `fld_assembly_id` int(11) NOT NULL DEFAULT '0',
  `fld_mode_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `fld_mode_description` varchar(512),
  `fld_mission_phase` varchar(64),
  `fld_local_effect` varchar(512),
  `fld_next_effect` varchar(512),
  `fld_end_effect` varchar(512),
  `fld_detection_method` varchar(512),
  `fld_other_indications` varchar(512),
  `fld_isolation_method` varchar(512),
  `fld_design_provisions` blob,
  `fld_operator_provisions` blob,
  `fld_severity_class` varchar(64),
  `fld_hazard_rate_source` varchar(64),
  `fld_effect_probability` float DEFAULT '1',
  `fld_mode_ratio` float DEFAULT '0',
  `fld_mode_failure_rate` float DEFAULT '0',
  `fld_mode_op_time` float DEFAULT '0',
  `fld_mode_criticality` float DEFAULT '0',
  `fld_rpn_severity` int(11) DEFAULT '0',
  `fld_immediate_cause` varchar(512),
  `fld_root_cause` varchar(512),
  `fld_rpn_occurence` int(11) DEFAULT '0',
  `fld_detection_control` blob,
  `fld_prevention_control` blob,
  `fld_rpn_detectability` int(11) DEFAULT '0',
  `fld_rpn` int(11) DEFAULT '0',
  `fld_recommended_action` blob,
  `fld_action_taken` blob,
  `fld_rpn_severity_new` int(11) DEFAULT '0',
  `fld_rpn_occurrence_new` int(11) DEFAULT '0',
  `fld_rpn_detectability_new` int(11) DEFAULT '0',
  `fld_rpn_new` int(11) DEFAULT '0',
  `fld_critical_item` tinyint(4),
  `fld_single_point` tinyint(4),
  `fld_remarks` blob
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `tbl_functional_matrix`
--

DROP TABLE IF EXISTS `tbl_functional_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_functional_matrix` (
  `fld_assembly_id` int(11) NOT NULL DEFAULT '0',
  `fld_function_id` int(11) NOT NULL DEFAULT '0',
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`fld_function_id`,`fld_assembly_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_functional_matrix`
--

LOCK TABLES `tbl_functional_matrix` WRITE;
/*!40000 ALTER TABLE `tbl_functional_matrix` DISABLE KEYS */;
INSERT INTO `tbl_functional_matrix` VALUES (0,0,0);
/*!40000 ALTER TABLE `tbl_functional_matrix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_functions`
--

DROP TABLE IF EXISTS `tbl_functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_functions` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  `fld_function_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_availability` float NOT NULL DEFAULT '1',
  `fld_availability_mission` float NOT NULL DEFAULT '1',
  `fld_code` varchar(16) NOT NULL DEFAULT 'Function Code',
  `fld_cost` float NOT NULL DEFAULT '0',
  `fld_failure_rate_mission` float NOT NULL DEFAULT '0',
  `fld_failure_rate_predicted` float NOT NULL DEFAULT '0',
  `fld_mmt` float NOT NULL DEFAULT '0',
  `fld_mcmt` float NOT NULL DEFAULT '0',
  `fld_mpmt` float NOT NULL DEFAULT '0',
  `fld_mtbf_mission` float NOT NULL DEFAULT '0',
  `fld_mtbf_predicted` float NOT NULL DEFAULT '0',
  `fld_mttr` float NOT NULL DEFAULT '0',
  `fld_name` varchar(255) DEFAULT 'Function Name',
  `fld_remarks` longblob,
  `fld_total_mode_quantity` int(11) NOT NULL DEFAULT '0',
  `fld_total_part_quantity` int(11) NOT NULL DEFAULT '0',
  `fld_type` int(11) NOT NULL DEFAULT '0',
  `fld_parent_id` varchar(16) NOT NULL DEFAULT '-',
  `fld_level` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`fld_revision_id`,`fld_function_id`) USING BTREE,
  KEY `lk_function` (`fld_function_id`),
  CONSTRAINT `tbl_functions_ibfk_1` FOREIGN KEY (`fld_revision_id`) REFERENCES `tbl_revisions` (`fld_revision_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_functions`
--

LOCK TABLES `tbl_functions` WRITE;
/*!40000 ALTER TABLE `tbl_functions` DISABLE KEYS */;
INSERT INTO `tbl_functions` VALUES (0,0,1,1,'UF-01',0,0,0,0,0,0,0,0,0,'Unassigned to Function','',0,0,0,'-',0);
/*!40000 ALTER TABLE `tbl_functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_mechanisms`
--

DROP TABLE IF EXISTS `tbl_mechanisms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_mechanisms` (
    `fld_mode_id` int(11) NOT NULL DEFAULT '0',
    `fld_mechanism_id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `fld_mechanism_description` varchar(512),
    `fld_damaging_conditions` blob,
    `fld_damage_model` varchar(256),
    `fld_primary_parameter` varchar(256),
    `fld_secondary_parameter` varchar(256),
    `fld_tertiary_parameter` varchar(256),
    `fld_mean_load_history` varchar(256),
    `fld_boundary_conditions` blob
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

--
-- Table structure for table `tbl_prediction`
--

DROP TABLE IF EXISTS `tbl_prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_prediction` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  `fld_assembly_id` int(11) NOT NULL DEFAULT '0',
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
  `fld_feature_size` float NOT NULL DEFAULT '1',
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
) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_program_info`
--

LOCK TABLES `tbl_program_info` WRITE;
/*!40000 ALTER TABLE `tbl_program_info` DISABLE KEYS */;
INSERT INTO `tbl_program_info` VALUES (0,'REVISION',1,'FUNCTION',1,'ASSEMBLY',1,'PART',1,'FMEA',1,'MODE',1,'EFFECT',1,'CAUSE',1,1,1,1,1,1,1,1,1,'0000-00-00 00:00:00','',NULL,NULL);
/*!40000 ALTER TABLE `tbl_program_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_requirements`
--

DROP TABLE IF EXISTS `tbl_requirements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_requirements` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  `fld_requirement_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_assembly_id` int(11) NOT NULL DEFAULT '0',
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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_revisions`
--

LOCK TABLES `tbl_revisions` WRITE;
/*!40000 ALTER TABLE `tbl_revisions` DISABLE KEYS */;
INSERT INTO `tbl_revisions` VALUES (0,1,1,0.0,0,0,0.0,0.0,0,0.0,0,0,0,0,0,0.0,0,'Original',1,1,'This is the original revision the system.',0,'');
/*!40000 ALTER TABLE `tbl_revisions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_similar_item`
--

DROP TABLE IF EXISTS `tbl_similar_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_similar_item` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  `fld_assembly_id` int(11) NOT NULL DEFAULT '0',
  `fld_sia_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_change_desc_1` blob DEFAULT 'No change',
  `fld_change_category_1` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_1` float DEFAULT '1',
  `fld_change_effort_1` int(11) DEFAULT '0',
  `fld_change_cost_1` float DEFAULT '0',
  `fld_change_desc_2` blob DEFAULT 'No change',
  `fld_change_category_2` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_2` float DEFAULT '1',
  `fld_change_effort_2` int(11) DEFAULT '0',
  `fld_change_cost_2` float DEFAULT '0',
  `fld_change_desc_3` blob DEFAULT 'No change',
  `fld_change_category_3` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_3` float DEFAULT '1',
  `fld_change_effort_3` int(11) DEFAULT '0',
  `fld_change_cost_3` float DEFAULT '0',
  `fld_change_desc_4` blob DEFAULT 'No change',
  `fld_change_category_4` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_4` float DEFAULT '1',
  `fld_change_effort_4` int(11) DEFAULT '0',
  `fld_change_cost_4` float DEFAULT '0',
  `fld_change_desc_5` blob DEFAULT 'No change',
  `fld_change_category_5` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_5` float DEFAULT '1',
  `fld_change_effort_5` int(11) DEFAULT '0',
  `fld_change_cost_5` float DEFAULT '0',
  `fld_change_desc_6` blob DEFAULT 'No change',
  `fld_change_category_6` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_6` float DEFAULT '1',
  `fld_change_effort_6` int(11) DEFAULT '0',
  `fld_change_cost_6` float DEFAULT '0',
  `fld_change_desc_7` blob DEFAULT 'No change',
  `fld_change_category_7` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_7` float DEFAULT '1',
  `fld_change_effort_7` int(11) DEFAULT '0',
  `fld_change_cost_7` float DEFAULT '0',
  `fld_change_desc_8` blob DEFAULT 'No change',
  `fld_change_category_8` varchar(32) NOT NULL DEFAULT 'None',
  `fld_change_factor_8` float DEFAULT '1',
  `fld_change_effort_8` int(11) DEFAULT '0',
  `fld_change_cost_8` float DEFAULT '0',
  `fld_function_1` varchar(128) NOT NULL DEFAULT '',
  `fld_function_2` varchar(128) NOT NULL DEFAULT '',
  `fld_function_3` varchar(128) NOT NULL DEFAULT '',
  `fld_function_4` varchar(128) NOT NULL DEFAULT '',
  `fld_function_5` varchar(128) NOT NULL DEFAULT '',
  `fld_result_1` float DEFAULT '0',
  `fld_result_2` float DEFAULT '0',
  `fld_result_3` float DEFAULT '0',
  `fld_result_4` float DEFAULT '0',
  `fld_result_5` float DEFAULT '0',
  `fld_user_blob_1` blob,
  `fld_user_blob_2` blob,
  `fld_user_blob_3` blob,
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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_similar_item`
--

LOCK TABLES `tbl_similar_item` WRITE;
/*!40000 ALTER TABLE `tbl_similar_item` DISABLE KEYS */;
INSERT INTO `tbl_similar_item` VALUES (0,0,0,'No change','None',1.0,0,0,'No change','None',1.0,0,0,'No change','None',1,0,0,'No change','None',1.0,0,0,'No change','None',1,0,0,'No change','None',1,0,0,'No change','None',1,0,0,'No change','None',1,0,0,'','','','','',0,0.0,0,0,0,'','','',0.0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `tbl_similar_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_system`
--

DROP TABLE IF EXISTS `tbl_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_system` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
  `fld_assembly_id` int(11) NOT NULL AUTO_INCREMENT,
  `fld_add_adj_factor` float NOT NULL DEFAULT '0',
  `fld_allocation_type` int(11) NOT NULL DEFAULT '0',
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
  `fld_failure_rate_type` int(11) NOT NULL DEFAULT '2',
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
  `fld_mttr_add_adj_factor` float NOT NULL DEFAULT '0',
  `fld_mttr_mult_adj_factor` float NOT NULL DEFAULT '1',
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
  `fld_reliability_goal_measure` int(11) NOT NULL DEFAULT '0',
  `fld_reliability_goal` float NOT NULL DEFAULT '1',
  PRIMARY KEY (`fld_revision_id`,`fld_assembly_id`),
  KEY `fld_assembly_id` (`fld_assembly_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Adding data for table `tbl_system`
--

LOCK TABLES `tbl_system` WRITE;
/*!40000 ALTER TABLE `tbl_system` DISABLE KEYS */;
INSERT INTO `tbl_system` VALUES (0,0,0,0,'',0,'',1,1,'',1,0,'',0.0,0.0,0.0,1,'System',0,100,100,'',0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0,0,0,'',0,'',0,0,'',0,-1,0,100,0,'',0,0.0,0.0,0,0,1,0,0,0,1.0,'','',0,'','-',0,'',0,0,1,'',0.0,0.0,'',0,0,0,1,0,'',0,0,0,0,0,0.0,0,0,'',2010,'',0,1);
/*!40000 ALTER TABLE `tbl_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_units`
--

DROP TABLE IF EXISTS `tbl_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_units` (
    `fld_serial_no` varchar(512) NOT NULL,
    `fld_model` varchar(64),
    `fld_market` varchar(16),
    `fld_build_date` datetime DEFAULT NULL,
    `fld_delivery_date` datetime DEFAULT NULL,
    `fld_warranty_date` datetime DEFAULT NULL,
    `fld_warranty_period` int(11) DEFAULT '1',
    `fld_warranty_type` varchar(8),
    PRIMARY KEY (`fld_serial_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `tbl_validation`
--

DROP TABLE IF EXISTS `tbl_validation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_validation` (
  `fld_revision_id` int(11) NOT NULL DEFAULT '0',
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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbl_validation_matrix`
--

DROP TABLE IF EXISTS `tbl_validation_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_validation_matrix` (
  `fld_validation_id` int(11) NOT NULL DEFAULT '0',
  `fld_requirement_id` int(11) NOT NULL DEFAULT '0',
  `fld_revision_id` int(11) DEFAULT '0',
  PRIMARY KEY (`fld_validation_id`,`fld_requirement_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
