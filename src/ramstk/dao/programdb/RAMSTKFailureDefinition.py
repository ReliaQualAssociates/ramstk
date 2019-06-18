# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKFailureDefinition.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFailureDefinition Table Module."""

# Third Party Imports
# Import third party modules.
from sqlalchemy import BLOB, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import error_handler, none_to_default


class RAMSTKFailureDefinition(RAMSTK_BASE):
    """
    Class representing ramstk_failure_definition table in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

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

    definition = Column('fld_definition', BLOB, default=b'Failure Definition')

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
        Set the current values of the RAMSTKFailureDefinition attributes.

        :param dict attributes: dict containing {attr name:attr value} pairs
                                of the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKFailureDefinition {0:d} attributes.".\
            format(self.definition_id)

        try:
            self.definition = none_to_default(
                attributes['definition'],
                b'Failure Definition',
            )
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKFailureDefinition.set_attributes().".format(str(_err))
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKFailureDefinition attributes."

        return _error_code, _msg
