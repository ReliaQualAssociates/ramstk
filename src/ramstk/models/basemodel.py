# -*- coding: utf-8 -*-
#
#       ramstk.models.basemodel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Metaclasses for the Record, Table, and View models."""

# Standard Library Imports
from typing import Any, Callable, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.utilities import none_to_default


class RAMSTKBaseRecord:
    """Meta-class for RAMSTK Common and Program database tables."""

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


class RAMSTKBaseView:
    """The meta-class for all RAMSTK View models."""

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
