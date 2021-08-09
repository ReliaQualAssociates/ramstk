# -*- coding: utf-8 -*-
#
#       ramstk.models.<MODULE>.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""<MODULE> Package View Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseView


class RAMSTK<MODULE>View(RAMSTKBaseView):
    """Contain the attributes and methods of the <MODULE> view.

    This class manages the usage profile data from the RAMSTK<MODULE_1>,
    RAMSTK<MODULE_2>, RAMSKT<MODULE_3>, etc. table models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _root = 0
    _tag = "<VIEW>"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a <MODULE> view model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_load_functions = {
            "<MODULE_1>": self._do_load_<MODULE_1>s,
            "<MODULE_2>": self._do_load_<MODULE_2>s,
            "<MODULE_3>": self._do_load_<MODULE_2>s,
        }
        self._dic_trees = {
            "<MODULE_1>": Tree(),
            "<MODULE_2>": Tree(),
            "<MODULE_3>": Tree(),
        }

        # Initialize private list attributes.
        self._lst_modules = [
            "<MODULE_1>",
            "<MODULE_2>",
            "<MODULE_3>",
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_insert, "succeed_insert_<MODULE_1>")
        pub.subscribe(super().on_insert, "succeed_insert_<MODULE_2>")
        pub.subscribe(super().on_insert, "succeed_insert_<MODULE_3>")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_<MODULE_1>s")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_<MODULE_2>s")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_<MODULE_3>s")
        pub.subscribe(super().do_set_tree, "succeed_delete_<MODULE_1>")
        pub.subscribe(super().do_set_tree, "succeed_delete_<MODULE_2>")
        pub.subscribe(super().do_set_tree, "succeed_delete_<MODULE_3>")

    def _do_load_<MODULE_3>s(self, <MODULE_2>_id: int, parent_id: str) -> None:
        """Load the <MODULE_3>s into the tree for the passed <MODULE_2> ID.

        :param phase_id: the <MODULE_2> ID to load the <MODULE_3>s for.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["<MODULE_3>"].all_nodes()[1:]:
            _<MODULE_3> = _node.data["<MODULE_3>"]
            _node_id = "{}.{}".format(parent_id, _<MODULE_3>.<MODULE_3>_id)

            if _<MODULE_3>.<MODULE_2>_id == <MODULE_2>_id:
                self.tree.create_node(
                    tag="<MODULE_3>",
                    identifier=_node_id,
                    parent=parent_id,
                    data={"<VIEW>>": _<MODULE_3>},
                )
