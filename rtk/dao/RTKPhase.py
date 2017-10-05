# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKPhase.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKPhase Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String      # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKPhase(RTK_BASE):
    """
    Class to represent the table rtk_phase in the RTK Common database.
    """

    __tablename__ = 'rtk_phase'
    __table_args__ = {'extend_existing': True}

    phase_id = Column('fld_phase_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Phase Description')
    phase_type = Column('fld_type', Integer, default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKPhase data model
        attributes.

        :return: (phase_id, description, phase_type)
        :rtype: tuple
        """

        _values = (self.phase_id, self.description, self.phase_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKPhase data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKPhase {0:d} attributes.". \
            format(self.phase_id)

        try:
            self.description = str(none_to_default(attributes[0],
                                                   'Phase Description'))
            self.phase_type = str(none_to_default(attributes[1], 'unknown'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKPhase.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKPhase attributes."

        return _error_code, _msg
