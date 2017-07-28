#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.FMEA.py is part of The RTK Project
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

"""
===========
FMEA Module
===========
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
from Mode import Model as Mode
from Mechanism import Model as Mechanism
from Cause import Model as Cause
from Control import Model as Control
from Action import Model as Action

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class OutOfRangeError(Exception):
    """
    Exception raised when an input value is outside legal limits.
    """

    pass


class ParentError(Exception):
    """
    Exception raised when neither a hardware ID or function ID are passed or
    when both a hardware ID and function ID are passed when initializing an
    instance of the FMEA model.
    """

    pass


class Model(object):
    """
    The FMEA data model aggregates the Mode, Mechanism, Cause, Control and
    Action data models to produce an overall FMEA/FMECA.  A Function or
    Hardware item will consist of one FMEA.  The attributes of a FMEA are:

    :ivar dict dicModes: Dictionary of the Modes associated with the FMEA.  Key
                         is the Mode ID; value is a pointer to the instance of
                         the Mode data model.
    :ivar int assembly_id: the ID of the Hardware associated with the FMEA.
    :ivar int function_id: the ID of the Function associated with the FMEA.
    """

    def __init__(self, assembly_id, function_id):
        """
        Method to initialize a FMEA data model instance.

        :param int assembly_id: the Hardware item ID that the FMEA will be
                                associated with.
        :param int function_id: the Function ID that the FMEA will be
                                associated with.
        """

        # Model must be associated with either a Function or Hardware item.
        if assembly_id is None and function_id is None:
            raise ParentError

        # Model cannot be associated with both a Function and a Hardware item.
        if isinstance(assembly_id, int) and isinstance(function_id, int):
            raise ParentError

        # Define private dict attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dict attributes.
        self.dicModes = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.function_id = function_id
        self.assembly_id = assembly_id


class FMEA(object):
    """
    The FMEA data controller provides an interface between the FMEA data model
    and an RTK view model.  A single FMEA data controller can manage one or
    more FMEA data models.

    :ivar _dao: default value: None
    :ivar dict dicDFMEA: Dictionary of the Hardware FMEA data models
                         controlled.  Key is the Hardware ID; value is a
                         pointer to the instance of the FMEA data model.
    :ivar dict dicFFMEA: Dictionary of the Function FMEA data models
                         controlled.  Key is the Function ID; value is a
                         pointer to the instance of the FMEA data model.
    """

    def __init__(self):
        """
        Method to initialize a FMEA controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicDFMEA = {}
        self.dicFFMEA = {}
        self.dicMissions = {}
        self.dicPhases = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.dao = None

    def request_fmea(self, assembly_id=None, function_id=None,
                     revision_id=None):
        """
        Method to load the entire FMEA for a Function or Hardware item.
        Starting at the Mode level, the steps to create the FMEA are:

        #. Create an instance of the FMEA (Mode, Mechanism, Cause, Control,
           Action) data model.
        #. Add instance pointer to the FMEA dictionary for the passed
           Function or Hardware item.
        #. Retrieve the modes (mechanisms, causes, controls, actions) from the
           RTK Project database.
        #. Create an instance of the data model.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add instance pointer to the Mode (Mechanism, Cause, Control, Action)
           dictionary.

        :keyword int assembly_id: the Hardware item ID that the FMEA will be
                                  associated with.
        :keyword int assembly_id: the Function ID that the FMEA will be
                                  associated with.
        :keyword int revision_id: the Revision ID that the FMEA will be
                                  associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Controller must be associated with either a Function or Hardware
        # item.
        if assembly_id is None and function_id is None:
            raise ParentError

        # Controller cannot be associated with both a Function and a Hardware
        # item.
        if isinstance(assembly_id, int) and isinstance(function_id, int):
            raise ParentError

        _fmea = Model(assembly_id, function_id)
        if assembly_id is not None:
            self.dicDFMEA[assembly_id] = _fmea

            _query = "SELECT * FROM rtk_modes \
                      WHERE fld_hardware_id={0:d} \
                      AND fld_type=1 \
                      ORDER BY fld_mode_id ASC".format(assembly_id)
        elif function_id is not None:
            self.dicFFMEA[function_id] = _fmea

            _query = "SELECT * FROM rtk_modes \
                      WHERE fld_function_id={0:d} \
                      AND fld_type=0 \
                      ORDER BY fld_mode_id ASC".format(function_id)

        (_results, _error_code, __) = self.dao.execute(_query)
        try:
            _n_modes = len(_results)
        except TypeError:
            _n_modes = 0

        for i in range(_n_modes):
            _mode = Mode()
            _mode.set_attributes(_results[i])
            _fmea.dicModes[_mode.mode_id] = _mode

            self._request_mechanisms(_mode)

        if revision_id is not None:
            _query = "SELECT * FROM tbl_missions \
                      WHERE fld_revision_id={0:d} \
                      ORDER BY fld_mission_id".format(revision_id)
            (_results, _error_code, __) = self.dao.execute(_query)
            try:
                _n_missions = len(_results)
            except TypeError:
                _n_missions = 0

            for i in range(_n_missions):
                self.dicMissions[_results[i][0]] = _results[i][1:]

                _query = "SELECT * FROM tbl_mission_phase \
                          WHERE fld_revision_id={0:d} \
                          AND fld_mission_id={1:d} \
                          ORDER BY fld_phase_id".format(revision_id,
                                                        _results[i][1])
                (_phases, _error_code, __) = self.dao.execute(_query)
                try:
                    _n_phases = len(_phases)
                except TypeError:
                    _n_phases = 0
                for j in range(_n_phases):
                    self.dicPhases[_results[i][0]] = _phases

        return False

    def _request_mechanisms(self, mode):
        """
        Method to request the failure Mechanisms for a failure Mode.

        :param mode: the :py:class:`rtk.analyses.fmea.Mode.Mode` to retrieve the
                     failure Mechanisms for.
        """

        _query = "SELECT * FROM rtk_mechanisms \
                  WHERE fld_mode_id={0:d}".format(mode.mode_id)
        (_mechanisms,
         _error_code,
         __) = self.dao.execute(_query, commit=False)
        try:
            _n_mechanisms = len(_mechanisms)
        except TypeError:
            _n_mechanisms = 0
        for i in range(_n_mechanisms):
            _mechanism = Mechanism()
            _mechanism.set_attributes(_mechanisms[i][2:])
            mode.dicMechanisms[_mechanism.mechanism_id] = _mechanism

            self._request_causes(_mechanism)

        return False

    def _request_causes(self, mechanism):
        """
        Method to request the failure Causes for a failure Mechanism.

        :param mechanism: the :py:class:`rtk.analyses.fmea.Mechanism.Mechanism`
                          to retrieve the failure Causes for.
        """

        _query = "SELECT * FROM rtk_causes \
                  WHERE fld_mechanism_id={0:d}".format(mechanism.mechanism_id)
        (_causes, _error_code, __) = self.dao.execute(_query)
        try:
            _n_causes = len(_causes)
        except TypeError:
            _n_causes = 0

        for j in range(_n_causes):
            _cause = Cause()
            _cause.set_attributes(_causes[j])
            mechanism.dicCauses[_cause.cause_id] = _cause

            self._request_controls(_cause)
            self._request_actions(_cause)

        return False

    def _request_controls(self, cause):
        """
        Method to request the Controls for a failure Cause.

        :param cause: the :py:class:`rtk.analyses.fmea.Cause.Cause` to retrieve
                      the Controls for.
        """

        _query = "SELECT * FROM rtk_controls \
                   WHERE fld_cause_id={0:d}".format(cause.cause_id)
        (_controls, _error_code, __) = self.dao.execute(_query)
        try:
            _n_controls = len(_controls)
        except TypeError:
            _n_controls = 0

        for k in range(_n_controls):
            _control = Control()
            _control.set_attributes(_controls[k])
            cause.dicControls[_control.control_id] = _control

        return False

    def _request_actions(self, cause):
        """
        Method to request the Actions for a failure Cause.

        :param cause: the :py:class:`rtk.analyses.fmea.Cause.Cause` to retrieve
                      the Actions for.
        """

        _query = "SELECT * FROM rtk_actions \
                  WHERE fld_cause_id={0:d}".format(cause.cause_id)
        (_actions, _error_code, __) = self.dao.execute(_query)
        try:
            _n_actions = len(_actions)
        except TypeError:
            _n_actions = 0

        for k in range(_n_actions):
            _action = Action()
            _action.set_attributes(_actions[k])
            cause.dicActions[_action.action_id] = _action

        return False

    def add_fmea(self, assembly_id=None, function_id=None):
        """
        Method to add a new FMEA to the dictionary of profiles managed by this
        controller.

        :keyword int assembly_id: the Hardware item ID to add the FMEA.
        :keyword int function_id: the Function ID to add the FMEA.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.request_fmea(assembly_id, function_id)

        return False

    def add_mode(self, assembly_id=None, function_id=None):
        """
        Method to add a new Mode to the FMEA.

        :keyword int assembly_id: the Hardware item ID to add the FMEA.
        :keyword int function_id: the Function ID to add the FMEA.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        if assembly_id is not None:
            _query = "INSERT INTO rtk_modes \
                      (fld_hardware_id, fld_function_id, fld_type) \
                      VALUES ({0:d}, 0, 1)".format(assembly_id)
            _fmea = self.dicDFMEA[assembly_id]
            _a_id = assembly_id
            _f_id = 0

        elif function_id is not None:
            _query = "INSERT INTO rtk_modes \
                      (fld_hardware_id, fld_function_id, fld_type) \
                      VALUES (0, {0:d}, 0)".format(function_id)
            _fmea = self.dicFFMEA[function_id]
            _a_id = 0
            _f_id = function_id

        (_results,
         _error_code,
         _last_id) = self.dao.execute(_query, commit=True)

        _mode = Mode()
        _mode.set_attributes((_a_id, _f_id, _last_id, '', '', '', '', '', '',
                              '', '', '', '', '', '', 1.0, 0.0, 0.0, 0.0, 0.0,
                              10, 10, 0, 0, ''))
        _fmea.dicModes[_last_id] = _mode

        return(_results, _error_code, _last_id)

    def delete_mode(self, mode_id, assembly_id=None, function_id=None):
        """
        Method to delete a Mode from the FMEA.

        :param int mode_id: the Mode ID to delete
        :keyword int assembly_id: the Hardware item ID to delete from.
        :keyword int function_id: the Function ID to delete from.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        if assembly_id is not None:
            _query = "DELETE FROM rtk_modes \
                      WHERE fld_hardware_id={0:d} \
                      AND fld_mode_id={1:d}".format(assembly_id, mode_id)
            _fmea = self.dicDFMEA[assembly_id]

        elif function_id is not None:
            _query = "DELETE FROM rtk_modes \
                      WHERE fld_function_id={0:d} \
                      AND fld_mode_id={1:d}".format(function_id, mode_id)
            _fmea = self.dicFFMEA[function_id]

        (_results, _error_code, __) = self.dao.execute(_query, commit=True)
        try:
            _fmea.dicModes.pop(mode_id)
        except KeyError:
            _error_code = 60

        return(_results, _error_code)

    def add_mechanism(self, hardware_id, mode_id):
        """
        Method to add a new Mechanism to the selected Mode.

        :param int hardware_id: the Hardware ID to add the Mechanism.
        :param int mode_id: the Mode ID to add the Mechanism.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]

        _query = "INSERT INTO rtk_mechanisms \
                  (fld_assembly_id, fld_mode_id) \
                  VALUES ({0:d}, {1:d})".format(hardware_id, mode_id)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                              commit=True)

        _mechanism = Mechanism()
        _mechanism.set_attributes((mode_id, _last_id, '', 9, 9, 1000, 9, 9,
                                   1000, 0))
        _mode.dicMechanisms[_last_id] = _mechanism

        return(_results, _error_code, _last_id)

    def delete_mechanism(self, hardware_id, mode_id, mechanism_id):
        """
        Method to delete the selected Mechanism.

        :param int hardware_id: the Hardware ID of the Mechanism to delete.
        :param int mode_id: the Mode ID of the Mechanism to delete.
        :param int mechanism_id: the Mechanism ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]

        _query = "DELETE FROM rtk_mechanisms \
                  WHERE fld_mechanism_id={0:d}".format(mechanism_id)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                              commit=True)

        try:
            _mode.dicMechanisms.pop(mechanism_id)
        except KeyError:
            _error_code = 60

        return(_results, _error_code)

    def add_cause(self, hardware_id, mode_id, mechanism_id):
        """
        Method to add a new Cause to the selected Mechanism.

        :param int hardware_id: the Hardware ID to add the Cause.
        :param int mode_id: the Mode ID to add the Cause.
        :param int mechanism_id: the Mechanism ID to add the Cause.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]
        _mechanism = _mode.dicMechanisms[mechanism_id]

        _query = "INSERT INTO rtk_causes \
                  (fld_mode_id, fld_mechanism_id) \
                  VALUES ({0:d}, {1:d})".format(mode_id, mechanism_id)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                              commit=True)

        _cause = Cause()
        _cause.set_attributes((mode_id, mechanism_id, _last_id, '', 9, 9,
                               1000, 9, 9, 1000))
        _mechanism.dicCauses[_last_id] = _cause

        return(_results, _error_code, _last_id)

    def delete_cause(self, hardware_id, mode_id, mechanism_id, cause_id):
        """
        Method to delete the selected Cause.

        :param int hardware_id: the Hardware ID of the Cause to delete.
        :param int mode_id: the Mode ID of the Cause to delete.
        :param int mechanism_id: the Mechanism ID of the Cause to delete.
        :param int cause_id: the Cause ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]
        _mechanism = _mode.dicMechanisms[mechanism_id]

        _query = "DELETE FROM rtk_causes \
                  WHERE fld_cause_id={0:d}".format(cause_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        try:
            _mechanism.dicCauses.pop(cause_id)
        except KeyError:
            _error_code = 60

        return(_results, _error_code)

    def add_control(self, hardware_id, mode_id, mechanism_id, cause_id):
        """
        Method to add a new Control to the selected Mechanism or Cause.

        :param int hardware_id: the Hardware ID to add the Control.
        :param int mode_id: the Mode ID to add the Control.
        :param int mechanism_id: the Mechanism ID to add the Control.
        :param int cause_id: the Cause ID to add the Control.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]
        _mechanism = _mode.dicMechanisms[mechanism_id]
        _cause = _mechanism.dicCauses[cause_id]

        _query = "INSERT INTO rtk_controls \
                  (fld_mode_id, fld_mechanism_id, fld_cause_id) \
                  VALUES ({0:d}, {1:d}, {2:d})".format(mode_id, mechanism_id,
                                                       cause_id)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                              commit=True)

        _control = Control()
        _control.set_attributes((mode_id, mechanism_id, cause_id, _last_id, '',
                                 0))
        _cause.dicControls[_last_id] = _control

        return(_results, _error_code, _last_id)

    def delete_control(self, hardware_id, mode_id, mechanism_id, cause_id,
                       control_id):
        """
        Method to delete the selected Control.

        :param int hardware_id: the Hardware ID of the Cause to delete.
        :param int mode_id: the Mode ID of the Cause to delete.
        :param int mechanism_id: the Mechanism ID of the Cause to delete.
        :param int cause_id: the Cause ID to delete.
        :param int control_id: the Control ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]
        _mechanism = _mode.dicMechanisms[mechanism_id]
        _cause = _mechanism.dicCauses[cause_id]

        _query = "DELETE FROM rtk_controls \
                  WHERE fld_control_id={0:d}".format(control_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        try:
            _mechanism.dicControls.pop(control_id)
            _cause.dicControls.pop(control_id)
        except KeyError:
            _error_code = 60

        return(_results, _error_code)

    def add_action(self, hardware_id, mode_id, mechanism_id, cause_id):
        """
        Method to add a new Action to the selected Mechanism or Cause.

        :param int hardware_id: the Hardware ID to add the Control.
        :param int mode_id: the Mode ID to add the Control.
        :param int mechanism_id: the Mechanism ID to add the Control.
        :param int cause_id: the Cause ID to add the Control.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]
        _mechanism = _mode.dicMechanisms[mechanism_id]
        _cause = _mechanism.dicCauses[cause_id]

        _query = "INSERT INTO rtk_actions \
                  (fld_mode_id, fld_mechanism_id, fld_cause_id) \
                  VALUES ({0:d}, {1:d}, {2:d})".format(mode_id, mechanism_id,
                                                       cause_id)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                              commit=True)

        _action = Action()
        _action.set_attributes((mode_id, mechanism_id, cause_id, _last_id, '',
                                0, 0, 0, 0, '', 0, 0, 0, 0))
        _cause.dicActions[_last_id] = _action

        return(_results, _error_code, _last_id)

    def delete_action(self, hardware_id, mode_id, mechanism_id, cause_id,
                      action_id):
        """
        Method to delete the selected Action.

        :param int hardware_id: the Hardware ID of the Cause to delete.
        :param int mode_id: the Mode ID of the Cause to delete.
        :param int mechanism_id: the Mechanism ID of the Cause to delete.
        :param int cause_id: the Cause ID to delete.
        :param int action_id: the Action ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _fmea = self.dicDFMEA[hardware_id]
        _mode = _fmea.dicModes[mode_id]
        _mechanism = _mode.dicMechanisms[mechanism_id]
        _cause = _mechanism.dicCauses[cause_id]

        _query = "DELETE FROM rtk_actions \
                  WHERE fld_action_id={0:d}".format(action_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        try:
            _mechanism.dicActions.pop(action_id)
            _cause.dicActions.pop(action_id)
        except KeyError:
            _error_code = 60

        return(_results, _error_code)

    def copy_fmea(self, new_id, assembly_id=None, function_id=None):
        """
        Method to copy a FMEA from the currently selected Revision to a newly
        created Revision.

        :param int new_id: the ID of the new Hardware item or Function to copy
                           the FMEA information to.
        :keyword int assembly_id: the ID of Hardware item to copy the FMEA
                                  information from.
        :keyword int function_id: the ID of the Function to copy the FMEA
                                  information from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _new_fmea = Model(assembly_id, function_id)

        if assembly_id is not None:
            _fmea = self.dicDFMEA[assembly_id]
            self.dicDFMEA[new_id] = _new_fmea
            for _mode in _fmea.dicModes.values():
                self._copy_mode(_mode, new_id)
        elif function_id is not None:
            _fmea = self.dicFFMEA[function_id]
            self.dicFFMEA[new_id] = _new_fmea
            for _mode in _fmea.dicModes.values():
                self._copy_mode(_mode, new_id, function=True)

        return _return

    def _copy_mode(self, mode, new_id, function=False):
        """
        Method to copy a failure Mode from the currently selected Revision to a
        newly created Revsion.

        :param mode: the :py:class:`rtk.analyses.fmea.Mode.Model` to copy.
        :param int new_id: the ID of the new Hardware item or Function to copy
                           the Mode information to.
        :keyword bool function: indicates whether or not the mode is associated
                                with a Functional FMEA.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not function:
            _fmea = self.dicDFMEA[new_id]
            _assembly_id = new_id
            _function_id = 0
        else:
            _fmea = self.dicFFMEA[new_id]
            _assembly_id = 0
            _function_id = new_id

        _query = "INSERT INTO rtk_modes \
                  (fld_hardware_id, fld_function_id, fld_description, \
                   fld_mission, fld_mission_phase, fld_local_effect, \
                   fld_next_effect, fld_end_effect, fld_detection_method, \
                   fld_other_indications, fld_isolation_method, \
                   fld_design_provisions, fld_operator_actions, \
                   fld_severity_class, fld_hazard_rate_source, \
                   fld_mode_probability, fld_effect_probability, \
                   fld_mode_ratio, fld_mode_hazard_rate, fld_mode_op_time, \
                   fld_mode_criticality, fld_rpn_severity, \
                   fld_rpn_severity_new, fld_critical_item, fld_single_point, \
                   fld_remarks) \
                  VALUES ({0:d}, {1:d}, '{2:s}', '{3:s}', '{4:s}', '{5:s}', \
                          '{6:s}', '{7:s}', '{8:s}', '{9:s}', '{10:s}', \
                          '{11:s}', '{12:s}', '{13:s}', '{14:s}', '{15:s}', \
                          {16:f}, {17:f}, {18:g}, {19:f}, {20:g}, {21:d}, \
                          {22:d}, {23:d}, {24:d}, \
                          '{25:s}')".format(_assembly_id, _function_id,
                                            mode.description, mode.mission,
                                            mode.mission_phase,
                                            mode.local_effect, mode.next_effect,
                                            mode.end_effect,
                                            mode.detection_method,
                                            mode.other_indications,
                                            mode.isolation_method,
                                            mode.design_provisions,
                                            mode.operator_actions,
                                            mode.severity_class,
                                            mode.hazard_rate_source,
                                            mode.mode_probability,
                                            mode.effect_probability,
                                            mode.mode_ratio,
                                            mode.mode_hazard_rate,
                                            mode.mode_op_time,
                                            mode.mode_criticality,
                                            mode.rpn_severity,
                                            mode.rpn_severity_new,
                                            mode.critical_item,
                                            mode.single_point, mode.remarks)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                             commit=True)

        if _error_code == 0:
            _mode = Mode()
            _mode.set_attributes((_assembly_id, _function_id, _last_id, '', '',
                                  '', '', '', '', '', '', '', '', '', '', 1.0,
                                  0.0, 0.0, 0.0, 0.0, 10, 10, 0, 0, ''))
            _fmea.dicModes[_last_id] = _mode
            if not function:
                for _mechanism in mode.dicMechanisms.values():
                    self._copy_mechanism(_mode, _mechanism)
        else:
            _return = True

        return _return

    def _copy_mechanism(self, mode, mechanism):
        """
        Method to copy a failure Mechanism from the currently selected Revision
        to a newly created Revision.

        :param mode: the newly added :py:class:`rtk.analyses.fmea.Mode.Model`.
        :param mechanism: the :py:class:`rtk.analyses.fmea.Mechanism.Model` to
                          copy.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _query = "INSERT INTO rtk_mechanisms \
                  (fld_mode_id, fld_description, fld_rpn_occurrence, \
                   fld_rpn_detection, fld_rpn, fld_rpn_occurrence_new, \
                   fld_rpn_detection_new, fld_rpn_new, fld_include_pof) \
                  VALUES({0:d}, '{1:s}', {2:d}, {3:d}, {4:d}, {5:d}, {6:d}, \
                         {7:d}, {8:d})".format(mode.mode_id,
                                               mechanism.description,
                                               mechanism.rpn_occurrence,
                                               mechanism.rpn_detection,
                                               mechanism.rpn,
                                               mechanism.rpn_occurrence_new,
                                               mechanism.rpn_detection_new,
                                               mechanism.rpn_new,
                                               mechanism.include_pof)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                             commit=True)

        if _error_code == 0:
            _mechanism = Mechanism()
            _mechanism.set_attributes((mode.mode_id, _last_id, '', 9, 9, 1000,
                                       9, 9, 1000, 0))
            mode.dicMechanisms[_last_id] = _mechanism
            for _cause in mechanism.dicCauses.values():
                self._copy_cause(_mechanism, _cause, mode.mode_id)
        else:
            _return = True

        return _return

    def _copy_cause(self, mechanism, cause, mode_id):
        """
        Method to copy a failure Cause from the currently selected Revision to
        a newly created Revision.

        :param mechanism: the new :py:class:`rtk.analyses.fmea.Mechanism.Model`.
        :param cause: the :py:class:`rtk.analyses.fmea.Cause.Model` to copy.
        :param int mode_id: the failure Mode ID of the newly copied failure
                            Mode.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _query = "INSERT INTO rtk_causes \
                  (fld_mode_id, fld_mechanism_id, fld_description, \
                   fld_rpn_occurrence, fld_rpn_detection, fld_rpn, \
                   fld_rpn_occurrence_new, fld_rpn_detection_new, fld_rpn_new) \
                  VALUES({0:d}, {1:d}, '{2:s}', {3:d}, {4:d}, {5:d}, \
                         {6:d}, {7:d}, {8:d})".format(mode_id,
                                                      mechanism.mechanism_id,
                                                      cause.description,
                                                      cause.rpn_occurrence,
                                                      cause.rpn_detection,
                                                      cause.rpn,
                                                      cause.rpn_occurrence_new,
                                                      cause.rpn_detection_new,
                                                      cause.rpn_new)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                             commit=True)

        if _error_code == 0:
            _cause = Cause()
            _cause.set_attributes((mode_id, mechanism.mechanism_id, _last_id,
                                   '', 9, 9, 1000, 9, 9, 1000))
            mechanism.dicCauses[_last_id] = _cause
            for _control in cause.dicControls.values():
                self._copy_control(_cause, _control, mode_id,
                                   mechanism.mechanism_id)
        else:
            _return = True

        return _return

    def _copy_control(self, cause, control, mode_id, mechanism_id):
        """
        Method to copy a failure cause Control from the currently selected
        Revision to a newly created Revision.

        :param cause: the newly added :py:class:`rtk.analyses.fmea.Cause.Model`.
        :param control: the :py:class:`rtk.analyses.fmea.Control.Model` to
                        copy.
        :param int mode_id: the failure Mode ID of the newly copied failure
                            Mode.
        :param int mechanism_id: the failure Mechanism ID of the newly copied
                                 failure Mechanism.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _query = "INSERT INTO rtk_controls \
                  (fld_mode_id, fld_mechanism_id, fld_cause_id, \
                   fld_control_description, fld_control_type) \
                  VALUES({0:d}, {1:d}, {2:d}, '{3:s}', \
                         {4:d})".format(mode_id, mechanism_id, cause.cause_id,
                                        control.description,
                                        control.control_type)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                             commit=True)

        if _error_code == 0:
            _control = Control()
            _control.set_attributes((mode_id, mechanism_id, cause.cause_id,
                                     _last_id, '', 0))
            cause.dicControls[_last_id] = _control
        else:
            _return = True

        return _return

    def save_fmea(self, assembly_id=None, function_id=None):
        """
        Method to save the FMEA.  Wrapper for the _save_mode, _save_mechanism,
        _save_cause, _save_control, and _save_action methods.

        :keyword int assembly_id: the Hardware item ID of the FMEA to save.
        :keyword int function_id: the Function ID of the FMEA to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Controller must be associated with either a Function or Hardware
        # item.
        if assembly_id is None and function_id is None:
            raise ParentError

        # Controller cannot be associated with both a Function and a Hardware
        # item.
        if isinstance(assembly_id, int) and isinstance(function_id, int):
            raise ParentError

        if assembly_id is not None:
            _fmea = self.dicDFMEA[assembly_id]
        elif function_id is not None:
            _fmea = self.dicFFMEA[function_id]

        for _mode in _fmea.dicModes.values():
            self._save_mode(_mode)
            for _mechanism in _mode.dicMechanisms.values():
                self._save_mechanism(_mechanism)
                for _cause in _mechanism.dicCauses.values():
                    self._save_cause(_cause)
                    for _control in _cause.dicControls.values():
                        self._save_control(_control)
                    for _action in _cause.dicActions.values():
                        self._save_action(_action)

        return False

    def _save_mode(self, mode):
        """
        Method to save the Mode attributes to the RTK Project database.

        :param mode: the :py:class:`rtk.analyses.fmea.Mode.Model` to save.
        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_modes \
                  SET fld_description='{0:s}', fld_mission='{1:s}', \
                      fld_mission_phase='{2:s}', fld_local_effect='{3:s}', \
                      fld_next_effect='{4:s}', fld_end_effect='{5:s}', \
                      fld_detection_method='{6:s}', \
                      fld_other_indications='{7:s}', \
                      fld_isolation_method='{8:s}', \
                      fld_design_provisions='{9:s}', \
                      fld_operator_actions='{10:s}', \
                      fld_severity_class='{11:s}', \
                      fld_hazard_rate_source='{12:s}', \
                      fld_mode_probability='{13:s}', \
                      fld_effect_probability={14:f}, fld_mode_ratio={15:f}, \
                      fld_mode_hazard_rate={16:g}, fld_mode_op_time={17:f}, \
                      fld_mode_criticality={18:g}, fld_rpn_severity={19:d}, \
                      fld_rpn_severity_new={20:d}, fld_critical_item={21:d}, \
                      fld_single_point={22:d}, fld_remarks='{23:s}' \
                  WHERE fld_mode_id={26:d} \
                  AND fld_hardware_id={24:d} \
                  AND fld_function_id={25:d}".format(
                      mode.description, mode.mission, mode.mission_phase,
                      mode.local_effect, mode.next_effect, mode.end_effect,
                      mode.detection_method, mode.other_indications,
                      mode.isolation_method, mode.design_provisions,
                      mode.operator_actions, mode.severity_class,
                      mode.hazard_rate_source, mode.mode_probability,
                      mode.effect_probability, mode.mode_ratio,
                      mode.mode_hazard_rate, mode.mode_op_time,
                      mode.mode_criticality, mode.rpn_severity,
                      mode.rpn_severity_new, mode.critical_item,
                      mode.single_point, mode.remarks, mode.assembly_id,
                      mode.function_id, mode.mode_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def _save_mechanism(self, mechanism):
        """
        Method to save the Mechanism attributes to the RTK Project database.

        :param mechanism: the :py:class:`rtk.analyses.fmea.Mechanism.Model` to
                          save.
        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_mechanisms \
                  SET fld_description='{0:s}', fld_rpn_occurrence={1:d}, \
                      fld_rpn_detection={2:d}, fld_rpn={3:d}, \
                      fld_rpn_occurrence_new={4:d}, \
                      fld_rpn_detection_new={5:d}, fld_rpn_new={6:d}, \
                      fld_include_pof={7:d} \
                  WHERE fld_mechanism_id={8:d}".format(
                      mechanism.description, mechanism.rpn_occurrence,
                      mechanism.rpn_detection, mechanism.rpn,
                      mechanism.rpn_occurrence_new,
                      mechanism.rpn_detection_new, mechanism.rpn_new,
                      mechanism.include_pof, mechanism.mechanism_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def _save_cause(self, cause):
        """
        Method to save the Cause attributes to the RTK Project database.

        :param cause: the :py:class:`rtk.analyses.fmea.Cause.Model` to save.
        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_causes \
                  SET fld_description='{0:s}', \
                      fld_rpn_occurrence={1:d}, fld_rpn_detection={2:d}, \
                      fld_rpn={3:d}, fld_rpn_occurrence_new={4:d}, \
                      fld_rpn_detection_new={5:d}, fld_rpn_new={6:d} \
                  WHERE fld_cause_id={7:d}".format(
                      cause.description, cause.rpn_occurrence,
                      cause.rpn_detection, cause.rpn, cause.rpn_occurrence_new,
                      cause.rpn_detection_new, cause.rpn_new, cause.cause_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def _save_control(self, control):
        """
        Method to save the Control attributes to the RTK Project database.

        :param control: the :py:class:`rtk.analyses.fmea.Control.Model` to
                        save.
        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_controls \
                  SET fld_control_description='{0:s}', fld_control_type={1:d} \
                  WHERE fld_control_id={2:d}".format(control.description,
                                                     control.control_type,
                                                     control.control_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def _save_action(self, action):
        """
        Method to save the Action attributes to the RTK Project database.

        :param action: the :py:class:`rtk.analyses.fmea.Action.Model` to save.
        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_actions \
                  SET fld_action_recommended='{0:s}', \
                      fld_action_category={1:d}, \
                      fld_action_owner={2:d}, \
                      fld_action_due_date={3:d}, \
                      fld_action_status={4:d}, \
                      fld_action_taken='{5:s}', \
                      fld_action_approved={6:d}, \
                      fld_action_approve_date={7:d}, \
                      fld_action_closed={8:d}, \
                      fld_action_close_date={9:d} \
                  WHERE fld_action_id={10:d}".format(
                      action.action_recommended, action.action_category,
                      action.action_owner, action.action_due_date,
                      action.action_status, action.action_taken,
                      action.action_approved, action.action_approved_date,
                      action.action_closed, action.action_closed_date,
                      action.action_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code
