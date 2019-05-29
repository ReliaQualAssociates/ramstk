# -*- coding: utf-8 -*-
#
#       ramstk.modules.preferences.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Preferences Package Data Controller Module."""

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from . import dtmPreferences


class PreferencesDataController(RAMSTKDataController):
    """
    Provide an interface between Preferences data models and RAMSTK views.

    A single Preferences data controller can manage one or more Preferences
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Preferences data controller instance.

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
            model=dtmPreferences(dao, _site_dao, configuration),
            ramstk_module='preferences',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_get_preferences(self, **kwargs):
        """
        Get the Site or User preferences dict.

        :return: program_options; dict containing program preferences.
        :rtype: dict
        """
        _site = kwargs['site']
        _user = kwargs['user']
        _preferences = None

        self._dtm_data_model.do_select_all(**kwargs)
        if _site:
            _preferences = self._dtm_data_model.site_preferences
        elif _user:
            _preferences = self._dtm_data_model.user_preferences

        return _preferences

    def request_set_preferences(self, preferences, **kwargs):
        """
        Set the Site or User preferences.

        :paran dict preferences: the dict containing the preferences and their
                                 values.
        :return: None
        :rtype: None
        """
        _site = kwargs['site']
        _user = kwargs['user']

        if _site:
            self._dtm_data_model.site_preferences = preferences
        elif _user:
            self._dtm_data_model.user_preferences = preferences

        return None

    def request_do_delete(self, entity):
        """
        Request to delete the record from the RAMSTK Site database.

        :param entity: the record in the RAMSTK Site database table to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_delete(entity)

    def request_do_update(self):
        """
        Request to update the Site or User Preferences.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_update()
