# -*- coding: utf-8 -*-
#
#       ramstk.models.hardware.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package View Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import milhdbk217f
from ramstk.models import RAMSTKBaseView


class RAMSTKHardwareBoMView(RAMSTKBaseView):
    """Contain the attributes and methods of the Hardware BoM view.

    This class manages the hardware BoM data from the RAMSTKHardware,
    RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKMilHdbkF, RAMSTKNSWC, and
    RAMSTKReliability table models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "hardware_bom"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Hardware BoM view model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_load_functions = {
            "hardware": self._do_load_hardware,
            "design_electric": self._do_load_design_electric,
            "design_mechanic": self._do_load_design_mechanic,
            "milhdbk217f": self._do_load_milhdbk217f,
            "nswc": self._do_load_nswc,
            "reliability": self._do_load_reliability,
        }
        self._dic_trees = {
            "hardware": Tree(),
            "design_electric": Tree(),
            "design_mechanic": Tree(),
            "milhdbk217f": Tree(),
            "nswc": Tree(),
            "reliability": Tree(),
        }

        # Initialize private list attributes.
        self._lst_modules = [
            "hardware",
            "design_electric",
            "design_mechanic",
            "milhdbk217f",
            "nswc",
            "reliability",
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_insert, "succeed_insert_hardware")
        pub.subscribe(super().on_insert, "succeed_insert_design_electric")
        pub.subscribe(super().on_insert, "succeed_insert_design_mechanic")
        pub.subscribe(super().on_insert, "succeed_insert_milhdbk217f")
        pub.subscribe(super().on_insert, "succeed_insert_nswc")
        pub.subscribe(super().on_insert, "succeed_insert_reliability")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_hardwares")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_design_electrics")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_design_mechanics")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_milhdbk217fs")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_nswcs")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_reliabilitys")
        pub.subscribe(super().do_set_tree, "succeed_delete_hardware")
        pub.subscribe(super().do_set_tree, "succeed_delete_design_electric")
        pub.subscribe(super().do_set_tree, "succeed_delete_design_mechanic")
        pub.subscribe(super().do_set_tree, "succeed_delete_milhdbk217f")
        pub.subscribe(super().do_set_tree, "succeed_delete_nswc")
        pub.subscribe(super().do_set_tree, "succeed_delete_reliability")

    def _do_load_hardware(self) -> None:
        """Load the hardware data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["hardware"].all_nodes()[1:]:
            _hardware = _node.data["hardware"]

            self.tree.create_node(
                tag="hardware",
                identifier=_hardware.hardware_id,
                parent=self._root,
                data={"hardware": _hardware},
            )

            if self._dic_trees["design_electric"].depth() > 0:
                self._dic_load_functions["design_electric"]()

    def _do_load_design_electric(self) -> None:
        """Load the design electric data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["design_electric"].all_nodes()[1:]:
            _design_electric = _node.data["design_electric"]

            _par_node = self.tree.get_node(_design_electric.hardware_id)
            _par_node.data["design_electric"] = _design_electric

            if self._dic_trees["design_mechanic"].depth() > 0:
                self._dic_load_functions["design_mechanic"]()

    def _do_load_design_mechanic(self) -> None:
        """Load the design_mechanic into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["design_mechanic"].all_nodes()[1:]:
            _design_mechanic = _node.data["design_mechanic"]

            _par_node = self.tree.get_node(_design_mechanic.hardware_id)
            _par_node.data["design_mechanic"] = _design_mechanic

            if self._dic_trees["milhdbk217f"].depth() > 0:
                self._dic_load_functions["milhdbk217f"]()

    def _do_load_milhdbk217f(self) -> None:
        """Load the MIL-HDBK-217F data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["milhdbk217f"].all_nodes()[1:]:
            _milhdbk217f = _node.data["milhdbk217f"]

            _par_node = self.tree.get_node(_milhdbk217f.hardware_id)
            _par_node.data["milhdbk217f"] = _milhdbk217f

            if self._dic_trees["nswc"].depth() > 0:
                self._dic_load_functions["nswc"]()

    def _do_load_nswc(self) -> None:
        """Load the NSWC data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["nswc"].all_nodes()[1:]:
            _nswc = _node.data["nswc"]

            _par_node = self.tree.get_node(_nswc.hardware_id)
            _par_node.data["nswc"] = _nswc

            if self._dic_trees["reliability"].depth() > 0:
                self._dic_load_functions["reliability"]()

    def _do_load_reliability(self) -> None:
        """Load the reliability data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["reliability"].all_nodes()[1:]:
            _reliability = _node.data["reliability"]

            _par_node = self.tree.get_node(_reliability.hardware_id)
            _par_node.data["reliability"] = _reliability

    def _do_calculate_power_dissipation(self, node_id: int) -> float:
        """Calculate the total power dissipation of a hardware item.

        :param node_id: the record ID to calculate.
        :return: _power_dissipation; the total power dissipation.
        :rtype: float
        """
        _node = self.tree.get_node(node_id)
        _design_electric = _node.data["design_electric"]
        _hardware = _node.data["hardware"]
        _power_dissipation: float = 0.0

        if _hardware.part == 1:
            _power_dissipation = _design_electric.power_operating * _hardware.quantity
        else:
            for _node_id in _node.successors(self.tree.identifier):
                _power_dissipation += self._do_calculate_power_dissipation(_node_id)
            _power_dissipation = _power_dissipation * _hardware.quantity

        _hardware.total_power_dissipation = _power_dissipation

        return _power_dissipation

    def _do_predict_active_hazard_rate(self, node_id: int) -> float:
        """Request that the hazard rate prediction be performed.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _node = self.tree.get_node(node_id)
        _hazard_rate_active: float = 0

        if _node.data["hardware"].part != 1:
            _hazard_rate_active = _node.data["reliability"].hazard_rate_active
        elif _node.data["reliability"].hazard_rate_method_id in [1, 2]:
            _attributes = {
                **_node.data["hardware"].get_attributes(),
                **_node.data["design_mechanic"].get_attributes(),
                **_node.data["design_electric"].get_attributes(),
                **_node.data["mil_hdbk_217f"].get_attributes(),
                **_node.data["nswc"].get_attributes(),
                **_node.data["reliability"].get_attributes(),
            }

            try:
                _hazard_rate_active = milhdbk217f.do_predict_active_hazard_rate(
                    **_attributes
                )
            except KeyError:
                _hazard_rate_active = 0.0

        return _hazard_rate_active
