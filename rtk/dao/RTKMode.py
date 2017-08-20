#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMode.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
===============================================================================
The RTKMode Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKMode(RTK_BASE):
    """
    Class to represent the table rtk_mode in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_function.
    This table shares a Many-to-One relationship with rtk_hardware.
    This table shares a One-to-Many relationship with rtk_mechanism.
    """

    __tablename__ = 'rtk_mode'
    __table_args__ = {'extend_existing': True}

    function_id = Column('fld_function_id', Integer,
                         ForeignKey('rtk_function.fld_function_id'),
                         nullable=False)
    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         nullable=False)
    mode_id = Column('fld_mode_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    critical_item = Column('fld_critial_item', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    design_provisions = Column('fld_design_provisions', BLOB, default='')
    detection_method = Column('fld_detection_method', String(512), default='')
    effect_end = Column('fld_effect_end', String(512), default='')
    effect_local = Column('fld_effect_local', String(512), default='')
    effect_next = Column('fld_effect_next', String(512), default='')
    effect_probability = Column('fld_effect_probability', Float, default=0.0)
    hazard_rate_source = Column('fld_hazard_rate_source', String(512),
                                default='')
    isolation_method = Column('fld_isolation_method', String(512), default='')
    mission = Column('fld_mission', String(64), default='Default Mission')
    mission_phase = Column('fld_mission_phase', String(64), default='')
    mode_criticality = Column('fld_mode_criticality', Float, default=0.0)
    mode_hazard_rate = Column('fld_mode_hazard_rate', Float, default=0.0)
    mode_op_time = Column('fld_mode_op_time', Float, default=0.0)
    mode_probability = Column('fld_mode_probability', String(64), default='')
    mode_ratio = Column('fld_mode_ratio', Float, default=0.0)
    operator_actions = Column('fld_operator_actions', BLOB, default='')
    other_indications = Column('fld_other_indications', String(512),
                               default='')
    remarks = Column('fld_remarks', BLOB, default='')
    rpn_severity = Column('fld_rpn_severity', String(64), default='')
    rpn_severity_new = Column('fld_rpn_severity_new', String(64), default='')
    severity_class = Column('fld_severity_class', String(64), default='')
    single_point = Column('fld_single_point', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    function = relationship('RTKFunction', back_populates='mode')
    hardware = relationship('RTKHardware', back_populates='mode')
    mechanism = relationship('RTKMechanism', back_populates='mode')

    # The following are required for functional FMEA.
    control = relationship('RTKControl', back_populates='mode')
    action = relationship('RTKAction', back_populates='mode')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKMode data model
        attributes.

        :return: (function_id, hardware_id, mode_id, critical_item,
                  description, design_provisions, detection_method,
                  effect_end, effect_local, effect_next, effect_probability,
                  hazard_rate_source, isolation_method, mission, mission_phase,
                  mode_criticality, mode_hazard_rate, mode_op_time,
                  mode_probability, mode_ratio, operator_actions,
                  other_indications, remarks, rpn_severity, rpn_severity_new,
                  severity_class, single_point, type_id)
        :rtype: tuple
        """

        _attributes = (self.function_id, self.hardware_id, self.mode_id,
                       self.critical_item, self.description,
                       self.design_provisions, self.detection_method,
                       self.effect_end, self.effect_local, self.effect_next,
                       self.effect_probability, self.hazard_rate_source,
                       self.isolation_method, self.mission, self.mission_phase,
                       self.mode_criticality, self.mode_hazard_rate,
                       self.mode_op_time, self.mode_probability,
                       self.mode_ratio, self.operator_actions,
                       self.other_indications, self.remarks, self.rpn_severity,
                       self.rpn_severity_new, self.severity_class,
                       self.single_point, self.type_id)

        return _attributes

    def set_attributes(self, values):
        """
        Method to set the RTKMode data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMode {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.critical_item = int(none_to_default(values[0], 0))
            self.description = str(none_to_default(values[1],
                                                   'Failure Mode Description'))
            self.design_provisions = str(none_to_default(values[2], ''))
            self.detection_method = str(none_to_default(values[3], ''))
            self.effect_end = str(none_to_default(values[4], 'End Effect'))
            self.effect_local = str(none_to_default(values[5], 'Local Effect'))
            self.effect_next = str(none_to_default(values[6], 'Next Effect'))
            self.effect_probability = float(none_to_default(values[7], 0.0))
            self.hazard_rate_source = str(none_to_default(values[8], ''))
            self.isolation_method = str(none_to_default(values[9], ''))
            self.mission = str(none_to_default(values[10], ''))
            self.mission_phase = str(none_to_default(values[11], ''))
            self.mode_criticality = float(none_to_default(values[12], 0.0))
            self.mode_hazard_rate = float(none_to_default(values[13], 0.0))
            self.mode_op_time = float(none_to_default(values[14], 0.0))
            self.mode_probability = str(none_to_default(values[15], ''))
            self.mode_ratio = float(none_to_default(values[16], 0.0))
            self.operator_actions = str(none_to_default(values[17], ''))
            self.other_indications = str(none_to_default(values[18], ''))
            self.remarks = str(none_to_default(values[19], ''))
            self.rpn_severity = str(none_to_default(values[20], ''))
            self.rpn_severity_new = str(none_to_default(values[21], ''))
            self.severity_class = str(none_to_default(values[22], ''))
            self.single_point = int(none_to_default(values[23], 0))
            self.type_id = int(none_to_default(values[24], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMode.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMode attributes."

        return _error_code, _msg
