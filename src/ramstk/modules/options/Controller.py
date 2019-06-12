# -*- coding: utf-8 -*-
#
#       ramstk.modules.options.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Package Data Controller Module."""

# RAMSTK Package Imports
# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController

# RAMSTK Local Imports
from . import dtmOptions


class OptionsDataController(RAMSTKDataController):
    """
    Provide an interface between Options data models and RAMSTK views.

    A single Options data controller can manage one or more Options
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Options data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RAMSTK Program database.
        :type dao: :py:class:`ramstk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        _site_dao = kwargs['site_dao']
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmOptions(dao, _site_dao),
            ramstk_module='options',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_select_all(self, attributes):
        """
        Retrieve the treelib Tree() from the RAMSTK Data Model.

        The RAMSTK Data Model method sends the 'retrieved_<module>' PyPubSub
        message.

        :return: None
        :rtype: None
        """
        return self._dtm_data_model.do_select_all(
            site=attributes['site'], program=attributes['program'],
        )

    def request_get_options(self, **kwargs):
        """
        Get the Site or Program options dict.

        :return: program_options; dict containing program options.
        :rtype: dict
        """
        _site = kwargs['site']
        _program = kwargs['program']
        _options = None

        if _site:
            _options = self._dtm_data_model.site_options.get_attributes()
        elif _program:
            _options = self._dtm_data_model.program_options.get_attributes()

        return _options

    def request_set_options(self, options, **kwargs):
        """
        Set the Site or Program options dict.

        :return: _error_code, _msg; the error code and associated message.
        :rtype: (int, str)
        """
        _site = kwargs['site']
        _program = kwargs['program']
        _error_code = 0
        _msg = ''

        if _site:
            (
                _error_code,
                _msg,
            ) = self._dtm_data_model.site_options.set_attributes(options)
        elif _program:
            (
                _error_code, _msg,
            ) = self._dtm_data_model.program_options.set_attributes(options)

        return (_error_code, _msg)

    def request_do_update(self):    # pylint: disable=arguments-differ
        """
        Request to update an RAMSTKOptions table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_update()
