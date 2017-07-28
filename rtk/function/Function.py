#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.function.Function.py is part of The RTK Project
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
############################
Function Package Data Module
############################
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Function data model contains the attributes and methods of a function.
    A :py:class:`rtk.revision.Revision` will consist of one or more Functions.
    The attributes of a Function are:

    :ivar int revision_id: the ID of the
                           :py:class:`rtk.revision.Revision.Model` the Function
                           belongs to.  Default value = 0.
    :ivar int function_id: the ID of the Function.  Default value = 0.
    :ivar availability: the estimated availability of the Function.  Default
                        value = 1.0.
    :ivar float mission_availability: the estimated mission availability of the
                                      Function.  Default value = 1.0.
    :ivar str code: the alphanumeric code for this Function.  Default
                    value = ''.
    :ivar float cost: the estimated O&M costs for this Function.  Default
                      value = 0.0.
    :ivar float cost_per_failure: the estimated O&M costs for this Function per
                                  failure.  Default value = 0.0.
    :ivar float cost_per_hour: the estimated O&M costs for this Function per
                               mission hour.  Default value = 0.0.
    :ivar float mission_hazard_rate: the estimated mission hazard rate for this
                                     Function.  Default value = 0.0.
    :ivar float hazard_rate: the estimated hazard rate for this Function.
                             Default value = 0.0.
    :ivar float mmt: the estimated mean maintenance time for this Function.
                     Default value = 0.0.
    :ivar float mcmt: the estimated mean corrective maintenance time for this
                      Function.  Default value = 0.0.
    :ivar float mpmt: the estimated mean preventive maintenance time for this
                      Function.  Default value = 0.0.
    :ivar float mission_mtbf: the estimated mission mean time between failures
                              for this Function.  Default value = 0.0.
    :ivar float mtbf: the estimated mean time between failures for this
                      Function.  Default value = 0.0.
    :ivar float mttr: the estimated mean time to repair this Function.  Default
                      value = 0.0.
    :ivar str name: the noun name or description of this Function.  Default
                    value = ''.
    :ivar str remarks: user remarks associated with this Function.  Default
                       value = ''.
    :ivar int n_modes: the number of failure modes this Function is susceptible
                       to.  Default value = 0.
    :ivar int n_parts: the number of hardware parts comprising this Function.
                       Default value = 0.
    :ivar int type: the type of function this Function is.  Default value = 0.
    :ivar int parent_id: the ID of this Function's parent Function.  Default
                         value = -1 (no parent).
    :ivar int level: the level this Function falls in the Function hierarchy.
                     Default value = 0.
    :ivar int safety_critical: indicates whether the Function is safety
                               critical or not.  Default value = 1 (yes).
    """

    def __init__(self):
        """
        Method to initialize a Function data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.revision_id = 0
        self.function_id = 0
        self.availability = 1.0
        self.mission_availability = 1.0
        self.function_code = ''
        self.cost = 0.0
        self.cost_per_failure = 0.0
        self.cost_per_hour = 0.0
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
        self.function_type = 0
        self.parent_id = -1
        self.level = 0
        self.safety_critical = 1


