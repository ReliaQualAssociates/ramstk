# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKSubCategory.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKSubCategory Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKSubCategory(RAMSTK_BASE):
    """Class to represent the table ramstk_subcategory in the RAMSTK Common database."""

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
    description = Column(
        'fld_description', String(512), default='Type Description',
    )

    # Define the relationships to other tables in the RAMSTK Program database.
    category = relationship('RAMSTKCategory', back_populates='subcategory')
    mode = relationship(
        'RAMSTKFailureMode', back_populates='subcategory', cascade='delete',
    )

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKSubCategory data model attributes.

        :return: {category_id, subcategory, description} pairs.
        :rtype: dict
        """
        _attributes = {
            'category_id': self.category_id,
            'subcategory_id': self.subcategory_id,
            'description': self.description,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKSubCategory data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKSubCategory {0:d} attributes.". \
            format(self.subcategory_id)

        try:
            self.category_id = int(
                none_to_default(attributes['category_id'], -1),
            )
            self.description = str(
                none_to_default(attributes['description'], ''),
            )
        except KeyError as _err:
            _error_code = 40
            _msg = (
                "RAMSTK ERROR: Missing attribute {0:s} in attribute "
                "dictionary passed to "
                "{1:s}.set_attributes()."
            ).format(
                str(_err),
                self.__class__.__name__,
            )

        return _error_code, _msg
