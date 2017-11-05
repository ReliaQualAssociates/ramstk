# pylint: disable=C0111,W0611
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.__init__.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com

from .WorkView import RTKWorkView

from .Revision import GeneralData as wvwRevisionGD
from .Revision import AssessmentResults as wvwRevisionAR
from .Function import GeneralData as wvwFunctionGD
from .Function import AssessmentResults as wvwFunctionAR
from .FMEA import FMEA as wvwFMEA
from .Requirement import GeneralData as wvwRequirementGD
from .Requirement import RequirementAnalysis as wvwRequirementAnalysis
