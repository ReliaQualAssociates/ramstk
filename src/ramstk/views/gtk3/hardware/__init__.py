# pylint: disable=unused-import, wrong-import-position
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 hardware package."""

ATTRIBUTE_KEYS = {
    0: ['revision_id', 'integer'],
    1: ['hardware_id', 'integer'],
    2: ['alt_part_number', 'string'],
    3: ['cage_code', 'string'],
    4: ['comp_ref_des', 'string'],
    5: ['cost', 'float'],
    6: ['cost_failure', 'float'],
    7: ['cost_hour', 'float'],
    8: ['description', 'string'],
    9: ['duty_cycle', 'float'],
    10: ['figure_number', 'string'],
    11: ['lcn', 'string'],
    12: ['level', 'integer'],
    13: ['manufacturer_id', 'integer'],
    14: ['mission_time', 'float'],
    15: ['name', 'string'],
    16: ['nsn', 'string'],
    17: ['page_number', 'string'],
    18: ['parent_id', 'integer'],
    19: ['part', 'boolean'],
    20: ['part_number', 'string'],
    21: ['quantity', 'integer'],
    22: ['ref_des', 'string'],
    23: ['remarks', 'string'],
    24: ['repairable', 'boolean'],
    25: ['specification_number', 'string'],
    26: ['tagged_part', 'boolean'],
    27: ['total_part_count', 'integer'],
    28: ['total_power_dissipation', 'float'],
    29: ['year_of_manufacture', 'integer'],
    30: ['cost_type_id', 'integer'],
    31: ['attachments', 'string'],
    32: ['category_id', 'integer'],
    33: ['subcategory_id', 'integer'],
}

# RAMSTK Local Imports
from .moduleview import ModuleView as mvwHardware
from .workview import AssessmentInputs as wvwHardwareAI
from .workview import AssessmentResults as wvwHardwareAR
from .workview import GeneralData as wvwHardwareGD
