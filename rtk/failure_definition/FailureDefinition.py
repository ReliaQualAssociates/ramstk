# -*- coding: utf-8 -*-
#
#       rtk.failure_definition.FailureDefinition.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Failure Definition Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub                              # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel                 # pylint: disable=E0401
from datamodels import RTKDataController            # pylint: disable=E0401
from dao import RTKFailureDefinition                # pylint: disable=E0401

_ = gettext.gettext


class Model(RTKDataModel):
    """
    The Failure Definition data model contains the attributes and methods of a
    failure definition.  A Revision will contain zero or more definitions.  The
    attributes of a Failure Definition are:
    """

    _tag = 'Failure Definitions'

    def __init__(self, dao):
        """
        Method to initialize a Failure Definition data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, definition_id):
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

        return RTKDataModel.select(self, definition_id)

    def select_all(self, revision_id):
        """
        Method to retrieve all the RTKFailureDefinitions from the RTK Program
        database.

        :param int revision_id: the Revision ID to select the Failure
                                Definitions for.
        :return: tree; the treelib Tree() of RTKFailureDefinition data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _definition in _session.query(RTKFailureDefinition).filter(
                RTKFailureDefinition.revision_id == revision_id).all():
            self.tree.create_node(_definition.definition,
                                  _definition.definition_id,
                                  parent=0, data=_definition)

        _session.close()

        return self.tree

    def insert(self, revision_id):
        """
        Method to add a Failure Definition to the RTK Program database.

        :param int revision_id: the Revision ID to add the Failure
                                Definition against.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _definition = RTKFailureDefinition()
        _definition.revision_id = revision_id
        _error_code, _msg = RTKDataModel.insert(self, [_definition, ])

        if _error_code == 0:
            self.tree.create_node(_definition.definition,
                                  _definition.definition_id,
                                  parent=0, data=_definition)
            self._last_id = _definition.definition_id   # pylint: disable=W0201

        return _error_code, _msg

    def delete(self, definition_id):
        """
        Method to remove the revision associated with Failure Definition ID.

        :param int definition_id: the ID of the Failure Definition to be
                                  removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _definition = self.tree.get_node(definition_id).data
            _error_code, _msg = RTKDataModel.delete(self, _definition)

            if _error_code == 0:
                self.tree.remove_node(definition_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Failure ' \
                   'Definition ID {0:d}.'.format(definition_id)

        return _error_code, _msg

    def update(self, definition_id):
        """
        Method to update the Failure Definition associated with Definition ID
        to the RTK Program database.

        :param int definition_id: the Failure Definition ID to save to the RTK
                                  Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = RTKDataModel.update(self, definition_id)

        if _error_code != 0:
            _error_code = 2207
            _msg = 'RTK ERROR: Attempted to save non-existent Failure ' \
                   'Definition ID {0:d}.'.format(definition_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Failure Definitions to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.definition_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg


class FailureDefinition(RTKDataController):
    """
    The Failure Definition data controller provides an interface between the
    Failure Definition data model and an RTK view model.  A single Failure
    Definition data controller can manage one or more Failure Definition data
    models.

    :ivar _dtm_revision: the :py:class:`rtk.Revision.Model` associated with
                         the Revision Data Controller.
    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Failure Definition data controller instance.
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.__test = kwargs['test']
        self._dtm_failure_definition = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, definition_id):
        """
        Method to request the Failure Definition Data Model to retrieve the
        RTKFailureDefinition model associated with the Definition ID.

        :param int definition_id: the Failure Definition ID to retrieve.
        :return: the RTKFailureDefinition model requested.
        :rtype: :py:class:`rtk.dao.DAO.RTKFailureDefinition` model
        """

        return self._dtm_failure_definition.select(definition_id)

    def request_select_all(self, revision_id):
        """
        Method to retrieve the Failure Definition tree from the Failure
        Definition Data Model.

        :return: tree; the treelib Tree() of RTKFailureDefinition models in
                 the Failure Definition tree.
        :rtype: dict
        """

        return self._dtm_failure_definition.select_all(revision_id)

    def request_insert(self, revision_id):
        """
        Method to request a Failure Definition be added to Revision ID.

        :param int revision_id: the Revision ID this Failure Definition will be
                                associated with.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _return = False

        _error_code, _msg = self._dtm_failure_definition.insert(revision_id)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('insertedDefinition')
        else:
            _msg = _msg + '  Failed to add a new Failure Definition to the ' \
                          'RTK Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, definition_id):
        """
        Method to request Failure Definition ID and it's children be deleted
        from the Failure Definition list.

        :param int definition_id: the Failure Definition ID to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _return = False

        _error_code, \
            _msg = self._dtm_failure_definition.delete(definition_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('deletedDefinition')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update(self, definition_id):
        """
        Method to request the Failure Definitions be saved to the RTK Program
        database.

        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _return = False

        _error_code, _msg = self._dtm_failure_definition.update(definition_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedDefinition')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Failure Definition Data Model to save all
        RTKFailureDefinition model attributes to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_failure_definition.update_all()

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return
