# pylint: disable=C0111,W0611
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.__init__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com

from .WorkView import RAMSTKWorkView

from .Allocation import Allocation as wvwAllocation
from .Function import GeneralData as wvwFunctionGD
from .FMEA import FFMEA as wvwFFMEA
from .FMEA import DFMECA as wvwDFMECA
from .Hardware import GeneralData as wvwHardwareGD
from .Hardware import AssessmentInputs as wvwHardwareAI
from .Hardware import AssessmentResults as wvwHardwareAR
from .HazOps import HazOps as wvwHazOps
from .PoF import PoF as wvwPoF
from .Requirement import GeneralData as wvwRequirementGD
from .Requirement import RequirementAnalysis as wvwRequirementAnalysis
from .Revision import GeneralData as wvwRevisionGD
from .SimilarItem import SimilarItem as wvwSimilarItem
from .Validation import GeneralData as wvwValidationGD
from .Validation import BurndownCurve as wvwBurndownCurve
