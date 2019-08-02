# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKModel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKModel Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKModel(RAMSTK_BASE):
    """Class to represent ramstk_model in the RAMSTK Common database."""

    __defaults__ = {
        'description': 'Model Description',
        'model_type': 'unknown'
    }
    __tablename__ = 'ramstk_model'
    __table_args__ = {'extend_existing': True}

    model_id = Column(
        'fld_model_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    model_type = Column('fld_model_type',
                        Integer,
                        default=__defaults__['model_type'])

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKModel data model attributes.

        :return: {model_id, description, model_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'model_id': self.model_id,
            'description': self.description,
            'model_type': self.model_type,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKModel attributes.

        .. note:: you should pop the model ID entry from the attributes dict
            before passing it to this method.

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
