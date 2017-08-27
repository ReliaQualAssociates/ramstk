#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Cause.py is part of The RTK Project
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
###############################################################################
FMEA Cause Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub

# Import other RTK modules.
from datamodels import RTKDataModel
from datamodels import RTKDataController
from dao.RTKCause import RTKCause

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


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

        for _cause in _session.query(RTKCause).filter(
                            RTKCause.mechanism_id == mechanism_id).all():
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

        try:
            _cause = self.tree.get_node(cause_id).data
            _error_code, _msg = RTKDataModel.update(self, _cause)
        except AttributeError:
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
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.cause_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg

    def calculate_rpn(self, cause_id, severity, severity_new):
        """
        Method to calculate the Risk Priority Number (RPN) for the Mechanism.

            RPN = S * O * D

        :param int cause_id: the ID of the Cause to calculate the RPN.
        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this Cause is associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating failure cause {0:d} RPN.'.\
                format(cause_id)

        _cause = self.tree.get_node(cause_id).data

        if not 0 < severity < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < _cause.rpn_occurrence < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < _cause.rpn_detection < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN detection is outside the range "
                                    u"[1, 10]."))
        if not 0 < severity_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < _cause.rpn_occurrence_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < _cause.rpn_detection_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new detection is outside the range "
                                    u"[1, 10]."))

        _cause.rpn = int(severity) \
                * int(_cause.rpn_occurrence) \
                * int(_cause.rpn_detection)
        _cause.rpn_new = int(severity_new) \
                * int(_cause.rpn_occurrence_new) \
                * int(_cause.rpn_detection_new)

        if _cause.rpn < 1:
            _error_code = 2030
            _msg = 'Failure cause RPN has a value less than 1.'
            raise OutOfRangeError(_(u"Failure cause RPN has a value less "
                                    u"than 1."))
        if _cause.rpn_new > 1000:
            _error_code = 2030
            _msg = 'Failure cause RPN has a value greater than 1000.'
            raise OutOfRangeError(_(u"Failure cause RPN has a value "
                                    u"greater than 1000."))

        return _error_code, _msg


class Cause(RTKDataController):
    """
    The Cause data controller provides an interface between the Cause data
    model and an RTK view model.  A single Cause controller can control one or
    more Cause data models.  Currently the Cause controller is unused.
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
        self.__test = kwargs['test']
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

        _return = False

        _error_code, _msg = self._dtm_cause.insert(mechanism_id=mechanism_id)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('insertedCause',
                                cause_id=self._dtm_cause.last_id)
        else:
            _msg = _msg + '  Failed to add a new Cause to the RTK Program \
                           database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, cause_id):
        """
        Method to request the Cause Data Model to delete a Cause from the RTK
        Program database.

        :param int cause_id: the Cause ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_cause.delete(cause_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('deletedCause')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update(self, cause_id):
        """
        Method to request the Cause Data Model save the RTKCause attributes to the RTK Program database.

        :param int cause_id: the ID of the cause to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_cause.update(cause_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedCause')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Cause Data Model to save all RTKCause model
        attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        return self._dtm_cause.update_all()

    def request_calculate_rpn(self, cause_id, severity, severity_new):
        """
        Method to request RPN attributes be calculated for the Cause ID
        passed.

        :param int cause_id: the Cause ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, \
            _msg = self._dtm_cause.calculate_rpn(cause_id, severity, 
                                                 severity_new)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('calculatedCause')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

