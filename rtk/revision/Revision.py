#!/usr/bin/env python
"""
############################
Revision Package Data Module
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Revision.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Model(object):
    """
    The Revision data model contains the attributes and methods of a revision.
    An RTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:

    :ivar revision_id: default value: 0
    :ivar name: default value: ''
    :ivar n_parts: default value: 0
    :ivar cost: default value: 0
    :ivar cost_per_failure: default value: 0.0
    :ivar cost_per_hour: default value: 0.0
    :ivar active_hazard_rate: default value: 0.0
    :ivar dormant_hazard_rate: default value: 0.0
    :ivar software_hazard_rate: default value: 0.0
    :ivar hazard_rate: default value: 0.0
    :ivar mission_hazard_rate: default value: 0.0
    :ivar mtbf: default value: 0.0
    :ivar mission_mtbf: default value: 0.0
    :ivar reliability: default value: 0.0
    :ivar mission_reliability: default value: 0.0
    :ivar mpmt: default value: 0.0
    :ivar mcmt: default value: 0.0
    :ivar mttr: default value: 0.0
    :ivar mmt: default value: 0.0
    :ivar availability: default value: 0.0
    :ivar mission_availability: default value: 0.0
    :ivar remarks: default value: ''
    :ivar code: default value: ''
    :ivar program_time: default value: 0.0
    :ivar program_time_se: default value: 0.0
    :ivar program_cost: default value: 0.0
    :ivar program_cost_se: default value: 0.0
    """

    def __init__(self):
        """
        Method to initialize a Revision data model instance.
        """

        # Define public Revision class attributes.
        self.revision_id = 0
        self.name = ''
        self.n_parts = 0
        self.cost = 0.0
        self.cost_per_failure = 0.0
        self.cost_per_hour = 0.0
        self.active_hazard_rate = 0.0
        self.dormant_hazard_rate = 0.0
        self.software_hazard_rate = 0.0
        self.hazard_rate = 0.0
        self.mission_hazard_rate = 0.0
        self.mtbf = 0.0
        self.mission_mtbf = 0.0
        self.reliability = 0.0
        self.mission_reliability = 0.0
        self.mpmt = 0.0
        self.mcmt = 0.0
        self.mttr = 0.0
        self.mmt = 0.0
        self.availability = 0.0
        self.mission_availability = 0.0
        self.remarks = ''
        self.code = ''
        self.program_time = 0.0
        self.program_time_se = 0.0
        self.program_cost = 0.0
        self.program_cost_se = 0.0

    def set_attributes(self, values):
        """
        Method to set the Revision data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.availability = float(values[1])
            self.mission_availability = float(values[2])
            self.cost = float(values[3])
            self.cost_per_failure = float(values[4])
            self.cost_per_hour = float(values[5])
            self.active_hazard_rate = float(values[6])
            self.dormant_hazard_rate = float(values[7])
            self.mission_hazard_rate = float(values[8])
            self.hazard_rate = float(values[9])
            self.software_hazard_rate = float(values[10])
            self.mmt = float(values[11])
            self.mcmt = float(values[12])
            self.mpmt = float(values[13])
            self.mtbf = float(values[14])
            self.mission_mtbf = float(values[15])
            self.mttr = float(values[16])
            self.name = str(values[17])
            self.mission_reliability = float(values[18])
            self.reliability = float(values[19])
            self.remarks = str(values[20])
            self.n_parts = int(values[21])
            self.code = str(values[22])
            self.program_time = float(values[23])
            self.program_time_se = float(values[24])
            self.program_cost = float(values[25])
            self.program_cost_se = float(values[26])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Revision data model
        attributes.

        :return: (revision_id, availability, mission_availability, cost,
                  cost_per_failure, cost_per_hour, active_hazard_rate,
                  dormant_hazard_rate, mission_hazard_rate, hazard_rate,
                  software_hazard_rate, mmt, mcmt, mpmt, mission_mtbf, mtbf,
                  mttr, name, mission_reliability, reliability, remarks,
                  n_parts, code, program_time, program_time_se, program_cost,
                  program_cost_se)
        :rtype: tuple
        """

        _values = (self.revision_id, self.availability,
                   self.mission_availability, self.cost, self.cost_per_failure,
                   self.cost_per_hour, self.active_hazard_rate,
                   self.dormant_hazard_rate, self.mission_hazard_rate,
                   self.hazard_rate, self.software_hazard_rate, self.mmt,
                   self.mcmt, self.mpmt, self.mission_mtbf, self.mtbf,
                   self.mttr, self.name, self.mission_reliability,
                   self.reliability, self.remarks, self.n_parts, self.code,
                   self.program_time, self.program_time_se, self.program_cost,
                   self.program_cost_se)

        return _values

    def calculate_reliability(self, inputs, mission_time, hr_multiplier=1.0):
        """
        Method to calculate the active hazard rate, dormant hazard rate,
        software hazard rate, inherent hazard rate, mission hazard rate,
        MTBF, mission MTBF, inherent reliability, and mission reliability.

        :param tuple inputs: tuple containing the input data for the
                             reliability calculations.  The tuple must be in
                             order:

                                #. Active Failure Rate
                                #. Dormant Failure Rate
                                #. Software Failure Rate
                                #. Mission Failure Rate

        :param float mission_time: the time to use in the reliability
                                   calculations.
        :keyword float hr_multiplier: the multiplier to use for the hazard rate
                                      calculations.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        try:
            self.active_hazard_rate = float(inputs[0])
        except TypeError:
            self.active_hazard_rate = 0.0

        try:
            self.dormant_hazard_rate = float(inputs[1])
        except TypeError:
            self.dormant_hazard_rate = 0.0

        try:
            self.software_hazard_rate = float(inputs[2])
        except TypeError:
            self.software_hazard_rate = 0.0

        try:
            self.mission_hazard_rate = float(inputs[3])
        except TypeError:
            self.mission_hazard_rate = 0

        # Calculate the logistics h(t).
        self.hazard_rate = self.active_hazard_rate + \
            self.dormant_hazard_rate + self.software_hazard_rate

        # Calculate the logistics MTBF.
        try:
            self.mtbf = 1.0 / self.hazard_rate
        except(ZeroDivisionError, OverflowError):
            self.mtbf = 0.0

        # Calculate the mission MTBF.
        try:
            self.mission_mtbf = 1.0 / self.mission_hazard_rate
        except(ZeroDivisionError, OverflowError):
            self.mission_mtbf = 0.0

        # Calculate reliabilities.
        self.reliability = exp(-1.0 * self.hazard_rate * mission_time /
                               hr_multiplier)
        self.mission_reliability = exp(-1.0 * self.mission_hazard_rate *
                                       mission_time / hr_multiplier)

        return False

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
        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """

        try:
            self.mpmt = 1.0 / float(inputs[0])
        except(TypeError, ZeroDivisionError):
            self.mpmt = 0.0

        try:
            self.mcmt = 1.0 / float(inputs[1])
        except(TypeError, ZeroDivisionError):
            self.mcmt = 0.0

        try:
            self.mttr = 1.0 / float(inputs[2])
        except(TypeError, ZeroDivisionError):
            self.mttr = 0.0

        try:
            self.mmt = 1.0 / float(inputs[3])
        except(TypeError, ZeroDivisionError):
            self.mmt = 0.0

        # Calculate logistics availability.
        try:
            self.availability = self.mtbf / (self.mtbf + self.mttr)
        except(ZeroDivisionError, OverflowError):
            self.availability = 1.0

        # Calculate mission availability.
        try:
            self.mission_availability = self.mission_mtbf / \
                (self.mission_mtbf + self.mttr)
        except(ZeroDivisionError, OverflowError):
            self.mission_availability = 1.0

        return False

    def calculate_costs(self, inputs, mission_time):
        """
        Method to calculate the total cost, cost per failure, and cost per
        operating hour.

        :revision tuple inputs: tuple containing the input data for the cost
                                calculations.  The tuple must be in order:

                                #. Cost

        :param float mission_time: the time over which to calculate costs.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        try:
            self.cost = float(inputs)
        except TypeError:
            self.cost = 0.0

        # Calculate costs.
        self.cost_per_failure = self.cost * self.hazard_rate
        try:
            self.cost_per_hour = self.cost / mission_time
        except ZeroDivisionError:
            self.cost_per_hour = 0.0

        return False


