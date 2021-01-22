# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.data.storage.RAMSTKHardware.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKHardware Table Module."""

# Standard Library Imports
from datetime import date

# Third Party Imports
from sqlalchemy import (
    Column, Float, ForeignKey, Integer, String, UniqueConstraint
)
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKHardware(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_hardware table in the RAMSTK Program database.

    This table shares a:
        * Many-to-One relationship with ramstk_revision.
        * One-to-Many relationship with ramstk_hazard.
        * One-to-Many relationship with ramstk_modes.
        * One-to-Many relationship with ramstk_similar_item.
        * One-to-One relationship with ramstk_allocation.
        * One-to-One relationship with ramstk_reliability.
        * One-to-One relationship with ramstk_mil_hdbk_f.
        * One-to-One relationship with ramstk_nswc.
        * One-to-One relationship with ramstk_design_electric.
        * One-to-One relationship with ramstk_design_mechanic.
    """

    __defaults__ = {
        'alt_part_number': '',
        'attachments': '',
        'cage_code': '',
        'category_id': 0,
        'comp_ref_des': '',
        'cost': 0.0,
        'cost_failure': 0.0,
        'cost_hour': 0.0,
        'cost_type_id': 0,
        'description': '',
        'duty_cycle': 100.0,
        'figure_number': '',
        'lcn': '',
        'level': 0,
        'manufacturer_id': 0,
        'mission_time': 100.0,
        'name': '',
        'nsn': '',
        'page_number': '',
        'parent_id': 0,
        'part': 0,
        'part_number': '',
        'quantity': 1,
        'ref_des': '',
        'remarks': '',
        'repairable': 0,
        'specification_number': '',
        'subcategory_id': 0,
        'tagged_part': 0,
        'total_cost': 0.0,
        'total_part_count': 0,
        'total_power_dissipation': 0.0,
        'year_of_manufacture': date.today().year
    }
    __tablename__ = 'ramstk_hardware'
    __table_args__ = (UniqueConstraint('fld_revision_id',
                                       'fld_hardware_id',
                                       name='ramstk_hardware_ukey'), {
                                           'extend_existing': True
                                       })

    revision_id = Column('fld_revision_id',
                         Integer,
                         ForeignKey('ramstk_revision.fld_revision_id'),
                         nullable=False)
    hardware_id = Column('fld_hardware_id',
                         Integer,
                         primary_key=True,
                         autoincrement=True,
                         nullable=False)

    alt_part_number = Column('fld_alt_part_number',
                             String(256),
                             default=__defaults__['alt_part_number'])
    attachments = Column('fld_attachments',
                         String(512),
                         default=__defaults__['attachments'])
    cage_code = Column('fld_cage_code',
                       String(256),
                       default=__defaults__['cage_code'])
    category_id = Column('fld_category_id',
                         Integer,
                         default=__defaults__['category_id'])
    comp_ref_des = Column('fld_comp_ref_des',
                          String(256),
                          default=__defaults__['comp_ref_des'])
    cost = Column('fld_cost', Float, default=__defaults__['cost'])
    cost_failure = Column('fld_cost_failure',
                          Float,
                          default=__defaults__['cost_failure'])
    cost_hour = Column('fld_cost_hour',
                       Float,
                       default=__defaults__['cost_hour'])
    cost_type_id = Column('fld_cost_type_id',
                          Integer,
                          default=__defaults__['cost_type_id'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    duty_cycle = Column('fld_duty_cycle',
                        Float,
                        default=__defaults__['duty_cycle'])
    figure_number = Column('fld_figure_number',
                           String(256),
                           default=__defaults__['figure_number'])
    lcn = Column('fld_lcn', String(256), default=__defaults__['lcn'])
    level = Column('fld_level', Integer, default=__defaults__['level'])
    manufacturer_id = Column('fld_manufacturer_id',
                             Integer,
                             default=__defaults__['manufacturer_id'])
    mission_time = Column('fld_mission_time',
                          Float,
                          default=__defaults__['mission_time'])
    name = Column('fld_name', String(256), default=__defaults__['name'])
    nsn = Column('fld_nsn', String(256), default=__defaults__['nsn'])
    page_number = Column('fld_page_number',
                         String(256),
                         default=__defaults__['page_number'])
    parent_id = Column('fld_parent_id',
                       Integer,
                       default=__defaults__['parent_id'])
    part = Column('fld_part', Integer, default=__defaults__['part'])
    part_number = Column('fld_part_number',
                         String(256),
                         default=__defaults__['part_number'])
    quantity = Column('fld_quantity',
                      Integer,
                      default=__defaults__['quantity'])
    ref_des = Column('fld_ref_des',
                     String(256),
                     default=__defaults__['ref_des'])
    remarks = Column('fld_remarks', String, default=__defaults__['remarks'])
    repairable = Column('fld_repairable',
                        Integer,
                        default=__defaults__['repairable'])
    specification_number = Column('fld_specification_number',
                                  String(256),
                                  default=__defaults__['specification_number'])
    subcategory_id = Column('fld_subcategory_id',
                            Integer,
                            default=__defaults__['subcategory_id'])
    tagged_part = Column('fld_tagged_part',
                         Integer,
                         default=__defaults__['tagged_part'])
    total_cost = Column('fld_total_cost',
                        Float,
                        default=__defaults__['total_cost'])
    total_part_count = Column('fld_total_part_count',
                              Integer,
                              default=__defaults__['total_part_count'])
    total_power_dissipation = Column(
        'fld_total_power_dissipation',
        Float,
        default=__defaults__['total_power_dissipation'])
    year_of_manufacture = Column('fld_year_of_manufacture',
                                 Integer,
                                 default=__defaults__['year_of_manufacture'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship(  # type: ignore
        'RAMSTKRevision',
        back_populates='hardware',
    )

    # One-to-one relationships.
    allocation = relationship(  # type: ignore
        'RAMSTKAllocation',
        back_populates='hardware',
        cascade='all,delete',
    )
    sia = relationship(  # type: ignore
        'RAMSTKSimilarItem',
        back_populates='hardware',
        cascade='all,delete',
    )
    reliability = relationship(  # type: ignore
        'RAMSTKReliability',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete',
    )
    milhdbkf = relationship(  # type: ignore
        'RAMSTKMilHdbkF',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete',
    )
    nswc = relationship(  # type: ignore
        'RAMSTKNSWC',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete',
    )
    design_electric = relationship(  # type: ignore
        'RAMSTKDesignElectric',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete',
    )
    design_mechanic = relationship(  # type: ignore
        'RAMSTKDesignMechanic',
        uselist=False,
        back_populates='hardware',
        cascade='all,delete',
    )

    def get_attributes(self):
        """Retrieve the current values of RAMSTKHardware data model attributes.

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
            'alt_part_number': self.alt_part_number,
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
            'year_of_manufacture': self.year_of_manufacture,
        }

        return _attributes
