# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.exim.exports_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Exports module."""

# Third Party Imports
import pandas as pd

# noinspection PyPackageRequirements
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.exim import Export
from ramstk.models.dbtables import (
    RAMSTKFunctionTable,
    RAMSTKHardwareTable,
    RAMSTKRequirementTable,
    RAMSTKValidationTable,
)
from ramstk.models.dbviews import RAMSTKHardwareBoMView


@pytest.mark.usefixtures("test_program_dao")
class TestExport:
    """Test class for export methods."""

    @pytest.mark.integration
    def test_do_load_output_function(self, test_program_dao):
        """Should create a dict of Function attributes for export."""
        _function = RAMSTKFunctionTable()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_function_tree")

        assert isinstance(dut._dic_output_data, dict)
        assert isinstance(dut._dic_output_data["function"], dict)

    @pytest.mark.integration
    def test_do_load_output_requirement(self, test_program_dao):
        """Should create a dict of Requirement attributes for export."""
        _requirement = RAMSTKRequirementTable()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_requirement_tree")

        assert isinstance(dut._dic_output_data, dict)
        assert isinstance(dut._dic_output_data["requirement"], dict)

    @pytest.mark.integration
    def test_do_load_output_hardware(self, test_program_dao):
        """Should create a dict of Hardware attributes for export."""
        _hardware = RAMSTKHardwareBoMView()

        dut = Export()

        pub.sendMessage("request_get_hardware_bom_tree")

        assert isinstance(dut._dic_output_data, dict)
        assert isinstance(dut._dic_output_data["hardware_bom"], dict)

    @pytest.mark.integration
    def test_do_load_output_validation(self, test_program_dao):
        """Should create a dict of Validation attributes for export."""
        _validation = RAMSTKValidationTable()
        _validation.do_connect(test_program_dao)
        _validation.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_validation_tree")

        assert isinstance(dut._dic_output_data, dict)
        assert isinstance(dut._dic_output_data["validation"], dict)

    @pytest.mark.integration
    def test_do_export_to_csv(self, test_program_dao, test_export_dir):
        """Should return None when exporting to a CSV file."""
        _function = RAMSTKFunctionTable()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_functions_tree")

        _test_csv = test_export_dir + "test_export_function.csv"
        assert dut._do_export({"requirement": True}, _test_csv) is None

    @pytest.mark.integration
    def test_do_export_to_xls(self, test_program_dao, test_export_dir):
        """Should return None when exporting to a legacy Excel file."""
        _requirement = RAMSTKRequirementTable()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_requirement_tree")

        _test_excel = test_export_dir + "test_export_requirement.xls"
        assert dut._do_export({"requirement": True}, _test_excel) is None

    @pytest.mark.integration
    def test_do_export_to_xlsx(self, test_program_dao, test_export_dir):
        """Should return None when exporting to an Excel file."""
        _requirement = RAMSTKRequirementTable()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_requirement_tree")

        _test_excel = test_export_dir + "test_export_requirement.xlsx"
        assert dut._do_export({"requirement": True}, _test_excel) is None

    @pytest.mark.integration
    def test_do_export_to_xlsm(self, test_program_dao, test_export_dir):
        """Should return None when exporting to a macro-enabled Excel file."""
        _requirement = RAMSTKRequirementTable()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_requirement_tree")

        _test_excel = test_export_dir + "test_export_requirement.xlsm"
        assert dut._do_export({"requirement": True}, _test_excel) is None

    @pytest.mark.integration
    def test_do_export_to_excel_unknown_extension(
        self, test_program_dao, test_export_dir
    ):
        """Should return None when exporting to an Excel file."""
        _requirement = RAMSTKRequirementTable()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_requirement_tree")

        _test_excel = test_export_dir + "test_export_requirement.xlbb"
        assert dut._do_export({"requirement": True}, _test_excel) is None

    @pytest.mark.integration
    def test_do_export_to_text(self, test_program_dao, test_export_dir):
        """Should return None when exporting to a delimited text file."""
        _function = RAMSTKFunctionTable()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_function_tree")

        _test_text = test_export_dir + "test_export_function.txt"
        assert dut._do_export({"function": True}, _test_text) is None

    @pytest.mark.integration
    def test_do_export_unknown_type(self, test_program_dao, test_export_dir):
        """Should return None and default to a text file."""
        _function = RAMSTKFunctionTable()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_function_tree")

        _test_text = test_export_dir + "test_export_function.pdf"
        assert dut._do_export({"requirement": True}, _test_text) is None

    @pytest.mark.integration
    def test_do_export_multi_sheet(self, test_program_dao, test_export_dir):
        """Should return None when exporting to a text file."""
        _function = RAMSTKFunctionTable()
        _function.do_connect(test_program_dao)
        _function.do_select_all(attributes={"revision_id": 1})

        _requirement = RAMSTKRequirementTable()
        _requirement.do_connect(test_program_dao)
        _requirement.do_select_all(attributes={"revision_id": 1})

        dut = Export()

        pub.sendMessage("request_get_function_tree")
        pub.sendMessage("request_get_requirement_tree")

        _test_multi = test_export_dir + "test_export_multi.xlsx"

        pub.sendMessage(
            "request_export_data",
            modules={"requirement": True, "function": True, "hardware_bom": False},
            file_name=_test_multi,
        )

        assert isinstance(dut._df_output_data, pd.core.frame.DataFrame)
