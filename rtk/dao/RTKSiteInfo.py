# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSiteInfo.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKSiteInfo Table
===============================================================================
"""

from datetime import date, timedelta

from sqlalchemy import Column, Date, \
                       Integer, String              # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKSiteInfo(RTK_BASE):
    """
    Class to represent the table rtk_site_info in the RTK Common database.
    """

    __tablename__ = 'rtk_site_info'
    __table_args__ = {'extend_existing': True}

    site_id = Column('fld_site_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    product_key = Column('fld_product_key', String(512), default='')
    expire_on = Column('fld_expire_on', Date,
                       default=date.today() + timedelta(30))

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSiteInfo data model
        attributes.

        :return: (site_id, product_key, expire_on)
        :rtype: tuple
        """

        _values = (self.site_id, self.product_key, self.expire_on)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKSiteInfo data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSiteInfo {0:d} attributes.". \
            format(self.site_id)

        try:
            self.product_key = str(none_to_default(attributes[0], ''))
            self.expire_on = none_to_default(attributes[1],
                                             date.today() + timedelta(30))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSiteInfo.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSiteInfo attributes."

        return _error_code, _msg
