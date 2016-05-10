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
<<<<<<< HEAD
    import Utilities as _util
except ImportError:
    import rtk.Utilities as _util
=======
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
=======
    :ivar int relevant :default value: False
    :ivar int chargeable :default value: False
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self):
        """
<<<<<<< HEAD
        Method to initialize a Incident data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
=======
        Method to initialize an Incident data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.
        self.lstRelevant = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                            -1, -1, -1, -1, -1, -1, -1]
        self.lstChargeable = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        # Define public scalar attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
        self.unit_id = 0
=======
        self.unit_id = ''
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
=======
        self.relevant = -1
        self.chargeable = -1
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
            self.unit_id = int(values[13])
=======
            self.unit_id = str(values[13])
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _util.error_handler(_err.args)
=======
            self.lstRelevant[0] = int(values[32])
            self.lstRelevant[1] = int(values[33])
            self.lstRelevant[2] = int(values[34])
            self.lstRelevant[3] = int(values[35])
            self.lstRelevant[4] = int(values[36])
            self.lstRelevant[5] = int(values[37])
            self.lstRelevant[6] = int(values[38])
            self.lstRelevant[7] = int(values[39])
            self.lstRelevant[8] = int(values[40])
            self.lstRelevant[9] = int(values[41])
            self.lstRelevant[10] = int(values[42])
            self.lstRelevant[11] = int(values[43])
            self.lstRelevant[12] = int(values[44])
            self.lstRelevant[13] = int(values[45])
            self.lstRelevant[14] = int(values[46])
            self.lstRelevant[15] = int(values[47])
            self.lstRelevant[16] = int(values[48])
            self.lstRelevant[17] = int(values[49])
            self.lstRelevant[18] = int(values[50])
            self.lstRelevant[19] = int(values[51])
            self.relevant = int(values[52])
            self.lstChargeable[0] = int(values[53])
            self.lstChargeable[1] = int(values[54])
            self.lstChargeable[2] = int(values[55])
            self.lstChargeable[3] = int(values[56])
            self.lstChargeable[4] = int(values[57])
            self.lstChargeable[5] = int(values[58])
            self.lstChargeable[6] = int(values[59])
            self.lstChargeable[7] = int(values[60])
            self.lstChargeable[8] = int(values[61])
            self.lstChargeable[9] = int(values[62])
            self.chargeable = int(values[63])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
<<<<<<< HEAD
        Retrieves the current values of the Verificaiton data model attributes.
=======
        Method to retrieve the current values of the Incident data model
        attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: (revision_id, incident_id, incident_category, incident_type,
                  short_description, detail_description, criticality,
                  detection_method, remarks, status, test, test_case,
                  execution_time, unit_id, cost, incident_age, hardware_id,
                  software_id, request_by, request_date, reviewed, review_by,
                  review_date, approved, approve_by, approve_date, closed,
<<<<<<< HEAD
                  close_by, close_date, life_cycle, analysis, accepted)
=======
                  close_by, close_date, life_cycle, analysis, accepted,
                  relevant, chargeable, lstRelevant, lstChargeable)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
                   self.life_cycle, self.analysis, self.accepted)
=======
                   self.life_cycle, self.analysis, self.accepted,
                   self.relevant, self.chargeable, self.lstRelevant,
                   self.lstChargeable)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
        Initializes a Incident data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicIncidents = {}

=======
        Method to initialize an Incident data controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._dao = None
        self._last_id = None

        # Define public dictionary attributes.
        self.dicIncidents = {}

        # Define public list attributes.

        # Define public scalar attributes.

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
        Adds a new Incident to the RTK Program's database.
=======
        Method to add a new Incident to the RTK Program's database.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
                      fld_unit={13:d}, fld_cost={14:f}, \
=======
                      fld_unit='{13:s}', fld_cost={14:f}, \
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
                      fld_incident_age={15:d}, fld_hardware_id={16:d}, \
                      fld_sftwr_id={17:d}, fld_request_by={18:d}, \
                      fld_request_date={19:d}, fld_reviewed={20:d}, \
                      fld_reviewed_by={21:d}, fld_reviewed_date={22:d}, \
                      fld_approved={23:d}, fld_approved_by={24:d}, \
                      fld_approved_date={25:d}, fld_complete={26:d}, \
                      fld_complete_by={27:d}, fld_complete_date={28:d}, \
                      fld_life_cycle={29:d}, fld_analysis='{30:s}', \
<<<<<<< HEAD
                      fld_accepted={31:d} \
=======
                      fld_accepted={31:d}, fld_relevant_1={32:d}, \
                      fld_relevant_2={33:d}, fld_relevant_3={34:d}, \
                      fld_relevant_4={35:d}, fld_relevant_5={36:d}, \
                      fld_relevant_6={37:d}, fld_relevant_7={38:d}, \
                      fld_relevant_8={39:d}, fld_relevant_9={40:d}, \
                      fld_relevant_10={41:d}, fld_relevant_11={42:d}, \
                      fld_relevant_12={43:d}, fld_relevant_13={44:d}, \
                      fld_relevant_14={45:d}, fld_relevant_15={46:d}, \
                      fld_relevant_16={47:d}, fld_relevant_17={48:d}, \
                      fld_relevant_18={49:d}, fld_relevant_19={50:d}, \
                      fld_relevant_20={51:d}, fld_relevant={52:d}, \
                      fld_chargeable_1={53:d}, fld_chargeable_2={54:d}, \
                      fld_chargeable_3={55:d}, fld_chargeable_4={56:d}, \
                      fld_chargeable_5={57:d}, fld_chargeable_6={58:d}, \
                      fld_chargeable_7={59:d}, fld_chargeable_8={60:d}, \
                      fld_chargeable_9={61:d}, fld_chargeable_10={62:d}, \
                      fld_chargeable={63:d} \
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
                      _incident.analysis, _incident.accepted)
=======
                      _incident.analysis, _incident.accepted,
                      _incident.lstRelevant[0], _incident.lstRelevant[1],
                      _incident.lstRelevant[2], _incident.lstRelevant[3],
                      _incident.lstRelevant[4], _incident.lstRelevant[5],
                      _incident.lstRelevant[6], _incident.lstRelevant[7],
                      _incident.lstRelevant[8], _incident.lstRelevant[9],
                      _incident.lstRelevant[10], _incident.lstRelevant[11],
                      _incident.lstRelevant[12], _incident.lstRelevant[13],
                      _incident.lstRelevant[14], _incident.lstRelevant[15],
                      _incident.lstRelevant[16], _incident.lstRelevant[17],
                      _incident.lstRelevant[18], _incident.lstRelevant[19],
                      _incident.relevant, _incident.lstChargeable[0],
                      _incident.lstChargeable[1], _incident.lstChargeable[2],
                      _incident.lstChargeable[3], _incident.lstChargeable[4],
                      _incident.lstChargeable[5], _incident.lstChargeable[6],
                      _incident.lstChargeable[7], _incident.lstChargeable[8],
                      _incident.lstChargeable[9], _incident.chargeable)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)
