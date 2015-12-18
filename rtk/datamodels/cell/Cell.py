#!/usr/bin/env python
"""
###########
Cell Module
###########
"""

# -*- coding: utf-8 -*-
#
#       rtk.datamodels.cell.Cell.py is part of The RTK Project
#
# All rights reserved.

# Import other RTK modules.
try:
    import Utilities as _util
except ImportError:
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Cell data model is used to represent a relationship in a row-column
    (matrix) configuration.  The attributes of a Cell are:


    :ivar row_id: default value: None
    :ivar col_id: default value: None
    :ivar value: default value: None
    """

    def __init__(self):
        """
        Method to initialize a Cell data model instance.
        """

        # Set public scalar attribute default values.
        self.row_id = None
        self.col_id = None
        self.value = None

    def set_attributes(self, values):
        """
        Method to set the Cell data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.row_id = int(values[0])
            self.col_id = int(values[1])
            self.value = values[2]
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Cell data model
        attributes.

        :return: (self.row_id, self.col_id, self.value)
        :rtype: tuple
        """

        return(self.row_id, self.col_id, self.value)


class Cell(object):
    """
    The Cell data controller provides an interface between the Cell data
    model and an RTK view model.  A single Cell controller can control one
    or more Cell data models.  Currently the Cell controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Cell data controller instance.
        """

        pass
