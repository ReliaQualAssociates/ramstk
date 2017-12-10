# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKDesignElectric.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKDesignElectric Table Module."""

# pylint: disable=E0401
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


# pylint: disable=R0902
class RTKDesignElectric(RTK_BASE):  # pragma: no cover
    """
    Represent the rtk_design_electric table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_design_electric'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    application_id = Column('fld_application_id', Integer, default=0)
    area = Column('fld_area', Float, default=0.0)
    capacitance = Column('fld_capacitance', Float, default=0.0)
    configuration_id = Column('fld_configuration_id', Integer, default=0)
    construction_id = Column('fld_construction_id', Integer, default=0)
    contact_form_id = Column('fld_contact_form_id', Integer, default=0)
    contact_gauge = Column('fld_contact_gauge', Integer, default=0)
    contact_rating_id = Column('fld_contact_rating_id', Integer, default=0)
    current_operating = Column('fld_current_operating', Float, default=0.0)
    current_rated = Column('fld_current_rated', Float, default=0.0)
    current_ratio = Column('fld_current_ratio', Float, default=0.0)
    environment_active_id = Column(
        'fld_environment_active_id', Integer, default=0)
    environment_dormant_id = Column(
        'fld_environment_dormant_id', Integer, default=0)
    family_id = Column('fld_family_id', Integer, default=0)
    feature_size = Column('fld_feature_size', Float, default=0.0)
    frequency_operating = Column('fld_frequency_operating', Float, default=0.0)
    insert_id = Column('fld_insert_id', Integer, default=0)
    insulation_id = Column('fld_insulation_id', Integer, default=0)
    manufacturing_id = Column('fld_manufacturing_id', Integer, default=0)
    matching_id = Column('fld_matching_id', Integer, default=0)
    n_active_pins = Column('fld_n_active_pins', Integer, default=0)
    n_circuit_planes = Column('fld_n_circuit_planes', Integer, default=1)
    n_cycles = Column('fld_n_cycles', Integer, default=0)
    n_elements = Column('fld_n_elements', Integer, default=0)
    n_hand_soldered = Column('fld_n_hand_soldered', Integer, default=0)
    n_wave_soldered = Column('fld_n_wave_soldered', Integer, default=0)
    operating_life = Column('fld_operating_life', Float, default=0.0)
    overstress = Column('fld_overstress', Integer, default=0)
    package_id = Column('fld_package_id', Integer, default=0)
    power_operating = Column('fld_power_operating', Float, default=0.0)
    power_rated = Column('fld_power_rated', Float, default=0.0)
    power_ratio = Column('fld_power_ratio', Float, default=0.0)
    reason = Column('fld_reason', String(1024), default='')
    resistance = Column('fld_resistance', Float, default=0.0)
    specification_id = Column('fld_specification_id', Integer, default=0)
    technology_id = Column('fld_technology_id', Integer, default=0)
    temperature_case = Column('fld_temperature_case', Float, default=0.0)
    temperature_hot_spot = Column(
        'fld_temperature_hot_spot', Float, default=0.0)
    temperature_junction = Column(
        'fld_temperature_junction', Float, default=0.0)
    temperature_rated_max = Column(
        'fld_temperature_rated_max', Float, default=0.0)
    temperature_rated_min = Column(
        'fld_temperature_rated_min', Float, default=0.0)
    temperature_rise = Column('fld_temperature_rise', Float, default=0.0)
    theta_jc = Column('fld_theta_jc', Float, default=0.0)
    type_id = Column('fld_type_id', Integer, default=0)
    voltage_ac_operating = Column(
        'fld_voltage_ac_operating', Float, default=0.0)
    voltage_dc_operating = Column(
        'fld_voltage_dc_operating', Float, default=0.0)
    voltage_esd = Column('fld_voltage_esd', Float, default=0.0)
    voltage_rated = Column('fld_voltage_rated', Float, default=0.0)
    voltage_ratio = Column('fld_voltage_ratio', Float, default=0.0)
    weight = Column('fld_weight', Float, default=0.0)
    years_in_production = Column('fld_years_in_production', Integer, default=1)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='design_electric')

    def get_attributes(self):  # pragma: no cover
        """
        Retrieve current values of the RTKDesignElectric data model attributes.

        :return: {hardware_id, application_id, area, capacitance,
                  configuration_id, construction_id, contact_form_id,
                  contact_gauge, contact_rating_id, current_operating,
                  current_rated, current_ratio, environment_active_id,
                  environment_dormant_id, family_id, feature_size,
                  frequency_operating, insert_id, insulation_id,
                  manufacturing_id, matching_id, n_active_pins,
                  n_circuit_planes, n_cycles, n_elements, n_hand_soldered,
                  n_wave_soldered, operating_life, overstress, package_id,
                  power_operating, power_rated, power_ratio, reason,
                  resistance, specification_id, technology_id,
                  temperature_case, temperature_hot_spot, temperature_junction,
                  temperature_rated_max, temperature_rated_min,
                  temperature_rise, theta_jc, type_id, voltage_ac_operating,
                  voltage_dc_operating, voltage_esd, voltage_rated,
                  voltage_ratio, weight, years_in_production} pairs.
        :rtype: dict
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'application_id': self.application_id,
            'area': self.area,
            'capacitance': self.capacitance,
            'configuration_id': self.configuration_id,
            'construction_id': self.construction_id,
            'contact_form_id': self.contact_form_id,
            'contact_gauge': self.contact_gauge,
            'contact_rating_id': self.contact_rating_id,
            'current_operating': self.current_operating,
            'current_rated': self.current_rated,
            'current_ratio': self.current_ratio,
            'environment_active_id': self.environment_active_id,
            'environment_dormant_id': self.environment_dormant_id,
            'family_id': self.family_id,
            'feature_size': self.feature_size,
            'frequency_operating': self.frequency_operating,
            'insert_id': self.insert_id,
            'insulation_id': self.insulation_id,
            'manufacturing_id': self.manufacturing_id,
            'matching_id': self.matching_id,
            'n_active_pins': self.n_active_pins,
            'n_circuit_planes': self.n_circuit_planes,
            'n_cycles': self.n_cycles,
            'n_elements': self.n_elements,
            'n_hand_soldered': self.n_hand_soldered,
            'n_wave_soldered': self.n_wave_soldered,
            'operating_life': self.operating_life,
            'overstress': self.overstress,
            'package_id': self.package_id,
            'power_operating': self.power_operating,
            'power_rated': self.power_rated,
            'power_ratio': self.power_ratio,
            'reason': self.reason,
            'resistance': self.resistance,
            'specification_id': self.specification_id,
            'technology_id': self.technology_id,
            'temperature_case': self.temperature_case,
            'temperature_hot_spot': self.temperature_hot_spot,
            'temperature_junction': self.temperature_junction,
            'temperature_rated_max': self.temperature_rated_max,
            'temperature_rated_min': self.temperature_rated_min,
            'temperature_rise': self.temperature_rise,
            'theta_jc': self.theta_jc,
            'type_id': self.type_id,
            'voltage_ac_operating': self.voltage_ac_operating,
            'voltage_dc_operating': self.voltage_dc_operating,
            'voltage_esd': self.voltage_esd,
            'voltage_rated': self.voltage_rated,
            'voltage_ratio': self.voltage_ratio,
            'weight': self.weight,
            'years_in_production': self.years_in_production
        }

        return _attributes

    def set_attributes(self, attributes):  # pragma: no cover
        """
        Set the cuurent values of the RTKDesignElectric data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKDesignElectric {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.hardware_id = int(
                none_to_default(attributes['hardware_id'], 0))
            self.application_id = int(
                none_to_default(attributes['application_id'], 0))
            self.area = float(none_to_default(attributes['area'], 0.0))
            self.capacitance = float(
                none_to_default(attributes['capacitance'], 0.0))
            self.configuration_id = int(
                none_to_default(attributes['configuration_id'], 0))
            self.construction_id = int(
                none_to_default(attributes['construction_id'], 0))
            self.contact_form_id = int(
                none_to_default(attributes['contact_form_id'], 0))
            self.contact_gauge = int(
                none_to_default(attributes['contact_gauge'], 0))
            self.contact_rating_id = int(
                none_to_default(attributes['contact_rating_id'], 0))
            self.current_operating = float(
                none_to_default(attributes['current_operating'], 0.0))
            self.current_rated = float(
                none_to_default(attributes['current_rated'], 0.0))
            self.current_ratio = float(
                none_to_default(attributes['current_ratio'], 0.0))
            self.environment_active_id = int(
                none_to_default(attributes['environment_active_id'], 0))
            self.environment_dormant_id = int(
                none_to_default(attributes['environment_dormant_id'], 0))
            self.family_id = int(none_to_default(attributes['family_id'], 0))
            self.feature_size = float(
                none_to_default(attributes['feature_size'], 0.0))
            self.frequency_operating = float(
                none_to_default(attributes['frequency_operating'], 0.0))
            self.insert_id = int(none_to_default(attributes['insert_id'], 0))
            self.insulation_id = int(
                none_to_default(attributes['insulation_id'], 0))
            self.manufacturing_id = int(
                none_to_default(attributes['manufacturing_id'], 0))
            self.matching_id = int(
                none_to_default(attributes['matching_id'], 0))
            self.n_active_pins = int(
                none_to_default(attributes['n_active_pins'], 0))
            self.n_circuit_planes = int(
                none_to_default(attributes['n_circuit_planes'], 1))
            self.n_cycles = int(none_to_default(attributes['n_cycles'], 0))
            self.n_elements = int(none_to_default(attributes['n_elements'], 0))
            self.n_hand_soldered = int(
                none_to_default(attributes['n_hand_soldered'], 0))
            self.n_wave_soldered = int(
                none_to_default(attributes['n_wave_soldered'], 0))
            self.operating_life = float(
                none_to_default(attributes['operating_life'], 0.0))
            self.overstress = int(none_to_default(attributes['overstress'], 0))
            self.package_id = int(none_to_default(attributes['package_id'], 0))
            self.power_operating = float(
                none_to_default(attributes['power_operating'], 0.0))
            self.power_rated = float(
                none_to_default(attributes['power_rated'], 0.0))
            self.power_ratio = float(
                none_to_default(attributes['power_ratio'], 0.0))
            self.reason = str(none_to_default(attributes['reason'], ''))
            self.resistance = float(
                none_to_default(attributes['resistance'], 0.0))
            self.specification_id = int(
                none_to_default(attributes['specification_id'], 0))
            self.technology_id = int(
                none_to_default(attributes['technology_id'], 0))
            self.temperature_case = float(
                none_to_default(attributes['temperature_case'], 0.0))
            self.temperature_hot_spot = float(
                none_to_default(attributes['temperature_hot_spot'], 0.0))
            self.temperature_junction = float(
                none_to_default(attributes['temperature_junction'], 0.0))
            self.temperature_rated_max = float(
                none_to_default(attributes['temperature_rated_max'], 0.0))
            self.temperature_rated_min = float(
                none_to_default(attributes['temperature_rated_min'], 0.0))
            self.temperature_rise = float(
                none_to_default(attributes['temperature_rise'], 0.0))
            self.theta_jc = float(none_to_default(attributes['theta_jc'], 0.0))
            self.type_id = float(none_to_default(attributes['type_id'], 0.0))
            self.voltage_ac_operating = float(
                none_to_default(attributes['voltage_ac_operating'], 0.0))
            self.voltage_dc_operating = float(
                none_to_default(attributes['voltage_dc_operating'], 0.0))
            self.voltage_esd = float(
                none_to_default(attributes['voltage_esd'], 0.0))
            self.voltage_rated = float(
                none_to_default(attributes['voltage_rated'], 0.0))
            self.voltage_ratio = float(
                none_to_default(attributes['voltage_ratio'], 0.0))
            self.weight = float(none_to_default(attributes['weight'], 0.0))
            self.years_in_production = int(
                none_to_default(attributes['years_in_production'], 1))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKDesignElectric.set_attributes().".format(_err)

        return _error_code, _msg
