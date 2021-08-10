# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.design_electric.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Design Electric Package Table Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import stress
from ramstk.models import RAMSTKBaseTable
from ramstk.models.programdb import RAMSTKDesignElectric


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

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
        ]

        # Initialize private scalar attributes.
        # This is the record class associated with the table being modelled.
        self._record: Type[RAMSTKDesignElectric] = RAMSTKDesignElectric

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.

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
