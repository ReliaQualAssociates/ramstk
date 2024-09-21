# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK test suite configuration module."""

# Standard Library Imports
import csv
import gettext
import glob
import os
import platform
import random
import shutil
import string
import sys
import tempfile
import xml.etree.ElementTree as ET
from distutils import dir_util
from pathlib import Path

# Third Party Imports
import psycopg2
import pytest
import toml
import xlwt
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration, RAMSTKUserConfiguration
from ramstk.models.db import BaseDatabase, RAMSTKCommonDB

_ = gettext.gettext

TEMPDIR = tempfile.gettempdir()
try:
    VIRTUAL_ENV = glob.glob(os.environ["VIRTUAL_ENV"])[0]
except IndexError:
    VIRTUAL_ENV = os.environ["VIRTUAL_ENV"]
except KeyError:
    if platform.system() == "Linux":
        VIRTUAL_ENV = os.getenv("HOME") + "/.local"
    elif platform.system() == "Windows":
        VIRTUAL_ENV = os.getenv("TEMP")
    else:
        print(f"The {platform.system()} system platform is not supported.")
        sys.exit(1)

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_DIR = f"{VIRTUAL_ENV}/share/RAMSTK"
DATA_DIR = f"{CONF_DIR}/layouts"
ICON_DIR = f"{CONF_DIR}/icons"
TMP_DIR = f"{VIRTUAL_ENV}/tmp"
LOG_DIR = f"{TMP_DIR}/logs"
TEST_PROGRAM_DB_PATH = f"{TMP_DIR}/TestProgramDB.ramstk"
TEST_COMMON_DB_PATH = f"{TEMPDIR}/TestCommonDB.ramstk"
TEST_COMMON_DB_URI = f"sqlite:///{TEST_COMMON_DB_PATH}"

DEBUG_LOG = f"{LOG_DIR}/RAMSTK_debug.log"
USER_LOG = f"{LOG_DIR}/RAMSTK_user.log"
IMPORT_LOG = f"{LOG_DIR}/RAMSTK_import.log"

HEADERS = {
    "Function": [
        "Revision ID",
        "Function ID",
        "Level",
        "Function Code",
        "Function Name",
        "Parent",
        "Remarks",
        "Safety Critical",
        "Type",
    ],
    "Requirement": [
        "Revision ID",
        "Requirement ID",
        "Derived?",
        "Requirement",
        "Figure Number",
        "Owner",
        "Page Number",
        "Parent ID",
        "Priority",
        "Requirement Code",
        "Specification",
        "Requirement Type",
        "Validated?",
        "Validated Date",
    ],
    "Hardware": [
        "Revision ID",
        "Hardware ID",
        "Alt. Part Num.",
        "CAGE Code",
        "Category",
        "Comp. Ref. Des.",
        "Unit Cost",
        "Cost Type",
        "Description",
        "Duty Cycle",
        "Fig. Num.",
        "LCN",
        "Level",
        "Supplier",
        "Mission Time",
        "Name",
        "NSN",
        "Page Num.",
        "Parent ID",
        "Part?",
        "PN",
        "Quantity",
        "Ref. Des.",
        "Remarks",
        "Repairable?",
        "Specification",
        "SubCat",
        "Tagged",
        "Year of Manufacture",
        "App. ID",
        "Area",
        "Capacitance",
        "Configuration",
        "Construction ID",
        "Contact Form",
        "Constact Gauge",
        "Contact Rating ID",
        "Operating Current",
        "Rated Current",
        "Current Ratio",
        "Active Environment",
        "Dormant Environment",
        "Family",
        "Feature Size",
        "Operating Freq.",
        "Insert ID",
        "Insulation ID",
        "Manufacturing ID",
        "Matching",
        "Num. Active Pins",
        "Num. Ckt. Planes",
        "Num. Cycles",
        "Num. Elements",
        "Hand Soldered",
        "Wave Soldered",
        "Operating Life",
        "Overstressed?",
        "Package ID",
        "Operating Power",
        "Rated Power",
        "Power Ratio",
        "Overstress Reason",
        "Resistance",
        "Specification ID",
        "Tech. ID",
        "Active Temp.",
        "Case Temp.",
        "Dormant Temp.",
        "Hot Spot Temp.",
        "Junction Temp.",
        "Knee Temp.",
        "Max. Rated Temp.",
        "Min. Rated Temp.",
        "Temperature Rise",
        "Theta JC",
        "Type",
        "AC Operating Voltage",
        "DC Operating Voltage",
        "ESD Withstand Volts",
        "Rated Voltage",
        "Voltage Ratio",
        "Weight",
        "Years in Prod.",
        "Add. Adj. Factor",
        "Fail. Dist. ID",
        "h(t) Method",
        "h(t) Model",
        "Specified h(t)",
        "h(t) Type",
        "Location",
        "Specified MTBF",
        "Mult. Adj. Factor",
        "Quality",
        "R(t) Goal",
        "R(t) Goal Measure",
        "Scale Parameter",
        "Shape Parameter",
        "Surv. Analysis",
        "Altitude, Operating",
        "Balance ID",
    ],
    "Validation": [
        "Revision ID",
        "Validation ID",
        "Maximum Acceptable",
        "Mean Acceptable",
        "Minimum Acceptable",
        "Acceptable Variance",
        "s-Confidence",
        "Avg. Task Cost",
        "Max. Task Cost",
        "Min. Task Cost",
        "Start Date",
        "Finish Date",
        "Description",
        "Unit of Measure",
        "Task Name",
        "Status",
        "Type",
        "Task Spec.",
        "Average Task Time",
        "Maximum Task Time",
        "Minimum Task Time",
    ],
}

# Row data for the Function import test file.
ROW_DATA = [
    [
        1,
        5,
        1,
        "PRESS-001",
        "Maintain system pressure.",
        0,
        "This is a function that is about system pressure.  This remarks box "
        "also needs to be larger.",
        1,
        0,
    ],
    [
        1,
        6,
        1,
        "FLOW-001",
        "Maintain system flow.",
        0,
        "These are remarks associated with the function FLOW-001.  The "
        "remarks box needs to be bigger.",
        0,
        0,
    ],
    [
        1,
        10,
        0,
        "Gotta do something",
        "Fig. 1",
        2,
        "3.2-1",
        0,
        4,
        "GEN-001",
        "Spec. 12",
        4,
        0,
        "2019-08-18",
    ],
    [
        1,
        10,
        "",
        "",
        0,
        "S1",
        47.28,
        1,
        "System That Was Imported",
        87.0,
        "",
        "",
        1,
        "",
        72.0,
        "Imported System",
        "",
        "",
        0,
        0,
        "",
        1,
        "S1",
        "Remarks in a binary field.",
        1,
        "",
        0,
        0,
        2018,
        0,
        0.0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0.0,
        0.0,
        0.0,
        4,
        1,
        0,
        0.0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0,
        0.0,
        0.0,
        0.0,
        "Overstress Reason",
        0.0,
        0,
        0,
        30.0,
        30.0,
        25.0,
        0.0,
        0.0,
        40.0,
        125.0,
        0.0,
        0.0,
        0.0,
        0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0.0,
        0.0,
        1.0,
        2,
        0.95,
        0,
        0.0,
        0.0,
        0,
        12000,
        1,
    ],
    [
        1,
        12,
        832.5,
        799.0,
        612.3,
        226.4,
        0.9,
        350.00,
        500.00,
        275.00,
        "2019-08-18",
        "2019-09-01",
        "Validation task that was imported by test suite.",
        0,
        "",
        "",
        0,
        "",
        120.0,
        140.0,
        95.0,
    ],
]


