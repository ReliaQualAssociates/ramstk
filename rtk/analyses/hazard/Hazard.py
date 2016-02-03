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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    import Utilities as _util
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Hazard data model contains the attributes and methods of an
    allocation.  The attributes of an Hazard are:

    :ivar hardware_id: default value: None
    :ivar parent_id: default value: -1
    """

    def __init__(self):
        """
        Initializes an Hazard data model instance.
        """

        # Initialize public scalar attributes.
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

    def set_attributes(self, values):
        """
        Sets the Hazard data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.hardware_id = int(values[0])
            self.hazard_id = int(values[1])
            self.potential_hazard = str(values[2])
            self.potential_cause = str(values[3])
            self.assembly_effect = str(values[4])
            self.assembly_severity = int(values[5])
            self.assembly_probability = int(values[6])
            self.assembly_hri = int(values[7])
            self.assembly_mitigation = str(values[8])
            self.assembly_severity_f = int(values[9])
            self.assembly_probability_f = int(values[10])
            self.assembly_hri_f = int(values[11])
            self.system_effect = str(values[12])
            self.system_severity = int(values[13])
            self.system_probability = int(values[14])
            self.system_hri = int(values[15])
            self.system_mitigation = str(values[16])
            self.system_severity_f = int(values[17])
            self.system_probability_f = int(values[18])
            self.system_hri_f = int(values[19])
            self.remarks = str(values[20])
            self.function_1 = str(values[21])
            self.function_2 = str(values[22])
            self.function_3 = str(values[23])
            self.function_4 = str(values[24])
            self.function_5 = str(values[25])
            self.result_1 = float(values[26])
            self.result_2 = float(values[27])
            self.result_3 = float(values[28])
            self.result_4 = float(values[29])
            self.result_5 = float(values[30])
            self.user_blob_1 = str(values[31])
            self.user_blob_2 = str(values[32])
            self.user_blob_3 = str(values[33])
            self.user_float_1 = float(values[34])
            self.user_float_2 = float(values[35])
            self.user_float_3 = float(values[36])
            self.user_int_1 = int(values[37])
            self.user_int_2 = int(values[38])
            self.user_int_3 = int(values[39])
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Hazard data model attributes.

        :return: (hardware_id, hazard_id, potential_hazard, potential_cause,
                  assembly_effect, assembly_severity, assembly_probability,
                  assembly_hri, assembly_mitigation, assembly_severity_f,
                  assembly_probability_f, assembly_hri_f, system_effect,
                  system_severity, system_probability, system_hri,
                  system_mitigation, system_severity_f, system_probability_f,
                  system_hri_f, remarks, function_1, function_2, function_3,
                  function_4, function_5, result_1, result_2, result_3,
                  result_4, result_5, user_blob_1, user_blob_2, user_blob_3,
                  user_float_1, user_float_2, user_float_3, user_int_1,
                  user_int_2, user_int_3)
        :rtype: tuple
        """

        _values = (self.hardware_id, self.hazard_id, self.potential_hazard,
                   self.potential_cause, self.assembly_effect,
                   self.assembly_severity, self.assembly_probability,
                   self.assembly_hri, self.assembly_mitigation,
                   self.assembly_severity_f, self.assembly_probability_f,
                   self.assembly_hri_f, self.system_effect,
                   self.system_severity, self.system_probability,
                   self.system_hri, self.system_mitigation,
                   self.system_severity_f, self.system_probability_f,
                   self.system_hri_f, self.remarks, self.function_1,
                   self.function_2, self.function_3, self.function_4,
                   self.function_5, self.result_1, self.result_2,
                   self.result_3, self.result_4, self.result_5,
                   self.user_blob_1, self.user_blob_2, self.user_blob_3,
                   self.user_float_1, self.user_float_2, self.user_float_3,
                   self.user_int_1, self.user_int_2, self.user_int_3)

        return _values

    def calculate(self):
        """
        Calculate the initial assembly hazard risk index (HRI), the final
        assembly HRI, the initial system HRI, and the final system HRI.

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

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar dicHazard: Dictionary of the Hazard data models managed.  Key is the Hardware ID; value is a pointer to the Hazard data model instance.
    """

    def __init__(self):
        """
        Initializes an Hazard data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None

        # Initialize public dictionary attributes.
        self.dicHazard = {}

    def request_hazard(self, dao):
        """
        Reads the RTK Project database and loads all the Hazard.  For each
        Hazard returned:

        #. Retrieve the Hazard from the RTK Project database.
        #. Create an Hazard data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Hardware being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

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
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

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
        Adds a potential hazard to a hardware item.

        :param int hardware_id: the Hardware ID to add the hazard to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO rtk_hazard \
                  (fld_hardware_id) \
                  VALUES({0:d})".format(hardware_id)
        (_results, _error_code, _last_id) = self._dao.execute(_query,
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
        Deletes a potential hazard from the RTK Project database.

        :param int hazard_id: the Hazard ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_hazard \
                  WHERE fld_hazard_id={0:d}".format(hazard_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)
        try:
            self.dicHazard.pop((hardware_id, hazard_id))
        except KeyError:
            _error_code = 60

        return(_results, _error_code)

    def calculate_hazard(self, hardware_id, hazard_id):
        """
        Calculates hazard risk index (HRI) and user-defined calculations for a
        Hazard.

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
        Saves the Hazard attributes to the RTK Project database.

        :param int hardware_id: the ID of the hardware to save.
        :param int hazard_id: the ID of the hazard to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _hazard = self.dicHazard[(hardware_id, hazard_id)]

        _query = "UPDATE rtk_hazard \
                  SET fld_potential_hazard='{0:s}', \
                      fld_potential_cause='{1:s}', \
                      fld_assembly_effect='{2:s}', fld_assembly_severity={3:d}, \
                      fld_assembly_probability={4:d}, fld_assembly_hri={5:d}, \
                      fld_assembly_mitigation='{6:s}', \
                      fld_assembly_severity_f={7:d}, \
                      fld_assembly_probability_f={8:d}, \
                      fld_assembly_hri_f={9:d}, fld_system_effect='{10:s}', \
                      fld_system_severity={11:d}, fld_system_probability={12:d}, \
                      fld_system_hri={13:d}, fld_system_mitigation='{14:s}', \
                      fld_system_severity_f={15:d}, \
                      fld_system_probability_f={16:d}, fld_system_hri_f={17:d}, \
                      fld_remarks='{18:s}', fld_function_1='{19:s}', \
                      fld_function_2='{20:s}', fld_function_3='{21:s}', \
                      fld_function_4='{22:s}', fld_function_5='{23:s}', \
                      fld_result_1={24:f}, fld_result_2={25:f}, fld_result_3={26:f}, \
                      fld_result_4={27:f}, fld_result_5={28:f}, \
                      fld_user_blob_1='{29:s}', fld_user_blob_2='{30:s}', \
                      fld_user_blob_3='{31:s}', fld_user_float_1={32:f}, \
                      fld_user_float_2={33:f}, fld_user_float_3={34:f}, \
                      fld_user_int_1={35:d}, fld_user_int_2={36:d}, \
                      fld_user_int_3={37:d} \
                  WHERE fld_hazard_id={38:d}".format(
                      _hazard.potential_hazard, _hazard.potential_cause,
                      _hazard.assembly_effect, _hazard.assembly_severity,
                      _hazard.assembly_probability, _hazard.assembly_hri,
                      _hazard.assembly_mitigation, _hazard.assembly_severity_f,
                      _hazard.assembly_probability_f, _hazard.assembly_hri_f,
                      _hazard.system_effect, _hazard.system_severity,
                      _hazard.system_probability, _hazard.system_hri,
                      _hazard.system_mitigation, _hazard.system_severity_f,
                      _hazard.system_probability_f, _hazard.system_hri_f,
                      _hazard.remarks, _hazard.function_1, _hazard.function_2,
                      _hazard.function_3, _hazard.function_4,
                      _hazard.function_5, _hazard.result_1, _hazard.result_2,
                      _hazard.result_3, _hazard.result_4, _hazard.result_5,
                      _hazard.user_blob_1, _hazard.user_blob_2,
                      _hazard.user_blob_3, _hazard.user_float_1,
                      _hazard.user_float_2, _hazard.user_float_3,
                      _hazard.user_int_1, _hazard.user_int_2,
                      _hazard.user_int_3, _hazard.hazard_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_hazards(self):
        """
        Saves all Hazard data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _hazard in self.dicHazard.values():
            (_results, _error_code) = self.save_hazard(_hazard.hardware_id,
                                                       _hazard.hazard_id)

        return False
