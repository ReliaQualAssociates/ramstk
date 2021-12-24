# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.design_electric.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Design Electric Package Table Model."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import derating, stress
from ramstk.models import RAMSTKBaseTable, RAMSTKDesignElectricRecord


def do_check_overstress(
    overstress: Dict[str, List[float]], stress_type: str
) -> Tuple[bool, str]:
    """Check the overstress condition and build a reason message.

    :param overstress: the dict containing the results of the
        overstress analysis.
    :param stress_type: the overstress type being checked.
    :return: (_overstress, _reason); whether a component is overstressed and the reason.
    :rtype: tuple
    """
    _overstress = False
    _reason = ""

    if overstress["harsh"][0]:
        _overstress = True
        _reason = _reason + (
            "Operating {0:s} is less than limit in a "
            "harsh environment.\n".format(str(stress_type))
        )
    if overstress["harsh"][1]:
        _overstress = True
        _reason = _reason + (
            "Operating {0:s} is greater than limit "
            "in a harsh environment.\n".format(str(stress_type))
        )
    if overstress["mild"][0]:
        _overstress = True
        _reason = _reason + (
            "Operating {0:s} is less than limit in a "
            "mild environment.\n".format(str(stress_type))
        )
    if overstress["mild"][1]:
        _overstress = True
        _reason = _reason + (
            "Operating {0:s} is greater than limit "
            "in a mild environment.\n".format(str(stress_type))
        )

    return _overstress, _reason


class RAMSTKDesignElectricTable(RAMSTKBaseTable):
    """Contain attributes and methods of the Design Electric table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_design_electric"
    _select_msg = "selected_revision"
    _tag = "design_electric"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Design Electric table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_stress_limits: Dict[int, List[float]] = kwargs.get(
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

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        # This is the record class associated with the table being modelled.
        self._record: Type[RAMSTKDesignElectricRecord] = RAMSTKDesignElectricRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_derating_analysis, "request_derating_analysis")
        pub.subscribe(self.do_stress_analysis, "request_stress_analysis")

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
        _new_record.hardware_id = self.last_id + 1

        return _new_record

    def do_calculate_current_ratio(self, node_id: int) -> None:
        """Calculate the current ratio.

        :return: None
        :rtype: None
        """
        _attributes = self.tree.get_node(node_id).data[self._tag].get_attributes()

        try:
            _attributes["current_ratio"] = stress.calculate_stress_ratio(
                _attributes["current_operating"],
                _attributes["current_rated"],
            )

            self.do_set_attributes(
                node_id=[node_id],
                package={"current_ratio": _attributes["current_ratio"]},
            )
        except ZeroDivisionError:
            _error_msg: str = (
                "Failed to calculate current ratio for hardware ID {0}.  Rated "
                "current={1}, operating current={2}."
            ).format(
                str(_attributes["hardware_id"]),
                _attributes["current_rated"],
                _attributes["current_operating"],
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_calculate_current_stress",
                error_message=_error_msg,
            )

    def do_calculate_power_ratio(self, node_id: int) -> None:
        """Calculate the power ratio.

        :return: None
        :rtype: None
        """
        _attributes = self.tree.get_node(node_id).data[self._tag].get_attributes()

        try:
            _attributes["power_ratio"] = stress.calculate_stress_ratio(
                _attributes["power_operating"],
                _attributes["power_rated"],
            )

            self.do_set_attributes(
                node_id=[node_id],
                package={"power_ratio": _attributes["power_ratio"]},
            )
        except ZeroDivisionError:
            _error_msg: str = (
                "Failed to calculate power ratio for hardware ID {0}.  Rated "
                "power={1}, operating power={2}."
            ).format(
                str(_attributes["hardware_id"]),
                _attributes["power_rated"],
                _attributes["power_operating"],
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_calculate_power_stress",
                error_message=_error_msg,
            )

    def do_calculate_voltage_ratio(self, node_id: int) -> None:
        """Calculate the voltage ratio.

        :return: None
        :rtype: None
        """
        _attributes = self.tree.get_node(node_id).data[self._tag].get_attributes()

        _voltage_operating = (
            _attributes["voltage_ac_operating"] + _attributes["voltage_dc_operating"]
        )

        try:
            _attributes["voltage_ratio"] = stress.calculate_stress_ratio(
                _voltage_operating, _attributes["voltage_rated"]
            )

            self.do_set_attributes(
                node_id=[node_id],
                package={"voltage_ratio": _attributes["voltage_ratio"]},
            )
        except ZeroDivisionError:
            _error_msg: str = (
                "Failed to calculate voltage ratio for hardware ID {0}.  Rated "
                "voltage={1}, operating ac voltage={2}, operating DC voltage={3}."
            ).format(
                str(_attributes["hardware_id"]),
                _attributes["voltage_rated"],
                _attributes["voltage_ac_operating"],
                _attributes["voltage_dc_operating"],
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_calculate_voltage_stress",
                error_message=_error_msg,
            )

    def do_derating_analysis(self, node_id: int, category_id: int) -> None:
        """Perform a derating analysis.

        :param node_id: the record ID to derate.
        :param category_id: the component category ID for the record to derate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _overstress = False
        _reason = ""

        _current_limits = {
            "harsh": [0.0, self._dic_stress_limits[category_id][0]],
            "mild": [0.0, self._dic_stress_limits[category_id][1]],
        }
        _power_limits = {
            "harsh": [0.0, self._dic_stress_limits[category_id][2]],
            "mild": [0.0, self._dic_stress_limits[category_id][3]],
        }
        _voltage_limits = {
            "harsh": [0.0, self._dic_stress_limits[category_id][4]],
            "mild": [0.0, self._dic_stress_limits[category_id][5]],
        }

        _ostress, _rsn = do_check_overstress(
            derating.check_overstress(_record.current_ratio, _current_limits),
            "current",
        )
        _overstress = _overstress or _ostress
        _reason = _reason + _rsn

        _ostress, _rsn = do_check_overstress(
            derating.check_overstress(_record.power_ratio, _power_limits), "power"
        )
        _overstress = _overstress or _ostress
        _reason = _reason + _rsn

        _ostress, _rsn = do_check_overstress(
            derating.check_overstress(_record.voltage_ratio, _voltage_limits), "voltage"
        )
        _overstress = _overstress or _ostress
        _reason = _reason + _rsn

        pub.sendMessage(
            "request_set_design_electric_attributes",
            node_id=node_id,
            package={"overstress": _overstress},
        )
        pub.sendMessage(
            "request_set_design_electric_attributes",
            node_id=node_id,
            package={"reason": _reason},
        )

    def do_stress_analysis(self, node_id: int, category_id: int) -> None:
        """Perform a stress analysis.

        :param node_id: the record ID to calculate.
        :param category_id: the component category ID of the record to calculate.
        :return: None
        :rtype: None
        """
        if category_id in [1, 2, 5, 6, 7, 8]:
            self.do_calculate_current_ratio(node_id)

        if category_id == 3:
            self.do_calculate_power_ratio(node_id)

        if category_id in [4, 5, 8]:
            self.do_calculate_voltage_ratio(node_id)
