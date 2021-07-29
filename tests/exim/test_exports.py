# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.exim.test_exports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle "weibullguy" Rowland
"""Test class for testing the Exports module."""

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import dmFunction, dmHardware, dmRequirement, dmValidation
from ramstk.exim import Export


@pytest.mark.usefixtures("test_program_dao")
class TestExport:
    """Test class for export methods."""

    @pytest.mark.unit
    def test_do_load_output_function(self, test_program_dao):
        """do_load_output() should return a Pandas DataFrame when loading
        Functions for export."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_function_tree")

        assert isinstance(DUT._dic_output_data, dict)
        assert isinstance(DUT._dic_output_data["function"], dict)

    @pytest.mark.unit
    def test_do_load_output_requirement(self, test_program_dao):
        """do_load_output() should return None when loading Requirements for
        export."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_requirement_tree")

        assert isinstance(DUT._dic_output_data, dict)
        assert isinstance(DUT._dic_output_data["requirement"], dict)

    @pytest.mark.unit
    def test_do_load_output_hardware(self, test_program_dao):
        """do_load_output() should return None when loading Hardware for
        export."""
        _hardware = dmHardware()
        _hardware.do_connect(test_program_dao)
        _hardware.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_hardwares_tree")

        assert isinstance(DUT._dic_output_data, dict)
        assert isinstance(DUT._dic_output_data["hardwares"], dict)

    @pytest.mark.unit
    def test_do_load_output_validation(self, test_program_dao):
        """do_load_output() should return None when loading Validations for
        export."""
        _validation = dmValidation()
        _validation.do_connect(test_program_dao)
        _validation.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_validation_tree")

        assert isinstance(DUT._dic_output_data, dict)
        assert isinstance(DUT._dic_output_data["validation"], dict)

    @pytest.mark.unit
    def test_do_export_to_csv(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to a CSV file."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_functions_tree")

        _test_csv = test_export_dir + "test_export_function.csv"
        assert DUT._do_export("csv", _test_csv) is None

    @pytest.mark.unit
    def test_do_export_to_xls(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to an Excel file."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_requirements_tree")

        _test_excel = test_export_dir + "test_export_requirement.xls"
        assert DUT._do_export("excel", _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_xlsx(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to an Excel file."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_requirements_tree")

        _test_excel = test_export_dir + "test_export_requirement.xlsx"
        assert DUT._do_export("excel", _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_xlsm(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to an Excel file."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_requirements_tree")

        _test_excel = test_export_dir + "test_export_requirement.xlsm"
        assert DUT._do_export("excel", _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_excel_unknown_extension(
        self, test_program_dao, test_export_dir
    ):
        """do_export() should return None when exporting to an Excel file and
        default to using the xlwt engine."""
        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_requirements_tree")

        _test_excel = test_export_dir + "test_export_requirement.xlbb"
        assert DUT._do_export("excel", _test_excel) is None

    @pytest.mark.unit
    def test_do_export_to_text(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to a text file."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_functions_tree")

        _test_text = test_export_dir + "test_export_function.txt"
        assert DUT._do_export("text", _test_text) is None

    @pytest.mark.unit
    def test_do_export_unknown_type(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to a text file."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_functions_tree")

        _test_text = test_export_dir + "test_export_function.txt"
        assert DUT._do_export("pdf", _test_text) is None

    @pytest.mark.unit
    def test_do_export_multi_sheet(self, test_program_dao, test_export_dir):
        """do_export() should return None when exporting to a text file."""
        _function = dmFunction()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        _requirement = dmRequirement()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        DUT = Export()

        pub.sendMessage("request_get_functions_tree")
        pub.sendMessage("request_get_requirements_tree")

        _test_multi = test_export_dir + "test_export_multi.xlsx"

        pub.sendMessage("request_export_data", file_type="excel", file_name=_test_multi)

        assert isinstance(DUT._df_output_data, pd.core.frame.DataFrame)
