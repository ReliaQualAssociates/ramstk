#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKProgramImfo.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKProgramInfo Table
==============================
"""

from datetime import date

from sqlalchemy import Column, Date, Integer, String

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
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKPhase(Base):
    """
    Class to represent the table rtk_program_info in the RTK Program database.
    """

    __tablename__ = 'rtk_program_info'
    __table_args__ = {'extend_existing': True}

    program_id = Column('fld_program_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    revision_prefix = Column('fld_revision_prefix', String(512),
                             default='REVISION')
    revision_next_id = Column('fld_revision_next_id', Integer, default=0)
    function_prefix = Column('fld_function_prefix', String(512),
                             default='FUNCTION')
    function_next_id = Column('fld_funcion_next_id', Integer, default=0)
    assembly_prefix = Column('fld_assembly_prefix', String(512),
                             default='ASSEMBLY')
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
    software_prefix = Column('fld_software_prefix', String(512),
                             default='MODULE')
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
    created_on = Column('fld_create_on', Date, default=date.today())
    created_by = Column('fld_created_by', String(512), default='')
    last_saved = Column('fld_last_saved', Date, default=date.today())
    last_saved_by = Column('fld_created_by', String(512), default='')
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
            self.revision_prefix = str(attributes[0])
            self.revision_next_id = int(attributes[1])
            self.function_prefix = str(attributes[2])
            self.function_next_id = int(attributes[3])
            self.assembly_prefix = str(attributes[4])
            self.assembly_next_id = int(attributes[5])
            self.part_prefix = str(attributes[6])
            self.part_next_id = int(attributes[7])
            self.fmeca_prefix = str(attributes[8])
            self.fmeca_next_id = int(attributes[9])
            self.mode_prefix = str(attributes[10])
            self.mode_next_id = int(attributes[11])
            self.effect_prefix = str(attributes[12])
            self.effect_next_id = int(attributes[13])
            self.cause_prefix = str(attributes[14])
            self.cause_next_id = int(attributes[15])
            self.software_prefix = str(attributes[16])
            self.software_next_id = int(attributes[17])
            self.revision_active = int(attributes[18])
            self.function_active = int(attributes[19])
            self.requirement_active = int(attributes[20])
            self.hardware_active = int(attributes[21])
            self.software_active = int(attributes[22])
            self.vandv_active = int(attributes[23])
            self.testing_active = int(attributes[24])
            self.fraca_active = int(attributes[25])
            self.survival_active = int(attributes[26])
            self.rcm_active = int(attributes[27])
            self.rbd_active = int(attributes[28])
            self.fta_active = int(attributes[29])
            self.created_on = attributes[30]
            self.created_by = str(attributes[31])
            self.last_saved = attributes[32]
            self.last_saved_by = str(attributes[33])
            self.method = str(attributes[34])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKProgramInfo.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKProgramInfo attributes."

        return _error_code, _msg
