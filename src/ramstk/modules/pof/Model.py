# -*- coding: utf-8 -*-
#
#       ramstk.modules.physics_of_failure.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Physics of Failure Data Model."""

# Import third party packages.
from pubsub import pub
from treelib import tree

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataModel
from ramstk.modules.fmea import dtmMode, dtmMechanism
from ramstk.dao import RAMSTKOpLoad, RAMSTKOpStress, RAMSTKTestMethod


class OpLoadDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a failure OpLoad.

    An RAMSTK Project will consist of one or more OpLoads.  The attributes of a
    OpLoad are:
    """

    _tag = 'OpLoads'

    def __init__(self, dao):
        """
        Initialize a OpLoad data model instance.

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
        Retrieve all the operating loads from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKOpLoad table in the
        connected RAMSTK Program database.  It then add each to the OpLoad data
        model treelib.Tree().

        :param int parent_id: the Mechanism ID the operating loads are
                              associated with.
        :return: tree; the Tree() of RAMSTKOpLoad data models.
        :rtype: :class:`treelib.Tree`
        """
        _parent_id = kwargs['parent_id']
        _session = RAMSTKDataModel.do_select_all(self)

        _oploads = _session.query(RAMSTKOpLoad).filter(
            RAMSTKOpLoad.mechanism_id == _parent_id).all()

        for _opload in _oploads:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _opload.get_attributes()
            _opload.set_attributes(_attributes)
            self.tree.create_node(
                _opload.description, _opload.load_id, parent=0, data=_opload)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _opload.load_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RAMSTKOpLoad table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _opload = RAMSTKOpLoad()
        _opload.mechanism_id = kwargs['mechanism_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _opload,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _opload.description, _opload.load_id, parent=0, data=_opload)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _opload.load_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKOpLoad table.

        :param int node_id: the ID of the RAMSTKOpLoad record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'OpLoad ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the OpLoad ID of the OpLoad to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent OpLoad ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKOpLoad table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.data.load_id)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = (
                    "RAMSTK ERROR: One or more operating loads in the damage "
                    "modeling worksheet did not update.")

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all operating loads in the damage "
                "modeling worksheet.")

        return _error_code, _msg


class OpStressDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a failure OpStress.

    An RAMSTK Project will consist of one or more OpStresss.  The attributes of a
    OpStress are:
    """

    _tag = 'OpStresss'

    def __init__(self, dao):
        """
        Initialize a OpStress data model instance.

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
        Retrieve all the operating stresss from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKOpStress table in the
        connected RAMSTK Program database.  It then add each to the OpStress data
        model treelib.Tree().

        :param int parent_id: the Mechanism ID the operating stresss are
                              associated with.
        :return: tree; the Tree() of RAMSTKOpStress data models.
        :rtype: :class:`treelib.Tree`
        """
        _load_id = kwargs['parent_id']
        _session = RAMSTKDataModel.do_select_all(self)

        _opstresses = _session.query(RAMSTKOpStress).filter(
            RAMSTKOpStress.load_id == _load_id).all()

        for _opstress in _opstresses:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _opstress.get_attributes()
            _opstress.set_attributes(_attributes)
            self.tree.create_node(
                _opstress.description,
                _opstress.stress_id,
                parent=0,
                data=_opstress)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _opstress.stress_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RAMSTKOpStress table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _opstress = RAMSTKOpStress()
        _opstress.load_id = kwargs['load_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _opstress,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _opstress.description,
                _opstress.stress_id,
                parent=0,
                data=_opstress)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _opstress.stress_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKOpStress table.

        :param int node_id: the ID of the RAMSTKOpStress record to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'OpStress ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the OpStress ID of the OpStress to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent OpStress ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKOpStress table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.data.stress_id)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RAMSTK ERROR: One or more operating stresses in the "
                        "damage modeling worksheet did not update.")

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all operating stresses in the "
                    "damage modeling worksheet.")

        return _error_code, _msg


class TestMethodDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a failure TestMethod.

    An RAMSTK Project will consist of one or more TestMethods.  The attributes of a
    TestMethod are:
    """

    _tag = 'TestMethods'

    def __init__(self, dao):
        """
        Initialize a TestMethod data model instance.

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
        Retrieve all the operating stresss from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKTestMethod table in the
        connected RAMSTK Program database.  It then add each to the TestMethod data
        model treelib.Tree().

        :param int parent_id: the Mechanism ID the operating stresss are
                              associated with.
        :return: tree; the Tree() of RAMSTKTestMethod data models.
        :rtype: :class:`treelib.Tree`
        """
        _parent_id = kwargs['parent_id']
        _session = RAMSTKDataModel.do_select_all(self)

        _testmethods = _session.query(RAMSTKTestMethod).filter(
            RAMSTKTestMethod.load_id == _parent_id).all()

        for _testmethod in _testmethods:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _testmethod.get_attributes()
            _testmethod.set_attributes(_attributes)
            self.tree.create_node(
                _testmethod.description,
                _testmethod.test_id,
                parent=0,
                data=_testmethod)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _testmethod.test_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RAMSTKTestMethod table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _testmethod = RAMSTKTestMethod()
        _testmethod.load_id = kwargs['load_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _testmethod,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _testmethod.description,
                _testmethod.test_id,
                parent=0,
                data=_testmethod)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _testmethod.test_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKTestMethod table.

        :param int node_id: the ID of the RAMSTKTestMethod record to be removed
                            from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'TestMethod ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the TestMethod ID of the TestMethod to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent TestMethod ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKTestMethod table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.data.load_id)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RAMSTK ERROR: One or more test methods in the damage "
                        "modeling worksheet did not update.")

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all test methods in the damage "
                    "modeling worksheet.")

        return _error_code, _msg


class PhysicsOfFailureDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a PhysicsOfFailure (PoF).

    The PhysicsOfFailure data model aggregates the Mechanism, OpLoad, OpStress
    and TestMethod data models to produce an overall PoF.  A Hardware item will
    consist of one PoF.  This is a hierarchical relationship, such as:

        Mode 1
          |
          |_Mechanism 1.1
              |
              |_Load 1.1.1
              |   |
              |   |_Stress 1.1.1.1s
              |   |_Stress 1.1.1.2s
              |   |_Test 1.1.1.1t
              |   |_Test 1.1.1.2t
              |
              |_Load 1.1.2
                  |
                  |_Stress 1.1.2.1s
                  |_Stress 1.1.2.2s
                  |_Test 1.1.2.1t
    """

    _tag = 'PhysicsOfFailure'

    def __init__(self, dao, **kwargs):
        """
        Initialize a PhysicsOfFailure data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._test = kwargs['test']
        self._functional = False

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_mode = dtmMode(dao)
        self.dtm_mechanism = dtmMechanism(dao)
        self.dtm_opload = OpLoadDataModel(dao)
        self.dtm_opstress = OpStressDataModel(dao)
        self.dtm_testmethod = TestMethodDataModel(dao)

    def do_select_all(self, **kwargs):
        """
        Retrieve and build the Physics of Failure tree for Hardware ID.

        :param str hardware_id: the Hardware ID to retrieve the Physics of
                                Failure information and build trees for.
        :return: tree; the PhysicsOfFailure treelib Tree().
        :rtype: :class:`treelib.Tree`
        """
        _hardware_id = kwargs['hardware_id']
        RAMSTKDataModel.do_select_all(self)

        _modes = self.dtm_mode.do_select_all(
            parent_id=_hardware_id, functional=False).nodes
        for _key in _modes:
            _mode = _modes[_key].data
            if _mode is not None:
                _node_id = '0.{0:d}'.format(_mode.mode_id)
                self.tree.create_node(
                    tag=_mode.description,
                    identifier=_node_id,
                    parent=0,
                    data=_mode)

                self._do_add_mechanisms(_mode.mode_id, _node_id)

        # If we're not running a test and there were requirements returned,
        # let anyone who cares know the Requirements have been selected.
        if not self._test and self.tree.size() > 1:
            pub.sendMessage('retrieved_pof', tree=self.tree)

        return None

    def _do_add_mechanisms(self, mode_id, parent_id):
        """
        Add the failure mechanisms to Physics of Failure tree for Mode ID.

        :param int mechanism_id: the Mechanism ID to add the operating loads
                                 to.
        :param str parent_id: the Node ID to add the operating loads to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _mechanisms = self.dtm_mechanism.do_select_all(
            parent_id=mode_id, pof=True).nodes
        for _key in _mechanisms:
            _mechanism = _mechanisms[_key].data
            if _mechanism is not None and _mechanism.pof_include:
                _node_id = '{0:s}.{1:d}'.format(parent_id,
                                                _mechanism.mechanism_id)
                self.tree.create_node(
                    tag=_mechanism.description,
                    identifier=_node_id,
                    parent=parent_id,
                    data=_mechanism)

                self._do_add_oploads(_mechanism.mechanism_id, _node_id)

        return self.tree

    def _do_add_oploads(self, mechanism_id, parent_id):
        """
        Add the operating loads to Physics of Failure tree for Mechanism ID.

        :param int mechanism_id: the Mechanism ID to add the operating loads
                                 to.
        :param str parent_id: the Node ID to add the operating loads to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _oploads = self.dtm_opload.do_select_all(parent_id=mechanism_id).nodes
        for _key in _oploads:
            _opload = _oploads[_key].data
            if _opload is not None:
                _node_id = '{0:s}.{1:d}'.format(parent_id, _opload.load_id)
                self.tree.create_node(
                    tag=_opload.description,
                    identifier=_node_id,
                    parent=parent_id,
                    data=_opload)

                self._do_add_opstress(_opload.load_id, _node_id)
                self._do_add_test_methods(_opload.load_id, _node_id)

        return _return

    def _do_add_opstress(self, load_id, parent_id):
        """
        Add the operating stresses to the PhysicsOfFailure tree for Load ID.

        :param int load_id: the Load ID to add the operating stresses to.
        :param str parent_id: the Node ID to add the operating stresses to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _opstresses = self.dtm_opstress.do_select_all(parent_id=load_id).nodes

        for _key in _opstresses:
            _opstress = _opstresses[_key].data
            if _opstress is not None:
                _node_id = '{0:s}.{1:d}s'.format(parent_id,
                                                 _opstress.stress_id)
                self.tree.create_node(
                    tag=_opstress.description,
                    identifier=_node_id,
                    parent=parent_id,
                    data=_opstress)

        return _return

    def _do_add_test_methods(self, load_id, parent_id):
        """
        Add the test methods to the PhysicsOfFailure tree for Stress ID.

        :param int load_id: the Operating Load ID to add the test method to.
        :param str parent_id: the Node ID to add the test method to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _methods = self.dtm_testmethod.do_select_all(parent_id=load_id).nodes
        for _key in _methods:
            _method = _methods[_key].data
            if _method is not None:
                _node_id = '{0:s}.{1:d}t'.format(parent_id, _method.test_id)
                self.tree.create_node(
                    tag=_method.description,
                    identifier=_node_id,
                    parent=parent_id,
                    data=_method)

        return _return

    def do_insert(self, **kwargs):
        """
        Add an entity to the PhysicsOfFailure and RAMSTK Program database..

        :param int entity_id: the RAMSTK Program database Mechanism ID, OpLoad ID,
                              or OpStress ID to add the entity to.
        :param str parent_id: the Node ID of the parent node in the treelib
                              Tree().
        :param str level: the type of entity to add to the PhysicsOfFailure.  Levels are:

                          * opload
                          * opstress
                          * testmethod

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Adding an item to the PhysicsOfFailure.'
        _entity = None
        _tag = 'Tag'
        _node_id = -1

        _entity_id = kwargs['entity_id']  # Parent ID in database.
        _parent_id = str(kwargs['parent_id'])  # Parent Node ID in Tree.
        _level = kwargs['level']

        if _level == 'opload':
            _error_code, _msg = self.dtm_opload.do_insert(
                mechanism_id=_entity_id)
            _entity = self.dtm_opload.do_select(self.dtm_opload.last_id)
            _tag = 'OpLoad'
            _node_id = '{0:s}.{1:d}'.format(_parent_id,
                                            self.dtm_opload.last_id)
        elif _level == 'opstress':
            _error_code, _msg = self.dtm_opstress.do_insert(load_id=_entity_id)
            _entity = self.dtm_opstress.do_select(self.dtm_opstress.last_id)
            _tag = 'OpStress'
            _node_id = '{0:s}.{1:d}s'.format(_parent_id,
                                             self.dtm_opstress.last_id)
        elif _level == 'testmethod':
            _error_code, _msg = self.dtm_testmethod.do_insert(
                load_id=_entity_id)
            _entity = self.dtm_testmethod.do_select(
                self.dtm_testmethod.last_id)
            _tag = 'TestMethod'
            _node_id = '{0:s}.{1:d}t'.format(_parent_id,
                                             self.dtm_testmethod.last_id)
        else:
            _error_code = 2005
            _msg = ('RAMSTK ERROR: Attempted to add an item to the Physics of '
                    'Failure with an undefined indenture level.  Level {0:s} '
                    'was requested.  Must be one of opload, opstress, or '
                    'testmethod.').format(_level)

        try:
            self.tree.create_node(
                _tag, _node_id, parent=_parent_id, data=_entity)
        except tree.NodeIDAbsentError:
            _error_code = 2005
            _msg = 'RAMSTK ERROR: Attempted to add an item under non-existent ' \
                   'Node ID: {0:s}.'.format(str(_parent_id))

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove record from the RAMSTKOpLoad, RAMSTKOpStress, or RAMSTKTestMethod table.

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
                          'Physics of Failure.'.format(node_id)

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
            _msg = 'RAMSTK ERROR: Attempted to save non-existent entity with ' \
                   'Node ID {0:s}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKControl table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RAMSTK ERROR: One or more line items in the damage "
                        "modeling worksheet did not update.")

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all line items in the damage "
                    "modeling worksheet.")

        return _error_code, _msg
