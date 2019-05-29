# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKHardware.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKHardware Table Module."""  # pragma: no cover

from datetime import date  # pragma: no cover

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKHardware(RAMSTK_BASE):
    """
    Class to represent the ramstk_hardware table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a One-to-Many relationship with ramstk_hazard.
    This table shares a One-to-Many relationship with ramstk_similar_item.
    This table shares a One-to-One relationship with ramstk_allocation.
    This table shares a One-to-One relationship with ramstk_reliability.
    This table shares a One-to-One relationship with ramstk_mil_hdbk_f.
    This table shares a One-to-One relationship with ramstk_nswc.
    This table shares a One-to-One relationship with ramstk_design_electric.
    This table shares a One-to-One relationship with ramstk_design_mechanic.
    """

    __tablename__ = 'ramstk_hardware'
    __table_args__ = {'extend_existing': True}  # pragma: no cover

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    alt_part_number = Column('fld_alt_part_number', String(256), default='')
    attachments = Column('fld_attachments', String(512), default='')
    cage_code = Column('fld_cage_code', String(256), default='')
    category_id = Column('fld_category_id', Integer, default=0)
    comp_ref_des = Column('fld_comp_ref_des', String(256), default='')
    cost = Column('fld_cost', Float, default=0.0)
    cost_failure = Column('fld_cost_failure', Float, default=0.0)
    cost_hour = Column('fld_cost_hour', Float, default=0.0)
    cost_type_id = Column('fld_cost_Type_id', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    duty_cycle = Column('fld_duty_cycle', Float, default=100.0)
    figure_number = Column('fld_figure_number', String(256), default='')
    lcn = Column('fld_lcn', String(256), default='')
    level = Column('fld_level', Integer, default=0)
    manufacturer_id = Column('fld_manufacturer_id', Integer, default=0)
    mission_time = Column('fld_mission_time', Float, default=100.0)
    name = Column('fld_name', String(256), default='')
    nsn = Column('fld_nsn', String(256), default='')
    page_number = Column('fld_page_number', String(256), default='')
    parent_id = Column('fld_parent_id', Integer, default=0)
    part = Column('fld_part', Integer, default=0)
    part_number = Column('fld_part_number', String(256), default='')
    quantity = Column('fld_quantity', Integer, default=1)
    ref_des = Column('fld_ref_des', String(256), default='')
    remarks = Column('fld_remarks', BLOB, default='')
    repairable = Column('fld_repairable', Integer, default=0)
    specification_number = Column(
        'fld_specification_number', String(256), default='')
    subcategory_id = Column('fld_subcategory_id', Integer, default=0)
    tagged_part = Column('fld_tagged_part', Integer, default=0)
    total_cost = Column('fld_total_cost', Float, default=0.0)
    total_part_count = Column('fld_total_part_count', Integer, default=0)
    total_power_dissipation = Column(
        'fld_total_power_dissipation', Float, default=0.0)
    year_of_manufacture = Column(
        'fld_year_of_manufacture', Integer, default=date.today().year)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='hardware')

    # One-to-one relationships.
    allocation = relationship(
        'RAMSTKAllocation', back_populates='hardware', cascade='all,delete')
    hazard = relationship(
        'RAMSTKHazardAnalysis',
        back_populates='hardware',
        cascade='all,delete')
    sia = relationship(
        'RAMSTKSimilarItem', back_populates='hardware', cascade='all,delete')
    mode = relationship(
        'RAMSTKMode', back_populates='hardware', cascade='all,delete')

    reliability = relationship(
        'RAMSTKReliability',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete')
    milhdbkf = relationship(
        'RAMSTKMilHdbkF',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete')
    nswc = relationship(
        'RAMSTKNSWC',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete')
    design_electric = relationship(
        'RAMSTKDesignElectric',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete')
    design_mechanic = relationship(
        'RAMSTKDesignMechanic',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKHardware data model attributes.

        :return: {revision_id, hardware_id, alt_part_number, attachments,
                  cage_code, category_id, comp_ref_des, cost, cost_failure,
                  cost_hour, cost_type_id, description, duty_cycle,
                  figure_number, lcn, level, manufacturer_id, mission_time,
                  name, nsn, page_number, parent_id, part, part_number,
                  quantity, ref_des, remarks, repairable, specification_number,
                  subcategory_id, tagged_part, total_cost, total_part_count,
                  total_power_dissipation, year_of_manufacture} pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'hardware_id': self.hardware_id,
            'alt_part_num': self.alt_part_number,
            'attachments': self.attachments,
            'cage_code': self.cage_code,
            'category_id': self.category_id,
            'comp_ref_des': self.comp_ref_des,
            'cost': self.cost,
            'cost_failure': self.cost_failure,
            'cost_hour': self.cost_hour,
            'cost_type_id': self.cost_type_id,
            'description': self.description,
            'duty_cycle': self.duty_cycle,
            'figure_number': self.figure_number,
            'lcn': self.lcn,
            'level': self.level,
            'manufacturer_id': self.manufacturer_id,
            'mission_time': self.mission_time,
            'name': self.name,
            'nsn': self.nsn,
            'page_number': self.page_number,
            'parent_id': self.parent_id,
            'part': self.part,
            'part_number': self.part_number,
            'quantity': self.quantity,
            'ref_des': self.ref_des,
            'remarks': self.remarks,
            'repairable': self.repairable,
            'specification_number': self.specification_number,
            'subcategory_id': self.subcategory_id,
            'tagged_part': self.tagged_part,
            'total_cost': self.total_cost,
            'total_part_count': self.total_part_count,
            'total_power_dissipation': self.total_power_dissipation,
            'year_of_manufacture': self.year_of_manufacture
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKHardware data model attributes.

        :param tuple attributes: tuple of attribute values to assign to the
                                 Hardware instance attributes.
        :return: (_code, _msg; the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKHardware {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.alt_part_number = str(
                none_to_default(attributes['alt_part_num'], ''))
            self.attachments = str(
                none_to_default(attributes['attachments'], ''))
            self.cage_code = str(none_to_default(attributes['cage_code'], ''))
            self.category_id = int(
                none_to_default(attributes['category_id'], 0))
            self.comp_ref_des = str(
                none_to_default(attributes['comp_ref_des'], ''))
            self.cost = float(none_to_default(attributes['cost'], 0.0))
            self.cost_failure = float(
                none_to_default(attributes['cost_failure'], 0.0))
            self.cost_hour = float(
                none_to_default(attributes['cost_hour'], 0.0))
            self.cost_type_id = int(
                none_to_default(attributes['cost_type_id'], 0))
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.duty_cycle = float(
                none_to_default(attributes['duty_cycle'], 100.0))
            self.figure_number = str(
                none_to_default(attributes['figure_number'], ''))
            self.lcn = str(none_to_default(attributes['lcn'], ''))
            self.level = int(none_to_default(attributes['level'], 0))
            self.manufacturer_id = int(
                none_to_default(attributes['manufacturer_id'], 0))
            self.mission_time = float(
                none_to_default(attributes['mission_time'], 100.0))
            self.name = str(none_to_default(attributes['name'], ''))
            self.nsn = str(none_to_default(attributes['nsn'], ''))
            self.page_number = str(
                none_to_default(attributes['page_number'], ''))
            self.parent_id = int(none_to_default(attributes['parent_id'], 0))
            self.part = int(none_to_default(attributes['part'], 0))
            self.part_number = str(
                none_to_default(attributes['part_number'], ''))
            self.quantity = int(none_to_default(attributes['quantity'], 1))
            self.ref_des = str(none_to_default(attributes['ref_des'], ''))
            self.remarks = str(none_to_default(attributes['remarks'], ''))
            self.repairable = int(none_to_default(attributes['repairable'], 0))
            self.specification_number = str(
                none_to_default(attributes['specification_number'], ''))
            self.subcategory_id = int(
                none_to_default(attributes['subcategory_id'], 0))
            self.tagged_part = int(
                none_to_default(attributes['tagged_part'], 0))
            self.total_cost = float(
                none_to_default(attributes['total_cost'], 0.0))
            self.total_part_count = int(
                none_to_default(attributes['total_part_count'], 0))
            self.total_power_dissipation = float(
                none_to_default(attributes['total_power_dissipation'], 0.0))
            self.year_of_manufacture = int(
                none_to_default(attributes['year_of_manufacture'],
                                date.today().year))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKHardware.set_attributes().".format(_err)

        return _error_code, _msg
