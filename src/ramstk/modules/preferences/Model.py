# -*- coding: utf-8 -*-
#
#       ramstk.modules.preferences.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Preferences Data Model."""

# RAMSTK Package Imports
from ramstk.dao.commondb import (
    RAMSTKRPN, RAMSTKCategory, RAMSTKCondition, RAMSTKFailureMode,
    RAMSTKGroup, RAMSTKHazards, RAMSTKLoadHistory,
    RAMSTKManufacturer, RAMSTKMeasurement, RAMSTKMethod, RAMSTKModel,
    RAMSTKStakeholders, RAMSTKStatus, RAMSTKType, RAMSTKUser,
)
from ramstk.modules import RAMSTKDataModel


class PreferencesDataModel(RAMSTKDataModel):
    """Contains the attributes and methods of a user Preferences data model."""

    _tag = 'Preferences'
    _root = 0

    def __init__(self, dao, site_dao, configuration):
        """
        Initialize a user Preferences data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.site_preferences = {}
        self.user_preferences = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_site_preferences = SitePreferencesDataModel(site_dao)
        self.dtm_user_preferences = UserPreferencesDataModel(
            dao, configuration,
        )

    def do_select_all(self, **kwargs):
        """
        Retrieve user Preferences from the Site and Program config files.

        :return: None
        :rtype: None
        """
        _site = kwargs['site']
        _user = kwargs['user']

        if _site:
            self.site_preferences = self.dtm_site_preferences.do_select_all()
        if _user:
            self.user_preferences = self.dtm_user_preferences.do_select_all()

    def do_delete(self, entity):  # pylint: disable=arguments-differ
        """
        Delete the Site Preferences record from the RAMSTK Site database.

        :param entity: the record in the RAMSTK Site database table to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self.dtm_site_preferences.do_delete(entity)

    def do_update(self):  # pylint: disable=arguments-differ
        """
        Update the selected user Preferences in the Program config file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = self.dtm_site_preferences.do_update(self.site_preferences)
        _return = _return or self.dtm_user_preferences.do_update(
            self.user_preferences,
        )

        return _return


class SitePreferencesDataModel(RAMSTKDataModel):
    """Contain the attributes and methods for Site-wide preferences."""

    _tag = 'SitePrefs'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Site Preferences data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.
        self._site_preferences = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Site Preferences from the RAMSTK Site database.

        This method retrieves all the records from the RAMSTKSiteInfo table in the
        connected RAMSTK Site database.  There should only be one record in the
        RAMSTKSiteInfo database.

        :return: None
        :rtype: None
        """
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        self._site_preferences['action_category'] = _session.query(
            RAMSTKCategory,
        ).filter(RAMSTKCategory.cat_type == 'action').all()
        self._site_preferences['incident_category'] = _session.query(
            RAMSTKCategory,
        ).filter(
            RAMSTKCategory.cat_type == 'incident',
        ).all()
        self._site_preferences['damaging_conditions'] = _session.query(
            RAMSTKCondition,
        ).filter(
            RAMSTKCondition.cond_type == 'operating',
        ).all()
        self._site_preferences['environment_conditions'] = _session.query(
            RAMSTKCondition,
        ).filter(
            RAMSTKCondition.cond_type == 'environment',
        ).all()
        self._site_preferences['failure_modes'] = _session.query(
            RAMSTKFailureMode,
        ).all()
        self._site_preferences['workgroups'] = _session.query(
            RAMSTKGroup,
        ).filter(RAMSTKGroup.group_type == 'workgroup').all()
        self._site_preferences['affinity_groups'] = _session.query(
            RAMSTKGroup,
        ).filter(RAMSTKGroup.group_type == 'affinity').all()
        self._site_preferences['hazards'] = _session.query(RAMSTKHazards).all()
        self._site_preferences['load_history'] = _session.query(
            RAMSTKLoadHistory,
        ).all()
        self._site_preferences['manufacturers'] = _session.query(
            RAMSTKManufacturer,
        ).all()
        self._site_preferences['measurement_units'] = _session.query(
            RAMSTKMeasurement,
        ).filter(
            RAMSTKMeasurement.measurement_type == 'unit',
        ).all()
        self._site_preferences['measureable_parameters'] = _session.query(
            RAMSTKMeasurement,
        ).filter(
            RAMSTKMeasurement.measurement_type == 'damage',
        ).all()
        self._site_preferences['detection_methods'] = _session.query(
            RAMSTKMethod,
        ).all()
        self._site_preferences['damage_models'] = _session.query(
            RAMSTKModel,
        ).all()
        self._site_preferences['rpn_detection'] = _session.query(
            RAMSTKRPN,
        ).filter(RAMSTKRPN.rpn_type == 'detection').all()
        self._site_preferences['rpn_occurrence'] = _session.query(
            RAMSTKRPN,
        ).filter(RAMSTKRPN.rpn_type == 'occurrence').all()
        self._site_preferences['rpn_severity'] = _session.query(
            RAMSTKRPN,
        ).filter(RAMSTKRPN.rpn_type == 'severity').all()
        self._site_preferences['stakeholders'] = _session.query(
            RAMSTKStakeholders,
        ).all()
        self._site_preferences['action_status'] = _session.query(
            RAMSTKStatus,
        ).filter(RAMSTKStatus.status_type == 'action').all()
        self._site_preferences['incident_status'] = _session.query(
            RAMSTKStatus,
        ).filter(RAMSTKStatus.status_type == 'incident').all()
        self._site_preferences['incident_types'] = _session.query(
            RAMSTKType,
        ).filter(RAMSTKType.type_type == 'incident').all()
        self._site_preferences['requirement_types'] = _session.query(
            RAMSTKType,
        ).filter(RAMSTKType.type_type == 'requirement').all()
        self._site_preferences['validation_types'] = _session.query(
            RAMSTKType,
        ).filter(RAMSTKType.type_type == 'validation').all()
        self._site_preferences['users'] = _session.query(RAMSTKUser).all()

        _session.close()

        return self._site_preferences

    def do_delete(self, entity):  # pylint: disable=arguments-differ
        """
        Delete the Site Preferences record from the RAMSTK Site database.

        :param entity: the record in the RAMSTK Site database table to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

        _error_code, _msg = self.dao.db_delete(entity, _session)

        _session.close()

        if _error_code != 0:
            _return = True

        return _return

    def do_update(self, preferences):  # pylint: disable=arguments-differ
        """
        Update the Site Preferences record to the RAMSTK Site database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

        for _key in preferences:
            for _entity in preferences[_key]:
                _session.add(_entity)
        _error_code, _msg = self.dao.db_update(_session)

        _session.close()

        if _error_code != 0:
            _return = True

        return _return