def setup_test_directory(test_dir) -> None:
    """Create test configuration directory."""
    if not os.path.exists(test_dir):
        os.makedirs(test_dir, exist_ok=True)


def populate_test_directory(test_dir) -> None:
    """Create test icon and layout directory."""
    dir_util.copy_tree(f"{os.getcwd()}/data/icons/", f"{test_dir}/icons/")
    dir_util.copy_tree(f"{os.getcwd()}/data/layouts/", f"{test_dir}/layouts/")


def teardown_test_directory(test_dir) -> None:
    """Remove test configuration directory."""
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def setup_test_db(db_config) -> None:
    """Create a test postgres database."""
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname="postgres",
        user=db_config["user"],
        password=db_config["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(db_config["database"])
        )
    )
    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_config["database"]))
    )
    cursor.close()
    conn.close()


def populate_test_db(db_config, sql_file) -> None:
    """Populate test database."""
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_session(autocommit=True)

    cursor = conn.cursor()
    cursor.execute(open(sql_file, "r").read())
    cursor.close()
    conn.close()


def teardown_test_db(db_config) -> None:
    """Drop test database."""
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname="postgres",
        user=db_config["user"],
        password=db_config["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    try:
        cursor.execute(
            sql.SQL("DROP DATABASE IF EXISTS {}").format(
                sql.Identifier(db_config["database"])
            )
        )
    except psycopg2.errors.ObjectInUse as e:
        print(e)

    cursor.close()
    conn.close()


# START FIXTURES
@pytest.fixture(scope="function")
def make_shibboly():
    """Create a read-only directory."""
    if os.path.exists("/tmp/shibboly"):
        shutil.rmtree("/tmp/shibboly")

    os.mkdir("/tmp/shibboly", 0o0444)


@pytest.fixture(scope="session")
def test_config_dir():
    """Create a configuration directory if one doesn't exist.

    This creates a configuration directory in the virtual environment base to allow
    testing certain functions/methods that look for a user configuration directory
    otherwise defaulting to the site-wide configuration directory.
    """
    _config_dir = f"{VIRTUAL_ENV}/share/RAMSTK"

    # Set up the test configuration directories.
    setup_test_directory(test_dir=_config_dir)

    # Copy files to the test configuration directories.
    populate_test_directory(test_dir=_config_dir)

    yield _config_dir


@pytest.fixture(scope="class")
def test_import_dir():
    """Create a directory for export testing."""
    # This simply creates the base name of the file and directory to create it
    # in.  A test would need to add the appropriate file extension.
    _import_dir = f"{TMP_DIR}/test_imports"

    # Set up the test import directory.
    setup_test_directory(test_dir=_import_dir)

    yield _import_dir

    # Teardown the test import directory.
    teardown_test_directory(test_dir=_import_dir)


@pytest.fixture(scope="class")
def test_export_dir():
    """Create a directory for export testing."""
    # This simply creates the base name of the file and directory to create it
    # in.  A test would need to add the appropriate file extension.
    _export_dir = f"{TMP_DIR}/test_exports/"

    # Set up the test export directory.
    setup_test_directory(test_dir=_export_dir)

    yield _export_dir

    # Teardown the test export directory.
    teardown_test_directory(test_dir=_export_dir)


@pytest.fixture(scope="session")
def make_home_config_dir():
    """Create a configuration directory to mimic a user's configuration directory."""
    _config_dir = f"{VIRTUAL_ENV}/tmp/.config/RAMSTK"

    # Set up the test home configuration directory.
    setup_test_directory(_config_dir)
    setup_test_directory(f"{_config_dir}/layouts")
    setup_test_directory(f"{_config_dir}/log")

    # Set up the test analyses directory.
    _analyses_dir = f"{VIRTUAL_ENV}/tmp/analyses/ramstk"
    setup_test_directory(_analyses_dir)

    shutil.copyfile(
        "./data/sqlite_program_db.sql", f"{_config_dir}/sqlite_program_db.sql"
    )
    shutil.copyfile(
        "./data/postgres_program_db.sql",
        f"{_config_dir}/postgres_program_db.sql",
    )
    if str(sys.version_info[0]) + "." + str(sys.version_info[1]) == "3.7":
        shutil.copytree("./data/icons", f"{_config_dir}/icons/")
    else:
        setup_test_directory(f"{_config_dir}/icons")
        shutil.copytree("./data/icons", f"{_config_dir}/icons/", dirs_exist_ok=True)

    yield _config_dir

    # Teardown the home configuration and analyses directories.
    teardown_test_directory(_config_dir)
    teardown_test_directory(_analyses_dir)


@pytest.fixture(scope="function")
def test_bald_dao():
    """Create a DAO with an unpopulated database attached."""
    dao = BaseDatabase()

    yield dao

    del dao


@pytest.fixture(scope="class")
def test_common_dao():
    """Create a test DAO object for testing against an RAMSTK Common DB."""
    # Create a random name for the test database.  This ensures each test class uses
    # a unique, clean database to test against.
    db_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # This will create a RAMSTK Common database using the
    # test_common_db.sql file in ./data for each group of tests collected in a
    # class.  Group tests in the class in such a way as to produce predictable behavior
    # (e.g., all the tests for select() and select_all()).
    test_config = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": f"test_common_db_{db_name}",
    }

    # Set up the test database.
    setup_test_db(db_config=test_config)

    # Populate the test database.
    testql_file = "./data/postgres_common_db.sql"
    populate_test_db(db_config=test_config, sql_file=testql_file)

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = RAMSTKCommonDB()
    dao.do_connect(test_config)

    yield dao

    dao.do_disconnect()

    # Teardown the test database.
    teardown_test_db(db_config=test_config)


@pytest.fixture(scope="class")
def test_program_dao():
    """Create a test DAO object for testing against a RAMSTK Program DB."""
    # Create a random name for the test database.  This ensures each test class uses
    # a unique, clean database to test against.
    db_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # This will create a RAMSTK Program database using the
    # test_program_db.sql file in tests/__data for each group of tests collected in a
    # class.  Group tests in the class in such a way as to produce predictable behavior
    # (e.g., all the tests for select() and select_all()).
    test_config = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": f"test_program_db_{db_name}",
    }

    # Set up the test database.
    setup_test_db(db_config=test_config)

    # Create the test database tables.
    populate_test_db(db_config=test_config, sql_file="./data/postgres_program_db.sql")

    # Populate the test database tables.
    populate_test_db(
        db_config=test_config, sql_file="./tests/__data/test_program_db.sql"
    )

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()
    dao.do_connect(test_config)

    yield dao

    dao.do_disconnect()

    # Teardown the test database.
    teardown_test_db(db_config=test_config)


