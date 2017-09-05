#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Control.py is part of The RTK Project
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
FMEA Control Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub                      # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel         # pylint: disable=E0401
from datamodels import RTKDataController    # pylint: disable=E0401
from dao.RTKControl import RTKControl       # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class Model(RTKDataModel):
    """
    The Control data model contains the attributes and methods of a FMEA
    control.  A Mechanism or a Cause will consist of one or more Controls.
    """

    _tag = 'Controls'

    def __init__(self, dao):
        """
        Method to initialize an Mode data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.last_id = None

    def select(self, control_id):
        """
        Method to retrieve the instance of the RTKControl data model for the
        Control ID passed.

        :param int control_id: the ID Of the Comtrol to retrieve.
        :return: the instance of the RTKControl class that was requested or
                 None if the requested Control ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKControl.RTKControl`
        """

        return RTKDataModel.select(self, control_id)

    def _select_all(self, parent_id, functional):
        """
        Helper method to retrieve all the Controls.

        :param int parent_id: the Mode ID (functional FMEA) or the Cause ID
                              (hardware FMEA) to select the Controls for.
        :param bool functional: indicates whether the Controls are for a
                                functional FMEA or a hardware FMEA (default).
        """

        _session = RTKDataModel.select_all(self)

        if functional:
            _controls = _session.query(RTKControl).filter(RTKControl.mode_id ==
                                                          parent_id).all()
        else:
            _controls = _session.query(RTKControl).filter(RTKControl.cause_id
                                                          == parent_id).all()

        _session.close()

        return _controls

    def select_all(self, parent_id, functional=False):
        """
        Method to retrieve all the Controls from the RTK Program database.
        Then add each to the Control treelib Tree().

        :param int parent_id: the Mode ID (functional FMEA) or the Cause ID
                              (hardware FMEA) to select the Controls for.
        :param bool functional: indicates whether the Controls are for a
                                functional FMEA or a hardware FMEA (default).
        :return: tree; the Tree() of RTKMode data models.
        :rtype: :py:class:`treelib.Tree`
        """

        for _control in self._select_all(parent_id, functional):
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _control.get_attributes()
            _control.set_attributes(_attributes[3:])
            self.tree.create_node(_control.description,
                                  _control.control_id,
                                  parent=0, data=_control)
            self.last_id = max(self.last_id, _control.control_id)

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Control to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _control = RTKControl()
        _control.mode_id = kwargs['mode_id']
        _control.cause_id = kwargs['cause_id']
        _error_code, _msg = RTKDataModel.insert(self, [_control, ])

        if _error_code == 0:
            self.tree.create_node(_control.description, _control.control_id,
                                  parent=0, data=_control)
            self.last_id = max(self.last_id, _control.control_id)

        return _error_code, _msg

    def delete(self, control_id):
        """
        Method to remove the control associated with Control ID.

        :param int control_id: the ID of the Control to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _control = self.tree.get_node(control_id).data
            _error_code, _msg = RTKDataModel.delete(self, _control)

            if _error_code == 0:
                self.tree.remove_node(control_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Control ' \
                   'ID {0:d}.'.format(control_id)

        return _error_code, _msg

    def update(self, control_id):
        """
        Method to update the mode associated with Control ID to the RTK
        Program database.

        :param int control_id: the Control ID of the Control to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _control = self.tree.get_node(control_id).data
            _error_code, _msg = RTKDataModel.update(self, _control)
        except AttributeError:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Control ID ' \
                   '{0:d}.'.format(control_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Controls to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.control_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg


class Control(RTKDataController):
    """
    The Control data controller provides an interface between the Control data
    model and an RTK view model.  A single Control controller can control one
    or more Control data models.  Currently the Control controller is unused.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Control data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Control Data
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
        self._dtm_control = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, control_id):
        """
        Method to request the Control Data Model to retrieve the RTKControl
        model associated with the Control ID.

        :param int control_id: the Control ID to retrieve.
        :return: the RTKControl model requested.
        :rtype: `:py:class:rtk.dao.DAO.RTKControl` model
        """

        return self._dtm_control.select(control_id)

    def request_select_all(self, parent_id, functional=False):
        """
        Method to retrieve the Control tree from the Control Data Model.

        :param int parent_id: the Mode ID (functional FMEA) or Cause ID
                              (hardware FMEA) to select the Controls for.
        :return: tree; the treelib Tree() of RTKControl models in the
                 Control tree.
        :rtype: treelib.Tree
        """

        return self._dtm_control.select_all(parent_id, functional)

    def request_insert(self, mode_id, cause_id):
        """
        Method to request the Control Data Model to add a new Control to the
        RTK Program database.

        :param int mode_id: the ID of the Mode the new Control is to be
                            associated with for a functional FMEA.
        :param int cause_id: the ID of the Cause the new Control is to be
                             associated with for a hardware FMEA.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_control.insert(mode_id=mode_id,
                                                     cause_id=cause_id)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('insertedControl',
                                mode_id=self._dtm_control.last_id,
                                parent_id=cause_id)
        else:
            _msg = _msg + '  Failed to add a new Control to the RTK Program \
                           database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, control_id):
        """
        Method to request the Control Data Model to delete a Control from the
        RTK Program database.

        :param int control_id: the Control ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_control.delete(control_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('deletedControl')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update(self, control_id):
        """
        Method to request the Control Data Model save the RTKControl
        attributes to the RTK Program database.

        :param int control_id: the ID of the control to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_control.update(control_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedControl')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Control Data Model to save all RTKControl
        model attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        return self._dtm_control.update_all()
