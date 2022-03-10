# -*- coding: utf-8 -*-
#
#       ramstk.models.dbviews.programdb_hardware_view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware BoM View Model."""

# Standard Library Imports
from typing import Dict, List, Union

# Third Party Imports
from pubsub import pub
from sqlalchemy.orm.exc import ObjectDeletedError
from treelib import Tree

# RAMSTK Local Imports
from .baseview import RAMSTKBaseView


class RAMSTKHardwareBoMView(RAMSTKBaseView):
    """Contain the attributes and methods of the Hardware BoM view model.

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

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
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
        self._dic_stress_limits: Dict[int, List[float]] = kwargs.get(  # type: ignore
            "stress_limits",
            {
                1: [
                    0.8,
                    0.9,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
                2: [
                    1.0,
                    1.0,
                    0.7,
                    0.9,
                    1.0,
                    1.0,
                ],
                3: [
                    1.0,
                    1.0,
                    0.5,
                    0.9,
                    1.0,
                    1.0,
                ],
                4: [
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    0.6,
                    0.9,
                ],
                5: [
                    0.6,
                    0.9,
                    1.0,
                    1.0,
                    0.5,
                    0.9,
                ],
                6: [
                    0.75,
                    0.9,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
                7: [
                    0.75,
                    0.9,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
                8: [
                    0.7,
                    0.9,
                    1.0,
                    1.0,
                    0.7,
                    0.9,
                ],
                9: [
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
                10: [
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
            },
        )
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
        self._hr_multiplier: float = kwargs.get("hr_multiplier", 1.0)  # type: ignore

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_tree, "succeed_insert_hardware")
        pub.subscribe(super().do_set_tree, "succeed_insert_design_electric")
        pub.subscribe(super().do_set_tree, "succeed_insert_design_mechanic")
        pub.subscribe(super().do_set_tree, "succeed_insert_milhdbk217f")
        pub.subscribe(super().do_set_tree, "succeed_insert_nswc")
        pub.subscribe(super().do_set_tree, "succeed_insert_reliability")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_hardware")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_design_electric")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_design_mechanic")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_milhdbk217f")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_nswc")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_reliability")
        pub.subscribe(super().do_set_tree, "succeed_delete_hardware")
        pub.subscribe(super().do_set_tree, "succeed_delete_design_electric")
        pub.subscribe(super().do_set_tree, "succeed_delete_design_mechanic")
        pub.subscribe(super().do_set_tree, "succeed_delete_milhdbk217f")
        pub.subscribe(super().do_set_tree, "succeed_delete_nswc")
        pub.subscribe(super().do_set_tree, "succeed_delete_reliability")
        pub.subscribe(self.do_calculate_hardware, "request_calculate_hardware")
        pub.subscribe(self.do_make_composite_ref_des, "request_make_comp_ref_des")

    def do_calculate_assembly_hazard_rates(self, node_id: int) -> None:
        """Calculate the hazard rates for assemblies.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)

        # There are no children for this node, or it is using one of the specified
        # hazard rate methods.  The specified methods will ignore the hazard rates of
        # any children.
        if _record.is_leaf() or _record.data["reliability"].hazard_rate_type_id != 1:
            _attributes = {
                **_record.data["hardware"].get_attributes(),
                **_record.data["reliability"].get_attributes(),
            }

            _record.data["reliability"].do_calculate_hazard_rate_active(
                self._hr_multiplier,
                _attributes,
                time=_record.data["hardware"].mission_time,
            )
        else:
            _hazard_rate_active: float = 0.0
            _hazard_rate_dormant: float = 0.0

            for _node in self.tree.children(node_id):
                self.do_calculate_hazard_rates(_node.identifier)
                _hazard_rate_active += _node.data["reliability"].hazard_rate_active
                _hazard_rate_dormant += _node.data["reliability"].hazard_rate_dormant

            _hazard_rate_active = (
                (_hazard_rate_active + _record.data["reliability"].add_adj_factor)
                * _record.data["reliability"].mult_adj_factor
                * (_record.data["hardware"].duty_cycle / 100.0)
                * _record.data["hardware"].quantity
            )

            _record.data["reliability"].hazard_rate_active = _hazard_rate_active
            _record.data["reliability"].hazard_rate_dormant = _hazard_rate_dormant

    def do_calculate_cost(self, node_id: int) -> None:
        """Calculate the cost related metrics.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data["hardware"]
        _total_cost: float = 0.0

        if _record.part == 1:
            _record.do_calculate_total_cost()
        else:
            for _node in self.tree.children(node_id):
                self.do_calculate_cost(_node.identifier)
                _total_cost += _node.data["hardware"].total_cost

            _total_cost *= _record.quantity
            _record.set_attributes({"cost": _total_cost})
            _record.set_attributes({"total_cost": _total_cost})

    def do_calculate_hardware(self, node_id: int) -> None:
        """Calculate all metrics for the hardware associated with node ID.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        self.do_calculate_cost(node_id)
        self.do_calculate_part_count(node_id)
        self.do_calculate_power_dissipation(node_id)
        self.do_calculate_hazard_rates(node_id)

        for _table in ["design_electric", "milhdbk217f", "reliability"]:
            pub.sendMessage(
                f"request_get_{_table}_attributes",
                node_id=node_id,
            )

    def do_calculate_hazard_rates(self, node_id: int) -> None:
        """Calculate the hazard rate of a hardware item.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)

        if _record.data["hardware"].part == 1:
            self.do_calculate_part_hazard_rates(node_id)
        else:
            self.do_calculate_assembly_hazard_rates(node_id)

        _record.data["reliability"].do_calculate_hazard_rate_logistics()
        _record.data["reliability"].do_calculate_hazard_rate_mission(
            _record.data["hardware"].duty_cycle
        )
        _record.data["reliability"].do_calculate_mtbf(
            multiplier=self._hr_multiplier,
        )
        _record.data["reliability"].do_calculate_reliability(
            _record.data["hardware"].mission_time,
            multiplier=self._hr_multiplier,
        )

    def do_calculate_part_count(self, node_id: int) -> None:
        """Calculate the total part count of a hardware item.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data["hardware"]
        _total_part_count: int = 0

        if _record.part == 1:
            _record.total_part_count = _record.quantity
        else:
            for _node in self.tree.children(node_id):
                self.do_calculate_part_count(_node.identifier)
                _total_part_count += _node.data["hardware"].total_part_count

            _total_part_count *= _record.quantity
            _record.set_attributes({"total_part_count": _total_part_count})

    def do_calculate_part_hazard_rates(self, node_id: int) -> None:
        """Calculate the hazard rates for parts.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)
        _attributes = {
            **_record.data["hardware"].get_attributes(),
            **_record.data["design_mechanic"].get_attributes(),
            **_record.data["design_electric"].get_attributes(),
            **_record.data["milhdbk217f"].get_attributes(),
            **_record.data["nswc"].get_attributes(),
            **_record.data["reliability"].get_attributes(),
        }

        self.do_calculate_part_stress(node_id)

        _record.data["reliability"].do_calculate_hazard_rate_active(
            self._hr_multiplier,
            _attributes,
            time=_record.data["hardware"].mission_time,
        )

        _record.data["reliability"].do_calculate_hazard_rate_dormant(
            _record.data["hardware"].category_id,
            _record.data["hardware"].subcategory_id,
            _record.data["design_electric"].environment_active_id,
            _record.data["design_electric"].environment_dormant_id,
        )

    def do_calculate_part_stress(self, node_id: int) -> None:
        """Calculate the electrical, mechanical, and thermal stress ratios on a part.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)

        _record.data["design_electric"].do_stress_analysis(
            _record.data["hardware"].category_id
        )
        _record.data["design_electric"].do_derating_analysis(
            self._dic_stress_limits[_record.data["hardware"].category_id]
        )

    def do_calculate_power_dissipation(self, node_id: int) -> float:
        """Calculate the total power dissipation of a hardware item.

        :param node_id: the record ID to calculate.
        :return: _total_power_dissipation; the total power dissipation.
        :rtype: float
        """
        _record = self.tree.get_node(node_id)
        _total_power_dissipation: float = 0.0

        if _record.data["hardware"].part == 1:
            _total_power_dissipation = (
                _record.data["design_electric"].power_operating
                * _record.data["hardware"].quantity
            )
        else:
            for _node_id in _record.successors(self.tree.identifier):
                _total_power_dissipation += self.do_calculate_power_dissipation(
                    _node_id
                )

            _total_power_dissipation *= _record.data["hardware"].quantity

        _record.data["hardware"].set_attributes(
            {"total_power_dissipation": _total_power_dissipation}
        )

        return _total_power_dissipation

    def do_make_composite_ref_des(self, node_id: int = 1) -> None:
        """Make the composite reference designators.

        :param node_id: the record ID to start making the composite reference
            designators.
        :return: None
        :rtype: None
        """
        # Retrieve the parent hardware item's composite reference designator.
        _node = self.tree.get_node(node_id)
        _record = _node.data["hardware"]

        if self.tree.parent(node_id).identifier != 0:
            _p_comp_ref_des = self.tree.parent(node_id).data["hardware"].comp_ref_des
        else:
            _p_comp_ref_des = ""

        if _p_comp_ref_des != "":
            _record.comp_ref_des = f"{_p_comp_ref_des}:{_record.ref_des}"
            _node.tag = f"{_p_comp_ref_des}:{_record.ref_des}"
        else:
            _record.comp_ref_des = _record.ref_des
            _node.tag = _record.ref_des

        # Now make the composite reference designator for all the child nodes.
        for _child_node in self.tree.children(node_id):
            self.do_make_composite_ref_des(node_id=_child_node.identifier)

        _record.set_attributes({"comp_ref_des": _record.comp_ref_des})

        pub.sendMessage(
            "succeed_make_comp_ref_des",
            comp_ref_des=_record.comp_ref_des,
        )

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
                parent=_hardware.parent_id,
                data={"hardware": _hardware},
            )

        self._dic_load_functions["design_electric"]()
        self._dic_load_functions["design_mechanic"]()
        self._dic_load_functions["milhdbk217f"]()
        self._dic_load_functions["nswc"]()
        self._dic_load_functions["reliability"]()

    def _do_load_design_electric(self) -> None:
        """Load the design electric data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["design_electric"].all_nodes()[1:]:
            _design_electric = _node.data["design_electric"]

            try:
                _par_node = self.tree.get_node(_design_electric.hardware_id)
                _par_node.data["design_electric"] = _design_electric
            except ObjectDeletedError:
                self._dic_trees["design_electric"].remove_node(_node.identifier)

    def _do_load_design_mechanic(self) -> None:
        """Load the design_mechanic into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["design_mechanic"].all_nodes()[1:]:
            _design_mechanic = _node.data["design_mechanic"]

            try:
                _par_node = self.tree.get_node(_design_mechanic.hardware_id)
                _par_node.data["design_mechanic"] = _design_mechanic
            except ObjectDeletedError:
                self._dic_trees["design_mechanic"].remove_node(_node.identifier)

    def _do_load_milhdbk217f(self) -> None:
        """Load the MIL-HDBK-217F data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["milhdbk217f"].all_nodes()[1:]:
            _milhdbk217f = _node.data["milhdbk217f"]

            try:
                _par_node = self.tree.get_node(_milhdbk217f.hardware_id)
                _par_node.data["milhdbk217f"] = _milhdbk217f
            except ObjectDeletedError:
                self._dic_trees["milhdbk217f"].remove_node(_node.identifier)

    def _do_load_nswc(self) -> None:
        """Load the NSWC data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["nswc"].all_nodes()[1:]:
            _nswc = _node.data["nswc"]

            try:
                _par_node = self.tree.get_node(_nswc.hardware_id)
                _par_node.data["nswc"] = _nswc
            except ObjectDeletedError:
                self._dic_trees["nswc"].remove_node(_node.identifier)

    def _do_load_reliability(self) -> None:
        """Load the reliability data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["reliability"].all_nodes()[1:]:
            _reliability = _node.data["reliability"]

            try:
                _par_node = self.tree.get_node(_reliability.hardware_id)
                _par_node.data["reliability"] = _reliability
            except ObjectDeletedError:
                self._dic_trees["reliability"].remove_node(_node.identifier)
