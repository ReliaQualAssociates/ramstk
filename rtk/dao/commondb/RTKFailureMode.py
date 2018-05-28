# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKFailureMode.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKFailureMode Table Module."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKFailureMode(RTK_BASE):
    """Class to represent the table rtk_failuremode in the RTK Common database."""

    __tablename__ = 'rtk_failure_mode'
    __table_args__ = {'extend_existing': True}

    category_id = Column(
        'fld_category_id',
        Integer,
        ForeignKey('rtk_category.fld_category_id'),
        nullable=False)
    subcategory_id = Column(
        'fld_subcategory_id',
        Integer,
        ForeignKey('rtk_subcategory.fld_subcategory_id'),
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

    # Define the relationships to other tables in the RTK Program database.
    category = relationship('RTKCategory', back_populates='mode')
    subcategory = relationship('RTKSubCategory', back_populates='mode')

    def get_attributes(self):
        """
        Retrieve current values of the RTKFailureMode data model attributes.

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
        Set the current values of the RTKFailureMode data model attributes.

        :param dict attributes: dict containing the key:value pairs to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKFailureMode {0:d} attributes.". \
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
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
