# -*- coding: utf-8 -*-
#
#       ramstk.modules.preferences.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Preferences Data Model."""

# Import other RAMSTK modules.
from rtk.modules import RTKDataModel
from rtk.dao import (RTKCategory, RTKCondition, RTKFailureMode, RTKGroup,
                     RTKHazards, RTKLoadHistory, RTKManufacturer,
                     RTKMeasurement, RTKMethod, RTKModel, RTKRPN,
                     RTKStakeholders, RTKStatus, RTKType, RTKUser)


class PreferencesDataModel(RTKDataModel):
    """Contains the attributes and methods of a user Preferences data model."""

    _tag = 'Preferences'

    def __init__(self, dao, site_dao, configuration):
        """
        Initialize a user Preferences data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

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
            dao, configuration)

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

        return None

    def do_delete(self, entity):    # pylint: disable=arguments-differ
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
            self.user_preferences)

        return _return


class SitePreferencesDataModel(RTKDataModel):
    """Contain the attributes and methods for Site-wide preferences."""

    _tag = 'SitePrefs'

    def __init__(self, dao):
        """
        Initialize a Site Preferences data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.
        self._site_preferences = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Site Preferences from the RTK Site database.

        This method retrieves all the records from the RTKSiteInfo table in the
        connected RTK Site database.  There should only be one record in the
        RTKSiteInfo database.

        :return: None
        :rtype: None
        """
        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        self._site_preferences['action_category'] = _session.query(
            RTKCategory).filter(RTKCategory.cat_type == 'action').all()
        self._site_preferences['incident_category'] = _session.query(
            RTKCategory).filter(RTKCategory.cat_type == 'incident').all()
        self._site_preferences['damaging_conditions'] = _session.query(
            RTKCondition).filter(RTKCondition.cond_type == 'operating').all()
        self._site_preferences['environment_conditions'] = _session.query(
            RTKCondition).filter(
                RTKCondition.cond_type == 'environment').all()
        self._site_preferences['failure_modes'] = _session.query(
            RTKFailureMode).all()
        self._site_preferences['workgroups'] = _session.query(RTKGroup).filter(
            RTKGroup.group_type == 'workgroup').all()
        self._site_preferences['affinity_groups'] = _session.query(
            RTKGroup).filter(RTKGroup.group_type == 'affinity').all()
        self._site_preferences['hazards'] = _session.query(RTKHazards).all()
        self._site_preferences['load_history'] = _session.query(
            RTKLoadHistory).all()
        self._site_preferences['manufacturers'] = _session.query(
            RTKManufacturer).all()
        self._site_preferences['measurement_units'] = _session.query(
            RTKMeasurement).filter(
                RTKMeasurement.measurement_type == 'unit').all()
        self._site_preferences['measureable_parameters'] = _session.query(
            RTKMeasurement).filter(
                RTKMeasurement.measurement_type == 'damage').all()
        self._site_preferences['detection_methods'] = _session.query(
            RTKMethod).all()
        self._site_preferences['damage_models'] = _session.query(
            RTKModel).all()
        self._site_preferences['rpn_detection'] = _session.query(
            RTKRPN).filter(RTKRPN.rpn_type == 'detection').all()
        self._site_preferences['rpn_occurrence'] = _session.query(
            RTKRPN).filter(RTKRPN.rpn_type == 'occurrence').all()
        self._site_preferences['rpn_severity'] = _session.query(RTKRPN).filter(
            RTKRPN.rpn_type == 'severity').all()
        self._site_preferences['stakeholders'] = _session.query(
            RTKStakeholders).all()
        self._site_preferences['action_status'] = _session.query(
            RTKStatus).filter(RTKStatus.status_type == 'action').all()
        self._site_preferences['incident_status'] = _session.query(
            RTKStatus).filter(RTKStatus.status_type == 'incident').all()
        self._site_preferences['incident_types'] = _session.query(
            RTKType).filter(RTKType.type_type == 'incident').all()
        self._site_preferences['requirement_types'] = _session.query(
            RTKType).filter(RTKType.type_type == 'requirement').all()
        self._site_preferences['validation_types'] = _session.query(
            RTKType).filter(RTKType.type_type == 'validation').all()
        self._site_preferences['users'] = _session.query(RTKUser).all()

        _session.close()

        return self._site_preferences

    def do_delete(self, entity):    # pylint: disable=arguments-differ
        """
        Delete the Site Preferences record from the RAMSTK Site database.

        :param entity: the record in the RAMSTK Site database table to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        _error_code, _msg = self.dao.db_delete(entity, _session)

        _session.close()

        if _error_code != 0:
            _return = True

        return _return

    def do_update(self, preferences):  # pylint: disable=arguments-differ
        """
        Update the Site Preferences record to the RTK Site database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        for _key in preferences:
            for _entity in preferences[_key]:
                _session.add(_entity)
        _error_code, _msg = self.dao.db_update(_session)

        _session.close()

        if _error_code != 0:
            _return = True

        return _return


class UserPreferencesDataModel(RTKDataModel):
    """Contains the attributes and methods for Program (user) preferences."""

    _tag = 'UserPrefs'

    def __init__(self, dao, configuration):
        """
        Initialize a User Preferences data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

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
        Retrieve all the Program preferences from the RTK Program database.

        This method retrieves all the records from the RTKProgramInfo table in
        the connected RTK Program database.

        :return: None
        :rtype: None
        """
        if not self._configuration.get_site_configuration():
            _temp = {'type': self._configuration.RTK_COM_BACKEND}
            self._user_preferences['common_db_info'] = _temp.copy()
            self._user_preferences['common_db_info'].update(
                self._configuration.RTK_COM_INFO)

        if not self._configuration.get_user_configuration():
            _temp = {'type': self._configuration.RTK_BACKEND}
            self._user_preferences['program_db_info'] = _temp.copy()
            self._user_preferences['program_db_info'].update(
                self._configuration.RTK_PROG_INFO)
            self._user_preferences[
                'report_size'] = self._configuration.RTK_REPORT_SIZE
            self._user_preferences[
                'hr_multiplier'] = self._configuration.RTK_HR_MULTIPLIER
            self._user_preferences[
                'decimal'] = self._configuration.RTK_DEC_PLACES
            self._user_preferences[
                'calcreltime'] = self._configuration.RTK_MTIME
            self._user_preferences['tabpos'] = self._configuration.RTK_TABPOS
            self._user_preferences[
                'sitedir'] = self._configuration.RTK_SITE_DIR
            self._user_preferences[
                'datadir'] = self._configuration.RTK_DATA_DIR
            self._user_preferences[
                'icondir'] = self._configuration.RTK_ICON_DIR
            self._user_preferences['logdir'] = self._configuration.RTK_LOG_DIR
            self._user_preferences[
                'progdir'] = self._configuration.RTK_PROG_DIR
            self._user_preferences[
                'format_files'] = self._configuration.RTK_FORMAT_FILE
            self._user_preferences['colors'] = self._configuration.RTK_COLORS

        return self._user_preferences

    def do_update(self, preferences):  # pylint: disable=arguments-differ
        """
        Update the User Preferences in the Site and Program config files.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._configuration.RTK_COM_BACKEND = preferences['common_db_info'][
            'type']
        self._configuration.RTK_COM_INFO['host'] = preferences[
            'common_db_info']['host']
        self._configuration.RTK_COM_INFO['socket'] = preferences[
            'common_db_info']['socket']
        self._configuration.RTK_COM_INFO['database'] = preferences[
            'common_db_info']['database']
        self._configuration.RTK_COM_INFO['user'] = preferences[
            'common_db_info']['user']
        self._configuration.RTK_COM_INFO['password'] = preferences[
            'common_db_info']['password']

        self._configuration.RTK_BACKEND = preferences['program_db_info'][
            'type']
        self._configuration.RTK_PROG_INFO['host'] = preferences[
            'program_db_info']['host']
        self._configuration.RTK_PROG_INFO['socket'] = preferences[
            'program_db_info']['socket']
        self._configuration.RTK_PROG_INFO['database'] = preferences[
            'program_db_info']['database']
        self._configuration.RTK_PROG_INFO['user'] = preferences[
            'program_db_info']['user']
        self._configuration.RTK_PROG_INFO['password'] = preferences[
            'program_db_info']['password']

        self._configuration.RTK_REPORT_SIZE = preferences['report_size']
        self._configuration.RTK_HR_MULTIPLIER = preferences['hr_multiplier']
        self._configuration.RTK_DEC_PLACES = preferences['decimal']
        self._configuration.RTK_MTIME = preferences['calcreltime']
        self._configuration.RTK_TABPOS = preferences['tabpos']
        self._configuration.RTK_SITE_DIR = preferences['sitedir']
        self._configuration.RTK_DATA_DIR = preferences['datadir']
        self._configuration.RTK_ICON_DIR = preferences['icondir']
        self._configuration.RTK_LOG_DIR = preferences['logdir']
        self._configuration.RTK_PROG_DIR = preferences['progdir']
        self._configuration.RTK_FORMAT_FILE = preferences['format_files']
        self._configuration.RTK_COLORS = preferences['colors']

        return self._configuration.set_user_configuration()
