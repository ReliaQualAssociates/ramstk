#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKDesignMechanic.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKDesignMechanic Package.
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer
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
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKDesignMechanic(Base):
    """
    Class to represent the rtk_design_mechanical table in the RTK Program
    database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_design_mechanic'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    altitude_operating = Column('fld_altitude_operating', Float, default=0.0)
    application_id = Column('fld_application_id', Integer, default=0)
    balance_id = Column('fld_balance_id', Integer, default=0)
    clearance = Column('fld_clearance', Float, default=0.0)
    casing_id = Column('fld_casing_id', Integer, default=0)
    contact_pressure = Column('fld_contact_pressure', Float, default=0.0)
    deflection = Column('fld_deflection', Float, default=0.0)
    diameter_coil = Column('fld_diameter_coil', Float, default=0.0)
    diameter_inner = Column('fld_diameter_inner', Float, default=0.0)
    diameter_outer = Column('fld_diameter_outer', Float, default=0.0)
    diameter_wire = Column('fld_diameter_wire', Float, default=0.0)
    filter_size = Column('fld_filter_size', Float, default=0.0)
    flow_design = Column('fld_flow_design', Float, default=0.0)
    flow_operating = Column('fld_flow_operating', Float, default=0.0)
    frequency_operating = Column('fld_frequency_operating', Float, default=0.0)
    friction = Column('fld_friction', Float, default=0.0)
    impact_id = Column('fld_impact_id', Integer, default=0)
    leakage_allowable = Column('fld_leakage_allowable', Float, default=0.0)
    length = Column('fld_length', Float, default=0.0)
    length_compressed = Column('fld_length_compressed', Float, default=0.0)
    length_relaxed = Column('fld_length_relaxed', Float, default=0.0)
    load_design = Column('fld_load_design', Float, default=0.0)
    load_id = Column('fld_load_id', Integer, default=0)
    load_operating = Column('fld_load_operating', Float, default=0.0)
    lubrication_id = Column('fld_lubrication_id', Integer, default=0)
    manufacturing_id = Column('fld_manufacturing_id', Integer, default=0)
    material_id = Column('fld_material_id', Integer, default=0)
    meyer_hardness = Column('fld_meyer_hardness', Float, default=0.0)
    misalignment_angle = Column('fld_misalignment_angle', Float, default=0.0)
    n_ten = Column('fld_n_ten', Integer, default=0)
    n_cycles = Column('fld_n_cycles', Integer, default=0)
    n_elements = Column('fld_n_elements', Integer, default=0)
    offset = Column('fld_offset', Float, default=0.0)
    particle_size = Column('fld_particle_size', Float, default=0.0)
    pressure_contact = Column('fld_pressure_contact', Float, default=0.0)
    pressure_delta = Column('fld_pressure_delta', Float, default=0.0)
    pressure_downstream = Column('fld_pressure_downstream', Float, default=0.0)
    pressure_rated = Column('fld_pressure_rated', Float, default=0.0)
    pressure_upstream = Column('fld_pressure_upstream', Float, default=0.0)
    rpm_design = Column('fld_rpm_design', Float, default=0.0)
    rpm_operating = Column('fld_rpm_operating', Float, default=0.0)
    service_id = Column('fld_service_id', Integer, default=0)
    spring_index = Column('fld_spring_index', Float, default=0.0)
    surface_finish = Column('fld_surface_finish', Float, default=0.0)
    technology_id = Column('fld_technology_id', Integer, default=0)
    thickness = Column('fld_thickness', Float, default=0.0)
    torque_id = Column('fld_torque_id', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)
    viscosity_design = Column('fld_viscosity_design', Float, default=0.0)
    viscosity_dynamic = Column('fld_viscosity_dynamic', Float, default=0.0)
    water_per_cent = Column('fld_water_per_cent', Float, default=0.0)
    width_minimum = Column('fld_width_minimum', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware',
                            back_populates='design_mechanic')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKDesignElectric data
        model attributes.

        :return: (hardware_id, altitude_operating, application_id, balance_id,
                  clearance, casing_id, contact_pressure, deflection,
                  diameter_coil, diameter_inner, diameter_outer, diameter_wire,
                  filter_size, flow_design, flow_operating,
                  frequency_operating, friction, impact_id, leakage_allowable,
                  length, length_compressed, length_relaxed, load_design,
                  load_id, load_operating, lubrication_id, manufacturing_id,
                  material_id, meyer_hardness, misalignment_angle, n_ten,
                  n_cycles, n_elements, offset, particle_size,
                  pressure_contact, pressure_delta, pressure_downstream,
                  pressure_rated, pressure_upstream, rpm_design, rpm_operating,
                  service_id, spring_index, surface_finish, technology_id,
                  thickness, torque_id, type_id, viscosity_design,
                  viscosity_dynamic, water_per_cent, width_minimum)
        :rtype: tuple
        """

        _attributes = (self.hardware_id, self.altitude_operating,
                       self.application_id, self.balance_id, self.clearance,
                       self.casing_id, self.contact_pressure, self.deflection,
                       self.diameter_coil, self.diameter_inner,
                       self.diameter_outer, self.diameter_wire,
                       self.filter_size, self.flow_design, self.flow_operating,
                       self.frequency_operating, self.friction, self.impact_id,
                       self.leakage_allowable, self.length,
                       self.length_compressed, self.length_relaxed,
                       self.load_design, self.load_id, self.load_operating,
                       self.lubrication_id, self.manufacturing_id,
                       self.material_id, self.meyer_hardness,
                       self.misalignment_angle, self.n_ten, self.n_cycles,
                       self.n_elements, self.offset, self.particle_size,
                       self.pressure_contact, self.pressure_delta,
                       self.pressure_downstream, self.pressure_rated,
                       self.pressure_upstream, self.rpm_design,
                       self.rpm_operating, self.service_id, self.spring_index,
                       self.surface_finish, self.technology_id, self.thickness,
                       self.torque_id, self.type_id, self.viscosity_design,
                       self.viscosity_dynamic, self.water_per_cent,
                       self.width_minimum)

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
        _msg = "RTK SUCCESS: Updating RTKDesignMechanic {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.altitude_operating = float(attributes[0])
            self.application_id = int(attributes[1])
            self.balance_id = int(attributes[2])
            self.clearance = float(attributes[3])
            self.casing_id = int(attributes[4])
            self.contact_pressure = float(attributes[5])
            self.deflection = float(attributes[6])
            self.diameter_coil = float(attributes[7])
            self.diameter_inner = float(attributes[8])
            self.diameter_outer = float(attributes[9])
            self.diameter_wire = float(attributes[10])
            self.filter_size = float(attributes[11])
            self.flow_design = float(attributes[12])
            self.flow_operating = float(attributes[13])
            self.frequency_operating = float(attributes[14])
            self.friction = float(attributes[15])
            self.impact_id = int(attributes[16])
            self.leakage_allowable = float(attributes[17])
            self.length = float(attributes[18])
            self.length_compressed = float(attributes[19])
            self.length_relaxed = float(attributes[20])
            self.load_design = float(attributes[21])
            self.load_id = int(attributes[22])
            self.load_operating = float(attributes[23])
            self.lubrication_id = int(attributes[24])
            self.manufacturing_id = int(attributes[25])
            self.material_id = int(attributes[26])
            self.meyer_hardness = float(attributes[27])
            self.misalignment_angle = float(attributes[28])
            self.n_ten = int(attributes[29])
            self.n_cycles = int(attributes[30])
            self.n_elements = int(attributes[31])
            self.offset = float(attributes[32])
            self.particle_size = float(attributes[33])
            self.pressure_contact = float(attributes[34])
            self.pressure_delta = float(attributes[35])
            self.pressure_downstream = float(attributes[36])
            self.pressure_rated = float(attributes[37])
            self.pressure_upstream = float(attributes[38])
            self.rpm_design = float(attributes[39])
            self.rpm_operating = float(attributes[40])
            self.service_id = int(attributes[41])
            self.spring_index = float(attributes[42])
            self.surface_finish = float(attributes[43])
            self.technology_id = int(attributes[44])
            self.thickness = float(attributes[45])
            self.torque_id = int(attributes[46])
            self.type_id = int(attributes[47])
            self.viscosity_design = float(attributes[48])
            self.viscosity_dynamic = float(attributes[49])
            self.water_per_cent = float(attributes[50])
            self.width_minimum = float(attributes[51])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKDesignMechanic.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKDesignMechanic attributes."

        return _error_code, _msg
