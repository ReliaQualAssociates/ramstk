#!/usr/bin/env python
"""
######################
PoF Test Method Module
######################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

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
    import configuration as _conf
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:  # Index error
        _error_code = 40
    elif('invalid literal' in message[0] or
         'could not convert string to float' in message[0]):   # Value error
        _error_code = 50
    else:                                   # Unhandled error
        _error_code = 1000

    return _error_code


class Model(object):
    """
    The Method data model contains the attributes and methods of a Physics of
    Failure test method.  A PoF will consist of one or more Methods per
    operating stress.  The attributes of a Method are:

    :ivar stress_id: default value: None
    :ivar method_id: default value: None
    :ivar description: default value: ''
    :ivar boundary_conditions: default value: ''
    :ivar remarks: default value: ''
    """

    def __init__(self, stress_id=None):
        """
        Method to initialize a Method data model instance.
        """

        # Set public scalar attribute default values.
        self.stress_id = stress_id
        self.method_id = None
        self.description = ''
        self.boundary_conditions = ''
        self.remarks = ''

    def set_attributes(self, values):
        """
        Method to set the Method data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.stress_id = int(values[0])
            self.method_id = int(values[1])
            self.description = str(values[2])
            self.boundary_conditions = str(values[3])
            self.remarks = str(values[4])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mode data model
        attributes.

        :return: (stress_id, method_id, description, boundary_conditions,
                  remarks)
        :rtype: tuple
        """

        return(self.stress_id, self.method_id, self.description,
               self.boundary_conditions, self.remarks)


class Method(object):
    """
    The Method data controller provides an interface between the Method data model
    and an RTK view model.  A single Method data controller can control one or
    more Method data models.  Currently the Method data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Method data controller instance.
        """

        pass
