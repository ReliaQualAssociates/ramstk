# pylint: disable=unused-import, wrong-import-position, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 validation package."""

ATTRIBUTE_KEYS = {
    0: ['revision_id', 'integer'],
    1: ['validation_id', 'integer'],
    2: ['acceptable_maximum', 'float'],
    3: ['acceptable_mean', 'float'],
    4: ['acceptable_minimum', 'float'],
    5: ['acceptable_variance', 'float'],
    6: ['confidence', 'float'],
    7: ['cost_average', 'float'],
    8: ['cost_ll', 'float'],
    9: ['cost_maximum', 'float'],
    10: ['cost_mean', 'float'],
    11: ['cost_minimum', 'float'],
    12: ['cost_ul', 'float'],
    13: ['cost_variance', 'float'],
    14: ['date_end', 'string'],
    15: ['date_start', 'string'],
    16: ['description', 'string'],
    17: ['measurement_unit', 'integer'],
    18: ['name', 'string'],
    19: ['status', 'float'],
    20: ['task_specification', 'string'],
    21: ['task_type', 'integer'],
    22: ['time_average', 'float'],
    23: ['time_ll', 'float'],
    24: ['time_maximum', 'float'],
    25: ['time_mean', 'float'],
    26: ['time_minimum', 'float'],
    27: ['time_ul', 'float'],
    28: ['time_variance', 'float'],
}

# RAMSTK Local Imports
from .moduleview import ModuleView as mvwValidation
from .workview import BurndownCurve as wvwBurndownCurve
from .workview import GeneralData as wvwValidationGD
