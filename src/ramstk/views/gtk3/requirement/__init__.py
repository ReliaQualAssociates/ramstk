# pylint: disable=unused-import, wrong-import-position
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 revision package."""

ATTRIBUTE_KEYS = {
    2: ['derived', 'integer'],
    3: ['description', 'string'],
    4: ['figure_number', 'string'],
    5: ['owner', 'integer'],
    6: ['page_number', 'string'],
    8: ['priority', 'integer'],
    10: ['specification', 'string'],
    11: ['requirement_type', 'integer'],
    12: ['validated', 'integer'],
    13: ['validated_date', 'string'],
}

# RAMSTK Local Imports
from .moduleview import ModuleView as mvwRequirement
from .workview import GeneralData as wvwRequirementGD
from .workview import RequirementAnalysis as wvwRequirementAnalysis
