#!/usr/bin/env python
"""
################################
Similar Item Package Data Module
################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.SimilarItem.py is part of The RTK Project
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
    The Similar Item data model contains the attributes and methods of an
    similar item analysis.  The attributes of a Similar Item are:

    :ivar hardware_id: default value: None
    """

    def __init__(self):
        """
        Initializes an Similar Item data model instance.
        """

        # Initialize private dict attributes.
        self._quality_convert = {(1, 1):1.0, (1, 2):0.8, (1, 3):0.5,
                                 (1, 4):0.2, (2, 1):1.3, (2, 2):1.0,
                                 (2, 3):0.6, (2, 4):0.3, (3, 1):2.0,
                                 (3, 2):1.7, (3, 3):1.0, (3, 4):0.4,
                                 (4, 1):5.0, (4, 2):3.3, (4, 3):2.5,
                                 (4, 4):1.0}
        self._environment_convert = {(1, 1):1.0, (1, 2):0.2, (1, 3):0.3,
                                     (1, 4):0.3, (1, 5):0.1, (1, 6):1.1,
                                     (2, 1):5.0, (2, 2):1.0, (2, 3):1.4,
                                     (2, 4):1.4, (2, 5):0.5, (2, 6):5.0,
                                     (3, 1):3.3, (3, 2):0.7, (3, 3):1.0,
                                     (3, 4):1.0, (3, 5):0.3, (3, 6):3.3,
                                     (4, 1):3.3, (4, 2):0.7, (4, 3):1.0,
                                     (4, 4):1.0, (4, 5):0.3, (4, 6):3.3,
                                     (5, 1):10.0, (5, 2):2.0, (5, 3):3.3,
                                     (5, 4):3.3, (5, 5):1.0, (5, 6):10.0,
                                     (6, 1):0.9, (6, 2):0.2, (6, 3):0.3,
                                     (6, 4):0.3, (6, 5):0.1, (6, 6):1.0}
        self._temperature_convert = {(10.0, 10.0):1.0, (10.0, 20.0):0.9,
                                     (10.0, 30.0):0.8, (10.0, 40.0):0.8,
                                     (10.0, 50.0):0.7, (10.0, 60.0):0.5,
                                     (10.0, 70.0):0.4, (20.0, 10.0):1.1,
                                     (20.0, 20.0):1.0, (20.0, 30.0):0.9,
                                     (20.0, 40.0):0.8, (20.0, 50.0):0.7,
                                     (20.0, 60.0):0.6, (20.0, 70.0):0.5,
                                     (30.0, 10.0):1.2, (30.0, 20.0):1.1,
                                     (30.0, 30.0):1.0, (30.0, 40.0):0.9,
                                     (30.0, 50.0):0.8, (30.0, 60.0):0.6,
                                     (30.0, 70.0):0.5, (40.0, 10.0):1.3,
                                     (40.0, 20.0):1.2, (40.0, 30.0):1.1,
                                     (40.0, 40.0):1.0, (40.0, 50.0):0.9,
                                     (40.0, 60.0):0.7, (40.0, 70.0):0.6,
                                     (50.0, 10.0):1.5, (50.0, 20.0):1.4,
                                     (50.0, 30.0):1.2, (50.0, 40.0):1.1,
                                     (50.0, 50.0):1.0, (50.0, 60.0):0.8,
                                     (50.0, 70.0):0.7, (60.0, 10.0):1.9,
                                     (60.0, 20.0):1.7, (60.0, 30.0):1.6,
                                     (60.0, 40.0):1.5, (60.0, 50.0):1.2,
                                     (60.0, 60.0):1.0, (60.0, 70.0):0.8,
                                     (70.0, 10.0):2.4, (70.0, 20.0):2.2,
                                     (70.0, 30.0):1.9, (70.0, 40.0):1.8,
                                     (70.0, 50.0):1.5, (70.0, 60.0):1.2,
                                     (70.0, 70.0):1.0}

        # Initialize public scalar attributes.
        self.hardware_id = None
        self.sia_id = None
        self.from_quality = 0
        self.to_quality = 0
        self.from_environment = 0
        self.to_environment = 0
        self.from_temperature = 30.0
        self.to_temperature = 30.0
        self.change_desc_1 = 'No changes'
        self.change_factor_1 = 1.0
        self.change_desc_2 = 'No changes'
        self.change_factor_2 = 1.0
        self.change_desc_3 = 'No changes'
        self.change_factor_3 = 1.0
        self.change_desc_4 = 'No changes'
        self.change_factor_4 = 1.0
        self.change_desc_5 = 'No changes'
        self.change_factor_5 = 1.0
        self.change_desc_6 = 'No changes'
        self.change_factor_6 = 1.0
        self.change_desc_7 = 'No changes'
        self.change_factor_7 = 1.0
        self.change_desc_8 = 'No changes'
        self.change_factor_8 = 1.0
        self.change_desc_9 = 'No changes'
        self.change_factor_9 = 1.0
        self.change_desc_10 = 'No changes'
        self.change_factor_10 = 1.0
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
        self.user_blob_1 = None
        self.user_blob_2 = None
        self.user_blob_3 = None
        self.user_blob_4 = None
        self.user_blob_5 = None
        self.user_float_1 = 0.0
        self.user_float_2 = 0.0
        self.user_float_3 = 0.0
        self.user_float_4 = 0.0
        self.user_float_5 = 0.0
        self.user_int_1 = 0
        self.user_int_2 = 0
        self.user_int_3 = 0
        self.user_int_4 = 0
        self.user_int_5 = 0
        self.parent_id = 0

    def set_attributes(self, values):
        """
        Sets the Similar Item data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.hardware_id = int(values[0])
            self.sia_id = int(values[1])
            self.from_quality = int(values[2])
            self.to_quality = int(values[3])
            self.from_environment = int(values[4])
            self.to_environment = int(values[5])
            self.from_temperature = float(values[6])
            self.to_temperature = float(values[7])
            self.change_desc_1 = str(values[8])
            self.change_factor_1 = float(values[9])
            self.change_desc_2 = str(values[10])
            self.change_factor_2 = float(values[11])
            self.change_desc_3 = str(values[12])
            self.change_factor_3 = float(values[13])
            self.change_desc_4 = str(values[14])
            self.change_factor_4 = float(values[15])
            self.change_desc_5 = str(values[16])
            self.change_factor_5 = float(values[17])
            self.change_desc_6 = str(values[18])
            self.change_factor_6 = float(values[19])
            self.change_desc_7 = str(values[20])
            self.change_factor_7 = float(values[21])
            self.change_desc_8 = str(values[22])
            self.change_factor_8 = float(values[23])
            self.change_desc_9 = str(values[24])
            self.change_factor_9 = float(values[25])
            self.change_desc_10 = str(values[26])
            self.change_factor_10 = float(values[27])
            self.function_1 = str(values[28])
            self.function_2 = str(values[29])
            self.function_3 = str(values[30])
            self.function_4 = str(values[31])
            self.function_5 = str(values[32])
            self.result_1 = float(values[33])
            self.result_2 = float(values[34])
            self.result_3 = float(values[35])
            self.result_4 = float(values[36])
            self.result_5 = float(values[37])
            self.user_blob_1 = str(values[38])
            self.user_blob_2 = str(values[39])
            self.user_blob_3 = str(values[40])
            self.user_blob_4 = str(values[41])
            self.user_blob_5 = str(values[42])
            self.user_float_1 = float(values[43])
            self.user_float_2 = float(values[44])
            self.user_float_3 = float(values[45])
            self.user_float_4 = float(values[46])
            self.user_float_5 = float(values[47])
            self.user_int_1 = int(values[48])
            self.user_int_2 = int(values[49])
            self.user_int_3 = int(values[50])
            self.user_int_4 = int(values[51])
            self.user_int_5 = int(values[52])
            self.parent_id = int(values[53])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Similar Item data model attributes.

        :return: (hardware_id, sia_id, from_quality, to_quality,
                  from_environment, to_environment, from_temperature,
                  to_temperature, change_desc_1, change_factor_1,
                  change_desc_2, change_factor_2, change_desc_3,
                  change_factor_3, change_desc_4, change_factor_4,
                  change_desc_5, change_factor_5, change_desc_6,
                  change_factor_6, change_desc_7, change_factor_7,
                  change_desc_8, change_factor_8, change_desc_9,
                  change_factor_9, change_desc_10, change_factor_10,
                  function_1, function_2, function_3, function_4, function_5,
                  result_1, result_2, result_3, result_4, result_5,
                  user_blob_1, user_blob_2, user_blob_3, user_blob_4,
                  user_blob_5, user_float_1, user_float_2, user_float_3,
                  user_float_4, user_float_5, user_int_1, user_int_2,
                  user_int_3, user_int_4, user_int_5, parent_id)
        :rtype: tuple
        """

        _values = (self.hardware_id, self.sia_id, self.from_quality,
                   self.to_quality, self.from_environment, self.to_environment,
                   self.from_temperature, self.to_temperature,
                   self.change_desc_1, self.change_factor_1,
                   self.change_desc_2, self.change_factor_2,
                   self.change_desc_3, self.change_factor_3,
                   self.change_desc_4, self.change_factor_4,
                   self.change_desc_5, self.change_factor_5,
                   self.change_desc_6, self.change_factor_6,
                   self.change_desc_7, self.change_factor_7,
                   self.change_desc_8, self.change_factor_8,
                   self.change_desc_9, self.change_factor_9,
                   self.change_desc_10, self.change_factor_10,
                   self.function_1, self.function_2, self.function_3,
                   self.function_4, self.function_5, self.result_1,
                   self.result_2, self.result_3, self.result_4, self.result_5,
                   self.user_blob_1, self.user_blob_2, self.user_blob_3,
                   self.user_blob_4, self.user_blob_5, self.user_float_1,
                   self.user_float_2, self.user_float_3, self.user_float_4,
                   self.user_float_5, self.user_int_1, self.user_int_2,
                   self.user_int_3, self.user_int_4, self.user_int_5,
                   self.parent_id)

        return _values

    def topic_633(self, hazard_rate):
        """
        Calculates the similar item analysis using the approach found in The
        Reliability Toolkit: Commercial Practices Edition, Topic 6.3.3.

        :param float hazard_rate: the current hazard rate of the hardware item
                                  being calculated.
        :return: False on success or True if an error is encountered.
        :rtype: bool
        """

        self.from_temperature = round(self.from_temperature / 10.0) * 10.0
        self.to_temperature = round(self.to_temperature / 10.0) * 10.0

        try:
            self.change_factor_1 = self._quality_convert[(self.from_quality,
                                                          self.to_quality)]
        except KeyError:
            self.change_factor_1 = 1.0

        try:
            self.change_factor_2 = self._environment_convert[(self.from_environment,
                                                              self.to_environment)]
        except KeyError:
            self.change_factor_2 = 1.0
        try:
            self.change_factor_3 = self._temperature_convert[(self.from_temperature,
                                                              self.to_temperature)]
        except KeyError:
            self.change_factor_3 = 1.0

        self.result_1 = hazard_rate / (self.change_factor_1 * \
                                       self.change_factor_2 * \
                                       self.change_factor_3)

        return False

    def user_defined(self, hazard_rate):
        """
        Calculates the user-defined similar item analysis.

        :param float hazard_rate: the current hazard rate of the hardware item
                                  being calculated.
        :return: False on success or True if an error is encountered.
        :rtype: bool
        """

        _sia = {}

        # Get the assembly failure intensity.
        _sia['hr'] = hazard_rate

        # Get the change factor values.
        _sia['pi1'] = self.change_factor_1
        _sia['pi2'] = self.change_factor_2
        _sia['pi3'] = self.change_factor_3
        _sia['pi4'] = self.change_factor_4
        _sia['pi5'] = self.change_factor_5
        _sia['pi6'] = self.change_factor_6
        _sia['pi7'] = self.change_factor_7
        _sia['pi8'] = self.change_factor_8
        _sia['pi9'] = self.change_factor_9
        _sia['pi10'] = self.change_factor_10

        # Get the user-defined float and integer values.
        _sia['uf1'] = self.user_float_1
        _sia['uf2'] = self.user_float_2
        _sia['uf3'] = self.user_float_3
        _sia['uf4'] = self.user_float_4
        _sia['uf5'] = self.user_float_5
        _sia['ui1'] = self.user_int_1
        _sia['ui2'] = self.user_int_2
        _sia['ui3'] = self.user_int_3
        _sia['ui4'] = self.user_int_4
        _sia['ui5'] = self.user_int_5

        # Get the user-defined functions.
        _sia['equation1'] = self.function_1
        _sia['equation2'] = self.function_2
        _sia['equation3'] = self.function_3
        _sia['equation4'] = self.function_4
        _sia['equation5'] = self.function_5

        # Get the existing results.  This allows the use of the results
        # fields to be manually set to a float values by the user.
        # Essentially creating five more user-defined float values.
        _sia['res1'] = self.result_1
        _sia['res2'] = self.result_2
        _sia['res3'] = self.result_3
        _sia['res4'] = self.result_4
        _sia['res5'] = self.result_5

        _keys = _sia.keys()
        _values = _sia.values()

        for i in range(len(_keys)):
            vars()[_keys[i]] = _values[i]

        try:
            self.result_1 = eval(_sia['equation1'])
        except SyntaxError:
            self.result_1 = 0.0

        try:
            self.result_2 = eval(_sia['equation2'])
        except SyntaxError:
            self.result_2 = 0.0

        try:
            self.result_3 = eval(_sia['equation3'])
        except SyntaxError:
            self.result_3 = 0.0

        try:
            self.result_4 = eval(_sia['equation4'])
        except SyntaxError:
            self.result_4 = 0.0

        try:
            self.result_5 = eval(_sia['equation5'])
        except SyntaxError:
            self.result_5 = 0.0

        return False


