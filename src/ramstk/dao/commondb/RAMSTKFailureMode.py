# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKFailureMode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFailureMode Table Module."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKFailureMode(RAMSTK_BASE):
    """Class to represent the table ramstk_failuremode in the RAMSTK Common database."""

    __tablename__ = 'ramstk_failure_mode'
    __table_args__ = {'extend_existing': True}

    category_id = Column(
        'fld_category_id',
        Integer,
        ForeignKey('ramstk_category.fld_category_id'),
        nullable=False)
    subcategory_id = Column(
        'fld_subcategory_id',
        Integer,
        ForeignKey('ramstk_subcategory.fld_subcategory_id'),
        nullable=False)
    mode_id = Column(
        'fld_failuremode_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Failure Mode Decription')
    mode_ratio = Column('fld_mode_ratio', Float, default=1.0)
    source = Column('fld_source', String(128), default='')

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
            'source': self.source
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKFailureMode data model attributes.

        :param dict attributes: dict containing the key:value pairs to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKFailureMode {0:d} attributes.". \
            format(self.mode_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Failure Mode Description'))
            self.mode_ratio = float(
                none_to_default(attributes['mode_ratio'], 1.0))
            self.source = str(none_to_default(attributes['source'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RAMSTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(str(_err),
                                                      self.__class__.__name__)

        return _error_code, _msg
