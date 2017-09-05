#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.FMEA.py is part of The RTK Project
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
FMEA Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub                      # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel         # pylint: disable=E0401
from datamodels import RTKDataController    # pylint: disable=E0401
from .Mode import Model as Mode
from .Mechanism import Model as Mechanism
from .Cause import Model as Cause
from .Control import Model as Control
from .Action import Model as Action

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class Model(RTKDataModel):
    """
    The FMEA data model aggregates the Mode, Mechanism, Cause, Control and
    Action data models to produce an overall FMEA/FMECA.  A Function or
    Hardware item will consist of one FMEA.  This is a hierarchical
    relationship, such as:

          Mode 1
          |
          |_Mechanism 11
          |   |
          |   |_Cause 111
          |   |   |
          |   |   |_Control 1111
          |   |   |_Control 1112
          |   |   |_Action 1111
          |   |_Cause 112
          |       |
          |       |_Control 1121
          |
          |_Mechanism 12
              |
              |_Cause 121
              |_Cause 122
    """

    _tag = 'FMEA'

    def __init__(self, dao):
        """
        Method to initialize a Usage Profile data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_mode = Mode(dao)
        self._dtm_mechanism = Mechanism(dao)
        self._dtm_cause = Cause(dao)
        self._dtm_control = Control(dao)
        self._dtm_action = Action(dao)
        self._functional = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, entity_id, level='mode'):
        """
        Method to retieve the failure mode, failure mechanism, failure cause,
        control, or action from the FMEA tree for the ID passed.

        :param int entity_id: the ID of the entity to select.
        :param str level: the level of the entity in the FMEA structure.
                          Levels are:

                          * mode (default)
                          * mechanism
                          * cause
                          * control
                          * action

        :return: None if the ID and level produce no results or the instance of
                 the entity level requested for the ID pased.
        :rtype: Object
        """

        _entity = None

        if level == 'mode':
            _entity = self._dtm_mode.select(entity_id)
        elif level == 'mechanism':
            _entity = self._dtm_mechanism.select(entity_id)
        elif level == 'cause':
            _entity = self._dtm_cause.select(entity_id)
        elif level == 'control':
            _entity = self._dtm_control.select(entity_id)
        elif level == 'action':
            _entity = self._dtm_action.select(entity_id)

        return _entity

    def select_all(self, parent_id, functional=False):
        """
        Method to retrieve and build the FMEA tree for Parent ID.  The Parent
        ID is one of Function ID (functional FMEA) or Hardware ID (hardware
        FMEA).

        :param int parent_id: the Function ID (functional FMEA) or Hardware ID
                              (hardware FMEA) to retrieve the FMEA and build
                              trees for.
        :param bool functional: indicates whether the FMEA is functional or
                                hardware.
        :return: tree; the FMEA treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        self._functional = functional

        RTKDataModel.select_all(self)

        # Build the tree.  We concatenate the Mode ID and the Mechanism ID to
        # create the Node() identifier for Mechanisms.  This prevents the
        # likely case when the first Mode and Mechanism have the same ID (1) in
        # the database from causing problems when building the tree.  Do the
        # same for the causes by concatenating the Cause ID with the
        # Mode ID and Mechanism ID.
        _modes = self._dtm_mode.select_all(parent_id, functional).nodes

        for _key in _modes:
            _mode = _modes[_key].data
            if _mode is not None:
                _node_id = 'Mode_' + str(_mode.mode_id)
                self.tree.create_node(tag=_mode.description,
                                      identifier=_node_id,
                                      parent=0, data=_mode)
                if functional:
                    self._do_add_controls(_mode.mode_id, _node_id,
                                          functional)
                    self._do_add_actions(_mode.mode_id, _node_id,
                                         functional)
                else:
                    self._do_add_mechanisms(_mode.mode_id, _node_id)

        return self.tree

    def _do_add_mechanisms(self, mode_id, parent_id):
        """
        Method to add the failure mechanisms to the FMEA tree for the Mode ID
        that is passed.

        :param int mode_id: the Mode ID to add the failure mechanisms to.
        :param int parent_id: the Node ID to add the failure mechanisms to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _mechanisms = self._dtm_mechanism.select_all(mode_id).nodes
        for _key in _mechanisms:
            _mechanism = _mechanisms[_key].data
            if _mechanism is not None:
                _node_id = 'Mechanism_' + str(_mechanism.mechanism_id)
                self.tree.create_node(tag=_mechanism.description,
                                      identifier=_node_id,
                                      parent=parent_id,
                                      data=_mechanism)

                self._do_add_causes(_mechanism.mechanism_id, _node_id)

        return _return

    def _do_add_causes(self, mechanism_id, parent_id):
        """
        Method to add the failure causes to the FMEA tree for the Mechanism ID
        that is passed.

        :param int mechanism_id: the Mechanism ID to add the failure causes to.
        :param int parent_id: the Node ID to add the failure causes to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _causes = self._dtm_cause.select_all(mechanism_id).nodes
        for _key in _causes:
            _cause = _causes[_key].data
            if _cause is not None:
                _node_id = 'Cause_' + str(_cause.cause_id)
                self.tree.create_node(tag=_cause.description,
                                      identifier=_node_id,
                                      parent=parent_id,
                                      data=_cause)

                self._do_add_controls(_cause.cause_id, _node_id, False)
                self._do_add_actions(_cause.cause_id, _node_id, False)

        return _return

    def _do_add_controls(self, cause_id, parent_id, functional):
        """
        Method to add the control methods to the FMEA tree for the Mode ID
        (funtional FMEA) or Cause ID (hardware FMEA) that is passed.

        :param int cause_id: the Mode ID (functional FMEA) or Cause ID
                             (hardware FMEA) to add the control methods to.
        :param int parent_id: the Node ID to add the control methods to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _controls = self._dtm_control.select_all(cause_id, functional).nodes
        for _key in _controls:
            _control = _controls[_key].data
            if _control is not None:
                _node_id = 'Control_' + str(_control.control_id)
                self.tree.create_node(tag=_control.description,
                                      identifier=_node_id,
                                      parent=parent_id,
                                      data=_control)

        return _return

    def _do_add_actions(self, cause_id, parent_id, functional):
        """
        Method to add the control methods to the FMEA tree for the Mode ID
        (funtional FMEA) or Cause ID (hardware FMEA) that is passed.

        :param int cause_id: the Mode ID (functional FMEA) or Cause ID
                             (hardware FMEA) to add the control methods to.
        :param int parent_id: the Node ID to add the control methods to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _actions = self._dtm_action.select_all(cause_id, functional).nodes
        for _key in _actions:
            _action = _actions[_key].data
            if _action is not None:
                _node_id = 'Action_' + str(_action.action_id)
                self.tree.create_node(tag=_action.action_category,
                                      identifier=_node_id,
                                      parent=parent_id,
                                      data=_action)

        return _return

    def insert(self, entity_id, parent_id, level):
        """
        Method to add an entity to the FMEA and RTK Program database..

        :param int entity_id: the RTK Program database Function ID, Hardware
                              ID, Mode ID, Mechanism ID, or Cause ID to add the
                              entity to.
        :param int parent_id: the Node ID of the parent node in the treelib
                              Tree().
        :param str level: the type of entity to add to the FMEA.  Levels are:

                          * mode
                          * mechanim
                          * cause
                          * control
                          * action

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Adding an item to the FMEA.'
        _entity = None
        _tag = 'Tag'
        _node_id = -1

        if level == 'mode':
            if self._functional:
                _error_code, \
                _msg = self._dtm_mode.insert(function_id=entity_id,
                                             hardware_id=-1)
            else:
                _error_code, \
                _msg = self._dtm_mode.insert(function_id=-1,
                                             hardware_id=entity_id)
            _entity = self._dtm_mode.select(self._dtm_mode.last_id)
            _tag = 'Mode'
            _node_id = 'Mode_' + str(self._dtm_mode.last_id)
        elif level == 'mechanism':
            _error_code, _msg = self._dtm_mechanism.insert(mode_id=entity_id)
            _entity = self._dtm_mechanism.select(self._dtm_mechanism.last_id)
            _tag = 'Mechanism'
            _node_id = 'Mechanism_' + str(self._dtm_mechanism.last_id)
        elif level == 'cause':
            _error_code, _msg = self._dtm_cause.insert(mechanism_id=entity_id)
            _entity = self._dtm_cause.select(self._dtm_cause.last_id)
            _tag = 'Cause'
            _node_id = 'Cause_' + str(self._dtm_cause.last_id)
        elif level == 'control':
            if self._functional:
                _error_code, _msg = self._dtm_control.insert(mode_id=entity_id,
                                                             cause_id=-1)
            else:
                _error_code, \
                _msg = self._dtm_control.insert(mode_id=-1, cause_id=entity_id)
            _entity = self._dtm_control.select(self._dtm_control.last_id)
            _tag = 'Control'
            _node_id = 'Control_' + str(self._dtm_control.last_id)
        elif level == 'action':
            if self._functional:
                _error_code, _msg = self._dtm_action.insert(mode_id=entity_id,
                                                            cause_id=-1)
            else:
                _error_code, \
                _msg = self._dtm_action.insert(mode_id=-1, cause_id=entity_id)
            _entity = self._dtm_action.select(self._dtm_action.last_id)
            _tag = 'Action'
            _node_id = 'Action_' + str(self._dtm_action.last_id)
        else:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to add an item to the FMEA with ' \
                   'an undefined indenture level.  Level {0:s} was ' \
                   'requested.  Must be one of mode, mechanism, cause, ' \
                   'control, or action.'.format(level)

        self.tree.create_node(_tag, _node_id, parent=parent_id, data=_entity)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Method to remove an entity from the FMEA and RTK Program database.

        :param int node_id: the Node ID of the entity to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _entity = self.tree.get_node(node_id).data
        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete a non-existent entity ' \
                   'with Node ID {0:s} from the FMEA.'.format(node_id)
        else:
            _error_code, _msg = RTKDataModel.delete(self, _entity)

            if _error_code == 0:
                self.tree.remove_node(node_id)

        return _error_code, _msg

    def update(self, node_id):
        """
        Method to update the FMEA treelib Node data package to the RTK
        Program database.

        :param int node_id: the Node ID of the entity to save to the RTK
                            Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _entity = self.tree.get_node(node_id).data
            _error_code, _msg = RTKDataModel.update(self, _entity)
        except AttributeError:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent FMEA entity ' \
                   'with Node ID {0:s}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all FMEA data packages to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _key in self.tree.nodes:
            if _key != 0:
                _error_code, _msg = self.update(_key)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print _error_code

        return _error_code, _msg

    def calculate_criticality(self, item_hr):
        """
        Method to calculate the FMEA MIL-STD-1629b, Task 102 criticality for
        all the failure Modes in the FMEA.
        """

        for _node in self.tree.children(0):
            _error_code, _msg = _node.data.calculate_criticality(item_hr)

        return _error_code, _msg

    def calculate_mechanism_rpn(self, mode_id, severity, severity_new):
        """
        Method to calculate the Mechanisms' RPN for the failure Mode ID that is
        passed.

        :param int mode_id: the ID of the failure Mode to calculate the
                            Mechanims' RPN.
        :param int severity: the severity of the failure Mode the Mechanism is
                             associated with.
        :param int severity_new: the severity of the failure Mode after
                                 corrective action.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        for _node in self.tree.children(mode_id):
            _error_code, _msg = _node.data.calculate_rpn(severity,
                                                         severity_new)

        return _error_code, _msg

    def calculate_cause_rpn(self, mechanism_id, severity, severity_new):
        """
        Method to calculate the FMEA RPN for the failure Cause ID that is
        passed.

        :param int mechanism_id: the ID of the failure Mechanism to calculate
                                 the Causes' RPN.
        :param int severity: the severity of the failure Mode the Mechanism is
                             associated with.
        :param int severity_new: the severity of the failure Mode after
                                 corrective action.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        for _node in self.tree.children(mechanism_id):
            _error_code, _msg = _node.data.calculate_rpn(severity,
                                                         severity_new)

        return _error_code, _msg


