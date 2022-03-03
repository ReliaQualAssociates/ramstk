# -*- coding: utf-8 -*-
#
#       ramstk.models.dbviews.baseview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Metaclass for the database view models."""

# Standard Library Imports
from typing import Callable, Dict, List, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase


class RAMSTKBaseView:
    """Metaclass for all RAMSTK View models.

    :cvar _root: the Node ID number for the treelib.Tree.
    :cvar _tag: the name of the RAMSTK work flow module.  This is the same for all
        classes associated with the work flow module.

    :ivar _dic_load_functions: a dict of functions to call for loading a row of data
        in the view's RAMSTKTreeView.
    :ivar _dic_trees: a dict of treelib.Tree, one for each database table the view is
        comprised from.
    :ivar _lst_modules: the list of RAMSTK work flow modules that comprise the view.
    :ivar _revision_id: the ID of the Revision the view is associated with.
    :ivar dao: the instanace of the RAMSTK Program database model.
    :ivar tree: the view's treelib.Tree.  This is a conblomerate of the trees in
        _dic_trees.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _root: int = 0
    _tag: str = ""

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
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
            self._dic_load_functions[self._lst_modules[0]]()

            pub.sendMessage(
                f"succeed_retrieve_{self._tag}",
                tree=self.tree,
            )
