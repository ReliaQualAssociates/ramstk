# pylint: disable=unused-import, wrong-import-position
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Revision Views."""

ATTRIBUTE_KEYS = {
    0: ["name", "string"],
    1: ["remarks", "string"],
    2: ["revision_code", "string"],
}

# RAMSTK Local Imports
from .panel import RevisionTreePanel
from .view import RevisionModuleView
from .workview import GeneralData as wvwRevisionGD
