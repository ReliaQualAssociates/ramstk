# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKHardware.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKHardware Table
===============================================================================
"""

from datetime import date

from sqlalchemy import BLOB, Column, Float, \
                       ForeignKey, Integer, String  # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKHardware(RTK_BASE):
    """
    Class to represent the rtk_hardware table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_hazard.
    This table shares a One-to-Many relationship with rtk_similar_item.
    This table shares a One-to-One relationship with rtk_allocation.
    This table shares a One-to-One relationship with rtk_reliability.
    This table shares a One-to-One relationship with rtk_mil_hdbk_f.
    This table shares a One-to-One relationship with rtk_nswc.
    This table shares a One-to-One relationship with rtk_design_electric.
    This table shares a One-to-One relationship with rtk_design_mechanic.
    """

    __tablename__ = 'rtk_hardware'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    hardware_id = Column('fld_hardware_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

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
    specification_number = Column('fld_specification_number', String(256),
                                  default='')
    subcategory_id = Column('fld_subcategory_id', Integer, default=0)
    tagged_part = Column('fld_tagged_part', Integer, default=0)
    total_part_count = Column('fld_total_part_count', Integer, default=0)
    total_power_dissipation = Column('fld_total_power_dissipation', Float,
                                     default=0.0)
    year_of_manufacture = Column('fld_year_of_manufacture', Integer,
                                 default=date.today().year)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='hardware')

    # One-to-one relationships.
    allocation = relationship('RTKAllocation', back_populates='hardware')
    hazard = relationship('RTKHazardAnalysis', back_populates='hardware')
    sia = relationship('RTKSimilarItem', back_populates='hardware')
    mode = relationship('RTKMode', back_populates='hardware')

    reliability = relationship('RTKReliability', uselist=False,
                               back_populates='hardware')
    milhdbkf = relationship('RTKMilHdbkF', uselist=False,
                            back_populates='hardware')
    nswc = relationship('RTKNSWC', uselist=False,
                        back_populates='hardware')
    design_electric = relationship('RTKDesignElectric', uselist=False,
                                   back_populates='hardware')
    design_mechanic = relationship('RTKDesignMechanic', uselist=False,
                                   back_populates='hardware')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKHardware data model
        attributes.

        :return: (revision_id, hardware_id, alt_part_number, attachments,
                  cage_code, category_id, comp_ref_des, cost, cost_failure,
                  cost_hour, cost_type_id, description, duty_cycle,
                  figure_number, lcn, level, manufacturer_id, mission_time,
                  name, nsn, page_number, parent_id, part, part_number,
                  quantity, ref_des, remarks, repairable, specification_number,
                  subcategory_id, tagged_part, total_part_count,
                  total_power_dissipation, year_of_manufacture)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.hardware_id,
                       self.alt_part_number, self.attachments, self.cage_code,
                       self.category_id, self.comp_ref_des, self.cost,
                       self.cost_failure, self.cost_hour, self.cost_type_id,
                       self.description, self.duty_cycle, self.figure_number,
                       self.lcn, self.level, self.manufacturer_id,
                       self.mission_time, self.name, self.nsn,
                       self.page_number, self.parent_id, self.part,
                       self.part_number, self.quantity, self.ref_des,
                       self.remarks, self.repairable,
                       self.specification_number, self.subcategory_id,
                       self.tagged_part, self.total_part_count,
                       self.total_power_dissipation, self.year_of_manufacture)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKHardware data model attributes.

        :param tuple attributes: tuple of attribute values to assign to the
                                 Hardware instance attributes.
        :return: (_code, _msg; the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKHardware {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.alt_part_number = str(none_to_default(attributes[0], ''))
            self.attachments = str(none_to_default(attributes[1], ''))
            self.cage_code = str(none_to_default(attributes[2], ''))
            self.category_id = int(none_to_default(attributes[3], 0))
            self.comp_ref_des = str(none_to_default(attributes[4], ''))
            self.cost = float(none_to_default(attributes[5], 0.0))
            self.cost_failure = float(none_to_default(attributes[6], 0.0))
            self.cost_hour = float(none_to_default(attributes[7], 0.0))
            self.cost_type_id = int(none_to_default(attributes[8], 0))
            self.description = str(none_to_default(attributes[9], ''))
            self.duty_cycle = float(none_to_default(attributes[10], 100.0))
            self.figure_number = str(none_to_default(attributes[11], ''))
            self.lcn = str(none_to_default(attributes[12], ''))
            self.level = int(none_to_default(attributes[13], 0))
            self.manufacturer_id = int(none_to_default(attributes[14], 0))
            self.mission_time = float(none_to_default(attributes[15], 100.0))
            self.name = str(none_to_default(attributes[16], ''))
            self.nsn = str(none_to_default(attributes[17], ''))
            self.page_number = str(none_to_default(attributes[18], ''))
            self.parent_id = int(none_to_default(attributes[19], 0))
            self.part = int(none_to_default(attributes[20], 0))
            self.part_number = str(none_to_default(attributes[21], ''))
            self.quantity = int(none_to_default(attributes[22], 1))
            self.ref_des = str(none_to_default(attributes[23], ''))
            self.remarks = str(none_to_default(attributes[24], ''))
            self.repairable = int(none_to_default(attributes[25], 0))
            self.specification_number = str(none_to_default(attributes[26],
                                                            ''))
            self.subcategory_id = int(none_to_default(attributes[27], 0))
            self.tagged_part = int(none_to_default(attributes[28], 0))
            self.total_part_count = int(none_to_default(attributes[29], 0))
            self.total_power_dissipation = float(
                none_to_default(attributes[30], 0.0))
            self.year_of_manufacture = int(none_to_default(attributes[31],
                                                           date.today().year))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKHardware.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKHardware attributes."

        return _error_code, _msg
