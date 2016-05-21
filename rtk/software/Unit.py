#!/usr/bin/env python
"""
############################
Software Package Unit Module
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.Unit.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
<<<<<<< HEAD
    import Configuration as _conf
    from software.Software import Model as Software
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
=======
    import Configuration
    from software.Software import Model as Software
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    from rtk.software.Software import Model as Software

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
<<<<<<< HEAD
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


<<<<<<< HEAD
class Model(Software):                        # pylint: disable=R0902
=======
class Model(Software):                      # pylint: disable=R0902
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """
    The Unit data model contains the attributes and methods of a software Unit
    item.
    """

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize an Unit data model instance.
=======
        Method to initialize a Unit data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Model, self).__init__()

        self.level_id = 3
        self.sm = 1.0

    def calculate_complexity_risk(self):
        """
        Method to calculate Software risk due to the software complexity.

        For software complexity risk (SX), this method uses the results of
        RL-TR-92-52, Worksheet 9D or 10D to determine the relative risk level.
        The risk is based on the number of software units in a software module
        and the complexity of each unit.

        sx = # of conditional branching statements +
             # of unconditional branching statements + 1

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

<<<<<<< HEAD
=======
        # Software complexity defaults to 1 since cb and ncb default to 0.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.sx = self.cb + self.ncb + 1

        return False

    def calculate_modularity_risk(self):
        """
        Method to calculate Software risk due to the software complexity.

        For software modularity risk (SM), this method uses the results of
        RL-TR-92-52, Worksheet 9D to determine the relative risk level.  The
        risk is based on the number of software units in a software module and
        the SLOC in each unit.

        SM = 1.0

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.sm = 1.0

        return False


class Unit(object):
    """
    The Unit data controller provides an interface between the Unit data model
    and an RTK view model.  A single Unit controller can manage one or more
    Unit data models.
    """

    def __init__(self):
        """
<<<<<<< HEAD
        Initializes an Unit data controller instance.
=======
        Method to initialize a Unit data controller instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        pass
