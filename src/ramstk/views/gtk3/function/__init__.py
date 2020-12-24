# pylint: disable=unused-import, wrong-import-position
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 revision package."""

ATTRIBUTE_KEYS = {
    0: ['function_code', 'string'],
    1: ['name', 'string'],
    2: ['remarks', 'string'],
    3: ['safety_critical', 'integer'],
    5: ['function_code', 'text'],
    15: ['name', 'text'],
    17: ['remarks', 'text'],
}

# RAMSTK Local Imports
from .moduleview import ModuleView as mvwFunction
from .workview import GeneralData as wvwFunctionGD
