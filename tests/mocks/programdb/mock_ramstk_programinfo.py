# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.__mocks__.programdb.mock_ramstk_programinfo.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mock program database ramstk_programinfo table."""

# Standard Library Imports
from datetime import date, timedelta

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKProgramInfo

_program_1 = RAMSTKProgramInfo()
_program_1.revision_id = 1
_program_1.function_active = 1
_program_1.requirement_active = 1
_program_1.hardware_active = 1
_program_1.software_active = 0
_program_1.rcm_active = 0
_program_1.testing_active = 0
_program_1.incident_active = 0
_program_1.survival_active = 0
_program_1.vandv_active = 1
_program_1.hazard_active = 1
_program_1.stakeholder_active = 1
_program_1.allocation_active = 1
_program_1.similar_item_active = 1
_program_1.fmea_active = 1
_program_1.pof_active = 1
_program_1.rbd_active = 0
_program_1.fta_active = 0
_program_1.created_on = date.today()
_program_1.created_by = ''
_program_1.last_saved = date.today()
_program_1.last_saved_by = ''

mock_ramstk_programinfo = [
    _program_1,
]
