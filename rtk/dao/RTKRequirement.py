#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRequirement.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKRequirement Table
==============================
"""

from datetime import date

# Import the database models.
from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKRequirement(RTK_BASE):
    """
    Class to represent the rtk_requirement table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_requirement'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    requirement_id = Column('fld_requirement_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)

    derived = Column('fld_derived', Integer, default=0)
    description = Column('fld_description', BLOB, default='')
    figure_number = Column('fld_figure_number', String(256), default='')
    owner_id = Column('fld_owner_id', Integer, default=0)
    page_number = Column('fld_page_number', String(256), default='')
    parent_id = Column('fld_parent_id', Integer, default=0)
    priority = Column('fld_priority', Integer, default=0)
    requirement_code = Column('fld_requirement_code', String(256), default='')
    specification = Column('fld_specification', String(256), default='')
    type_id = Column('fld_type_id', Integer, default=0)
    validated = Column('fld_validated', Integer, default=0)
    validated_date = Column('fld_validated_date', Date,
                            default=date.today())

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='requirement')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Requirement data model
        attributes.

        :return: (revsion_id, requirement_id, description, requirement_code,
                  requirement_type, priority, specification, page_number,
                  figure_number, derived, owner, validated, validated_date,
                  parent_id)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.requirement_id, self.derived,
                       self.description, self.figure_number, self.owner_id,
                       self.page_number, self.parent_id, self.priority,
                       self.requirement_code, self.specification,
                       self.type_id, self.validated, self.validated_date)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the Requirement data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKRequirement {0:d} attributes.". \
               format(self.requirement_id)

        try:
            self.derived = int(attributes[0])
            self.description = str(attributes[1])
            self.figure_number = str(attributes[2])
            self.owner_id = int(attributes[3])
            self.page_number = str(attributes[4])
            self.parent_id = int(attributes[5])
            self.priority = int(attributes[6])
            self.requirement_code = str(attributes[7])
            self.specification = str(attributes[8])
            self.type_id = int(attributes[9])
            self.validated = int(attributes[10])
            self.validated_date = attributes[11]
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKRequirement.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKRequirement attributes."

        return _error_code, _msg
