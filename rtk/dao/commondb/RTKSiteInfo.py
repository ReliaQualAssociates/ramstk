# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKSiteInfo.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKSiteInfo Table Module."""

from datetime import date, timedelta

from sqlalchemy import Column, Date, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKSiteInfo(RTK_BASE):
    """Class to represent the table rtk_site_info in the RTK Common database."""

    __tablename__ = 'rtk_site_info'
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

    def get_attributes(self):
        """
        Retrieve the current values of the RTKSiteInfo data model attributes.

        :return: {site_id, product_key, expire_on} pairs.
        :rtype: dict
        """
        _attributes = {
            'site_id': self.site_id,
            'product_key': self.product_key,
            'expire_on': self.expire_on
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKSiteInfo data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSiteInfo {0:d} attributes.". \
            format(self.site_id)

        try:
            self.product_key = str(
                none_to_default(attributes['product_key'], '0000'))
            self.expire_on = none_to_default(attributes['expire_on'],
                                             date.today() + timedelta(30))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
