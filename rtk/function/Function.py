#!/usr/bin/env python
"""
############################
Function Package Data Module
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Function.py is part of The RTK Project
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
    elif 'division by zero' in message[0]:  # Zero division error
        _error_code = 20
    elif 'referenced before assignment' in message[0]:  # Unbound local error
        _error_code = 30
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Model(object):
    """
    The Function data model contains the attributes and methods of a function.
    A :class:`rtk.revision.Revision` will consist of one or more Functions.
    The attributes of a Function are:

    :ivar revision_id: default value: 0
    :ivar function_id: default value: 0
    :ivar availability: default value: 1.0
    :ivar mission_availability: default value: 1.0
    :ivar code: default value: ''
    :ivar cost: default value: 0.0
    :ivar mission_hazard_rate: default value: 0.0
    :ivar hazard_rate: default value: 0.0
    :ivar mmt: default value: 0.0
    :ivar mcmt: default value: 0.0
    :ivar mpmt: default value: 0.0
    :ivar mission_mtbf: default value: 0.0
    :ivar mtbf: default value: 0.0
    :ivar mttr: default value: 0.0
    :ivar name: default value: ''
    :ivar remarks: default value: ''
    :ivar n_modes: default value: 0
    :ivar n_parts: default value: 0
    :ivar type: default value: 0
    :ivar parent_id: default value: -1
    :ivar level: default value: 0
    :ivar safety_critical: default value: 1
    """

    def __init__(self):
        """
        Method to initialize a Function data model instance.
        """

        # Define public Function class attributes.
        self.revision_id = 0
        self.function_id = 0
        self.availability = 1.0
        self.mission_availability = 1.0
        self.code = ''
        self.cost = 0.0
        self.mission_hazard_rate = 0.0
        self.hazard_rate = 0.0
        self.mmt = 0.0
        self.mcmt = 0.0
        self.mpmt = 0.0
        self.mission_mtbf = 0.0
        self.mtbf = 0.0
        self.mttr = 0.0
        self.name = ''
        self.remarks = ''
        self.n_modes = 0
        self.n_parts = 0
        self.type = 0
        self.parent_id = -1
        self.level = 0
        self.safety_critical = 1

    def set_attributes(self, values):
        """
        Method to set the Function data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.function_id = int(values[1])
            self.availability = float(values[2])
            self.mission_availability = float(values[3])
            self.code = str(values[4])
            self.cost = float(values[5])
            self.mission_hazard_rate = float(values[6])
            self.hazard_rate = float(values[7])
            self.mmt = float(values[8])
            self.mcmt = float(values[9])
            self.mpmt = float(values[10])
            self.mission_mtbf = float(values[11])
            self.mtbf = float(values[12])
            self.mttr = float(values[13])
            self.name = str(values[14])
            self.remarks = str(values[15])
            self.n_modes = int(values[16])
            self.n_parts = int(values[17])
            self.type = int(values[18])
            self.parent_id = int(values[19])
            self.level = int(values[20])
            self.safety_critical = int(values[21])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Function data model
        attributes.

        :return: (self.revision_id, self.function_id, self.availability,
                  self.mission_availability, self.code, self.cost,
                  self.mission_hazard_rate, self.hazard_rate, self.mmt,
                  self.mcmt, self.mpmt, self.mission_mtbf, self.mtbf,
                  self.mttr, self.name, self.remarks, self.n_modes,
                  self.n_parts, self.type, self.parent_id, self.level,
                  self.safety_critical)
        :rtype: tuple
        """

        _values = (self.revision_id, self.function_id, self.availability,
                   self.mission_availability, self.code, self.cost,
                   self.mission_hazard_rate, self.hazard_rate, self.mmt,
                   self.mcmt, self.mpmt, self.mission_mtbf, self.mtbf,
                   self.mttr, self.name, self.remarks, self.n_modes,
                   self.n_parts, self.type, self.parent_id, self.level,
                   self.safety_critical)

        return _values

    def calculate_reliability(self, inputs):
        """
        Method to calculate the logistics hazard rate, mission hazard rate,
        logistics MTBF, and mission MTBF.

        :param tuple inputs: tuple containing the input data for the
                             reliability calculations.  The tuple must be in
                             order:

                                #. Logistics Failure Rate
                                #. Mission Failure Rate
                                #. Number of parts

        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.hazard_rate = float(inputs[0])
            self.mission_hazard_rate = float(inputs[1])
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to float."
        else:
            # Calculate the logistics and mission MTBF.
            try:
                self.mtbf = 1.0 / self.hazard_rate
                self.mission_mtbf = 1.0 / self.mission_hazard_rate
            except ZeroDivisionError as _err:
                _code = _error_handler(_err.args)
                _msg = "ERROR: Calculating logistics or mission MTBF."

        return(_code, _msg)

    def calculate_availability(self, inputs):
        """
        Method to calculate the MPMT, MCMT, MTTR, MMT, logistics availability,
        and mission availability.

        :param tuple inputs: tuple containing the input data for the
                             availability calculations.  The tuple must be in
                             order:

                                #. Mean Preventive Maintenance Time (MPMT)
                                #. Mean Corrective Maintenance Time (MCMT)
                                #. Mean Time to Repair (MTTR)
                                #. Mean Maintenance Time (MMT)

        :revision rtk.revision.Revision.Model: the Revision data model to
                                               calculate costs.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.mpmt = float(inputs[0])
            self.mcmt = float(inputs[1])
            self.mttr = float(inputs[2])
            self.mmt = float(inputs[3])
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "FAIL: Convert one or more inputs to float."
        else:
            # Calculate logistics and mission availability.
            try:
                self.availability = self.mtbf / (self.mtbf + self.mttr)
                self.mission_availability = self.mission_mtbf / \
                    (self.mission_mtbf + self.mttr)
            except ZeroDivisionError as _err:
                _code = _error_handler(_err.args)
                _msg = "FAIL: Calculate logistics or mission availability."

        return(_code, _msg)

    def calculate_costs(self, inputs, mission_time):
        """
        Method to calculate the total cost, cost per failure, and cost per
        operating hour.

        :revision tuple inputs: tuple containing the input data for the cost
                                calculations.  The tuple must be in order:

                                #. Cost

        :param float mission_time: the time over which to calculate costs.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.cost = float(inputs)
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "FAIL: Convert one or more inputs to float."
        else:
            # Calculate costs.
            _cost_per_failure = self.cost * self.hazard_rate
            try:
                _cost_per_hour = self.cost / mission_time
            except ZeroDivisionError as _err:
                _code = _error_handler(_err.args)
                _msg = "FAIL: Calculate cost per failure or cost per hour."

        return(_code, _msg)


