#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.failure_definition.FailureDefinition.py is part of The RTK Project
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

"""
#########################
Failure Definition Module
#########################
"""

# Import other RTK modules.
try:
    import Configuration as Configuration
    import Utilities as Utilities
    from dao.DAO import RTKFailureDefinition
except ImportError:
    import rtk.Configuration as Configuration       # pylint: disable=E0401
    import rtk.Utilities as Utilities               # pylint: disable=E0401
    from rtk.dao.DAO import RTKFailureDefinition    # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Failure Definition data model contains the attributes and methods of a
    failure definition.  A Revision will contain zero or more definitions.  The
    attributes of a Failure Definition are:

    :cvar dict dicDefinition: dictionary containing all the
                              RTKFailureDefintion models that are part of the
                              Failure Definition tree.  Key is the Definition
                              ID; value is a pointer to the instance of the
                              RTKFailureDefinition model.

    :ivar int last_id: the last Failure Definition ID used in the RTK Program
                       database.
    :ivar dao: the `:py:class:rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    # Define public class dictionary attributes.
    dicDefinition = {}

    def __init__(self):
        """
        Method to initialize a Failure Definition data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None
        self.last_id = None

    def retrieve(self, definition_id):
        """
        Method to retrieve the instance of the RTKFailureDefinition data model
        for the Definition ID passed.

        :param int definition_id: the ID Of the RTKFailureDefinition to
                                  retrieve.
        :return: the instance of the RTKFailureDefinition class that was
                 requested or None if the requested Definition ID does not
                 exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKFailureDefinition`
        """

        try:
            _definition = self.dicDefinition[definition_id]
        except KeyError:
            _definition = None

        return _definition

    def retrieve_all(self, dao, revision_id):
        """
        Method to retrieve all the RTKMissions from the RTK Program database.

        :param dao: the `:py:class:dao.DAO.DAO` instance connected to the RTK
                    Program database.
        :param int revision_id: the ID of the Revision to retrieve the Failure
                                definitions.
        :return: dicDefinition; the dictionary of RTKFailureDefinition data
                 models that comprise the Failure Definition tree.
        :rtype: dict
        """

        self.dao = dao

        # Clear the Failure Defintion dictionary of previous Revision's
        # Failure Defintions.
        self.dicDefinition = {}
        for _definition in self.dao.session.query(RTKFailureDefinition).\
                filter(RTKFailureDefinition.revision_id == revision_id).all():
            self.dicDefinition[_definition.definition_id] = _definition

        return self.dicDefinition

    def add_definition(self, revision_id):
        """
        Method to add a Failure Definition to the RTK Program database for
        Revision ID.

        :param int revision_id: the Revision ID to add the Failure Definition
                                to.
        :return: _definition
        :rtype: `:py:test:rtk.dao.DAO.RTKFailureDefinition`
        """

        _definition = RTKFailureDefinition()
        _definition.revision_id = revision_id

        (_error_code, _msg) = self.dao.db_add(_definition)

        # If the add was successful add the new RTKFailureDefinition data model
        # instance to dicDefinition and log the success message to the user
        # log.  Otherwise, update the error message and write it to the error
        # log.
        if _error_code == 0:
            self.last_id = _definition.definition_id
            self.dicDefinition[_definition.definition_id] = _definition
            Configuration.RTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + "  Failed to add a new Failure Definition to the " \
                          "RTK Program database."
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _definition = None

        return _definition

    def delete_definition(self, definition_id):
        """
        Method to remove the Failure Definition associated with Definition ID.

        :param int definition_id: the ID of the Failure Definition to be
                                  removed.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _definition = self.dicDefinition[definition_id]

            (_error_code, _msg) = self.dao.db_delete(_definition)

            if _error_code == 0:
                self.dicDefinition.pop(definition_id)
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to delete Failure Definition " \
                                  "ID {0:d} from the RTK Program "\
                                  "database.".format(definition_id)
                except ValueError:      # Mission ID is None.
                    _msg = _msg + "  Failed to delete Failure Definition " \
                            "ID {0:s} from the RTK Program " \
                            "database.".format(definition_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to delete non-existent Failure Definition " \
                       "ID {0:d}.".format(definition_id)
            except ValueError:      # Mission ID is None.
                _msg = "Attempted to delete non-existent Failure Definition " \
                        "ID {0:s}.".format(definition_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_definition(self, definition_id):
        """
        Method to update the Failure Definition associated with Definition ID
        to the RTK Program database.

        :param int definition_id: the Failure Definition ID to save to the RTK
                                  Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _definition = self.dicDefinition[definition_id]

            (_error_code, _msg) = self.dao.db_update()

            if _error_code == 0:
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to save Failure Definition ID " \
                            "{0:d} to the RTK Program database".\
                        format(definition_id)
                except ValueError:      # If the revision_id = None.
                    _msg = _msg + "  Failed to save Failure Definition ID " \
                            "{0:s} to the RTK Program database".\
                        format(definition_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to save non-existent Failure Definition " \
                        "ID {0:d}.".format(definition_id)
            except ValueError:          # If the revision_id = None.
                _msg = "Attempted to save non-existent Failure Definition " \
                        "ID {0:s}.".format(definition_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_all_definitions(self):
        """
        Method to save all Failure Definitions to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        for _definition_id in self.dicDefinition.keys():
            if self.save_definition(_definition_id):
                _return = True

        return _return



class FailureDefinition(object):
    """
    The Failure Definition data controller provides an interface between the
    Failure Definition data model and an RTK view model.  A single Failure
    Definition data controller can manage one or more Failure Definition data
    models.

    :ivar definition_model: the
    `:py:class:rtk.failure_definition.FailureDefinition.Model` associated with
    the data controller instance.
    """

    def __init__(self):
        """
        Method to initialize a Failure Definition data controller instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.failure_model = Model()

    def request_failure_definitions(self, dao, revision_id):
        """
        Method to request the Failure Definition tree from the Failure
        Definition data model.

        :param dao: the `:py:class:rtk.dao.DAO.DAO` object connected to the RTK
                    Program database.
        :param int revision_id: the Revision ID to retrieve the Failure
                                Definitions for.
        :return: dicDefinition
        :rtype: dict
        """

        return self.failure_model.retrieve_all(dao, revision_id)

    def request_add_definition(self, revision_id):
        """
        Method to request a Failure Definition be added to Revision ID.

        :param int revision_id: the Revision ID this Mission will be
                                associated with.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.failure_model.add_definition(revision_id)

    def request_delete_definition(self, definition_id):
        """
        Method to request Failure Definition ID and it's children be deleted
        from the Failure Definition list.

        :param int definition_id: the Failure Definition ID to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.failure_model.delete_definition(definition_id)

    def request_save_definitions(self):
        """
        Method to request the Failure Definitions be saved to the RTK Program
        database.

        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.failure_model.save_all_definitions()