class Revision(object):
    """
    The Revision data controller provides an interface between the Revision
    data model and an RTK view model.  A single Revision controller can manage
    one or more Revision data models.  The attributes of a Revision data
    controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
    Project database.
    :ivar dicRevisions: Dictionary of the Revision data models controlled.  Key
    is the Revision ID; value is a pointer to the Revision data model instance.
    """

    def __init__(self):
        """
        Initializes a Revision data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicRevisions = {}

    def request_revisions(self, dao):
        """
        Reads the RTK Project database and loads all the revisions.  For each
        revision returned:

        #. Retrieve the revisions from the RTK Project database.
        #. Create a Revision data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Revisions being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('tbl_revisions')[0]

        _query = "SELECT * FROM tbl_revisions ORDER BY fld_revision_id"
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_revisions = len(_results)
        except ValueError:
            _n_revisions = 0

        for i in range(_n_revisions):
            _revision = Model()
            _revision.set_attributes(_results[i])
            self.dicRevisions[_revision.revision_id] = _revision

        return(_results, _error_code)

    def add_revision(self, code=None, name=None, remarks=''):
        """
        Adds a new Revision to the RTK Project.

        :keyword str code: the code to use for the new Revision.
        :keyword str name: the name of the new Revision.
        :keyword str remarks: any remarks associated with the new Revision.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        if code == '' or code is None:
            code = '{0} {1}'.format(str(_conf.RTK_PREFIX[0]),
                                    str(_conf.RTK_PREFIX[1]))

            # Increment the revision index.
            _conf.RTK_PREFIX[1] += 1

        if name == '' or name is None:
            name = 'New Revision'

        # First we add the new revision.  Second we retrieve thew new revision
        # id.  Third, we create a new, top-level system entry for this
        # revision.
        _query = "INSERT INTO tbl_revisions (fld_name, fld_remarks, \
                                             fld_revision_code) \
                  VALUES ('{0:s}', '{1:s}', '{2:s}')".format(name, remarks,
                                                             code)
        (_results,
         _error_code,
         _revision_id) = self._dao.execute(_query, commit=True)

        # If the new revision was added successfully to the RTK Project
        # database, add a new Revision model to the controller, add a mission
        # to the new Revision and then refresh the Module View.
        if _results:
            self._last_id = self._dao.get_last_id('tbl_revisions')[0]
            _revision = Model()
            _revision.set_attributes((self._last_id, 1.0, 1.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0, name, 1.0, 1.0, remarks,
                                      1, code, 0.0, 0.0, 0.0, 0.0))
            self.dicRevisions[_revision.revision_id] = _revision

            _query = "INSERT INTO tbl_missions (fld_revision_id) \
                      VALUES ({0:d})".format(_revision.revision_id)
            (_results,
             _error_code,
             _mission_id) = self._dao.execute(_query, commit=True)

        return(_results, _error_code, _revision_id)

    def delete_revision(self, revision_id):
        """
        Deletes a Revision from the RTK Project.

        :param int revision_id: the Revision ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM tbl_revisions \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        self.dicRevisions.pop(revision_id)

        return(_results, _error_code)

    def calculate_revision(self, revision_id, mission_time, hr_multiplier=1.0):
        """
        Calculates reliability, availability, and cost information for a
        Revision.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the calculations.
        :keyword float hr_multiplier: the multiplier to use for the hazard rate
                                      calculations.
        :return: _error_code
        :rtype: int
        """

        _revision = self.dicRevisions[revision_id]

        # First attempt to retrieve results based on components associated
        # with the selected revision.
        _query = "SELECT SUM(fld_failure_rate_active), \
                         SUM(fld_failure_rate_dormant), \
                         SUM(fld_failure_rate_software), \
                         SUM(fld_failure_rate_mission), \
                         SUM(1.0 / fld_mpmt), SUM(1.0 / fld_mcmt), \
                         SUM(1.0 / fld_mttr), SUM(1.0 / fld_mmt), \
                         SUM(fld_cost), COUNT(fld_assembly_id) \
                  FROM rtk_hardware \
                  WHERE fld_revision_id={0:d} \
                  AND fld_part=1".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)
        if _error_code != 0:
            return _error_code

        # If that doesn't work, attempt to retrieve results based on the first
        # level of assemblies associated with the selected revision.
        if _results[0][9] == 0:
            _query = "SELECT SUM(fld_failure_rate_active), \
                             SUM(fld_failure_rate_dormant), \
                             SUM(fld_failure_rate_software), \
                             SUM(fld_failure_rate_mission), \
                             SUM(1.0 / fld_mpmt), SUM(1.0 / fld_mcmt), \
                             SUM(1.0 / fld_mttr), SUM(1.0 / fld_mmt), \
                             SUM(fld_cost) \
                      FROM rtk_hardware \
                      WHERE fld_revision_id={0:d} \
                      AND fld_level=1 AND fld_part=0".format(revision_id)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=False)
            if _error_code != 0:
                return _error_code

        # Finally, if that doesn't work, use the system results for the
        # revision.
        if _results[0][0] == 0:
            _query = "SELECT fld_failure_rate_active, \
                             fld_failure_rate_dormant, \
                             fld_failure_rate_software, \
                             fld_failure_rate_mission, \
                             (1.0 / fld_mpmt),(1.0 / fld_mcmt), \
                             (1.0 / fld_mttr), (1.0 / fld_mmt), fld_cost \
                      FROM rtk_hardware \
                      WHERE fld_revision_id={0:d} \
                      AND fld_level=0".format(revision_id)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=False)
            if _error_code != 0:
                return _error_code

        _revision.calculate_reliability(_results[0][0:4], mission_time,
                                        hr_multiplier)
        _revision.calculate_availability(_results[0][4:8])
        _revision.calculate_costs(_results[0][8], mission_time)

        return 0

    def save_revision(self, revision_id):
        """
        Saves the Revision attributes to the RTK Project database.

        :param int revision_id: the ID of the revision to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _revision = self.dicRevisions[revision_id]

        _query = "UPDATE tbl_revisions \
                  SET fld_availability={1:f}, fld_availability_mission={2:f}, \
                      fld_cost={3:f}, fld_cost_failure={4:f}, \
                      fld_cost_hour={5:f}, \
                      fld_failure_rate_active={6:g}, \
                      fld_failure_rate_dormant={7:g}, \
                      fld_failure_rate_mission={8:g}, \
                      fld_failure_rate_predicted={9:g}, \
                      fld_failure_rate_software={10:g}, fld_mmt={11:g}, \
                      fld_mcmt={12:g}, fld_mpmt={13:g}, \
                      fld_mtbf_mission={14:g}, fld_mtbf_predicted={15:g}, \
                      fld_mttr={16:g}, fld_name='{17:s}', \
                      fld_reliability_mission={18:f}, \
                      fld_reliability_predicted={19:f}, fld_remarks='{20:s}', \
                      fld_total_part_quantity={21:d}, \
                      fld_revision_code='{22:s}', fld_program_time={23:f}, \
                      fld_program_time_sd={24:f}, fld_program_cost={25:f}, \
                      fld_program_cost_sd={26:f} \
                  WHERE fld_revision_id={0:d}".format(
                      _revision.revision_id,
                      _revision.availability, _revision.mission_availability,
                      _revision.cost, _revision.cost_per_failure,
                      _revision.cost_per_hour, _revision.active_hazard_rate,
                      _revision.dormant_hazard_rate,
                      _revision.mission_hazard_rate,
                      _revision.hazard_rate, _revision.software_hazard_rate,
                      _revision.mmt, _revision.mcmt, _revision.mpmt,
                      _revision.mission_mtbf, _revision.mtbf, _revision.mttr,
                      _revision.name, _revision.mission_reliability,
                      _revision.reliability, _revision.remarks,
                      _revision.n_parts, _revision.code,
                      _revision.program_time, _revision.program_time_se,
                      _revision.program_cost, _revision.program_cost_se)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_revisions(self):
        """
        Saves all Revision data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _revision in self.dicRevisions.values():
            (_results,
             _error_code) = self.save_revision(_revision.revision_id)

        return False
