#!/usr/bin/env python
"""
===========
FMEA Module
===========
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       FMEA.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
from Mode import Model as Mode
from Mechanism import Model as Mechanism
from Cause import Model as Cause
from Control import Model as Control
from Action import Model as Action

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    elif 'invalid literal' in message[0]:   # Value error
        _error_code = 50
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class OutOfRangeError(Exception): pass


class ParentError(Exception): pass


class Model(object):
    """
    The FMEA data model aggregates the Mode, Mechanism, Cause, Control and
    Action data models to produce an overall FMEA/FMECA.  A Function or
    Hardware item will consist of one FMEA.  The attributes of a FMEA are:

    :ivar dicModes: Dictionary of the Modes associated with the FMEA.  Key is
    the Mode ID; value is a pointer to the instance of the Mode data model.

    :ivar assembly_id: default value: None
    :ivar function_id: default value: None
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

        # Set public dict attribute default values.
        self.dicModes = {}

        # Set public scalar attribute default values.

    def calculate(self, severity, occurrence, detection):
        """
        Calculate the Risk Priority Number (RPN) for the FMEA.

            RPN = S * O * D

        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this FMEA is associated
                             with.
        :param int occurrence: the Occurrence (O) value of the FMEA.
        :param int detection: the Detection (D) value of the FMEA.
        :return: _rpn
        :rtype: int
        """

        if not 0 < severity < 11:
            raise OutOfRangeError
        if not 0 < occurrence < 11:
            raise OutOfRangeError
        if not 0 < detection < 11:
            raise OutOfRangeError

        _rpn = int(severity) * int(occurrence) * int(detection)

        if not 0 < _rpn < 1001:
            raise OutOfRangeError

        return _rpn


