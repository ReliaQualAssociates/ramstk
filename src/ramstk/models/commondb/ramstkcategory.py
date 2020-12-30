# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKCategory.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCategory Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKCategory(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_category in the RAMSTK Common database.

    Types of category are:     # 1. Hardware     # 2. Risk     # 3.
    Software     # 4. Incident     # 5. Action
    """

    __defaults__ = {
        'name': 'Category Name',
        'description': 'Category Description',
        'category_type': 'unknown',
        'value': 1,
        'harsh_ir_limit': 0.8,
        'mild_ir_limit': 0.9,
        'harsh_pr_limit': 1.0,
        'mild_pr_limit': 1.0,
        'harsh_vr_limit': 1.0,
        'mild_vr_limit': 1.0,
        'harsh_deltat_limit': 0.0,
        'mild_deltat_limit': 0.0,
        'harsh_maxt_limit': 125.0,
        'mild_maxt_limit': 125.0
    }
    __tablename__ = 'ramstk_category'
    __table_args__ = {'extend_existing': True}

    category_id = Column(
        'fld_category_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = Column('fld_name', String(256), default=__defaults__['name'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    category_type = Column('fld_category_type',
                           String(256),
                           default=__defaults__['category_type'])
    value = Column('fld_value', Integer, default=__defaults__['value'])
    harsh_ir_limit = Column('fld_harsh_ir_limit',
                            Float,
                            default=__defaults__['harsh_ir_limit'])
    mild_ir_limit = Column('fld_mild_ir_limit',
                           Float,
                           default=__defaults__['mild_ir_limit'])
    harsh_pr_limit = Column('fld_harsh_pr_limit',
                            Float,
                            default=__defaults__['harsh_pr_limit'])
    mild_pr_limit = Column('fld_mild_pr_limit',
                           Float,
                           default=__defaults__['mild_pr_limit'])
    harsh_vr_limit = Column('fld_harsh_vr_limit',
                            Float,
                            default=__defaults__['harsh_vr_limit'])
    mild_vr_limit = Column('fld_mild_vr_limit',
                           Float,
                           default=__defaults__['mild_vr_limit'])
    harsh_deltat_limit = Column('fld_harsh_deltat_limit',
                                Float,
                                default=__defaults__['harsh_deltat_limit'])
    mild_deltat_limit = Column('fld_mild_deltat_limit',
                               Float,
                               default=__defaults__['mild_deltat_limit'])
    harsh_maxt_limit = Column('fld_harsh_maxt_limit',
                              Float,
                              default=__defaults__['harsh_maxt_limit'])
    mild_maxt_limit = Column('fld_mild_maxt_limit',
                             Float,
                             default=__defaults__['mild_maxt_limit'])

    # Define the relationships to other tables in the RAMSTK Program database.
    subcategory = relationship(  # type: ignore
        'RAMSTKSubCategory',
        back_populates='category',
        cascade='delete',
    )
    mode = relationship(  # type: ignore
        'RAMSTKFailureMode',
        back_populates='category',
        cascade='delete',
    )

    def get_attributes(self):
        """Retrieve current values of the RAMSTKCategory data model attributes.

        :return: {category_id, name, description, category_type, value,
                  harsh_ir_limit, mild_ir_limit, harsh_pr_limit,
                  mild_pr_limit, harsh_vr_limit, mild_vr_limit,
                  harsh_deltat_limit, mild_deltat_limit, harsh_maxt_limit,
                  mild_maxt_limit} pairs
        :rtype: dict
        """
        _attributes = {
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'category_type': self.category_type,
            'value': self.value,
            'harsh_ir_limit': self.harsh_ir_limit,
            'mild_ir_limit': self.mild_ir_limit,
            'harsh_pr_limit': self.harsh_pr_limit,
            'mild_pr_limit': self.mild_pr_limit,
            'harsh_vr_limit': self.harsh_vr_limit,
            'mild_vr_limit': self.mild_vr_limit,
            'harsh_deltat_limit': self.harsh_deltat_limit,
            'mild_deltat_limit': self.mild_deltat_limit,
            'harsh_maxt_limit': self.harsh_maxt_limit,
            'mild_maxt_limit': self.mild_maxt_limit,
        }

        return _attributes
