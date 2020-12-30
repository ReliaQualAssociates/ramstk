# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKSubCategory.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKSubCategory Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKSubCategory(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_subcategory in the RAMSTK Common database."""

    __defaults__ = {'description': 'Subcategory Description'}
    __tablename__ = 'ramstk_subcategory'
    __table_args__ = {'extend_existing': True}

    category_id = Column(
        'fld_category_id',
        Integer,
        ForeignKey('ramstk_category.fld_category_id'),
        nullable=False,
    )
    subcategory_id = Column(
        'fld_subcategory_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])

    # Define the relationships to other tables in the RAMSTK Program database.
    category = relationship(  # type: ignore
        'RAMSTKCategory', back_populates='subcategory')
    mode = relationship(  # type: ignore
        'RAMSTKFailureMode',
        back_populates='subcategory',
        cascade='delete',
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKSubCategory data model attributes.

        :return: {category_id, subcategory, description} pairs.
        :rtype: dict
        """
        _attributes = {
            'category_id': self.category_id,
            'subcategory_id': self.subcategory_id,
            'description': self.description,
        }

        return _attributes
