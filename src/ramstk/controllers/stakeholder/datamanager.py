# -*- coding: utf-8 -*-
#
#       ramstk.controllers.stakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Model."""

# Third Party Imports
from pubsub import pub
from treelib import Tree
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKStakeholder


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Stakeholder data manager.

    This class manages the stakeholder data from the RAMSTKStakeholder and
    RAMSTKStakeholder data models.
    """

    _tag = 'stakeholder'
    _root = 0

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize a Stakeholder data manager instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataManager.__init__(self, dao, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'request_retrieve_stakeholders')
        pub.subscribe(self._do_delete_stakeholder,
                      'request_delete_stakeholder')
        pub.subscribe(self.do_insert_stakeholder, 'request_insert_stakeholder')
        pub.subscribe(self.do_update_stakeholder, 'request_update_stakeholder')
        pub.subscribe(self.do_update_all, 'request_update_all_stakeholders')
        pub.subscribe(self.do_get_attributes,
                      'request_get_stakeholder_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_stakeholder_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_stakeholder_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_stakeholder_attributes')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_stakeholder_attributes')

    def _do_delete_stakeholder(self, node_id):
        """
        Remove a stakeholder.

        :param int node_id: the node (stakeholder) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        (_error_code,
         _error_msg) = RAMSTKDataManager.do_delete(self, node_id,
                                                   'stakeholder')

        # pylint: disable=attribute-defined-outside-init
        # self.last_id is defined in RAMSTKDataManager.__init__
        if _error_code == 0:
            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_stakeholder', node_id=node_id)
        else:
            _error_msg = ("Attempted to delete non-existent stakeholder ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_stakeholder', error_msg=_error_msg)

    def do_get_all_attributes(self, node_id):
        """
        Retrieve all RAMSTK data tables' attributes for the stakeholder.

        This is a helper method to be able to retrieve all the stakeholder's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (stakeholder) ID of the stakeholder item
            to get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes = {}
        for _table in ['stakeholder']:
            _attributes.update(
                self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_stakeholder_attributes',
                        attributes=_attributes)

    def do_get_attributes(self, node_id, table):
        """
        Retrieve the RAMSTK data table attributes for the stakeholder.

        :param int node_id: the node (stakeholder) ID of the stakeholder to get
            the attributes for.
        :param str table: the RAMSTK data table to retrieve the attributes
            from.
        :return: None
        :rtype: None
        """
        if table in ['stakeholders', 'usage_profile']:
            _attributes = self.do_select(node_id, table=table)
        else:
            _attributes = self.do_select(node_id, table=table).get_attributes()

        pub.sendMessage('succeed_get_{0:s}_attributes'.format(table),
                        attributes=_attributes)

    def do_get_tree(self):
        """
        Retrieve the stakeholder treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_stakeholder_tree', dmtree=self.tree)

    def do_insert_stakeholder(self, parent_id=None):  # pylint: disable=arguments-differ
        """
        Add a new stakeholder.

        :param int parent_id: the parent (stakeholder) ID the new stakeholder
            will be a child (derived) of.
        :return: None
        :rtype: None
        """
        _tree = Tree()
        if parent_id is None:
            parent_id = self._root

        try:
            _stakeholder = RAMSTKStakeholder(
                description=b'New Stakeholder Input')
            _error_code, _msg = self.dao.db_add([_stakeholder])
            if _error_code == 0:
                self.last_id = _stakeholder.stakeholder_id
                self.tree.create_node(tag=_stakeholder.description,
                                      identifier=self.last_id,
                                      parent=parent_id,
                                      data={'stakeholder': _stakeholder})
                pub.sendMessage('succeed_insert_stakeholder',
                                node_id=self.last_id)
            else:
                raise DataAccessError(_msg)
        except NodeIDAbsentError:
            pub.sendMessage("fail_insert_stakeholder",
                            error_msg=("Attempting to add child stakeholder "
                                       "to non-existent stakeholder "
                                       "{0:d}.").format(parent_id))
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_stakeholder",
                            error_msg=("Failed to insert stakeholder into "
                                       "program dabase."))

    def do_select_all(self, revision_id):  # pylint: disable=arguments-differ
        """
        Retrieve all the Stakeholder data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Stakeholders for.
        :return: None
        :rtype: None
        """
        self._revision_id = revision_id

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _stakeholder in self.dao.session.query(RAMSTKStakeholder).filter(
                RAMSTKStakeholder.revision_id == self._revision_id).all():
            _data_package = {'stakeholder': _stakeholder}

            self.tree.create_node(tag=_stakeholder.description,
                                  identifier=_stakeholder.stakeholder_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_stakeholders', tree=self.tree)

    def do_set_all_attributes(self, attributes):
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the
            stakeholder.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(attributes['stakeholder_id'], _key,
                                   attributes[_key])

    def do_set_attributes(self, node_id, key, value):
        """
        Set the attributes of the record associated with the node ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :return: None
        :rtype: None
        """
        for _table in ['stakeholder']:
            _attributes = self.do_select(node_id,
                                         table=_table).get_attributes()
            if key in _attributes:
                _attributes[key] = value

                try:
                    _attributes.pop('revision_id')
                    _attributes.pop('stakeholder_id')
                except KeyError:
                    pass

                self.do_select(node_id,
                               table=_table).set_attributes(_attributes)

    def do_update_stakeholder(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the node (stakeholder) ID of the stakeholder to
            save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.session.add(
                self.tree.get_node(node_id).data['stakeholder'])
            _error_code, _error_msg = self.dao.db_update()

            if _error_code == 0:
                pub.sendMessage('succeed_update_stakeholder', node_id=node_id)
            else:
                pub.sendMessage('fail_update_stakeholder',
                                error_msg=_error_msg)
        except AttributeError:
            pub.sendMessage('fail_update_stakeholder',
                            error_msg=('Attempted to save non-existent '
                                       'stakeholder with stakeholder ID '
                                       '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_stakeholder',
                                error_msg=('No data package found for '
                                           'stakeholder ID {0:s}.').format(
                                               str(node_id)))
