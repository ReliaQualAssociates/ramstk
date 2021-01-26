# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.__mocks__.programdb.mock_ramstk_revision.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mock program database ramstk_revision table."""

# Standard Library Imports
from datetime import date, timedelta

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKRevision

_revision_1 = RAMSTKRevision()
_revision_1.revision_id = 1
_revision_1.availability_logistics = 0.9986
_revision_1.availability_mission = 0.99934
_revision_1.cost = 12532.15
_revision_1.cost_failure = 0.0000352
_revision_1.cost_hour = 1.2532
_revision_1.hazard_rate_active = 0.0
_revision_1.hazard_rate_dormant = 0.0
_revision_1.hazard_rate_logistics = 0.0
_revision_1.hazard_rate_mission = 0.0
_revision_1.hazard_rate_software = 0.0
_revision_1.mmt = 0.0
_revision_1.mcmt = 0.0
_revision_1.mpmt = 0.0
_revision_1.mtbf_logistics = 0.0
_revision_1.mtbf_mission = 0.0
_revision_1.mttr = 0.0
_revision_1.name = 'Original Revision'
_revision_1.reliability_logistics = 0.99986
_revision_1.reliability_mission = 0.99992
_revision_1.remarks = 'This is the original revision.'
_revision_1.revision_code = 'Rev. -'
_revision_1.program_time = 2562
_revision_1.program_time_sd = 26.83
_revision_1.program_cost = 26492.83
_revision_1.program_cost_sd = 15.62

_revision_2 = RAMSTKRevision()
_revision_2.revision_id = 2
_revision_2.availability_logistics = 1.0
_revision_2.availability_mission = 1.0
_revision_2.cost = 0.0
_revision_2.cost_failure = 0.0
_revision_2.cost_hour = 0.0
_revision_2.hazard_rate_active = 0.0
_revision_2.hazard_rate_dormant = 0.0
_revision_2.hazard_rate_logistics = 0.0
_revision_2.hazard_rate_mission = 0.0
_revision_2.hazard_rate_software = 0.0
_revision_2.mmt = 0.0
_revision_2.mcmt = 0.0
_revision_2.mpmt = 0.0
_revision_2.mtbf_logistics = 0.0
_revision_2.mtbf_mission = 0.0
_revision_2.mttr = 0.0
_revision_2.name = 'Revision A'
_revision_2.reliability_logistics = 1.0
_revision_2.reliability_mission = 1.0
_revision_2.remarks = 'This is the second revision.'
_revision_2.revision_code = 'Rev. A'
_revision_2.program_time = 0
_revision_2.program_time_sd = 0.0
_revision_2.program_cost = 0.0
_revision_2.program_cost_sd = 0.0

mock_ramstk_revision = [
    _revision_1,
    _revision_2,
]
