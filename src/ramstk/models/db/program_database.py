# -*- coding: utf-8 -*-
#
#       ramstk.models.db.program_database.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK program database model."""

# Standard Library Imports
from typing import Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.exceptions import DataAccessError

# RAMSTK Local Imports
from .basedatabase import BaseDatabase, do_create_program_db


class RAMSTKProgramDB:
    """The RAMSTK program database model class.

    The attributes of a RAMSTK program database model are:

    :ivar dic_tables: a dict containing the instances of all the database table
        models this program database model is managing.
    :ivar dic_views: a dict containing the instances of all the database view
        models this program database model is managing.
    :ivar user_configuration: the RAMSTKUserConfiguration instance associated with
        this progam database model.
    :ivar program_dao: the BaseDatabase() object that will connect to the
        RAMSTK program database.
    """

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTK program database model."""

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_tables: Dict[str, object] = {
            "action": object,
            "allocation": object,
            "cause": object,
            "control": object,
            "design_electric": object,
            "design_mechanic": object,
            "environment": object,
            "failure_definition": object,
            "function": object,
            "hardware": object,
            "hazards": object,
            "mechanism": object,
            "milhdbk217f": object,
            "mission": object,
            "mission_phase": object,
            "mode": object,
            "nswc": object,
            "opload": object,
            "opstress": object,
            "program_info": object,
            "program_status": object,
            "reliability": object,
            "requirement": object,
            "revision": object,
            "similar_item": object,
            "stakeholder": object,
            "test_method": object,
            "validation": object,
            "options": object,
            "export": object,
            "import": object,
        }
        self.dic_views: Dict[str, object] = {
            "fmea": object,
            "hardwarebom": object,
            "pof": object,
            "usage_profile": object,
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.user_configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration()
        self.program_dao: BaseDatabase = BaseDatabase()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_create_program, "request_create_program")
        pub.subscribe(self.do_open_program, "request_open_program")
        pub.subscribe(self.do_open_program, "succeed_create_program_database")
        pub.subscribe(self.do_close_program, "request_close_program")
        pub.subscribe(self.do_save_program, "request_update_program")

    def do_create_program(
        self, program_db: BaseDatabase, database: Dict[str, str]
    ) -> None:
        """Create a new RAMSTK Program database.

        :param program_db: the BaseDatabase() that is to be used to create and connect
            to the new RAMSTK program database.
        :param database: a dict containing the database connection arguments.
        :return: None
        :rtype: None
        """
        with open(
            f"{self.user_configuration.RAMSTK_CONF_DIR}/"
            f"{database['dialect']}_program_db.sql",
            "r",
            encoding="utf-8",
        ) as _sql_file:
            self.program_dao = program_db
            do_create_program_db(database, _sql_file)
            pub.sendMessage(
                "succeed_create_program_database",
                program_db=self.program_dao,
                database=database,
            )

    def do_open_program(
        self, program_db: BaseDatabase, database: Dict[str, str]
    ) -> None:
        """Open an RAMSTK Program database for analyses.

        :param program_db: the BaseDatabase() that is to be used to create and
            connect to the new RAMSTK program database.
        :param database: a dictionary of parameters to pass to the DAO.
        :return: None
        :rtype: None
        """
        self.program_dao = program_db

        try:
            self.program_dao.do_connect(database)
            pub.sendMessage("succeed_connect_program_database", dao=self.program_dao)
            pub.sendMessage(
                "request_retrieve_revisions", attributes={"revision_id": None}
            )
        except DataAccessError as _error:
            pub.sendMessage("fail_connect_program_database", error_message=_error.msg)

    def do_close_program(self) -> None:
        """Close the open RAMSTK Program database.

        :return: None
        :rtype: None
        :raises: AttributeError if a database isn't open.
        """
        try:
            self.program_dao.do_disconnect()
            pub.sendMessage("succeed_disconnect_program_database")
        except AttributeError:
            _error_msg = "Not currently connected to a database.  Nothing to close."
            pub.sendMessage(
                "fail_disconnect_program_database", error_message=_error_msg
            )

    @staticmethod
    def do_save_program() -> None:
        """Save the open RAMSTK Program database.

        :return: None
        :rtype: None
        """
        pub.sendMessage("request_update_all_revision")
        pub.sendMessage("request_update_all_function")
        pub.sendMessage("request_update_all_requirement")
        pub.sendMessage("request_update_all_stakeholder")
        pub.sendMessage("request_update_all_hardware")
        pub.sendMessage("request_update_all_validation")
