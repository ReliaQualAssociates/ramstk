#!/usr/bin/env python
"""
################################
Similar Item Package Data Module
################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.similar_item.SimilarItem.py is part of The RTK Project
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
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):                        # pylint: disable=R0902
    """
    The Similar Item data model contains the attributes and methods of an
    similar item analysis.  The attributes of a Similar Item are:

    :ivar dict _quality_convert: the dictionary of quality adjustment factors
                                 for the Topic 6.3.3 method.  Key is a tuple of
                                 indices of form (old, new).  Value is the
                                 adjustment factor.
    :ivar dict _environment_convert: the dictionary of operating environment
                                     adjustment factors for the Topic 6.3.3
                                     method.  Key is a tuple of indices of form
                                     (old, new).  Value is the adjustment
                                     factor.
    :ivar dict _temperature_convert: the dictionary of operating ambient
                                     temperature adjustment factors for the
                                     Topic 6.3.3 method.  Key is a tuple of
                                     indices of form (old, new).  Value is the
                                     adjustment factor.
    :ivar int hardware_id: the Hardware ID the Similar Item is associated with.
    :ivar int sia_id: the ID of the Similar Item.
    :ivar int from_quality: the first index (old system) in the quality key.
    :ivar int to_quality: the second index (new system) in the quality key.
    :ivar int from_environment: the first index (old system) in the operating
                                environment key.
    :ivar int to_environment: the second index (new system) in the operating
                              environment key.
    :ivar float from_temperature: the first index (old system) in the operating
                                  temperature key.
    :ivar float to_temperature: the second index (new system) in the operating
                                temperature key.
    :ivar str change_desc_1: the description of change for the first
                             user-defined change category.
    :ivar float change_factor_1: the adjustment factor for the first
                                 user-defined change category.
    :ivar str change_desc_2: the description of change for the second
                             user-defined change category.
    :ivar float change_factor_2: the adjustment factor for the second
                                 user-defined change category.
    :ivar str change_desc_3: the description of change for the third
                             user-defined change category.
    :ivar float change_factor_3: the adjustment factor for the third
                                 user-defined change category.
    :ivar str change_desc_4: the description of change for the fourth
                             user-defined change category.
    :ivar float change_factor_4: the adjustment factor for the fourth
                                 user-defined change category.
    :ivar str change_desc_5: the description of change for the fifth
                             user-defined change category.
    :ivar float change_factor_5: the adjustment factor for the fifth
                                 user-defined change category.
    :ivar str change_desc_6: the description of change for the sixth
                             user-defined change category.
    :ivar float change_factor_6: the adjustment factor for the sixth
                                 user-defined change category.
    :ivar str change_desc_7: the description of change for the seventh
                             user-defined change category.
    :ivar float change_factor_7: the adjustment factor for the seventh
                                 user-defined change category.
    :ivar str change_desc_8: the description of change for the eighth
                             user-defined change category.
    :ivar float change_factor_8: the adjustment factor for the eighth
                                 user-defined change category.
    :ivar str change_desc_9: the description of change for the ninth
                             user-defined change category.
    :ivar float change_factor_9: the adjustment factor for the ninth
                                 user-defined change category.
    :ivar str change_desc_10: the description of change for the tenth
                              user-defined change category.
    :ivar float change_factor_10: the adjustment factor for the tenth
                                 user-defined change category.
    :ivar str function_1: the first user-defined Similar Item Analysis
                          function.
    :ivar str function_2: the second user-defined Similar Item Analysis
                          function.
    :ivar str function_3: the third user-defined Similar Item Analysis
                          function.
    :ivar str function_4: the fourth user-defined Similar Item Analysis
                          function.
    :ivar str function_5: the fifth user-defined Similar Item Analysis
                          function.
    :ivar float result_1: the result of the first Similar Item Analysis.
    :ivar float result_2: the result of the second Similar Item Analysis.
    :ivar float result_3: the result of the third Similar Item Analysis.
    :ivar float result_4: the result of the fourth Similar Item Analysis.
    :ivar float result_5: the result of the fifth Similar Item Analysis.
    :ivar str user_blob_1: user-defined blob field 1.
    :ivar str user_blob_2: user-defined blob field 2.
    :ivar str user_blob_3: user-defined blob field 3.
    :ivar str user_blob_4: user-defined blob field 4.
    :ivar str user_blob_5: user-defined blob field 5.
    :ivar float user_float_1: user-defined float field 1.
    :ivar float user_float_2: user-defined float field 2.
    :ivar float user_float_3: user-defined float field 3.
    :ivar float user_float_4: user-defined float field 4.
    :ivar float user_float_5: user-defined float field 5.
    :ivar int user_int_1: user-defined integer field 1.
    :ivar int user_int_2: user-defined integer field 2.
    :ivar int user_int_3: user-defined integer field 3.
    :ivar int user_int_4: user-defined integer field 4.
    :ivar int user_int_5: user-defined integer field 5.
    :ivar int parent_id: the Hardware ID of the parent Hardware item.
    :ivar int method: the Similar Item method to use.
                        * 1 = Topic 6.3.3
                        * 2 = User-defined
    """

    def __init__(self):
        """
        Method to initialize a Similar Item data model instance.
        """

        # Define private dict attributes.
        self._quality_convert = {(1, 1): 1.0, (1, 2): 0.8, (1, 3): 0.5,
                                 (1, 4): 0.2, (2, 1): 1.3, (2, 2): 1.0,
                                 (2, 3): 0.6, (2, 4): 0.3, (3, 1): 2.0,
                                 (3, 2): 1.7, (3, 3): 1.0, (3, 4): 0.4,
                                 (4, 1): 5.0, (4, 2): 3.3, (4, 3): 2.5,
                                 (4, 4): 1.0}
        self._environment_convert = {(1, 1): 1.0, (1, 2): 0.2, (1, 3): 0.3,
                                     (1, 4): 0.3, (1, 5): 0.1, (1, 6): 1.1,
                                     (2, 1): 5.0, (2, 2): 1.0, (2, 3): 1.4,
                                     (2, 4): 1.4, (2, 5): 0.5, (2, 6): 5.0,
                                     (3, 1): 3.3, (3, 2): 0.7, (3, 3): 1.0,
                                     (3, 4): 1.0, (3, 5): 0.3, (3, 6): 3.3,
                                     (4, 1): 3.3, (4, 2): 0.7, (4, 3): 1.0,
                                     (4, 4): 1.0, (4, 5): 0.3, (4, 6): 3.3,
                                     (5, 1): 10.0, (5, 2): 2.0, (5, 3): 3.3,
                                     (5, 4): 3.3, (5, 5): 1.0, (5, 6): 10.0,
                                     (6, 1): 0.9, (6, 2): 0.2, (6, 3): 0.3,
                                     (6, 4): 0.3, (6, 5): 0.1, (6, 6): 1.0}
        self._temperature_convert = {(10.0, 10.0): 1.0, (10.0, 20.0): 0.9,
                                     (10.0, 30.0): 0.8, (10.0, 40.0): 0.8,
                                     (10.0, 50.0): 0.7, (10.0, 60.0): 0.5,
                                     (10.0, 70.0): 0.4, (20.0, 10.0): 1.1,
                                     (20.0, 20.0): 1.0, (20.0, 30.0): 0.9,
                                     (20.0, 40.0): 0.8, (20.0, 50.0): 0.7,
                                     (20.0, 60.0): 0.6, (20.0, 70.0): 0.5,
                                     (30.0, 10.0): 1.2, (30.0, 20.0): 1.1,
                                     (30.0, 30.0): 1.0, (30.0, 40.0): 0.9,
                                     (30.0, 50.0): 0.8, (30.0, 60.0): 0.6,
                                     (30.0, 70.0): 0.5, (40.0, 10.0): 1.3,
                                     (40.0, 20.0): 1.2, (40.0, 30.0): 1.1,
                                     (40.0, 40.0): 1.0, (40.0, 50.0): 0.9,
                                     (40.0, 60.0): 0.7, (40.0, 70.0): 0.6,
                                     (50.0, 10.0): 1.5, (50.0, 20.0): 1.4,
                                     (50.0, 30.0): 1.2, (50.0, 40.0): 1.1,
                                     (50.0, 50.0): 1.0, (50.0, 60.0): 0.8,
                                     (50.0, 70.0): 0.7, (60.0, 10.0): 1.9,
                                     (60.0, 20.0): 1.7, (60.0, 30.0): 1.6,
                                     (60.0, 40.0): 1.5, (60.0, 50.0): 1.2,
                                     (60.0, 60.0): 1.0, (60.0, 70.0): 0.8,
                                     (70.0, 10.0): 2.4, (70.0, 20.0): 2.2,
                                     (70.0, 30.0): 1.9, (70.0, 40.0): 1.8,
                                     (70.0, 50.0): 1.5, (70.0, 60.0): 1.2,
                                     (70.0, 70.0): 1.0}

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
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
        self.method = 0

    def set_attributes(self, values):
        """
        Method to set the Similar Item data model attributes.

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
            self.method = int(values[54])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Similar Item data model
        attributes.

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
                  user_int_3, user_int_4, user_int_5, parent_id, method)
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
                   self.parent_id, self.method)

        return _values

    def topic_633(self, hazard_rate):
        """
        Method to calculate the Similar Item analysis using the approach found
        in The Reliability Toolkit: Commercial Practices Edition, Topic 6.3.3.

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
            self.change_factor_2 = self._environment_convert[
                (self.from_environment, self.to_environment)]
        except KeyError:
            self.change_factor_2 = 1.0
        try:
            self.change_factor_3 = self._temperature_convert[
                (self.from_temperature, self.to_temperature)]
        except KeyError:
            self.change_factor_3 = 1.0

        self.result_1 = hazard_rate / (self.change_factor_1 *
                                       self.change_factor_2 *
                                       self.change_factor_3)

        return False

    def user_defined(self, hazard_rate):
        """
        Method to calculate the user-defined similar item analysis.

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

        for _index, _key in enumerate(_keys):
            vars()[_key] = _values[_index]

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

    :ivar dao: the Data Access Object to use when communicating with the RTK
               Project database.
    :ivar dicSimilarItem: Dictionary of the SimilarItem data models managed.
                          Key is the Hardware ID; value is a pointer to the
                          SimilarItem data model instance.
    """

    def __init__(self):
        """
        Method to initialize a SimilarItem data controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._last_id = 0

        # Define public dictionary attributes.
        self.dicSimilarItem = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.dao = None

    def request_similar_item(self):
        """
        Method to read the RTK Project database and loads all the SimilarItems.
        For each SimilarItem returned:

        #. Retrieve the SimilarItem from the RTK Project database.
        #. Create a SimilarItem data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of SimilarItem being managed
           by this controller.

        :return: (_results, _error_code)
        :rtype: tuple
        """

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
                         fld_user_int_5, fld_parent_id, fld_method \
                  FROM rtk_similar_item"
        (_results, _error_code, __) = self.dao.execute(_query, commit=False)

        try:
            _n_similar_item = len(_results)
        except TypeError:
            _n_similar_item = 0

        for i in range(_n_similar_item):
            _similar_item = Model()
            _similar_item.set_attributes(_results[i])
            self.dicSimilarItem[_similar_item.hardware_id] = _similar_item

        return(_results, _error_code)

    def add_similar_item(self, hardware_id, parent_id):
        """
        Method to add a record to rtk_similar_item in the open RTK Project
        database.

        :param int hardware_id: the Hardware ID to add to the similar item
                                analysis table.
        :param int parent_id: the Hardware ID of the parent Hardware item.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO rtk_similar_item \
                  (fld_hardware_id, fld_parent_id) \
                  VALUES ({0:d}, {1:d})".format(hardware_id, parent_id)
        (_results, _error_code, _sia_id) = self.dao.execute(_query,
                                                            commit=True)

        # If the new record was added successfully to the RTK Project database:
        #   1. Retrieve the ID of the newly inserted similar item record.
        #   2. Create a new Similar Item data model instance.
        #   3. Set the attributes of the new Similar Item data model instance.
        #   4. Add the new Similar Item data model to the controller
        #      dictionary.
        if _error_code == 0:
            self._last_id = _sia_id
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
                                          0, 0, 0, 0, 0, parent_id))
            self.dicSimilarItem[_similar_item.hardware_id] = _similar_item

        return (_results, _error_code)

    def delete_similar_item(self, hardware_id):
        """
        Method to delete a Similar Item data model instance from the dictionary
        of models controlled by an instance of the Similar Item data
        controller.

        :param int hardware_id: the hardware ID of the Similar Item to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.dicSimilarItem.pop(hardware_id)

        return False

    def calculate(self, hardware_id, hazard_rate, method=1):
        """
        Method to calculate the similar item analysis for the selected Hardware
        item.

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

        if _similar_item.method == 0:
            _similar_item.method = method

        return False

    def save_similar_item(self, hardware_id):
        """
        Method to save the Similar Item analysis for the selected Hardware.

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
                      fld_parent_id={51:d}, fld_method={52:d} \
                  WHERE fld_hardware_id={53:d}".format(
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
                      _similar_item.parent_id, _similar_item.method,
                      hardware_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return (_results, _error_code)

    def save_all_similar_item(self):
        """
        Method to save all SimilarItem data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_codes = []

        for _similar_item in self.dicSimilarItem.values():
            (_results,
             _error_code) = self.save_similar_item(_similar_item.hardware_id)
            _error_codes.append((_similar_item.hardware_id, _error_code))

        return _error_codes
