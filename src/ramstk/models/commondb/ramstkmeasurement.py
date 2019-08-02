# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKMeasurement.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMeasurement Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKMeasurement(RAMSTK_BASE):
    """Class to represent the table ramstk_measurement in the RAMSTK Common database."""

    __tablename__ = 'ramstk_measurement'
    __table_args__ = {'extend_existing': True}

    measurement_id = Column(
        'fld_measurement_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    code = Column('fld_code', String(128), default='Measurement Code')
    description = Column(
        'fld_description', String(512), default='Measurement Decription',
    )
    measurement_type = Column('fld_type', String(128), default='unknown')

    def get_attributes(self):
        """
        Retrieve the current values of RAMSTKMeasurement data model attributes.

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

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKMeasurement data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKMeasurement {0:d} attributes.". \
            format(self.measurement_id)

        try:
            self.code = str(
                none_to_default(attributes['code'], 'Measurement Code'),
            )
            self.description = str(
                none_to_default(
                    attributes['description'],
                    'Measurement Description',
                ),
            )
            self.description = str(
                none_to_default(attributes['measurement_type'], 'unknown'),
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
