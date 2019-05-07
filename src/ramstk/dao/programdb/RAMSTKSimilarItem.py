# -*- coding: utf-8 -*-
#
#       ramstk.dao.programdb.RAMSTKSimilarItem.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKSimilarItem Table."""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


# pylint: disable=R0902
class RAMSTKSimilarItem(RAMSTK_BASE):
    """
    Class to represent the ramstk_similar_item table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_hardware.
    """

    __tablename__ = 'ramstk_similar_item'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    change_description_1 = Column('fld_change_description_1', BLOB, default='')
    change_description_2 = Column('fld_change_description_2', BLOB, default='')
    change_description_3 = Column('fld_change_description_3', BLOB, default='')
    change_description_4 = Column('fld_change_description_4', BLOB, default='')
    change_description_5 = Column('fld_change_description_5', BLOB, default='')
    change_description_6 = Column('fld_change_description_6', BLOB, default='')
    change_description_7 = Column('fld_change_description_7', BLOB, default='')
    change_description_8 = Column('fld_change_description_8', BLOB, default='')
    change_description_9 = Column('fld_change_description_9', BLOB, default='')
    change_description_10 = Column(
        'fld_change_description_10', BLOB, default='')
    change_factor_1 = Column('fld_change_factor_1', Float, default=1.0)
    change_factor_2 = Column('fld_change_factor_2', Float, default=1.0)
    change_factor_3 = Column('fld_change_factor_3', Float, default=1.0)
    change_factor_4 = Column('fld_change_factor_4', Float, default=1.0)
    change_factor_5 = Column('fld_change_factor_5', Float, default=1.0)
    change_factor_6 = Column('fld_change_factor_6', Float, default=1.0)
    change_factor_7 = Column('fld_change_factor_7', Float, default=1.0)
    change_factor_8 = Column('fld_change_factor_8', Float, default=1.0)
    change_factor_9 = Column('fld_change_factor_9', Float, default=1.0)
    change_factor_10 = Column('fld_change_factor_10', Float, default=1.0)
    environment_from_id = Column('fld_environment_from_id', Integer, default=0)
    environment_to_id = Column('fld_environment_to_id', Integer, default=0)
    function_1 = Column('fld_function_1', String(128), default='')
    function_2 = Column('fld_function_2', String(128), default='')
    function_3 = Column('fld_function_3', String(128), default='')
    function_4 = Column('fld_function_4', String(128), default='')
    function_5 = Column('fld_function_5', String(128), default='')
    method_id = Column('fld_method_id', Integer, default=0)
    parent_id = Column('fld_parent_id', Integer, default=0)
    quality_from_id = Column('fld_quality_from_id', Integer, default=0)
    quality_to_id = Column('fld_quality_to_id', Integer, default=0)
    result_1 = Column('fld_result_1', Float, default=0.0)
    result_2 = Column('fld_result_2', Float, default=0.0)
    result_3 = Column('fld_result_3', Float, default=0.0)
    result_4 = Column('fld_result_4', Float, default=0.0)
    result_5 = Column('fld_result_5', Float, default=0.0)
    temperature_from = Column('fld_temperature_from', Float, default=30.0)
    temperature_to = Column('fld_temperature_to', Float, default=30.0)
    user_blob_1 = Column('fld_user_blob_1', BLOB, default='')
    user_blob_2 = Column('fld_user_blob_2', BLOB, default='')
    user_blob_3 = Column('fld_user_blob_3', BLOB, default='')
    user_blob_4 = Column('fld_user_blob_4', BLOB, default='')
    user_blob_5 = Column('fld_user_blob_5', BLOB, default='')
    user_float_1 = Column('fld_user_Float_1', Float, default=0.0)
    user_float_2 = Column('fld_user_Float_2', Float, default=0.0)
    user_float_3 = Column('fld_user_Float_3', Float, default=0.0)
    user_float_4 = Column('fld_user_Float_4', Float, default=0.0)
    user_float_5 = Column('fld_user_Float_5', Float, default=0.0)
    user_int_1 = Column('fld_user_int_1', Integer, default=0)
    user_int_2 = Column('fld_user_int_2', Integer, default=0)
    user_int_3 = Column('fld_user_int_3', Integer, default=0)
    user_int_4 = Column('fld_user_int_4', Integer, default=0)
    user_int_5 = Column('fld_user_int_5', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship('RAMSTKHardware', back_populates='sia')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKSimilarItem data model attributes.

        :return: {hardware_id, change_description_1, change_description_2,
                  change_description_3, change_description_4,
                  change_description_5, change_description_6,
                  change_description_7, change_description_8,
                  change_description_9, change_description_10, change_factor_1,
                  change_factor_2, change_factor_3, change_factor_4,
                  change_factor_5, change_factor_6, change_factor_7,
                  change_factor_8, change_factor_9, change_factor_10,
                  environment_from_id, environment_to_id, function_1,
                  function_2, function_3, function_4, function_5, method_id,
                  parent_id, quality_from_id, quality_to_id, result_1,
                  result_2, result_3, result_4, result_5, temperature_from,
                  temperature_to, user_blob_1, user_blob_2, user_blob_3,
                  user_blob_4, user_blob_5, user_float_1, user_float_2,
                  user_float_3, user_float_4, user_float_5, user_int_1,
                  user_int_2, user_int_3, user_int_4, user_int_5}
        :rtype: tuple
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'change_description_1': self.change_description_1,
            'change_description_2': self.change_description_2,
            'change_description_3': self.change_description_3,
            'change_description_4': self.change_description_4,
            'change_description_5': self.change_description_5,
            'change_description_6': self.change_description_6,
            'change_description_7': self.change_description_7,
            'change_description_8': self.change_description_8,
            'change_description_9': self.change_description_9,
            'change_description_10': self.change_description_10,
            'change_factor_1': self.change_factor_1,
            'change_factor_2': self.change_factor_2,
            'change_factor_3': self.change_factor_3,
            'change_factor_4': self.change_factor_4,
            'change_factor_5': self.change_factor_5,
            'change_factor_6': self.change_factor_6,
            'change_factor_7': self.change_factor_7,
            'change_factor_8': self.change_factor_8,
            'change_factor_9': self.change_factor_9,
            'change_factor_10': self.change_factor_10,
            'environment_from_id': self.environment_from_id,
            'environment_to_id': self.environment_to_id,
            'function_1': self.function_1,
            'function_2': self.function_2,
            'function_3': self.function_3,
            'function_4': self.function_4,
            'function_5': self.function_5,
            'method_id': self.method_id,
            'parent_id': self.parent_id,
            'quality_from_id': self.quality_from_id,
            'quality_to_id': self.quality_to_id,
            'result_1': self.result_1,
            'result_2': self.result_2,
            'result_3': self.result_3,
            'result_4': self.result_4,
            'result_5': self.result_5,
            'temperature_from': self.temperature_from,
            'temperature_to': self.temperature_to,
            'user_blob_1': self.user_blob_1,
            'user_blob_2': self.user_blob_2,
            'user_blob_3': self.user_blob_3,
            'user_blob_4': self.user_blob_4,
            'user_blob_5': self.user_blob_5,
            'user_float_1': self.user_float_1,
            'user_float_2': self.user_float_2,
            'user_float_3': self.user_float_3,
            'user_float_4': self.user_float_4,
            'user_float_5': self.user_float_5,
            'user_int_1': self.user_int_1,
            'user_int_2': self.user_int_2,
            'user_int_3': self.user_int_3,
            'user_int_4': self.user_int_4,
            'user_int_5': self.user_int_5
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the RAMSTKSimilarItem data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKSimilarItem {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.change_description_1 = str(
                none_to_default(attributes['change_description_1'], ''))
            self.change_description_2 = str(
                none_to_default(attributes['change_description_2'], ''))
            self.change_description_3 = str(
                none_to_default(attributes['change_description_3'], ''))
            self.change_description_4 = str(
                none_to_default(attributes['change_description_4'], ''))
            self.change_description_5 = str(
                none_to_default(attributes['change_description_5'], ''))
            self.change_description_6 = str(
                none_to_default(attributes['change_description_6'], ''))
            self.change_description_7 = str(
                none_to_default(attributes['change_description_7'], ''))
            self.change_description_8 = str(
                none_to_default(attributes['change_description_8'], ''))
            self.change_description_9 = str(
                none_to_default(attributes['change_description_9'], ''))
            self.change_description_10 = str(
                none_to_default(attributes['change_description_10'], ''))
            self.change_factor_1 = float(
                none_to_default(attributes['change_factor_1'], 1.0))
            self.change_factor_2 = float(
                none_to_default(attributes['change_factor_2'], 1.0))
            self.change_factor_3 = float(
                none_to_default(attributes['change_factor_3'], 1.0))
            self.change_factor_4 = float(
                none_to_default(attributes['change_factor_4'], 1.0))
            self.change_factor_5 = float(
                none_to_default(attributes['change_factor_5'], 1.0))
            self.change_factor_6 = float(
                none_to_default(attributes['change_factor_6'], 1.0))
            self.change_factor_7 = float(
                none_to_default(attributes['change_factor_7'], 1.0))
            self.change_factor_8 = float(
                none_to_default(attributes['change_factor_8'], 1.0))
            self.change_factor_9 = float(
                none_to_default(attributes['change_factor_9'], 1.0))
            self.change_factor_10 = float(
                none_to_default(attributes['change_factor_10'], 1.0))
            self.environment_from_id = int(
                none_to_default(attributes['environment_from_id'], 0))
            self.environment_to_id = int(
                none_to_default(attributes['environment_to_id'], 0))
            self.function_1 = str(
                none_to_default(attributes['function_1'], ''))
            self.function_2 = str(
                none_to_default(attributes['function_2'], ''))
            self.function_3 = str(
                none_to_default(attributes['function_3'], ''))
            self.function_4 = str(
                none_to_default(attributes['function_4'], ''))
            self.function_5 = str(
                none_to_default(attributes['function_5'], ''))
            self.method_id = int(none_to_default(attributes['method_id'], 0))
            self.parent_id = int(none_to_default(attributes['parent_id'], 0))
            self.quality_from_id = int(
                none_to_default(attributes['quality_from_id'], 0))
            self.quality_to_id = int(
                none_to_default(attributes['quality_to_id'], 0))
            self.result_1 = float(none_to_default(attributes['result_1'], 0))
            self.result_2 = float(none_to_default(attributes['result_2'], 0))
            self.result_3 = float(none_to_default(attributes['result_3'], 0))
            self.result_4 = float(none_to_default(attributes['result_4'], 0))
            self.result_5 = float(none_to_default(attributes['result_5'], 0))
            self.temperature_from = float(
                none_to_default(attributes['temperature_from'], 0))
            self.temperature_to = float(
                none_to_default(attributes['temperature_to'], 0))
            self.user_blob_1 = str(
                none_to_default(attributes['user_blob_1'], ''))
            self.user_blob_2 = str(
                none_to_default(attributes['user_blob_2'], ''))
            self.user_blob_3 = str(
                none_to_default(attributes['user_blob_3'], ''))
            self.user_blob_4 = str(
                none_to_default(attributes['user_blob_4'], ''))
            self.user_blob_5 = str(
                none_to_default(attributes['user_blob_5'], ''))
            self.user_float_1 = float(
                none_to_default(attributes['user_float_1'], 0.0))
            self.user_float_2 = float(
                none_to_default(attributes['user_float_2'], 0.0))
            self.user_float_3 = float(
                none_to_default(attributes['user_float_3'], 0.0))
            self.user_float_4 = float(
                none_to_default(attributes['user_float_4'], 0.0))
            self.user_float_5 = float(
                none_to_default(attributes['user_float_5'], 0.0))
            self.user_int_1 = int(none_to_default(attributes['user_int_1'], 0))
            self.user_int_2 = int(none_to_default(attributes['user_int_2'], 0))
            self.user_int_3 = int(none_to_default(attributes['user_int_3'], 0))
            self.user_int_4 = int(none_to_default(attributes['user_int_4'], 0))
            self.user_int_5 = int(none_to_default(attributes['user_int_5'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKSimilarItem.set_attributes().".format(str(_err))
        except ValueError as _err:
            # FIXME: Handle ValueError in RAMSTKSimilarItem.set_attrobutes().
            print(_err)

        return _error_code, _msg

    def topic_633(self, hazard_rate):
        """
        Calculate the Similar Item analysis using Topic 6.3.3 approach.

        This method calculates the new hazard rate using the approach found
        in The Reliability Toolkit: Commercial Practices Edition, Topic 6.3.3.

        :param float hazard_rate: the current hazard rate of the hardware item
                                  being calculated.
        :return: False on success or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _environment_convert = {
            (1, 1): 1.0,
            (1, 2): 0.2,
            (1, 3): 0.3,
            (1, 4): 0.3,
            (1, 5): 0.1,
            (1, 6): 1.1,
            (2, 1): 5.0,
            (2, 2): 1.0,
            (2, 3): 1.4,
            (2, 4): 1.4,
            (2, 5): 0.5,
            (2, 6): 5.0,
            (3, 1): 3.3,
            (3, 2): 0.7,
            (3, 3): 1.0,
            (3, 4): 1.0,
            (3, 5): 0.3,
            (3, 6): 3.3,
            (4, 1): 3.3,
            (4, 2): 0.7,
            (4, 3): 1.0,
            (4, 4): 1.0,
            (4, 5): 0.3,
            (4, 6): 3.3,
            (5, 1): 10.0,
            (5, 2): 2.0,
            (5, 3): 3.3,
            (5, 4): 3.3,
            (5, 5): 1.0,
            (5, 6): 10.0,
            (6, 1): 0.9,
            (6, 2): 0.2,
            (6, 3): 0.3,
            (6, 4): 0.3,
            (6, 5): 0.1,
            (6, 6): 1.0
        }
        _quality_convert = {
            (1, 1): 1.0,
            (1, 2): 0.8,
            (1, 3): 0.5,
            (1, 4): 0.2,
            (2, 1): 1.3,
            (2, 2): 1.0,
            (2, 3): 0.6,
            (2, 4): 0.3,
            (3, 1): 2.0,
            (3, 2): 1.7,
            (3, 3): 1.0,
            (3, 4): 0.4,
            (4, 1): 5.0,
            (4, 2): 3.3,
            (4, 3): 2.5,
            (4, 4): 1.0
        }
        _temperature_convert = {
            (10.0, 10.0): 1.0,
            (10.0, 20.0): 0.9,
            (10.0, 30.0): 0.8,
            (10.0, 40.0): 0.8,
            (10.0, 50.0): 0.7,
            (10.0, 60.0): 0.5,
            (10.0, 70.0): 0.4,
            (20.0, 10.0): 1.1,
            (20.0, 20.0): 1.0,
            (20.0, 30.0): 0.9,
            (20.0, 40.0): 0.8,
            (20.0, 50.0): 0.7,
            (20.0, 60.0): 0.6,
            (20.0, 70.0): 0.5,
            (30.0, 10.0): 1.2,
            (30.0, 20.0): 1.1,
            (30.0, 30.0): 1.0,
            (30.0, 40.0): 0.9,
            (30.0, 50.0): 0.8,
            (30.0, 60.0): 0.6,
            (30.0, 70.0): 0.5,
            (40.0, 10.0): 1.3,
            (40.0, 20.0): 1.2,
            (40.0, 30.0): 1.1,
            (40.0, 40.0): 1.0,
            (40.0, 50.0): 0.9,
            (40.0, 60.0): 0.7,
            (40.0, 70.0): 0.6,
            (50.0, 10.0): 1.5,
            (50.0, 20.0): 1.4,
            (50.0, 30.0): 1.2,
            (50.0, 40.0): 1.1,
            (50.0, 50.0): 1.0,
            (50.0, 60.0): 0.8,
            (50.0, 70.0): 0.7,
            (60.0, 10.0): 1.9,
            (60.0, 20.0): 1.7,
            (60.0, 30.0): 1.6,
            (60.0, 40.0): 1.5,
            (60.0, 50.0): 1.2,
            (60.0, 60.0): 1.0,
            (60.0, 70.0): 0.8,
            (70.0, 10.0): 2.4,
            (70.0, 20.0): 2.2,
            (70.0, 30.0): 1.9,
            (70.0, 40.0): 1.8,
            (70.0, 50.0): 1.5,
            (70.0, 60.0): 1.2,
            (70.0, 70.0): 1.0
        }

        # Convert user-supplied temperatures to whole values used in Topic 633.
        self.temperature_from = round(self.temperature_from / 10.0) * 10.0
        self.temperature_to = round(self.temperature_to / 10.0) * 10.0

        try:
            self.change_factor_1 = _quality_convert[(self.quality_from_id,
                                                     self.quality_to_id)]
        except KeyError:
            self.change_factor_1 = 1.0
            _return = True

        try:
            self.change_factor_2 = _environment_convert[(
                self.environment_from_id, self.environment_to_id)]
        except KeyError:
            self.change_factor_2 = 1.0
            _return = True

        try:
            self.change_factor_3 = _temperature_convert[(self.temperature_from,
                                                         self.temperature_to)]
        except KeyError:
            self.change_factor_3 = 1.0
            _return = True

        self.result_1 = hazard_rate / (
            self.change_factor_1 * self.change_factor_2 * self.change_factor_3)

        return _return

    def user_defined(self, hazard_rate):
        """
        Calculate the user-defined similar item analysis.

        :param float hazard_rate: the current hazard rate of the hardware item
                                  being calculated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Create list of safe functions.
        _safe_list = [
            'hr', 'pi1', 'pi3', 'pi3', 'pi4', 'pi5', 'pi6', 'pi7', 'pi8',
            'pi9', 'pi10', 'uf1', 'uf2', 'uf3', 'uf4', 'uf5', 'ui1', 'ui2',
            'ui3', 'ui4', 'ui5', 'equation1', 'equation2', 'equation3',
            'equation4', 'equation5', 'res1', 'res2', 'res3', 'res4', 'res5'
        ]

        # Use the list to filter the local namespace
        _sia = dict([(k, locals().get(k, None)) for k in _safe_list])

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
        # fields to be manually set to float values by the user essentially
        # creating five more user-defined float values.
        _sia['res1'] = self.result_1
        _sia['res2'] = self.result_2
        _sia['res3'] = self.result_3
        _sia['res4'] = self.result_4
        _sia['res5'] = self.result_5

        _keys = list(_sia.keys())
        _values = list(_sia.values())

        for _index, _key in enumerate(_keys):
            vars()[_key] = _values[_index]

        try:
            self.result_1 = eval(_sia['equation1'], {"__builtins__": None},
                                 _sia)
        except SyntaxError:
            self.result_1 = 0.0
            _return = True

        try:
            self.result_2 = eval(_sia['equation2'], {"__builtins__": None},
                                 _sia)
        except SyntaxError:
            self.result_2 = 0.0
            _return = True

        try:
            self.result_3 = eval(_sia['equation3'], {"__builtins__": None},
                                 _sia)
        except SyntaxError:
            self.result_3 = 0.0
            _return = True

        try:
            self.result_4 = eval(_sia['equation4'], {"__builtins__": None},
                                 _sia)
        except SyntaxError:
            self.result_4 = 0.0
            _return = True

        try:
            self.result_5 = eval(_sia['equation5'], {"__builtins__": None},
                                 _sia)
        except SyntaxError:
            self.result_5 = 0.0
            _return = True

        # If all the equations are set and _return is True, then there is a
        # real issue.  Otherwise, _return was set just because one or more
        # equations was empty and it is a false True.
        if (_return and _sia['equation1'] != '' or _sia['equation2'] != ''
                or _sia['equation3'] != '' or _sia['equation4'] != ''
                or _sia['equation5'] != ''):
            _return = False

        return _return
