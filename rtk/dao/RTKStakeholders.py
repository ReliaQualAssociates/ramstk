#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKStakeholders.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKStakeholders Table
==============================
"""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
try:
    import Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


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
        Stakeholders to retrieve the current values of the RTKStakeholders data model
        attributes.

        :return: (stakeholders_id, stakeholder)
        :rtype: tuple
        """

        _values = (self.stakeholders_id, self.stakeholder)

        return _values

    def set_attributes(self, attributes):
        """
        Stakeholders to set the current values of the RTKStakeholders data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKStakeholders {0:d} attributes.". \
            format(self.stakeholders_id)

        try:
            self.stakeholder = str(attributes[0])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKStakeholders.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKStakeholders attributes."

        return _error_code, _msg
