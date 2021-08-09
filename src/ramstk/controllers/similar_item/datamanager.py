# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.similar_item.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Similar Item Package Data Model."""

# Standard Library Imports
from collections import OrderedDict
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import similaritem
from ramstk.models import RAMSTKBaseTable
from ramstk.models.programdb import RAMSTKSimilarItem


class DataManager(RAMSTKBaseTable):
    """Contain the attributes and methods of the Similar Item data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_similar_item"
    _select_msg = "selected_revision"
    _tag = "similar_item"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Hardware data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
        ]

        # Initialize private scalar attributes.
        self._node_hazard_rate: float = 0.0
        self._record: Type[RAMSTKSimilarItem] = RAMSTKSimilarItem

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_calculate_similar_item, "request_calculate_similar_item")
        pub.subscribe(
            self.do_roll_up_change_descriptions, "request_roll_up_change_descriptions"
        )

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes["parent_id"]

        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.hardware_id = attributes["hardware_id"]
        _new_record.parent_id = attributes["parent_id"]

        return _new_record

    def do_calculate_similar_item(self, node_id: int) -> None:
        """Perform a similar item calculation for record ID.

        :param node_id: the node (similar item) ID to calculate.
        :return: None
        :rtype: None
        """
        _dic_method = {
            1: self._do_calculate_topic_633,
            2: self._do_calculate_user_defined,
        }

        _record = self.tree.get_node(node_id).data[self._tag]
        try:
            _method = _dic_method[_record.similar_item_method_id]
            _method(node_id)

            pub.sendMessage(
                "succeed_calculate_similar_item",
                tree=self.tree,
            )
        except KeyError:
            _error_msg: str = (
                "Failed to calculate similar item reliability for hardware ID {0}.  "
                "Unknown similar item method ID {1} selected.".format(
                    node_id, _record.similar_item_method_id
                )
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_calculate_similar_item",
                error_message=_error_msg,
            )

    def do_roll_up_change_descriptions(self, node_id: int) -> None:
        """Concatenate child change descriptions for the node ID similar item.

        :param node_id: the record ID of the parent to which the rolled-up
            descriptions are assigned.
        :return: None
        :rtype: None
        """
        _change_description_1 = ""
        _change_description_2 = ""
        _change_description_3 = ""
        _change_description_4 = ""
        _change_description_5 = ""
        _change_description_6 = ""
        _change_description_7 = ""
        _change_description_8 = ""
        _change_description_9 = ""
        _change_description_10 = ""

        for _node in self.tree.children(node_id):
            _change_description_1 += (
                _node.data["similar_item"].change_description_1 + "\n\n"
            )
            _change_description_2 += (
                _node.data["similar_item"].change_description_2 + "\n\n"
            )
            _change_description_3 += (
                _node.data["similar_item"].change_description_3 + "\n\n"
            )
            _change_description_4 += (
                _node.data["similar_item"].change_description_4 + "\n\n"
            )
            _change_description_5 += (
                _node.data["similar_item"].change_description_5 + "\n\n"
            )
            _change_description_6 += (
                _node.data["similar_item"].change_description_6 + "\n\n"
            )
            _change_description_7 += (
                _node.data["similar_item"].change_description_7 + "\n\n"
            )
            _change_description_8 += (
                _node.data["similar_item"].change_description_8 + "\n\n"
            )
            _change_description_9 += (
                _node.data["similar_item"].change_description_9 + "\n\n"
            )
            _change_description_10 += (
                _node.data["similar_item"].change_description_10 + "\n\n"
            )

        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_1": _change_description_1,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_2": _change_description_2,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_3": _change_description_3,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_4": _change_description_4,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_5": _change_description_5,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_6": _change_description_6,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_7": _change_description_7,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_8": _change_description_8,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_9": _change_description_9,
            },
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={
                "change_description_10": _change_description_10,
            },
        )

        pub.sendMessage(
            "succeed_roll_up_change_descriptions",
            tree=self.tree,
        )

    def _do_calculate_topic_633(self, node_id: int) -> None:
        """Calculate the similar item hazard rate per topic 6.3.3.

        .. note:: this analysis uses the adjustment factors from RAC/RiAC's The
            Reliability Toolkit, Commercial Practices Edition, section 6.3.3.

        :param node_id: the record ID to calculate similar item reliability.
        :return: None
        :rtype: None
        """
        _attributes = self.tree.get_node(node_id).data[self._tag].get_attributes()

        _environment = {
            "from": _attributes["environment_from_id"],
            "to": _attributes["environment_to_id"],
        }
        _quality = {
            "from": _attributes["quality_from_id"],
            "to": _attributes["quality_to_id"],
        }
        _temperature = {
            "from": _attributes["temperature_from"],
            "to": _attributes["temperature_to"],
        }

        (
            _attributes["change_factor_1"],
            _attributes["change_factor_2"],
            _attributes["change_factor_3"],
            _attributes["result_1"],
        ) = similaritem.calculate_topic_633(
            _environment, _quality, _temperature, self._node_hazard_rate
        )

        self.do_set_attributes_all(
            attributes=_attributes,
        )

    def _do_calculate_user_defined(self, node_id: int) -> None:
        """Calculate the user-defined similar item hazard rate.

        :param node_id: the record ID to calculate similar item reliability.
        :return: None
        :rtype: None
        """
        _attributes = self.tree.get_node(node_id).data[self._tag].get_attributes()

        _sia: Dict[str, Any] = OrderedDict(
            {
                _key: None
                for _key in [
                    "hr",
                    "pi1",
                    "pi2",
                    "pi3",
                    "pi3",
                    "pi4",
                    "pi5",
                    "pi6",
                    "pi7",
                    "pi8",
                    "pi9",
                    "pi10",
                    "uf1",
                    "uf2",
                    "uf3",
                    "uf4",
                    "uf5",
                    "ui1",
                    "ui2",
                    "ui3",
                    "ui4",
                    "ui5",
                    "equation1",
                    "equation2",
                    "equation3",
                    "equation4",
                    "equation5",
                    "res1",
                    "res2",
                    "res3",
                    "res4",
                    "res5",
                ]
            }
        )

        _sia["hr"] = self._node_hazard_rate

        _sia = similaritem.set_user_defined_change_factors(
            _sia,
            [
                _attributes["change_factor_1"],
                _attributes["change_factor_2"],
                _attributes["change_factor_3"],
                _attributes["change_factor_4"],
                _attributes["change_factor_5"],
                _attributes["change_factor_6"],
                _attributes["change_factor_7"],
                _attributes["change_factor_8"],
                _attributes["change_factor_9"],
                _attributes["change_factor_10"],
            ],
        )

        _sia = similaritem.set_user_defined_floats(
            _sia,
            [
                _attributes["user_float_1"],
                _attributes["user_float_2"],
                _attributes["user_float_3"],
                _attributes["user_float_4"],
                _attributes["user_float_5"],
            ],
        )

        _sia = similaritem.set_user_defined_ints(
            _sia,
            [
                _attributes["user_int_1"],
                _attributes["user_int_2"],
                _attributes["user_int_3"],
                _attributes["user_int_4"],
                _attributes["user_int_5"],
            ],
        )

        _sia = similaritem.set_user_defined_functions(
            _sia,
            [
                _attributes["function_1"],
                _attributes["function_2"],
                _attributes["function_3"],
                _attributes["function_4"],
                _attributes["function_5"],
            ],
        )

        _sia = similaritem.set_user_defined_results(
            _sia,
            [
                _attributes["result_1"],
                _attributes["result_2"],
                _attributes["result_3"],
                _attributes["result_4"],
                _attributes["result_5"],
            ],
        )

        _sia = similaritem.calculate_user_defined(_sia)
        _attributes["result_1"] = _sia["res1"]
        _attributes["result_2"] = _sia["res2"]
        _attributes["result_3"] = _sia["res3"]
        _attributes["result_4"] = _sia["res4"]
        _attributes["result_5"] = _sia["res5"]

        self.do_set_attributes_all(
            attributes=_attributes,
        )
