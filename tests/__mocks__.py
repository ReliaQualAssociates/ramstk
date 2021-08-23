# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.__mocks__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""File for organizing mock structures."""

# Standard Library Imports
from datetime import date, timedelta

MOCK_STATUS = {
    1: {
        "cost_remaining": 284.98,
        "date_status": date.today() - timedelta(days=1),
        "time_remaining": 125.0,
    },
    2: {"cost_remaining": 212.32, "date_status": date.today(), "time_remaining": 112.5},
}

MOCK_STAKEHOLDERS = {
    1: {
        "customer_rank": 1,
        "description": "Stakeholder Input",
        "group": "",
        "improvement": 0.0,
        "overall_weight": 0.0,
        "planned_rank": 1,
        "priority": 1,
        "requirement_id": 0,
        "stakeholder": "",
        "user_float_1": 1.0,
        "user_float_2": 1.0,
        "user_float_3": 1.0,
        "user_float_4": 1.0,
        "user_float_5": 1.0,
    },
    2: {
        "customer_rank": 1,
        "description": "Stakeholder Input",
        "group": "",
        "improvement": 0.0,
        "overall_weight": 0.0,
        "planned_rank": 1,
        "priority": 1,
        "requirement_id": 0,
        "stakeholder": "",
        "user_float_1": 1.0,
        "user_float_2": 1.0,
        "user_float_3": 1.0,
        "user_float_4": 1.0,
        "user_float_5": 1.0,
    },
}
