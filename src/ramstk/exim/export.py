# -*- coding: utf-8 -*-
#
#       ramstk.exim.export.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Export module."""

# Standard Library Imports
import os
from typing import Any, Dict

# Third Party Imports
# noinspection PyPackageRequirements
import pandas as pd
# noinspection PyPackageRequirements
from openpyxl import load_workbook
from pubsub import pub
from treelib import Tree


class Export:
    """Contains the methods for exporting data from a program database."""
    def __init__(self) -> None:
        """Initialize an Export module instance."""
        # Initialize private dictionary attributes.
        self._dic_output_data: Dict[str, Dict[int, Dict[Any, Any]]] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._df_output_data: pd.DataFrame = pd.DataFrame()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_data, 'succeed_get_function_tree')
        pub.subscribe(self._do_load_data, 'succeed_get_requirement_tree')
        pub.subscribe(self._do_load_data, 'succeed_get_hardware_tree')
        pub.subscribe(self._do_load_data, 'succeed_get_validation_tree')
        pub.subscribe(self._do_load_output, 'request_load_output')
        pub.subscribe(self._do_export, 'request_export_data')

    def _do_export(self, file_type: str, file_name: str) -> None:
        """Export selected RAMSTK module data to external file.

        :param file_type: the type of file to export the data to.
            Supported files types are:
                - CSV (using a semi-colon (;) delimiter)
                - Excel
                - Text (using a blank space delimiter)
        :param file_name: the name, with full path, of the file to export
            the RAMSTK Program database data to.
        :return: None
        :rtype: None
        """
        if file_type == 'csv':
            self._do_export_to_delimited_text(file_name, separator=';')
        elif file_type == 'excel':
            self._do_export_to_excel(file_name)
        elif file_type == 'text':
            self._do_export_to_delimited_text(file_name, separator=' ')

    def _do_export_to_delimited_text(self, file_name: str, separator: str):
        """Export RAMSTK project data to a delimited text file.

        :param file_name: the name of the file to export data.
        :param separator: the field delimiter to use.
        :return: None
        :rtype: None
        """
        for _key in self._dic_output_data:
            self._df_output_data = pd.DataFrame(self._dic_output_data[_key])

            self._df_output_data.to_csv(file_name, sep=separator, index=True)

    # pylint: disable=abstract-class-instantiated
    def _do_export_to_excel(self, file_name: str) -> None:
        """Export RAMSTK project data to an Excel file.

        :param file_name: the name of the file to export data.
        :return: None
        :rtype: None
        """
        _file, _extension = os.path.splitext(file_name)

        for _key in self._dic_output_data:
            self._df_output_data = pd.DataFrame(self._dic_output_data[_key])
            if _extension == '.xls':
                # xlwt can't write each module to a separate sheet so we'll
                # have to make a separate workbook for each work stream module.
                _writer = pd.ExcelWriter('{0:s}_{1:s}.xls'.format(_file, _key),
                                         engine='xlwt')
            elif _extension in ['.xlsx', '.xlsm']:
                _writer = pd.ExcelWriter(file_name, engine='openpyxl')
                # Set the writer workbook if it already exists, otherwise
                # just continue.  This allows each work stream module to be
                # written to it's own worksheet.  If the workbook doesn't
                # exist it will be created when the first module is written.
                try:
                    _workbook = load_workbook(file_name)
                    _writer.book = _workbook
                except FileNotFoundError:
                    pass
            else:
                file_name = _file + '.xls'
                _writer = pd.ExcelWriter(file_name, engine='xlwt')
            self._df_output_data.to_excel(_writer,
                                          '{0:s}'.format(_key),
                                          index=True)
            _writer.save()

            _writer.close()

    @staticmethod
    def _do_load_output(module: str) -> None:
        """Load data from the requested RAMSTK module into a Pandas DataFrame.

        :param module: the RAMSTK module to load for export.
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_get_{0:s}_tree'.format(module.lower()))

    def _do_load_data(self, tree: Tree) -> None:
        """Load the attribute data into a Pandas DataFrame.

        :param tree: the data manager tree for the module to export.
        :return: None
        :rtype: None
        """
        _dic_temp = {}
        _module = tree.get_node(0).tag.lower()
        self._dic_output_data[_module] = {}

        # pylint: disable=unused-variable
        for __, _node in enumerate(tree.nodes):
            try:
                _attributes = tree.nodes[_node].data[_module].get_attributes()
                for _key in _attributes:
                    _dic_temp[_key] = _attributes[_key]
            except TypeError:
                pass
            self._dic_output_data[_module][
                tree.nodes[_node].identifier] = _dic_temp
