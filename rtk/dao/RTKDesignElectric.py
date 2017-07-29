#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKDesignElectric.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKDesignElectric Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer, String
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


class RTKDesignElectric(RTK_BASE):
    """
    Class to represent the rtk_design_electric table in the RTK Program
    database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_design_electric'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

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
    environment_active_id = Column('fld_environment_active_id', Integer,
                                   default=0)
    environment_dormant_id = Column('fld_environment_dormant_id', Integer,
                                    default=0)
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
    temperature_hot_spot = Column('fld_temperature_hot_spot', Float,
                                  default=0.0)
    temperature_junction = Column('fld_temperature_junction', Float,
                                  default=0.0)
    temperature_rated_max = Column('fld_temperature_rated_max', Float,
                                   default=0.0)
    temperature_rated_min = Column('fld_temperature_rated_min', Float,
                                   default=0.0)
    temperature_rise = Column('fld_temperature_rise', Float, default=0.0)
    theta_jc = Column('fld_theta_jc', Float, default=0.0)
    type_id = Column('fld_type_id', Integer, default=0)
    voltage_ac_operating = Column('fld_voltage_ac_operating', Float,
                                  default=0.0)
    voltage_dc_operating = Column('fld_voltage_dc_operating', Float,
                                  default=0.0)
    voltage_esd = Column('fld_voltage_esd', Float, default=0.0)
    voltage_rated = Column('fld_voltage_rated', Float, default=0.0)
    voltage_ratio = Column('fld_voltage_ratio', Float, default=0.0)
    weight = Column('fld_weight', Float, default=0.0)
    years_in_production = Column('fld_years_in_production', Integer, default=1)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware',
                            back_populates='design_electric')

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

        _attributes = (self.hardware_id, self.application_id, self.area,
                       self.capacitance, self.configuration_id,
                       self.construction_id, self.contact_form_id,
                       self.contact_gauge, self.contact_rating_id,
                       self.current_operating, self.current_rated,
                       self.current_ratio, self.environment_active_id,
                       self.environment_dormant_id, self.family_id,
                       self.feature_size, self.frequency_operating,
                       self.insert_id, self.insulation_id,
                       self.manufacturing_id, self.matching_id,
                       self.n_active_pins, self.n_circuit_planes,
                       self.n_cycles, self.n_elements, self.n_hand_soldered,
                       self.n_wave_soldered, self.operating_life,
                       self.overstress, self.package_id, self.power_operating,
                       self.power_rated, self.power_ratio, self.reason,
                       self.resistance, self.specification_id,
                       self.technology_id, self.temperature_case,
                       self.temperature_hot_spot, self.temperature_junction,
                       self.temperature_rated_max, self.temperature_rated_min,
                       self.temperature_rise, self.theta_jc, self.type_id,
                       self.voltage_ac_operating, self.voltage_dc_operating,
                       self.voltage_esd, self.voltage_rated,
                       self.voltage_ratio, self.weight,
                       self.years_in_production)

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
            self.hardware_id = int(attributes[0])
            self.application_id = int(attributes[1])
            self.area = float(attributes[2])
            self.capacitance = float(attributes[3])
            self.configuration_id = int(attributes[4])
            self.construction_id = int(attributes[5])
            self.contact_form_id = int(attributes[6])
            self.contact_gauge = int(attributes[7])
            self.contact_rating_id = int(attributes[8])
            self.current_operating = float(attributes[9])
            self.current_rated = float(attributes[10])
            self.current_ratio = float(attributes[11])
            self.environment_active_id = int(attributes[12])
            self.environment_dormant_id = int(attributes[13])
            self.family_id = int(attributes[14])
            self.feature_size = float(attributes[15])
            self.frequency_operating = float(attributes[16])
            self.insert_id = int(attributes[17])
            self.insulation_id = int(attributes[18])
            self.manufacturing_id = int(attributes[19])
            self.matching_id = int(attributes[20])
            self.n_active_pins = int(attributes[21])
            self.n_circuit_planes = int(attributes[22])
            self.n_cycles = int(attributes[23])
            self.n_elements = int(attributes[24])
            self.n_hand_soldered = int(attributes[25])
            self.n_wave_soldered = int(attributes[26])
            self.operating_life = float(attributes[27])
            self.overstress = int(attributes[28])
            self.package_id = int(attributes[29])
            self.power_operating = float(attributes[30])
            self.power_rated = float(attributes[31])
            self.power_ratio = float(attributes[32])
            self.reason = str(attributes[33])
            self.resistance = float(attributes[34])
            self.specification_id = int(attributes[35])
            self.technology_id = int(attributes[36])
            self.temperature_case = float(attributes[37])
            self.temperature_hot_spot = float(attributes[38])
            self.temperature_junction = float(attributes[39])
            self.temperature_rated_max = float(attributes[40])
            self.temperature_rated_min = float(attributes[41])
            self.temperature_rise = float(attributes[42])
            self.theta_jc = float(attributes[43])
            self.type_id = float(attributes[44])
            self.voltage_ac_operating = float(attributes[45])
            self.voltage_dc_operating = float(attributes[46])
            self.voltage_esd = float(attributes[47])
            self.voltage_rated = float(attributes[48])
            self.voltage_ratio = float(attributes[49])
            self.weight = float(attributes[50])
            self.years_in_production = int(attributes[51])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKDesignElectric.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKDesignElectric attributes."

        return _error_code, _msg
