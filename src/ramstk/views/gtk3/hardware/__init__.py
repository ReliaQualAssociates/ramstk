# pylint: disable=unused-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 hardware package."""

ATTRIBUTE_KEYS = {
    2: ['alt_part_number', 'text'],
    3: ['cage_code', 'text'],
    4: ['comp_ref_des', 'text'],
    5: ['cost', 'float'],
    6: ['cost_failure', 'float'],
    7: ['cost_hour', 'float'],
    8: ['description', 'text'],
    9: ['duty_cycle', 'float'],
    10: ['figure_number', 'text'],
    11: ['lcn', 'text'],
    12: ['level', 'integer'],
    13: ['manufacturer_id', 'integer'],
    14: ['mission_time', 'float'],
    15: ['name', 'text'],
    16: ['nsn', 'text'],
    17: ['page_number', 'text'],
    18: ['parent_id', 'integer'],
    19: ['part', 'boolean'],
    20: ['part_number', 'text'],
    21: ['quantity', 'integer'],
    22: ['ref_des', 'text'],
    23: ['remarks', 'text'],
    24: ['repairable', 'boolean'],
    25: ['specification_number', 'text'],
    26: ['tagged_part', 'boolean'],
    27: ['total_part_count', 'integer'],
    28: ['total_power_dissipation', 'float'],
    29: ['year_of_manufacture', 'integer'],
    30: ['cost_type_id', 'integer'],
    31: ['attachments', 'text'],
    32: ['category_id', 'integer'],
    33: ['subcategory_id', 'integer'],
}

# RAMSTK Local Imports
from .listview import HardwareRequirement as mtxHardwareRequirement
from .listview import HardwareValidation as mtxHardwareValidation
from .moduleview import ModuleView as mvwHardware
from .workview import AssessmentInputs as wvwHardwareAI
from .workview import AssessmentResults as wvwHardwareAR
from .workview import GeneralData as wvwHardwareGD
