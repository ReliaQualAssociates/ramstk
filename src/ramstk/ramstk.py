# -*- coding: utf-8 -*-
#
#       ramstk.ramstk.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK program manager."""

# Standard Library Imports
from typing import Dict

# Third Party Imports
from pubsub import pub
# noinspection PyPackageRequirements
from sqlalchemy.exc import (  # type: ignore
    ArgumentError, NoSuchModuleError, OperationalError
)

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.db import BaseDatabase, do_create_program_db
from ramstk.exceptions import DataAccessError


class RAMSTKProgramManager:
    """The RAMSTK program manager class.

    The RAMSTK program manager is responsible for managing all the analysis,
    data, and matrix managers associated with the RAMSTK program database that
    is currently open.  The attributes of a RAMSTK program manager are:

    :ivar dict dic_managers: a dict containing the instances of all the
        analysis, data, and matrix managers associated with the currently
        active run of RAMSTK.  The first key is the workstream module name
        which has a dict as a value.  The key of this second dict is the type
        of manager (analysis, data, matrix) and the value will be the instance
        of the applicable manager.
    :ivar program_dao: the BaseDatabase() object that will connect to the
        RAMSTK program database.
    :type program_dao: :class:`ramstk.db.base.BaseDatabase`
    """
    def __init__(self) -> None:
        """Initialize an instance of the RAMSTK program manager."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_managers: Dict[str, Dict[str, object]] = {
            'allocation': {
                'analysis': None,
                'data': None
            },
            'revision': {
                'data': None
            },
            'failure_definition': {
                'data': None
            },
            'function': {
                'analysis': None,
                'data': None
            },
            'ffmea': {
                'analysis': None,
                'data': None
            },
            'requirement': {
                'data': None
            },
            'similar_item': {
                'analysis': None,
                'data': None
            },
            'stakeholder': {
                'analysis': None,
                'data': None
            },
            'hardware': {
                'analysis': None,
                'data': None
            },
            'hazards': {
                'analysis': None,
                'data': None
            },
            'fmea': {
                'analysis': None,
                'data': None
            },
            'pof': {
                'data': None
            },
            'program_status': {
                'data': None
            },
            'usage_profile': {
                'data': None
            },
            'validation': {
                'analysis': None,
                'data': None
            },
            'options': {
                'data': None
            },
            'exim': {
                'export': None
            },
            'preferences': {
                'data': None
            },
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.user_configuration: RAMSTKUserConfiguration = \
            RAMSTKUserConfiguration()
        self.program_dao: BaseDatabase = BaseDatabase()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_create_program, 'request_create_program')
        pub.subscribe(self.do_open_program, 'request_open_program')
        pub.subscribe(self.do_open_program, 'succeed_create_program_database')
        pub.subscribe(self.do_close_program, 'request_close_program')
        pub.subscribe(self.do_save_program, 'request_update_program')

    def do_create_program(self, program_db: BaseDatabase,
                          database: Dict[str, str]) -> None:
        """Create a new RAMSTK Program database.

        :param program_db: the BaseDatabase() that is to be used to create and
            connect to the new RAMSTK program database.
        :param database: a dict containing the database connection
            arguments.
        :return: None
        :rtype: None
        """
        _sql_file = open(
            self.user_configuration.RAMSTK_CONF_DIR
            + '/{0}_program_db.sql'.format(database['dialect']), 'r')
        self.program_dao = program_db
        do_create_program_db(database, _sql_file)
        pub.sendMessage('succeed_create_program_database',
                        program_db=self.program_dao,
                        database=database)

    def do_open_program(self, program_db: BaseDatabase,
                        database: Dict[str, str]) -> None:
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
            pub.sendMessage('succeed_connect_program_database',
                            dao=self.program_dao)
            pub.sendMessage('request_retrieve_revisions')
        except NoSuchModuleError:
            _error_msg = ("RAMSTK does not currently support database dialect "
                          "{0:s}.".format(database['dialect']))
            pub.sendMessage('fail_connect_program_database',
                            error_message=_error_msg)
        except ArgumentError:
            _error_msg = (
                "The database URL {0:s} did not conform to the RFC 1738 "
                "standard and could not be opened.".format(
                    database['database']))
            pub.sendMessage('fail_connect_program_database',
                            error_message=_error_msg)
        except OperationalError:
            _error_msg = ("The database {0:s} does not exist.".format(
                database['database']))
            pub.sendMessage('fail_connect_program_database',
                            error_message=_error_msg)
        except DataAccessError as _error:
            pub.sendMessage('fail_connect_program_database',
                            error_message=_error.msg)

    def do_close_program(self) -> None:
        """Close the open RAMSTK Program database.

        :return: None
        :rtype: None
        :raises: AttributeError if a database isn't open.
        """
        try:
            self.program_dao.do_disconnect()
            pub.sendMessage('succeed_disconnect_program_database')
        except AttributeError:
            _error_msg = ("Not currently connected to a database.  Nothing to "
                          "close.")
            pub.sendMessage('fail_disconnect_program_database',
                            error_message=_error_msg)

    @staticmethod
    def do_save_program() -> None:
        """Save the open RAMSTK Program database.

        :return: None
        :rtype: None
        """
        pub.sendMessage('request_update_all_revisions')
        pub.sendMessage('request_update_all_functions')
        pub.sendMessage('request_update_all_requirements')
        pub.sendMessage('request_update_all_stakeholders')
        pub.sendMessage('request_update_all_hardware')
        pub.sendMessage('request_update_all_validation')
