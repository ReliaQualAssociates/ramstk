# -*- coding: utf-8 -*-
#
#       ramstk.ramstk.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""This is the RAMSTK program manager."""

# Standard Library Imports
import re
from typing import Dict, TextIO

# Third Party Imports
from pubsub import pub
from sqlalchemy.exc import ArgumentError, NoSuchModuleError

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase


class RAMSTKProgramManager:
    """
    The RAMSTK program manager class.

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
        """
        Initialize an instance of the RAMSTK program manager.

        :param user_configuration: the RAMSTKUserConfiguration() instance.
        :type user_configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_managers: Dict[str, Dict[str, object]] = {
            'revision': {
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
                'data': None,
                'matrix': None
            },
            'stakeholder': {
                'analysis': None,
                'data': None
            },
            'hardware': {
                'analysis': None,
                'data': None,
                'matrix': None
            },
            'fmea': {
                'analysis': None,
                'data': None
            },
            'pof': {
                'data': None
            },
            'validation': {
                'analysis': None,
                'data': None,
                'matrix': None
            },
            'options': {
                'data': None
            }
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.user_configuration: RAMSTKUserConfiguration = None
        self.program_dao: BaseDatabase = None

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_create_program, 'request_create_program')
        pub.subscribe(self.do_open_program, 'request_open_program')
        pub.subscribe(self.do_open_program, 'succeed_create_program_database')
        pub.subscribe(self.do_close_program, 'request_close_program')
        pub.subscribe(self.do_save_program, 'request_update_program')

    def do_create_program(self, program_db: BaseDatabase,
                          database: TextIO) -> None:
        """
        Create a new RAMSTK Program database.

        :param program_db: the BaseDatabase() that is to be used to create and
            connect to the new RAMSTK program database.
        :type program_db: :class:`ramstk.db.base.BaseDatabase`
        :param str database: the RFC1738 URL path to the database to create and
            connect to.
        :return: None
        :rtype: None
        """
        _sql_file = open(
            self.user_configuration.RAMSTK_CONF_DIR + '/sqlite_program_db.sql',
            'r')
        self.program_dao = program_db
        self.program_dao.do_create_program_db(database, _sql_file)
        pub.sendMessage('succeed_create_program_database',
                        program_db=self.program_dao,
                        database=database)

    def do_open_program(self, program_db: BaseDatabase, database: str) -> None:
        """
        Open an RAMSTK Program database for analyses.

        :param program_dao: the BaseDatabase() that is to be used to create and
            connect to the new RAMSTK program database.
        :type program_dao: :class:`ramstk.db.base.BaseDatabase`
        :param str database: the RFC1738 URL path to the database to create and
            connect to.
        :return: None
        :rtype: None
        """
        try:
            self.program_dao = program_db
            self.program_dao.do_connect(database)
            pub.sendMessage('succeed_connect_program_database',
                            dao=self.program_dao)
            pub.sendMessage('request_retrieve_revisions')
        except NoSuchModuleError:
            _d = re.search('://', database)
            _dialect = database[:_d.start(0)]
            _error_msg = ("RAMSTK does not currently support database dialect "
                          "{0:s}.".format(_dialect))
            pub.sendMessage('fail_connect_program_database',
                            error_message=_error_msg)
        except ArgumentError:
            _error_msg = (
                "The database URL {0:s} did not conform to the "
                "RFC 1738 standard and could not be opened.".format(database))
            pub.sendMessage('fail_connect_program_database',
                            error_message=_error_msg)

    def do_close_program(self) -> None:
        """
        Close the open RAMSTK Program database.

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
        """
        Save the open RAMSTK Program database.

        :return: None
        :rtype: None
        """
        pub.sendMessage('request_update_all_revisions')
        pub.sendMessage('request_update_all_functions')
        pub.sendMessage('request_update_all_requirements')
        pub.sendMessage('request_update_all_stakeholders')
        pub.sendMessage('request_update_all_hardware')
        pub.sendMessage('request_update_all_validation')
