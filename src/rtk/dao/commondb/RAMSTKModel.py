# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RAMSTKModel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RAMSTKModel Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKModel(RAMSTK_BASE):
    """Class to represent the table rtk_model in the RAMSTK Common database."""

    __tablename__ = 'rtk_model'
    __table_args__ = {'extend_existing': True}

    model_id = Column(
        'fld_model_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Model Description')
    model_type = Column('fld_type', Integer, default='unknown')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKModel data model attributes.

        :return: {model_id, description, model_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'model_id': self.model_id,
            'description': self.description,
            'model_type': self.model_type
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKModel data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKModel {0:d} attributes.". \
            format(self.model_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Model Description'))
            self.model_type = str(
                none_to_default(attributes['model_type'], 'unkown'))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RAMSTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