class UserPreferencesDataModel(RAMSTKDataModel):
    """Contains the attributes and methods for Program (user) preferences."""

    _tag = 'UserPrefs'
    _root = 0

    def __init__(self, dao, configuration):
        """
        Initialize a User Preferences data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.
        self._user_preferences = {}
        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._configuration = configuration

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Program preferences from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKProgramInfo table in
        the connected RAMSTK Program database.

        :return: None
        :rtype: None
        """
        if not self._configuration.get_site_configuration():
            _temp = {'type': self._configuration.RAMSTK_COM_BACKEND}
            self._user_preferences['common_db_info'] = _temp.copy()
            self._user_preferences['common_db_info'].update(
                self._configuration.RAMSTK_COM_INFO,
            )

        if not self._configuration.get_user_configuration():
            _temp = {'type': self._configuration.RAMSTK_BACKEND}
            self._user_preferences['program_db_info'] = _temp.copy()
            self._user_preferences['program_db_info'].update(
                self._configuration.RAMSTK_PROG_INFO,
            )
            self._user_preferences[
                'report_size'
            ] = self._configuration.RAMSTK_REPORT_SIZE
            self._user_preferences[
                'hr_multiplier'
            ] = self._configuration.RAMSTK_HR_MULTIPLIER
            self._user_preferences[
                'decimal'
            ] = self._configuration.RAMSTK_DEC_PLACES
            self._user_preferences[
                'calcreltime'
            ] = self._configuration.RAMSTK_MTIME
            self._user_preferences[
                'tabpos'
            ] = self._configuration.RAMSTK_TABPOS
            self._user_preferences[
                'sitedir'
            ] = self._configuration.RAMSTK_SITE_DIR
            self._user_preferences[
                'datadir'
            ] = self._configuration.RAMSTK_DATA_DIR
            self._user_preferences[
                'icondir'
            ] = self._configuration.RAMSTK_ICON_DIR
            self._user_preferences[
                'logdir'
            ] = self._configuration.RAMSTK_LOG_DIR
            self._user_preferences[
                'progdir'
            ] = self._configuration.RAMSTK_PROG_DIR
            self._user_preferences[
                'format_files'
            ] = self._configuration.RAMSTK_FORMAT_FILE
            self._user_preferences[
                'colors'
            ] = self._configuration.RAMSTK_COLORS

        return self._user_preferences

    def do_update(self, preferences):  # pylint: disable=arguments-differ
        """
        Update the User Preferences in the Site and Program config files.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._configuration.RAMSTK_COM_BACKEND = preferences['common_db_info'][
            'type'
        ]
        self._configuration.RAMSTK_COM_INFO['host'] = preferences[
            'common_db_info'
        ]['host']
        self._configuration.RAMSTK_COM_INFO['socket'] = preferences[
            'common_db_info'
        ]['socket']
        self._configuration.RAMSTK_COM_INFO['database'] = preferences[
            'common_db_info'
        ]['database']
        self._configuration.RAMSTK_COM_INFO['user'] = preferences[
            'common_db_info'
        ]['user']
        self._configuration.RAMSTK_COM_INFO['password'] = preferences[
            'common_db_info'
        ]['password']

        self._configuration.RAMSTK_BACKEND = preferences['program_db_info'][
            'type'
        ]
        self._configuration.RAMSTK_PROG_INFO['host'] = preferences[
            'program_db_info'
        ]['host']
        self._configuration.RAMSTK_PROG_INFO['socket'] = preferences[
            'program_db_info'
        ]['socket']
        self._configuration.RAMSTK_PROG_INFO['database'] = preferences[
            'program_db_info'
        ]['database']
        self._configuration.RAMSTK_PROG_INFO['user'] = preferences[
            'program_db_info'
        ]['user']
        self._configuration.RAMSTK_PROG_INFO['password'] = preferences[
            'program_db_info'
        ]['password']

        self._configuration.RAMSTK_REPORT_SIZE = preferences['report_size']
        self._configuration.RAMSTK_HR_MULTIPLIER = preferences['hr_multiplier']
        self._configuration.RAMSTK_DEC_PLACES = preferences['decimal']
        self._configuration.RAMSTK_MTIME = preferences['calcreltime']
        self._configuration.RAMSTK_TABPOS = preferences['tabpos']
        self._configuration.RAMSTK_SITE_DIR = preferences['sitedir']
        self._configuration.RAMSTK_DATA_DIR = preferences['datadir']
        self._configuration.RAMSTK_ICON_DIR = preferences['icondir']
        self._configuration.RAMSTK_LOG_DIR = preferences['logdir']
        self._configuration.RAMSTK_PROG_DIR = preferences['progdir']
        self._configuration.RAMSTK_FORMAT_FILE = preferences['format_files']
        self._configuration.RAMSTK_COLORS = preferences['colors']

        return self._configuration.set_user_configuration()
