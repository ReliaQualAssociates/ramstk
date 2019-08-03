# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKSiteInfo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKSiteInfo Table Module."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
from sqlalchemy import Column, Date, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKSiteInfo(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_site_info in the RAMSTK Common database."""

    __defaults__ = {
        'product_key': '',
        'expire_on': date.today() + timedelta(30),
        'function_enabled': 0,
        'requirement_enabled': 0,
        'hardware_enabled': 0,
        'vandv_enabled': 0,
        'fmea_enabled': 0
    }
    __tablename__ = 'ramstk_site_info'
    __table_args__ = {'extend_existing': True}

    site_id = Column('fld_site_id',
                     Integer,
                     primary_key=True,
                     autoincrement=True,
                     nullable=False)
    product_key = Column('fld_product_key',
                         String(512),
                         default=__defaults__['product_key'])
    expire_on = Column('fld_expire_on',
                       Date,
                       default=__defaults__['expire_on'])
    function_enabled = Column('fld_function_enabled',
                              Integer,
                              default=__defaults__['function_enabled'])
    requirement_enabled = Column('fld_requirement_enabled',
                                 Integer,
                                 default=__defaults__['requirement_enabled'])
    hardware_enabled = Column('fld_hardware_enabled',
                              Integer,
                              default=__defaults__['hardware_enabled'])
    vandv_enabled = Column('fld_vandv_enabled',
                           Integer,
                           default=__defaults__['vandv_enabled'])
    fmea_enabled = Column('fld_fmea_enabled',
                          Integer,
                          default=__defaults__['fmea_enabled'])

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKSiteInfo data model attributes.

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
            'fmea_enabled': self.fmea_enabled,
        }

        return _attributes
