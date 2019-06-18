# -*- coding: utf-8 -*-
#
#       ramstk.analyses.fmea.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Models."""

# Third Party Imports
from pubsub import pub
from treelib import tree

# RAMSTK Package Imports
from ramstk.dao import (
    RAMSTKAction, RAMSTKCause, RAMSTKControl, RAMSTKMechanism, RAMSTKMode,
)
from ramstk.modules import RAMSTKDataModel
from ramstk.Utilities import OutOfRangeError


class ModeDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a failure Mode.

    An RAMSTK Project will consist of one or more Modes.  The attributes of a
    Mode are inherited.
    """

    _tag = 'Modes'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Mode data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the failure Modes from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKMode table in the
        connected RAMSTK Program database.  It then add each to the Mode data
        model treelib.Tree().

        :param int parent_id: the Function ID or Hardware ID the failure Modes
        are associated with.
        :return: tree; the Tree() of RAMSTKMode data models.
        :rtype: :py:class:`treelib.Tree`
        """
        _parent_id = kwargs['parent_id']
        _functional = kwargs['functional']

        _session = RAMSTKDataModel.do_select_all(self)

        if _functional:
            _modes = _session.query(RAMSTKMode).filter(
                RAMSTKMode.function_id == _parent_id, ).all()
        else:
            _modes = _session.query(RAMSTKMode).filter(
                RAMSTKMode.hardware_id == _parent_id, ).all()

        for _mode in _modes:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _mode.get_attributes()
            _mode.set_attributes(_attributes)
            self.tree.create_node(
                _mode.description,
                _mode.mode_id,
                parent=self._root,
                data=_mode,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _mode.mode_id)
            except TypeError:
                self.last_id = _mode.mode_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKMode table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _mode = RAMSTKMode()
        _mode.function_id = kwargs['function_id']
        _mode.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self,
            entities=[
                _mode,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _mode.description,
                _mode.mode_id,
                parent=self._root,
                data=_mode,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _mode.mode_id)
            except TypeError:
                self.last_id = self.last_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKMode table.

        :param int node_id: the ID of the RAMSTKMode record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Mode ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Mode ID of the Mode to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Mode ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKMode table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the FMEA modes "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the FMEA modes "
                "table did not update."
            )

        return _error_code, _msg


class MechanismDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a failure Mechanism.

    An RAMSTK Project will consist of one or more Mechanisms.  The attributes of
    a Mechanism are inherited.
    """

    _tag = 'Mechanisms'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Mechanism data mechanisml instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the failure Mechanisms from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKMechanism table in
        the connected RAMSTK Program database.  It then add each to the Mechanism
        data mechanism treelib.Tree().

        :return: tree; the Tree() of RAMSTKMechanism data mechanismls.
        :rtype: :class:`treelib.Tree`
        """
        _parent_id = kwargs['parent_id']
        _session = RAMSTKDataModel.do_select_all(self)

        _mechanisms = _session.query(RAMSTKMechanism).filter(
            RAMSTKMechanism.mode_id == _parent_id, ).all()

        for _mechanism in _mechanisms:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _mechanism.get_attributes()
            _mechanism.set_attributes(_attributes)
            self.tree.create_node(
                _mechanism.description,
                _mechanism.mechanism_id,
                parent=self._root,
                data=_mechanism,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _mechanism.mechanism_id)
            except TypeError:
                self.last_id = _mechanism.mechanism_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKMechanism table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _mechanism = RAMSTKMechanism()
        _mechanism.mode_id = kwargs['mode_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self,
            entities=[
                _mechanism,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _mechanism.description,
                _mechanism.mechanism_id,
                parent=self._root,
                data=_mechanism,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _mechanism.mechanism_id)
            except TypeError:
                self.last_id = self.last_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKMechanism table.

        :param int node_id: the ID of the RAMSTKMechanism record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Mechanism ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Mechanism ID of the Mechanism to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Mechanism ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKMechanism table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the FMEA mechanisms "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the FMEA "
                "mechanisms table did not update."
            )

        return _error_code, _msg


class CauseDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a failure Cause.

    An RAMSTK Project will consist of one or more Causes.  The attributes of a
    Cause are:
    """

    _tag = 'Causes'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Cause data causel instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the failure Causes from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKCause table in the
        connected RAMSTK Program database.  It then add each to the Cause data
        causel treelib.Tree().

        :param int parent_id: the Function ID or Hardware ID the failure Causes
                              are associated with.
        :return: tree; the Tree() of RAMSTKCause data causels.
        :rtype: :class:`treelib.Tree`
        """
        _parent_id = kwargs['parent_id']
        _functional = kwargs['functional']

        _session = RAMSTKDataModel.do_select_all(self)

        if _functional:
            _causes = _session.query(RAMSTKCause).filter(
                RAMSTKCause.mode_id == _parent_id, ).all()
        else:
            _causes = _session.query(RAMSTKCause).filter(
                RAMSTKCause.mechanism_id == _parent_id, ).all()

        for _cause in _causes:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _cause.get_attributes()
            _cause.set_attributes(_attributes)
            self.tree.create_node(
                _cause.description,
                _cause.cause_id,
                parent=self._root,
                data=_cause,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _cause.cause_id)
            except TypeError:
                self.last_id = _cause.cause_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKCause table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _cause = RAMSTKCause()
        _cause.mode_id = kwargs['mode_id']
        _cause.mechanism_id = kwargs['mechanism_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self,
            entities=[
                _cause,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _cause.description,
                _cause.cause_id,
                parent=self._root,
                data=_cause,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _cause.cause_id)
            except TypeError:
                self.last_id = self.last_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKCause table.

        :param int node_id: the ID of the RAMSTKCause record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Cause ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Cause ID of the Cause to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Cause ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKCause table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the FMEA causes "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the FMEA causes "
                "table did not update."
            )

        return _error_code, _msg


class ControlDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a FMEA Control.

    An RAMSTK Project will consist of one or more Controls.  The attributes of a
    Control are inherited.
    """

    _tag = 'Controls'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Control data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Controls from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKControl table in the
        connected RAMSTK Program database.  It then add each to the Control data
        model treelib.Tree().

        :param int parent_id: Mode ID or Cause ID the Controls are associated
                              with.
        :return: tree; the Tree() of RAMSTKControl data models.
        :rtype: :class:`treelib.Tree`
        """
        _parent_id = kwargs['parent_id']

        _session = RAMSTKDataModel.do_select_all(self)

        _controls = _session.query(RAMSTKControl).filter(
            RAMSTKControl.cause_id == _parent_id, ).all()

        for _control in _controls:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _control.get_attributes()
            _control.set_attributes(_attributes)
            self.tree.create_node(
                _control.description,
                _control.control_id,
                parent=self._root,
                data=_control,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _control.control_id)
            except TypeError:
                self.last_id = _control.control_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKControl table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _control = RAMSTKControl()
        _control.cause_id = kwargs['cause_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self,
            entities=[
                _control,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _control.description,
                _control.control_id,
                parent=self._root,
                data=_control,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _control.control_id)
            except TypeError:
                self.last_id = self.last_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKControl table.

        :param int node_id: the ID of the RAMSTKMode record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Control ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Mode ID of the Mode to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Control ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKControl table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the FMEA controls "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the FMEA controls "
                "table did not update."
            )

        return _error_code, _msg


class ActionDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a FMEA Action.

    An RAMSTK Project will consist of one or more Actions.  The attributes of a
    Action are inherited.
    """

    _tag = 'Actions'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Action data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Actions from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKAction table in the
        connected RAMSTK Program database.  It then add each to the Action data
        model treelib.Tree().

        :return: tree; the Tree() of RAMSTKAction data models.
        :rtype: :class:`treelib.Tree`
        """
        _parent_id = kwargs['parent_id']
        _session = RAMSTKDataModel.do_select_all(self)

        _actions = _session.query(RAMSTKAction).filter(
            RAMSTKAction.cause_id == _parent_id, ).all()

        for _action in _actions:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _action.get_attributes()
            _action.set_attributes(_attributes)
            self.tree.create_node(
                _action.action_status,
                _action.action_id,
                parent=self._root,
                data=_action,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _action.action_id)
            except TypeError:
                self.last_id = _action.action_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKAction table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _action = RAMSTKAction()
        _action.cause_id = kwargs['cause_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self,
            entities=[
                _action,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _action.action_status,
                _action.action_id,
                parent=self._root,
                data=_action,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _action.action_id)
            except TypeError:
                self.last_id = self.last_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKAction table.

        :param int node_id: the ID of the RAMSTKMode record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # last_id is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Action ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Mode ID of the Mode to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Action ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKAction table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the FMEA actions "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the FMEA actions "
                "table did not update."
            )

        return _error_code, _msg


class FMEADataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a FMEA.

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
    _root = '0'

    def __init__(self, dao, **kwargs):
        """
        Initialize a FMEA data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :py:class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._test = kwargs['test']
        self._functional = False

        # Initialize public dictionary attributes.
        self.item_criticality = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_mode = ModeDataModel(dao)
        self.dtm_mechanism = MechanismDataModel(dao)
        self.dtm_cause = CauseDataModel(dao)
        self.dtm_control = ControlDataModel(dao)
        self.dtm_action = ActionDataModel(dao)

    def do_select_all(self, **kwargs):
        """
        Retrieve and build the FMEA tree for Parent ID.

        The Parent ID is one of Function ID (functional FMEA) or Hardware ID
        (hardware FMEA).

        :return: None
        :rtype: None
        """
        self._functional = kwargs['functional']
        _parent_id = kwargs['parent_id']

        RAMSTKDataModel.do_select_all(self)

        _modes = self.dtm_mode.do_select_all(
            parent_id=_parent_id,
            functional=self._functional,
        ).nodes

        for _key in _modes:
            _mode = _modes[_key].data
            if _mode is not None:
                _node_id = '0.' + str(_mode.mode_id)
                self.tree.create_node(
                    tag=_mode.description,
                    identifier=_node_id,
                    parent=self._root,
                    data=_mode,
                )
                if self._functional:
                    self._do_add_causes(_mode.mode_id, _node_id, True)
                else:
                    self._do_add_mechanisms(_mode.mode_id, _node_id)

        # If we're not running a test and there were allocations returned,
        # let anyone who cares know the Allocations have been selected.
        if not self._test and self.tree.size() > 1:
            if self._functional:
                pub.sendMessage(
                    'retrieved_ffmea',
                    attributes={
                        'tree': self.tree,
                        'row': None,
                        'parent_id': _parent_id,
                    },
                )
            else:
                pub.sendMessage(
                    'retrieved_dfmeca',
                    attributes={
                        'tree': self.tree,
                        'row': None,
                        'parent_id': _parent_id,
                    },
                )

    def _do_add_mechanisms(self, mode_id, parent_id):
        """
        Add the failure mechanisms to the FMEA tree for Mode ID.

        :param int mode_id: the Mode ID to add the failure mechanisms to.
        :param str parent_id: the Node ID to add the failure mechanisms to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _mechanisms = self.dtm_mechanism.do_select_all(parent_id=mode_id).nodes
        for _key in _mechanisms:
            _mechanism = _mechanisms[_key].data
            if _mechanism is not None:
                _node_id = parent_id + '.' + str(_mechanism.mechanism_id)
                self.tree.create_node(
                    tag=_mechanism.description,
                    identifier=_node_id,
                    parent=parent_id,
                    data=_mechanism,
                )

                self._do_add_causes(_mechanism.mechanism_id, _node_id, False)

        return _return

    def _do_add_causes(self, parent_id, parent_node, functional):
        """
        Add the failure causes to the FMEA tree for Mechanism ID.

        :param int parent_id: the Mode ID (functional FMEA) or Mechanism ID
                              (hardware FMEA) to add the failure causes to.
        :param str parent_node: the Node ID to add the failure causes to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _causes = self.dtm_cause.do_select_all(
            parent_id=parent_id,
            functional=functional,
        ).nodes
        for _key in _causes:
            _cause = _causes[_key].data
            if _cause is not None:
                _node_id = parent_node + '.' + str(_cause.cause_id)
                self.tree.create_node(
                    tag=_cause.description,
                    identifier=_node_id,
                    parent=parent_node,
                    data=_cause,
                )

                self._do_add_controls(_cause.cause_id, _node_id)
                self._do_add_actions(_cause.cause_id, _node_id)

        return _return

    def _do_add_controls(self, cause_id, parent_id):
        """
        Add the control methods to the FMEA tree for Mode ID or Cause ID.

        :param int cause_id: the Mode ID (functional FMEA) or Cause ID
                             (hardware FMEA) to add the control methods to.
        :param str parent_id: the Node ID to add the control methods to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _controls = self.dtm_control.do_select_all(parent_id=cause_id).nodes

        for _key in _controls:
            _control = _controls[_key].data
            if _control is not None:
                # Since Controls and Actions are at the same level in the FMEA
                # tree, we prepend a zero to the Control ID to differentiate it
                # from an Action.
                _node_id = parent_id + '.' + str(_control.control_id) + 'c'
                self.tree.create_node(
                    tag=_control.description,
                    identifier=_node_id,
                    parent=parent_id,
                    data=_control,
                )

        return _return

    def _do_add_actions(self, cause_id, parent_id):
        """
        Add the action to the FMEA tree for Mode ID or Cause ID.

        :param int cause_id: the Mode ID (functional FMEA) or Cause ID
                             (hardware FMEA) to add the action to.
        :param str parent_id: the Node ID to add the action to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _actions = self.dtm_action.do_select_all(parent_id=cause_id).nodes
        for _key in _actions:
            _action = _actions[_key].data
            if _action is not None:
                _node_id = parent_id + '.' + str(_action.action_id) + 'a'
                self.tree.create_node(
                    tag=_action.action_category,
                    identifier=_node_id,
                    parent=parent_id,
                    data=_action,
                )

        return _return

    def do_insert(self, **kwargs):
        """
        Add an entity to the FMEA and RAMSTK Program database..

        :param int entity_id: the RAMSTK Program database Function ID, Hardware
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
        _msg = 'RAMSTK SUCCESS: Adding an item to the FMEA.'
        _entity = None
        _tag = 'Tag'
        _node_id = -1

        _entity_id = kwargs['entity_id']
        _parent_id = kwargs['parent_id']
        _level = kwargs['level']
        if self._functional:
            _function_id = _entity_id
            _hardware_id = -1
        else:
            _function_id = -1
            _hardware_id = _entity_id

        if _level == 'mode':
            _error_code, _msg = self.dtm_mode.do_insert(
                function_id=_function_id,
                hardware_id=_hardware_id,
            )
            _entity = self.dtm_mode.do_select(self.dtm_mode.last_id)
            _tag = 'Mode'
            _node_id = '0.' + str(self.dtm_mode.last_id)
        elif _level == 'mechanism':
            _error_code, _msg = self.dtm_mechanism.do_insert(
                mode_id=_entity_id, )
            _entity = self.dtm_mechanism.do_select(self.dtm_mechanism.last_id)
            _tag = 'Mechanism'
            _node_id = _parent_id + '.' + str(self.dtm_mechanism.last_id)
        elif _level == 'cause':
            if self._functional:
                _error_code, _msg = self.dtm_cause.do_insert(
                    mode_id=_entity_id,
                    mechanism_id=-1,
                )
            else:
                _error_code, _msg = self.dtm_cause.do_insert(
                    mode_id=-1,
                    mechanism_id=_entity_id,
                )
            _entity = self.dtm_cause.do_select(self.dtm_cause.last_id)
            _tag = 'Cause'
            _node_id = _parent_id + '.' + str(self.dtm_cause.last_id)
        elif _level == 'control':
            _error_code, _msg = self.dtm_control.do_insert(cause_id=_entity_id)
            _entity = self.dtm_control.do_select(self.dtm_control.last_id)
            _tag = 'Control'
            _node_id = _parent_id + '.' + str(self.dtm_control.last_id) + 'c'
        elif _level == 'action':
            _error_code, _msg = self.dtm_action.do_insert(cause_id=_entity_id)
            _entity = self.dtm_action.do_select(self.dtm_action.last_id)
            _tag = 'Action'
            _node_id = _parent_id + '.' + str(self.dtm_action.last_id) + 'a'
        else:
            _error_code = 2005
            _msg = 'RAMSTK ERROR: Attempted to add an item to the FMEA with ' \
                   'an undefined indenture level.  Level {0:s} was ' \
                   'requested.  Must be one of mode, mechanism, cause, ' \
                   'control, or action.'.format(_level)

        try:
            self.tree.create_node(
                _tag,
                _node_id,
                parent=_parent_id,
                data=_entity,
            )
        except tree.NodeIDAbsentError:
            _error_code = 2005
            _msg = 'RAMSTK ERROR: Attempted to add an item under ' \
                   'non-existent Node ID {0:s} in Failure Mode and Effects ' \
                   'Analysis.'.format(str(_parent_id))

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKControl table.

        :param int node_id: the ID of the RAMSTKMode record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'entity with Node ID {0:s} from the ' \
                          'FMEA.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Mode ID of the Mode to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 1
            if self._functional:
                _msg = "RAMSTK ERROR: Attempted to save non-existent " \
                       "Functional FMEA entity with Node ID " \
                       "{0:s}.".format(node_id)
            else:
                _msg = "RAMSTK ERROR: Attempted to save non-existent " \
                       "Hardware FMEA entity with Node ID " \
                       "{0:s}.".format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all FMEA table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all line items in the FMEA.")
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more line items in the FMEA did not "
                "update."
            )

        return _error_code, _msg

    def do_calculate(self, item_hr, criticality, rpn):  # pylint: disable=arguments-differ
        """
        Calculate the RPN or criticality for the selected Node ID.

        :param str node_id: the PyPubSub Tree() ID of the failure Mode to
        calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        if criticality:
            (_error_code, _msg) = self._do_calculate_criticality(item_hr)

        if rpn:
            (_error_code, _msg) = self._do_calculate_rpn()

        return (_error_code, _msg)

    def _do_calculate_criticality(self, item_hr):
        """
        Calculate the FMEA MIL-STD-1629b, Task 102 criticality.

        :param float item_hr: the hazard rate of the item the criticality is
        being calculated for.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        self.item_criticality = {}
        for _node in self.tree.children(self._root):
            _error_code, _msg = _node.data.calculate_criticality(item_hr)
            try:
                self.item_criticality[
                    _node.data.severity_class
                ] += _node.data.mode_criticality
            except KeyError:
                self.item_criticality[
                    _node.data.severity_class
                ] = _node.data.mode_criticality

        return _error_code, _msg

    def _do_calculate_rpn(self):
        """
        Calculate the Risk Priority Number (RPN).

        :param int node_id: the ID of the treelib Node to calculate the RPN.
        :param int severity: the severity of the failure Mode the Mechanism is
        associated with.
        :param int severity_new: the severity of the failure Mode after
        corrective action.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK INFO: Success calculating (D)FME(C)A.'

        for _node in self.tree.children(self._root):
            if _node.data is None:
                _msg = "Node ID: {0:s} has no data package.".format(
                    str(_node.identifier), )
            elif _node.data.is_mode:
                for _child in self.tree.subtree(_node.identifier).all_nodes():
                    try:
                        _error_code, _msg = _child.data.calculate_rpn(
                            _node.data.rpn_severity,
                            _node.data.rpn_severity_new,
                        )
                    except OutOfRangeError as _error:
                        _error_code = 1
                        _msg = _error.message
                    except AttributeError:
                        _msg = (
                            "Node ID: {0:s} is not a Mechanism or Cause."
                        ).format(str(_child.identifier))

        return _error_code, _msg
