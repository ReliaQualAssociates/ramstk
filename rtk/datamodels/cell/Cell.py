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
import Utilities as _util                   # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Cell data model is used to represent a relationship in a row-column
    (matrix) configuration.  The attributes of a Cell are:

    :ivar int cell_id: the ID of the Cell.
    :ivar int row_id: the ID of the Row this Cell is in.
    :ivar int col_id: the ID of the column this Cell is in.
    :ivar int value: the value of the Cell at (row_id, col_id).
    """

    def __init__(self):
        """
        Method to initialize a Cell data model instance.
        """

        # Define private dict attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dict attributes.

        # Define public list attributes.

        # Define public scalar attributes.
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
            self.cell_id = int(values[0])
            self.row_id = int(values[1])
            self.col_id = int(values[2])
            self.value = values[3]
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

        :return: (row_id, col_id, value)
        :rtype: tuple
        """

        return(self.row_id, self.col_id, self.value)


class Cell(object):
    """
    The Cell data controller provides an interface between the Cell data model
    and an RTK view model.  A single Cell data controller can control one or
    more Cell data models.  Currently the Cell data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Cell data controller instance.
        """

        pass
