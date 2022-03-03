# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_hazard_table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKHazard Table Model."""

# Standard Library Imports
from collections import OrderedDict
from datetime import date
from typing import Dict, Type, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import fha

# RAMSTK Local Imports
from ..dbrecords import RAMSTKHazardRecord
from .basetable import RAMSTKBaseTable


class RAMSTKHazardTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Hazard table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hazard_id"
    _db_tablename = "ramstk_hazard_analysis"
    _select_msg = "selected_revision"
    _tag = "hazard"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKHazard table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "function_id",
            "hazard_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKHazardRecord] = RAMSTKHazardRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hazard_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_calculate_fha, "request_calculate_fha")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKHazardRecord:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        attributes["hazard_id"] = self.last_id + 1
        attributes["parent_id"] = attributes["function_id"]
        attributes["record_id"] = attributes["hazard_id"]

        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.function_id = attributes["function_id"]
        _new_record.hazard_id = attributes["hazard_id"]

        return _new_record

    def do_calculate_fha(self, node_id: int) -> None:
        """Perform a hazards analysis calculation for currently selected item.

        :param node_id: the ID of the record to calculate.
        :return: None
        :rtype: None
        """
        self._do_calculate_hri(node_id)
        self._do_calculate_user_defined(node_id)

        pub.sendMessage(
            f"succeed_calculate_{self._tag}",
            tree=self.tree,
        )

    def _do_calculate_hri(self, node_id: int) -> None:
        """Calculate the hazard risk index (HRI).

        This method calculates the assembly and system level HRI for both
        before and after mitigation actions.

        :param node_id: the ID of the record to calculate.
        :return: None
        :rtype: None
        :raises: KeyError if one or more attribute keys is missing.
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _attributes = _record.get_attributes()

        _result = fha.calculate_hri(
            _attributes["assembly_probability"],
            _attributes["assembly_severity"],
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"assembly_hri": _result},
        )

        _result = fha.calculate_hri(
            _attributes["system_probability"],
            _attributes["system_severity"],
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"system_hri": _result},
        )

        _result = fha.calculate_hri(
            _attributes["assembly_probability_f"],
            _attributes["assembly_severity_f"],
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"assembly_hri_f": _result},
        )

        _result = fha.calculate_hri(
            _attributes["system_probability_f"],
            _attributes["system_severity_f"],
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"system_hri_f": _result},
        )

    def _do_calculate_user_defined(self, node_id: int) -> None:
        """Calculate the user-defined hazard analysis.

        :param node_id: the ID of the record to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _attributes = _record.get_attributes()

        _fha = OrderedDict(
            {
                _key: ""
                for _key in [
                    "uf1",
                    "uf2",
                    "uf3",
                    "ui1",
                    "ui2",
                    "ui3",
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

        _fha = fha.set_user_defined_floats(
            _fha,
            [
                _attributes["user_float_1"],
                _attributes["user_float_2"],
                _attributes["user_float_3"],
            ],
        )

        _fha = fha.set_user_defined_ints(
            _fha,
            [
                _attributes["user_int_1"],
                _attributes["user_int_2"],
                _attributes["user_int_3"],
            ],
        )

        _fha = fha.set_user_defined_functions(
            _fha,
            [
                _attributes["function_1"],
                _attributes["function_2"],
                _attributes["function_3"],
                _attributes["function_4"],
                _attributes["function_5"],
            ],
        )

        _fha = fha.set_user_defined_results(
            _fha,
            [
                _attributes["result_1"],
                _attributes["result_2"],
                _attributes["result_3"],
                _attributes["result_4"],
                _attributes["result_5"],
            ],
        )

        _fha = fha.calculate_user_defined(_fha)

        self.do_set_attributes(
            node_id=node_id,
            package={"result_1": float(_fha["res1"])},
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"result_2": float(_fha["res2"])},
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"result_3": float(_fha["res3"])},
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"result_4": float(_fha["res4"])},
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"result_5": float(_fha["res5"])},
        )
