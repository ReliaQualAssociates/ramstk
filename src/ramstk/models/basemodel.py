# -*- coding: utf-8 -*-
#
#       ramstk.models.basemodel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Metaclasses for the Record, Table, and View models."""

# Standard Library Imports
import inspect
from typing import Any, Callable, Dict, List, Type

# Third Party Imports
import treelib
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.utilities import none_to_default


def do_clear_tree(tree: treelib.Tree) -> treelib.Tree:
    """Clear all nodes from a tree except the root node.

    :param tree: the treelib.Tree to clear.
    :return: the original tree with all child nodes removed.
    :rtype: treelib.Tree
    """
    for _node in tree.children(tree.root):
        tree.remove_node(_node.identifier)

    return tree


class RAMSTKBaseRecord:
    """Meta-class for all RAMSTK Record models."""

    def set_attributes(self, attributes):
        """Set one or more RAMSTK<Table> attributes.

        .. note:: you should pop the primary and foreign key entries from the
            attributes dict before passing it to this method.

        :param attributes: dict of key:value pairs to assign to the
            instance attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(
                self, _key, none_to_default(attributes[_key], self.__defaults__[_key])
            )


class RAMSTKBaseTable:
    """Meta-class for all RAMSTK Table Models.

    :ivar tree: the treelib Tree()that will contain the structure of the RAMSTK
        module being modeled.
    :type tree: :class:`treelib.Tree`
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
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize an RAMSTK data model instance."""
        # Initialize private dictionary attributes.
        self._fkey: Dict[str, int] = {}
        self._pkey: Dict[str, List[str]] = {}

        # Initialize private list attributes.
        self._lst_id_columns: List[str] = []

        # Initialize private scalar attributes.
        self._parent_id: int = 0
        self._record: Type[object]
        self._revision_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao: BaseDatabase = BaseDatabase()
        self.last_id: int = 0
        self.pkey: str = ""
        self.tree: treelib.Tree = treelib.Tree()
        self.do_get_new_record: Callable[[Dict[str, Any]], object]

        # Add the root to the Tree().  This is necessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RAMSTK module tree needs to
        # ignore the root of the tree.
        self.tree.create_node(tag=self._tag, identifier=self._root)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_connect, "succeed_connect_program_database")
        pub.subscribe(self.do_delete, "request_delete_{}".format(self._tag))
        pub.subscribe(
            self.do_get_attributes, "request_get_{}_attributes".format(self._tag)
        )
        pub.subscribe(self.do_get_tree, "request_get_{}_tree".format(self._tag))
        pub.subscribe(self.do_insert, "request_insert_{}".format(self._tag))
        pub.subscribe(self.do_select_all, self._select_msg)
        pub.subscribe(
            self.do_set_attributes, "request_set_{}_attributes".format(self._tag)
        )
        pub.subscribe(self.do_set_attributes, "lvw_editing_{}".format(self._tag))
        pub.subscribe(self.do_set_attributes, "mvw_editing_{}".format(self._tag))
        pub.subscribe(self.do_set_attributes, "wvw_editing_{}".format(self._tag))
        pub.subscribe(
            self.do_set_attributes_all,
            "request_set_all_{}_attributes".format(self._tag),
        )
        pub.subscribe(self.do_set_tree, "succeed_calculate_{}".format(self._tag))
        pub.subscribe(self.do_update, "request_update_{}".format(self._tag))
        pub.subscribe(self.do_update_all, "request_update_all_{}".format(self._tag))
        pub.subscribe(self.do_update_all, "request_save_project")

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
            # noinspection PyUnresolvedReferences
            self.do_create_code(_node.identifier, prefix)  # type: ignore

    def do_delete(self, node_id: int) -> None:
        """Remove a record from the Program database and records tree.

        :param node_id: the ID of the record to delete.
        :return: None
        :rtype: None
        """
        try:
            for _node in self.tree.children(node_id):
                _record = self.do_select(_node.identifier)
                self.dao.do_delete(_record)

            _record = self.do_select(node_id)
            self.dao.do_delete(_record)

            self.tree.remove_node(node_id)
            self.last_id = self.dao.get_last_id(self._db_tablename, self._db_id_colname)

            pub.sendMessage(
                "succeed_delete_{}".format(self._tag),
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _error_msg: str = "Attempted to delete non-existent {1} ID {0}.".format(
                str(node_id), self._tag.replace("_", " ").title()
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_{}".format(self._tag),
                error_message=_error_msg,
            )

    def do_get_attributes(self, node_id: int, table: str = "") -> None:
        """Retrieve the RAMSTK data table attributes for node ID.

        :param node_id: the node ID in the treelib Tree to get the
            attributes for.
        :param table: the RAMSTK data table to retrieve the attributes from.
        :return: None
        :rtype: None
        """
        try:
            pub.sendMessage(
                "succeed_get_{0}_attributes".format(self._tag),
                attributes=self.do_select(node_id).get_attributes(),
            )
        except AttributeError:
            _method_name = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = (
                "{0}: No attributes found for record ID {1} in "
                "{2} table.".format(_method_name, node_id, self._tag)
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_get_{0}_attributes".format(table),
                error_message=_error_msg,
            )

    def do_get_tree(self) -> None:
        """Retrieve the records tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_{}_tree".format(self._tag),
            tree=self.tree,
        )

    def do_insert(self, attributes: Dict[str, Any]) -> None:
        """Add a new record to the RAMSTK program database and records tree.

        :param attributes: the attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        try:
            _record = self.do_get_new_record(attributes)
            for _id in self._lst_id_columns:
                attributes.pop(_id)
            _record.set_attributes(attributes)  # type: ignore
            _identifier = self.last_id + 1

            self.dao.do_insert(_record)
            self.last_id = self.dao.get_last_id(self._db_tablename, self._db_id_colname)

            self.tree.create_node(
                tag=self._tag,
                identifier=_identifier,
                parent=self._parent_id,
                data={self._tag: _record},
            )

            pub.sendMessage(
                "succeed_insert_{}".format(self._tag),
                node_id=_identifier,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_{}".format(self._tag),
                error_message=_error.msg,
            )
        except NodeIDAbsentError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=str(_error),
            )
            pub.sendMessage(
                "fail_insert_{}".format(self._tag),
                error_message=str(_error),
            )

    def do_select(self, node_id: Any) -> Any:
        """Retrieve the RAMSTK data table record for the Node ID passed.

        :param node_id: the Node ID of the data package to retrieve.
        :return: the instance of the RAMSTK<MODULE> data table that was
            requested or None if the requested Node ID does not exist.
        :raise: KeyError if passed the name of a table that isn't managed by
            this manager.
        """
        try:
            _entity = self.tree.get_node(node_id).data[self._tag]
        except (AttributeError, KeyError, treelib.tree.NodeIDAbsentError, TypeError):
            _method_name = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{2}: No data package for node ID {0} in module {1}.".format(
                    node_id, self._tag, _method_name
                )
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            _entity = None

        return _entity

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the records from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected failure action.
        :return: None
        :rtype: None
        """
        self.tree = do_clear_tree(self.tree)

        try:
            self._revision_id = attributes["revision_id"]
        except KeyError:
            try:
                self._revision_id = attributes["site_id"]
            except KeyError:
                self._revision_id = 0

        for _record in self.dao.do_select_all(
            self._record,
            key=[
                self._lst_id_columns[0],
            ],
            value=[
                self._revision_id,
            ],
        ):
            try:
                self._parent_id = _record.get_attributes()["parent_id"]
            except KeyError:
                self._parent_id = 0

            self.tree.create_node(
                tag=self._tag,
                identifier=_record.get_attributes()[self.pkey],
                parent=self._parent_id,
                data={self._tag: _record},
            )
        self.last_id = self.dao.get_last_id(self._db_tablename, self._db_id_colname)

        pub.sendMessage(
            "succeed_retrieve_{}s".format(self._tag),
            tree=self.tree,
        )

    def do_set_attributes(self, node_id: List, package: Dict[str, Any]) -> None:
        """Set the attributes of the record associated with node ID.

        :param node_id: the ID of the record in the RAMSTK Program database
            table whose attributes are to be set.
        :param package: the key:value pair of the attribute to set.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()
        # ISSUE: Make node_id an integer argument to do_set_attributes()
        #
        # The node_id argument to RAMSTKBaseTable.do_set_attributes() is currently a
        # List type argument.  This is deprecated and all calls should replace this
        # with an integer argument.  After fixing all calls, remove the try construct
        # in do_set_attributes() that exists to handle the List and int types.
        # labels: type: refactor
        try:
            _node_id = node_id[0]
        except TypeError:
            _node_id = node_id

        try:
            _attributes = self.do_select(_node_id).get_attributes()
        except (AttributeError, KeyError):
            _method_name = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{2}: No data package for node ID {0} in module "
                "{1}.".format(_node_id, self._tag, _method_name)
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            _attributes = {}

        for _field in self._lst_id_columns:
            try:
                _attributes.pop(_field)
            except KeyError:
                pass

        if _key in _attributes:
            _attributes[_key] = _value

            self.do_select(_node_id).set_attributes(_attributes)

        # noinspection PyUnresolvedReferences
        self.do_get_tree()  # type: ignore

    def do_set_attributes_all(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the record associated with the Module ID.

        :param attributes: the aggregate attributes dict for the allocation
            item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(
                node_id=[attributes[self.pkey]],
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

    def do_update(self, node_id: int, table: str = "") -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node ID of the record to save.
        :param table: the table in the database to update.
        :return: None
        :rtype: None
        """
        _fail_topic = "fail_update_{}".format(self._tag)
        _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore

        try:
            self.dao.do_update(self.tree.get_node(node_id).data[self._tag])
            pub.sendMessage(
                "succeed_update_{}".format(self._tag),
                tree=self.tree,
            )
        except AttributeError:
            _error_msg: str = (
                "{1}: Attempted to save non-existent {2} with {2} ID {0}."
            ).format(str(node_id), _method_name, self._tag.replace("_", " "))
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                _fail_topic,
                error_message=_error_msg,
            )
        except KeyError:
            _error_msg = "{1}: No data package found for {2} ID {0}.".format(
                str(node_id), _method_name, self._tag.replace("_", " ")
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                _fail_topic,
                error_message=_error_msg,
            )
        except (DataAccessError, TypeError):
            if node_id != 0:
                _error_msg = (
                    "{1}: The value for one or more attributes for "
                    "{2} ID {0} was the wrong type."
                ).format(str(node_id), _method_name, self._tag.replace("_", " "))
            else:
                _error_msg = "{1}: Attempting to update the root node {0}.".format(
                    str(node_id), _method_name
                )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                _fail_topic,
                error_message=_error_msg,
            )

    # noinspection PyUnresolvedReferences
    # pylint: disable=no-value-for-parameter
    def do_update_all(self) -> None:
        """Update all MODULE data table records in the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            try:
                self.do_update(_node.identifier, table=self._tag[:-1])  # type: ignore
            except TypeError:
                self.do_update(_node.identifier)  # type: ignore

        pub.sendMessage("succeed_update_all")


class RAMSTKBaseView:
    """Meta-class for all RAMSTK View models."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _root = 0
    _tag = ""

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a RAMSTK view model instance."""
        # Initialize private dictionary attributes.
        self._dic_load_functions: Dict[str, Callable[..., object]] = {}
        self._dic_trees: Dict[str, treelib.Tree] = {}

        # Initialize private list attributes.
        self._lst_modules: List[str] = []

        # Initialize private scalar attributes.
        self._revision_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao: BaseDatabase = BaseDatabase()
        self.tree: treelib.Tree = treelib.Tree()

        # Add the root to the Tree().  This is necessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RAMSTK module tree needs to
        # ignore the root of the tree.
        self.tree.create_node(tag=self._tag, identifier=self._root)

        # Subscribe to PyPubSub messages.

    def do_set_tree(self, tree: treelib.Tree) -> None:
        """Assign the treelib Tree() for the constituent module.

        :param tree: the calling module's treelib Tree().
        :return: None
        :rtype: None
        """
        self._dic_trees[tree.get_node(0).tag] = tree
        self.on_select_all()

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_insert(self, tree: treelib.Tree, node_id: int) -> None:
        """Wrap _do_set_<module>_tree() on insert.

        succeed_insert_<module> messages have node_id in the broadcast data
        so this method is needed to wrap the _do_set_tree() method.

        :param tree: the treelib Tree() passed by the calling message.
        :param node_id: the node ID of the element that was inserted.
            Unused in this method but required for compatibility with the
            'succeed_insert_<module>' message data.
        :return: None
        :rtype: None
        """
        return self.do_set_tree(tree)

    def on_select_all(self) -> None:
        """Build the usage profile treelib Tree().

        This method builds the hierarchical treelib Tree() from the individual
        module trees.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        if self._dic_trees[self._lst_modules[0]].depth() > 0:
            self._dic_load_functions[self._lst_modules[0]]()  # type: ignore

            pub.sendMessage(
                "succeed_retrieve_{}".format(self._tag),
                tree=self.tree,
            )
