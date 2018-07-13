# pylint: disable=C0111,W0611
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.matrixviews.__init__.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
from .MatrixView import RTKMatrixView

from .FunctionHardware import MatrixView as FunctionHardware
#from .FunctionSoftware import MatrixView as FunctionSoftware
#from .FunctionValidation import MatrixView as FunctionValidation
from .RequirementHardware import MatrixView as RequirementHardware
from .RequirementSoftware import MatrixView as RequirementSoftware
from .RequirementValidation import MatrixView as RequirementValidation
from .HardwareRequirement import MatrixView as HardwareRequirement
from .HardwareValidation import MatrixView as HardwareValidation
from .ValidationRequirement import MatrixView as ValidationRequirement
from .ValidationHardware import MatrixView as ValidationHardware
