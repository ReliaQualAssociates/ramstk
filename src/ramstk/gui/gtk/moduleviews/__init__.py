# pylint: disable=C0111,W0611
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.__init__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
from .ModuleView import RAMSTKModuleView

from .Function import ModuleView as mvwFunction
from .Revision import ModuleView as mvwRevision
from .Requirement import ModuleView as mvwRequirement
from .Hardware import ModuleView as mvwHardware
from .Validation import ModuleView as mvwValidation
