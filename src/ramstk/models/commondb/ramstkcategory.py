# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKCategory.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCategory Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKCategory(RAMSTK_BASE):
    """
    Class to represent the table ramstk_category in the RAMSTK Common database.

    Types of category are:
        # 1. Hardware
        # 2. Risk
        # 3. Software
        # 4. Incident
        # 5. Action
    """

    __tablename__ = 'ramstk_category'
    __table_args__ = {'extend_existing': True}

    category_id = Column(
        'fld_category_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = Column('fld_name', String(256), default='Category Name')
    description = Column(
        'fld_description',
        String(512),
        default='Category Description',
    )
    cat_type = Column('fld_type', String(256), default='unknown')
    value = Column('fld_value', Integer, default=1)
    harsh_ir_limit = Column('fld_harsh_ir_limit', Float, default=0.8)
    mild_ir_limit = Column('fld_mild_ir_limit', Float, default=0.9)
    harsh_pr_limit = Column('fld_harsh_pr_limit', Float, default=1.0)
    mild_pr_limit = Column('fld_mild_pr_limit', Float, default=1.0)
    harsh_vr_limit = Column('fld_harsh_vr_limit', Float, default=1.0)
    mild_vr_limit = Column('fld_mild_vr_limit', Float, default=1.0)
    harsh_deltat_limit = Column('fld_harsh_deltat_limit', Float, default=0.0)
    mild_deltat_limit = Column('fld_mild_deltat_limit', Float, default=0.0)
    harsh_maxt_limit = Column('fld_harsh_maxt_limit', Float, default=125.0)
    mild_maxt_limit = Column('fld_mild_maxt_limit', Float, default=125.0)

    # Define the relationships to other tables in the RAMSTK Program database.
    subcategory = relationship(
        'RAMSTKSubCategory',
        back_populates='category',
        cascade='delete',
    )
    mode = relationship(
        'RAMSTKFailureMode',
        back_populates='category',
        cascade='delete',
    )

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKCategory data model attributes.

        :return: {category_id, name, description, cat_type, value,
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
            'category_type': self.cat_type,
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

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKCategory data model attributes.

        :param dict attributes: dict containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKCategory {0:d} attributes.". \
            format(self.category_id)

        try:
            self.name = str(
                none_to_default(attributes['name'], 'Category Name'), )
            self.description = str(
                none_to_default(
                    attributes['description'],
                    'Category Description',
                ), )
            self.cat_type = str(
                none_to_default(attributes['category_type'], 'unknown'), )
            self.value = int(none_to_default(attributes['value'], 1))
            self.harsh_ir_limit = float(
                none_to_default(attributes['harsh_ir_limit'], 1.0), )
            self.mild_ir_limit = float(
                none_to_default(attributes['mild_ir_limit'], 1.0), )
            self.harsh_pr_limit = float(
                none_to_default(attributes['harsh_pr_limit'], 1.0), )
            self.mild_pr_limit = float(
                none_to_default(attributes['mild_pr_limit'], 1.0), )
            self.harsh_vr_limit = float(
                none_to_default(attributes['harsh_vr_limit'], 1.0), )
            self.mild_vr_limit = float(
                none_to_default(attributes['mild_vr_limit'], 1.0), )
            self.harsh_deltat_limit = float(
                none_to_default(attributes['harsh_deltat_limit'], 1.0), )
            self.mild_deltat_limit = float(
                none_to_default(attributes['mild_deltat_limit'], 1.0), )
            self.harsh_maxt_limit = float(
                none_to_default(attributes['harsh_maxt_limit'], 1.0), )
            self.mild_maxt_limit = float(
                none_to_default(attributes['mild_maxt_limit'], 1.0), )
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKCategory.set_attributes().".format(str(_err))

        return _error_code, _msg