class Function(object):
    """
    The Function data controller provides an interface between the Function
    data model and an RTK view model.  A single Function controller can manage
    one or more Function data models.  The attributes of a Function data
    controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
    Project database.
    :ivar _last_id: the last Function ID used.
    :ivar dicFunctions: Dictionary of the Function data models controlled.  Key is the Function ID; value is a pointer to the Function data model instance.
    """

    def __init__(self):
        """
        Initializes a Function data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicFunctions = {}

    def request_functions(self, dao):
        """
        Reads the RTK Project database and loads all the functions associated
        with the selected Revision.  For each function returned:

        #. Retrieve the functions from the RTK Project database.
        #. Create a Function data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Functions being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the functions for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('tbl_functions')[0]

        # Select everything from the function table.
        _query = "SELECT * FROM tbl_functions \
                  ORDER BY fld_parent_id"
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_functions = len(_results)
        except TypeError as _err:
            _n_functions = 0

        for i in range(_n_functions):
            _function = Model()
            _function.set_attributes(_results[i])
            self.dicFunctions[_function.function_id] = _function

        return(_results, _error_code)

    def add_function(self, revision_id, parent_id=None, code=None, name=None,
                     remarks=''):
        """
        Adds a new Function to the RTK Project for the selected Revision.

        :param int revision_id: the Revision ID to add the new Function(s).
        :keyword int parent_id: the Function ID of the parent function.
        :keyword str code: the code to use for the new Function.
        :keyword str name: the name of the new Function.
        :keyword str remarks: any remarks associated with the new Function.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # By default we add the new function as a top-level function.
        if parent_id is None:
            parent_id = -1

        if code is None:
            code = '{0} {1}'.format(str(_conf.RTK_PREFIX[2]),
                                    str(_conf.RTK_PREFIX[3]))

            # Increment the revision index.
            _conf.RTK_PREFIX[3] += 1

        if name is None:
            name = 'New Function'

        _query = "INSERT INTO tbl_functions \
                  (fld_revision_id, fld_name, fld_remarks, fld_code, \
                   fld_parent_id) \
                  VALUES ({0:d}, '{1:s}', '{2:s}', '{3:s}', {4:d})".format(
                      revision_id, name, remarks, code, parent_id)
        (_results,
         _error_code,
         _function_id) = self._dao.execute(_query, commit=True)

        # If the new function was added successfully to the RTK Project
        # database:
        #   1. Retrieve the ID of the newly inserted function.
        #   2. Create a new Function model instance.
        #   3. Set the attributes of the new Function model instance.
        #   2. Add the new Function model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('tbl_functions')[0]
            _function = Model()
            _function.set_attributes((revision_id, self._last_id, 1.0, 1.0,
                                      code, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, name, remarks, 0, 0, 0,
                                      parent_id, 0, 1))
            self.dicFunctions[_function.function_id] = _function

        return(_function, _error_code)

    def delete_function(self, function_id):
        """
        Deletes a Function from the RTK Project.

        :param int function_id: the Function ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Delete all the child functions, if any.
        _query = "DELETE FROM tbl_functions \
                  WHERE fld_parent_id={0:d}".format(function_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Then delete the parent function.
        _query = "DELETE FROM tbl_functions \
                  WHERE fld_function_id={0:d}".format(function_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        self.dicFunctions.pop(function_id)

        return(_results, _error_code)

    def calculate_function(self, function_id, mission_time, hr_multiplier=1.0):
        """
        Calculates reliability, availability, and cost information for a
        Function.

        :param int function_id: the Function ID to calculate.
        :param float mission_time: the time to use in the calculations.
        :keyword float hr_multiplier: the multiplier to use for the hazard rate
                                      calculations.
        :return: _error_code
        :rtype: int
        """

        _function = self.dicFunctions[function_id]

        _query = "SELECT SUM(t2.fld_failure_rate_predicted), \
                         SUM(t2.fld_failure_rate_mission), \
                         COUNT(t2.fld_assembly_id), \
                         SUM(1.0 / fld_mpmt), SUM(1.0 / fld_mcmt), \
                         SUM(1.0 / mttr), SUM(1.0 / fld_mmt), \
                         SUM(t2.fld_cost) \
                  FROM tbl_system AS t2 \
                  INNER JOIN tbl_functional_matrix AS t1 \
                  ON t2.fld_assembly_id = t1.fld_assembly_id \
                  WHERE t1.fld_function_id={0:d} \
                  AND t2.fld_part=1".format(function_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)
        if _error_code != 0:
            return _error_code

        _function.calculate_reliability(_results[0][0:3], mission_time,
                                        hr_multiplier)
        _function.calculate_availability(_results[0][3:7])
        _function.calculate_costs(_results[0][8], mission_time)

        return 0

    def save_function(self, function_id):
        """
        Saves the Function attributes to the RTK Project database.

        :param int function_id: the ID of the function to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _function = self.dicFunctions[function_id]

        _query = "UPDATE tbl_functions \
                  SET fld_availability={1:f}, fld_availability_mission={2:f}, \
                      fld_code='{3:s}', fld_cost={4:f}, \
                      fld_failure_rate_mission={5:f}, \
                      fld_failure_rate_predicted={6:f}, fld_mmt={7:f}, \
                      fld_mcmt={8:f}, fld_mpmt={9:f}, \
                      fld_mtbf_mission={10:f}, fld_mtbf_predicted={11:f}, \
                      fld_mttr={12:f}, fld_name='{13:s}', \
                      fld_remarks='{14:s}', fld_total_mode_quantity={15:d}, \
                      fld_total_part_quantity={16:d}, \
                      fld_type={17:d}, fld_parent_id={18:d}, \
                      fld_level={19:d}, fld_safety_critical={20:d} \
                  WHERE fld_function_id={0:d}".format(
                      _function.function_id, _function.availability,
                      _function.mission_availability, _function.code,
                      _function.cost, _function.mission_hazard_rate,
                      _function.hazard_rate, _function.mmt, _function.mcmt,
                      _function.mpmt, _function.mission_mtbf, _function.mtbf,
                      _function.mttr, _function.name, _function.remarks,
                      _function.n_modes, _function.n_parts, _function.type,
                      int(_function.parent_id), _function.level,
                      _function.safety_critical)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_functions(self):
        """
        Saves all Function data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _function in self.dicFunctions.values():
            (_results,
             _error_code) = self.save_function(_function.function_id)

        return False
