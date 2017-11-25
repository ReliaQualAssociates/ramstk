# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMode.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKMode Table Module."""

import gettext
# pylint: disable=E0401
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
# pylint: disable=E0401
from Utilities import none_to_default, OutOfRangeError
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class RTKMode(RTK_BASE):
    """
    Class to represent the table rtk_mode in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_function.
    This table shares a Many-to-One relationship with rtk_hardware.
    This table shares a One-to-Many relationship with rtk_mechanism.
    """

    __tablename__ = 'rtk_mode'
    __table_args__ = {'extend_existing': True}

    function_id = Column(
        'fld_function_id',
        Integer,
        ForeignKey('rtk_function.fld_function_id'),
        nullable=False)
    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        nullable=False)
    mode_id = Column(
        'fld_mode_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    critical_item = Column('fld_critial_item', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    design_provisions = Column('fld_design_provisions', BLOB, default='')
    detection_method = Column('fld_detection_method', String(512), default='')
    effect_end = Column('fld_effect_end', String(512), default='')
    effect_local = Column('fld_effect_local', String(512), default='')
    effect_next = Column('fld_effect_next', String(512), default='')
    effect_probability = Column('fld_effect_probability', Float, default=0.0)
    hazard_rate_source = Column(
        'fld_hazard_rate_source', String(512), default='')
    isolation_method = Column('fld_isolation_method', String(512), default='')
    mission = Column('fld_mission', String(64), default='Default Mission')
    mission_phase = Column('fld_mission_phase', String(64), default='')
    mode_criticality = Column('fld_mode_criticality', Float, default=0.0)
    mode_hazard_rate = Column('fld_mode_hazard_rate', Float, default=0.0)
    mode_op_time = Column('fld_mode_op_time', Float, default=0.0)
    mode_probability = Column('fld_mode_probability', String(64), default='')
    mode_ratio = Column('fld_mode_ratio', Float, default=0.0)
    operator_actions = Column('fld_operator_actions', BLOB, default='')
    other_indications = Column(
        'fld_other_indications', String(512), default='')
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

    is_mode = True
    is_mechanism = False
    is_cause = False
    is_control = False
    is_action = False

    def get_attributes(self):
        """
        Retrieve the current values of the RTKMode data model attributes.

        :return: {function_id, hardware_id, mode_id, critical_item,
                  description, design_provisions, detection_method,
                  effect_end, effect_local, effect_next, effect_probability,
                  hazard_rate_source, isolation_method, mission, mission_phase,
                  mode_criticality, mode_hazard_rate, mode_op_time,
                  mode_probability, mode_ratio, operator_actions,
                  other_indications, remarks, rpn_severity, rpn_severity_new,
                  severity_class, single_point, type_id} pairs.
        :rtype: dict
        """
        _attributes = {
            'function_id': self.function_id,
            'hardware_id': self.hardware_id,
            'mode_id': self.mode_id,
            'critical_item': self.critical_item,
            'description': self.description,
            'design_provisions': self.design_provisions,
            'detection_method': self.detection_method,
            'effect_end': self.effect_end,
            'effect_local': self.effect_local,
            'effect_next': self.effect_next,
            'effect_probability': self.effect_probability,
            'hazard_rate_source': self.hazard_rate_source,
            'isolation_method': self.isolation_method,
            'mission': self.mission,
            'mission_phase': self.mission_phase,
            'mode_criticality': self.mode_criticality,
            'mode_hazard_rate': self.mode_hazard_rate,
            'mode_op_time': self.mode_op_time,
            'mode_probability': self.mode_probability,
            'mode_ratio': self.mode_ratio,
            'operator_actions': self.operator_actions,
            'other_indications': self.other_indications,
            'remarks': self.remarks,
            'rpn_severity': self.rpn_severity,
            'rpn_severity_new': self.rpn_severity_new,
            'severity_class': self.severity_class,
            'single_point': self.single_point,
            'type_id': self.type_id
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKMode data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMode {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.critical_item = int(
                none_to_default(attributes['critical_item'], 0))
            self.description = str(
                none_to_default(attributes['description'],
                                'Failure Mode Description'))
            self.design_provisions = str(
                none_to_default(attributes['design_provisions'], ''))
            self.detection_method = str(
                none_to_default(attributes['detection_method'], ''))
            self.effect_end = str(
                none_to_default(attributes['effect_end'], 'End Effect'))
            self.effect_local = str(
                none_to_default(attributes['effect_local'], 'Local Effect'))
            self.effect_next = str(
                none_to_default(attributes['effect_next'], 'Next Effect'))
            self.effect_probability = float(
                none_to_default(attributes['effect_probability'], 0.0))
            self.hazard_rate_source = str(
                none_to_default(attributes['hazard_rate_source'], ''))
            self.isolation_method = str(
                none_to_default(attributes['isolation_method'], ''))
            self.mission = str(none_to_default(attributes['mission'], ''))
            self.mission_phase = str(
                none_to_default(attributes['mission_phase'], ''))
            self.mode_criticality = float(
                none_to_default(attributes['mode_criticality'], 0.0))
            self.mode_hazard_rate = float(
                none_to_default(attributes['mode_hazard_rate'], 0.0))
            self.mode_op_time = float(
                none_to_default(attributes['mode_op_time'], 0.0))
            self.mode_probability = str(
                none_to_default(attributes['mode_probability'], ''))
            self.mode_ratio = float(
                none_to_default(attributes['mode_ratio'], 0.0))
            self.operator_actions = str(
                none_to_default(attributes['operator_actions'], ''))
            self.other_indications = str(
                none_to_default(attributes['other_indications'], ''))
            self.remarks = str(none_to_default(attributes['remarks'], ''))
            self.rpn_severity = str(
                none_to_default(attributes['rpn_severity'], ''))
            self.rpn_severity_new = str(
                none_to_default(attributes['rpn_severity_new'], ''))
            self.severity_class = str(
                none_to_default(attributes['severity_class'], ''))
            self.single_point = int(
                none_to_default(attributes['single_point'], 0))
            self.type_id = int(none_to_default(attributes['type_id'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKMode.set_attributes().".format(_err)

        return _error_code, _msg

    def calculate_criticality(self, item_hr):
        """
        Calculate the Criticality for the Mode.

            Mode Criticality = Item Hazard Rate * Mode Ratio *
                               Mode Operating Time * Effect Probability

        :param float item_hr: the hazard rate of the hardware item being
                              calculated.
        :return: (_error_code, _msg); the error code and associated message
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating failure mode {0:d} criticality.'.\
            format(self.mode_id)

        if item_hr < 0.0:
            _error_code = 2010
            _msg = 'RTK ERROR: Item hazard rate has a negative value.'
            raise OutOfRangeError(_(u"Item hazard rate has a negative value."))
        if not 0.0 <= self.mode_ratio <= 1.0:
            _error_code = 2010
            _msg = 'RTK ERROR: Failure mode ratio is outside the range of ' \
                   '[0.0, 1.0].'
            raise OutOfRangeError(
                _(u"Failure mode ratio is outside the range "
                  u"of [0.0, 1.0]."))
        if self.mode_op_time < 0.0:
            _error_code = 2010
            _msg = 'Failure mode operating time has a negative value.'
            raise OutOfRangeError(
                _(u"Failure mode operating time has a "
                  u"negative value."))
        if not 0.0 <= self.effect_probability <= 1.0:
            _error_code = 2010
            _msg = 'Failure effect probability is outside the range ' \
                   '[0.0, 1.0].'
            raise OutOfRangeError(
                _(u"Failure effect probability is outside "
                  u"the range [0.0, 1.0]."))

        self.mode_hazard_rate = item_hr * self.mode_ratio
        self.mode_criticality = self.mode_hazard_rate \
            * self.mode_op_time * self.effect_probability

        if self.mode_hazard_rate < 0.0:
            _error_code = 2010
            _msg = 'Failure mode hazard rate has a negative value.'
            raise OutOfRangeError(
                _(u"Failure mode hazard rate has a negative "
                  u"value."))
        if self.mode_criticality < 0.0:
            _error_code = 2010
            _msg = 'Failure mode criticality has a negative value.'
            raise OutOfRangeError(
                _(u"Failure mode criticality has a negative "
                  u"value."))

        return _error_code, _msg
