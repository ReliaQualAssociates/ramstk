# pylint: disable=unused-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 revision package."""

ATTRIBUTE_KEYS = {
    0: ['description', 'string'],
    1: ['task_type', 'integer'],
    2: ['task_specification', 'string'],
    3: ['measurement_unit', 'integer'],
    4: ['acceptable_minimum', 'float'],
    5: ['acceptable_maximum', 'float'],
    6: ['acceptable_mean', 'float'],
    7: ['acceptable_variance', 'float'],
    8: ['date_start', 'string'],
    9: ['date_end', 'string'],
    10: ['status', 'float'],
    11: ['name', 'string'],
    12: ['time_minimum', 'float'],
    14: ['time_average', 'float'],
    15: ['time_maximum', 'float'],
    16: ['cost_minimum', 'float'],
    17: ['cost_average', 'float'],
    18: ['cost_maximum', 'float'],
}

# RAMSTK Local Imports
from .listview import ValidationRequirement as mtxValidationRequirement
from .moduleview import ModuleView as mvwValidation
from .workview import BurndownCurve as wvwBurndownCurve
from .workview import GeneralData as wvwValidationGD
