# -*- coding: utf-8 -*-
#
#       rtk.modules.export.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle "weibullguy" Rowland
"""Export Package Data Controller Module."""

# Export other RTK modules.
from rtk.modules import RTKDataController
from . import dtmExports


class ExportDataController(RTKDataController):
    """
    Provide an interface between Export data models and RTK views.

    A single Export data controller can manage one or more Export
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Export data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RTK Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        :param configuration: the RTK configuration instance.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmExports(dao),
            rtk_module='exports',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_load_output(self, module, tree):
        """
        Request to load the module into the Pandas dataframe.

        :param str module: the module to load.
        :param tree: the treelib Tree() containing the data packages.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        return self._dtm_data_model.do_load_output(module, tree)

    def request_do_export(self, file_type, file_name):
        """
        Request to export RAMSTK module data to an external file.

        :param str file_type: the type of file to export the data to.
                              Currently supported files types are:
                                  - CSV (with semi-colon (;) delimiter.
                                  - Excel
                                  - Text
                                  - PDF
        :param str file_name: the name, with full path, of the file to export
                              the RAMSTK Progam database data to.
        :return: None
        :rtype: None
        """
        return self._dtm_data_model.do_export(file_type, file_name)
