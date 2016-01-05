#!/usr/bin/env python
"""
##########################################
Incident Component Sub-Package Data Module
##########################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.incident.component.Component.py is part of The RTK Project
#
# All rights reserved.

# Import other RTK modules.
try:
    import Utilities as _util
except ImportError:
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'


class Model(object):                       # pylint: disable=R0902, R0904
    """
    The Incident Component data model contains the attributes and methods for
    an Incident Component. The attributes of an Incident Component model are:

    :ivar lstRelevant :default value: [False, False, False, False, False,
                                       False, False, False, False, False,
                                       False, False, False, False, False,
                                       False, False, False, False, False]
    :ivar lstChargeable :default value: [False, False, False, False, False,
                                         False, False, False, False, False]
    :ivar incident_id :default value: None
    :ivar component_id :default value: None
    :ivar age_at_incident :default value: 0.0
    :ivar failure :default value: False
    :ivar suspension :default value: False
    :ivar cnd_nff :default value: False
    :ivar occ_fault :default value: False
    :ivar initial_installation :default value: False
    :ivar interval_censored :default value: False
    :ivar use_op_time :default value: False
    :ivar use_cal_time :default value: False
    :ivar ttf :default value: 0.0
    :ivar mode_type :default value: 0
    :ivar relevant :default value: False
    :ivar chargeable :default value: False
    """

    def __init__(self):
        """
        Method to initialize a Incident data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.

        # Initialize public list attributes.
        self.lstRelevant = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                            -1, -1, -1, -1, -1, -1, -1]
        self.lstChargeable = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        # Initialize public scalar attributes.
        self.incident_id = None
        self.component_id = None
        self.age_at_incident = 0.0
        self.failure = 0
        self.suspension = 0
        self.cnd_nff = 0
        self.occ_fault = 0
        self.initial_installation = 0
        self.interval_censored = 0
        self.use_op_time = 0
        self.use_cal_time = 0
        self.ttf = 0.0
        self.mode_type = 0
        self.relevant = -1
        self.chargeable = -1

    def set_attributes(self, values):
        """
        Method to set the Incident data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.incident_id = int(values[0])
            self.component_id = int(values[1])
            self.age_at_incident = float(values[2])
            self.failure = values[3]
            self.suspension = values[4]
            self.cnd_nff = values[5]
            self.occ_fault = values[6]
            self.initial_installation = values[7]
            self.interval_censored = values[8]
            self.use_op_time = values[9]
            self.use_cal_time = values[10]
            self.ttf = float(values[11])
            self.mode_type = int(values[12])
            self.lstRelevant[0] = int(values[13])
            self.lstRelevant[1] = int(values[14])
            self.lstRelevant[2] = int(values[15])
            self.lstRelevant[3] = int(values[16])
            self.lstRelevant[4] = int(values[17])
            self.lstRelevant[5] = int(values[18])
            self.lstRelevant[6] = int(values[19])
            self.lstRelevant[7] = int(values[20])
            self.lstRelevant[8] = int(values[21])
            self.lstRelevant[9] = int(values[22])
            self.lstRelevant[10] = int(values[23])
            self.lstRelevant[11] = int(values[24])
            self.lstRelevant[12] = int(values[25])
            self.lstRelevant[13] = int(values[26])
            self.lstRelevant[14] = int(values[27])
            self.lstRelevant[15] = int(values[28])
            self.lstRelevant[16] = int(values[29])
            self.lstRelevant[17] = int(values[30])
            self.lstRelevant[18] = int(values[31])
            self.lstRelevant[19] = int(values[32])
            self.relevant = int(values[33])
            self.lstChargeable[0] = int(values[34])
            self.lstChargeable[1] = int(values[35])
            self.lstChargeable[2] = int(values[36])
            self.lstChargeable[3] = int(values[37])
            self.lstChargeable[4] = int(values[38])
            self.lstChargeable[5] = int(values[39])
            self.lstChargeable[6] = int(values[40])
            self.lstChargeable[7] = int(values[41])
            self.lstChargeable[8] = int(values[42])
            self.lstChargeable[9] = int(values[43])
            self.chargeable = int(values[44])
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Verificaiton data model attributes.

        :return: (incident_id, component_id, age_at_incident, failure,
                  suspension, cnd_nff, occ_fault, initial_installation,
                  interval_censored, use_op_time, use_cal_time, ttf, mode_type,
                  relevant, chargeable, lstRelevant, lstChargeable)
        :rtype: tuple
        """

        _values = (self.incident_id, self.component_id, self.age_at_incident,
                   self.failure, self.suspension, self.cnd_nff, self.occ_fault,
                   self.initial_installation, self.interval_censored,
                   self.use_op_time, self.use_cal_time, self.ttf,
                   self.mode_type, self.relevant, self.chargeable,
                   self.lstRelevant, self.lstChargeable)

        return _values


