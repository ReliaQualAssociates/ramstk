# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Mechanism.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
FMEA Failure Mechanism Module
###############################################################################
"""

from pubsub import pub                          # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel             # pylint: disable=E0401
from datamodels import RTKDataController        # pylint: disable=E0401
from dao.RTKMechanism import RTKMechanism       # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'


class Model(RTKDataModel):
    """
    The Mechanism data model contains the attributes and methods of a FMEA
    failure mechanism.  A :py:class:`rtk.analyses.fmea.Mode.Mode` will consist
    of one or more failure mechanisms.
    """

    _tag = 'Mechanisms'

    def __init__(self, dao):
        """
        Method to initialize a Mechanism data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.last_id = None

    def select(self, mechanism_id):
        """
        Method to retrieve the instance of the RTKMechanism data model for the
        Mechanism ID passed.

        :param int mechanism_id: the ID of the failure mechanism to retrieve.
        :return: the instance of the RTKMechanism class that was requested or
                 None if the requested Mechanism ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKMechanism.RTKMechanism`
        """

        return RTKDataModel.select(self, mechanism_id)

    def select_all(self, mode_id):
        """
        Method to retrieve all the Mechanisms from the RTK Program database.
        Then add each to the Mechanism treelib Tree().

        :param int mode_id: the Mode ID to the Mechanisms for.
        :return: tree; the Tree() of RTKMechanism data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _mechanism in _session.query(RTKMechanism).\
                filter(RTKMechanism.mode_id == mode_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default values.
            _attributes = _mechanism.get_attributes()
            _mechanism.set_attributes(_attributes[2:])
            self.tree.create_node(
                _mechanism.description,
                _mechanism.mechanism_id,
                parent=0,
                data=_mechanism)
            self.last_id = max(self.last_id, _mechanism.mechanism_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Mechanism to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _mechanism = RTKMechanism()
        _mechanism.mode_id = kwargs['mode_id']
        _error_code, _msg = RTKDataModel.insert(self, [
            _mechanism,
        ])

        if _error_code == 0:
            self.tree.create_node(
                _mechanism.description,
                _mechanism.mechanism_id,
                parent=0,
                data=_mechanism)
            self.last_id = _mechanism.mechanism_id

        return _error_code, _msg

    def delete(self, mechanism_id):
        """
        Method to remove the mechanism associated with Mechanism ID.

        :param int mechanism_id: the ID of the Mechanism to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _mechanism = self.tree.get_node(mechanism_id).data
            _error_code, _msg = RTKDataModel.delete(self, _mechanism)

            if _error_code == 0:
                self.tree.remove_node(mechanism_id)

        except AttributeError:
            _error_code = 2015
            _msg = 'RTK ERROR: Attempted to delete non-existent Mechanism ' \
                   'ID {0:d}.'.format(mechanism_id)

        return _error_code, _msg

    def update(self, mechanism_id):
        """
        Method to update the mechanism associated with Mechanism ID to the RTK
        Program database.

        :param int mechanism_id: the Mechanism ID Of the Mechanism to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _mechanism = self.tree.get_node(mechanism_id).data
            _error_code, _msg = RTKDataModel.update(self, _mechanism)
        except AttributeError:
            _error_code = 2016
            _msg = 'RTK ERROR: Attempted to save non-existent Mechanism ID ' \
                   '{0:d}.'.format(mechanism_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Mechanisms to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.mechanism_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return
            if _error_code != 0:
                print 'FIXME: Refactor ' \
                      'rtk.analyses.fmea.Mechanism.Model.update_all().'

        return _error_code, _msg


class Mechanism(RTKDataController):
    """
    The Mechanism data controller provides an interface between the Mechanism
    data model and an RTK view model.  A single Mechanism data controller can
    control one or more Mechanism data models.  Currently the Mechanism
    data controller is unused.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Mechanism data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Mode Data
                    Model.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.__test = kwargs['test']
        self._dtm_mechanism = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, mechanism_id):
        """
        Method to request the Mechanism Data Model to retrieve the RTKMechanism
        model associated with the Mode ID.

        :param int mechanism_id: the Mechanism ID to retrieve.
        :return: the RTKMechanism model requested.
        :rtype: `:py:class:rtk.dao.DAO.RTKMechansim` model
        """

        return self._dtm_mechanism.select(mechanism_id)

    def request_select_all(self, mode_id):
        """
        Method to retrieve the Mechanism tree from the Mechanism Data Model.

        :param int mode_id: the Mode ID to select the Mechanisms for.
        :return: tree; the treelib Tree() of RTKMechanism models in the
                 Mechanism tree.
        :rtype: dict
        """

        return self._dtm_mechanism.select_all(mode_id)

    def request_insert(self, mode_id):
        """
        Method to request the Mechanism Data Model to add a new Mechanism to
        the RTK Program database.

        :param int mode_id: the ID of the Mode the new Mechanism is to be
                            associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_mechanism.insert(mode_id=mode_id)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage(
                    'insertedMechanism',
                    mechanism_id=self._dtm_mechanism.last_id)
        else:
            _msg = _msg + '  Failed to add a new Mechanism to the RTK Program \
                           database.'

            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, mechanism_id):
        """
        Method to request the Mechanism Data Model to delete a Mechanism from
        the RTK Program database.

        :param int mechanism_id: the Mechanism ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_mechanism.delete(mechanism_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('deletedMechanism')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update(self, mechanism_id):
        """
        Method to request the Mechanism Data Model save the RTKMechanism
        attributes to the RTK Program database.

        :param int mechanism_id: the ID of the mechanism to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_mechanism.update(mechanism_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedMechanism')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Mechanism Data Model to save all RTKMechanism
        model attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        return self._dtm_mechanism.update_all()

    def request_calculate_rpn(self, mechanism_id, severity, severity_new):
        """
        Method to request RPN attributes be calculated for the Mechanism ID
        passed.

        :param int mechanism_id: the Mechanism ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, \
            _msg = self._dtm_mechanism.calculate_rpn(mechanism_id, severity,
                                                     severity_new)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('calculatedMechanism')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return
