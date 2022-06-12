# -*- coding: utf-8 -*-
#
#       ramstk.exim.export.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Export module."""


# Standard Library Imports
import contextlib
import os
from typing import Dict, Union

# Third Party Imports
import pandas as pd

# noinspection PyPackageRequirements
from openpyxl import Workbook

# noinspection PyPackageRequirements
from openpyxl.utils.dataframe import dataframe_to_rows
from pubsub import pub
from treelib import Tree


class Export:
    """Contains the methods for exporting data from a program database."""

    def __init__(self) -> None:
        """Initialize an Export module instance."""
        # Initialize private dictionary attributes.
        self._dic_output_data: Dict[
            str, Dict[int, Dict[str, Union[bool, float, int, str]]]
        ] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._df_output_data: pd.DataFrame = pd.DataFrame()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_data, "succeed_get_allocation_tree")
        pub.subscribe(self._do_load_data, "succeed_get_fmeca_tree")
        pub.subscribe(self._do_load_data, "succeed_get_function_tree")
        pub.subscribe(self._do_load_data, "succeed_get_hardware_bom_tree")
        pub.subscribe(self._do_load_data, "succeed_get_hazard_tree")
        pub.subscribe(self._do_load_data, "succeed_get_pof_tree")
        pub.subscribe(self._do_load_data, "succeed_get_requirement_tree")
        pub.subscribe(self._do_load_data, "succeed_get_revision_tree")
        pub.subscribe(self._do_load_data, "succeed_get_similar_item_tree")
        pub.subscribe(self._do_load_data, "succeed_get_stakeholder_tree")
        pub.subscribe(self._do_load_data, "succeed_get_usage_profile_tree")
        pub.subscribe(self._do_load_data, "succeed_get_validation_tree")
        pub.subscribe(self._do_request_data_trees, "request_export_data")

    def _do_export(self, modules: Dict[str, bool], file_name: str) -> None:
        """Export selected RAMSTK module data to external file.

        :param modules: dict of RAMSTK modules to export.
        :param file_name: the name, with full path, of the file to export
            the RAMSTK Program database data to.
        :return: None
        :rtype: None
        """
        _file_type = os.path.splitext(file_name)[1]

        if _file_type == ".csv":
            self._do_export_to_delimited_text(file_name, separator=";")
        elif _file_type == ".xls":
            for _module in modules:
                self._do_export_to_excel_legacy(_module, file_name)
        elif _file_type in [".xlsx", ".xlsm"]:
            self._do_export_to_excel(modules, file_name)
        else:
            self._do_export_to_delimited_text(file_name, separator=" ")

    def _do_export_to_delimited_text(self, file_name: str, separator: str) -> None:
        """Export RAMSTK project data to a delimited text file.

        :param file_name: the name of the file to export data.
        :param separator: the field delimiter to use.
        :return: None
        :rtype: None
        """
        _file, _extension = os.path.splitext(file_name)

        if not os.path.isdir(_file):
            os.makedirs(f"{_file}")

        for (
            _module,
            _data,
        ) in self._dic_output_data.items():
            self._df_output_data = pd.DataFrame(_data)

            self._df_output_data.to_csv(
                f"{_file}/{_module}{_extension}", sep=separator, index=True
            )

    # pylint: disable=abstract-class-instantiated
    def _do_export_to_excel_legacy(self, module: str, file_name: str) -> None:
        """Export RAMSTK project data to an Excel file.

        :param module: the RAMSTK work flow module to export.
        :param file_name: the name of the file to export data.
        :return: None
        :rtype: None
        """
        _file, _extension = os.path.splitext(file_name)

        for (
            _key,
            _data,
        ) in self._dic_output_data.items():
            self._df_output_data = pd.DataFrame(_data)

            # xlwt can't write each module to a separate sheet, so we'll
            # have to make a separate workbook for each work stream module.
            _writer = pd.ExcelWriter(f"{_file}_{module}.xls")
            self._df_output_data.to_excel(_writer, f"{module}", index=True)
            _writer.save()
            _writer.close()

    # pylint: disable=abstract-class-instantiated
    def _do_export_to_excel(self, modules: Dict[str, bool], file_name: str) -> None:
        """Export RAMSTK project data to an Excel file.

        :param module: the RAMSTK work flow module to export.
        :param file_name: the name of the file to export data.
        :return: None
        :rtype: None
        """
        _workbook = Workbook()

        for _module, _request in modules.items():
            if _request:
                self._df_output_data = pd.DataFrame(self._dic_output_data[_module])
                _worksheet = _workbook.create_sheet(title=f"{_module}")

                for _row in dataframe_to_rows(
                    self._df_output_data,
                    index=True,
                    header=True,
                ):
                    _worksheet.append(_row)

        # It's a hack!  openpyxl creates a worksheet 'Sheet' by default.  We don't
        # need this worksheet, so remove it.
        _workbook.remove(_workbook["Sheet"])
        _workbook.save(file_name)

    def _do_load_data(self, tree: Tree) -> None:
        """Load the attribute data into a Pandas DataFrame.

        :param tree: the data manager tree for the module to export.
        :return: None
        :rtype: None
        """
        _module = tree.get_node(0).tag.lower()
        self._dic_output_data[_module] = {}

        for _node in tree.all_nodes()[1:]:
            with contextlib.suppress(KeyError, TypeError):
                self._dic_output_data[_module][_node.identifier] = {}
                for _model in _node.data:
                    self._dic_output_data[_module][_node.identifier].update(
                        _node.data[_model].get_attributes()
                    )

    def _do_request_data_trees(self, modules: Dict[str, bool], file_name: str) -> None:
        """Request RAMSTK module data trees.

        :param modules: dict of RAMSTK modules to export.
        :param file_name: the name, with full path, of the file to export
            the RAMSTK Program database data to.
        :return: None
        :rtype: None
        """
        for _module, _request in modules.items():
            if _request:
                pub.sendMessage(f"request_get_{_module}_tree")

        self._do_export(modules, file_name)
