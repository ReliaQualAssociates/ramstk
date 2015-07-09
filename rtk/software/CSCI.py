#!/usr/bin/env python
"""
############################
Software Package CSCI Module
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.software.CSCI.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    from software.Software import Model as Software
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    import rtk.utilities as _util
    from rtk.software.Software import Model as Software

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(Software):                        # pylint: disable=R0902
    """
    The CSCI data model contains the attributes and methods of a software CSCI
    item.
    """

    def __init__(self):
        """
        Initialize an CSCI data model instance.
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

        For software units:
            sx = # of conditional branching statements
                 # of unconditional branching statements + 1

        For software modules:
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
            _util.rtk_error(_(u"Attempted to divide by zero when calculating "
                              u"the software complexity risk for %s.  Perhaps "
                              u"you forgot to answer one or more questions.  "
                              u"If the problem persists, you may report it to "
                              u"bugs@reliaqual.com.") % self.description)
            self.sx = 1.5

        return False

    def calculate_modularity_risk(self):
        """
        Method to calculate Software risk due to the software complexity.

        For software modularity risk (SM), this method uses the results of
        RL-TR-92-52, Worksheet 9D to determine the relative risk level.  The
        risk is based on the number of software units in a software module and
        the SLOC in each unit.

        For software units:
            SM = 1.0

        For software modules:
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
            _util.rtk_error(_(u"Attempted to divide by zero when calculating "
                              u"the software modularity risk for %s.  Perhaps "
                              u"you forgot to answer one or more questions.  "
                              u"If the problem persists, you may report it to "
                              u"bugs@reliaqual.com.") % self.description)
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
        Initializes an CSCI data controller instance.
        """

        pass
