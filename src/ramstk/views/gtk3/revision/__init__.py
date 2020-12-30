# pylint: disable=unused-import, wrong-import-position
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 revision package."""

ATTRIBUTE_KEYS = {
    0: ['name', 'string'],
    1: ['remarks', 'string'],
    2: ['revision_code', 'string'],
}

# RAMSTK Local Imports
from .moduleview import ModuleView as mvwRevision
from .workview import GeneralData as wvwRevisionGD
