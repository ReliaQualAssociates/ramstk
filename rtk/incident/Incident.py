#!/usr/bin/env python
"""
############################
Incident Package Data Module
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.incident.Incident.py is part of The RTK Project
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
    The Incident data model contains the attributes and methods for an
    Incident. The attributes of an Incident model are:

    :ivar revision_id: default value: None
    :ivar incident_id: default value: None
    :ivar incident_category: default value: 0
    :ivar incident_type: default value: 0
    :ivar short_description: default value: ''
    :ivar detail_description: default value: ''
    :ivar criticality: default value: 0
    :ivar detection_method: default value: 0
    :ivar remarks: default value: ''
    :ivar status: default value: 0
    :ivar test: default value: ''
    :ivar test_case: default value: ''
    :ivar execution_time: default value: 0.0
    :ivar unit_id: default value: 0
    :ivar cost: default value: 0.0
    :ivar incident_age: default value: 0.0
    :ivar hardware_id: default value: 0
    :ivar software_id: default value: 0
    :ivar request_by: default value: ''
    :ivar request_date: default value: 0
    :ivar reviewed: default value: False
    :ivar review_by: default value: ''
    :ivar review_date: default value: 0
    :ivar approved: default value: False
    :ivar approve_by: default value: ''
    :ivar approve_date: default value: 0
    :ivar closed: default value: False
    :ivar close_by: default value: ''
    :ivar close_date: default value: 0
    :ivar life_cycle: default value: ''
    :ivar analysis: default value: ''
    :ivar accepted: default value: False
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

        # Initialize public scalar attributes.
        self.revision_id = None
        self.incident_id = None
        self.incident_category = 0
        self.incident_type = 0
        self.short_description = ''
        self.detail_description = ''
        self.criticality = 0
        self.detection_method = 0
        self.remarks = ''
        self.status = 0
        self.test = ''
        self.test_case = ''
        self.execution_time = 0.0
        self.unit_id = 0
        self.cost = 0.0
        self.incident_age = 0
        self.hardware_id = 0
        self.software_id = 0
        self.request_by = 0
        self.request_date = 0
        self.reviewed = False
        self.review_by = 0
        self.review_date = 0
        self.approved = False
        self.approve_by = 0
        self.approve_date = 0
        self.closed = False
        self.close_by = 0
        self.close_date = 0
        self.life_cycle = 0
        self.analysis = ''
        self.accepted = False

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
            self.revision_id = int(values[0])
            self.incident_id = int(values[1])
            self.incident_category = int(values[2])
            self.incident_type = int(values[3])
            self.short_description = str(values[4])
            self.detail_description = str(values[5])
            self.criticality = int(values[6])
            self.detection_method = int(values[7])
            self.remarks = str(values[8])
            self.status = int(values[9])
            self.test = str(values[10])
            self.test_case = str(values[11])
            self.execution_time = float(values[12])
            self.unit_id = int(values[13])
            self.cost = float(values[14])
            self.incident_age = int(values[15])
            self.hardware_id = int(values[16])
            self.software_id = int(values[17])
            self.request_by = int(values[18])
            self.request_date = int(values[19])
            self.reviewed = values[20]
            self.review_by = int(values[21])
            self.review_date = int(values[22])
            self.approved = values[23]
            self.approve_by = int(values[24])
            self.approve_date = int(values[25])
            self.closed = values[26]
            self.close_by = int(values[27])
            self.close_date = int(values[28])
            self.life_cycle = int(values[29])
            self.analysis = str(values[30])
            self.accepted = values[31]
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

        :return: (revision_id, incident_id, incident_category, incident_type,
                  short_description, detail_description, criticality,
                  detection_method, remarks, status, test, test_case,
                  execution_time, unit_id, cost, incident_age, hardware_id,
                  software_id, request_by, request_date, reviewed, review_by,
                  review_date, approved, approve_by, approve_date, closed,
                  close_by, close_date, life_cycle, analysis, accepted)
        :rtype: tuple
        """

        _values = (self.revision_id, self.incident_id, self.incident_category,
                   self.incident_type, self.short_description,
                   self.detail_description, self.criticality,
                   self.detection_method, self.remarks, self.status, self.test,
                   self.test_case, self.execution_time, self.unit_id,
                   self.cost, self.incident_age, self.hardware_id,
                   self.software_id, self.request_by, self.request_date,
                   self.reviewed, self.review_by, self.review_date,
                   self.approved, self.approve_by, self.approve_date,
                   self.closed, self.close_by, self.close_date,
                   self.life_cycle, self.analysis, self.accepted)

        return _values


