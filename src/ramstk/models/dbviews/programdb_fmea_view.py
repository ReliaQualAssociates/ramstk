# -*- coding: utf-8 -*-
#
#       ramstk.models.dbviews.programdb_fmea_view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Mode and Effects Analysis (FMEA) View Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Local Imports
from .baseview import RAMSTKBaseView


class RAMSTKFMEAView(RAMSTKBaseView):
    """Contain the attributes and methods of the FMEA view model.

    This class manages the usage profile data from the RAMSTKMode,
    RAMSTKMechanism, RAMSTKCause, RAMSTKControl, and RAMSKTAction table models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _root = 0
    _tag = "fmeca"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a FMEA view model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_load_functions = {
            "mode": self._do_load_modes,
            "mechanism": self._do_load_mechanisms,
            "cause": self._do_load_causes,
            "control": self._do_load_controls,
            "action": self._do_load_actions,
        }
        self._dic_trees = {
            "mode": Tree(),
            "mechanism": Tree(),
            "cause": Tree(),
            "control": Tree(),
            "action": Tree(),
        }

        # Initialize private list attributes.
        self._lst_modules = [
            "mode",
            "mechanism",
            "cause",
            "control",
            "action",
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_tree, "succeed_insert_mode")
        pub.subscribe(super().do_set_tree, "succeed_insert_mechanism")
        pub.subscribe(super().do_set_tree, "succeed_insert_cause")
        pub.subscribe(super().do_set_tree, "succeed_insert_control")
        pub.subscribe(super().do_set_tree, "succeed_insert_action")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_mode")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_mechanism")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_cause")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_control")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_action")
        pub.subscribe(super().do_set_tree, "succeed_delete_mode")
        pub.subscribe(super().do_set_tree, "succeed_delete_mechanism")
        pub.subscribe(super().do_set_tree, "succeed_delete_cause")
        pub.subscribe(super().do_set_tree, "succeed_delete_control")
        pub.subscribe(super().do_set_tree, "succeed_delete_action")

    def _do_load_modes(self) -> None:
        """Load the failure modes into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["mode"].all_nodes()[1:]:
            _mode = _node.data["mode"]
            _node_id = f"{_mode.mode_id}"

            self.tree.create_node(
                tag="mode",
                identifier=_node_id,
                parent=self._root,
                data={self._tag: _mode},
            )

            if self._dic_trees["mechanism"].depth() > 0:
                self._dic_load_functions["mechanism"](
                    _mode.mode_id,
                )

    def _do_load_mechanisms(self, mode_id: int) -> None:
        """Load the failure mechanisms into the tree.

        :param mode_id: the ID of the parent failure mode.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["mechanism"].all_nodes()[1:]:
            _mechanism = _node.data["mechanism"]
            _node_id = f"{mode_id}.{_mechanism.mechanism_id}"

            if _mechanism.mode_id == mode_id:
                self.tree.create_node(
                    tag="mechanism",
                    identifier=_node_id,
                    parent=f"{mode_id}",
                    data={self._tag: _mechanism},
                )

                if self._dic_trees["cause"].depth() > 0:
                    self._dic_load_functions["cause"](
                        _mechanism.mechanism_id,
                        _node_id,
                    )

    def _do_load_causes(self, mechanism_id: int, parent_id: str) -> None:
        """Load the failure causes into the tree for the passed mechanism ID.

        :param mechanism_id: the failure mechanism ID to add the new operating load.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["cause"].all_nodes()[1:]:
            _cause = _node.data["cause"]

            if _cause.mechanism_id == mechanism_id:
                self.tree.create_node(
                    tag="cause",
                    identifier=f"{parent_id}.{_cause.cause_id}",
                    parent=parent_id,
                    data={self._tag: _cause},
                )

                if self._dic_trees["control"].depth() > 0:
                    self._dic_load_functions["control"](
                        _cause.cause_id,
                        f"{parent_id}.{_cause.cause_id}",
                    )

                if self._dic_trees["action"].depth() > 0:
                    self._dic_load_functions["action"](
                        _cause.cause_id,
                        f"{parent_id}.{_cause.cause_id}",
                    )

    def _do_load_controls(self, cause_id: int, parent_id: str) -> None:
        """Load the FNEA controls into the tree.

        :param cause_id: the ID of the parent failure cause.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["control"].all_nodes()[1:]:
            _control = _node.data["control"]

            if _control.cause_id == cause_id:
                self.tree.create_node(
                    tag="control",
                    identifier=f"{parent_id}.{_control.control_id}c",
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
        for _node in self._dic_trees["action"].all_nodes()[1:]:
            _action = _node.data["action"]

            if _action.cause_id == cause_id:
                self.tree.create_node(
                    tag="action",
                    identifier=f"{parent_id}.{_action.action_id}a",
                    parent=parent_id,
                    data={self._tag: _action},
                )
