#!/usr/bin/env python
"""
##########################
Hazard Package Data Module
##########################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.hazard.Hazard.py is part of The RTK Project
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
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Hazard data model contains the attributes and methods of a Hazard.  The
    attributes of a Hazard are:

    :ivar hardware_id: the Hardware ID the Hazard is associated with.
    :ivar hazard_id: the ID of the Hazard.
    :ivar potential_hazard: the description of the potential hazard.
    :ivar potential_cause: the description of the potential cause of the
                           potential hazard.
    :ivar assembly_effect: the effect of the potential hazard on the assembly
                           being analyzed with no design mitigation.
    :ivar assembly_severity: the severity of the effect of the potential hazard
                             on the assembly being analyzed with no design
                             mitigation.
    :ivar assembly_probability: the probability of the effect of the potential
                                hazard on the assembly being analyzed with no
                                design mitigation.
    :ivar assembly_hri: the assembly hazard risk index with no design
                        mitigation.
    :ivar assembly_mitigation: the proposed design mitigation strategy at the
                               assembly level.
    :ivar assembly_severity_f: the effect of the potential hazard on the
                               assembly being analyzed with design mitigation.
    :ivar assembly_probability_f: the probability of the effect of the
                                  potential hazard on the assembly being
                                  analyzed with design mitigation.
    :ivar assembly_hri_f: the assembly hazard risk index with design
                          mitigation.
    :ivar system_effect: the effect of the potential hazard on the system being
                         analyzed.
    :ivar system_severity: the severity of the effect of the potential hazard
                           on the system being analyzed with no design
                           mitigation.
    :ivar system_probability: the probability of the effect of the potential
                              hazard on the system being analyzed with no
                              design mitigation.
    :ivar system_hri: the system hazard risk index with no design mitigation.
    :ivar system_mitigation: the proposed design mitigation strategy at the
                             system level.
    :ivar system_severity_f: the severity of the effect of the potential hazard
                             on the system being analyzed with design
                             mitigation.
    :ivar system_probability_f: the probability of the effect of the potential
                                hazard on the system being analyzed with
                                design mitigation.
    :ivar system_hri_f: the system hazard risk index with design mitigation.
    :ivar remarks: remarks associated with the potential hazard.
    :ivar function_1: user-defined mathematical function 1.
    :ivar function_2: user-defined mathematical function 2.
    :ivar function_3: user-defined mathematical function 3.
    :ivar function_4: user-defined mathematical function 4.
    :ivar function_5: user-defined mathematical function 5.
    :ivar result_1: results of user-defined mathematical function 1.
    :ivar result_2: results of user-defined mathematical function 2.
    :ivar result_3: results of user-defined mathematical function 3.
    :ivar result_4: results of user-defined mathematical function 4.
    :ivar result_5: results of user-defined mathematical function 5.
    :ivar user_blob_1: user-defined blob field 1.
    :ivar user_blob_2: user-defined blob field 2.
    :ivar user_blob_3: user-defined blob field 3.
    :ivar user_float_1: user-defined float field 1.  Can be used in the user-
                        defined functions.
    :ivar user_float_2: user-defined float field 2.  Can be used in the user-
                        defined functions.
    :ivar user_float_3: user-defined float field 3.  Can be used in the user-
                        defined functions.
    :ivar user_int_1: user-defined integer field 1.  Can be used in the user-
                      defined functions.
    :ivar user_int_2: user-defined integer field 2.  Can be used in the user-
                      defined functions.
    :ivar user_int_3: user-defined integer field 3.  Can be used in the user-
                      defined functions.
    """

    def __init__(self):
        """
        Method to initialize a Hazard data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.hardware_id = None
        self.hazard_id = None
        self.potential_hazard = ''
        self.potential_cause = ''
        self.assembly_effect = ''
        self.assembly_severity = 0
        self.assembly_probability = 0
        self.assembly_hri = 0
        self.assembly_mitigation = ''
        self.assembly_severity_f = 0
        self.assembly_probability_f = 0
        self.assembly_hri_f = 0
        self.system_effect = ''
        self.system_severity = 0
        self.system_probability = 0
        self.system_hri = 0
        self.system_mitigation = ''
        self.system_severity_f = 0
        self.system_probability_f = 0
        self.system_hri_f = 0
        self.remarks = ''
        self.function_1 = ''
        self.function_2 = ''
        self.function_3 = ''
        self.function_4 = ''
        self.function_5 = ''
        self.result_1 = 0.0
        self.result_2 = 0.0
        self.result_3 = 0.0
        self.result_4 = 0.0
        self.result_5 = 0.0
        self.user_blob_1 = ''
        self.user_blob_2 = ''
        self.user_blob_3 = ''
        self.user_float_1 = 0.0
        self.user_float_2 = 0.0
        self.user_float_3 = 0.0
        self.user_int_1 = 0
        self.user_int_2 = 0
        self.user_int_3 = 0

    def calculate(self):
        """
        Method to calculate the initial assembly hazard risk index (HRI), the
        final assembly HRI, the initial system HRI, and the final system HRI.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Calculate the MIL-STD-882 hazard risk indices.
        self.assembly_hri = self.assembly_probability * self.assembly_severity
        self.assembly_hri_f = self.assembly_probability_f * \
                              self.assembly_severity_f

        self.system_hri = self.system_probability * self.system_severity
        self.system_hri_f = self.system_probability_f * self.system_severity_f

        # Calculate the user-defined hazard calculations.
        _calculations = {}

        # Get the user-defined float and integer values.
        _calculations['uf1'] = self.user_float_1
        _calculations['uf2'] = self.user_float_2
        _calculations['uf3'] = self.user_float_3
        _calculations['ui1'] = self.user_int_1
        _calculations['ui2'] = self.user_int_2
        _calculations['ui3'] = self.user_int_3

        # Get the user-defined functions.
        _calculations['equation1'] = self.function_1
        _calculations['equation2'] = self.function_2
        _calculations['equation3'] = self.function_3
        _calculations['equation4'] = self.function_4
        _calculations['equation5'] = self.function_5

        # Get the existing results.  This allows the use of the results
        # fields to be manually set to a float values by the user.
        # Essentially creating five more user-defined float values.
        _calculations['res1'] = self.result_1
        _calculations['res2'] = self.result_2
        _calculations['res3'] = self.result_3
        _calculations['res4'] = self.result_4
        _calculations['res5'] = self.result_5

        _keys = _calculations.keys()
        _values = _calculations.values()

        for _index, _key in enumerate(_keys):
            vars()[_key] = _values[_index]

        try:
            self.result_1 = eval(_calculations['equation1'])
        except SyntaxError:
            self.result_1 = _calculations['res1']
        try:
            self.result_2 = eval(_calculations['equation2'])
        except SyntaxError:
            self.result_2 = _calculations['res2']
        try:
            self.result_3 = eval(_calculations['equation3'])
        except SyntaxError:
            self.result_3 = _calculations['res3']
        try:
            self.result_4 = eval(_calculations['equation4'])
        except SyntaxError:
            self.result_4 = _calculations['res4']
        try:
            self.result_5 = eval(_calculations['equation5'])
        except SyntaxError:
            self.result_5 = _calculations['res5']

        return False


