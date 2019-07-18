# -*- coding: utf-8 -*-
#
#       ramstk.controllers.revision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Model."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.Exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFailureDefinition, RAMSTKRevision


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Revision data manager.

    This class manages the revision data from the RAMSTKRevision,
    RAMSTKFailureDefinition, RAMSTKMission, RAMSTKMissionPhase, and
    RAMSKTEnvironment data models.
    """

    _tag = 'revision'
    _root = 0

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize a Revision data manager instance.

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
        pub.subscribe(self.do_select_all, 'request_retrieve_revisions')
        pub.subscribe(self._do_delete, 'request_delete_revision')
        pub.subscribe(self.do_insert, 'request_insert_revision')
        pub.subscribe(self.do_update, 'request_update_revision')
        pub.subscribe(self.do_update_all, 'request_update_all_revisions')
        pub.subscribe(self.do_get_attributes,
                      'request_get_revision_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_revision_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_revision_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_revision_attributes')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_revision_attributes')

    def _do_delete(self, node_id):
        """
        Remove a Hardware item.

        :param int node_id: the node (revision) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        (_error_code,
         _error_msg) = RAMSTKDataManager.do_delete(self, node_id, 'revision')

        # pylint: disable=attribute-defined-outside-init
        # self.last_id is defined in RAMSTKDataManager.__init__
        if _error_code == 0:
            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_revision', node_id=node_id)
        else:
            _error_msg = ("Attempted to delete non-existent revision ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_revision', error_msg=_error_msg)

    def _do_set_failure_definition(self, node_id, key, value, definition_id):
        """
        Set the attributes of the record associated with definition ID.

        This is a helper method to set the desired failure definition attribute
        since the failure definitions are carried in a dict and we need to
        select the correct record to update.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :param int definition_id: the failure definition ID if the attribute
            being set is a failure definition attribute.
        :return: None
        :rtype: None
        """
        try:
            _attributes = self.do_select(
                node_id,
                table='failure_definitions')[definition_id].get_attributes()
            _attributes.pop('revision_id')
            _attributes.pop('definition_id')
        except KeyError:
            _attributes = {}

        if key in _attributes:
            _attributes[key] = value
            self.do_select(
                node_id,
                table='failure_definitions')[definition_id].set_attributes(
                    _attributes)

    def do_get_all_attributes(self, node_id):
        """
        Retrieve all RAMSTK data tables' attributes for the revision.

        This is a helper method to be able to retrieve all the revision's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (revision) ID of the revision item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes = {'failure_definitions': {}}
        for _table in ['revision', 'failure_definitions']:
            if _table == 'failure_definitions':
                _attributes['failure_definitions'].update(
                    self.do_select(node_id, table=_table))
            else:
                _attributes.update(
                    self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_revision_attributes',
                        attributes=_attributes)

    def do_get_attributes(self, node_id, table):
        """
        Retrieve the RAMSTK data table attributes for the revision.

        :param int node_id: the node (revision) ID of the revision to get the
            attributes for.
        :param str table: the RAMSTK data table to retrieve the attributes
            from.
        :return: None
        :rtype: None
        """
        if table == 'failure_definitions':
            _attributes = self.do_select(node_id, table=table)
        else:
            _attributes = self.do_select(node_id, table=table).get_attributes()

        pub.sendMessage('succeed_get_revision_attributes',
                        attributes=_attributes)

    def do_get_tree(self):
        """
        Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_revision_tree', tree=self.tree)

    def do_insert(self):  # pylint: disable=arguments-differ
        """
        Add a new revision.

        :return: None
        :rtype: None
        """
        try:
            _revision = RAMSTKRevision(name='New Revision')

            _error_code, _msg = self.dao.db_add([_revision])

            self.last_id = _revision.revision_id

            _data_package = {'revision': _revision, 'failure_definitions': {}}
            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_revision', node_id=self.last_id)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_revision", error_message=_error)

    def do_select_all(self):  # pylint: disable=arguments-differ
        """
        Retrieve all the Revision data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Hardware BoM for.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _revision in self.dao.session.query(RAMSTKRevision).all():

            _failure_definitions = self.dao.session.query(
                RAMSTKFailureDefinition).filter(
                    RAMSTKFailureDefinition.revision_id ==
                    _revision.revision_id).all()
            _failure_definitions = self.do_build_dict(_failure_definitions,
                                                      'definition_id')

            _data_package = {
                'revision': _revision,
                'failure_definitions': _failure_definitions
            }

            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_revisions', tree=self.tree)

    def do_set_all_attributes(self, attributes, definition_id=None):
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the revision.
        :keyword int definition_id: the failure definition ID if the attribute
            being set is a failure definition attribute.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(attributes['revision_id'], _key,
                                   attributes[_key], definition_id)

    def do_set_attributes(self, node_id, key, value, definition_id=None):
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :keyword int definition_id: the failure definition ID if the attribute
            being set is a failure definition attribute.
        :return: None
        :rtype: None
        """
        for _table in ['revision', 'failure_definitions']:
            if _table == 'failure_definitions':
                self._do_set_failure_definition(node_id, key, value,
                                                definition_id)
            else:
                _attributes = self.do_select(node_id,
                                             table=_table).get_attributes()
                if key in _attributes:
                    _attributes[key] = value

                    try:
                        _attributes.pop('revision_id')
                    except KeyError:
                        pass

                    self.do_select(node_id,
                                   table=_table).set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the node (revision) ID of the revision to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.session.add(self.tree.get_node(node_id).data['revision'])
            _error_code, _error_msg = self.dao.db_update()

            if _error_code == 0:
                pub.sendMessage('succeed_update_revision', node_id=node_id)
            else:
                pub.sendMessage('fail_update_revision', error_msg=_error_msg)
        except AttributeError:
            pub.sendMessage('fail_update_revision',
                            error_msg=('Attempted to save non-existent '
                                       'revision with revision ID '
                                       '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_revision',
                                error_msg=('No data package found for '
                                           'revision ID {0:s}.').format(
                                               str(node_id)))
