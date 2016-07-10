#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.revision.Revision.py is part of The RTK Project
#
# All rights reserved.

"""
############################
Revision Package Data Module
############################
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as Configuration
    import Utilities as Utilities
except ImportError:
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.Utilities as Utilities           # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):

    """
    The Revision data model contains the attributes and methods of a revision.
    An RTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:

    :ivar int revision_id: the ID of the Revision.
    :ivar str name: the noun name of the Revision.
    :ivar int n_parts: the number of hardware components comprising the
                       Revision.
    :ivar float cost: the total cost of the Revision.
    :ivar float cost_per_failure: the cost per failure of the Revision.
    :ivar float cost_per_hour: the cost per mission hour of the Revision.
    :ivar float active_hazard_rate: the active hazard rate of the Revision.
    :ivar float dormant_hazard_rate: the dormant hazard rate of the Revision.
    :ivar float software_hazard_rate: the software hazard rate of the Revision.
    :ivar float hazard_rate: the logistics hazard rate of the Revision.
    :ivar float mission_hazard_rate: the mission hazard rate of the Revision.
    :ivar float mtbf: the logistics mean time between failure of the Revision.
    :ivar float mission_mtbf: the mission mean time between failure of the
                              Revision.
    :ivar float reliability: the logistics reliability of the Revision.
    :ivar float mission_reliability: the mission reliability of the Revision.
    :ivar float mpmt: the mean preventive maintenance time of the Revision.
    :ivar float mcmt: the mean corrective maintenance time of the Revision.
    :ivar float mttr: the mean time to repair of the Revision.
    :ivar float mmt: the mean maintenance time of the Revision.
    :ivar float availability: the logistics availability of the Revision.
    :ivar float mission_availability: the mission availability of the Revision.
    :ivar str remarks: any user remarks related to the Revision.
    :ivar str code: the alphanumeric code for the Revision.
    :ivar float program_time: the program development time for the Revision.
    :ivar float program_time_se: the standard error of the program development
                                 time for the Revision.
    :ivar float program_cost: the program development cost for the Revision.
    :ivar float program_cost_se: the standard error of the program development
                                 cost for the Revision.
    """

    def __init__(self):
        """
        Method to initialize a Revision data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
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
            self.mission_mtbf = float(values[14])
            self.mtbf = float(values[15])
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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
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
            self.mission_hazard_rate = 0.0

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

    :ivar int _last_id: the last Revision ID used in the RTK Project database.
    :ivar dict dicRevisions: Dictionary of the Revision data models controlled.
                             Key is the Revision ID; value is a pointer to the
                             Revision data model instance.
    :ivar dao: the :py:class:`rtk.dao.DAO.DAO` to use when communicating with
               the RTK Project database.
    """

    def __init__(self):
        """
        Method to initialize a Revision data controller instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicRevisions = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None

    def request_revisions(self):
        """
        Method to read the RTK Project database and loads all the Revisions.
        For each Revision returned:

        #. Retrieve the revisions from the RTK Project database.
        #. Create a Revision data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Revisions being managed
           by this controller.

        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._last_id = self.dao.get_last_id('tbl_revisions')[0]

        _query = "SELECT * FROM tbl_revisions ORDER BY fld_revision_id"
        (_results, _error_code, __) = self.dao.execute(_query, commit=False)

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
        Method to add a new Revision to the RTK Project.

        :keyword str code: the code to use for the new Revision.
        :keyword str name: the name of the new Revision.
        :keyword str remarks: any remarks associated with the new Revision.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        if code == '' or code is None:
            code = '{0} {1}'.format(str(Configuration.RTK_PREFIX[0]),
                                    str(Configuration.RTK_PREFIX[1]))

            # Increment the revision index.
            Configuration.RTK_PREFIX[1] += 1

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
         _revision_id) = self.dao.execute(_query, commit=True)

        # If the new revision was added successfully to the RTK Project
        # database, add a new Revision model to the controller, add a mission
        # to the new Revision and then refresh the Module View.
        if _results:
            self._last_id = self.dao.get_last_id('tbl_revisions')[0]
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
             _mission_id) = self.dao.execute(_query, commit=True)

        return(_results, _error_code, _revision_id)

    def delete_revision(self, revision_id):
        """
        Method to delete a Revision from the RTK Project.

        :param int revision_id: the Revision ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM tbl_revisions \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        self.dicRevisions.pop(revision_id)

        return(_results, _error_code)

    def calculate_revision(self, revision_id, mission_time, hr_multiplier=1.0):
        """
        Method to calculate reliability, availability, and cost information for
        a Revision.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the calculations.
        :keyword float hr_multiplier: the multiplier to use for the hazard rate
                                      calculations.
        :return: _error_code
        :rtype: int
        """

        _revision = self.dicRevisions[revision_id]

        # First, attempt to retrieve results based on components associated
        # with the selected revision.
        _query = "SELECT SUM(t1.fld_hazard_rate_active), \
                         SUM(t1.fld_hazard_rate_dormant), \
                         SUM(t1.fld_hazard_rate_software), \
                         SUM(t1.fld_hazard_rate_mission), \
                         SUM(t2.fld_cost), COUNT(t1.fld_hardware_id) \
                  FROM rtk_reliability AS t1 \
                  INNER JOIN rtk_hardware AS t2 \
                  ON t2.fld_hardware_id=t1.fld_hardware_id \
                  WHERE t2.fld_revision_id={0:d} \
                  AND t2.fld_part=1".format(revision_id)
        # FIXME: See bug 186.
        # _query = "SELECT SUM(t1.fld_hazard_rate_active), \
        #                  SUM(t1.fld_hazard_rate_dormant), \
        #                  SUM(t1.fld_hazard_rate_software), \
        #                  SUM(t1.fld_hazard_rate_mission), \
        #                  SUM(1.0 / t2.fld_mpmt), SUM(1.0 / t2.fld_mcmt), \
        #                  SUM(1.0 / t2.fld_mttr), SUM(1.0 / t2.fld_mmt), \
        #                  SUM(t3.fld_cost), COUNT(t1.fld_hardware_id) \
        #           FROM rtk_reliability AS t1 \
        #           INNER JOIN rtk_maintainability AS t2 \
        #           ON t2.fld_hardware_id=t1.fld_hardware_id \
        #           INNER JOIN rtk_hardware AS t3 \
        #           ON t3.fld_hardware_id=t1.fld_hardware_id \
        #           WHERE t3.fld_revision_id={0:d} \
        #           AND t3.fld_part=1".format(revision_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=False)
        if _error_code != 0:
            return _error_code
        else:
            _revision.n_parts = int(_results[0][5])

        # If that doesn't work, attempt to retrieve results based on the first
        # level of assemblies associated with the selected revision.
        if _results[0][5] == 0:
            _query = "SELECT SUM(t1.fld_hazard_rate_active), \
                             SUM(t1.fld_hazard_rate_dormant), \
                             SUM(t1.fld_hazard_rate_software), \
                             SUM(t1.fld_hazard_rate_mission), \
                             SUM(t2.fld_cost) \
                      FROM rtk_reliability AS t1 \
                      INNER JOIN rtk_hardware AS t2 \
                      ON t2.fld_hardware_id=t1.fld_hardware_id \
                      WHERE t2.fld_revision_id={0:d} \
                      AND t2.fld_level=1 AND t2.fld_part=0".format(revision_id)
            # FIXME: See bug 186.
            # _query = "SELECT SUM(t1.fld_hazard_rate_active), \
            #                  SUM(t1.fld_hazard_rate_dormant), \
            #                  SUM(t1.fld_hazard_rate_software), \
            #                  SUM(t1.fld_hazard_rate_mission), \
            #                  SUM(1.0 / t2.fld_mpmt), SUM(1.0 / t2.fld_mcmt), \
            #                  SUM(1.0 / t2.fld_mttr), SUM(1.0 / t2.fld_mmt), \
            #                  SUM(t3.fld_cost) \
            #           FROM rtk_reliability AS t1 \
            #           INNER JOIN rtk_maintainability AS t2 \
            #           ON t2.fld_hardware_id=t1.fld_hardware_id \
            #           INNER JOIN rtk_hardware AS t3 \
            #           ON t3.fld_hardware_id=t1.fld_hardware_id \
            #           WHERE t3.fld_revision_id={0:d} \
            #           AND t3.fld_level=1 AND t3.fld_part=0".format(revision_id)
            (_results, _error_code, __) = self.dao.execute(_query,
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
                             fld_cost \
                      FROM rtk_hardware \
                      WHERE fld_revision_id={0:d} \
                      AND fld_level=0".format(revision_id)
            # FIXME: See bug 186.
            # _query = "SELECT fld_failure_rate_active, \
            #                  fld_failure_rate_dormant, \
            #                  fld_failure_rate_software, \
            #                  fld_failure_rate_mission, \
            #                  (1.0 / fld_mpmt), (1.0 / fld_mcmt), \
            #                  (1.0 / fld_mttr), (1.0 / fld_mmt), fld_cost \
            #           FROM rtk_hardware \
            #           WHERE fld_revision_id={0:d} \
            #           AND fld_level=0".format(revision_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                           commit=False)
            if _error_code != 0:
                return _error_code

        _revision.calculate_reliability(_results[0][0:4], mission_time,
                                        hr_multiplier)
        # FIXME: See bug 187.
        # _revision.calculate_availability(_results[0][4:8])
        _revision.calculate_costs(_results[0][4], mission_time)

        return 0

    def save_revision(self, revision_id):
        """
        Method to save the Revision attributes to the RTK Project database.

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
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_revisions(self):
        """
        Method to save all Revision data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _revision in self.dicRevisions.values():
            (_results,
             _error_code) = self.save_revision(_revision.revision_id)

        return False
