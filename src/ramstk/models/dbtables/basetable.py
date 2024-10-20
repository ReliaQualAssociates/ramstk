# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.basetable.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Metaclass for the database table models."""


# Standard Library Imports
import contextlib
from datetime import date
from typing import Any, Callable, Dict, List, Tuple, Type, Union

# Third Party Imports
import treelib
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError
from ramstk.models.db import BaseDatabase
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _


def do_clear_tree(tree: treelib.Tree) -> treelib.Tree:
    """Clear all nodes from a tree except the root node.

    :param tree: the treelib.Tree to clear.
    :return: the original tree with all child nodes removed.
    :rtype: treelib.Tree
    """
    for _node in tree.children(tree.root):
        tree.remove_node(_node.identifier)

    return tree


class RAMSTKBaseTable:
    """Metaclass for all RAMSTK Table Models.

    :cvar _db_id_colname: the name of the primary key column in the database. :cvar
    _db_tablename: the name of the database table. :cvar _root: the root node in the
    Treelib.tree; nominally 0. :cvar _select_msg: the message to listen for to call the
    do_select_all() method. :cvar _tag: the name of the RAMSTK work flow module.  This
    is the same for all     classes associated with the work flow module.

    :ivar _lst_id_columns: the list of column names in the database table that
    contain an ID value.  These are generally primary and/or foreign key columns. :ivar
    _parent_id: the ID of the parent object in a hierarchical structure such as a
    hardware BoM. :ivar _record: the database record model object associated with the
    table model. :ivar _revision_id: the ID of the revision that is currently selected.
    :ivar dao: the instanace of the RAMSTK Program database model. :ivar last_id: the
    last ID number used in the database table. :ivar pkey: the name of the primary key
    column for the database table. :ivar tree: the treelib Tree()that will contain the
    structure of the RAMSTK     module being modeled.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname: str = ""
    _db_tablename: str = ""
    _root: int = 0
    _select_msg: str = "selected_revision"
    _tag: str = ""

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize an RAMSTK table model instance."""
        # Initialize attributes
        self._do_initialize_attributes()

        # Initialize the tree structure for the RAMSTK module.
        self._do_initialize_tree()

        # Subscribe to PyPubSub messages.
        self._do_subscribe_to_messages()

    def do_connect(self, dao: BaseDatabase) -> None:
        """Connect data manager to a database.

        :param dao: the BaseDatabase() instance (data access object)
            representing the connected RAMSTK Program database.
        :type dao: :class:`ramstk.db.base.BaseDatabase`
        """
        self.dao = dao

    def do_create_all_codes(self, prefix: str) -> None:
        """Create codes for all MODULE data table records.

        :param prefix: the string to use as a prefix for each code.
        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            self.do_create_code_for_node(_node, prefix)

    def do_create_code_for_node(self, node, prefix: str) -> None:
        """Create a code for a single node.

        :param node: The node from the tree structure.
        :param prefix: The prefix to use for the code.
        :return: None
        :rtype: None
        """
        # Ensure identifier and prefix are passed to the code creation method.
        self.do_create_code(node.identifier, prefix)

    def do_delete(self, node_id: int) -> None:  # sourcery skip: extract-method
        """Remove a record from the Program database and records tree.

        :param node_id: the ID of the record to delete.
        :return: None
        :rtype: None
        """
        try:
            self._do_delete_database_record(node_id)
            self._do_update_last_id()
            self._do_remove_tree_node(node_id)
            pub.sendMessage(
                f"succeed_delete_{self._tag}",
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"Attempted to delete non-existent "
                    f"{self._tag.replace('_', ' ').title()} ID {node_id}."
                ),
            )

    def do_get_attributes(self, node_id: int) -> None:
        """Retrieve the RAMSTK data table attributes for node ID.

        :param node_id: the node ID in the treelib Tree to get the attributes for.
        :return: None
        :rtype: None
        """
        try:
            pub.sendMessage(
                f"succeed_get_{self._tag}_attributes",
                attributes=self.do_select(node_id).get_attributes(),
            )
        except AttributeError:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"No attributes found for record ID {node_id} in {self._tag} table."
                ),
            )

    def do_get_tree(self) -> None:
        """Retrieve the records tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            f"succeed_get_{self._tag}_tree",
            tree=self.tree,
        )

    def do_insert(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> None:  # sourcery skip: extract-method
        """Add a new record to the RAMSTK program database and records tree.

        :param attributes: the attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        try:
            _record = self._do_create_new_record(attributes)
            self._do_insert_record_in_database(_record)
            self._do_insert_record_in_tree(_record)
            pub.sendMessage(
                f"succeed_insert_{self._tag}",
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=str(_error.msg),
            )
        except NodeIDAbsentError as _error:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=str(_error),
            )

    def do_select(self, node_id: Any) -> Any:
        """Retrieve the RAMSTK data table record for the Node ID passed.

        :param node_id: the Node ID of the data package to retrieve.
        :return: the instance of the RAMSTK<MODULE> data table that was requested or
            None if the requested Node ID does not exist. :raise: KeyError if passed the
            name of a table that isn't managed by this manager.
        """
        try:
            _entity = self.tree.get_node(node_id).data[self._tag]
        except (
            AttributeError,
            KeyError,
            NodeIDAbsentError,
            TypeError,
        ):
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"No data package for node ID {node_id} in module {self._tag}."
                ),
            )
            _entity = None

        return _entity

    def do_select_all(self, attributes: Dict[str, Union[float, int, str]]) -> None:
        """Retrieve all the records from the RAMSTK Program database.

        :param attributes: the attribute dict for the selected record.
        :return: None
        :rtype: None
        """
        self.tree = do_clear_tree(self.tree)
        _keys, _values = self._do_extract_keys_and_values(attributes)

        _records = self.dao.do_select_all(
            self._record,
            key=_keys,
            value=_values,
            order=self._db_id_colname,
        )

        for _record in _records:
            _parent_id = self._do_get_parent_id(_record)
            self._do_add_record_to_tree(_record, _parent_id)

        self._do_update_last_id()
        pub.sendMessage(
            f"succeed_retrieve_all_{self._tag}",
            tree=self.tree,
        )

    def do_set_attributes(
        self, node_id: int, package: Dict[str, Union[float, int, str]]
    ) -> None:
        """Set the attributes of the record associated with node ID.

        :param node_id: the ID of the record in the RAMSTK Program database table whose
            attributes are to be set.
        :param package: the key:value pair of the attribute to set.
        :return: None
        :rtype: None
        """
        _key, _value = self._do_extract_key_and_value(package)

        _attributes = self._do_get_record_attributes(node_id)

        if _key in _attributes:
            _attributes[_key] = _value
            self._do_update_record_attributes(node_id, _attributes)

        self.do_get_tree()

    def do_set_attributes_all(
        self, attributes: Dict[str, Union[float, int, str]]
    ) -> None:
        """Set all the attributes of the record associated with the Module ID.

        :param attributes: the aggregate attribute dict for the allocation item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(
                node_id=attributes[self.pkey],  # type: ignore
                package={_key: attributes[_key]},
            )

    def do_set_tree(self, tree: treelib.Tree) -> None:
        """Set the MODULE treelib Tree().

        This method is generally used to respond to events such as successful
        calculations of the entire system.

        :param tree: the treelib Tree() to assign to the tree attribute.
        :return: None
        :rtype: None
        """
        self.tree = tree

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node ID of the record to save.
        :return: None
        :rtype: None
        """
        if self._is_invalid_node_id(node_id):
            return

        if node_id == 0:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(f"Attempting to update the root node {node_id}."),
            )
            return

        try:
            self.dao.do_update(self.tree.get_node(node_id).data[self._tag])
            pub.sendMessage(
                f"succeed_update_{self._tag}",
                tree=self.tree,
            )
        except AttributeError:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"Attempted to save non-existent {self._tag.replace('_', ' ')} "
                    f"with {self._tag.replace('_', ' ')} ID {node_id}."
                ),
            )
        except KeyError:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"No data package found for {self._tag.replace('_', ' ')} ID "
                    f"{node_id}."
                ),
            )
        except (DataAccessError, TypeError):
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"The value for one or more attributes for "
                    f"{self._tag.replace('_', ' ')} ID {node_id} was the wrong type."
                ),
            )

        pub.sendMessage("request_set_cursor_active")

    # noinspection PyUnresolvedReferences
    # pylint: disable=no-value-for-parameter
    def do_update_all(self) -> None:
        """Update all MODULE data table records in the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            self.do_update(_node.identifier)  # type: ignore

        pub.sendMessage("request_set_cursor_active")
        pub.sendMessage(f"succeed_update_all_{self._tag}")

    def _do_add_record_to_tree(self, _record: object, _parent_id: int) -> None:
        """Add a record to the tree."""
        self.tree.create_node(
            tag=self._tag,
            identifier=_record.get_attributes()[self.pkey],
            parent=_parent_id,
            data={self._tag: _record},
        )

    def _do_create_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> object:
        """Create a new record object."""
        _record = self.do_get_new_record(attributes)
        for _id in self._lst_id_columns:
            attributes.pop(_id)
        _record.set_attributes(attributes)  # type: ignore
        return _record

    def _do_extract_key_and_value(
        self, package: Dict[str, Union[float, int, str]]
    ) -> tuple[tuple[str, float | int | str], tuple[str, float | int | str]]:
        """Extract the key and value from the package."""
        [[_key, _value]] = package.items()
        return _key, _value

    def _do_extract_keys_and_values(
        self, attributes: Dict[str, Union[float, int, str]]
    ) -> Tuple[List[str], List[Union[float, int, str]]]:
        """Extract keys and values from attributes."""
        _keys = [_key for _key in self._lst_id_columns if _key in attributes]
        _values = [
            attributes[_key]  # type: ignore
            for _key in self._lst_id_columns
            if _key in attributes
        ]
        return _keys, _values

    def _do_get_parent_id(self, _record: object) -> int:
        """Get the parent ID from a record."""
        try:
            return _record.get_attributes()["parent_id"]
        except KeyError:
            return 0

    def _do_get_record_attributes(
        self, node_id: int
    ) -> Dict[str, Union[float, int, str]]:
        """Retrieve the record attributes for a given node ID."""
        try:
            return self.do_select(node_id).get_attributes()
        except (AttributeError, KeyError):
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"No data package for node ID {node_id} in module {self._tag}."
                ),
            )
            return {}

    def _do_insert_record_in_database(self, _record: object) -> None:
        """Insert a new record into the database."""
        self.dao.do_insert(_record)
        self.last_id = self.dao.get_last_id(self._db_tablename, self._db_id_colname)

    def _do_insert_record_in_tree(self, record: object) -> None:
        """Insert a new record into the tree structure."""
        self.tree.create_node(
            tag=self._tag,
            identifier=self.last_id,
            parent=self._parent_id,
            data={self._tag: record},
        )

    def _do_delete_database_record(self, node_id: int) -> None:
        """Delete a record from the database."""
        self.dao.do_delete(self.do_select(node_id))

    def _do_initialize_attributes(self) -> None:
        """Initialize the attributes of the RAMSTK table model."""
        self._lst_id_columns: List[str] = []

        self._parent_id: int = 0
        self._record: Type[object]
        self._revision_id: int = 0

        self.dao: BaseDatabase = BaseDatabase()
        self.last_id: int = 0
        self.pkey: str = ""
        self.tree: treelib.Tree = treelib.Tree()
        self.do_get_new_record: Callable[
            [Dict[str, Union[date, float, int, str]]], object
        ]

    def _do_initialize_tree(self) -> None:
        """Initialize the tree structure for the RAMSTK module."""
        # Add the root to the Tree(). This allows multiple entries at the top
        # level, since only one root is allowed in a treelib Tree. Manipulation
        # and viewing of a RAMSTK module tree should ignore the root of the tree.
        self.tree.create_node(tag=self._tag, identifier=self._root)

    def _do_remove_tree_node(self, node_id: int) -> None:
        """Delete any child nodes and then the deleted node from the treelib Tree.

        :param node_id: the ID of the node to be removed from the tree.
        :return: None
        :rtype: None
        """
        with contextlib.suppress(NodeIDAbsentError):
            for _node in self.tree.children(node_id):
                self.dao.do_delete(self.do_select(_node.identifier))
            self.tree.remove_node(node_id)

    def _do_subscribe_to_messages(self) -> None:
        """Subscribe to PyPubSub messages."""
        do_subscribe_to_messages(
            {
                "succeed_connect_program_database": self.do_connect,
                f"request_delete_{self._tag}": self.do_delete,
                f"request_get_{self._tag}_attributes": self.do_get_attributes,
                f"request_get_{self._tag}_tree": self.do_get_tree,
                f"request_insert_{self._tag}": self.do_insert,
                self._select_msg: self.do_select_all,
                f"request_set_{self._tag}_attributes": self.do_set_attributes,
                f"mvw_editing_{self._tag}": self.do_set_attributes,
                f"wvw_editing_{self._tag}": self.do_set_attributes,
                f"request_set_all_{self._tag}_attributes": self.do_set_attributes_all,
                f"succeed_calculate_{self._tag}": self.do_set_tree,
                f"request_update_{self._tag}": self.do_update,
                f"request_update_all_{self._tag}": self.do_update_all,
                "request_save_project": self.do_update_all,
            }
        )

    def _do_update_last_id(self) -> None:
        """Update the last ID."""
        self.last_id = self.dao.get_last_id(self._db_tablename, self._db_id_colname)

    def _do_update_record_attributes(
        self, node_id: int, attributes: Dict[str, Union[float, int, str]]
    ) -> None:
        """Update the record attributes and remove ID columns."""
        for _field in self._lst_id_columns:
            with contextlib.suppress(KeyError):
                attributes.pop(_field)

        self.do_select(node_id).set_attributes(attributes)

    def _is_invalid_node_id(self, node_id: int) -> bool:
        """Check if the node ID is invalid (i.e., it's the root node)."""
        if node_id == 0:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(f"Attempting to update the root node {node_id}."),
            )
            return True
        return False
