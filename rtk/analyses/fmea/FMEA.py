# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.FMEA.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
FMEA Module
###############################################################################
"""

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
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class Model(RTKDataModel):
    """
    The FMEA data model aggregates the Mode, Mechanism, Cause, Control and
    Action data models to produce an overall (D)FME(C)A.  A Function or
    Hardware item will consist of one (D)FME(C)A.  This is a hierarchical
    relationship, such as:

          Mode 1
          |
          |_Mechanism 1.1
          |   |
          |   |_Cause 1.1.1
          |   |   |
          |   |   |_Control 1.1.1.01
          |   |   |_Control 1.1.1.02
          |   |   |_Action 1.1.1.1
          |   |_Cause 1.1.2
          |       |
          |       |_Control 1.1.2.01
          |
          |_Mechanism 1.2
              |
              |_Cause 1.2.1
              |_Cause 1.2.2
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
        self._functional = False

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, node_id):
        """
        Method to retrieve the failure mode, failure mechanism, failure cause,
        control, or action from the FMEA tree for the ID passed.

        :param str node_id: the Node ID of the entity to select.
        :return: None if the ID produces no results or the instance of the
                 entity level requested for the ID pased.
        :rtype: Object
        """

        _entity = self.tree.nodes[node_id].data

        return _entity

    def select_all(self, parent_id, functional=False):
        """
        Method to retrieve and build the FMEA tree for Parent ID.  The Parent
        ID is one of Function ID (functional FMEA) or Hardware ID (hardware
        FMEA).

        :param str parent_id: the Function ID (functional FMEA) or Hardware ID
                              (hardware FMEA) to retrieve the FMEA and build
                              trees for.
        :param bool functional: indicates whether the FMEA is functional or
                                hardware.
        :return: tree; the FMEA treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        self._functional = functional

        RTKDataModel.select_all(self)

        _modes = self._dtm_mode.select_all(parent_id, functional).nodes

        for _key in _modes:
            _mode = _modes[_key].data
            if _mode is not None:
                _node_id = '0.' + str(_mode.mode_id)
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
        :param str parent_id: the Node ID to add the failure mechanisms to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _mechanisms = self._dtm_mechanism.select_all(mode_id).nodes
        for _key in _mechanisms:
            _mechanism = _mechanisms[_key].data
            if _mechanism is not None:
                _node_id = parent_id + '.' + str(_mechanism.mechanism_id)
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
        :param str parent_id: the Node ID to add the failure causes to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _causes = self._dtm_cause.select_all(mechanism_id).nodes
        for _key in _causes:
            _cause = _causes[_key].data
            if _cause is not None:
                _node_id = parent_id + '.' + str(_cause.cause_id)
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
        :param str parent_id: the Node ID to add the control methods to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _controls = self._dtm_control.select_all(cause_id, functional).nodes

        for _key in _controls:
            _control = _controls[_key].data
            if _control is not None:
                # Since Controls and Actions are at the same level in the FMEA
                # tree, we prepend a zero to the Control ID to differentiate it
                # from an Action.
                _node_id = parent_id + '.0' + str(_control.control_id)
                self.tree.create_node(tag=_control.description,
                                      identifier=_node_id,
                                      parent=parent_id,
                                      data=_control)

        return _return

    def _do_add_actions(self, cause_id, parent_id, functional):
        """
        Method to add the action to the FMEA tree for the Mode ID
        (funtional FMEA) or Cause ID (hardware FMEA) that is passed.

        :param int cause_id: the Mode ID (functional FMEA) or Cause ID
                             (hardware FMEA) to add the action to.
        :param str parent_id: the Node ID to add the action to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _actions = self._dtm_action.select_all(cause_id, functional).nodes
        for _key in _actions:
            _action = _actions[_key].data
            if _action is not None:
                _node_id = parent_id + '.' + str(_action.action_id)
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
        :param str parent_id: the Node ID of the parent node in the treelib
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

        if self._functional:
            _function_id = entity_id
            _hardware_id = -1
            _mode_id = entity_id
            _cause_id = -1
        else:
            _function_id = -1
            _hardware_id = entity_id
            _mode_id = -1
            _cause_id = entity_id

        if level == 'mode':
            _error_code, _msg = self._dtm_mode.insert(function_id=_function_id,
                                                      hardware_id=_hardware_id)
            _entity = self._dtm_mode.select(self._dtm_mode.last_id)
            _tag = 'Mode'
            _node_id = '0.' + str(self._dtm_mode.last_id)
        elif level == 'mechanism':
            _error_code, _msg = self._dtm_mechanism.insert(mode_id=entity_id)
            _entity = self._dtm_mechanism.select(self._dtm_mechanism.last_id)
            _tag = 'Mechanism'
            _node_id = parent_id + '.' + str(self._dtm_mechanism.last_id)
        elif level == 'cause':
            _error_code, _msg = self._dtm_cause.insert(mechanism_id=entity_id)
            _entity = self._dtm_cause.select(self._dtm_cause.last_id)
            _tag = 'Cause'
            _node_id = parent_id + '.' + str(self._dtm_cause.last_id)
        elif level == 'control':
            _error_code, _msg = self._dtm_control.insert(mode_id=_mode_id,
                                                         cause_id=_cause_id)
            _entity = self._dtm_control.select(self._dtm_control.last_id)
            _tag = 'Control'
            _node_id = parent_id + '.0' + str(self._dtm_control.last_id)
        elif level == 'action':
            _error_code, _msg = self._dtm_action.insert(mode_id=_mode_id,
                                                        cause_id=_cause_id)
            _entity = self._dtm_action.select(self._dtm_action.last_id)
            _tag = 'Action'
            _node_id = parent_id + '.' + str(self._dtm_action.last_id)
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

        :param str node_id: the Node ID of the entity to be removed.
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

        :param str node_id: the Node ID of the entity to save to the RTK
                            Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
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
        _msg = 'RTK SUCCESS: Saving all entities in the FMEA.'

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.identifier)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.analyses.fmea.Mode.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.analyses.fmea.FMEA.Model.update_all().'

        return _error_code, _msg

    def calculate_criticality(self, item_hr):
        """
        Method to calculate the FMEA MIL-STD-1629b, Task 102 criticality for
        all the failure Modes in the FMEA.
        """

        for _node in self.tree.children(0):
            _error_code, _msg = _node.data.calculate_criticality(item_hr)

        return _error_code, _msg

    def calculate_rpn(self, node_id, severity, severity_new):
        """
        Method to calculate the Mechanisms' RPN for the failure Mode ID that is
        passed.

        :param int node_id: the ID of the treelib Node to calculate the RPN.
        :param int severity: the severity of the failure Mode the Mechanism is
                             associated with.
        :param int severity_new: the severity of the failure Mode after
                                 corrective action.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        for _node in self.tree.children(node_id):
            _error_code, _msg = _node.data.calculate_rpn(severity,
                                                         severity_new)

        return _error_code, _msg


class FMEA(RTKDataController):
    """
    The FMEA data controller provides an interface between the FMEA data model
    and an RTK view model.  A single FMEA data controller can manage one or
    more FMEA data models.

    :ivar bool __test: indicates whether or not the FMEA Data Controller is
                       being tested.  Suppresses pypubsub calls.
    :ivar _dtm_fmea: the FMEA Data Model associated with the FMEA Data
                     Controller.
    :type _dtm_fmea: :py:class:`rtk.analyses.fmea.FMEA.Model`
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a FMEA controller instance.

        :param dao: the Data Access Object used by the FMEA Data Model to
                    communicate with the RTK Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        :param configuration: the configuration object instance for the running
                              RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_fmea = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, node_id):
        """
        Method to select the Node data package associated with node_id.

        :param str node_id: the Node ID of the data package to retrieve.
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
        :return: tree; the FMEA treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        return self._dtm_fmea.select_all(parent_id, functional)

    def request_insert(self, entity_id, parent_id, level):
        """
        Method to add a new entity to the FMEA managed by this controller.

        :param int entity_id: the RTK Program database Function ID, Hardware
                              ID, Mode ID, Mechanism ID, or Cause ID to add the
                              entity to.
        :param str parent_id: the Node ID of the parent node in the treelib
                              Tree().
        :param int level: the level in the FMEA to add the new entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_fmea.insert(entity_id, parent_id, level)

        return RTKDataController.handle_results(self, _error_code, _msg)

    def request_delete(self, node_id):
        """
        Method to request Mode, Mechanism, Cause, Control or Action and it's
        children be deleted from the FMEA.

        :param str node_id: the Mode, Mechanism, Cause, Controle, or Action ID
                            to add the entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_fmea.delete(node_id)

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_update_all(self):
        """
        Method to request the (D)FME(C)A be saved to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_fmea.update_all()

        return RTKDataController.handle_results(self, _error_code, _msg, None)
