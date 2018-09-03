# -*- coding: utf-8 -*-
#
#       rtk.dao.programdb.RAMSTKProgramStatus.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RAMSTKProgramStatus Table Module."""

from datetime import date

from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKProgramStatus(RAMSTK_BASE):
    """
    Class to represent the table rtk_validation in the RAMSTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_program_status'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('rtk_revision.fld_revision_id'),
        nullable=False)
    status_id = Column(
        'fld_status_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    cost_remaining = Column('fld_cost_remaining', Float, default=0.0)
    date_status = Column(
        'fld_date_status', Date, unique=True, default=date.today())
    time_remaining = Column('fld_time_remaining', Float, default=0.0)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='program_status')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKProgramStatus data model attributes.

        :return: {revision_id, cost_remaining, date_status, time_remaining}
                 pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'status_id': self.status_id,
            'cost_remaining': self.cost_remaining,
            'date_status': self.date_status,
            'time_remaining': self.time_remaining
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current value of the RAMSTKProgramStatus data model attributes.

        :param tuple attributes: dicte of values to assign to the instance
                                 attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKProgramStatus {0:d} attributes.". \
               format(self.revision_id)

        try:
            self.cost_remaining = float(
                none_to_default(attributes['cost_remaining'], 0.0))
            self.date_status = none_to_default(attributes['date_status'],
                                               date.today())
            self.time_remaining = float(
                none_to_default(attributes['time_remaining'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKProgramStatus.set_attributes().".format(_err)

        return _error_code, _msg
