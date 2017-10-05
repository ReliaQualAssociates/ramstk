# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKDesignMechanic.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKDesignMechanic Table
===============================================================================
"""

from sqlalchemy import Column, Float, \
                       ForeignKey, Integer          # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


# pylint: disable=R0902
class RTKDesignMechanic(RTK_BASE):
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
            self.altitude_operating = float(none_to_default(attributes[0],
                                                            0.0))
            self.application_id = int(none_to_default(attributes[1], 0))
            self.balance_id = int(none_to_default(attributes[2], 0))
            self.clearance = float(none_to_default(attributes[3], 0.0))
            self.casing_id = int(none_to_default(attributes[4], 0))
            self.contact_pressure = float(none_to_default(attributes[5], 0.0))
            self.deflection = float(none_to_default(attributes[6], 0.0))
            self.diameter_coil = float(none_to_default(attributes[7], 0.0))
            self.diameter_inner = float(none_to_default(attributes[8], 0.0))
            self.diameter_outer = float(none_to_default(attributes[9], 0.0))
            self.diameter_wire = float(none_to_default(attributes[10], 0.0))
            self.filter_size = float(none_to_default(attributes[11], 0.0))
            self.flow_design = float(none_to_default(attributes[12], 0.0))
            self.flow_operating = float(none_to_default(attributes[13], 0.0))
            self.frequency_operating = float(none_to_default(attributes[14],
                                                             0.0))
            self.friction = float(none_to_default(attributes[15], 0.0))
            self.impact_id = int(none_to_default(attributes[16], 0))
            self.leakage_allowable = float(none_to_default(attributes[17],
                                                           0.0))
            self.length = float(none_to_default(attributes[18], 0.0))
            self.length_compressed = float(none_to_default(attributes[19],
                                                           0.0))
            self.length_relaxed = float(none_to_default(attributes[20], 0.0))
            self.load_design = float(none_to_default(attributes[21], 0.0))
            self.load_id = int(none_to_default(attributes[22], 0))
            self.load_operating = float(none_to_default(attributes[23], 0.0))
            self.lubrication_id = int(none_to_default(attributes[24], 0))
            self.manufacturing_id = int(none_to_default(attributes[25], 0))
            self.material_id = int(none_to_default(attributes[26], 0))
            self.meyer_hardness = float(none_to_default(attributes[27], 0.0))
            self.misalignment_angle = float(none_to_default(attributes[28],
                                                            0.0))
            self.n_ten = int(none_to_default(attributes[29], 0))
            self.n_cycles = int(none_to_default(attributes[30], 0))
            self.n_elements = int(none_to_default(attributes[31], 0))
            self.offset = float(none_to_default(attributes[32], 0.0))
            self.particle_size = float(none_to_default(attributes[33], 0.0))
            self.pressure_contact = float(none_to_default(attributes[34], 0.0))
            self.pressure_delta = float(none_to_default(attributes[35], 0.0))
            self.pressure_downstream = float(none_to_default(attributes[36],
                                                             0.0))
            self.pressure_rated = float(none_to_default(attributes[37], 0.0))
            self.pressure_upstream = float(none_to_default(attributes[38],
                                                           0.0))
            self.rpm_design = float(none_to_default(attributes[39], 0.0))
            self.rpm_operating = float(none_to_default(attributes[40], 0.0))
            self.service_id = int(none_to_default(attributes[41], 0))
            self.spring_index = float(none_to_default(attributes[42], 0.0))
            self.surface_finish = float(none_to_default(attributes[43], 0.0))
            self.technology_id = int(none_to_default(attributes[44], 0))
            self.thickness = float(none_to_default(attributes[45], 0.0))
            self.torque_id = int(none_to_default(attributes[46], 0))
            self.type_id = int(none_to_default(attributes[47], 0))
            self.viscosity_design = float(none_to_default(attributes[48], 0.0))
            self.viscosity_dynamic = float(none_to_default(attributes[49],
                                                           0.0))
            self.water_per_cent = float(none_to_default(attributes[50], 0.0))
            self.width_minimum = float(none_to_default(attributes[51], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKDesignMechanic.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKDesignMechanic attributes."

        return _error_code, _msg
