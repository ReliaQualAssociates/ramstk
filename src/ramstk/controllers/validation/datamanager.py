# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Model."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKProgramStatus, RAMSTKValidation


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Validation data manager.

    This class manages the validation data from the RAMSTKValidation and
    RAMSKTProgramStatus data models.
    """

    _tag: str = 'validation'

    def __init__(self, **kwargs) -> None:
        """Initialize a Validation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.
        self.last_id = [0, 0]

        # Initialize public scalar attributes.
        self.status_tree = Tree()
        self.status_tree.create_node(tag='program_status',
                                     identifier=self._root)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_set_tree, 'succeed_calculate_all_validation')
        pub.subscribe(self._do_delete_validation, 'request_delete_validation')
        pub.subscribe(self.do_insert_validation, 'request_insert_validation')
        pub.subscribe(self.do_update, 'request_update_validation')
        pub.subscribe(self.do_update_all, 'request_update_all_validation')
        pub.subscribe(self.do_get_attributes,
                      'request_get_validation_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_validation_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_validation_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_validation_attributes')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_validation_attributes')
        pub.subscribe(self._do_update_program_status,
                      'succeed_calculate_tasks')

    def _do_delete_validation(self, node_id: int) -> None:
        """
        Remove a Validation task.

        :param int node_id: the node (validation) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        :raises: NodeIDAbsentError if the record is deleted from the
            database but there is no corresponding node in the tree.  This
            condition shouldn't happen, so it should be dealt with using the
            logger and a user dialog.
        """
        _error_msg = ("Attempted to delete non-existent validation ID "
                      "{0:s}.").format(str(node_id))

        try:
            super().do_delete(node_id, 'validation')

            self.tree.remove_node(node_id)
            self.last_id[0] = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_validation',
                            node_id=node_id,
                            tree=self.tree)
        except DataAccessError:
            pub.sendMessage('fail_delete_validation', error_message=_error_msg)

    # pylint: disable=arguments-differ
    def _do_insert_status(self) -> RAMSTKProgramStatus:
        """
        Add a new program status record.

        :return: _status; the newly inserted RAMSTKProgramStatus record.
        :rtype: :class:`ramstk.models.programdb.RAMSTKProgramStatus`
        """
        _status = RAMSTKProgramStatus()
        _status.revision_id = self._revision_id
        _status.status_id = self.last_id[1]

        self.dao.do_insert(_status)

        self.last_id[1] = _status.status_id

        _data_package = {'status': _status}
        self.status_tree.create_node(tag=_status.status_id,
                                     identifier=_status.date_status,
                                     parent=self._root,
                                     data=_data_package)

        return _status

    def _do_select_all_status_tree(self):
        """
        Retrieve all the status updates from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.status_tree.children(self.status_tree.root):
            self.status_tree.remove_node(_node.identifier)

        for _status in self.dao.do_select_all(
                RAMSTKProgramStatus,
                key=RAMSTKProgramStatus.revision_id,
                value=self._revision_id):

            _data_package = {'status': _status}

            self.status_tree.create_node(tag=_status.status_id,
                                         identifier=_status.date_status,
                                         parent=self._root,
                                         data=_data_package)

    def _do_update_program_status(self, cost_remaining, time_remaining):
        """
        Update the remaining cost and time of the selected program.

        .. note:: This method will always update the status for the current
            day.  If no status record exists for the current day, it will
            create one.

        :param float cost_remaining: the calculated remaining cost of the
            program.
        :param float time_remaining: the calculate remaining time to completion
            of the program.
        :return: None
        :rtype: None
        """
        try:
            _status = self.status_tree.get_node(date.today()).data['status']
        except AttributeError:
            _status = self._do_insert_status()

        try:
            _status.cost_remaining = cost_remaining
            _status.time_remaining = time_remaining

            self.dao.do_update(_status)

            pub.sendMessage('succeed_update_program_status',
                            node_id=_status.date_status)
        except DataAccessError:
            _error_msg = "Failed to update program status."
            pub.sendMessage('fail_update_program_status', error_msg=_error_msg)

    def do_get_all_attributes(self, node_id):
        """
        Retrieve all RAMSTK data tables' attributes for the validation item.

        This is a helper method to be able to retrieve all the validation
        item's attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (validation) ID of the validation item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes = {}
        for _table in ['validation']:
            _attributes.update(
                self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_validation_attributes',
                        attributes=_attributes)

    def do_get_tree(self):
        """
        Retrieve the validation treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_validation_tree', dmtree=self.tree)

    # pylint: disable=arguments-differ
    def do_insert_validation(self) -> None:
        """
        Add a new validation task.

        :return: None
        :rtype: None
        """
        try:
            _validation = RAMSTKValidation()
            _validation.revision_id = self._revision_id
            _validation.validation_id = self.last_id[0] + 1
            _validation.name = "New Validation Task"

            self.dao.do_insert(_validation)

            self.last_id[0] = _validation.validation_id

            _data_package = {'validation': _validation}
            self.tree.create_node(tag=_validation.name,
                                  identifier=_validation.validation_id,
                                  parent=self._root,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_validation',
                            node_id=self.last_id[0],
                            tree=self.tree)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_validation", error_message=_error)

    # pylint: disable=arguments-differ
    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """
        Retrieve all the Validation BoM data from the RAMSTK Program database.

        :param dict attributes: the attributes for the selected Requirement.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _validation in self.dao.do_select_all(
                RAMSTKValidation,
                key=RAMSTKValidation.revision_id,
                value=self._revision_id,
                order=RAMSTKValidation.validation_id):

            _data_package = {'validation': _validation}

            self.tree.create_node(tag=_validation.name,
                                  identifier=_validation.validation_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id[0] = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_validations', tree=self.tree)

        self._do_select_all_status_tree()

    def do_set_all_attributes(self, attributes):
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the
            validation task.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes([attributes['validation_id']],
                                   package={_key: attributes[_key]})

    def do_set_attributes(self, node_id: List, package: Dict) -> None:
        """
        Set the attributes of the record associated with the Nonee ID.


        :param list node_id: a list of the ID's of the record in the RAMSTK
            Program database table whose attributes are to be set.  The list
            is:

                0 - Validation ID

        :param dict package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        :raises: KeyError if the revision ID or validation ID keys are missing.
        """
        [[_key, _value]] = package.items()

        _attributes = self.do_select(node_id[0],
                                     table='validation').get_attributes()
        if _key in _attributes:
            _attributes[_key] = _value
            _attributes.pop('revision_id')
            _attributes.pop('validation_id')

            self.do_select(node_id[0],
                           table='validation').set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the validation ID of the validation item to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['validation'])

            pub.sendMessage('succeed_update_validation', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_validation',
                            error_msg=('Attempted to save non-existent '
                                       'validation task with validation ID '
                                       '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_validation',
                                error_msg=('No data package found for '
                                           'validation task ID {0:s}.').format(
                                               str(node_id)))
