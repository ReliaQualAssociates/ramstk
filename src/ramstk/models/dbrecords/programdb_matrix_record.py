# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_matrix_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMatrix Record Module."""

# Third Party Imports
# noinspection PyPackageRequirements
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKMatrixRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent a ramstk_matrix record in the RAMSTK Program database."""

    __defaults__ = {
        "description": "",
        "column_id": 0,
        "row_id": 0,
        "correlation": "",
    }
    __tablename__ = "ramstk_matrix"
    __table_args__ = (
        ForeignKeyConstraint(
            ("fld_revision_id",),
            [
                "ramstk_revision.fld_revision_id",
            ],
        ),
        {"extend_existing": True},
    )

    revision_id = Column(
        "fld_revision_id",
        Integer,
        nullable=False,
    )
    matrix_id = Column(
        "fld_matrix_id",
        Integer,
        primary_key=True,
        default=-1,
        nullable=False,
    )

    description = Column(
        "fld_description",
        String,
        default=__defaults__["description"],
        nullable=False,
    )
    column_id = Column(
        "fld_column_id",
        Integer,
        default=__defaults__["column_id"],
    )
    row_id = Column(
        "fld_row_id",
        Integer,
        default=__defaults__["row_id"],
    )
    correlation = Column(
        "fld_correlation",
        String,
        default=__defaults__["correlation"],
    )

    # Define the relationships to other tables in the RAMSTK Program database.

    def get_attributes(self):
        """Retrieve current values of the RAMSTKMatrix db record model attributes.

        :return: {matrix_id, description, column_id, row_id, correlation} pairs.
        :rtype: dict
        """
        return {
            "matrix_id": self.matrix_id,
            "description": self.description,
            "column_id": self.column_id,
            "row_id": self.row_id,
            "correlation": self.correlation,
        }
