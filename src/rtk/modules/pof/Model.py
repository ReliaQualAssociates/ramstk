# -*- coding: utf-8 -*-
#
#       rtk.modules.physics_of_failure.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Physics of Failure Data Model."""

from treelib import tree

# Import other RTK modules.
from rtk.modules import RTKDataModel
from rtk.modules.fmea import dtmMechanism
from rtk.dao import RTKMechanism, RTKOpLoad, RTKOpStress, RTKTestMethod


class OpLoadDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a failure OpLoad.

    An RTK Project will consist of one or more OpLoads.  The attributes of a
    OpLoad are:
    """

    _tag = 'OpLoads'

    def __init__(self, dao):
        """
        Initialize a OpLoad data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, parent_id):
        """
        Retrieve all the operating loads from the RTK Program database.

        This method retrieves all the records from the RTKOpLoad table in the
        connected RTK Program database.  It then add each to the OpLoad data
        model treelib.Tree().

        :param int parent_id: the Mechanism ID the operating loads are
                              associated with.
        :return: tree; the Tree() of RTKOpLoad data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        _oploads = _session.query(RTKOpLoad).filter(
            RTKOpLoad.mechanism_id == parent_id).all()

        for _opload in _oploads:
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _opload.get_attributes()
            _opload.set_attributes(_attributes)
            self.tree.create_node(
                _opload.description, _opload.load_id, parent=0, data=_opload)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _opload.load_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RTKOpLoad table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _opload = RTKOpLoad()
        _opload.mechanism_id = kwargs['mechanism_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _opload,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _opload.description, _opload.load_id, parent=0, data=_opload)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _opload.load_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKOpLoad table.

        :param int node_id: the ID of the RTKOpLoad record to be removed from the
                            RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'OpLoad ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the OpLoad ID of the OpLoad to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent OpLoad ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKOpLoad table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.update(_node.data.load_id)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more operating loads in the damage "
                        "modeling worksheet did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all operating loads in the damage "
                    "modeling worksheet.")

        return _error_code, _msg


class OpStressDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a failure OpStress.

    An RTK Project will consist of one or more OpStresss.  The attributes of a
    OpStress are:
    """

    _tag = 'OpStresss'

    def __init__(self, dao):
        """
        Initialize a OpStress data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, parent_id):
        """
        Retrieve all the operating stresss from the RTK Program database.

        This method retrieves all the records from the RTKOpStress table in the
        connected RTK Program database.  It then add each to the OpStress data
        model treelib.Tree().

        :param int parent_id: the Mechanism ID the operating stresss are
                              associated with.
        :return: tree; the Tree() of RTKOpStress data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        _opstresss = _session.query(RTKOpStress).filter(
            RTKOpStress.load_id == parent_id).all()

        for _opstress in _opstresss:
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
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _opstress.stress_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RTKOpStress table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _opstress = RTKOpStress()
        _opstress.load_id = kwargs['load_id']
        _error_code, _msg = RTKDataModel.insert(
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
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _opstress.stress_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKOpStress table.

        :param int node_id: the ID of the RTKOpStress record to be removed from the
                            RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'OpStress ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the OpStress ID of the OpStress to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent OpStress ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKOpStress table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.update(_node.data.stress_id)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more operating stresses in the "
                        "damage modeling worksheet did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all operating stresses in the "
                    "damage modeling worksheet.")

        return _error_code, _msg


class TestMethodDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a failure TestMethod.

    An RTK Project will consist of one or more TestMethods.  The attributes of a
    TestMethod are:
    """

    _tag = 'TestMethods'

    def __init__(self, dao):
        """
        Initialize a TestMethod data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, parent_id):
        """
        Retrieve all the operating stresss from the RTK Program database.

        This method retrieves all the records from the RTKTestMethod table in the
        connected RTK Program database.  It then add each to the TestMethod data
        model treelib.Tree().

        :param int parent_id: the Mechanism ID the operating stresss are
                              associated with.
        :return: tree; the Tree() of RTKTestMethod data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        _testmethods = _session.query(RTKTestMethod).filter(
            RTKTestMethod.load_id == parent_id).all()

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
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _testmethod.test_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RTKTestMethod table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _testmethod = RTKTestMethod()
        _testmethod.load_id = kwargs['load_id']
        _error_code, _msg = RTKDataModel.insert(
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
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _testmethod.test_id)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKTestMethod table.

        :param int node_id: the ID of the RTKTestMethod record to be removed from the
                            RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'TestMethod ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the TestMethod ID of the TestMethod to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent TestMethod ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKTestMethod table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.update(_node.data.load_id)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more test methods in the damage "
                        "modeling worksheet did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all test methods in the damage "
                    "modeling worksheet.")

        return _error_code, _msg


class PhysicsOfFailureDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a PhysicsOfFailure (PoF).

    The PhysicsOfFailure data model aggregates the Mechanism, OpLoad, OpStress
    and TestMethod data models to produce an overall PoF.  A Hardware item will
    consist of one PoF.  This is a hierarchical relationship, such as:

          Mechanism 1
          |
          |_Load 1.1
          |   |
          |   |_Stress 1.1.1
          |   |   |
          |   |   |_Test 1.1.1.1
          |   |   |_Test 1.1.1.2
          |   |_Stress 1.1.2
          |       |
          |       |_Test 1.1.2.1
          |
          |_Load 1.2
              |
              |_Stress 1.2.1
              |_Stress 1.2.2
    """

    _tag = 'PhysicsOfFailure'

    def __init__(self, dao):
        """
        Initialize a PhysicsOfFailure data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._functional = False

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_mechanism = dtmMechanism(dao)
        self.dtm_opload = OpLoadDataModel(dao)
        self.dtm_opstress = OpStressDataModel(dao)
        self.dtm_testmethod = TestMethodDataModel(dao)

    def select_all(self, parent_id):
        """
        Retrieve and build the PhysicsOfFailure tree for Parent ID.

        :param str parent_id: the Mode ID to retrieve the PhysicsOfFailure
                              and build trees for.
        :return: tree; the PhysicsOfFailure treelib Tree().
        :rtype: :class:`treelib.Tree`
        """
        RTKDataModel.select_all(self)

        _mechanisms = self.dtm_mechanism.do_select_all(
            parent_id=parent_id, pof=True).nodes

        for _key in _mechanisms:
            _mechanism = _mechanisms[_key].data
            if _mechanism is not None and _mechanism.pof_include:
                _node_id = '0.{0:d}'.format(_mechanism.mechanism_id)
                self.tree.create_node(
                    tag=_mechanism.description,
                    identifier=_node_id,
                    parent=0,
                    data=_mechanism)

                self._do_add_oploads(_mechanism.mechanism_id, _node_id)

        return self.tree

    def _do_add_oploads(self, mechanism_id, parent_id):
        """
        Add the operating loadss to the PhysicsOfFailure tree for Mechanism ID.

        :param int mechanism_id: the Mechanism ID to add the operating loads
                                 to.
        :param str parent_id: the Node ID to add the operating loads to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _oploads = self.dtm_opload.select_all(mechanism_id).nodes
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

        _opstresses = self.dtm_opstress.select_all(load_id).nodes

        for _key in _opstresses:
            _opstress = _opstresses[_key].data
            if _opstress is not None:
                _node_id = '{0:s}.{1:d}s'.format(parent_id, _opstress.stress_id)
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

        _methods = self.dtm_testmethod.select_all(load_id).nodes
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

    def insert(self, **kwargs):
        """
        Add an entity to the PhysicsOfFailure and RTK Program database..

        :param int entity_id: the RTK Program database Mechanism ID, OpLoad ID,
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
        _msg = 'RTK SUCCESS: Adding an item to the PhysicsOfFailure.'
        _entity = None
        _tag = 'Tag'
        _node_id = -1

        _entity_id = kwargs['entity_id']  # Parent ID in database.
        _parent_id = str(kwargs['parent_id'])  # Parent Node ID in Tree.
        _level = kwargs['level']

        if _level == 'opload':
            _error_code, _msg = self.dtm_opload.insert(mechanism_id=_entity_id)
            _entity = self.dtm_opload.select(self.dtm_opload.last_id)
            _tag = 'OpLoad'
            _node_id = '{0:s}.{1:d}'.format(_parent_id,
                                            self.dtm_opload.last_id)
        elif _level == 'opstress':
            _error_code, _msg = self.dtm_opstress.insert(load_id=_entity_id)
            _entity = self.dtm_opstress.select(self.dtm_opstress.last_id)
            _tag = 'OpStress'
            _node_id = '{0:s}.{1:d}s'.format(_parent_id,
                                            self.dtm_opstress.last_id)
        elif _level == 'testmethod':
            _error_code, _msg = self.dtm_testmethod.insert(
                load_id=_entity_id)
            _entity = self.dtm_testmethod.select(self.dtm_testmethod.last_id)
            _tag = 'TestMethod'
            _node_id = '{0:s}.{1:d}t'.format(_parent_id,
                                            self.dtm_testmethod.last_id)
        else:
            _error_code = 2005
            _msg = ('RTK ERROR: Attempted to add an item to the Physics of '
                    'Failure with an undefined indenture level.  Level {0:s} '
                    'was requested.  Must be one of opload, opstress, or '
                    'testmethod.').format(_level)

        try:
            self.tree.create_node(
                _tag, _node_id, parent=_parent_id, data=_entity)
        except tree.NodeIDAbsentError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to add an item under non-existent ' \
                   'Node ID: {0:s}.'.format(str(_parent_id))

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove record from the RTKOpLoad, RTKOpStress, or RTKTestMethod table.

        :param int node_id: the ID of the RTKMode record to be removed from the
                            RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'entity with Node ID {0:s} from the ' \
                          'Physics of Failure.'.format(node_id)

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Mode ID of the Mode to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent entity with ' \
                   'Node ID {0:s}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKControl table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more line items in the damage "
                        "modeling worksheet did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all line items in the damage "
                    "modeling worksheet.")

        return _error_code, _msg
