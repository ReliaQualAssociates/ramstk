# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Model."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKProgramStatus, RAMSTKValidation


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Validation data manager.

    This class manages the validation data from the RAMSTKValidation and
    RAMSKTProgramStatus data models.
    """

    _tag: str = 'validation'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Validation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_status: Dict[Any, float] = {}
        self._pkey = {'validation': ['revision_id', 'validation_id']}

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
        pub.subscribe(super().do_get_attributes,
                      'request_get_validation_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_validation_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_validation')
        pub.subscribe(super().do_set_tree, 'succeed_calculate_all_validation')
        pub.subscribe(super().do_update_all, 'request_update_all_validation')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_update, 'request_update_validation')
        pub.subscribe(self.do_get_tree, 'request_get_validation_tree')
        pub.subscribe(self.do_get_status_tree, 'request_get_status_tree')

        pub.subscribe(self._do_delete_validation, 'request_delete_validation')
        pub.subscribe(self._do_get_all_attributes,
                      'request_get_all_validation_attributes')
        pub.subscribe(self._do_insert_validation, 'request_insert_validation')
        pub.subscribe(self._do_set_all_attributes,
                      'request_set_all_validation_attributes')
        pub.subscribe(self._do_update_program_status,
                      'succeed_calculate_all_tasks')

    def do_get_status_tree(self) -> None:
        """Retrieve the status treelib Tree().

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_status_tree', stree=self.status_tree)

    def do_get_tree(self) -> None:
        """Retrieve the validation treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_validation_tree', tree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all Validation BoM data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Requirement.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _validation in self.dao.do_select_all(
                RAMSTKValidation,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKValidation.validation_id):

            _data_package = {'validation': _validation}

            self.tree.create_node(tag=_validation.name,
                                  identifier=_validation.validation_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id[0] = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_validations', tree=self.tree)

        self._do_select_all_status_tree()

    def do_update(self, node_id):
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the validation ID of the validation item to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['validation'])

            pub.sendMessage('succeed_update_validation', node_id=node_id)
        except AttributeError:
            pub.sendMessage(
                'fail_update_validation',
                error_message=('Attempted to save non-existent '
                               'validation task with validation ID '
                               '{0:s}.').format(str(node_id)))
        except (KeyError, TypeError):
            if node_id != 0:
                pub.sendMessage(
                    'fail_update_validation',
                    error_message=('No data package found for '
                                   'validation task ID {0:s}.').format(
                                       str(node_id)))

    def _do_delete_validation(self, node_id: int) -> None:
        """Remove a Validation task.

        :param node_id: the node (validation) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        :raises: NodeIDAbsentError if the record is deleted from the
            database but there is no corresponding node in the tree.  This
            condition shouldn't happen, so it should be dealt with using the
            logger and a user dialog.
        """
        try:
            super().do_delete(node_id, 'validation')

            self.tree.remove_node(node_id)
            self.last_id[0] = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_validation_2', node_id=node_id)
            pub.sendMessage('succeed_delete_validation',
                            node_id=node_id,
                            tree=self.tree)
        except DataAccessError:
            pub.sendMessage('fail_delete_validation',
                            error_message=("Attempted to delete non-existent "
                                           "validation ID {0:s}.").format(
                                               str(node_id)))

    def _do_get_all_attributes(self, node_id: int) -> None:
        """Retrieve all RAMSTK data tables' attributes for the validation item.

        This is a helper method to be able to retrieve all the validation
        item's attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param node_id: the node (validation) ID of the validation item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_all_validation_attributes',
                        attributes=self.do_select(
                            node_id, table='validation').get_attributes())

    # pylint: disable=arguments-differ
    def _do_insert_status(self) -> RAMSTKProgramStatus:
        """Add a new program status record.

        :return: _status; the newly inserted RAMSTKProgramStatus record.
        :rtype: :class:`ramstk.models.programdb.RAMSTKProgramStatus`
        """
        _status = RAMSTKProgramStatus()
        _status.revision_id = self._revision_id
        _status.status_id = self.last_id[1] + 1

        self.dao.do_insert(_status)

        self.last_id[1] = _status.status_id

        _data_package = {'status': _status}
        self._dic_status[_status.date_status] = _status.time_remaining
        self.status_tree.create_node(tag=_status.status_id,
                                     identifier=_status.date_status,
                                     parent=self._root,
                                     data=_data_package)

        return _status

    def _do_insert_validation(self) -> None:
        """Add a new validation task.

        :return: None
        :rtype: None
        """
        _last_id = self.dao.get_last_id('ramstk_validation', 'validation_id')
        try:
            _validation = RAMSTKValidation()
            _validation.revision_id = self._revision_id
            _validation.validation_id = _last_id + 1
            _validation.name = "New Validation Task"

            self.dao.do_insert(_validation)

            self.last_id[0] = _validation.validation_id

            _data_package = {'validation': _validation}
            self.tree.create_node(tag=_validation.name,
                                  identifier=_validation.validation_id,
                                  parent=self._root,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_validation_2',
                            node_id=self.last_id[0])
            pub.sendMessage('succeed_insert_validation',
                            node_id=self.last_id[0],
                            tree=self.tree)
        except DataAccessError as _error:
            pub.sendMessage("fail_insert_validation", error_message=_error)

    def _do_select_all_status_tree(self):
        """Retrieve all the status updates from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.status_tree.children(self.status_tree.root):
            self.status_tree.remove_node(_node.identifier)

        for _status in self.dao.do_select_all(
                RAMSTKProgramStatus,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKProgramStatus.date_status):

            _data_package = {'status': _status}
            self._dic_status[_status.date_status] = _status.time_remaining

            self.status_tree.create_node(tag=_status.status_id,
                                         identifier=_status.date_status,
                                         parent=self._root,
                                         data=_data_package)

            self.last_id[1] = max(self.last_id[1], _status.status_id)

    def _do_set_all_attributes(self, attributes):
        """Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the validation
            task.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            super().do_set_attributes([attributes['validation_id']],
                                      package={_key: attributes[_key]})

    def _do_update_program_status(self, cost_remaining, time_remaining):
        """Update the remaining cost and time of the selected program.

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

        _status.cost_remaining = cost_remaining
        _status.time_remaining = time_remaining

        self.dao.do_update(_status)

        pub.sendMessage('succeed_update_program_status',
                        attributes={'y_actual': self._dic_status})
