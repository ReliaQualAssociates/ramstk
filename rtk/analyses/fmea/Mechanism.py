#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Mechanism.py is part of The RTK Project
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
FMEA Failure Mechanism Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub

# Import other RTK modules.
from datamodels import RTKDataModel
from datamodels import RTKDataController
from dao.RTKMechanism import RTKMechanism

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
        Methodt ot retrieve the instance of the RTKMechanism data model for the
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

        for _mechanism in  _session.query(RTKMechanism).\
                           filter(RTKMechanism.mode_id == mode_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default values.
            _attributes = _mechanism.get_attributes()
            _mechanism.set_attributes(_attributes[2:])
            self.tree.create_node(_mechanism.description,
                                  _mechanism.mechanism_id, parent = 0,
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
        _error_code, _msg = RTKDataModel.insert(self, [_mechanism, ])

        if _error_code == 0:
            self.tree.create_node(_mechanism.description,
                                  _mechanism.mechanism_id, parent=0,
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
                print _error_code

        return _error_code, _msg

    def calculate_rpn(self, mechanism_id, severity, severity_new):
        """
        Method to calculate the Risk Priority Number (RPN) for the Mechanism.

            RPN = S * O * D

        :param int mechanism_id: the ID of the Mechanism to calculate the RPN.
        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this Mechanism is associated
                             with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating failure mechanism {0:d} RPN.'.\
                format(mechanism_id)

        _mechanism = self.tree.get_node(mechanism_id).data

        if not 0 < severity < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < _mechanism.rpn_occurrence < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < _mechanism.rpn_detection < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN detection is outside the range "
                                    u"[1, 10]."))
        if not 0 < severity_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < _mechanism.rpn_occurrence_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < _mechanism.rpn_detection_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new detection is outside the range "
                                    u"[1, 10]."))

        _mechanism.rpn = int(severity) \
                * int(_mechanism.rpn_occurrence) \
                * int(_mechanism.rpn_detection)
        _mechanism.rpn_new = int(severity_new) \
                * int(_mechanism.rpn_occurrence_new) \
                * int(_mechanism.rpn_detection_new)

        if _mechanism.rpn < 1:
            _error_code = 2020
            _msg = 'Failure mechanism RPN has a value less than 1.'
            raise OutOfRangeError(_(u"Failure mechanism RPN has a value less "
                                    u"than 1."))
        if _mechanism.rpn_new > 1000:
            _error_code = 2020
            _msg = 'Failure mechanism RPN has a value greater than 1000.'
            raise OutOfRangeError(_(u"Failure mechanism RPN has a value "
                                    u"greater than 1000."))

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
                pub.sendMessage('insertedMechanism',
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

