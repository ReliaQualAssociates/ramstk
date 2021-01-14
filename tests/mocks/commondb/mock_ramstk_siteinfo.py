# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.__mocks__.commondb.mock_ramstk_siteinfo.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mock common database ramstk_siteinfo table."""

# Standard Library Imports
from datetime import date, timedelta

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKSiteInfo

_site_1 = RAMSTKSiteInfo()
_site_1.site_id = 1
_site_1.site_name = 'DEMO SITE'
_site_1.product_key = 'DEMO'
_site_1.expire_on = date.today() + timedelta(30)
_site_1.function_enabled = 1
_site_1.requirement_enabled = 1
_site_1.hardware_enabled = 1
_site_1.software_enabled = 0
_site_1.rcm_enabled = 0
_site_1.testing_enabled = 0
_site_1.incident_enabled = 0
_site_1.survival_enabled = 0
_site_1.vandv_enabled = 1
_site_1.hazard_enabled = 1
_site_1.stakeholder_enabled = 1
_site_1.allocation_enabled = 1
_site_1.similar_item_enabled = 1
_site_1.fmea_enabled = 1
_site_1.pof_enabled = 1
_site_1.rbd_enabled = 0
_site_1.fta_enabled = 0

mock_ramstk_siteinfo = [
    _site_1,
]
