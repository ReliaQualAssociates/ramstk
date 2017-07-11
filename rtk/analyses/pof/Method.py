#!/usr/bin/env python
"""
######################
PoF Test Method Module
######################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.Method.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Method data model contains the attributes and methods of a Physics of
    Failure test method.  A PoF will consist of one or more Methods per
    operating stress.  The attributes of a Method are:

    :ivar int stress_id: the PoF Stress ID associated with the PoF test Method.
    :ivar int method_id: the ID of the PoF test Method.
    :ivar str description: the description of the PoF test Method.
    :ivar str boundary_conditions: the boundary conditions for the PoF test
                                   Method.
    :ivar str remarks: any remarks associated with the PoF test Method.
    """

    def __init__(self, stress_id=None):
        """
        Method to initialize a Method data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.stress_id = stress_id
        self.method_id = None
        self.description = ''
        self.boundary_conditions = ''
        self.remarks = ''


class Method(object):
    """
    The Method data controller provides an interface between the Method data
    model and an RTK view model.  A single Method data controller can control
    one or more Method data models.  Currently the Method data controller is
    unused.
    """

    def __init__(self):
        """
        Method to initialize a Method data controller instance.
        """

        pass
