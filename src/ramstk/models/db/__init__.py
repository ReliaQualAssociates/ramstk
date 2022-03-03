# pylint: disable=unused-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.db.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK database models package."""

# Third Party Imports
from sqlalchemy.ext.declarative import declarative_base

RAMSTK_BASE = declarative_base()  # isort: skip

# RAMSTK Local Imports
from .basedatabase import BaseDatabase, do_create_program_db
from .common_database import RAMSTKCommonDB
from .program_database import RAMSTKProgramDB