class SimilarItem(object):
    """
    The SimilarItem data controller provides an interface between the
    SimilarItem data model and an RTK view model.  A single SimilarItem
    controller can manage one or more SimilarItem data models.  The attributes
    of a SimilarItem data controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar dicSimilarItem: Dictionary of the SimilarItem data models managed.  Key is the Hardware ID; value is a pointer to the SimilarItem data model instance.
    """

    def __init__(self):
        """
        Initializes an SimilarItem data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = 0

        # Initialize public dictionary attributes.
        self.dicSimilarItem = {}

    def request_similar_item(self, dao):
        """
        Reads the RTK Project database and loads all the SimilarItems.  For
        each SimilarItem returned:

        #. Retrieve the SimilarItem from the RTK Project database.
        #. Create a SimilarItem data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of SimilarItem being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        _query = "SELECT fld_hardware_id, fld_sia_id, fld_from_quality, \
                         fld_to_quality, fld_from_environment, \
                         fld_to_environment, fld_from_temperature, \
                         fld_to_temperature, fld_change_desc_1, \
                         fld_change_factor_1, fld_change_desc_2, \
                         fld_change_factor_2, fld_change_desc_3, \
                         fld_change_factor_3, fld_change_desc_4, \
                         fld_change_factor_4, fld_change_desc_5, \
                         fld_change_factor_5, fld_change_desc_6, \
                         fld_change_factor_6, fld_change_desc_7, \
                         fld_change_factor_7, fld_change_desc_8, \
                         fld_change_factor_8, fld_change_desc_9, \
                         fld_change_factor_9, fld_change_desc_10, \
                         fld_change_factor_10, fld_function_1, \
                         fld_function_2, fld_function_3, fld_function_4, \
                         fld_function_5, fld_result_1, fld_result_2, \
                         fld_result_3, fld_result_4, fld_result_5, \
                         fld_user_blob_1, fld_user_blob_2, fld_user_blob_3, \
                         fld_user_blob_4, fld_user_blob_5, fld_user_float_1, \
                         fld_user_float_2, fld_user_float_3, \
                         fld_user_float_4, fld_user_float_5, fld_user_int_1, \
                         fld_user_int_2, fld_user_int_3, fld_user_int_4, \
                         fld_user_int_5, fld_parent_id \
                  FROM rtk_similar_item"
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_similar_item = len(_results)
        except TypeError as _err:
            _n_similar_item = 0

        for i in range(_n_similar_item):
            _similar_item = Model()
            _similar_item.set_attributes(_results[i])
            self.dicSimilarItem[_similar_item.hardware_id] = _similar_item

        return(_results, _error_code)

    def add_similar_item(self, hardware_id):
        """
        Adds a record to rtk_similar_item in the open RTK Project database.

        :param int hardware_id: the Hardware ID to add to the similar item
                                analysis table.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO rtk_similar_item (fld_hardware_id) \
                  VALUES ({0:d})".format(hardware_id)
        (_results, _error_code, _sia_id) = self._dao.execute(_query,
                                                             commit=True)

        # If the new record was added successfully to the RTK Project database:
        #   1. Retrieve the ID of the newly inserted similar item record.
        #   2. Create a new Similar Item data model instance.
        #   3. Set the attributes of the new Similar Item data model instance.
        #   2. Add the new Similar Item data model to the controller
        #      dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_similar_item')[0]
            _similar_item = Model()
            _similar_item.set_attributes((hardware_id, self._last_id, 0, 0, 0,
                                          0, 30, 30.0, 'No changes', 1.0,
                                          'No changes', 1.0, 'No changes', 1.0,
                                          'No changes', 1.0, 'No changes', 1.0,
                                          'No changes', 1.0, 'No changes', 1.0,
                                          'No changes', 1.0, 'No changes', 1.0,
                                          'No changes', 1.0, '', '', '', '',
                                          '', 0.0, 0.0, 0.0, 0.0, 0.0, '', '',
                                          '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0,
                                          0, 0, 0, 0, 0, 0))
            self.dicSimilarItem[_similar_item.hardware_id] = _similar_item
# TODO: Handle errors.
        return (_results, _error_code)

    def calculate(self, hardware_id, hazard_rate, method=1):
        """
        Calculates the similar item analysis for the selected hardware item.

        :param int hardware_id: the Hardware ID to calculate the similar item
                                analysis for.
        :param float hazard_rate: the current hazard rate of the Hardware item
                                  being calculated.
        :keyword int method: the method to use for the similar item analysis.
                             * 1 = Reliability Toolkit, Topic 6.3.3
                             * 2 = User-defined
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _similar_item = self.dicSimilarItem[hardware_id]

        if method == 1:
            _similar_item.topic_633(hazard_rate)
        elif method == 2:
            _similar_item.user_defined(hazard_rate)

        return False

    def save_similar_item(self, hardware_id):
        """
        Saves the Similar Item analysis for the selected Hardware.

        :param int hardware_id: the Hardware ID to save the Similar Item
                                analysis for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _similar_item = self.dicSimilarItem[hardware_id]

        _query = "UPDATE rtk_similar_item \
                  SET fld_from_quality={0:d}, fld_to_quality={1:d}, \
                      fld_from_environment={2:d}, fld_to_environment={3:d}, \
                      fld_from_temperature={4:f}, fld_to_temperature={5:f}, \
                      fld_change_desc_1='{6:s}', fld_change_factor_1={7:f}, \
                      fld_change_desc_2='{8:s}', fld_change_factor_2={9:f}, \
                      fld_change_desc_3='{10:s}', fld_change_factor_3={11:f}, \
                      fld_change_desc_4='{12:s}', fld_change_factor_4={13:f}, \
                      fld_change_desc_5='{14:s}', fld_change_factor_5={15:f}, \
                      fld_change_desc_6='{16:s}', fld_change_factor_6={17:f}, \
                      fld_change_desc_7='{18:s}', fld_change_factor_7={19:f}, \
                      fld_change_desc_8='{20:s}', fld_change_factor_8={21:f}, \
                      fld_change_desc_9='{22:s}', fld_change_factor_9={23:f}, \
                      fld_change_desc_10='{24:s}', \
                      fld_change_factor_10={25:f}, fld_function_1='{26:s}', \
                      fld_function_2='{27:s}', fld_function_3='{28:s}', \
                      fld_function_4='{29:s}', fld_function_5='{30:s}', \
                      fld_result_1={31:f}, fld_result_2={32:f}, \
                      fld_result_3={33:f}, fld_result_4={34:f}, \
                      fld_result_5={35:f}, fld_user_blob_1='{36:s}', \
                      fld_user_blob_2='{37:s}', fld_user_blob_3='{38:s}', \
                      fld_user_blob_4='{39:s}', fld_user_blob_5='{40:s}', \
                      fld_user_float_1={41:f}, fld_user_float_2={42:f}, \
                      fld_user_float_3={43:f}, fld_user_float_4={44:f}, \
                      fld_user_float_5={45:f}, fld_user_int_1={46:d}, \
                      fld_user_int_2={47:d}, fld_user_int_3={48:d}, \
                      fld_user_int_4={49:d}, fld_user_int_5={50:d}, \
                      fld_parent_id={51:d} \
                  WHERE fld_hardware_id={52:d}".format(
                      _similar_item.from_quality, _similar_item.to_quality,
                      _similar_item.from_environment,
                      _similar_item.to_environment,
                      _similar_item.from_temperature,
                      _similar_item.to_temperature,
                      _similar_item.change_desc_1,
                      _similar_item.change_factor_1,
                      _similar_item.change_desc_2,
                      _similar_item.change_factor_2,
                      _similar_item.change_desc_3,
                      _similar_item.change_factor_3,
                      _similar_item.change_desc_4,
                      _similar_item.change_factor_4,
                      _similar_item.change_desc_5,
                      _similar_item.change_factor_5,
                      _similar_item.change_desc_6,
                      _similar_item.change_factor_6,
                      _similar_item.change_desc_7,
                      _similar_item.change_factor_7,
                      _similar_item.change_desc_8,
                      _similar_item.change_factor_8,
                      _similar_item.change_desc_9,
                      _similar_item.change_factor_9,
                      _similar_item.change_desc_10,
                      _similar_item.change_factor_10, _similar_item.function_1,
                      _similar_item.function_2, _similar_item.function_3,
                      _similar_item.function_4, _similar_item.function_5,
                      _similar_item.result_1, _similar_item.result_2,
                      _similar_item.result_3, _similar_item.result_4,
                      _similar_item.result_5, _similar_item.user_blob_1,
                      _similar_item.user_blob_2, _similar_item.user_blob_3,
                      _similar_item.user_blob_4, _similar_item.user_blob_5,
                      _similar_item.user_float_1, _similar_item.user_float_2,
                      _similar_item.user_float_3, _similar_item.user_float_4,
                      _similar_item.user_float_5, _similar_item.user_int_1,
                      _similar_item.user_int_2, _similar_item.user_int_3,
                      _similar_item.user_int_4, _similar_item.user_int_5,
                      _similar_item.parent_id, hardware_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)
        # TODO: Handle errors.
        return (_results, _error_code)

    def save_all_similar_item(self):
        """
        Saves all SimilarItem data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _similar_item in self.dicSimilarItem.values():
            (_results,
             _error_code) = self.save_similar_item(_similar_item.hardware_id)

        return False