class Incident(object):
    """
    The Incident data controller provides an interface between the Incident
    data model and an RTK view model.  A single Incident controller can
    manage one or more Incident data models.  The attributes of a
    Incident data controller are:

    :ivar _dao: the :class:`rtk.dao.DAO` to use when communicating with the RTK
                Project database.
    :ivar int _last_id: the last Incident ID used.
    :ivar dict dicIncidents: Dictionary of the Incident data models managed.
                             Key is the Incident ID; value is a pointer to the
                             Incident data model instance.
    """

    def __init__(self):
        """
        Initializes a Incident data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicIncidents = {}

    def request_incidents(self, dao, revision_id, load_all=False, query=None):
        """
        Method to read the RTK Project database and load all the Incidents
        associated with the selected Revision.  For each Incident returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Incident data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Incidents being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the tasks for.
        :param bool load_all: indicates whether or not to load incidents for
                              all revisions.
        :param str query: the query used to retrieve a filtered set of
                          incidents.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_incident')[0]

        if query is None:
            if not load_all:
                _query = "SELECT * FROM rtk_incident \
                          WHERE fld_revision_id={0:d}".format(revision_id)
            else:
                _query = "SELECT * FROM rtk_incident"
        else:
            _query = query
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_incidents = len(_results)
        except TypeError:
            _n_incidents = 0

        for i in range(_n_incidents):
            _incident = Model()
            _incident.set_attributes(_results[i])
            self.dicIncidents[_incident.incident_id] = _incident

        return(_results, _error_code)

    def add_incident(self, revision_id):
        """
        Adds a new Incident to the RTK Program's database.

        :param int revision_id: the Revision ID to add the new Incident to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        try:
            _short_description = "New Incident " + str(self._last_id + 1)
        except TypeError:                   # No tasks exist.
            _short_description = "New Incident 1"

        _query = "INSERT INTO rtk_incident \
                  (fld_revision_id, fld_short_description) \
                  VALUES (%d, '%s')" % (revision_id, _short_description)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new test was added successfully to the RTK Project database:
        #   1. Retrieve the ID of the newly inserted task.
        #   2. Create a new Incident model instance.
        #   4. Set the attributes of the new Incident model instance.
        #   5. Add the new Incident model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_incident')[0]

            _incident = Model()
            _incident.set_attributes((revision_id, self._last_id, 0, 0,
                                      _short_description, '', 0, 0, '', 0, '',
                                      '', 0.0, 0, 0.0, 0.0, 0, 0, 0, 719163,
                                      False, 0, 719163, False, 0, 719164,
                                      False, 0, 719163, '', '', False))
            self.dicIncidents[_incident.incident_id] = _incident

        return(_results, _error_code)

    def save_incident(self, incident_id):
        """
        Method to save the Incident model information to the open RTK Program
        database.

        :param int incident_id: the ID of the Incident task to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _incident = self.dicIncidents[incident_id]

        _query = "UPDATE rtk_incident \
                  SET fld_incident_category={2:d}, fld_incident_type={3:d}, \
                      fld_short_description='{4:s}', \
                      fld_long_description='{5:s}', fld_criticality={6:d}, \
                      fld_detection_method={7:d}, fld_remarks='{8:s}', \
                      fld_status={9:d}, fld_test_found='{10:s}', \
                      fld_test_case='{11:s}', fld_execution_time={12:f}, \
                      fld_unit={13:d}, fld_cost={14:f}, \
                      fld_incident_age={15:d}, fld_hardware_id={16:d}, \
                      fld_sftwr_id={17:d}, fld_request_by={18:d}, \
                      fld_request_date={19:d}, fld_reviewed={20:d}, \
                      fld_reviewed_by={21:d}, fld_reviewed_date={22:d}, \
                      fld_approved={23:d}, fld_approved_by={24:d}, \
                      fld_approved_date={25:d}, fld_complete={26:d}, \
                      fld_complete_by={27:d}, fld_complete_date={28:d}, \
                      fld_life_cycle={29:d}, fld_analysis='{30:s}', \
                      fld_accepted={31:d} \
                  WHERE fld_revision_id={0:d} \
                  AND fld_incident_id={1:d}".format(
                      _incident.revision_id, _incident.incident_id,
                      _incident.incident_category, _incident.incident_type,
                      _incident.short_description,
                      _incident.detail_description, _incident.criticality,
                      _incident.detection_method, _incident.remarks,
                      _incident.status, _incident.test, _incident.test_case,
                      _incident.execution_time, _incident.unit_id,
                      _incident.cost, _incident.incident_age,
                      _incident.hardware_id, _incident.software_id,
                      _incident.request_by, _incident.request_date,
                      _incident.reviewed, _incident.review_by,
                      _incident.review_date, _incident.approved,
                      _incident.approve_by, _incident.approve_date,
                      _incident.closed, _incident.close_by,
                      _incident.close_date, _incident.life_cycle,
                      _incident.analysis, _incident.accepted)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)
