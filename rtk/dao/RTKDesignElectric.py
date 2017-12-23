# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKDesignElectric.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKDesignElectric Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


# pylint: disable=R0902
class RTKDesignElectric(RTK_BASE):
    """
    Class to represent the rtk_design_electric table in the RTK Program
    database.

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

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKDesignElectric data
        model attributes.

        :return: (hardware_id, application_id, area, capacitance,
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
                  voltage_ratio, weight, years_in_production)
        :rtype: tuple
        """

        _attributes = (
            self.hardware_id, self.application_id, self.area, self.capacitance,
            self.configuration_id, self.construction_id, self.contact_form_id,
            self.contact_gauge, self.contact_rating_id, self.current_operating,
            self.current_rated, self.current_ratio, self.environment_active_id,
            self.environment_dormant_id, self.family_id, self.feature_size,
            self.frequency_operating, self.insert_id, self.insulation_id,
            self.manufacturing_id, self.matching_id, self.n_active_pins,
            self.n_circuit_planes, self.n_cycles, self.n_elements,
            self.n_hand_soldered, self.n_wave_soldered, self.operating_life,
            self.overstress, self.package_id, self.power_operating,
            self.power_rated, self.power_ratio, self.reason, self.resistance,
            self.specification_id, self.technology_id, self.temperature_case,
            self.temperature_hot_spot, self.temperature_junction,
            self.temperature_rated_max, self.temperature_rated_min,
            self.temperature_rise, self.theta_jc, self.type_id,
            self.voltage_ac_operating, self.voltage_dc_operating,
            self.voltage_esd, self.voltage_rated, self.voltage_ratio,
            self.weight, self.years_in_production)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKDesignElectric data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKDesignElectric {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.hardware_id = int(none_to_default(attributes[0], 0))
            self.application_id = int(none_to_default(attributes[1], 0))
            self.area = float(none_to_default(attributes[2], 0.0))
            self.capacitance = float(none_to_default(attributes[3], 0.0))
            self.configuration_id = int(none_to_default(attributes[4], 0))
            self.construction_id = int(none_to_default(attributes[5], 0))
            self.contact_form_id = int(none_to_default(attributes[6], 0))
            self.contact_gauge = int(none_to_default(attributes[7], 0))
            self.contact_rating_id = int(none_to_default(attributes[8], 0))
            self.current_operating = float(none_to_default(attributes[9], 0.0))
            self.current_rated = float(none_to_default(attributes[10], 0.0))
            self.current_ratio = float(none_to_default(attributes[11], 0.0))
            self.environment_active_id = int(
                none_to_default(attributes[12], 0))
            self.environment_dormant_id = int(
                none_to_default(attributes[13], 0))
            self.family_id = int(none_to_default(attributes[14], 0))
            self.feature_size = float(none_to_default(attributes[15], 0.0))
            self.frequency_operating = float(
                none_to_default(attributes[16], 0.0))
            self.insert_id = int(none_to_default(attributes[17], 0))
            self.insulation_id = int(none_to_default(attributes[18], 0))
            self.manufacturing_id = int(none_to_default(attributes[19], 0))
            self.matching_id = int(none_to_default(attributes[20], 0))
            self.n_active_pins = int(none_to_default(attributes[21], 0))
            self.n_circuit_planes = int(none_to_default(attributes[22], 1))
            self.n_cycles = int(none_to_default(attributes[23], 0))
            self.n_elements = int(none_to_default(attributes[24], 0))
            self.n_hand_soldered = int(none_to_default(attributes[25], 0))
            self.n_wave_soldered = int(none_to_default(attributes[26], 0))
            self.operating_life = float(none_to_default(attributes[27], 0.0))
            self.overstress = int(none_to_default(attributes[28], 0))
            self.package_id = int(none_to_default(attributes[29], 0))
            self.power_operating = float(none_to_default(attributes[30], 0.0))
            self.power_rated = float(none_to_default(attributes[31], 0.0))
            self.power_ratio = float(none_to_default(attributes[32], 0.0))
            self.reason = str(none_to_default(attributes[33], ''))
            self.resistance = float(none_to_default(attributes[34], 0.0))
            self.specification_id = int(none_to_default(attributes[35], 0))
            self.technology_id = int(none_to_default(attributes[36], 0))
            self.temperature_case = float(none_to_default(attributes[37], 0.0))
            self.temperature_hot_spot = float(
                none_to_default(attributes[38], 0.0))
            self.temperature_junction = float(
                none_to_default(attributes[39], 0.0))
            self.temperature_rated_max = float(
                none_to_default(attributes[40], 0.0))
            self.temperature_rated_min = float(
                none_to_default(attributes[41], 0.0))
            self.temperature_rise = float(none_to_default(attributes[42], 0.0))
            self.theta_jc = float(none_to_default(attributes[43], 0.0))
            self.type_id = float(none_to_default(attributes[44], 0.0))
            self.voltage_ac_operating = float(
                none_to_default(attributes[45], 0.0))
            self.voltage_dc_operating = float(
                none_to_default(attributes[46], 0.0))
            self.voltage_esd = float(none_to_default(attributes[47], 0.0))
            self.voltage_rated = float(none_to_default(attributes[48], 0.0))
            self.voltage_ratio = float(none_to_default(attributes[49], 0.0))
            self.weight = float(none_to_default(attributes[50], 0.0))
            self.years_in_production = int(none_to_default(attributes[51], 1))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKDesignElectric.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKDesignElectric attributes."

        return _error_code, _msg
