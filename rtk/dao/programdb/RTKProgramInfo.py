# -*- coding: utf-8 -*-
#
#       rtk.dao.programdb.RTKProgramImfo.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKProgramInfo Table Module."""

from datetime import date

from sqlalchemy import Column, Date, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKProgramInfo(RTK_BASE):
    """
    Class to represent the table rtk_program_info in the RTK Program database.

    This table has a one-to-one relationship with RTKProgramStatus.
    """

    __tablename__ = 'rtk_program_info'
    __table_args__ = {'extend_existing': True}

    program_id = Column(
        'fld_program_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    revision_active = Column('fld_revision_active', Integer, default=1)
    function_active = Column('fld_function_active', Integer, default=1)
    requirement_active = Column('fld_requirement_active', Integer, default=1)
    hardware_active = Column('fld_hardware_active', Integer, default=1)
    software_active = Column('fld_software_active', Integer, default=1)
    vandv_active = Column('fld_vandv_active', Integer, default=1)
    testing_active = Column('fld_testing_active', Integer, default=1)
    fraca_active = Column('fld_fraca_active', Integer, default=1)
    survival_active = Column('fld_survival_active', Integer, default=1)
    rcm_active = Column('fld_rcm_active', Integer, default=0)
    rbd_active = Column('fld_rbd_active', Integer, default=0)
    fta_active = Column('fld_fta_active', Integer, default=0)
    created_on = Column('fld_created_on', Date, default=date.today())
    created_by = Column('fld_created_by', String(512), default='')
    last_saved = Column('fld_last_saved_on', Date, default=date.today())
    last_saved_by = Column('fld_last_saved_by', String(512), default='')
    method = Column('fld_method', String(512), default='STANDARD')

    def get_attributes(self):
        """
        Retrieve the current values of RTKProgramInfo data model attributes.

        :return: {program_id, revision_active, function_active,
                  requirement_active, hardware_active, software_active,
                  vandv_active, testing_active, fraca_active, survival_active,
                  rcm_active, rbd_active, fta_active, created_on, created_by,
                  last_saved, last_saved_by, method} pairs.
        :rtype: dict
        """
        _attributes = {
            'program_id': self.program_id,
            'revision_active': self.revision_active,
            'function_active': self.function_active,
            'requirement_active': self.requirement_active,
            'hardware_active': self.hardware_active,
            'software_active': self.software_active,
            'vandv_active': self.vandv_active,
            'testing_active': self.testing_active,
            'fraca_active': self.fraca_active,
            'survival_active': self.survival_active,
            'rcm_active': self.rcm_active,
            'rbd_active': self.rbd_active,
            'fta_active': self.fta_active,
            'created_on': self.created_on,
            'created_by': self.created_by,
            'last_saved': self.last_saved,
            'last_saved_by': self.last_saved_by,
            'method': self.method
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKProgramInfo data model attributes.

        :param dict attributes: dict containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKProgramInfo {0:d} attributes.". \
            format(self.program_id)

        try:
            self.revision_active = int(
                none_to_default(attributes['revision_active'], 1))
            self.function_active = int(
                none_to_default(attributes['function_active'], 1))
            self.requirement_active = int(
                none_to_default(attributes['requirement_active'], 1))
            self.hardware_active = int(
                none_to_default(attributes['hardware_active'], 1))
            self.software_active = int(
                none_to_default(attributes['software_active'], 1))
            self.vandv_active = int(
                none_to_default(attributes['vandv_active'], 1))
            self.testing_active = int(
                none_to_default(attributes['testing_active'], 1))
            self.fraca_active = int(
                none_to_default(attributes['fraca_active'], 1))
            self.survival_active = int(
                none_to_default(attributes['survival_active'], 1))
            self.rcm_active = int(none_to_default(attributes['rcm_active'], 0))
            self.rbd_active = int(none_to_default(attributes['rbd_active'], 0))
            self.fta_active = int(none_to_default(attributes['fta_active'], 0))
            self.created_on = none_to_default(attributes['created_on'],
                                              date.today())
            self.created_by = str(
                none_to_default(attributes['created_by'], ''))
            self.last_saved = none_to_default(attributes['last_saved'],
                                              date.today())
            self.last_saved_by = str(
                none_to_default(attributes['last_saved_by'], ''))
            self.method = str(
                none_to_default(attributes['method'], 'STANDARD'))
        except KeyError as _err:
            _error_code = 1
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKProgramInfo.set_attributes().".format(_err)

        return _error_code, _msg
