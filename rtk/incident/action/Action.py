#!/usr/bin/env python
"""
#######################################
Incident Action Sub-Package Data Module
#######################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.incident.action.Action.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
#    may be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
    The Incident Action data model contains the attributes and methods for an
    Incident Action. The attributes of an Incident Action model are:

    :ivar incident_id: default value: None
    :ivar action_id: default value: None
    :ivar prescribed_action: default value: ''
    :ivar action_taken: default value: ''
    :ivar action_owner: default value: ''
    :ivar due_date: default value: 719163
    :ivar status: default value: 0
    :ivar approved_by: default value: ''
    :ivar approved_date: default value: 719163
    :ivar approved: default value: False
    :ivar closed_by: default value: ''
    :ivar closed_date: default value: 719163
    :ivar closed: default value: False
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
        self.incident_id = None
        self.action_id = None
        self.prescribed_action = ''
        self.action_taken = ''
        self.action_owner = 0
        self.due_date = 0
        self.status = 0
        self.approved_by = 0
        self.approved_date = 0
        self.approved = False
        self.closed_by = 0
        self.closed_date = 0
        self.closed = False


class Action(object):
    """
    The Incident Action data controller provides an interface between the
    Incident Action data model and an RTK view model.  A single Incident Action
    controller can manage one or more Incident Action data models.  The
    attributes of an Incident Action data controller are:

    :ivar _dao: the :class:`rtk.dao.DAO` to use when communicating with the RTK
                Project database.
    :ivar int _last_id: the last Incident Action ID used.
    :ivar dict dicActions: Dictionary of the Incident Action data models
                           managed.  Key is the Action ID; value is a pointer
                           to the Incident Action data model instance.
    """

    def __init__(self):
        """
        Initializes a Incident Action data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicActions = {}

    def request_actions(self, dao, incident_id):
        """
        Method to read the RTK Project database and load the Incident actions
        associated with the selected Revision.  For each Incident action
        returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create an Incident Action data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Incident Actions being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int incident_id: the Incident ID to select the updates for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self.dicActions.clear()

        _query = "SELECT * FROM rtk_incident_actions \
                  WHERE fld_incident_id={0:d}".format(incident_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_actions = len(_results)
        except TypeError:
            _n_actions = 0

        for i in range(_n_actions):
            _action = Model()
            _action.set_attributes(_results[i])
            self.dicActions[_results[i][1]] = _action

        return(_results, _error_code)

    def add_action(self, incident_id):
        """
        Adds a new Incident Action to the RTK Program's database.

        :param int incident_id: the Incident ID to add the new Action to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        from datetime import datetime

        _query = "INSERT INTO rtk_incident_actions \
                  (fld_incident_id) \
                  VALUES (%d)" % (incident_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new test was added successfully to the RTK Project database:
        #   1. Retrieve the ID of the newly inserted action.
        #   2. Set the due date to 30 days from current day.
        #   3. Create a new Incident Action model instance.
        #   4. Set the attributes of the new Incident Action model instance.
        #   5. Add the new Incident Action model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_incident_actions')[0]
            _due_date = datetime.today().toordinal() + 30

            _action = Model()
            _action.set_attributes((incident_id, self._last_id, '', '', 0,
                                    _due_date, 0, 0, 0, 0, 0, 0, 0))
            self.dicActions[_action.action_id] = _action

        return(_results, _error_code)

    def save_all_actions(self):
        """
        Saves all Incident Action data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _action in self.dicActions.values():
            (_results, _error_code) = self.save_action(_action.action_id)

        return False

    def save_action(self, action_id):
        """
        Method to save the Incident Action model information to the open RTK
        Program database.

        :param int action_id: the ID of the Incident Action to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _action = self.dicActions[action_id]

        _query = "UPDATE rtk_incident_actions \
                  SET fld_prescribed_action='{2:s}', \
                      fld_action_taken='{3:s}', fld_action_owner={4:d}, \
                      fld_due_date={5:d}, fld_status={6:d}, \
                      fld_approved_by={7:d}, fld_approved_date={8:d}, \
                      fld_approved={9:d}, fld_closed_by={10:d}, \
                      fld_closed_date={11:d}, fld_closed={12:d} \
                  WHERE fld_incident_id={0:d} \
                  AND fld_action_id={1:d}".format(
                      _action.incident_id, _action.action_id,
                      _action.prescribed_action, _action.action_taken,
                      _action.action_owner, _action.due_date, _action.status,
                      _action.approved_by, _action.approved_date,
                      _action.approved, _action.closed_by, _action.closed_date,
                      _action.closed)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)
