# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKMeasurement.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKMeasurement Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKMeasurement(RTK_BASE):
    """Class to represent the table rtk_measurement in the RTK Common database."""

    __tablename__ = 'rtk_measurement'
    __table_args__ = {'extend_existing': True}

    measurement_id = Column(
        'fld_measurement_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Measurement Decription')

    def get_attributes(self):
        """
        Retrieve the current values of RTKMeasurement data model attributes.

        :return: {measurement_id, description} pairs.
        :rtype: dict
        """
        _attributes = {
            'measurement_id': self.measurement_id,
            'description': self.description
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKMeasurement data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMeasurement {0:d} attributes.". \
            format(self.measurement_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Measurement Description'))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
