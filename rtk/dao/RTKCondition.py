# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCondition.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKCondition Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKCondition(RTK_BASE):
    """
    Class to represent the table rtk_condition in the RTK Common database.
    """

    __tablename__ = 'rtk_condition'
    __table_args__ = {'extend_existing': True}

    condition_id = Column(
        'fld_condition_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Condition Decription')
    cond_type = Column('fld_type', String(256), default='')

    def get_attributes(self):
        """
        Condition to retrieve the current values of the RTKCondition data model
        attributes.

        :return: (condition_id, description, cond_type)
        :rtype: tuple
        """

        _values = (self.condition_id, self.description, self.cond_type)

        return _values

    def set_attributes(self, attributes):
        """
        Condition to set the current values of the RTKCondition data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCondition {0:d} attributes.". \
            format(self.condition_id)

        try:
            self.description = str(
                none_to_default(attributes[0], 'Condition Description'))
            self.cond_type = str(none_to_default(attributes[1], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCondition.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCondition attributes."

        return _error_code, _msg
