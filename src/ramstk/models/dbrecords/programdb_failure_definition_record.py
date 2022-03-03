# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_failure_definition_record.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFailureDefinition Record Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKFailureDefinitionRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class representing ramstk_failure_definition table in RAMSTK Program db.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {"definition": "Failure Definition"}
    __tablename__ = "ramstk_failure_definition"
    __table_args__ = {"extend_existing": True}

    revision_id = Column(
        "fld_revision_id",
        Integer,
        ForeignKey("ramstk_revision.fld_revision_id", ondelete="CASCADE"),
        nullable=False,
    )
    function_id = Column(
        "fld_function_id",
        Integer,
        ForeignKey("ramstk_function.fld_function_id", ondelete="CASCADE"),
        nullable=False,
    )
    definition_id = Column(
        "fld_definition_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    definition = Column("fld_definition", String, default=__defaults__["definition"])

    # Define the relationships to other tables in the RAMSTK Program database.

    def get_attributes(self) -> Dict[str, Union[float, int, str]]:
        """Retrieve current values of the RAMSTKFailureDefinition attributes.

        :return: {revision_id, definition_id, definition} pairs.
        :rtype: (int, int, str)
        """
        return {
            "revision_id": self.revision_id,
            "function_id": self.function_id,
            "definition_id": self.definition_id,
            "definition": self.definition,
        }
