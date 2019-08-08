PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE ramstk_revision (
    fld_revision_id INTEGER NOT NULL,
    fld_availability_logistics FLOAT,
    fld_availability_mission FLOAT,
    fld_cost FLOAT,
    fld_cost_failure FLOAT,
    fld_cost_hour FLOAT,
    fld_hazard_rate_active,
    fld_hazard_rate_dormant FLOAT,
    fld_hazard_rate_logistics FLOAT,
    fld_hazard_rate_mission FLOAT,
    fld_hazard_rate_software FLOAT,
    fld_mmt FLOAT,
    fld_mcmt FLOAT,
    fld_mpmt FLOAT,
    fld_mtbf_logistics FLOAT,
    fld_mtbf_mission FLOAT,
    fld_mttr FLOAT,
    fld_name VARCHAR(128),
    fld_reliability_logistics FLOAT,
    fld_reliability_mission FLOAT,
    fld_remarks BLOB,
    fld_total_part_count INTEGER,
    fld_revision_code VARCHAR(8),
    fld_program_time FLOAT,
    fld_program_time_sd FLOAT,
    fld_program_cost FLOAT,
    fld_program_cost_sd FLOAT,
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
COMMIT;
