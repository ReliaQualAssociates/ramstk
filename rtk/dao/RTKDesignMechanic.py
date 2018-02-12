# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKDesignMechanic.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKDesignMechanic Table Module."""  # pragma: no cover


from sqlalchemy import Column, Float, ForeignKey, Integer  # pragma: no cover
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default

from rtk.dao.RTKCommonDB import RTK_BASE  # pragma: no cover


# pylint: disable=R0902
class RTKDesignMechanic(RTK_BASE):
    """
    Represent the rtk_design_mechanic table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_design_mechanic'  # pragma: no cover
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

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
        Retrieve current values of the RTKDesignMechanic data model attributes.

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
            'width_minimum': self.width_minimum
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKDesignMechanic data model attributes.

        :param dict attributes: dict of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKDesignMechanic {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.altitude_operating = float(
                none_to_default(attributes['altitude_operating'], 0.0))
            self.application_id = int(
                none_to_default(attributes['application_id'], 0))
            self.balance_id = int(none_to_default(attributes['balance_id'], 0))
            self.clearance = float(
                none_to_default(attributes['clearance'], 0.0))
            self.casing_id = int(none_to_default(attributes['casing_id'], 0))
            self.contact_pressure = float(
                none_to_default(attributes['contact_pressure'], 0.0))
            self.deflection = float(
                none_to_default(attributes['deflection'], 0.0))
            self.diameter_coil = float(
                none_to_default(attributes['diameter_coil'], 0.0))
            self.diameter_inner = float(
                none_to_default(attributes['diameter_inner'], 0.0))
            self.diameter_outer = float(
                none_to_default(attributes['diameter_outer'], 0.0))
            self.diameter_wire = float(
                none_to_default(attributes['diameter_wire'], 0.0))
            self.filter_size = float(
                none_to_default(attributes['filter_size'], 0.0))
            self.flow_design = float(
                none_to_default(attributes['flow_design'], 0.0))
            self.flow_operating = float(
                none_to_default(attributes['flow_operating'], 0.0))
            self.frequency_operating = float(
                none_to_default(attributes['frequency_operating'], 0.0))
            self.friction = float(none_to_default(attributes['friction'], 0.0))
            self.impact_id = int(none_to_default(attributes['impact_id'], 0))
            self.leakage_allowable = float(
                none_to_default(attributes['leakage_allowable'], 0.0))
            self.length = float(none_to_default(attributes['length'], 0.0))
            self.length_compressed = float(
                none_to_default(attributes['length_compressed'], 0.0))
            self.length_relaxed = float(
                none_to_default(attributes['length_relaxed'], 0.0))
            self.load_design = float(
                none_to_default(attributes['load_design'], 0.0))
            self.load_id = int(none_to_default(attributes['load_id'], 0))
            self.load_operating = float(
                none_to_default(attributes['load_operating'], 0.0))
            self.lubrication_id = int(
                none_to_default(attributes['lubrication_id'], 0))
            self.manufacturing_id = int(
                none_to_default(attributes['manufacturing_id'], 0))
            self.material_id = int(
                none_to_default(attributes['material_id'], 0))
            self.meyer_hardness = float(
                none_to_default(attributes['meyer_hardness'], 0.0))
            self.misalignment_angle = float(
                none_to_default(attributes['misalignment_angle'], 0.0))
            self.n_ten = int(none_to_default(attributes['n_ten'], 0))
            self.n_cycles = int(none_to_default(attributes['n_cycles'], 0))
            self.n_elements = int(none_to_default(attributes['n_elements'], 0))
            self.offset = float(none_to_default(attributes['offset'], 0.0))
            self.particle_size = float(
                none_to_default(attributes['particle_size'], 0.0))
            self.pressure_contact = float(
                none_to_default(attributes['pressure_contact'], 0.0))
            self.pressure_delta = float(
                none_to_default(attributes['pressure_delta'], 0.0))
            self.pressure_downstream = float(
                none_to_default(attributes['pressure_downstream'], 0.0))
            self.pressure_rated = float(
                none_to_default(attributes['pressure_rated'], 0.0))
            self.pressure_upstream = float(
                none_to_default(attributes['pressure_upstream'], 0.0))
            self.rpm_design = float(
                none_to_default(attributes['rpm_design'], 0.0))
            self.rpm_operating = float(
                none_to_default(attributes['rpm_operating'], 0.0))
            self.service_id = int(none_to_default(attributes['service_id'], 0))
            self.spring_index = float(
                none_to_default(attributes['spring_index'], 0.0))
            self.surface_finish = float(
                none_to_default(attributes['surface_finish'], 0.0))
            self.technology_id = int(
                none_to_default(attributes['technology_id'], 0))
            self.thickness = float(
                none_to_default(attributes['thickness'], 0.0))
            self.torque_id = int(none_to_default(attributes['torque_id'], 0))
            self.type_id = int(none_to_default(attributes['type_id'], 0))
            self.viscosity_design = float(
                none_to_default(attributes['viscosity_design'], 0.0))
            self.viscosity_dynamic = float(
                none_to_default(attributes['viscosity_dynamic'], 0.0))
            self.water_per_cent = float(
                none_to_default(attributes['water_per_cent'], 0.0))
            self.width_minimum = float(
                none_to_default(attributes['width_minimum'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKDesignMechanic.set_attributes().".format(_err)

        return _error_code, _msg
