# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKMeasurement.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMeasurement Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKMeasurement(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_measurement in the RAMSTK Common database."""

    __defaults__ = {
        'code': 'Measurement Code',
        'description': 'Measurement Description',
        'measurement_type': 'unknown'
    }
    __tablename__ = 'ramstk_measurement'
    __table_args__ = {'extend_existing': True}

    measurement_id = Column(
        'fld_measurement_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    code = Column('fld_code', String(128), default=__defaults__['code'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    measurement_type = Column('fld_type',
                              String(128),
                              default=__defaults__['measurement_type'])

    def get_attributes(self):
        """Retrieve current values of RAMSTKMeasurement data model attributes.

        :return: {measurement_id, description} pairs.
        :rtype: dict
        """
        _attributes = {
            'measurement_id': self.measurement_id,
            'code': self.code,
            'description': self.description,
            'measurement_type': self.measurement_type,
        }

        return _attributes
