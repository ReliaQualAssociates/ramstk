# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKSiteInfo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKSiteInfo Table Module."""

from datetime import date, timedelta

from sqlalchemy import Column, Date, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKSiteInfo(RAMSTK_BASE):
    """Class to represent the table ramstk_site_info in the RAMSTK Common database."""

    __tablename__ = 'ramstk_site_info'
    __table_args__ = {'extend_existing': True}

    site_id = Column(
        'fld_site_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    product_key = Column('fld_product_key', String(512), default='')
    expire_on = Column(
        'fld_expire_on', Date, default=date.today() + timedelta(30))
    function_enabled = Column('fld_function_enabled', Integer, default=0)
    requirement_enabled = Column('fld_requirement_enabled', Integer, default=0)
    hardware_enabled = Column('fld_hardware_enabled', Integer, default=0)
    vandv_enabled = Column('fld_vandv_enabled', Integer, default=0)
    fmea_enabled = Column('fld_fmea_enabled', Integer, default=0)

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKSiteInfo data model attributes.

        :return: {site_id, product_key, expire_on, function_enabled,
                  requirement_enabled, vandv_enabled, fmea_enabled} pairs.
        :rtype: dict
        """
        _attributes = {
            'site_id': self.site_id,
            'product_key': self.product_key,
            'expire_on': self.expire_on,
            'function_enabled': self.function_enabled,
            'requirement_enabled': self.requirement_enabled,
            'hardware_enabled': self.hardware_enabled,
            'vandv_enabled': self.vandv_enabled,
            'fmea_enabled': self.fmea_enabled
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKSiteInfo data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKSiteInfo attributes."

        try:
            self.product_key = str(
                none_to_default(attributes['product_key'], '0000'))
            self.expire_on = none_to_default(attributes['expire_on'],
                                             date.today() + timedelta(30))
            self.function_enabled = int(
                none_to_default(attributes['function_enabled'], 0))
            self.requirement_enabled = int(
                none_to_default(attributes['requirement_enabled'], 0))
            self.hardware_enabled = int(
                none_to_default(attributes['hardware_enabled'], 0))
            self.vandv_enabled = int(
                none_to_default(attributes['vandv_enabled'], 0))
            self.fmea_enabled = int(
                none_to_default(attributes['fmea_enabled'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RAMSTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