class Component(object):
    """
    The Incident Component data controller provides an interface between the
    Incident Component data model and an RTK view model.  A single Incident Component
    controller can manage one or more Incident Component data models.  The
    attributes of an Incident Component data controller are:

    :ivar _dao: the :class:`rtk.dao.DAO` to use when communicating with the RTK
                Project database.
    :ivar int _last_id: the last Incident Component ID used.
    :ivar dict dicComponents: Dictionary of the Incident Component data models
                           managed.  Key is the Component ID; value is a pointer
                           to the Incident Component data model instance.
    """

    def __init__(self):
        """
        Initializes a Incident Component data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicComponents = {}

    def request_components(self, dao, incident_id):
        """
        Method to read the RTK Project database and load the Incident
        components associated with the selected Revision.  For each Incident
        component returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create an Incident Component data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Incident Components being
           managed by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int incident_id: the Incident ID to select the updates for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self.dicComponents.clear()

        _query = "SELECT t1.fld_incident_id, t1.fld_component_id, \
                         t1.fld_age_at_incident, t1.fld_failure, \
                         t1.fld_suspension, t1.fld_cnd_nff, t1.fld_occ_fault, \
                         t1.fld_initial_installation, \
                         t1.fld_interval_censored, t1.fld_use_op_time, \
                         t1.fld_use_cal_time, t1.fld_ttf, t1.fld_mode_type, \
                         t1.fld_relevant_1, t1.fld_relevant_2, \
                         t1.fld_relevant_3, t1.fld_relevant_4, \
                         t1.fld_relevant_5, t1.fld_relevant_6, \
                         t1.fld_relevant_7, t1.fld_relevant_8, \
                         t1.fld_relevant_9, t1.fld_relevant_10, \
                         t1.fld_relevant_11, t1.fld_relevant_12, \
                         t1.fld_relevant_13, t1.fld_relevant_14, \
                         t1.fld_relevant_15, t1.fld_relevant_16, \
                         t1.fld_relevant_17, t1.fld_relevant_18, \
                         t1.fld_relevant_19, t1.fld_relevant_20, \
                         t1.fld_relevant, t1.fld_chargeable_1, \
                         t1.fld_chargeable_2, t1.fld_chargeable_3, \
                         t1.fld_chargeable_4, t1.fld_chargeable_5, \
                         t1.fld_chargeable_6, t1.fld_chargeable_7, \
                         t1.fld_chargeable_8, t1.fld_chargeable_9, \
                         t1.fld_chargeable_10, t1.fld_chargeable, \
                         t2.fld_part_number \
                  FROM rtk_incident_detail AS t1 \
                  INNER JOIN rtk_hardware AS t2 ON fld_hardware_id \
                  WHERE t2.fld_hardware_id=t1.fld_component_id \
                  AND t1.fld_incident_id={0:d}".format(incident_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_components = len(_results)
        except TypeError:
            _n_components = 0

        for i in range(_n_components):
            _component = Model()
            _component.set_attributes(_results[i])
            self.dicComponents[_results[i][1]] = _component

        return(_results, _error_code)

    def add_component(self, incident_id, component_id):
        """
        Adds a new Incident Component to the RTK Program's database.

        :param int incident_id: the Incident ID to add the new Component to.
        :param int n_components: the number of components to add to the
                                 Incident.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO rtk_incident_detail \
                  (fld_incident_id, fld_component_id) \
                  VALUES ({0:d}, {1:d})".format(incident_id, component_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new component was added successfully to the RTK Project
        # database:
        #   1. Create a new Incident Component model instance.
        #   2. Set the attributes of the new Incident Component model
        #      instance.
        #   3. Add the new Incident Component model to the controller
        #      dictionary.
        if _results:
            _component = Model()
            _component.incident_id = incident_id
            _component.component_id = component_id
            self.dicComponents[_component.component_id] = _component

        return(_results, _error_code)

    def delete_component(self, incident_id, component_id):
        """
        Deletes an Incident Component from the selected Incident.

        :param int incident_id: the ID of the incident to delete the
                                component from.
        :param int component_id: the ID of the component to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_incident_detail \
                  WHERE fld_incident_id={0:d} \
                  AND fld_component_id={1:d}".format(incident_id, component_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_components(self):
        """
        Saves all Incident Component data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _component in self.dicComponents.values():
            (_results, _error_code) = self.save_component(_component.component_id)

        return False

    def save_component(self, component_id):
        """
        Method to save the Incident Component model information to the open RTK
        Program database.

        :param int component_id: the ID of the Incident Component to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _component = self.dicComponents[component_id]

        _query = "UPDATE rtk_incident_detail \
                  SET fld_initial_installation={2:d}, fld_failure={3:d}, \
                      fld_suspension={4:d}, fld_occ_fault={5:d}, \
                      fld_cnd_nff={6:d}, fld_interval_censored={7:d}, \
                      fld_use_op_time={8:d}, fld_use_cal_time={9:d}, \
                      fld_ttf={10:f}, fld_mode_type={11:d}, \
                      fld_relevant_1={12:d}, fld_relevant_2={13:d}, \
                      fld_relevant_3={14:d}, fld_relevant_4={15:d}, \
                      fld_relevant_5={16:d}, fld_relevant_6={17:d}, \
                      fld_relevant_7={18:d}, fld_relevant_8={19:d}, \
                      fld_relevant_9={20:d}, fld_relevant_10={21:d}, \
                      fld_relevant_11={22:d}, fld_relevant_12={23:d}, \
                      fld_relevant_13={24:d}, fld_relevant_14={25:d}, \
                      fld_relevant_15={26:d}, fld_relevant_16={27:d}, \
                      fld_relevant_17={28:d}, fld_relevant_18={29:d}, \
                      fld_relevant_19={30:d}, fld_relevant_20={31:d}, \
                      fld_relevant={32:d}, fld_chargeable_1={33:d}, \
                      fld_chargeable_2={34:d}, fld_chargeable_3={35:d}, \
                      fld_chargeable_4={36:d}, fld_chargeable_5={37:d}, \
                      fld_chargeable_6={38:d}, fld_chargeable_7={39:d}, \
                      fld_chargeable_8={40:d}, fld_chargeable_9={41:d}, \
                      fld_chargeable_10={42:d}, fld_chargeable={43:d} \
                  WHERE fld_incident_id={0:d} \
                  AND fld_component_id={1:d}".format(
                      _component.incident_id, _component.component_id,
                      _component.initial_installation, _component.failure,
                      _component.suspension, _component.occ_fault,
                      _component.cnd_nff, _component.interval_censored,
                      _component.use_op_time, _component.use_cal_time,
                      _component.ttf, _component.mode_type,
                      _component.lstRelevant[0], _component.lstRelevant[1],
                      _component.lstRelevant[2], _component.lstRelevant[3],
                      _component.lstRelevant[4], _component.lstRelevant[5],
                      _component.lstRelevant[6], _component.lstRelevant[7],
                      _component.lstRelevant[8], _component.lstRelevant[9],
                      _component.lstRelevant[10], _component.lstRelevant[11],
                      _component.lstRelevant[12], _component.lstRelevant[13],
                      _component.lstRelevant[14], _component.lstRelevant[15],
                      _component.lstRelevant[16], _component.lstRelevant[17],
                      _component.lstRelevant[18], _component.lstRelevant[19],
                      _component.relevant, _component.lstChargeable[0],
                      _component.lstChargeable[1], _component.lstChargeable[2],
                      _component.lstChargeable[3], _component.lstChargeable[4],
                      _component.lstChargeable[5], _component.lstChargeable[6],
                      _component.lstChargeable[7], _component.lstChargeable[8],
                      _component.lstChargeable[9], _component.chargeable)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)
