# -*- coding: utf-8 -*-
#
#       ramstk.models.dbviews.programdb_pof_view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Physics of Failure (PoF) View Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Local Imports
from .baseview import RAMSTKBaseView


class RAMSTKPoFView(RAMSTKBaseView):
    """Contain the attributes and methods of the Physics of Failure (PoF) view model.

    This class manages the usage profile data from the RAMSTKMechanism,
    RAMSTKOpLoad, RAMSTKOpStress, and RAMSKTTestMethod table models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "pof"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a PoF view model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_load_functions = {
            "mechanism": self._do_load_mechanisms,
            "opload": self._do_load_oploads,
            "opstress": self._do_load_opstress,
            "test_method": self._do_load_test_method,
        }
        self._dic_trees = {
            "mechanism": Tree(),
            "opload": Tree(),
            "opstress": Tree(),
            "test_method": Tree(),
        }

        # Initialize private list attributes.
        self._lst_modules = [
            "mechanism",
            "opload",
            "opstress",
            "test_method",
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_tree, "succeed_insert_mechanism")
        pub.subscribe(super().do_set_tree, "succeed_insert_opload")
        pub.subscribe(super().do_set_tree, "succeed_insert_opstress")
        pub.subscribe(super().do_set_tree, "succeed_insert_test_method")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_mechanism")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_opload")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_opstress")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_test_method")
        pub.subscribe(super().do_set_tree, "succeed_delete_mechanism")
        pub.subscribe(super().do_set_tree, "succeed_delete_opload")
        pub.subscribe(super().do_set_tree, "succeed_delete_opstress")
        pub.subscribe(super().do_set_tree, "succeed_delete_test_method")

    def _do_load_mechanisms(self) -> None:
        """Load the mechanisms into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["mechanism"].all_nodes()[1:]:
            _mechanism = _node.data["mechanism"]

            self.tree.create_node(
                tag="mechanism",
                identifier=f"{_mechanism.mechanism_id}",
                parent=self._root,
                data={self._tag: _mechanism},
            )

            if self._dic_trees["opload"].depth() > 0:
                self._dic_load_functions["opload"](  # type: ignore
                    _mechanism.mechanism_id,
                )

    def _do_load_oploads(self, mechanism_id: int) -> None:
        """Load the operating loads into the tree for the passed mechanism ID.

        :param mechanism_id: the failure mechanism ID to add the new operating load.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["opload"].all_nodes()[1:]:
            _opload = _node.data["opload"]

            if _opload.mechanism_id == mechanism_id:
                self.tree.create_node(
                    tag="opload",
                    identifier=f"{mechanism_id}.{_opload.opload_id}",
                    parent=f"{mechanism_id}",
                    data={self._tag: _opload},
                )

                if self._dic_trees["opstress"].depth() > 0:
                    self._dic_load_functions["opstress"](  # type: ignore
                        _opload.opload_id,
                        f"{mechanism_id}.{_opload.opload_id}",
                    )

                if self._dic_trees["test_method"].depth() > 0:
                    self._dic_load_functions["test_method"](  # type: ignore
                        _opload.opload_id,
                        f"{mechanism_id}.{_opload.opload_id}",
                    )

    def _do_load_opstress(self, opload_id: int, parent_id: str) -> None:
        """Load the operating stresses into the tree for the passed load ID.

        :param opload_id: the operating load ID to load the operating stresses for.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["opstress"].all_nodes()[1:]:
            _opstress = _node.data["opstress"]

            if _opstress.opload_id == opload_id:
                self.tree.create_node(
                    tag="opstress",
                    identifier=f"{parent_id}.{_opstress.opstress_id}s",
                    parent=parent_id,
                    data={self._tag: _opstress},
                )

    def _do_load_test_method(self, opload_id: int, parent_id: str) -> None:
        """Load the operating stresses into the tree for the passed load ID.

        :param opload_id: the operating load ID to load the operating stresses for.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["test_method"].all_nodes()[1:]:
            _test_method = _node.data["test_method"]

            if _test_method.opload_id == opload_id:
                self.tree.create_node(
                    tag="test_method",
                    identifier=f"{parent_id}.{_test_method.test_method_id}t",
                    parent=parent_id,
                    data={self._tag: _test_method},
                )