class FMEA(RTKDataController):
    """
    The FMEA data controller provides an interface between the FMEA data model
    and an RTK view model.  A single FMEA data controller can manage one or
    more FMEA data models.

    :ivar _dao: default value: None
    :ivar dict dicDFMEA: Dictionary of the Hardware FMEA data models
                         controlled.  Key is the Hardware ID; value is a
                         pointer to the instance of the FMEA data model.
    :ivar dict dicFFMEA: Dictionary of the Function FMEA data models
                         controlled.  Key is the Function ID; value is a
                         pointer to the instance of the FMEA data model.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a FMEA controller instance.
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.__test = kwargs['test']
        self._dtm_fmea = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, node_id):
        """
        Method to select the Node data package associated with node_id.

        :param int node_id: the Node ID of the data package to retrieve.
        :return: the instance of the RTKMode, RTKMechanism. RTKCause,
                 RTKControl, or RTKAction associated with node_id.
        """

        return self._dtm_fmea.select(node_id)

    def request_select_all(self, parent_id, functional=False):
        """
        Method to load the entire FMEA for a Function or Hardware item.
        Starting at the Mode level, the steps to create the FMEA are:

        :param int parent_id: the Function ID (functional FMEA) or Hardware ID
                              (hardware FMEA) to retrieve the FMEA and build
                              trees for.
        :keyword bool functional: indicates whether the FMEA is functional or
                                  hardware.
        :return: tree; the FMEA treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        return self._dtm_fmea.select_all(parent_id, functional)

    def request_insert(self, entity_id, parent_id, level):
        """
        Method to add a new entity to the FMEA managed by this controller.

        :param int entity_id: the Hardware item ID to add the FMEA.
        :param int parent_id: the Function ID to add the FMEA.
        :param int level: the level in the FMEA to add the new entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_fmea.insert(entity_id, parent_id, level)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                if level == 0:
                    pub.sendMessage('addedMode')
                elif level == 1:
                    pub.sendMessage('addedMechanism')
                elif level == 2:
                    pub.sendMessage('addedCause')
                elif level == 3:
                    pub.sendMessage('addedControl')
                elif level == 4:
                    pub.sendMessage('addedAction')

        else:
            _msg = _msg + '  Failed to add a new FMEA entity to the RTK ' \
                    'Program '
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, node_id):
        """
        Method to request Mode, Mechanism, Cause, Control or Action and it's
        children be deleted from the FMEA.

        :param int node_id: the Mode, Mechanism, Cause, Controle, or Action ID
                            to add the entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_fmea.delete(node_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Usage Profile be saved to the RTK Program
        database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_fmea.update_all()

        # If the update was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