@pytest.fixture(scope="class")
def test_simple_database():
    """Create a simple test database using postgres."""
    # Create a random name for the test database.  This ensures each test class uses
    # a unique, clean database to test against.
    db_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # This temporary database has two tables (RAMSTKRevision and
    # RAMSTKSiteInfo) and is used primarily to test the connection, insert,
    # insert_many, delete, and update methods of the database drivers.
    test_config = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": f"test_simple_db_{db_name}",
    }

    # Set up the test database.
    setup_test_db(db_config=test_config)

    # Populate the test database.
    testql_file = "./tests/__data/test_simple_db.sql"
    populate_test_db(db_config=test_config, sql_file=testql_file)

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()
    dao.do_connect(test_config)

    yield dao

    dao.do_disconnect()

    # Teardown the test database.
    teardown_test_db(db_config=test_config)


@pytest.fixture(scope="function")
def test_simple_program_database():
    """Create a simple test database using postgres."""
    # Create a random name for the test database.  This ensures each test class uses
    # a unique, clean database to test against.
    db_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # This temporary database has two tables (RAMSTKRevision and
    # RAMSTKSiteInfo) and is used primarily to test the connection, insert,
    # insert_many, delete, and update methods of the database drivers.
    test_config = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": f"test_simple_program_db_{db_name}",
    }

    # Set up the test database.
    setup_test_db(db_config=test_config)

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()
    dao.do_connect(test_config)

    yield dao

    dao.do_disconnect()

    # Teardown the test database.
    teardown_test_db(db_config=test_config)


