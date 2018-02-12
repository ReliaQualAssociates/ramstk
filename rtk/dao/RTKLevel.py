# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKLevel.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKLevel Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKLevel(RTK_BASE):
    """
    Class to represent the table rtk_level in the RTK Common database.
    """

    __tablename__ = 'rtk_level'
    __table_args__ = {'extend_existing': True}

    level_id = Column(
        'fld_level_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Level Description')
    level_type = Column('fld_type', String(256), default='')
    value = Column('fld_value', Integer, default=0)

    def get_attributes(self):
        """
        Level to retrieve the current values of the RTKLevel data model
        attributes.

        :return: (level_id, description, level_type, value)
        :rtype: tuple
        """

        _values = (self.level_id, self.description, self.level_type,
                   self.value)

        return _values

    def set_attributes(self, attributes):
        """
        Level to set the current values of the RTKLevel data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKLevel {0:d} attributes.". \
            format(self.level_id)

        try:
            self.description = str(
                none_to_default(attributes[0], 'Level Description'))
            self.level_type = str(none_to_default(attributes[1], ''))
            self.value = int(none_to_default(attributes[2], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKLevel.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKLevel attributes."

        return _error_code, _msg
