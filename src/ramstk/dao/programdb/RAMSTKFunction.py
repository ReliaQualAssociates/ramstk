# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKFunction.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFunction Table Module."""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Doyle "weibullguy" Rowland'


class RAMSTKFunction(RAMSTK_BASE):
    """
    Class to represent the ramstk_function table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a One-to-Many relationship with ramstk_mode.
    """

    __tablename__ = 'ramstk_function'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    function_id = Column(
        'fld_function_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    availability_logistics = Column(
        'fld_availability_logistics', Float, default=1.0)
    availability_mission = Column(
        'fld_availability_mission', Float, default=1.0)
    cost = Column('fld_cost', Float, default=0.0)
    function_code = Column(
        'fld_function_code', String(16), default='Function Code')
    hazard_rate_logistics = Column(
        'fld_hazard_rate_logistics', Float, default=0.0)
    hazard_rate_mission = Column('fld_hazard_rate_mission', Float, default=0.0)
    level = Column('fld_level', Integer, default=0)
    mmt = Column('fld_mmt', Float, default=0.0)
    mcmt = Column('fld_mcmt', Float, default=0.0)
    mpmt = Column('fld_mpmt', Float, default=0.0)
    mtbf_logistics = Column('fld_mtbf_logistics', Float, default=0.0)
    mtbf_mission = Column('fld_mtbf_mission', Float, default=0.0)
    mttr = Column('fld_mttr', Float, default=0.0)
    name = Column('fld_name', String(256), default='Function Name')
    parent_id = Column('fld_parent_id', Integer, default=0)
    remarks = Column('fld_remarks', BLOB, default='')
    safety_critical = Column('fld_safety_critical', Integer, default=0)
    total_mode_count = Column('fld_mode_count', Integer, default=0)
    total_part_count = Column('fld_part_count', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='function')
    mode = relationship('RAMSTKMode', back_populates='function')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKFunction data model attributes.

        :return: {revision_id, function_id, availability_logistics,
                  availability_mission, cost, function_code,
                  hazard_rate_logistics, hazard_rate_mission, level, mmt, mcmt,
                  mpmt, mtbf_logistics, mtbf_mission, mttr, name, parent_id,
                  remarks, safety_critical, total_mode_count, total_part_count,
                  type_id} pairs.
        :rtype: tuple
        """
        _values = {
            'revision_id': self.revision_id,
            'function_id': self.function_id,
            'availability_logistics': self.availability_logistics,
            'availability_mission': self.availability_mission,
            'cost': self.cost,
            'function_code': self.function_code,
            'hazard_rate_logistics': self.hazard_rate_logistics,
            'hazard_rate_mission': self.hazard_rate_mission,
            'level': self.level,
            'mmt': self.mmt,
            'mcmt': self.mcmt,
            'mpmt': self.mpmt,
            'mtbf_logistics': self.mtbf_logistics,
            'mtbf_mission': self.mtbf_mission,
            'mttr': self.mttr,
            'name': self.name,
            'parent_id': self.parent_id,
            'remarks': self.remarks,
            'safety_critical': self.safety_critical,
            'total_mode_count': self.total_mode_count,
            'total_part_count': self.total_part_count,
            'type_id': self.type_id
        }

        return _values

    def set_attributes(self, values):
        """
        Set the RAMSTKFunction data model attributes.

        :param dict values: dict of {attribute name:attribute value} pairs to
                            assign to the instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKFunction {0:d} attributes.". \
               format(int(self.function_id))

        try:
            self.availability_logistics = float(
                none_to_default(values['availability_logistics'], 1.0))
            self.availability_mission = float(
                none_to_default(values['availability_mission'], 1.0))
            self.cost = float(none_to_default(values['cost'], 0.0))
            self.function_code = str(
                none_to_default(values['function_code'], 'Function Code'))
            self.hazard_rate_logistics = float(
                none_to_default(values['hazard_rate_logistics'], 0.0))
            self.hazard_rate_mission = float(
                none_to_default(values['hazard_rate_mission'], 0.0))
            self.level = int(none_to_default(values['level'], 0.0))
            self.mmt = float(none_to_default(values['mmt'], 0.0))
            self.mcmt = float(none_to_default(values['mcmt'], 0.0))
            self.mpmt = float(none_to_default(values['mpmt'], 0.0))
            self.mtbf_logistics = float(
                none_to_default(values['mtbf_logistics'], 0.0))
            self.mtbf_mission = float(
                none_to_default(values['mtbf_mission'], 0.0))
            self.mttr = float(none_to_default(values['mttr'], 0.0))
            self.name = str(none_to_default(values['name'], 'Function Name'))
            self.parent_id = int(none_to_default(values['parent_id'], 0))
            self.remarks = str(none_to_default(values['remarks'], ''))
            self.safety_critical = int(
                none_to_default(values['safety_critical'], 0))
            self.total_mode_count = int(
                none_to_default(values['total_mode_count'], 0))
            self.total_part_count = int(
                none_to_default(values['total_part_count'], 0))
            self.type_id = int(none_to_default(values['type_id'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKFunction.set_attributes().".format(str(_err))

        return _error_code, _msg

    def calculate_mtbf(self):
        """
        Calculate the MTBF metrics.

        This method calculates the logistics and mission MTBF.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Calculating MTBF metrics for Function ' \
               'ID {0:d}.'.format(self.function_id)

        try:
            self.mtbf_logistics = 1.0 / self.hazard_rate_logistics
        except OverflowError:
            self.mtbf_logistics = 0.0
            _error_code = 101
            _msg = 'RAMSTK ERROR: Overflow Error when calculating the ' \
                   'logistics MTBF for Function ID {0:d}.  Logistics hazard ' \
                   'rate: {1:f}.'.format(self.function_id,
                                         self.hazard_rate_logistics)
        except ZeroDivisionError:
            self.mtbf_logistics = 0.0
            _error_code = 102
            _msg = 'RAMSTK ERROR: Zero Division Error when calculating the ' \
                   'logistics MTBF for Function ID {0:d}.  Logistics hazard ' \
                   'rate: {1:f}.'.format(self.function_id,
                                         self.hazard_rate_logistics)

        try:
            self.mtbf_mission = 1.0 / self.hazard_rate_mission
        except OverflowError:
            self.mtbf_mission = 0.0
            _error_code = 101
            _msg = 'RAMSTK ERROR: Overflow Error when calculating the mission ' \
                   'MTBF for Function ID {0:d}.  Mission hazard rate: ' \
                   '{1:f}.'.format(self.function_id, self.hazard_rate_mission)
        except ZeroDivisionError:
            self.mtbf_mission = 0.0
            _error_code = 102
            _msg = 'RAMSTK ERROR: Zero Division Error when calculating the ' \
                   'mission MTBF for Function ID {0:d}.  Mission hazard ' \
                   'rate: {1:f}.'.format(self.function_id,
                                         self.hazard_rate_mission)

        return _error_code, _msg

    def calculate_availability(self):
        """
        Calculate the availability metrics.

        This method calculates the logistics and mission availability.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Calculating availability metrics for Function ' \
               'ID {0:d}.'.format(self.function_id)

        try:
            self.availability_logistics = self.mtbf_logistics \
                / (self.mtbf_logistics + self.mttr)
        except OverflowError:
            self.availability_logistics = 0.0
            _error_code = 101
            _msg = 'RAMSTK ERROR: Overflow Error when calculating the ' \
                   'logistics availability for Function ID {0:d}.  ' \
                   'Logistics MTBF: {1:f} MTTR: {2:f}.'.\
                   format(self.function_id, self.mtbf_logistics, self.mttr)
        except ZeroDivisionError:
            self.availability_logistics = 0.0
            _error_code = 102
            _msg = 'RAMSTK ERROR: Zero Division Error when calculating the ' \
                   'logistics availability for Function ID {0:d}.  ' \
                   'Logistics MTBF: {1:f} MTTR: {2:f}.'.\
                   format(self.function_id, self.mtbf_logistics, self.mttr)

        try:
            self.availability_mission = self.mtbf_mission \
                / (self.mtbf_mission + self.mttr)
        except OverflowError:
            self.availability_mission = 0.0
            _error_code = 101
            _msg = 'RAMSTK ERROR: Overflow Error when calculating the ' \
                   'mission availability for Function ID {0:d}.  ' \
                   'Mission MTBF: {1:f} MTTR: {2:f}.'.format(self.function_id,
                                                             self.mtbf_mission,
                                                             self.mttr)
        except ZeroDivisionError:
            self.availability_mission = 0.0
            _error_code = 102
            _msg = 'RAMSTK ERROR: Zero Division Error when calculating the ' \
                   'mission availability for Function ID {0:d}.  ' \
                   'Mission MTBF: {1:f} MTTR: {2:f}.'.format(self.function_id,
                                                             self.mtbf_mission,
                                                             self.mttr)

        return _error_code, _msg
