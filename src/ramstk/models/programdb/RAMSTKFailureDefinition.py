# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb..RAMSTKFailureDefinition.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFailureDefinition Table Module."""

# Third Party Imports
from sqlalchemy import BLOB, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKFailureDefinition(RAMSTK_BASE):
    """
    Class representing ramstk_failure_definition table in RAMSTK Program db.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {'definition': b'Failure Definition'}
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
                        BLOB,
                        default=__defaults__['definition'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='failures')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKFailureDefinition attributes.

        :return: {revision_id, definition_id, definition} pairs.
        :rtype: (int, int, str)
        """
        _attributes = {
            'revision_id': self.revision_id,
            'definition_id': self.definition_id,
            'definition': self.definition,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set current values of RAMSTKFailureDefinition data model attributes.

        .. note:: you should pop the revision ID and failure definition ID
        entries from the attributes dict before passing it to this method.

        :param dict attributes: dict of values to assign to the instance
            attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(self, _key,
                    none_to_default(attributes[_key], self.__defaults__[_key]))
