#!/usr/bin/env python
"""
############################
Software Package CSCI Module
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.CSCI.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    from software.Software import Model as Software
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.software.Software import Model as Software

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(Software):  # pylint: disable=R0902
    """
    The CSCI data model contains the attributes and methods of a software CSCI
    item.
    """

    def __init__(self):
        """
        Method to initialize a CSCI data model instance.
        """

        super(Model, self).__init__()

        self.level_id = 2

    def calculate_complexity_risk(self):
        """
        Method to calculate Software risk due to the software complexity.

        For software complexity risk (SX), this method uses the results of
        RL-TR-92-52, Worksheet 9D or 10D to determine the relative risk level.
        The risk is based on the number of software units in a software module
        and the complexity of each unit.

        NM = number of units in module
        ax = # of units with sx >= 20
        bx = # of units with 7 <= sx < 20
        cx = # of units with sx < 7

        SX = (1.5 * ax + bx + 0.8 * cx) / NM

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Sum data from each unit subordinate to the CSCI.
        try:
            _units = self.dicUnits[self.software_id]
        except KeyError:
            _units = []

        self.nm = 0
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.aloc = 0
        self.hloc = 0
        self.sloc = 0
        for _unit in _units:
            self.nm += 1
            if _unit.sx >= 20:
                self.ax += 1
            elif _unit.sx >= 7 and _unit.sx < 20:
                self.bx += 1
            elif _unit.sx < 7:
                self.cx += 1

            # Calculate the number of lines of code in the CSCI.
            self.aloc += _unit.aloc
            self.hloc += _unit.hloc
            self.sloc += _unit.sloc

        # Calculate the Software Complexity factor for the CSCI:
        #
        #   SX = (1.5 * ax + bx + 0.8 * cx) / NM
        try:
            self.sx = (1.5 * self.ax + self.bx + 0.8 * self.cx) / self.nm
        except ZeroDivisionError:
            Widgets.rtk_error(
                _(u"Attempted to divide by zero when "
                  u"calculating the software complexity risk "
                  u"for {0:s}.  Perhaps you forgot to answer "
                  u"one or more questions.").format(self.description))
            self.sx = 1.5

        return False

    def calculate_modularity_risk(self):
        """
        Method to calculate Software risk due to the software complexity.

        For software modularity risk (SM), this method uses the results of
        RL-TR-92-52, Worksheet 9D to determine the relative risk level.  The
        risk is based on the number of software units in a software module and
        the SLOC in each unit.

        NM = number of units in module
        um = # of units in module with SLOC <= 100
        wm = # of units in module with 100 < SLOC <= 500
        xm = # of units in module with SLOC > 500

        SM = (0.9 * um + wm + 2.0 * xm) / NM

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Sum data from each unit subordinate to the CSCI.
        try:
            _units = self.dicUnits[self.software_id]
        except KeyError:
            _units = []

        self.um = 0
        self.wm = 0
        self.xm = 0
        for _unit in _units:
            if _unit.sloc <= 100:
                self.um += 1
            elif _unit.sloc > 100 and _unit.sloc <= 500:
                self.wm += 1
            elif _unit.sloc > 500:
                self.xm += 1

        # Calculate the Software Modularity factor:
        #
        #   SM = (0.9 * um + wm + 2.0 * xm) / NM
        try:
            self.sm = (0.9 * self.um + self.wm + 2.0 * self.xm) / self.nm
        except ZeroDivisionError:
            Widgets.rtk_error(
                _(u"Attempted to divide by zero when "
                  u"calculating the software modularity risk "
                  u"for {0:s}.  Perhaps you forgot to answer "
                  u"one or more questions.").format(self.description))
            self.sm = 2.0

        return False


class CSCI(object):
    """
    The CSCI data controller provides an interface between the CSCI data model
    and an RTK view model.  A single CSCI controller can manage one or more
    CSCI data models.
    """

    def __init__(self):
        """
        Method to initialize a CSCI data controller instance.
        """

        pass
