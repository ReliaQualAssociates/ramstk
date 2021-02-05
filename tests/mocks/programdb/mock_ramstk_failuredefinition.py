# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.__mocks__.programdb.mock_ramstk_revision.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mock program database ramstk_revision table."""

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKFailureDefinition

_definition_1 = RAMSTKFailureDefinition()
_definition_1.revision_id = 1
_definition_1.definition_id = 1
_definition_1.definition = 'Mock Failure Definition 1'

_definition_2 = RAMSTKFailureDefinition()
_definition_2.revision_id = 1
_definition_2.definition_id = 2
_definition_2.definition = 'Mock Failure Definition 2'

mock_ramstk_failuredefinition = [
    _definition_1,
    _definition_2,
]
