# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKFailureMode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFailureMode Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKFailureMode(RAMSTK_BASE):
    """Class to represent ramstk_failuremode in the RAMSTK Common database."""

    __defaults__ = {
        'description': 'Failure Mode Description',
        'mode_ratio': 1.0,
        'source': ''
    }
    __tablename__ = 'ramstk_failure_mode'
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
        ForeignKey('ramstk_subcategory.fld_subcategory_id'),
        nullable=False,
    )
    mode_id = Column(
        'fld_failuremode_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column(
        'fld_description',
        String(512),
        default=__defaults__['description'],
    )
    mode_ratio = Column('fld_mode_ratio',
                        Float,
                        default=__defaults__['mode_ratio'])
    source = Column('fld_source', String(128), default=__defaults__['source'])

    # Define the relationships to other tables in the RAMSTK Program database.
    category = relationship('RAMSTKCategory', back_populates='mode')
    subcategory = relationship('RAMSTKSubCategory', back_populates='mode')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKFailureMode data model attributes.

        :return: {failuremode_id, description, type} pairs
        :rtype: dict
        """
        _attributes = {
            'category_id': self.category_id,
            'subcategory_id': self.subcategory_id,
            'mode_id': self.mode_id,
            'description': self.description,
            'mode_ratio': self.mode_ratio,
            'source': self.source,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKFailureMode attributes.

        .. note:: you should pop the category ID, subcategory ID, and
            failuremode ID entries from the attributes dict before passing it
            to this method.

        :param dict attributes: dict of key:value pairs to assign to the
            instance attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(self, _key,
                    none_to_default(attributes[_key], self.__defaults__[_key]))