class FMEA(object):
    """
    The FMEA data controller provides an interface between the FMEA data model
    and an RTK view model.  A single FMEA data controller can manage one or
    more FMEA data models.

    :ivar _dao: default value: None
    :ivar dicDFMEA: Dictionary of the Hardware FMEA data models controlled.  Key is the Assembly ID; value is a pointer to the instance of the FMEA data model.
    :ivar dicFFMEA: Dictionary of the Function FMEA data models controlled.  Key is the Function ID; value is a pointer to the instance of the FMEA data model.
    """

    def __init__(self):
        """
        Initializes a FMEA controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None

        # Initialize public dictionary attributes.
        self.dicDFMEA = {}
        self.dicFFMEA = {}

    def request_fmea(self, dao, assembly_id=None, function_id=None):
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

        :param `rtk.DAO` dao: the Data Access object to use for communicating
                              with the RTK Project database.
        :keyword int assembly_id: the Hardware item ID that the FMEA will be
                                  associated with.
        :keyword int assembly_id: the Function ID that the FMEA will be
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

        self._dao = dao

        _fmea = Model(assembly_id, function_id)
        if assembly_id is not None:
            self.dicDFMEA[assembly_id] = _fmea

            _query = "SELECT * FROM tbl_modes \
                      WHERE fld_assembly_id={0:d} \
                      ORDER BY fld_mode_id ASC".format(assembly_id)
        elif function_id is not None:
            self.dicFFMEA[function_id] = _fmea

            _query = "SELECT * FROM tbl_modes \
                      WHERE fld_function_id={0:d} \
                      ORDER BY fld_mode_id ASC".format(function_id)

        (_results, _error_code, __) = self._dao.execute(_query)
        try:
            _n_modes = len(_results)
        except TypeError:
            _n_modes = 0

        for i in range(_n_modes):
            _mode = Mode()
            _mode.set_attributes(_results[i])
            _fmea.dicModes[_mode.mode_id] = _mode

            _query = "SELECT * FROM tbl_mechanisms \
                      WHERE fld_mode_id={0:d}".format(_mode.mode_id)
            (_mechanisms,
             _error_code,
             __) = self._dao.execute(_query, commit=False)
            try:
                _n_mechanisms = len(_mechanisms)
            except TypeError:
                _n_mechanisms = 0

            for i in range(_n_mechanisms):
                _mechanism = Mechanism()
                _mechanism.set_attributes(_mechanisms[i])
                _mode.dicMechanisms[_mechanism.mechanism_id] = _mechanism

                _query = "SELECT * FROM tbl_causes \
                          WHERE fld_mechanism_id={0:d}".format(
                              _mechanism.mechanism_id)
                (_causes, _error_code, __) = self._dao.execute(_query)
                try:
                    _n_causes = len(_causes)
                except TypeError:
                    _n_causes = 0

                for i in range(_n_causes):
                    _cause = Cause()
                    _cause.set_attributes(_causes[i])
                    _mechanism.dicCauses[_cause.cause_id] = _cause

        return False

    def add_fmea(self, assembly_id=None, function_id=None):
        """
        Adds a new FMEA to the dictionary of profiles managed by this
        controller.

        :keyword int assembly_id: the Hardware item ID to add the FMEA.
        :keyword int function_id: the Function ID to add the FMEA.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.request_fmea(self._dao, assembly_id, function_id)

        return False

    def add_mode(self, assembly_id=None, function_id=None):
        """
        Adds a new Mode to the FMEA.

        :keyword int assembly_id: the Hardware item ID to add the FMEA.
        :keyword int function_id: the Function ID to add the FMEA.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        if assembly_id is not None:
            _query = "INSERT INTO tbl_modes \
                      (fld_assembly_id, fld_function_id) \
                      VALUES ({0:d}, -1)".format(assembly_id)
            _fmea = self.dicDFMEA[assembly_id]
            _a_id = assembly_id
            _f_id = -1

        elif function_id is not None:
            _query = "INSERT INTO tbl_modes \
                      (fld_assembly_id, fld_function_id) \
                      VALUES (-1, {0:d})".format(function_id)
            _fmea = self.dicFFMEA[function_id]
            _a_id = -1
            _f_id = function_id

        (_results,
         _error_code,
         _last_id) = self._dao.execute(_query, commit=True)

        _mode = Mode()
        _mode.set_attributes((_a_id, _f_id, _last_id, '', '', '', '', '', '',
                              '', '', '', '', '', '', 1.0, 0.0, 0.0, 0.0, 0.0,
                              10, 10, 0, 0, ''))
        _fmea.dicModes[_last_id] = _mode

        return(_results, _error_code, _last_id)

    def delete_mode(self, mode_id, assembly_id=None, function_id=None):
        """
        Deletes a Mode from the FMEA.

        :param int mode_id: the Mode ID to delete
        :keyword int assembly_id: the Hardware item ID to delete from.
        :keyword int function_id: the Function ID to delete from.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        if assembly_id is not None:
            _query = "DELETE FROM tbl_modes \
                      WHERE fld_assembly_id={0:d} \
                      AND fld_mode_id={1:d}".format(assembly_id, mode_id)
            _fmea = self.dicDFMEA[assembly_id]

        elif function_id is not None:
            _query = "DELETE FROM tbl_modes \
                      WHERE fld_function_id={0:d} \
                      AND fld_mode_id={1:d}".format(function_id, mode_id)
            _fmea = self.dicFFMEA[function_id]

        (_results, _error_code, __) = self._dao.execute(_query, commit=True)
        try:
            _fmea.dicModes.pop(mode_id)
        except KeyError as _err:
            _error_code = 60

        return(_results, _error_code)

    def add_mechanism(self):

        pass

    def delete_mechanism(self):

        pass

    def add_cause(self):

        pass

    def delete_cause(self):

        pass

    def add_control(self):

        pass

    def delete_control(self):

        pass

    def add_action(self):

        pass

    def delete_action(self):

        pass

    def save_fmea(self, assembly_id=None, function_id=None):
        """
        Saves the FMEA.  Wrapper for the _save_mode, _save_mechanism,
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

        return False

    def _save_mode(self, mode):
        """
        Saves the Mode attributes to the RTK Project database.

        :param rtk.fmea.Mode.Model: the Mode data model to save.
        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE tbl_modes \
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
                      fld_mode_hazard_rate={16:f}, fld_mode_op_time={17:f}, \
                      fld_mode_criticality={18:f}, fld_rpn_severity={19:d}, \
                      fld_rpn_severity_new={20:d}, fld_critical_item={21:d}, \
                      fld_single_point={22:d}, fld_remarks='{23:s}', \
                      fld_assembly_id={24:d}, fld_function_id={25:d} \
                  WHERE fld_mode_id={26:d}".format(
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
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return _error_code

    def _save_mechanism(self, mechanism):

        pass

    def _save_cause(self, cause):

        pass

    def _save_control(self, control):

        pass

    def _save_action(self, action):

        pass
