#!/usr/bin/env python
"""
#########################
Failure Definition Module
#########################
"""

# -*- coding: utf-8 -*-
#
#       rtk.failure_definition.FailureDefinition.py is part of The RTK Project
#
# All rights reserved.

try:
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Failure Definition data model contains the attributes and methods of a
    failure definition.  A Revision will contain zero or more definitions.  The
    attributes of a Failure Definition are:

    :ivar revision_id: the ID of the Revision the definition is associated
                       with.
    :ivar definition_id: the ID of the Failure Definition.
    :ivar definition: the definition.
    """

    def __init__(self):
        """
        Method to initialize a Failure Definition data model instance.
        """

        # Set public scalar attribute default values.
        self.revision_id = 0
        self.definition_id = 0
        self.definition = ''

    def set_attributes(self, values):
        """
        Method to set the Failure Definition data model attributes.

        :param tuple values: values to assign to the attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.definition_id = int(values[1])
            self.definition = str(values[2])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Failure Definition data
        model attributes.

        :return: values; the values of the attributes.
        :rtype: tuple
        """

        return(self.revision_id, self.definition_id, self.definition)


class FailureDefinition(object):
    """
    The Failure Definition data controller provides an interface between the
    Failure Definition data model and an RTK view model.  A single Failure
    Definition data controller can manage one or more Failure Definition data
    models.

    :ivar _dao: default value: None

    :ivar dicDefinitions: Dictionary of the Failure Definition data models
    managed by this data controller.  Key is the Revision ID; value is a list
    of pointers to the Failure Definition data model instances for the
    Revision.
    """

    def __init__(self):
        """
        Initialize a Failure Definition data controller instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dicDefinitions = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None

    def request_definitions(self, revision_id):
        """
        Method to load all of the failure definitions for a Revision.

        :param int revision_id: the Revision ID that the Failure Definition
                                will be associated with.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT * FROM tbl_failure_definitions \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=None)

        try:
            _n_definitions = len(_results)
        except TypeError:
            _n_definitions = 0

        # Create a list of Failure Definition data models for the Revision.
        _temp = {}
        for i in range(_n_definitions):
            _definition = Model()
            _definition.set_attributes(_results[i])
            _temp[_definition.definition_id] = _definition

        self.dicDefinitions[revision_id] = _temp

        return(_results, _error_code)

    def add_definition(self, revision_id):
        """
        Adds a new Failure Definition to a Revision.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int revision_id: the Revision ID to add the new Failure
                                Definition.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _query = "INSERT INTO tbl_failure_definitions \
                              (fld_revision_id, fld_definition) \
                  VALUES ({0:d}, '')".format(revision_id)
        (_results,
         _error_code,
         _last_id) = self.dao.execute(_query, commit=True)

        _definition = Model()
        _definition.set_attributes((revision_id, _last_id, ''))
        self.dicDefinitions[revision_id][_last_id] = _definition

        return(_results, _error_code, _last_id)

    def delete_definition(self, revision_id, definition_id):
        """
        Deletes a Failure Definition from the RTK Project.

        :param int revision_id: the Revision ID from which to delete.
        :param int definition_id: the Failure Definition ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM tbl_failure_definitions \
                  WHERE fld_definition_id={0:d}".format(definition_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        self.dicDefinitions[revision_id].pop(definition_id)

        return(_results, _error_code)

    def save_definitions(self, revision_id):
        """
        Saves the Failure Definition attributes to the RTK Project database.

        :param int revision_id: the Revision ID for which to save the Failure
                                Definitions.
        :return: (_results, _error_codes)
        :rtype: tuple
        """

        _results = []
        _error_codes = []

        for _definition in self.dicDefinitions[revision_id].values():
            _query = "UPDATE tbl_failure_definitions \
                      SET fld_definition='{0:s}' \
                      WHERE fld_definition_id={1:d}".format(
                          _definition.definition, _definition.definition_id)
            (_result, _error_code, __) = self.dao.execute(_query, commit=True)

            _results.append(_result)
            _error_codes.append(_error_code)

        return(_results, _error_codes)
