# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKStakeholders.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKStakeholders Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String        # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKStakeholders(RTK_BASE):
    """
    Class to represent the table rtk_stakeholders in the RTK Common database.
    """

    __tablename__ = 'rtk_stakeholders'
    __table_args__ = {'extend_existing': True}

    stakeholders_id = Column('fld_stakeholders_id', Integer, primary_key=True,
                             autoincrement=True, nullable=False)
    stakeholder = Column('fld_stakeholder', String(512), default='Stakeholder')

    def get_attributes(self):
        """
        Stakeholders to retrieve the current values of the RTKStakeholders data
        model attributes.

        :return: (stakeholders_id, stakeholder)
        :rtype: tuple
        """

        _values = (self.stakeholders_id, self.stakeholder)

        return _values

    def set_attributes(self, attributes):
        """
        Stakeholders to set the current values of the RTKStakeholders data
        model attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKStakeholders {0:d} attributes.". \
            format(self.stakeholders_id)

        try:
            self.stakeholder = str(none_to_default(attributes[0],
                                                   'Stakeholder'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKStakeholders.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKStakeholders attributes."

        return _error_code, _msg
