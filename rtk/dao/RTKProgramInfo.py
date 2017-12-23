# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKProgramImfo.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKProgramInfo Table
===============================================================================
"""

from datetime import date

from sqlalchemy import Column, Date, Integer, String  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKProgramInfo(RTK_BASE):
    """
    Class to represent the table rtk_program_info in the RTK Program database.
    """

    __tablename__ = 'rtk_program_info'
    __table_args__ = {'extend_existing': True}

    program_id = Column(
        'fld_program_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    revision_prefix = Column(
        'fld_revision_prefix', String(512), default='REVN')
    revision_next_id = Column('fld_revision_next_id', Integer, default=0)
    function_prefix = Column(
        'fld_function_prefix', String(512), default='FUNC')
    function_next_id = Column('fld_function_next_id', Integer, default=0)
    requirement_prefix = Column(
        'fld_requirement_prefix', String(512), default='RQMT')
    requirement_next_id = Column('fld_requirement_next_id', Integer, default=0)
    assembly_prefix = Column(
        'fld_assembly_prefix', String(512), default='ASSY')
    assembly_next_id = Column('fld_assembly_next_id', Integer, default=0)
    part_prefix = Column('fld_part_prefix', String(512), default='PART')
    part_next_id = Column('fld_part_next_id', Integer, default=0)
    fmeca_prefix = Column('fld_fmeca_prefix', String(512), default='FMECA')
    fmeca_next_id = Column('fld_fmeca_next_id', Integer, default=0)
    mode_prefix = Column('fld_mode_prefix', String(512), default='MODE')
    mode_next_id = Column('fld_mode_next_id', Integer, default=0)
    effect_prefix = Column('fld_effect_prefix', String(512), default='EFFECT')
    effect_next_id = Column('fld_effect_next_id', Integer, default=0)
    cause_prefix = Column('fld_cause_prefix', String(512), default='CAUSE')
    cause_next_id = Column('fld_cause_next_id', Integer, default=0)
    software_prefix = Column(
        'fld_software_prefix', String(512), default='MODULE')
    software_next_id = Column('fld_software_next_id', Integer, default=0)
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
        Method to retrieve the current values of the RTKProgramInfo data model
        attributes.

        :return: (program_id, revision_prefix, revision_next_id,
                  function_prefix, function_next_id, assembly_prefix,
                  assembly_next_id, part_prefix, part_next_id, fmeca_prefix,
                  fmeca_next_id, mode_prefix, mode_next_id, effect_prefix,
                  effect_next_id, cause_prefix, cause_next_id, software_prefix,
                  software_next_id, revision_active, function_active,
                  requirement_active, hardware_active, software_active,
                  vandv_active, testing_active, fraca_active, survival_active,
                  rcm_active, rbd_active, fta_active, created_on, created_by,
                  last_saved, last_saved_by, method)
        :rtype: tuple
        """

        _values = (self.program_id, self.revision_prefix,
                   self.revision_next_id, self.function_prefix,
                   self.function_next_id, self.assembly_prefix,
                   self.assembly_next_id, self.part_prefix, self.part_next_id,
                   self.fmeca_prefix, self.fmeca_next_id, self.mode_prefix,
                   self.mode_next_id, self.effect_prefix, self.effect_next_id,
                   self.cause_prefix, self.cause_next_id, self.software_prefix,
                   self.software_next_id, self.revision_active,
                   self.function_active, self.requirement_active,
                   self.hardware_active, self.software_active,
                   self.vandv_active, self.testing_active, self.fraca_active,
                   self.survival_active, self.rcm_active, self.rbd_active,
                   self.fta_active, self.created_on, self.created_by,
                   self.last_saved, self.last_saved_by, self.method)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKProgramInfo data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKProgramInfo {0:d} attributes.". \
            format(self.program_id)

        try:
            self.revision_prefix = str(
                none_to_default(attributes[0], 'REVISION'))
            self.revision_next_id = int(none_to_default(attributes[1], 0))
            self.function_prefix = str(
                none_to_default(attributes[2], 'FUNCTION'))
            self.function_next_id = int(none_to_default(attributes[3], 0))
            self.assembly_prefix = str(
                none_to_default(attributes[4], 'ASSEMBLY'))
            self.assembly_next_id = int(none_to_default(attributes[5], 0))
            self.part_prefix = str(none_to_default(attributes[6], 'PART'))
            self.part_next_id = int(none_to_default(attributes[7], 0))
            self.fmeca_prefix = str(none_to_default(attributes[8], 'FMECA'))
            self.fmeca_next_id = int(none_to_default(attributes[9], 0))
            self.mode_prefix = str(none_to_default(attributes[10], 'MODE'))
            self.mode_next_id = int(none_to_default(attributes[11], 0))
            self.effect_prefix = str(none_to_default(attributes[12], 'EFECT'))
            self.effect_next_id = int(none_to_default(attributes[13], 0))
            self.cause_prefix = str(none_to_default(attributes[14], 'CAUSE'))
            self.cause_next_id = int(none_to_default(attributes[15], 0))
            self.software_prefix = str(
                none_to_default(attributes[16], 'SOFTWARE'))
            self.software_next_id = int(none_to_default(attributes[17], 0))
            self.revision_active = int(none_to_default(attributes[18], 1))
            self.function_active = int(none_to_default(attributes[19], 1))
            self.requirement_active = int(none_to_default(attributes[20], 1))
            self.hardware_active = int(none_to_default(attributes[21], 1))
            self.software_active = int(none_to_default(attributes[22], 1))
            self.vandv_active = int(none_to_default(attributes[23], 1))
            self.testing_active = int(none_to_default(attributes[24], 1))
            self.fraca_active = int(none_to_default(attributes[25], 1))
            self.survival_active = int(none_to_default(attributes[26], 1))
            self.rcm_active = int(none_to_default(attributes[27], 0))
            self.rbd_active = int(none_to_default(attributes[28], 0))
            self.fta_active = int(none_to_default(attributes[29], 0))
            self.created_on = none_to_default(attributes[30], date.today())
            self.created_by = str(none_to_default(attributes[31], ''))
            self.last_saved = none_to_default(attributes[32], date.today())
            self.last_saved_by = str(none_to_default(attributes[33], ''))
            self.method = str(none_to_default(attributes[34], 'STANDARD'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKProgramInfo.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKProgramInfo attributes."

        return _error_code, _msg
