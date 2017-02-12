DROP TABLE IF EXISTS "tbl_failure_modes";
CREATE TABLE "tbl_failure_modes" (
    "fld_category_id" INTEGER NOT NULL DEFAULT(0),      -- The component the failure mode belongs to category ID.
    "fld_subcategory_id" INTEGER NOT NULL DEFAULT(0),   -- The component the failure mode belongs to subcategory ID.
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),          -- The failure mode ID.
    "fld_mode_description" VARCHAR(256),                -- The description of the failure mode.
    "fld_mode_ratio" REAL,                              -- The failure mode ratio (0.0 - 100.0).
    "fld_source" INTEGER DEFAULT(0)                     -- The source of the failure mode information.  (1=FMD-97, 2=MIL-HDBK-338B, 3=
);
INSERT INTO tbl_failure_modes(1, 1, 1, "Improper Output", 0.77, 2);
INSERT INTO tbl_failure_modes(1, 1, 2, "No Output", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 2, 1, "Output Stuck High", 0.28, 2);
INSERT INTO tbl_failure_modes(1, 2, 2, "Output Stuck Low", 0.28, 2);
INSERT INTO tbl_failure_modes(1, 2, 3, "Input Open", 0.22, 2);
INSERT INTO tbl_failure_modes(1, 2, 4, "Output Open", 0.22, 2);
INSERT INTO tbl_failure_modes(1, 3, 1, "Improper Output", 0.77, 2);
INSERT INTO tbl_failure_modes(1, 3, 2, "No Output", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 4, 1, "Improper Output", 0.77, 2);
INSERT INTO tbl_failure_modes(1, 4, 2, "No Output", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 5, 1, "Data Bit Loss", 0.34, 2);
INSERT INTO tbl_failure_modes(1, 5, 2, "Short", 0.26, 2);
INSERT INTO tbl_failure_modes(1, 5, 3, "Open", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 5, 4, "Slow Transfer of Data", 0.17, 2);
INSERT INTO tbl_failure_modes(1, 6, 1, "Data Bit Loss", 0.34, 2);
INSERT INTO tbl_failure_modes(1, 6, 2, "Short", 0.26, 2);
INSERT INTO tbl_failure_modes(1, 6, 3, "Open", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 6, 4, "Slow Transfer of Data", 0.17, 2);
INSERT INTO tbl_failure_modes(1, 7, 1, "Data Bit Loss", 0.34, 2);
INSERT INTO tbl_failure_modes(1, 7, 2, "Short", 0.26, 2);
INSERT INTO tbl_failure_modes(1, 7, 3, "Open", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 7, 4, "Slow Transfer of Data", 0.17, 2);
INSERT INTO tbl_failure_modes(1, 8, 1, "Data Bit Loss", 0.34, 2);
INSERT INTO tbl_failure_modes(1, 8, 2, "Short", 0.26, 2);
INSERT INTO tbl_failure_modes(1, 8, 3, "Open", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 8, 4, "Slow Transfer of Data", 0.17, 2);
INSERT INTO tbl_failure_modes(1, 9, 1, "Output Stuck High", 0.28, 2);
INSERT INTO tbl_failure_modes(1, 9, 2, "Output Stuck Low", 0.28, 2);
INSERT INTO tbl_failure_modes(1, 9, 3, "Input Open", 0.22, 2);
INSERT INTO tbl_failure_modes(1, 9, 4, "Output Open", 0.22, 2);
INSERT INTO tbl_failure_modes(1, 10, 1, "Improper Output", 0.77, 2);
INSERT INTO tbl_failure_modes(1, 10, 2, "No Output", 0.23, 2);
INSERT INTO tbl_failure_modes(1, 11, 1, "Open Circuit", 0.51, 2);
INSERT INTO tbl_failure_modes(1, 11, 2, "Degraded Output", 0.26, 2);
INSERT INTO tbl_failure_modes(1, 11, 3, "Short Circuit", 0.17, 2);
INSERT INTO tbl_failure_modes(1, 11, 4, "No Output", 0.06, 2);
INSERT INTO tbl_failure_modes(2, 12, 1, "Short", 0.49, 2);
INSERT INTO tbl_failure_modes(2, 12, 2, "Open", 0.36, 2);
INSERT INTO tbl_failure_modes(2, 12, 3, "Parameter Change", 0.15, 2);
INSERT INTO tbl_failure_modes(2, 13, 1, "Short", 0.49, 2);
INSERT INTO tbl_failure_modes(2, 13, 2, "Open", 0.36, 2);
INSERT INTO tbl_failure_modes(2, 13, 3, "Parameter Change", 0.15, 2);
INSERT INTO tbl_failure_modes(2, 14, 1, "Short", 0.73, 2);
INSERT INTO tbl_failure_modes(2, 14, 2, "Open", 0.27, 2);