class Hazard(object):
    """
    The Hazard data controller provides an interface between the Hazard data
    model and an RTK view model.  A single Hazard controller can manage one or
    more Hazard data models.  The attributes of an Hazard data controller are:

    :ivar dao: the Data Access Object to use when communicating with the RTK
               Project database.
    :ivar dicHazard: Dictionary of the Hazard data models managed.  Key is a
                     tuple of the Hardware ID and Hazard ID; value is a pointer
                     to the Hazard data model instance.
    """

    def __init__(self):
        """
        Method to initialize a Hazard data controller instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dicHazard = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None

    def request_hazard(self):
        """
        Method to read the RTK Project database and load all the Hazards.  For
        each Hazard returned:

        #. Retrieve the Hazard from the RTK Project database.
        #. Create an Hazard data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Hardware being managed
           by this controller.

        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT t1.fld_hardware_id, t1.fld_hazard_id, \
                         t1.fld_potential_hazard, t1.fld_potential_cause, \
                         t1.fld_assembly_effect, t1.fld_assembly_severity, \
                         t1.fld_assembly_probability, t1.fld_assembly_hri, \
                         t1.fld_assembly_mitigation, \
                         t1.fld_assembly_severity_f, \
                         t1.fld_assembly_probability_f, \
                         t1.fld_assembly_hri_f, t1.fld_system_effect, \
                         t1.fld_system_severity, t1.fld_system_probability, \
                         t1.fld_system_hri, t1.fld_system_mitigation, \
                         t1.fld_system_severity_f, \
                         t1.fld_system_probability_f, t1.fld_system_hri_f, \
                         t1.fld_remarks, t1.fld_function_1, \
                         t1.fld_function_2, t1.fld_function_3, \
                         t1.fld_function_4, t1.fld_function_5, \
                         t1.fld_result_1, t1.fld_result_2, t1.fld_result_3, \
                         t1.fld_result_4, t1.fld_result_5, \
                         t1.fld_user_blob_1, t1.fld_user_blob_2, \
                         t1.fld_user_blob_3, t1.fld_user_float_1, \
                         t1.fld_user_float_2, t1.fld_user_float_3, \
                         t1.fld_user_int_1, t1.fld_user_int_2, \
                         t1.fld_user_int_3, t2.fld_name, \
                         t3.fld_hazard_rate_logistics \
                  FROM rtk_hazard AS t1 \
                  INNER JOIN rtk_hardware AS t2 \
                  ON t2.fld_hardware_id=t1.fld_hardware_id \
                  INNER JOIN rtk_reliability AS t3 \
                  ON t3.fld_hardware_id=t1.fld_hardware_id \
                  ORDER BY t1.fld_hazard_id"
        (_results, _error_code, __) = self.dao.execute(_query, commit=False)

        try:
            _n_hazards = len(_results)
        except TypeError:
            _n_hazards = 0

        for i in range(_n_hazards):
            _hazard = Model()
            _hazard.set_attributes(_results[i][0:40])
            self.dicHazard[(_hazard.hardware_id, _hazard.hazard_id)] = _hazard

        return(_results, _error_code)

    def add_hazard(self, hardware_id):
        """
        Method to add a potential hazard to a Hardware item.

        :param int hardware_id: the Hardware ID to add the hazard to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO rtk_hazard \
                  (fld_hardware_id) \
                  VALUES({0:d})".format(hardware_id)
        (_results, _error_code, _last_id) = self.dao.execute(_query,
                                                             commit=True)

        _hazard = Model()
        _hazard.set_attributes((hardware_id, _last_id, '', '', '', 0, 0, 0,
                                '', 0, 0, 0, '', 0, 0, 0, '', 0, 0, 0, '',
                                '', '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0,
                                '', '', '', 0.0, 0.0, 0.0, 0, 0, 0))
        self.dicHazard[(hardware_id, _last_id)] = _hazard

        return(_results, _error_code, _last_id)

    def delete_hazard(self, hardware_id, hazard_id):
        """
        Method to delete a potential Hazard from the RTK Project database.

        :param int hardware_id: the Hardware ID to delete the hazards from.
        :param int hazard_id: the Hazard ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_hazard \
                  WHERE fld_hazard_id={0:d}".format(hazard_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)
        try:
            self.dicHazard.pop((hardware_id, hazard_id))
        except KeyError:
            _error_code = 60

        return(_results, _error_code)

    def calculate_hazard(self, hardware_id, hazard_id):
        """
        Method to calculate the hazard risk index (HRI) and user-defined
        calculations for a Hazard.

        :param int hardware_id: the Hardware ID to calculate.
        :param int hazard_id: the Hazard ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _hazard = self.dicHazard[(hardware_id, hazard_id)]

        _hazard.calculate()

        return False

    def save_hazard(self, hardware_id, hazard_id):
        """
        Method to save the Hazard attributes to the RTK Project database.

        :param int hardware_id: the ID of the hardware to save.
        :param int hazard_id: the ID of the hazard to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _hazard = self.dicHazard[(hardware_id, hazard_id)]

        _query = "UPDATE rtk_hazard \
                  SET fld_potential_hazard='{0:s}', \
                      fld_potential_cause='{1:s}', \
                      fld_assembly_effect='{2:s}', \
                      fld_assembly_severity={3:d}, \
                      fld_assembly_probability={4:d}, fld_assembly_hri={5:d}, \
                      fld_assembly_mitigation='{6:s}', \
                      fld_assembly_severity_f={7:d}, \
                      fld_assembly_probability_f={8:d}, \
                      fld_assembly_hri_f={9:d}, fld_system_effect='{10:s}', \
                      fld_system_severity={11:d}, \
                      fld_system_probability={12:d}, \
                      fld_system_hri={13:d}, fld_system_mitigation='{14:s}', \
                      fld_system_severity_f={15:d}, \
                      fld_system_probability_f={16:d}, \
                      fld_system_hri_f={17:d}, \
                      fld_remarks='{18:s}', fld_function_1='{19:s}', \
                      fld_function_2='{20:s}', fld_function_3='{21:s}', \
                      fld_function_4='{22:s}', fld_function_5='{23:s}', \
                      fld_result_1={24:f}, fld_result_2={25:f}, \
                      fld_result_3={26:f}, fld_result_4={27:f}, \
                      fld_result_5={28:f}, fld_user_blob_1='{29:s}', \
                      fld_user_blob_2='{30:s}', fld_user_blob_3='{31:s}', \
                      fld_user_float_1={32:f}, fld_user_float_2={33:f}, \
                      fld_user_float_3={34:f}, fld_user_int_1={35:d}, \
                      fld_user_int_2={36:d}, fld_user_int_3={37:d} \
                  WHERE fld_hazard_id={38:d}".format(
                      _hazard.potential_hazard,
                      _hazard.potential_cause.replace("'", r"''"),
                      _hazard.assembly_effect.replace("'", r"''"),
                      _hazard.assembly_severity, _hazard.assembly_probability,
                      _hazard.assembly_hri,
                      _hazard.assembly_mitigation.replace("'", r"''"),
                      _hazard.assembly_severity_f,
                      _hazard.assembly_probability_f, _hazard.assembly_hri_f,
                      _hazard.system_effect.replace("'", r"''"),
                      _hazard.system_severity, _hazard.system_probability,
                      _hazard.system_hri,
                      _hazard.system_mitigation.replace("'", r"''"),
                      _hazard.system_severity_f, _hazard.system_probability_f,
                      _hazard.system_hri_f,
                      _hazard.remarks.replace("'", r"''"), _hazard.function_1,
                      _hazard.function_2, _hazard.function_3,
                      _hazard.function_4, _hazard.function_5, _hazard.result_1,
                      _hazard.result_2, _hazard.result_3, _hazard.result_4,
                      _hazard.result_5,
                      _hazard.user_blob_1.replace("'", r"''"),
                      _hazard.user_blob_2.replace("'", r"''"),
                      _hazard.user_blob_3.replace("'", r"''"),
                      _hazard.user_float_1, _hazard.user_float_2,
                      _hazard.user_float_3, _hazard.user_int_1,
                      _hazard.user_int_2, _hazard.user_int_3,
                      _hazard.hazard_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_hazards(self):
        """
        Method to save all Hazard data models managed by the controller.

        :return: _error_codes; list of tuples containing hardware ID, hazard
                 ID, and error code.
        :rtype: list
        """

        _error_codes = []

        for _hazard in self.dicHazard.values():
            (_results, _error_code) = self.save_hazard(_hazard.hardware_id,
                                                       _hazard.hazard_id)
            _error_codes.append((_hazard.hardware_id, _hazard.hazard_id,
                                 _error_code))

        return _error_codes
