# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb..RAMSTKFailureDefinition.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFailureDefinition Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKFailureDefinition(RAMSTK_BASE, RAMSTKBaseTable):
    """Class representing ramstk_failure_definition table in RAMSTK Program db.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {'definition': 'Failure Definition'}
    __tablename__ = 'ramstk_failure_definition'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    definition_id = Column(
        'fld_definition_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    definition = Column('fld_definition',
                        String,
                        default=__defaults__['definition'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship(  # type: ignore
        'RAMSTKRevision', back_populates='failures')

    def get_attributes(self):
        """Retrieve current values of the RAMSTKFailureDefinition attributes.

        :return: {revision_id, definition_id, definition} pairs.
        :rtype: (int, int, str)
        """
        _attributes = {
            'revision_id': self.revision_id,
            'definition_id': self.definition_id,
            'definition': self.definition,
        }

        return _attributes
