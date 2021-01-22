# pylint: disable=duplicate-code, too-many-instance-attributes
# -*- coding: utf-8 -*-
#
#       ramstk.data.storage.RAMSTKDesignMechanic.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKDesignMechanic Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKDesignMechanic(RAMSTK_BASE, RAMSTKBaseTable):
    """Represent ramstk_design_mechanic table in the RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __defaults__ = {
        'altitude_operating': 0.0,
        'application_id': 0,
        'balance_id': 0,
        'clearance': 0.0,
        'casing_id': 0,
        'contact_pressure': 0.0,
        'deflection': 0.0,
        'diameter_coil': 0.0,
        'diameter_inner': 0.0,
        'diameter_outer': 0.0,
        'diameter_wire': 0.0,
        'filter_size': 0.0,
        'flow_design': 0.0,
        'flow_operating': 0.0,
        'frequency_operating': 0.0,
        'friction': 0.0,
        'impact_id': 0,
        'leakage_allowable': 0.0,
        'length': 0.0,
        'length_compressed': 0.0,
        'length_relaxed': 0.0,
        'load_design': 0.0,
        'load_id': 0,
        'load_operating': 0.0,
        'lubrication_id': 0,
        'manufacturing_id': 0,
        'material_id': 0,
        'meyer_hardness': 0.0,
        'misalignment_angle': 0.0,
        'n_ten': 0,
        'n_cycles': 0,
        'n_elements': 0,
        'offset': 0.0,
        'particle_size': 0.0,
        'pressure_contact': 0.0,
        'pressure_delta': 0.0,
        'pressure_downstream': 0.0,
        'pressure_rated': 0.0,
        'pressure_upstream': 0.0,
        'rpm_design': 0.0,
        'rpm_operating': 0.0,
        'service_id': 0,
        'spring_index': 0.0,
        'surface_finish': 0.0,
        'technology_id': 0,
        'thickness': 0.0,
        'torque_id': 0,
        'type_id': 0,
        'viscosity_design': 0.0,
        'viscosity_dynamic': 0.0,
        'water_per_cent': 0.0,
        'width_minimum': 0.0
    }
    __tablename__ = 'ramstk_design_mechanic'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False,
    )

    altitude_operating = Column('fld_altitude_operating',
                                Float,
                                default=__defaults__['altitude_operating'])
    application_id = Column('fld_application_id',
                            Integer,
                            default=__defaults__['application_id'])
    balance_id = Column('fld_balance_id',
                        Integer,
                        default=__defaults__['balance_id'])
    clearance = Column('fld_clearance',
                       Float,
                       default=__defaults__['clearance'])
    casing_id = Column('fld_casing_id',
                       Integer,
                       default=__defaults__['casing_id'])
    contact_pressure = Column('fld_contact_pressure',
                              Float,
                              default=__defaults__['contact_pressure'])
    deflection = Column('fld_deflection',
                        Float,
                        default=__defaults__['deflection'])
    diameter_coil = Column('fld_diameter_coil',
                           Float,
                           default=__defaults__['diameter_coil'])
    diameter_inner = Column('fld_diameter_inner',
                            Float,
                            default=__defaults__['diameter_inner'])
    diameter_outer = Column('fld_diameter_outer',
                            Float,
                            default=__defaults__['diameter_outer'])
    diameter_wire = Column('fld_diameter_wire',
                           Float,
                           default=__defaults__['diameter_wire'])
    filter_size = Column('fld_filter_size',
                         Float,
                         default=__defaults__['filter_size'])
    flow_design = Column('fld_flow_design',
                         Float,
                         default=__defaults__['flow_design'])
    flow_operating = Column('fld_flow_operating',
                            Float,
                            default=__defaults__['flow_operating'])
    frequency_operating = Column('fld_frequency_operating',
                                 Float,
                                 default=__defaults__['frequency_operating'])
    friction = Column('fld_friction', Float, default=__defaults__['friction'])
    impact_id = Column('fld_impact_id',
                       Integer,
                       default=__defaults__['impact_id'])
    leakage_allowable = Column('fld_leakage_allowable',
                               Float,
                               default=__defaults__['leakage_allowable'])
    length = Column('fld_length', Float, default=__defaults__['length'])
    length_compressed = Column('fld_length_compressed',
                               Float,
                               default=__defaults__['length_compressed'])
    length_relaxed = Column('fld_length_relaxed',
                            Float,
                            default=__defaults__['length_relaxed'])
    load_design = Column('fld_load_design',
                         Float,
                         default=__defaults__['load_design'])
    load_id = Column('fld_load_id', Integer, default=__defaults__['load_id'])
    load_operating = Column('fld_load_operating',
                            Float,
                            default=__defaults__['load_operating'])
    lubrication_id = Column('fld_lubrication_id',
                            Integer,
                            default=__defaults__['lubrication_id'])
    manufacturing_id = Column('fld_manufacturing_id',
                              Integer,
                              default=__defaults__['manufacturing_id'])
    material_id = Column('fld_material_id',
                         Integer,
                         default=__defaults__['material_id'])
    meyer_hardness = Column('fld_meyer_hardness',
                            Float,
                            default=__defaults__['meyer_hardness'])
    misalignment_angle = Column('fld_misalignment_angle',
                                Float,
                                default=__defaults__['misalignment_angle'])
    n_ten = Column('fld_n_ten', Integer, default=__defaults__['n_ten'])
    n_cycles = Column('fld_n_cycles',
                      Integer,
                      default=__defaults__['n_cycles'])
    n_elements = Column('fld_n_elements',
                        Integer,
                        default=__defaults__['n_elements'])
    offset = Column('fld_offset', Float, default=__defaults__['offset'])
    particle_size = Column('fld_particle_size',
                           Float,
                           default=__defaults__['particle_size'])
    pressure_contact = Column('fld_pressure_contact',
                              Float,
                              default=__defaults__['pressure_contact'])
    pressure_delta = Column('fld_pressure_delta',
                            Float,
                            default=__defaults__['pressure_delta'])
    pressure_downstream = Column('fld_pressure_downstream',
                                 Float,
                                 default=__defaults__['pressure_downstream'])
    pressure_rated = Column('fld_pressure_rated',
                            Float,
                            default=__defaults__['pressure_rated'])
    pressure_upstream = Column('fld_pressure_upstream',
                               Float,
                               default=__defaults__['pressure_upstream'])
    rpm_design = Column('fld_rpm_design',
                        Float,
                        default=__defaults__['rpm_design'])
    rpm_operating = Column('fld_rpm_operating',
                           Float,
                           default=__defaults__['rpm_operating'])
    service_id = Column('fld_service_id',
                        Integer,
                        default=__defaults__['service_id'])
    spring_index = Column('fld_spring_index',
                          Float,
                          default=__defaults__['spring_index'])
    surface_finish = Column('fld_surface_finish',
                            Float,
                            default=__defaults__['surface_finish'])
    technology_id = Column('fld_technology_id',
                           Integer,
                           default=__defaults__['technology_id'])
    thickness = Column('fld_thickness',
                       Float,
                       default=__defaults__['thickness'])
    torque_id = Column('fld_torque_id',
                       Integer,
                       default=__defaults__['torque_id'])
    type_id = Column('fld_type_id', Integer, default=__defaults__['type_id'])
    viscosity_design = Column('fld_viscosity_design',
                              Float,
                              default=__defaults__['viscosity_design'])
    viscosity_dynamic = Column('fld_viscosity_dynamic',
                               Float,
                               default=__defaults__['viscosity_dynamic'])
    water_per_cent = Column('fld_water_per_cent',
                            Float,
                            default=__defaults__['water_per_cent'])
    width_minimum = Column('fld_width_minimum',
                           Float,
                           default=__defaults__['width_minimum'])

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship(  # type: ignore
        'RAMSTKHardware', back_populates='design_mechanic')

    def get_attributes(self):
        """Retrieve current values of RAMSTKDesignMechanic model attributes.

        :return: {hardware_id, altitude_operating, application_id, balance_id,
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
                  viscosity_dynamic, water_per_cent, width_minimum} pairs.
        :rtype: dict
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'altitude_operating': self.altitude_operating,
            'application_id': self.application_id,
            'balance_id': self.balance_id,
            'clearance': self.clearance,
            'casing_id': self.casing_id,
            'contact_pressure': self.contact_pressure,
            'deflection': self.deflection,
            'diameter_coil': self.diameter_coil,
            'diameter_inner': self.diameter_inner,
            'diameter_outer': self.diameter_outer,
            'diameter_wire': self.diameter_wire,
            'filter_size': self.filter_size,
            'flow_design': self.flow_design,
            'flow_operating': self.flow_operating,
            'frequency_operating': self.frequency_operating,
            'friction': self.friction,
            'impact_id': self.impact_id,
            'leakage_allowable': self.leakage_allowable,
            'length': self.length,
            'length_compressed': self.length_compressed,
            'length_relaxed': self.length_relaxed,
            'load_design': self.load_design,
            'load_id': self.load_id,
            'load_operating': self.load_operating,
            'lubrication_id': self.lubrication_id,
            'manufacturing_id': self.manufacturing_id,
            'material_id': self.material_id,
            'meyer_hardness': self.meyer_hardness,
            'misalignment_angle': self.misalignment_angle,
            'n_ten': self.n_ten,
            'n_cycles': self.n_cycles,
            'n_elements': self.n_elements,
            'offset': self.offset,
            'particle_size': self.particle_size,
            'pressure_contact': self.pressure_contact,
            'pressure_delta': self.pressure_delta,
            'pressure_downstream': self.pressure_downstream,
            'pressure_rated': self.pressure_rated,
            'pressure_upstream': self.pressure_upstream,
            'rpm_design': self.rpm_design,
            'rpm_operating': self.rpm_operating,
            'service_id': self.service_id,
            'spring_index': self.spring_index,
            'surface_finish': self.surface_finish,
            'technology_id': self.technology_id,
            'thickness': self.thickness,
            'torque_id': self.torque_id,
            'type_id': self.type_id,
            'viscosity_design': self.viscosity_design,
            'viscosity_dynamic': self.viscosity_dynamic,
            'water_per_cent': self.water_per_cent,
            'width_minimum': self.width_minimum,
        }

        return _attributes
