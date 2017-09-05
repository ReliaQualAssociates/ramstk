#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Mode.py is part of The RTK Project
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
FMEA Failure Mode Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub                      # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel         # pylint: disable=E0401
from datamodels import RTKDataController    # pylint: disable=E0401
from dao.RTKMode import RTKMode             # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class Model(RTKDataModel):
    """
    The Mode data model contains the attributes and methods of a FMEA failure
    mode.  A :py:class:`rtk.analyses.fmea.FMEA` will consist of one or more
    failure modes.
    """

    _tag = 'Modes'

    def __init__(self, dao):
        """
        Method to initialize a Mode data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.last_id = None

    def select(self, mode_id):
        """
        Method to retrieve the instance of the RTKMode data model for the
        Mode ID passed.

        :param int mode_id: the ID Of the Mode to retrieve.
        :return: the instance of the RTKMode class that was requested or
                 None if the requested Mode ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKMode.RTKMode`
        """

        return RTKDataModel.select(self, mode_id)

    def select_all(self, parent_id, functional=False):
        """
        Method to retrieve all the Modes from the RTK Program database.
        Then add each to the Mode treelib Tree().

        :param int parent_id: the Function ID or the Hardware ID to select the
                              Modes for.
        :param bool functional: indicates whether to return Modeal
                                failure modes or Hardware failure modes.
        :return: tree; the Tree() of RTKMode data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        if functional:
            for _mode in _session.query(RTKMode).filter(
                            RTKMode.function_id == parent_id).all():
                # We get and then set the attributes to replace any None values
                # (NULL fields in the database) with their default value.
                _attributes = _mode.get_attributes()
                _mode.set_attributes(_attributes[3:])
                self.tree.create_node(_mode.description, _mode.mode_id,
                                      parent=0, data=_mode)
                self.last_id = max(self.last_id, _mode.mode_id)
        else:
            for _mode in _session.query(RTKMode).filter(
                            RTKMode.hardware_id == parent_id).all():
                # We get and then set the attributes to replace any None values
                # (NULL fields in the database) with their default value.
                _attributes = _mode.get_attributes()
                _mode.set_attributes(_attributes[3:])
                self.tree.create_node(_mode.description, _mode.mode_id,
                                      parent=0, data=_mode)
                self.last_id = max(self.last_id, _mode.mode_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Mode to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _mode = RTKMode()
        _mode.function_id = kwargs['function_id']
        _mode.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RTKDataModel.insert(self, [_mode, ])

        if _error_code == 0:
            self.tree.create_node(_mode.description, _mode.mode_id,
                                  parent=0, data=_mode)
            self.last_id = _mode.mode_id

        return _error_code, _msg

    def delete(self, mode_id):
        """
        Method to remove the mode associated with Mode ID.

        :param int mode_id: the ID of the Mode to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _mode = self.tree.get_node(mode_id).data
            _error_code, _msg = RTKDataModel.delete(self, _mode)

            if _error_code == 0:
                self.tree.remove_node(mode_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Mode ' \
                   'ID {0:d}.'.format(mode_id)

        return _error_code, _msg

    def update(self, mode_id):
        """
        Method to update the mode associated with Mode ID to the RTK
        Program database.

        :param int mode_id: the Mode ID of the Mode to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _mode = self.tree.get_node(mode_id).data
            _error_code, _msg = RTKDataModel.update(self, _mode)
        except AttributeError:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Mode ID ' \
                   '{0:d}.'.format(mode_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Modes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.mode_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg

class Mode(RTKDataController):
    """
    The Mode data controller provides an interface between the Mode
    data model and an RTK view model.  A single Mode controller can manage
    one or more Mode data models.  The attributes of a Mode data
    controller are:

    :ivar _dtm_mode: the :py:class:`rtk.analyses.fmea.Mode.Model` data model
                     associated with this data controller.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Mode data controller instance.

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
        self._dtm_mode = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, mode_id):
        """
        Method to request the Mode Data Model to retrieve the RTKMode
        model associated with the Mode ID.

        :param int mode_id: the Mode ID to retrieve.
        :return: the RTKMode model requested.
        :rtype: `:py:class:rtk.dao.DAO.RTKMode` model
        """

        return self._dtm_mode.select(mode_id)

    def request_select_all(self, parent_id, functional=False):
        """
        Method to retrieve the Mode tree from the Mode Data Model.

        :param int parent_id: the Function ID (functional FMEA) or Hardware ID
                              (hardware FMEA) to select the Modes for.
        :param bool functional: indicates whether or not to select the Modes
                                for a functional FMEA or hardware FMEA
                                (default).
        :return: tree; the treelib Tree() of RTKMode models in the
                 Mode tree.
        :rtype: dict
        """

        return self._dtm_mode.select_all(parent_id, functional)

    def request_insert(self, function_id, hardware_id):
        """
        Method to request the Mode Data Model to add a new Mode to the
        RTK Program database.

        :param int function_id: the ID of the Function the new Mode is to be
                                associated with.
        :param int hardware_id: the ID of the Hardware the new Mode is to be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_mode.insert(function_id=function_id,
                                                  hardware_id=hardware_id)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('insertedAction',
                                mode_id=self._dtm_action.last_id)
        else:
            _msg = _msg + '  Failed to add a new Mode to the RTK Program \
                           database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, mode_id):
        """
        Method to request the Mode Data Model to delete a Mode from the
        RTK Program database.

        :param int mode_id: the Mode ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_mode.delete(mode_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('deletedMode')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update(self, mode_id):
        """
        Method to request the Mode Data Model save the RTKMode
        attributes to the RTK Program database.

        :param int mode_id: the ID of the mode to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_mode.update(mode_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedMode')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Mode Data Model to save all RTKMode
        model attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        return self._dtm_mode.update_all()

    def request_calculate_criticality(self, mode_id, item_hr):
        """
        Method to request criticality attributes be calculated for the
        Mode ID passed.

        :param int mode_id: the Mode ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, \
            _msg = self._dtm_mode.calculate_criticality(mode_id, item_hr)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('calculatedMode')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return
