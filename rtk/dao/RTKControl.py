# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKControl.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKControl Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import Column, ForeignKey, \
                       Integer, String              # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKControl(RTK_BASE):
    """
    Class to represent the table rtk_control in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_control'
    __table_args__ = {'extend_existing': True}

    mode_id = Column('fld_mode_id', Integer,
                     ForeignKey('rtk_mode.fld_mode_id'), nullable=False)
    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    control_id = Column('fld_control_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mode = relationship('RTKMode', back_populates='control')
    cause = relationship('RTKCause', back_populates='control')

    is_mode = False
    is_mechanism = False
    is_cause = False
    is_control = True
    is_action = False

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKControl data model
        attributes.

        :return: (mode_id, cause_id, control_id, description, type_id)
        :rtype: tuple
        """

        _attributes = (self.mode_id, self.cause_id, self.control_id,
                       self.description, self.type_id)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKControl data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKControl {0:d} attributes.". \
               format(self.control_id)

        try:
            self.description = str(none_to_default(attributes[0], ''))
            self.type_id = int(none_to_default(attributes[1], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKControl.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKControl attributes."

        return _error_code, _msg
