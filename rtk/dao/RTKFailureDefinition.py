# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKFailureDefinition.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKFailureDefinition Table
===============================================================================
"""

from sqlalchemy import BLOB, Column, \
                       ForeignKey, Integer          # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKFailureDefinition(RTK_BASE):
    """
    Class to represent the rtk_failure_definition table in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_failure_definition'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    definition_id = Column('fld_definition_id', Integer, primary_key=True,
                           autoincrement=True, nullable=False)

    definition = Column('fld_definition', BLOB, default='Failure Definition')

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='failures')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKFailureDefinition data
        model attributes.

        :return: (revision_id, definition_id, definition)
        :rtype: (int, int, str)
        """

        _values = (self.revision_id, self.definition_id, self.definition)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKFailureDefinition data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return:
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKFailureDefinition {0:d} attributes.".\
            format(self.definition_id)

        try:
            self.definition = str(none_to_default(attributes[0],
                                                  'Failure Definition'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKFailureDefinition.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKFailureDefinition attributes."

        return _error_code, _msg
