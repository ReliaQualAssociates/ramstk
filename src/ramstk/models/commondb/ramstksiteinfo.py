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
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKSiteInfo(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_site_info in the RAMSTK Common database."""

    __defaults__ = {
        'site_name': '',
        'product_key': '',
        'expire_on': date.today() + timedelta(30),
        'function_enabled': 0,
        'requirement_enabled': 0,
        'hardware_enabled': 0,
        'software_enabled': 0,
        'rcm_enabled': 0,
        'testing_enabled': 0,
        'incident_enabled': 0,
        'survival_enabled': 0,
        'vandv_enabled': 0,
        'hazard_enabled': 0,
        'stakeholder_enabled': 0,
        'allocation_enabled': 0,
        'similar_item_enabled': 0,
        'fmea_enabled': 0,
        'pof_enabled': 0,
        'rbd_enabled': 0,
        'fta_enabled': 0,
    }

    __tablename__ = 'ramstk_site_info'
    __table_args__ = {'extend_existing': True}

    site_id = Column('fld_site_id',
                     Integer,
                     primary_key=True,
                     autoincrement=True,
                     nullable=False)
    site_name = Column('fld_site_name',
                       String(512),
                       default=__defaults__['site_name'])
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
    software_enabled = Column('fld_software_enabled',
                              Integer,
                              default=__defaults__['software_enabled'])
    rcm_enabled = Column('fld_rcm_enabled',
                         Integer,
                         default=__defaults__['rcm_enabled'])
    testing_enabled = Column('fld_testing_enabled',
                             Integer,
                             default=__defaults__['testing_enabled'])
    incident_enabled = Column('fld_incident_enabled',
                              Integer,
                              default=__defaults__['incident_enabled'])
    survival_enabled = Column('fld_survival_enabled',
                              Integer,
                              default=__defaults__['survival_enabled'])
    vandv_enabled = Column('fld_vandv_enabled',
                           Integer,
                           default=__defaults__['vandv_enabled'])
    hazard_enabled = Column('fld_hazard_enabled',
                            Integer,
                            default=__defaults__['hazard_enabled'])
    stakeholder_enabled = Column('fld_stakeholder_enabled',
                                 Integer,
                                 default=__defaults__['stakeholder_enabled'])
    allocation_enabled = Column('fld_allocation_enabled',
                                Integer,
                                default=__defaults__['allocation_enabled'])
    similar_item_enabled = Column('fld_similar_item_enabled',
                                  Integer,
                                  default=__defaults__['similar_item_enabled'])
    fmea_enabled = Column('fld_fmea_enabled',
                          Integer,
                          default=__defaults__['fmea_enabled'])
    pof_enabled = Column('fld_pof_enabled',
                         Integer,
                         default=__defaults__['pof_enabled'])
    rbd_enabled = Column('fld_rbd_enabled',
                         Integer,
                         default=__defaults__['rbd_enabled'])
    fta_enabled = Column('fld_fta_enabled',
                         Integer,
                         default=__defaults__['fta_enabled'])

    def get_attributes(self):
        """Retrieve current values of the RAMSTKSiteInfo data model attributes.

        :return: {site_id, product_key, expire_on, function_enabled,
                  requirement_enabled, vandv_enabled, fmea_enabled} pairs.
        :rtype: dict
        """
        _attributes = {
            'site_id': self.site_id,
            'site_name': self.site_name,
            'product_key': self.product_key,
            'expire_on': self.expire_on,
            'function_enabled': self.function_enabled,
            'requirement_enabled': self.requirement_enabled,
            'hardware_enabled': self.hardware_enabled,
            'software_enabled': self.software_enabled,
            'rcm_enabled': self.rcm_enabled,
            'testing_enabled': self.testing_enabled,
            'incident_enabled': self.incident_enabled,
            'survival_enabled': self.survival_enabled,
            'vandv_enabled': self.vandv_enabled,
            'hazard_enabled': self.hazard_enabled,
            'stakeholder_enabled': self.stakeholder_enabled,
            'allocation_enabled': self.allocation_enabled,
            'similar_item_enabled': self.similar_item_enabled,
            'fmea_enabled': self.fmea_enabled,
            'pof_enabled': self.pof_enabled,
            'rbd_enabled': self.rbd_enabled,
            'fta_enabled': self.fta_enabled,
        }

        return _attributes
