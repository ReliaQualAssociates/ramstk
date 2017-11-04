# pylint: disable=C0111,W0611
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.__init__.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com

from .ModuleView import RTKModuleView

from .Function import ModuleView as mvwFunction
from .Revision import ModuleView as mvwRevision
from .Requirement import ModuleView as mvwRequirement
