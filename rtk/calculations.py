#!/usr/bin/env python2
"""
This module contains various calculations used by the RTK Project.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       calculations.py is part of The RTK Project
#
# All rights reserved.

import gettext
import sys

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)

# Add NLS support.
_ = gettext.gettext

import numpy as np

import Configuration as _conf
import Utilities as _util


def calculate_part(model):
    """
    Calculates the hazard rate for a component.

    :param dict model: the component's h(t) prediction model and the input
                       variables.  The keys are the model variables and the
                       values are the values of the variable in the key.
    :return: _lambdap, the calculated h(t).
    :rtype: float
    """
# TODO: Move to Hardware class.
    _keys = model.keys()
    _values = model.values()

    for i in range(len(_keys)):
        vars()[_keys[i]] = _values[i]

    _lambdap = eval(model['equation'])      # pylint: disable=W0123

    return _lambdap
