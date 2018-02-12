# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCriticality.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKCriticality Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKCriticality(RTK_BASE):
    """
    Class to represent the table rtk_criticality in the RTK Common database.
    """

    __tablename__ = 'rtk_criticality'
    __table_args__ = {'extend_existing': True}

    criticality_id = Column(
        'fld_criticality_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    name = Column('fld_name', String(256), default='Criticality Name')
    description = Column(
        'fld_description', String(512), default='Criticality Description')
    category = Column('fld_category', String(256), default='')
    value = Column('fld_value', Integer, default=0)

    def get_attributes(self):
        """
        Criticality to retrieve the current values of the RTKCriticality data
        model attributes.

        :return: (criticality_id, name, description, category, value)
        :rtype: tuple
        """

        _values = (self.criticality_id, self.name, self.description,
                   self.category, self.value)

        return _values

    def set_attributes(self, attributes):
        """
        Criticality to set the current values of the RTKCriticality data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCriticality {0:d} attributes.". \
            format(self.criticality_id)

        try:
            self.name = str(none_to_default(attributes[0], 'Criticality Name'))
            self.description = str(
                none_to_default(attributes[1], 'Criticality Description'))
            self.category = str(none_to_default(attributes[2], ''))
            self.value = int(none_to_default(attributes[3], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCriticality.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCriticality attributes."

        return _error_code, _msg