@pytest.fixture(scope="function")
def test_license_file():
    """Create a license key file for testing."""
    _cwd = os.getcwd()
    with open(f"{_cwd}/license.key", "w") as _license_file:
        _license_file.write("100\n")
        _license_file.write("apowdigfb3rh9214839qu\n")
        _license_file.write("2019-08-07\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("0\n")
        _license_file.write("0\n")
        _license_file.write("0\n")
        _license_file.write("0\n")
        _license_file.write("0\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("1\n")
        _license_file.write("0\n")
        _license_file.write("0\n")
        _license_file.write("ReliaQual Test Site")
    yield _license_file

    os.remove(f"{_cwd}/license.key")


@pytest.fixture
def test_log_file():
    """Create a log file."""
    _test_file = f"{TMP_DIR}/test_file.log"
    Path(_test_file).touch()

    yield _test_file

    os.remove(_test_file)


@pytest.fixture(scope="session")
def test_toml_site_configuration(test_config_dir):
    """Create a toml site configuration file."""
    _site_config = RAMSTKSiteConfiguration()
    _site_config.RAMSTK_SITE_CONF = f"{VIRTUAL_ENV}/share/RAMSTK/Site.toml"
    _dic_site_configuration = {
        "title": "RAMSTK Site Configuration",
        "backend": {
            "dialect": "sqlite",
            "host": "localhost",
            "port": "3306",
            "database": f"{VIRTUAL_ENV}/share/RAMSTK/ramstk_common.ramstk",
            "user": "johnny.tester",
            "password": "clear.text.password",
        },
    }

    toml.dump(_dic_site_configuration, open(_site_config.RAMSTK_SITE_CONF, "w"))

    yield _site_config


@pytest.fixture(scope="session")
def test_toml_user_configuration(make_home_config_dir):
    """Create a toml user configuration file."""
    _user_config = RAMSTKUserConfiguration()
    _user_config._INSTALL_PREFIX = VIRTUAL_ENV
    _user_config.RAMSTK_HOME_DIR = f"{VIRTUAL_ENV}/tmp"
    _user_config.RAMSTK_CONF_DIR = f"{VIRTUAL_ENV}/tmp/.config/RAMSTK"
    _user_config.RAMSTK_PROG_CONF = f"{_user_config.RAMSTK_CONF_DIR}/RAMSTK.toml"
    _user_config.RAMSTK_DATA_DIR = f"{_user_config.RAMSTK_CONF_DIR}/layouts"
    _user_config.RAMSTK_ICON_DIR = f"{_user_config.RAMSTK_CONF_DIR}/icons"
    _user_config.RAMSTK_LOG_DIR = f"{_user_config.RAMSTK_CONF_DIR}/logs"
    _user_config.RAMSTK_PROG_DIR = f"{VIRTUAL_ENV}/tmp/analyses/ramstk"
    _dic_user_configuration = {
        "title": "RAMSTK User Configuration",
        "general": {
            "firstrun": "True",
            "reportsize": "letter",
            "frmultiplier": "1000000.0",
            "calcreltime": "100.0",
            "decimal": "6",
            "modesource": "1",
            "clearmodes": "false",
            "moduletabpos": "top",
            "listtabpos": "bottom",
            "worktabpos": "bottom",
            "loglevel": "INFO",
        },
        "backend": {
            "dialect": "sqlite",
            "host": "localhost",
            "port": "3306",
            "database": "",
            "user": "",
            "password": "",
        },
        "directories": {
            "datadir": _user_config.RAMSTK_DATA_DIR,
            "icondir": _user_config.RAMSTK_ICON_DIR,
            "logdir": _user_config.RAMSTK_LOG_DIR,
            "progdir": _user_config.RAMSTK_PROG_DIR,
        },
        "layouts": {
            "allocation": "allocation.toml",
            "definition": "failure_definition.toml",
            "fmea": "fmea.toml",
            "function": "function.toml",
            "hardware": "hardware.toml",
            "hazard": "hazops.toml",
            "pof": "pof.toml",
            "requirement": "requirement.toml",
            "revision": "revision.toml",
            "similar_item": "similar_item.toml",
            "stakeholder": "stakeholder.toml",
            "usage_profile": "usage_profile.toml",
            "validation": "validation.toml",
        },
        "colors": {
            "allocationbg": "#FFFFFF",
            "allocationfg": "#000000",
            "definitionbg": "#FFFFFF",
            "definitionfg": "#000000",
            "fmeabg": "#FFFFFF",
            "fmeafg": "#000000",
            "functionbg": "#FFFFFF",
            "functionfg": "#000000",
            "hardwarebg": "#FFFFFF",
            "hardwarefg": "#000000",
            "hazardbg": "#FFFFFF",
            "hazardfg": "#000000",
            "pofbg": "#FFFFFF",
            "poffg": "#000000",
            "requirementbg": "#FFFFFF",
            "requirementfg": "#000000",
            "revisionbg": "#FFFFFF",
            "revisionfg": "#000000",
            "similar_itembg": "#FFFFFF",
            "similar_itemfg": "#000000",
            "stakeholderbg": "#FFFFFF",
            "stakeholderfg": "#000000",
            "validationbg": "#FFFFFF",
            "validationfg": "#000000",
        },
        "stress": {
            "integrated_circuit": {
                "digital": {
                    "mos": {
                        "hermetic": {
                            "current": [0.9, 0.85, 0.8],
                            "fanout": [1.0, 0.9, 0.9],
                            "frequency": [0.9, 0.9, 0.9],
                            "temperature": [125.0, 110.0, 100.0],
                        },
                        "plastic1": {
                            "current": [0.9, 0.8, 0.0],
                            "fanout": [1.0, 0.9, 0.0],
                            "frequency": [0.9, 0.8, 0.0],
                            "temperature": [90.0, 85.0, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "fanout": [0.8, 0.0, 0.0],
                            "frequency": [0.8, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                        },
                    },
                    "bipolar": {
                        "hermetic": {
                            "current": [0.9, 0.85, 0.8],
                            "fanout": [0.9, 0.85, 0.8],
                            "frequency": [1.0, 0.9, 0.85],
                            "temperature": [125.0, 110.0, 100.0],
                        },
                        "plastic1": {
                            "current": [0.9, 0.8, 0.0],
                            "fanout": [0.9, 0.8, 0.0],
                            "frequency": [1.0, 0.9, 0.0],
                            "temperature": [90.0, 85.0, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "fanout": [0.7, 0.0, 0.0],
                            "frequency": [0.75, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                        },
                    },
                },
                "linear": {
                    "mos": {
                        "hermetic": {
                            "current": [0.9, 0.85, 0.8],
                            "fanout": [1.0, 0.9, 0.9],
                            "frequency": [0.9, 0.9, 0.9],
                            "temperature": [125.0, 110.0, 100.0],
                            "voltage": [0.8, 0.8, 0.7],
                        },
                        "plastic1": {
                            "current": [0.9, 0.8, 0.0],
                            "fanout": [1.0, 0.9, 0.0],
                            "frequency": [0.9, 0.8, 0.0],
                            "temperature": [90.0, 85.0, 0.0],
                            "voltage": [0.8, 0.7, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "fanout": [0.8, 0.0, 0.0],
                            "frequency": [0.8, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                            "voltage": [0.6, 0.0, 0.0],
                        },
                    },
                    "bipolar": {
                        "hermetic": {
                            "current": [0.9, 0.85, 0.8],
                            "fanout": [0.9, 0.85, 0.8],
                            "frequency": [1.0, 0.9, 0.85],
                            "temperature": [125.0, 110.0, 100.0],
                            "voltage": [0.8, 0.8, 0.7],
                        },
                        "plastic1": {
                            "current": [0.9, 0.8, 0.0],
                            "fanout": [0.9, 0.8, 0.0],
                            "frequency": [1.0, 0.9, 0.0],
                            "temperature": [90.0, 85.0, 0.0],
                            "voltage": [0.8, 0.7, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "fanout": [0.7, 0.0, 0.0],
                            "frequency": [0.75, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                            "voltage": [0.6, 0.0, 0.0],
                        },
                    },
                },
                "microprocessor": {
                    "mos": {
                        "hermetic": {
                            "current": [0.9, 0.85, 0.8],
                            "fanout": [1.0, 0.9, 0.9],
                            "frequency": [0.9, 0.9, 0.9],
                            "temperature": [125.0, 110.0, 100.0],
                        },
                        "plastic1": {
                            "current": [0.9, 0.8, 0.0],
                            "fanout": [1.0, 0.85, 0.0],
                            "frequency": [0.9, 0.8, 0.0],
                            "temperature": [85.0, 75.0, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "fanout": [0.8, 0.0, 0.0],
                            "frequency": [0.8, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                        },
                    },
                    "bipolar": {
                        "hermetic": {
                            "current": [0.8, 0.75, 0.7],
                            "fanout": [0.8, 0.75, 0.7],
                            "frequency": [0.9, 0.8, 0.75],
                            "temperature": [125.0, 110.0, 100.0],
                        },
                        "plastic1": {
                            "current": [0.8, 0.75, 0.0],
                            "fanout": [0.8, 0.75, 0.0],
                            "frequency": [0.9, 0.8, 0.0],
                            "temperature": [85.0, 75.0, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "fanout": [0.7, 0.0, 0.0],
                            "frequency": [0.75, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                        },
                    },
                },
                "memory": {
                    "mos": {
                        "hermetic": {
                            "current": [0.9, 0.85, 0.8],
                            "frequency": [1.0, 0.9, 0.9],
                            "temperature": [125.0, 110.0, 100.0],
                        },
                        "plastic1": {
                            "current": [0.9, 0.8, 0.0],
                            "frequency": [1.0, 0.9, 0.0],
                            "temperature": [90.0, 85.0, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "frequency": [0.8, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                        },
                    },
                    "bipolar": {
                        "hermetic": {
                            "current": [0.9, 0.85, 0.8],
                            "frequency": [1.0, 1.0, 0.9],
                            "temperature": [125.0, 110.0, 100.0],
                        },
                        "plastic1": {
                            "current": [0.9, 0.8, 0.0],
                            "frequency": [1.0, 0.95, 0.0],
                            "temperature": [90.0, 85.0, 0.0],
                        },
                        "plastic2": {
                            "current": [0.7, 0.0, 0.0],
                            "frequency": [0.8, 0.0, 0.0],
                            "temperature": [70.0, 0.0, 0.0],
                        },
                    },
                },
            },
            "semiconductor": {
                "diode": {
                    "general_purpose": {
                        "jantx": {
                            "current": [1.0, 1.0, 1.0],
                            "surge_current": [1.0, 0.9, 0.8],
                            "voltage": [0.95, 0.9, 0.85],
                            "temperature": [150.0, 125.0, 125.0],
                        },
                        "military": {
                            "current": [0.9, 0.9, 0.7],
                            "surge_current": [0.8, 0.8, 0.5],
                            "voltage": [0.8, 0.75, 0.5],
                            "temperature": [100.0, 85.0, 70.0],
                        },
                        "commercial": {
                            "current": [0.75, 0.7, 0.0],
                            "surge_current": [0.6, 0.3, 0.0],
                            "voltage": [0.7, 0.6, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                        },
                    },
                    "power_rectifier": {
                        "jantx": {
                            "current": [1.0, 1.0, 1.0],
                            "voltage": [0.95, 0.9, 0.85],
                            "temperature": [150.0, 125.0, 125.0],
                        },
                        "military": {
                            "current": [0.9, 0.85, 0.6],
                            "voltage": [0.8, 0.75, 0.3],
                            "temperature": [100.0, 85.0, 70.0],
                        },
                        "commercial": {
                            "current": [0.6, 0.5, 0.0],
                            "voltage": [0.5, 0.3, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                        },
                    },
                    "schottky": {
                        "jantx": {
                            "power": [1.0, 1.0, 0.9],
                            "voltage": [0.95, 0.9, 0.85],
                            "temperature": [150.0, 125.0, 125.0],
                        },
                        "military": {
                            "power": [0.9, 0.9, 0.5],
                            "voltage": [0.8, 0.8, 0.25],
                            "temperature": [100.0, 85.0, 70.0],
                        },
                        "commercial": {
                            "power": [0.75, 0.75, 0.0],
                            "voltage": [0.5, 0.3, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                        },
                    },
                    "regulator": {
                        "jantx": {
                            "power": [1.0, 1.0, 0.9],
                            "temperature": [150.0, 125.0, 125.0],
                        },
                        "military": {
                            "power": [0.9, 0.8, 0.5],
                            "temperature": [100.0, 85.0, 70.0],
                        },
                        "commercial": {
                            "power": [0.5, 0.5, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                        },
                    },
                    "suppressor": {
                        "jantx": {
                            "current": [1.0, 1.0, 0.9],
                            "power": [1.0, 1.0, 0.9],
                            "temperature": [150.0, 125.0, 125.0],
                        },
                        "military": {
                            "current": [0.8, 0.8, 0.5],
                            "power": [0.8, 0.8, 0.5],
                            "temperature": [100.0, 85.0, 70.0],
                        },
                        "commercial": {
                            "current": [0.75, 0.5, 0.0],
                            "power": [0.75, 0.5, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                        },
                    },
                },
                "thyristor": {
                    "jantx": {
                        "current": [1.0, 1.0, 0.9],
                        "temperature": [150.0, 125.0, 125.0],
                        "voltage": [1.0, 1.0, 0.9],
                    },
                    "military": {
                        "current": [0.9, 0.8, 0.5],
                        "temperature": [100.0, 85.0, 70.0],
                        "voltage": [0.9, 0.8, 0.5],
                    },
                    "commercial": {
                        "current": [0.6, 0.5, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                        "voltage": [0.6, 0.5, 0.0],
                    },
                },
                "transistor": {
                    "bjt": {
                        "jantx": {
                            "current": [1.0, 0.9, 0.9],
                            "power": [1.0, 1.0, 0.9],
                            "temperature": [150.0, 125.0, 125.0],
                            "voltage": [1.0, 0.9, 0.8],
                        },
                        "military": {
                            "current": [0.9, 0.8, 0.6],
                            "power": [0.9, 0.8, 0.6],
                            "temperature": [100.0, 85.0, 70.0],
                            "voltage": [0.8, 0.75, 0.3],
                        },
                        "commercial": {
                            "current": [0.5, 0.5, 0.0],
                            "power": [0.5, 0.5, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                            "voltage": [0.25, 0.25, 0.0],
                        },
                    },
                    "fet": {
                        "jantx": {
                            "power": [1.0, 1.0, 0.9],
                            "temperature": [150.0, 125.0, 125.0],
                            "voltage": [1.0, 0.95, 0.9],
                        },
                        "military": {
                            "power": [0.9, 0.8, 0.5],
                            "temperature": [100.0, 85.0, 70.0],
                            "voltage": [0.8, 0.75, 0.5],
                        },
                        "commercial": {
                            "power": [0.5, 0.5, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                            "voltage": [0.25, 0.25, 0.0],
                        },
                    },
                },
            },
            "resistor": {
                "fixed_composition": {
                    "low_power": {
                        "power": [0.65, 0.65, 0.65],
                        "temperature": [0.65, 0.65, 0.65],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "high_power": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                },
                "fixed_chip": {
                    "low_power": {
                        "power": [0.7, 0.7, 0.7],
                        "temperature": [0.7, 0.7, 0.7],
                    },
                    "high_power": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                    },
                },
                "fixed_film": {
                    "low_power": {
                        "power": [0.65, 0.65, 0.65],
                        "temperature": [0.65, 0.65, 0.65],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "high_power": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                },
                "fixed_film_power": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                },
                "fixed_film_network": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "fixed_wirewound": {
                    "low_power": {
                        "power": [0.7, 0.7, 0.7],
                        "temperature": [1.0, 1.0, 1.0],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "high_power": {
                        "power": [0.5, 0.5, 0.5],
                        "temperature": [1.0, 1.0, 1.0],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                },
                "fixed_wirewound_power": {
                    "power": [0.6, 0.6, 0.6],
                    "temperature": [0.6, 0.6, 0.6],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "fixed_wirewound_chassis": {
                    "power": [0.5, 0.5, 0.5],
                    "temperature": [0.5, 0.5, 0.5],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "variable_wirewound": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                },
                "variable_wirewound_precision": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                },
                "variable_wirewound_power": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [110.0, 110.0, 110.0],
                },
                "variable_composition": {
                    "power": [0.5, 0.5, 0.5],
                    "temperature": [0.5, 0.5, 0.5],
                },
                "variable_film": {
                    "power": [0.5, 0.5, 0.5],
                    "temperature": [0.5, 0.5, 0.5],
                },
                "variable_non_wirewound": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                },
            },
            "capacitor": {
                "paper": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.55, 0.55, 0.55],
                },
                "plastic": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.55, 0.55, 0.55],
                },
                "metallized": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.55, 0.55, 0.55],
                },
                "mica": {"temperature": [25.0, 25.0, 25.0], "voltage": [0.7, 0.7, 0.7]},
                "mica_button": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.55, 0.55, 0.55],
                },
                "glass": {
                    "temperature": [15.0, 15.0, 15.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "ceramic_fixed": {
                    "temperature": [15.0, 15.0, 15.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "temp_comp_ceramic": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "ceramic_chip": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "tantalum_chip": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "tantalum_solid": {
                    "reverse_voltage": [0.02, 0.02, 0.02],
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "tantalum_wet": {
                    "reverse_voltage": [0.02, 0.02, 0.02],
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "aluminum": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "aluminum_dry": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "ceramic_variable": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "piston": {
                    "temperature": [15.0, 15.0, 15.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "trimmer": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
                "vacuum": {
                    "temperature": [10.0, 10.0, 10.0],
                    "voltage": [0.6, 0.6, 0.6],
                },
            },
            "inductor": {
                "low_frequency": {
                    "current": [0.7, 0.7, 0.6],
                    "surge_current": [0.9, 0.9, 0.8],
                    "surge_voltage": [0.9, 0.9, 0.8],
                    "temperature": [30.0, 30.0, 30.0],
                    "voltage": [0.7, 0.7, 0.6],
                },
                "high_frequency": {
                    "current": [0.9, 0.9, 0.8],
                    "temperature": [30.0, 30.0, 30.0],
                },
            },
            "relay": {
                "capacitive_load": {
                    "current": [0.7, 0.6, 0.5],
                    "drop_out": [0.9, 0.9, 0.9],
                    "pick_up": [1.1, 1.1, 1.1],
                    "temperature": [10.0, 20.0, 30.0],
                },
                "inductive_load": {
                    "current": [0.5, 0.4, 0.3],
                    "drop_out": [0.9, 0.9, 0.9],
                    "pick_up": [1.1, 1.1, 1.1],
                    "temperature": [10.0, 20.0, 30.0],
                },
                "resistive_load": {
                    "current": [0.7, 0.6, 0.5],
                    "drop_out": [0.9, 0.9, 0.9],
                    "pick_up": [1.1, 1.1, 1.1],
                    "temperature": [10.0, 20.0, 30.0],
                },
            },
            "switch": {
                "lamp_load": {
                    "current": [0.2, 0.1, 0.1],
                    "power": [0.7, 0.6, 0.5],
                    "surge_current": [0.8, 0.8, 0.8],
                },
                "inductive_load": {
                    "current": [0.5, 0.4, 0.3],
                    "power": [0.7, 0.6, 0.5],
                    "surge_current": [0.8, 0.8, 0.8],
                },
                "resistive_load": {
                    "current": [0.7, 0.6, 0.5],
                    "power": [0.7, 0.6, 0.5],
                    "surge_current": [0.8, 0.8, 0.8],
                },
            },
            "connection": {"current": [1.0, 1.0, 1.0]},
            "miscellaneous": {"lamp": {"current": [0.2, 0.1, 0.1]}},
        },
    }

    toml.dump(_dic_user_configuration, open(_user_config.RAMSTK_PROG_CONF, "w"))
    _user_config.get_user_configuration()

    yield _user_config


@pytest.fixture
def test_csv_file_function(test_import_dir):
    """Create and populate a *.csv file for testing Function imports."""
    _test_file = f"{TMP_DIR}/test_inputs_functions.csv"

    with open(_test_file, "w", newline="") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Function"])
        filewriter.writerow(ROW_DATA[0])
        filewriter.writerow(ROW_DATA[1])

    yield _test_file


@pytest.fixture
def test_text_file_function(test_import_dir):
    """Create and populate a *.txt file for testing Function imports."""
    _test_file = f"{TMP_DIR}/test_inputs_functions.txt"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=" ", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Function"])
        filewriter.writerow(ROW_DATA[0])
        filewriter.writerow(ROW_DATA[1])

    yield _test_file


@pytest.fixture
def test_csv_file_requirement(test_import_dir):
    """Create and populate a *.csv file for testing Requirement import mapping."""
    _test_file = f"{TMP_DIR}/test_inputs_requirements.csv"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Requirement"])
        filewriter.writerow(ROW_DATA[2])

    yield _test_file


@pytest.fixture
def test_csv_file_hardware(test_import_dir):
    """Create and populate a *.csv file for testing Hardware import mapping."""
    _test_file = f"{TMP_DIR}/test_inputs_hardware.csv"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Hardware"])
        filewriter.writerow(ROW_DATA[3])

    yield _test_file


@pytest.fixture
def test_csv_file_validation(test_import_dir):
    """Create and populate a *.csv file for testing Validation import mapping."""
    _test_file = f"{TMP_DIR}/test_inputs_validation.csv"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Validation"])
        filewriter.writerow(ROW_DATA[4])

    yield _test_file


@pytest.fixture
def test_excel_file():
    """Create and populate a *.xls file for tests."""
    _test_file = f"{TMP_DIR}/test_inputs.xls"

    _book = xlwt.Workbook()
    _sheet = _book.add_sheet("Sheet 1", cell_overwrite_ok=True)

    for _col_num, _header in enumerate(HEADERS["Function"], start=1):
        _sheet.write(0, _col_num, _header)
    for _row_num, _row in enumerate(ROW_DATA[:2], start=1):
        _col_num = 1
        for _data in enumerate(_row):
            _sheet.write(_row_num, _col_num, _data[1])
            _col_num += 1
    _book.save(_test_file)

    yield _test_file


@pytest.fixture
def test_format_file():
    """Create and populate a RAMSTK layout format file."""
    _test_file = f"{TMP_DIR}/Test.xml"

    _root = ET.Element("root")
    _tree = ET.SubElement(_root, "tree", name="Test")
    _column = ET.SubElement(_tree, "column")
    ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 0"
    _column = ET.SubElement(_tree, "column")
    ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 1"
    _column = ET.SubElement(_tree, "column")
    ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 2"
    _column = ET.SubElement(_tree, "column")
    ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 3"

    _layout = ET.ElementTree(_root)
    _layout.write(_test_file)

    yield _test_file


@pytest.fixture(scope="function")
def test_stress_limits():
    """Create test stress limit dict."""
    yield {
        "integrated_circuit": {
            "digital": {
                "mos": {
                    "hermetic": {
                        "current": [0.9, 0.85, 0.8],
                        "fanout": [1.0, 0.9, 0.9],
                        "frequency": [0.9, 0.9, 0.9],
                        "temperature": [125.0, 110.0, 100.0],
                    },
                    "plastic1": {
                        "current": [0.9, 0.8, 0.0],
                        "fanout": [1.0, 0.9, 0.0],
                        "frequency": [0.9, 0.8, 0.0],
                        "temperature": [90.0, 85.0, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "fanout": [0.8, 0.0, 0.0],
                        "frequency": [0.8, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                    },
                },
                "bipolar": {
                    "hermetic": {
                        "current": [0.9, 0.85, 0.8],
                        "fanout": [0.9, 0.85, 0.8],
                        "frequency": [1.0, 0.9, 0.85],
                        "temperature": [125.0, 110.0, 100.0],
                    },
                    "plastic1": {
                        "current": [0.9, 0.8, 0.0],
                        "fanout": [0.9, 0.8, 0.0],
                        "frequency": [1.0, 0.9, 0.0],
                        "temperature": [90.0, 85.0, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "fanout": [0.7, 0.0, 0.0],
                        "frequency": [0.75, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                    },
                },
            },
            "linear": {
                "mos": {
                    "hermetic": {
                        "current": [0.9, 0.85, 0.8],
                        "fanout": [1.0, 0.9, 0.9],
                        "frequency": [0.9, 0.9, 0.9],
                        "temperature": [125.0, 110.0, 100.0],
                        "voltage": [0.8, 0.8, 0.7],
                    },
                    "plastic1": {
                        "current": [0.9, 0.8, 0.0],
                        "fanout": [1.0, 0.9, 0.0],
                        "frequency": [0.9, 0.8, 0.0],
                        "temperature": [90.0, 85.0, 0.0],
                        "voltage": [0.8, 0.7, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "fanout": [0.8, 0.0, 0.0],
                        "frequency": [0.8, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                        "voltage": [0.6, 0.0, 0.0],
                    },
                },
                "bipolar": {
                    "hermetic": {
                        "current": [0.9, 0.85, 0.8],
                        "fanout": [0.9, 0.85, 0.8],
                        "frequency": [1.0, 0.9, 0.85],
                        "temperature": [125.0, 110.0, 100.0],
                        "voltage": [0.8, 0.8, 0.7],
                    },
                    "plastic1": {
                        "current": [0.9, 0.8, 0.0],
                        "fanout": [0.9, 0.8, 0.0],
                        "frequency": [1.0, 0.9, 0.0],
                        "temperature": [90.0, 85.0, 0.0],
                        "voltage": [0.8, 0.7, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "fanout": [0.7, 0.0, 0.0],
                        "frequency": [0.75, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                        "voltage": [0.6, 0.0, 0.0],
                    },
                },
            },
            "microprocessor": {
                "mos": {
                    "hermetic": {
                        "current": [0.9, 0.85, 0.8],
                        "fanout": [1.0, 0.9, 0.9],
                        "frequency": [0.9, 0.9, 0.9],
                        "temperature": [125.0, 110.0, 100.0],
                    },
                    "plastic1": {
                        "current": [0.9, 0.8, 0.0],
                        "fanout": [1.0, 0.85, 0.0],
                        "frequency": [0.9, 0.8, 0.0],
                        "temperature": [85.0, 75.0, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "fanout": [0.8, 0.0, 0.0],
                        "frequency": [0.8, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                    },
                },
                "bipolar": {
                    "hermetic": {
                        "current": [0.8, 0.75, 0.7],
                        "fanout": [0.8, 0.75, 0.7],
                        "frequency": [0.9, 0.8, 0.75],
                        "temperature": [125.0, 110.0, 100.0],
                    },
                    "plastic1": {
                        "current": [0.8, 0.75, 0.0],
                        "fanout": [0.8, 0.75, 0.0],
                        "frequency": [0.9, 0.8, 0.0],
                        "temperature": [85.0, 75.0, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "fanout": [0.7, 0.0, 0.0],
                        "frequency": [0.75, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                    },
                },
            },
            "memory": {
                "mos": {
                    "hermetic": {
                        "current": [0.9, 0.85, 0.8],
                        "frequency": [1.0, 0.9, 0.9],
                        "temperature": [125.0, 110.0, 100.0],
                    },
                    "plastic1": {
                        "current": [0.9, 0.8, 0.0],
                        "frequency": [1.0, 0.9, 0.0],
                        "temperature": [90.0, 85.0, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "frequency": [0.8, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                    },
                },
                "bipolar": {
                    "hermetic": {
                        "current": [0.9, 0.85, 0.8],
                        "frequency": [1.0, 1.0, 0.9],
                        "temperature": [125.0, 110.0, 100.0],
                    },
                    "plastic1": {
                        "current": [0.9, 0.8, 0.0],
                        "frequency": [1.0, 0.95, 0.0],
                        "temperature": [90.0, 85.0, 0.0],
                    },
                    "plastic2": {
                        "current": [0.7, 0.0, 0.0],
                        "frequency": [0.8, 0.0, 0.0],
                        "temperature": [70.0, 0.0, 0.0],
                    },
                },
            },
        },
        "semiconductor": {
            "diode": {
                "general_purpose": {
                    "jantx": {
                        "current": [1.0, 1.0, 1.0],
                        "surge_current": [1.0, 0.9, 0.8],
                        "voltage": [0.95, 0.9, 0.85],
                        "temperature": [150.0, 125.0, 125.0],
                    },
                    "military": {
                        "current": [0.9, 0.9, 0.7],
                        "surge_current": [0.8, 0.8, 0.5],
                        "voltage": [0.8, 0.75, 0.5],
                        "temperature": [100.0, 85.0, 70.0],
                    },
                    "commercial": {
                        "current": [0.75, 0.7, 0.0],
                        "surge_current": [0.6, 0.3, 0.0],
                        "voltage": [0.7, 0.6, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                    },
                },
                "power_rectifier": {
                    "jantx": {
                        "current": [1.0, 1.0, 1.0],
                        "voltage": [0.95, 0.9, 0.85],
                        "temperature": [150.0, 125.0, 125.0],
                    },
                    "military": {
                        "current": [0.9, 0.85, 0.6],
                        "voltage": [0.8, 0.75, 0.3],
                        "temperature": [100.0, 85.0, 70.0],
                    },
                    "commercial": {
                        "current": [0.6, 0.5, 0.0],
                        "voltage": [0.5, 0.3, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                    },
                },
                "schottky": {
                    "jantx": {
                        "power": [1.0, 1.0, 0.9],
                        "voltage": [0.95, 0.9, 0.85],
                        "temperature": [150.0, 125.0, 125.0],
                    },
                    "military": {
                        "power": [0.9, 0.9, 0.5],
                        "voltage": [0.8, 0.8, 0.25],
                        "temperature": [100.0, 85.0, 70.0],
                    },
                    "commercial": {
                        "power": [0.75, 0.75, 0.0],
                        "voltage": [0.5, 0.3, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                    },
                },
                "regulator": {
                    "jantx": {
                        "power": [1.0, 1.0, 0.9],
                        "temperature": [150.0, 125.0, 125.0],
                    },
                    "military": {
                        "power": [0.9, 0.8, 0.5],
                        "temperature": [100.0, 85.0, 70.0],
                    },
                    "commercial": {
                        "power": [0.5, 0.5, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                    },
                },
                "suppressor": {
                    "jantx": {
                        "current": [1.0, 1.0, 0.9],
                        "power": [1.0, 1.0, 0.9],
                        "temperature": [150.0, 125.0, 125.0],
                    },
                    "military": {
                        "current": [0.8, 0.8, 0.5],
                        "power": [0.8, 0.8, 0.5],
                        "temperature": [100.0, 85.0, 70.0],
                    },
                    "commercial": {
                        "current": [0.75, 0.5, 0.0],
                        "power": [0.75, 0.5, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                    },
                },
            },
            "thyristor": {
                "jantx": {
                    "current": [1.0, 1.0, 0.9],
                    "temperature": [150.0, 125.0, 125.0],
                    "voltage": [1.0, 1.0, 0.9],
                },
                "military": {
                    "current": [0.9, 0.8, 0.5],
                    "temperature": [100.0, 85.0, 70.0],
                    "voltage": [0.9, 0.8, 0.5],
                },
                "commercial": {
                    "current": [0.6, 0.5, 0.0],
                    "temperature": [70.0, 35.0, 0.0],
                    "voltage": [0.6, 0.5, 0.0],
                },
            },
            "transistor": {
                "bjt": {
                    "jantx": {
                        "current": [1.0, 0.9, 0.9],
                        "power": [1.0, 1.0, 0.9],
                        "temperature": [150.0, 125.0, 125.0],
                        "voltage": [1.0, 0.9, 0.8],
                    },
                    "military": {
                        "current": [0.9, 0.8, 0.6],
                        "power": [0.9, 0.8, 0.6],
                        "temperature": [100.0, 85.0, 70.0],
                        "voltage": [0.8, 0.75, 0.3],
                    },
                    "commercial": {
                        "current": [0.5, 0.5, 0.0],
                        "power": [0.5, 0.5, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                        "voltage": [0.25, 0.25, 0.0],
                    },
                },
                "fet": {
                    "jantx": {
                        "power": [1.0, 1.0, 0.9],
                        "temperature": [150.0, 125.0, 125.0],
                        "voltage": [1.0, 0.95, 0.9],
                    },
                    "military": {
                        "power": [0.9, 0.8, 0.5],
                        "temperature": [100.0, 85.0, 70.0],
                        "voltage": [0.8, 0.75, 0.5],
                    },
                    "commercial": {
                        "power": [0.5, 0.5, 0.0],
                        "temperature": [70.0, 35.0, 0.0],
                        "voltage": [0.25, 0.25, 0.0],
                    },
                },
            },
        },
        "resistor": {
            "fixed_composition": {
                "low_power": {
                    "power": [0.65, 0.65, 0.65],
                    "temperature": [0.65, 0.65, 0.65],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "high_power": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                    "voltage": [0.7, 0.7, 0.7],
                },
            },
            "fixed_chip": {
                "low_power": {
                    "power": [0.7, 0.7, 0.7],
                    "temperature": [0.7, 0.7, 0.7],
                },
                "high_power": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                },
            },
            "fixed_film": {
                "low_power": {
                    "power": [0.65, 0.65, 0.65],
                    "temperature": [0.65, 0.65, 0.65],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "high_power": {
                    "power": [0.55, 0.55, 0.55],
                    "temperature": [0.55, 0.55, 0.55],
                    "voltage": [0.7, 0.7, 0.7],
                },
            },
            "fixed_film_power": {
                "power": [0.55, 0.55, 0.55],
                "temperature": [0.55, 0.55, 0.55],
            },
            "fixed_film_network": {
                "power": [0.55, 0.55, 0.55],
                "temperature": [0.55, 0.55, 0.55],
                "voltage": [0.7, 0.7, 0.7],
            },
            "fixed_wirewound": {
                "low_power": {
                    "power": [0.7, 0.7, 0.7],
                    "temperature": [1.0, 1.0, 1.0],
                    "voltage": [0.7, 0.7, 0.7],
                },
                "high_power": {
                    "power": [0.5, 0.5, 0.5],
                    "temperature": [1.0, 1.0, 1.0],
                    "voltage": [0.7, 0.7, 0.7],
                },
            },
            "fixed_wirewound_power": {
                "power": [0.6, 0.6, 0.6],
                "temperature": [0.6, 0.6, 0.6],
                "voltage": [0.7, 0.7, 0.7],
            },
            "fixed_wirewound_chassis": {
                "power": [0.5, 0.5, 0.5],
                "temperature": [0.5, 0.5, 0.5],
                "voltage": [0.7, 0.7, 0.7],
            },
            "variable_wirewound": {
                "power": [0.55, 0.55, 0.55],
                "temperature": [0.55, 0.55, 0.55],
            },
            "variable_wirewound_precision": {
                "power": [0.55, 0.55, 0.55],
                "temperature": [0.55, 0.55, 0.55],
            },
            "variable_wirewound_power": {
                "power": [0.55, 0.55, 0.55],
                "temperature": [110.0, 110.0, 110.0],
            },
            "variable_composition": {
                "power": [0.5, 0.5, 0.5],
                "temperature": [0.5, 0.5, 0.5],
            },
            "variable_film": {
                "power": [0.5, 0.5, 0.5],
                "temperature": [0.5, 0.5, 0.5],
            },
            "variable_non_wirewound": {
                "power": [0.55, 0.55, 0.55],
                "temperature": [0.55, 0.55, 0.55],
            },
        },
        "capacitor": {
            "paper": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.55, 0.55, 0.55],
            },
            "plastic": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.55, 0.55, 0.55],
            },
            "metallized": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.55, 0.55, 0.55],
            },
            "mica": {"temperature": [25.0, 25.0, 25.0], "voltage": [0.7, 0.7, 0.7]},
            "mica_button": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.55, 0.55, 0.55],
            },
            "glass": {
                "temperature": [15.0, 15.0, 15.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "ceramic_fixed": {
                "temperature": [15.0, 15.0, 15.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "temp_comp_ceramic": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "ceramic_chip": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "tantalum_chip": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "tantalum_solid": {
                "reverse_voltage": [0.02, 0.02, 0.02],
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "tantalum_wet": {
                "reverse_voltage": [0.02, 0.02, 0.02],
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "aluminum": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.7, 0.7, 0.7],
            },
            "aluminum_dry": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.7, 0.7, 0.7],
            },
            "ceramic_variable": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "piston": {
                "temperature": [15.0, 15.0, 15.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "trimmer": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
            "vacuum": {
                "temperature": [10.0, 10.0, 10.0],
                "voltage": [0.6, 0.6, 0.6],
            },
        },
        "inductor": {
            "low_frequency": {
                "current": [0.7, 0.7, 0.6],
                "surge_current": [0.9, 0.9, 0.8],
                "surge_voltage": [0.9, 0.9, 0.8],
                "temperature": [30.0, 30.0, 30.0],
                "voltage": [0.7, 0.7, 0.6],
            },
            "high_frequency": {
                "current": [0.9, 0.9, 0.8],
                "temperature": [30.0, 30.0, 30.0],
            },
        },
        "relay": {
            "capacitive_load": {
                "current": [0.7, 0.6, 0.5],
                "drop_out": [0.9, 0.9, 0.9],
                "pick_up": [1.1, 1.1, 1.1],
                "temperature": [10.0, 20.0, 30.0],
            },
            "inductive_load": {
                "current": [0.5, 0.4, 0.3],
                "drop_out": [0.9, 0.9, 0.9],
                "pick_up": [1.1, 1.1, 1.1],
                "temperature": [10.0, 20.0, 30.0],
            },
            "resistive_load": {
                "current": [0.7, 0.6, 0.5],
                "drop_out": [0.9, 0.9, 0.9],
                "pick_up": [1.1, 1.1, 1.1],
                "temperature": [10.0, 20.0, 30.0],
            },
        },
        "switch": {
            "lamp_load": {
                "current": [0.2, 0.1, 0.1],
                "power": [0.7, 0.6, 0.5],
                "surge_current": [0.8, 0.8, 0.8],
            },
            "inductive_load": {
                "current": [0.5, 0.4, 0.3],
                "power": [0.7, 0.6, 0.5],
                "surge_current": [0.8, 0.8, 0.8],
            },
            "resistive_load": {
                "current": [0.7, 0.6, 0.5],
                "power": [0.7, 0.6, 0.5],
                "surge_current": [0.8, 0.8, 0.8],
            },
        },
        "connection": {"current": [1.0, 1.0, 1.0]},
        "miscellaneous": {"lamp": {"current": [0.2, 0.1, 0.1]}},
    }


@pytest.fixture(scope="function")
def test_record_model(mock_dao):
    """Get a record model instance for each test function."""
    dut = mock_dao.do_select(node_id=0)

    yield dut

    # Delete the device under test.
    del dut
