# -*- coding: utf-8 -*-
#
#       ramstk.controllers.fmea.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the FMEA data manager."""

    _tag = "fmea"
    _root = 0

    # pylint: disable=unused-argument
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a FMEA data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mode_tree: Tree = Tree()
        self._mechanism_tree: Tree = Tree()
        self._cause_tree: Tree = Tree()
        self._control_tree: Tree = Tree()
        self._action_tree: Tree = Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_mode_tree, "succeed_retrieve_modes")
        pub.subscribe(self.do_set_mechanism_tree, "succeed_retrieve_mechanisms")
        pub.subscribe(self.do_set_cause_tree, "succeed_retrieve_causes")
        pub.subscribe(self.do_set_control_tree, "succeed_retrieve_controls")
        pub.subscribe(self.do_set_action_tree, "succeed_retrieve_actions")
        pub.subscribe(self.do_set_mode_tree, "succeed_delete_mode")
        pub.subscribe(self.do_set_mechanism_tree, "succeed_delete_mechanism")
        pub.subscribe(self.do_set_cause_tree, "succeed_delete_cause")
        pub.subscribe(self.do_set_control_tree, "succeed_delete_control")
        pub.subscribe(self.do_set_action_tree, "succeed_delete_action")
        pub.subscribe(self._on_insert, "succeed_insert_mode")
        pub.subscribe(self._on_insert, "succeed_insert_mechanism")
        pub.subscribe(self._on_insert, "succeed_insert_cause")
        pub.subscribe(self._on_insert, "succeed_insert_control")
        pub.subscribe(self._on_insert, "succeed_insert_action")

    def do_set_mode_tree(self, tree: Tree) -> None:
        """Set the failure mode treelib Tree().

        :param tree: the failure mode package treelib Tree().
        :return: None
        :rtype: None
        """
        self._mode_tree = tree
        self.on_select_all()

    def do_set_mechanism_tree(self, tree: Tree) -> None:
        """Set the failure mechanism treelib Tree().

        :param tree: the failure mechanism package treelib Tree().
        :return: None
        :rtype: None
        """
        self._mechanism_tree = tree
        self.on_select_all()

    def do_set_cause_tree(self, tree: Tree) -> None:
        """Set the failure cause treelib Tree().

        :param tree: the failure cause package treelib Tree().
        :return: None
        :rtype: None
        """
        self._cause_tree = tree
        self.on_select_all()

    def do_set_control_tree(self, tree: Tree) -> None:
        """Set the FMEA control treelib Tree().

        :param tree: the FMEA control package treelib Tree().
        :return: None
        :rtype: None
        """
        self._control_tree = tree
        self.on_select_all()

    def do_set_action_tree(self, tree: Tree) -> None:
        """Set the FMEA action treelib Tree().

        :param tree: the FMEA action package treelib Tree().
        :return: None
        :rtype: None
        """
        self._action_tree = tree
        self.on_select_all()

    def on_select_all(self) -> None:
        """Build the FMEA treelib Tree().

        This method builds the hierarchical treelib Tree() from the individual
        mode, mechanism, cause, control, and action trees.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        if self._mechanism_tree.depth() > 0:
            self._do_load_modes()

            pub.sendMessage(
                "succeed_retrieve_fmea",
                tree=self.tree,
            )

    def _do_load_modes(self) -> None:
        """Load the failure modes into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._mode_tree.all_nodes()[1:]:
            _mode = _node.data["mode"]
            _node_id = "{}".format(_mode.mode_id)

            self.tree.create_node(
                tag="mode",
                identifier=_node_id,
                parent=self._root,
                data={self._tag: _mode},
            )

            if self._mechanism_tree.depth() > 0:
                self._do_load_mechanisms(_mode.mode_id)

    def _do_load_mechanisms(self, mode_id: int) -> None:
        """Load the failure mechanisms into the tree.

        :param mode_id: the ID of the parent failure mode.
        :return: None
        :rtype: None
        """
        for _node in self._mechanism_tree.all_nodes()[1:]:
            _mechanism = _node.data["mechanism"]
            _node_id = "{}.{}".format(mode_id, _mechanism.mechanism_id)

            if _mechanism.mode_id == mode_id:
                self.tree.create_node(
                    tag="mechanism",
                    identifier=_node_id,
                    parent="{}".format(mode_id),
                    data={self._tag: _mechanism},
                )

                if self._cause_tree.depth() > 0:
                    self._do_load_causes(_mechanism.mechanism_id, _node_id)

    def _do_load_causes(self, mechanism_id: int, parent_id: str) -> None:
        """Load the failure causes into the tree.

        :param mechanism_id: the ID of the parent failure mechanism.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._cause_tree.all_nodes()[1:]:
            _cause = _node.data["cause"]
            _node_id = "{}.{}".format(parent_id, _cause.cause_id)

            if _cause.mechanism_id == mechanism_id:
                self.tree.create_node(
                    tag="cause",
                    identifier=_node_id,
                    parent=parent_id,
                    data={self._tag: _cause},
                )

                if self._control_tree.depth() > 0:
                    self._do_load_controls(_cause.cause_id, _node_id)

                if self._action_tree.depth() > 0:
                    self._do_load_actions(_cause.cause_id, _node_id)

    def _do_load_controls(self, cause_id: int, parent_id: str) -> None:
        """Load the FNEA controls into the tree.

        :param cause_id: the ID of the parent failure cause.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._control_tree.all_nodes()[1:]:
            _control = _node.data["control"]
            _node_id = "{}.{}c".format(parent_id, _control.control_id)

            if _control.cause_id == cause_id:
                self.tree.create_node(
                    tag="control",
                    identifier=_node_id,
                    parent=parent_id,
                    data={self._tag: _control},
                )

    def _do_load_actions(self, cause_id: int, parent_id: str) -> None:
        """Load the FMEA actions into the tree.

        :param cause_id: the ID of the parent failure cause.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._action_tree.all_nodes()[1:]:
            _action = _node.data["action"]
            _node_id = "{}.{}a".format(parent_id, _action.action_id)

            if _action.cause_id == cause_id:
                self.tree.create_node(
                    tag="action",
                    identifier=_node_id,
                    parent=parent_id,
                    data={self._tag: _action},
                )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert(self, tree: Tree, node_id: int) -> None:
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
        _module: str = tree.get_node(0).tag

        _function = {
            "mode": self.do_set_mode_tree,
            "mechanism": self.do_set_mechanism_tree,
            "cause": self.do_set_cause_tree,
            "control": self.do_set_control_tree,
            "action": self.do_set_action_tree,
        }[_module]

        # noinspection PyArgumentList
        _function(tree)
