# -*- coding: utf-8 -*-
#
#       rtk.modules.import.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Import Package Data Controller Module."""

# Import other RTK modules.
from rtk.modules import RTKDataController
from . import dtmImports


class ImportDataController(RTKDataController):
    """
    Provide an interface between Import data models and RTK views.

    A single Import data controller can manage one or more Import
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Import data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RTK Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        :param configuration: the RTK configuration instance.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmImports(dao),
            rtk_module='imports',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_get_db_fields(self, module):
        """
        Get the database field names.

        :param str module: the RAMSTK module to retrieve the fixed field names
                           for.
        :return: list of fixed field names.
        :rtype: list
        """
        return self._dtm_data_model.get_db_fields(module)

    def request_get_import(self, **kwargs):
        """
        Get the Site or Program import dict.

        :return: program_import; dict containing program import.
        :rtype: dict
        """
        _site = kwargs['site']
        _program = kwargs['program']
        _import = None

        if _site:
            _import = self._dtm_data_model.site_import.get_attributes()
        elif _program:
            _import = self._dtm_data_model.program_import.get_attributes()

        return _import

    def request_do_read_input(self, file_type, file_name):
        """
        Request to read the input file of file type.

        :param str file_type: the type of input file to be read.
        :param str file_name: the URL to the file to be read.
        :return: None
        :rtype: None
        """
        return self._dtm_data_model.do_read_input(file_type, file_name)

    def request_do_map_to_field(self, module, exim_field, format_field):
        """
        Request to map an input file field to a RAMSTK database table field.

        :param str module: the RAMSTK module to map header fields for.
        :param str exim_field: the string used for the column header in the
                               import file.
        :param str format_field: the string used for default titles in the RAMSTK
                                 layout file.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_map_to_field(module, exim_field,
                                                    format_field)

    def request_do_insert(self, module):
        """
        Request to insert an entity.

        :param str module: the RAMSTK module to insert a new entity for.th
        :return: (_count, _error_code, _msg); the number of entities inserted,
                 the error code and error message returned from the DAO object.
        :rtype: (int, int, str)
        """
        (_count, _error_code,
         _msg) = self._dtm_data_model.do_insert(module=module)

        if _error_code != 0:
            self._configuration.RTK_IMPORT_LOG.error(_msg)

        return _count, _error_code, _msg
