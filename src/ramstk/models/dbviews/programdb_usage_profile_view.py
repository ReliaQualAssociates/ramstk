# -*- coding: utf-8 -*-
#
#       ramstk.models.dbviews.programdb.usage_profile_view.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Usage Profile View Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Local Imports
from .baseview import RAMSTKBaseView


class RAMSTKUsageProfileView(RAMSTKBaseView):
    """Contain the attributes and methods of the Usage Profile view model.

    This class manages the usage profile data from the RAMSTKMissionRecord,
    RAMSTKMissionPhase, and RAMSKTEnvironment table models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "usage_profile"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a usage profile view model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_load_functions = {
            "mission": self._do_load_missions,
            "mission_phase": self._do_load_mission_phases,
            "environment": self._do_load_environments,
        }
        self._dic_trees = {
            "mission": Tree(),
            "mission_phase": Tree(),
            "environment": Tree(),
        }

        # Initialize private list attributes.
        self._lst_modules = [
            "mission",
            "mission_phase",
            "environment",
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_tree, "succeed_insert_environment")
        pub.subscribe(super().do_set_tree, "succeed_insert_mission")
        pub.subscribe(super().do_set_tree, "succeed_insert_mission_phase")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_environment")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_mission")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_mission_phase")
        pub.subscribe(super().do_set_tree, "succeed_delete_environment")
        pub.subscribe(super().do_set_tree, "succeed_delete_mission")
        pub.subscribe(super().do_set_tree, "succeed_delete_mission_phase")

    def _do_load_environments(self, mission_phase_id: int, parent_id: str) -> None:
        """Load the environments into the tree for the passed phase ID.

        :param mission_phase_id: the mission phase ID to load the environments for.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["environment"].all_nodes()[1:]:
            _environment = _node.data["environment"]
            if _environment.mission_phase_id == mission_phase_id:
                _node_id = f"{parent_id}.{_environment.environment_id}"

                self.tree.create_node(
                    tag="environment",
                    identifier=_node_id,
                    parent=parent_id,
                    data={"usage_profile": _environment},
                )

    def _do_load_missions(self) -> None:
        """Load the missions into the tree for the passed mission ID.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["mission"].all_nodes()[1:]:
            _mission = _node.data["mission"]
            _node_id = f"{_mission.mission_id}"

            self.tree.create_node(
                tag="mission",
                identifier=_node_id,
                parent=self._root,
                data={"usage_profile": _mission},
            )

            if self._dic_trees["mission_phase"].depth() > 0:
                self._dic_load_functions["mission_phase"](  # type: ignore
                    _mission.mission_id,
                )

    def _do_load_mission_phases(self, mission_id: int) -> None:
        """Load the mission phases into the tree for the passed mission ID.

        :param mission_id: the mission ID to add the new mission phase.
        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["mission_phase"].all_nodes()[1:]:
            _mission_phase = _node.data["mission_phase"]
            _node_id = f"{mission_id}.{_mission_phase.mission_phase_id}"

            if _mission_phase.mission_id == mission_id:
                self.tree.create_node(
                    tag="mission_phase",
                    identifier=_node_id,
                    parent=f"{mission_id}",
                    data={"usage_profile": _mission_phase},
                )

                if self._dic_trees["environment"].depth() > 0:
                    self._dic_load_functions["environment"](  # type: ignore
                        _mission_phase.mission_phase_id,
                        _node_id,
                    )
