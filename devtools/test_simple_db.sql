CREATE TABLE ramstk_revision (
    fld_revision_id INTEGER NOT NULL,
    fld_availability_logistics FLOAT NOT NULL,
    fld_availability_mission FLOAT NOT NULL,
    fld_cost FLOAT NOT NULL,
    fld_cost_failure FLOAT NOT NULL,
    fld_cost_hour FLOAT NOT NULL,
    fld_hazard_rate_active FLOAT NOT NULL,
    fld_hazard_rate_dormant FLOAT NOT NULL,
    fld_hazard_rate_logistics FLOAT NOT NULL,
    fld_hazard_rate_mission FLOAT NOT NULL,
    fld_hazard_rate_software FLOAT NOT NULL,
    fld_mmt FLOAT NOT NULL,
    fld_mcmt FLOAT NOT NULL,
    fld_mpmt FLOAT NOT NULL,
    fld_mtbf_logistics FLOAT NOT NULL,
    fld_mtbf_mission FLOAT NOT NULL,
    fld_mttr FLOAT NOT NULL,
    fld_name VARCHAR(128) NOT NULL,
    fld_reliability_logistics FLOAT NOT NULL,
    fld_reliability_mission FLOAT NOT NULL,
    fld_remarks VARCHAR NOT NULL,
    fld_total_part_count INTEGER NOT NULL,
    fld_revision_code VARCHAR(8) NOT NULL,
    fld_program_time FLOAT NOT NULL,
    fld_program_time_sd FLOAT NOT NULL,
    fld_program_cost FLOAT NOT NULL,
    fld_program_cost_sd FLOAT NOT NULL,
    PRIMARY KEY (fld_revision_id)
);
CREATE TABLE ramstk_site_info (
    fld_site_id INTEGER NOT NULL,
    fld_product_key VARCHAR(512),
    fld_expire_on DATE,
    fld_function_enabled INTEGER,
    fld_requirement_enabled INTEGER,
    fld_hardware_enabled INTEGER,
    fld_vandv_enabled INTEGER,
    fld_fmea_enabled INTEGER,
    PRIMARY KEY (fld_site_id)
);
CREATE TABLE ramstk_empty_table(
    fld_empty_id INTEGER NOT NULL)
