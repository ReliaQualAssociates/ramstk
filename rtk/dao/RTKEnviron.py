# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKEnviron.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKEnviron Table
===============================================================================
"""

from sqlalchemy import Column, Float, \
                       Integer, String              # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKEnviron(RTK_BASE):
    """
    Class to represent the table rtk_environ in the RTK Common database.
    """

    __tablename__ = 'rtk_environ'
    __table_args__ = {'extend_existing': True}

    environ_id = Column('fld_environ_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    code = Column('fld_code', String(256), default='Environ Code')
    description = Column('fld_description', String(512),
                         default='Environ Description')
    environ_type = Column('fld_type', Integer, default='unknown')
    pi_e = Column('fld_pi_e', Float, default=1.0)
    # pylint: disable=invalid-name
    do = Column('fld_do', Float, default=1.0)

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKEnviron data model
        attributes.

        :return: (environs_id, code, description, environ_type, pi_e, do)
        :rtype: tuple
        """

        _values = (self.environ_id, self.code, self.description,
                   self.environ_type, self.pi_e, self.do)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKEnviron data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKEnviron {0:d} attributes.". \
            format(self.environ_id)

        try:
            self.code = str(none_to_default(attributes[0], 'Environ Code'))
            self.description = str(none_to_default(attributes[1],
                                                   'Environ Description'))
            self.environ_type = str(none_to_default(attributes[2], 'unknown'))
            self.pi_e = float(none_to_default(attributes[3], 1.0))
            self.do = float(none_to_default(attributes[4], 1.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKEnviron.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKEnviron attributes."

        return _error_code, _msg
