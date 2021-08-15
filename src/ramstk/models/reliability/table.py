# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.reliability.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Reliability Package Table Model."""

# Standard Library Imports
from math import exp
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import dormancy
from ramstk.analyses.statistics import exponential, lognormal, normal, weibull
from ramstk.models import RAMSTKBaseTable
from ramstk.models.programdb import RAMSTKReliability


class RAMSTKReliabilityTable(RAMSTKBaseTable):
    """Contain attributes and methods of the Reliability table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_reliability"
    _select_msg = "selected_revision"
    _tag = "reliability"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Reliability table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKReliability] = RAMSTKReliability

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self.do_calculate_hazard_rate_active, "request_calculate_hazard_rate_active"
        )
        pub.subscribe(
            self.do_calculate_hazard_rate_dormant,
            "request_calculate_hazard_rate_dormant",
        )
        pub.subscribe(
            self.do_calculate_hazard_rate_logistics,
            "request_calculate_hazard_rate_logistics",
        )
        pub.subscribe(
            self.do_calculate_hazard_rate_mission,
            "request_calculate_hazard_rate_mission",
        )
        pub.subscribe(self.do_calculate_mtbf, "request_calculate_mtbf")
        pub.subscribe(self.do_calculate_reliability, "request_calculate_reliability")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.hardware_id = attributes["hardware_id"]

        return _new_record

    def do_calculate_hazard_rate_active(
        self,
        node_id: int,
        duty_cycle: float,
        quantity: int,
        multiplier: float,
        time: float = 1.0,
    ) -> None:
        """Calculate the active hazard rate.

        :param node_id: the record ID to calculate.
        :param duty_cycle: the duty cycle of the item being calculated.  Comes from
            RAMSTKHardwareTable.
        :param quantity: the quantity of the item being calculated.  Comes from
            RAMSTKHardwareTable.
        :param multiplier: the time multiplier for hazard rates.  Typically set to
            1.0 to work with failures/hour or 1000000.0 to work with failures/10^6
            hours.  Set the value in RAMSTK.toml.
        :param time: the time at which to calculate the hazard rate.  Applicable to
            non-EXP hazard functions.
        :return: _hazard_rate_active; the active hazard rate.
        :rtype: float
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _record.hazard_rate_active = 0.0

        if _record.hazard_rate_type_id == 1:
            pub.sendMessage("request_predict_active_hazard_rate", node_id=node_id)
        elif _record.hazard_rate_type_id == 2:
            _record.hazard_rate_active = _record.hazard_rate_specified
        elif _record.hazard_rate_type_id == 3:
            _record.hazard_rate_active = exponential.get_hazard_rate(
                _record.mtbf_specified
            )
        elif _record.hazard_rate_type_id == 4:
            _function = {
                1: exponential.get_hazard_rate(
                    _record.scale_parameter,
                    location=0.0,
                ),
                2: exponential.get_hazard_rate(
                    _record.scale_parameter,
                    location=_record.location_parameter,
                ),
                3: lognormal.get_hazard_rate(
                    _record.shape_parameter,
                    time,
                    location=0.0,
                    scale=_record.scale_parameter,
                ),
                4: lognormal.get_hazard_rate(
                    _record.shape_parameter,
                    time,
                    location=_record.location_parameter,
                    scale=_record.scale_parameter,
                ),
                5: normal.get_hazard_rate(
                    _record.location_parameter,
                    _record.scale_parameter,
                    time,
                ),
                6: weibull.get_hazard_rate(
                    _record.shape_parameter,
                    _record.scale_parameter,
                    time,
                    location=0.0,
                ),
                7: weibull.get_hazard_rate(
                    _record.shape_parameter,
                    _record.scale_parameter,
                    time,
                    location=_record.location_parameter,
                ),
            }[_record.failure_distribution_id]
            _record.hazard_rate_active = _function

        _record.hazard_rate_active = (
            (_record.hazard_rate_active + _record.add_adj_factor)
            * _record.mult_adj_factor
            * (duty_cycle / 100.0)
            * quantity
            * multiplier
        )

        pub.sendMessage(
            "request_update_reliability_attributes",
            node_id=[1],
            package={"hazard_rate_active": _record.hazard_rate_active},
        )

    def do_calculate_hazard_rate_dormant(
        self,
        node_id: int,
        category_id: int,
        subcategory_id: int,
        env_active: int,
        env_dormant: int,
    ) -> None:
        """Calculate the dormant hazard rate.

        :param node_id: the record ID to calculate.
        :param category_id: the ID of the component category.
        :param subcategory_id: the ID of the component subcategory.
        :param env_active: the ID of the active environment.
        :param env_dormant: the ID of the dormant environment.
        :return: _hazard_rate_dormant; the dormant hazard rate.
        :rtype: float
        """
        _record = self.tree.get_node(node_id).data[self._tag]

        _record.hazard_rate_dormant = dormancy.do_calculate_dormant_hazard_rate(
            [
                category_id,
                subcategory_id,
                _record.hazard_rate_active,
            ],
            [
                env_active,
                env_dormant,
            ],
        )

        pub.sendMessage(
            "request_update_reliability_attributes",
            node_id=[1],
            package={"hazard_rate_dormant": _record.hazard_rate_dormant},
        )

    def do_calculate_hazard_rate_logistics(self, node_id: int) -> None:
        """Calculate the logistics hazard rate.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]

        _record.hazard_rate_logistics = (
            _record.hazard_rate_active
            + _record.hazard_rate_dormant
            + _record.hazard_rate_software
        )

        pub.sendMessage(
            "request_set_reliability_attributes",
            node_id=[node_id],
            package={"hazard_rate_logistics": _record.hazard_rate_logistics},
        )

    def do_calculate_hazard_rate_mission(self, node_id: int, duty_cycle: float) -> None:
        """Calculate the logistics hazard rate.

        :param node_id: the record ID to calculate.
        :param duty_cycle: the duty cycle of the item record.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]

        _record.hazard_rate_mission = (
            (_record.hazard_rate_active * duty_cycle)
            + (_record.hazard_rate_dormant * (1 - duty_cycle))
            + _record.hazard_rate_software
        )

        pub.sendMessage(
            "request_set_reliability_attributes",
            node_id=[node_id],
            package={"hazard_rate_mission": _record.hazard_rate_mission},
        )

    def do_calculate_mtbf(self, node_id: int, multiplier: float) -> None:
        """Calculate the logistics and mission MTBF.

        :param node_id: the record ID to calculate.
        :param multiplier: the time multiplier for MTBF.  Typically set to
            1.0 to work with hours/failure or 1000000.0 to work with 10^6 hours/failure.
            Set the value in RAMSTK.toml.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]

        try:
            _record.mtbf_logistics = multiplier / _record.hazard_rate_logistics
        except ZeroDivisionError:
            _record.mtbf_logistics = 0.0

        pub.sendMessage(
            "request_set_reliability_attributes",
            node_id=[node_id],
            package={"mtbf_logistics": _record.mtbf_logistics},
        )

        try:
            _record.mtbf_mission = multiplier / _record.hazard_rate_mission
        except ZeroDivisionError:
            _record.mtbf_mission = 0.0

        pub.sendMessage(
            "request_set_reliability_attributes",
            node_id=[node_id],
            package={"mtbf_mission": _record.mtbf_mission},
        )

    def do_calculate_reliability(self, node_id: int, time: float) -> None:
        """Calculate the reliability related metrics.

        :param node_id: the record ID to calculate.
        :param time: the time at which to calculate the reliabilities.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]

        _record.reliability_logistics = exp(-1.0 * _record.hazard_rate_logistics * time)

        pub.sendMessage(
            "request_set_reliability_attributes",
            node_id=[node_id],
            package={"reliability_logistics": _record.reliability_logistics},
        )

        _record.reliability_mission = exp(-1.0 * _record.hazard_rate_mission * time)

        pub.sendMessage(
            "request_set_reliability_attributes",
            node_id=[node_id],
            package={"reliability_mission": _record.reliability_mission},
        )
