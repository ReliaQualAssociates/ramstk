# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Cause.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
FMEA Cause Module
###############################################################################
"""

from pubsub import pub                          # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel             # pylint: disable=E0401
from datamodels import RTKDataController        # pylint: disable=E0401
from dao.RTKCause import RTKCause               # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'


class OutOfRangeError(Exception):
    """
    Exception raised when an input value is outside legal limits.
    """

    def __init__(self, message):
        """
        Method to initialize OutOfRangeError instance.
        """

        Exception.__init__(self)

        self.message = message


class Model(RTKDataModel):
    """
    The Cause data model contains the attributes and methods of a FMEA cause.
    A :py:class:`rtk.analyses.fmea.Mechanism.Model` will have one or more
    Causes.
    """

    _tag = 'Causes'

    def __init__(self, dao):
        """
        Method to initialize a Cause data model instance.

        :param dao: the Data Access Object to Communicate with the RTK Program
                    database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.last_id = None

    def select(self, cause_id):
        """
        Method to retrieve the instance of the RTKCause data model for the
        Cause ID passed.

        :param int cause_id: the ID Of the Cause to retrieve.
        :return: the instance of the RTKCause class that was requested or
                 None if the requested Cause ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKCause.RTKCause`
        """

        return RTKDataModel.select(self, cause_id)

    def select_all(self, mechanism_id):
        """
        Method to retrieve all the Causes from the RTK Program database.
        Then add each to the Cause treelib Tree().

        :param int mechanism_id: the failure Mechanism ID to select the Causes
                                 for.
        :return: tree; the Tree() of RTKCause data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _cause in _session.query(RTKCause).filter(RTKCause.mechanism_id ==
                                                      mechanism_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _cause.get_attributes()
            _cause.set_attributes(_attributes[2:])
            self.tree.create_node(_cause.description, _cause.cause_id,
                                  parent=0, data=_cause)
            self.last_id = max(self.last_id, _cause.cause_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Cause to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _cause = RTKCause()
        _cause.mechanism_id = kwargs['mechanism_id']
        _error_code, _msg = RTKDataModel.insert(self, [_cause, ])

        if _error_code == 0:
            self.tree.create_node(_cause.description, _cause.cause_id,
                                  parent=0, data=_cause)
            self.last_id = _cause.cause_id

        return _error_code, _msg

    def delete(self, cause_id):
        """
        Method to remove the cause associated with Cause ID.

        :param int cause_id: the ID of the Cause to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _cause = self.tree.get_node(cause_id).data
            _error_code, _msg = RTKDataModel.delete(self, _cause)

            if _error_code == 0:
                self.tree.remove_node(cause_id)

        except AttributeError:
            _error_code = 2025
            _msg = 'RTK ERROR: Attempted to delete non-existent Cause ' \
                   'ID {0:d}.'.format(cause_id)

        return _error_code, _msg

    def update(self, cause_id):
        """
        Method to update the cause associated with Cause ID to the RTK
        Program database.

        :param int cause_id: the Cause ID of the Cause to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, cause_id)

        if _error_code != 0:
            _error_code = 2026
            _msg = 'RTK ERROR: Attempted to save non-existent Cause ID ' \
                   '{0:d}.'.format(cause_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Causes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Saving all Causes in the FMEA.'

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.cause_id)

                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.analyses.fmea.Cause.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.analyses.fmea.Cause.Model.update_all().'

        return _error_code, _msg


class Cause(RTKDataController):
    """
    The Cause data controller provides an interface between the Cause data
    model and an RTK view model.  A single Cause controller can control one or
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Cause controller instance.

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
        self._dtm_cause = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, cause_id):
        """
        Method to request the Cause Data Model to retrieve the RTKCause model
        associated with the Cause ID.

        :param int cause_id: the Cause ID to retrieve.
        :return: the RTKCause model requested.
        :rtype: `:py:class:rtk.dao.RTKCause.RTKCause` model
        """

        return self._dtm_cause.select(cause_id)

    def request_select_all(self, mechanism_id):
        """
        Method to retrieve the Cause tree from the Cause Data Model.

        :param int mechanism_id: the Mechanism ID to select the Causes for.
        :return: tree; the treelib Tree() of RTKCause models in the
                 Cause tree.
        :rtype: dict
        """

        return self._dtm_cause.select_all(mechanism_id)

    def request_insert(self, mechanism_id):
        """
        Method to request the Cause Data Model to add a new Cause to the RTK
        Program database.

        :param int mechanism_id: the ID of the Mechanism the new Cause is to be
                                 associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_cause.insert(mechanism_id=mechanism_id)

        if _error_code == 0 and not self._test:
            pub.sendMessage('insertedCause',
                            cause_id=self._dtm_cause.last_id)
        else:
            _msg = _msg + '  Failed to add a new Cause to the RTK Program ' \
                'database.'

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_delete(self, cause_id):
        """
        Method to request the Cause Data Model to delete a Cause from the RTK
        Program database.

        :param int cause_id: the Cause ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_cause.delete(cause_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'deletedCause')

    def request_update(self, cause_id):
        """
        Method to request the Cause Data Model save the RTKCause attributes to
        the RTK Program database.

        :param int cause_id: the ID of the cause to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_cause.update(cause_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'savedCause')

    def request_update_all(self):
        """
        Method to request the Cause Data Model to save all RTKCause model
        attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = self._dtm_cause.update_all()

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_calculate_rpn(self, cause_id, severity, severity_new):
        """
        Method to request RPN attributes be calculated for the Cause ID
        passed.

        :param int cause_id: the Cause ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, \
            _msg = self._dtm_cause.calculate_rpn(cause_id, severity,
                                                 severity_new)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'calculatedCause')
