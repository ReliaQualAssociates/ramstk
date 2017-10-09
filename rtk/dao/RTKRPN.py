# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRPN.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKRPN Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String        # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKRPN(RTK_BASE):
    """
    Class to represent the table rtk_rpn in the RTK Common database.
    """

    __tablename__ = 'rtk_rpn'
    __table_args__ = {'extend_existing': True}

    rpn_id = Column('fld_rpn_id', Integer, primary_key=True,
                    autoincrement=True, nullable=False)
    name = Column('fld_name', String(512), default='RPN Name')
    description = Column('fld_description', String(512),
                         default='RPN Description')
    rpn_type = Column('fld_type', String(256), default='')
    value = Column('fld_value', Integer, default=0)

    def get_attributes(self):
        """
        RPN to retrieve the current values of the RTKRPN data
        model attributes.

        :return: (rpn_id, name, description, rpn_type, value)
        :rtype: tuple
        """

        _values = (self.rpn_id, self.name, self.description, self.rpn_type,
                   self.value)

        return _values

    def set_attributes(self, attributes):
        """
        RPN to set the current values of the RTKRPN data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKRPN {0:d} attributes.". \
            format(self.rpn_id)

        try:
            self.name = str(none_to_default(attributes[0], 'RPN Name'))
            self.description = str(none_to_default(attributes[1],
                                                   'RPN Description'))
            self.rpn_type = str(none_to_default(attributes[2], ''))
            self.value = int(none_to_default(attributes[3], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKRPN.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKRPN attributes."

        return _error_code, _msg
