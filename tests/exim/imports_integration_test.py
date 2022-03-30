# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.exim.imports_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT>
# reliaqual <DOT> com
"""Test class for testing the Imports class."""

# Standard Library Imports
import math
from collections import OrderedDict

# Third Party Imports
import numpy as np
import pandas as pd
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.exim import Import, _do_replace_nan, _get_input_value
from ramstk.models.db import BaseDatabase


@pytest.mark.usefixtures("test_csv_file_function", "test_program_dao")
class TestImport:
    """Test class for import methods."""

    def on_succeed_read_db_fields(self, db_fields):
        assert isinstance(db_fields, list)
        assert db_fields == [
            "Revision ID",
            "Function ID",
            "Level",
            "Function Code",
            "Function Name",
            "Parent",
            "Remarks",
            "Safety Critical",
            "Type",
        ]
        print("\033[36m\nsucceed_read_db_fields topic was broadcast.")

    def on_succeed_import_function(self, module):
        assert module == "Function"
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    def on_fail_import_function(self, error_message):
        assert error_message == (
            "_do_import: There was a problem importing "
            "Function records.  This is usually caused "
            "by key violations; check the ID and/or "
            "parent ID fields in the import file."
        )
        print("\033[35m\nfail_import_module topic was broadcast.")

    def on_succeed_import_requirement(self, module):
        assert module == "Requirement"
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    def on_succeed_import_hardware(self, module):
        assert module == "Hardware"
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    def on_succeed_import_validation(self, module):
        assert module == "Validation"
        print("\033[36m\nsucceed_import_module topic was broadcast.")

    @pytest.mark.integration
    def test_do_read_db_fields(self):
        """_do_read_db_fields() should return a list of database fields for the work
        stream module name passed."""
        pub.subscribe(self.on_succeed_read_db_fields, "succeed_read_db_fields")

        DUT = Import()

        pub.sendMessage("request_db_fields", module="Function")

        pub.unsubscribe(self.on_succeed_read_db_fields, "succeed_read_db_fields")

    @pytest.mark.integration
    def test_fail_insert_function(self, test_csv_file_function):
        """do_insert() should return a zero error code on success and create a new
        RAMSTKFunction object with it's attributes set from the external file data."""
        pub.subscribe(self.on_fail_import_function, "fail_import_module")

        DUT = Import()

        DUT._do_read_file("csv", test_csv_file_function)

        for _idx, _key in enumerate(DUT._dic_field_map["Function"]):
            DUT._do_map_to_field("Function", list(DUT._df_input_data)[_idx], _key)

        pub.sendMessage("request_import", module="Function")

        pub.unsubscribe(self.on_fail_import_function, "fail_import_module")

    @pytest.mark.integration
    def test_do_insert_requirement(self, test_program_dao, test_csv_file_requirement):
        """do_insert() should return a zero error code on success and create a new
        RAMSTKRequirement object with it's attributes set from the external file
        data."""
        pub.subscribe(self.on_succeed_import_requirement, "succeed_import_module")

        DUT = Import()
        pub.sendMessage("succeed_connect_program_database", dao=test_program_dao)

        DUT._do_read_file("csv", test_csv_file_requirement)

        for _idx, _key in enumerate(DUT._dic_field_map["Requirement"]):
            DUT._do_map_to_field("Requirement", list(DUT._df_input_data)[_idx], _key)

        pub.sendMessage("request_import", module="Requirement")

        pub.unsubscribe(self.on_succeed_import_requirement, "succeed_import_module")

    @pytest.mark.integration
    def test_do_insert_hardware(self, test_program_dao, test_csv_file_hardware):
        """do_insert() should return a zero error code on success and create a new
        RAMSTKHardware, RAMSTKDesignElectric, and RAMSTKReliability object with it's
        attributes set from the external file data."""
        pub.subscribe(self.on_succeed_import_hardware, "succeed_import_module")

        DUT = Import()
        pub.sendMessage("succeed_connect_program_database", dao=test_program_dao)

        DUT._do_read_file("csv", test_csv_file_hardware)

        for _idx, _key in enumerate(DUT._dic_field_map["Hardware"]):
            DUT._do_map_to_field("Hardware", list(DUT._df_input_data)[_idx], _key)
        for _idx, _key in enumerate(DUT._dic_field_map["Design Electric"]):
            if _idx == 0:
                DUT._do_map_to_field(
                    "Design Electric", list(DUT._df_input_data)[1], "Hardware ID"
                )
            else:
                DUT._do_map_to_field(
                    "Design Mechanic", list(DUT._df_input_data)[_idx + 28], _key
                )
        for _idx, _key in enumerate(DUT._dic_field_map["Reliability"]):
            if _idx == 0:
                DUT._do_map_to_field(
                    "Reliability", list(DUT._df_input_data)[1], "Hardware ID"
                )
            else:
                DUT._do_map_to_field(
                    "Reliability", list(DUT._df_input_data)[_idx + 82], _key
                )

        pub.sendMessage("request_import", module="Hardware")

        pub.unsubscribe(self.on_succeed_import_hardware, "succeed_import_module")

    @pytest.mark.skip
    def test_do_insert_validation(self, test_program_dao, test_csv_file_validation):
        """do_insert() should return None on success and create a new RAMSTKValidation
        object with it's attributes set from the external file data."""
        pub.subscribe(self.on_succeed_import_validation, "succeed_import_module")

        DUT = Import()
        pub.sendMessage("succeed_connect_program_database", dao=test_program_dao)

        DUT._do_read_file("csv", test_csv_file_validation)

        for _idx, _key in enumerate(DUT._dic_field_map["Validation"]):
            DUT._do_map_to_field("Validation", list(DUT._df_input_data)[_idx], _key)

        pub.sendMessage("request_import", module="Validation")

        pub.unsubscribe(self.on_succeed_import_validation, "succeed_import_module")

    @pytest.mark.integration
    def test_do_insert_unsupported(self, test_program_dao, test_csv_file_validation):
        """do_insert() should return None when passed a module name that doesn't
        exist."""
        DUT = Import()
        pub.sendMessage("succeed_connect_program_database", dao=test_program_dao)

        DUT._do_read_file("csv", test_csv_file_validation)

        for _idx, _key in enumerate(DUT._dic_field_map["Validation"]):
            DUT._do_map_to_field("Validation", list(DUT._df_input_data)[_idx], _key)

        assert DUT._do_import("Shibboly") is None