class Function(object):
    """
    The Function data controller provides an interface between the Function
    data model and an RTK view model.  A single Function controller can manage
    one or more Function data models.  The attributes of a Function data
    controller are:

    :ivar _last_id: the last Function ID used.  Default value = None.
    :ivar dicFunctions: Dictionary of the Function data models controlled.  Key
                        is the Function ID; value is a pointer to the Function
                        data model instance.  Default value = {}.
    :ivar dao: the :py:class:`rtk.dao.DAO` to use when communicating with the
               RTK Project database.  Default value = None.
    """

    def __init__(self):
        """
        Method to initialize a Function data controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._last_id = None

        # Define public dictionary attributes.
        self.dicFunctions = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.dao = None

    def request_functions(self, revision_id):
        """
        Reads the RTK Project database and loads all the Functions associated
        with the selected Revision.  For each Function returned:

        #. Retrieve the functions from the RTK Project database.
        #. Create a Function data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Functions being managed
           by this controller.

        :param int revision_id: the Revision ID to select the Functions for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._last_id = self.dao.get_last_id('tbl_functions')[0]

        # Select everything from the function table.
        _query = "SELECT * FROM tbl_functions \
                  WHERE fld_revision_id={0:d} \
                  ORDER BY fld_parent_id".format(revision_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=False)

        try:
            _n_functions = len(_results)
        except TypeError:
            _n_functions = 0

        for i in range(_n_functions):
            _function = Model()
            _function.set_attributes(_results[i])
            self.dicFunctions[_function.function_id] = _function

        return(_results, _error_code)

    def add_function(self, revision_id, parent_id=-1, fcode=None, name=None,
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

        if parent_id is None:
            parent_id = -1
        if fcode is None:
            fcode = 'FUNC'
        if name is None:
            name = 'New Function'

        _query = "INSERT INTO tbl_functions \
                  (fld_revision_id, fld_name, fld_remarks, fld_code, \
                   fld_parent_id) \
                  VALUES ({0:d}, '{1:s}', '{2:s}', '{3:s}', {4:d})".format(
                      revision_id, name, remarks, fcode, parent_id)
        (_results,
         _error_code,
         _function_id) = self.dao.execute(_query, commit=True)

        # If the new function was added successfully to the RTK Project
        # database:
        #   1. Retrieve the ID of the newly inserted function.
        #   2. Create a new Function model instance.
        #   3. Set the attributes of the new Function model instance.
        #   4. Add the new Function model to the controller dictionary.
        if _results:
            self._last_id = self.dao.get_last_id('tbl_functions')[0]
            _function = Model()
            _function.set_attributes((revision_id, self._last_id, 1.0, 1.0,
                                      fcode, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0, name, remarks, 0, 0, 0,
                                      parent_id, 0, 1))
            self.dicFunctions[_function.function_id] = _function

        return(_function, _error_code, _function_id)

    def delete_function(self, function_id):
        """
        Deletes a Function from the RTK Project.

        :param int function_id: the Function ID to delete.
        :return: (_results, _error_codes)
        :rtype: tuple
        """

        _error_codes = [0, 0]

        # Delete all the child Functions, if any.
        _query = "DELETE FROM tbl_functions \
                  WHERE fld_parent_id={0:d}".format(function_id)
        (_results,
         _error_codes[0],
         __) = self.dao.execute(_query, commit=True)

        # Then delete the parent Function.
        _query = "DELETE FROM tbl_functions \
                  WHERE fld_function_id={0:d}".format(function_id)
        (_results,
         _error_codes[1],
         __) = self.dao.execute(_query, commit=True)

        self.dicFunctions.pop(function_id)

        return(_results, _error_codes)

    def copy_function(self, revision_id):
        """
        Method to copy a Function from the currently selected Revision to the
        new Revision.

        :param int revision_id: the ID of the newly created Revision.
        :return: _dic_index_xref; a dictionary cross-referencing the original
                 Function ID's with the new Function ID's.  Key is the original
                 Function ID, value is the new Function ID.
        :rtype: dict
        """
        # FIXME: See bug 184.
        # FIXME: See bug 185.
        # Find the existing maximum Function ID already in the RTK Project
        # database and increment it by one.  If there are no existing Functions
        # set the first Function ID to zero.
        _query = "SELECT MAX(fld_function_id) FROM tbl_functions"
        (_function_id, _error_code, __) = self.dao.execute(_query,
                                                            commit=False)

        if _function_id[0][0] is not None:
            _function_id = _function_id[0][0] + 1
        else:
            _function_id = 0

        # Copy the Function hierarchy for the new Revision.
        _dic_index_xref = {}
        _dic_index_xref[-1] = -1
        for _function in self.dicFunctions.values():
            _query = "INSERT INTO tbl_functions \
                      (fld_revision_id, fld_function_id, fld_code, \
                       fld_level, fld_name, fld_parent_id, \
                       fld_remarks) \
                      VALUES ({0:d}, {1:d}, '{2:s}', {3:d}, '{4:s}', {5:d}, \
                              '{6:s}')".format(revision_id, _function_id,
                                               _function.function_code,
                                               _function.level,
                                               _function.name,
                                               _function.parent_id,
                                               _function.remarks)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

            # Add an entry to the Function ID cross-reference dictionary for
            # for the newly added Function.
            if _error_code == 0:
                _dic_index_xref[_function.function_id] = _function_id
                _function_id += 1

        # Update the parent IDs for the new Functions using the index
        # cross-reference dictionary that was created when adding the new
        # Functions.
        for _key in _dic_index_xref.keys():
            _query = "UPDATE tbl_functions \
                      SET fld_parent_id={0:d} \
                      WHERE fld_parent_id={1:d} \
                      AND fld_revision_id={2:d}".format(_dic_index_xref[_key],
                                                        _key, revision_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=True)

        return _dic_index_xref

    def calculate_function(self, mission_time):
        """
        Method to clculate reliability, availability, and cost information for
        all Functions.

        :param float mission_time: the time to use in the calculations.
        :return: _error_codes; a list of tuples where each tuple is:
                 (Function ID, Error Code Returned from it's Calculation)
        :rtype: list
        """

        _error_codes = []

        for __, _function_id in enumerate(self.dicFunctions.keys()):

            _function = self.dicFunctions[_function_id]

            # All the calculations are pretty simple, so just do them using
            # SQL.
            _query = "SELECT SUM(t2.fld_hazard_rate_logistics), \
                             SUM(t2.fld_hazard_rate_mission), \
                             COUNT(t2.fld_hardware_id), \
                             SUM(t3.fld_cost) \
                      FROM rtk_reliability AS t2 \
                      INNER JOIN rtk_matrix AS t1 \
                      ON t2.fld_hardware_id = t1.fld_col_item_id \
                      INNER JOIN rtk_hardware AS t3 \
                      ON t3.fld_hardware_id = t1.fld_col_item_id \
                      WHERE t1.fld_value='2' \
                      AND t1.fld_row_item_id={0:d}".format(_function_id)
            # FIXME: See bug 189.
            # _query = "SELECT SUM(t2.fld_hazard_rate_logistics), \
            #                  SUM(t2.fld_hazard_rate_mission), \
            #                  COUNT(t2.fld_hardware_id), \
            #                  SUM(1.0 / t4.fld_mpmt), SUM(1.0 / t4.fld_mcmt), \
            #                  SUM(1.0 / t4.fld_mttr), SUM(1.0 / t4.fld_mmt), \
            #                  SUM(t3.fld_cost) \
            #           FROM rtk_reliability AS t2 \
            #           INNER JOIN rtk_matrix AS t1 \
            #           ON t2.fld_hardware_id = t1.fld_col_item_id \
            #           INNER JOIN rtk_hardware AS t3 \
            #           ON t3.fld_hardware_id = t1.fld_col_item_id \
            #           INNER JOIN rtk_maintainability AS t4 \
            #           ON t4.fld_hardware_id = t1.fld_col_item_id \
            #           WHERE t1.fld_value='2' \
            #           AND t1.fld_row_item_id={0:d}".format(_function_id)
            (_results, _error_code, __) = self.dao.execute(_query,
                                                            commit=False)

            _error_codes.append((_function.function_id, _error_code))

            # Perform the calculations if the query returned the proper values.
            if _error_code == 0:
                _function.calculate_reliability(_results[0][0:3])
                # FIXME: See bug 189.
                # _function.calculate_availability(_results[0][3:7])
                _function.calculate_costs(_results[0][3], mission_time)

        return _error_codes

    def save_function(self, function_id):
        """
        Method to save the Function attributes to the RTK Project database.

        :param int function_id: the ID of the Function to save.
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
                      _function.mission_availability, _function.function_code,
                      _function.cost, _function.mission_hazard_rate,
                      _function.hazard_rate, _function.mmt, _function.mcmt,
                      _function.mpmt, _function.mission_mtbf, _function.mtbf,
                      _function.mttr, _function.name, _function.remarks,
                      _function.n_modes, _function.n_parts,
                      _function.function_type, int(_function.parent_id),
                      _function.level, _function.safety_critical)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_functions(self):
        """
        Method to save all Function data models managed by the controller.

        :return: _error_codes; a list of tuples where each tuple is:
                 (Function ID, Error Code Returned from it's Save)
        :rtype: list
        """

        _error_codes = []

        for _function in self.dicFunctions.values():
            (_results,
             _error_code) = self.save_function(_function.function_id)

            _error_codes.append((_function.function_id, _error_code))

        return _error_codes
