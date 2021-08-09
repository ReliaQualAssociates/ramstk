# -*- coding: utf-8 -*-
#
#       ramstk.models.<MODULE>.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""<MODULE> Package Table Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable
from ramstk.models.programdb import RAMSTK<MODULE>Record


class RAMSTK<MODULE>Table(RAMSTKBaseTable):
    """Contain the attributes and methods of the <MODULE> table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    # This is the name of the primary key field in the table being modelled
    _db_id_colname = "fld_<MODULE>_id"
    # This is the name of the database table being modelled.
    _db_tablename = "ramstk_<MODULE>"
    # This is the message that this class responds to to load all the records.
    _select_msg = "selected_revision"
    # This is the name of the module (all lowercase).
    _tag = "<MODULE>"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a <MODULE> table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        # This is the list of key/index columns in the table being modelled with the
        # fld_prefix removed.
        self._lst_id_columns = [
            ""
        ]

        # Initialize private scalar attributes.
        # This is the record class associated with the table being modelled.
        self._record: Type[RAMSTK<MODULE>Record] = RAMSTK<MODULE>Record

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        # This is the primary key in the database table with the fld_ prefix removed.
        self.pkey = ""

        # Subscribe to PyPubSub messages.
        # Add any pypubsub subscribers here.  Remember to import pubsub's pub.

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        # These are the attributes to populate and the values to use for new records.
        # At a minimum each of the key/index fields need to be populated.
        #_new_record.revision_id = attributes["revision_id"]
        #_new_record.validation_id = self.last_id + 1
        #_new_record.name = "New Validation Task"

        return _new_record

# ----- ----- ----- Add any module specific methods below this line. ----- ----- ----- #
