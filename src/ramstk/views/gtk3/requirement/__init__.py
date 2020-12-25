# pylint: disable=unused-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 revision package."""

ATTRIBUTE_KEYS = {
    0: ['requirement_code', 'string'],
    1: ['description', 'string'],
    2: ['requirement_type', 'integer'],
    4: ['specification', 'string'],
    5: ['page_number', 'string'],
    6: ['figure_number', 'string'],
    7: ['priority', 'integer'],
    8: ['owner', 'integer'],
    9: ['requirement_code', 'string'],
    10: ['validated_date', 'date'],
}

# RAMSTK Local Imports
from .moduleview import ModuleView as mvwRequirement
from .workview import GeneralData as wvwRequirementGD
from .workview import RequirementAnalysis as wvwRequirementAnalysis
