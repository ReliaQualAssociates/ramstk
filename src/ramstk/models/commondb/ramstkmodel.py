# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKModel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKModel Table Module."""

# Standard Library Imports
from typing import Dict

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKModel(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_model in the RAMSTK Common database."""

    __defaults__ = {'description': 'Model Description', 'model_type': 0}
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

    def get_attributes(self) -> Dict[str, object]:
        """Retrieve current values of the RAMSTKModel data model attributes.

        :return: {model_id, description, model_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'model_id': self.model_id,
            'description': self.description,
            'model_type': self.model_type,
        }

        return _attributes
