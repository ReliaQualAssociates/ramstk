# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name, too-many-public-methods
# -*- coding: utf-8 -*-
#
#       ramstk.tests.test_ramstk.py is part of The RAMSTK Project
#
# All rights reserved.
"""This is the test class for the RAMSTK module algorithms and models."""

# Standard Library Imports
import os

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.ramstk import RAMSTKProgramManager


@pytest.mark.usefixtures('make_home_config_dir', 'test_program_dao',
                         'test_toml_user_configuration')
class TestProgramManager():
    """Test class for the RAMSTK Program Manager."""
    def on_succeed_open_program(self, dao):
        assert isinstance(dao, BaseDatabase)
        print("\033[36m\nsucceed_connect_program_database topic was broadcast")

    def on_fail_open_program_bad_url(self, error_message):
        assert error_message == ('The database URL /bad_database_url.ramstk '
                                 'did not conform to the RFC 1738 standard '
                                 'and could not be opened.')
        print("\033[35m\nfail_connect_program_database topic was broadcast.")

    def on_fail_open_program_unknown_dialect(self, error_message):
        assert error_message == ('RAMSTK does not currently support database '
                                 'dialect http.')
        print("\033[35m\nfail_connect_program_database topic was broadcast.")

    def on_fail_open_program_non_string_url(self, error_message):
        assert error_message == ('The URL 8742.11 for the database was not a '
                                 'string.')
        print("\033[35m\nfail_connect_program_database topic was broadcast.")

    def on_succeed_close_program(self):
        print(
            "\033[36m\nsucceed_disconnect_program_database topic was broadcast"
        )

    def on_fail_close_program(self, error_message):
        assert error_message == ('Not currently connected to a database.  '
                                 'Nothing to close.')
        print("\033[35m\nfail_disconnect_program_database topic was broadcast")

    def on_request_update_revision(self):
        print("\033[36m\nrequest_update_all_revisions topic was broadcast")

    def on_request_update_function(self):
        print("\033[36mrequest_update_all_functions topic was broadcast")

    def on_request_update_requirement(self):
        print("\033[36mrequest_update_all_requirements topic was broadcast")

    def on_request_update_stakeholder(self):
        print("\033[36mrequest_update_all_stakeholders topic was broadcast")

    def on_request_update_hardware(self):
        print("\033[36mrequest_update_all_hardware topic was broadcast")

    def on_request_update_validation(self):
        print("\033[36mrequest_update_all_validation topic was broadcast")

    def on_succeed_create_program(self, program_db, database):
        assert isinstance(program_db, BaseDatabase)
        assert database == '/tmp/_ramstk_program_db.ramstk'
        print("\033[36m\nsucceed_create_program_database topic was broadcast")

    @pytest.mark.unit
    def test_create_program_manager(self):
        """__init__() should create an instance of the RAMSTK program manager."""
        DUT = RAMSTKProgramManager()

        assert isinstance(DUT, RAMSTKProgramManager)
        assert isinstance(DUT.dic_managers, dict)
        assert DUT.dic_managers['revision'] == {'data': None}
        assert DUT.dic_managers['function'] == {'analysis': None, 'data': None}
        assert DUT.dic_managers['ffmea'] == {'analysis': None, 'data': None}
        assert DUT.dic_managers['requirement'] == {
            'data': None,
            'matrix': None
        }
        assert DUT.dic_managers['stakeholder'] == {
            'analysis': None,
            'data': None
        }
        assert DUT.dic_managers['hardware'] == {
            'analysis': None,
            'data': None,
            'matrix': None
        }
        assert DUT.dic_managers['fmea'] == {'analysis': None, 'data': None}
        assert DUT.dic_managers['pof'] == {'data': None}
        assert DUT.dic_managers['validation'] == {
            'analysis': None,
            'data': None,
            'matrix': None
        }
        assert DUT.dic_managers['options'] == {'data': None}
        assert DUT.program_dao is None
        assert pub.isSubscribed(DUT.do_create_program,
                                'request_create_program')
        assert pub.isSubscribed(DUT.do_open_program, 'request_open_program')
        assert pub.isSubscribed(DUT.do_close_program, 'request_close_program')
        assert pub.isSubscribed(DUT.do_save_program, 'request_update_program')

    @pytest.mark.unit
    def test_do_open_program(self, test_program_dao):
        """do_open_program() should connect to the test program database and broadcast the success message."""
        pub.subscribe(self.on_succeed_open_program,
                      'succeed_connect_program_database')

        _database = test_program_dao.database

        DUT = RAMSTKProgramManager()
        DUT.do_open_program(BaseDatabase(), _database)

        assert DUT.program_dao.database == _database

        pub.unsubscribe(self.on_succeed_open_program,
                        'succeed_connect_program_database')

    @pytest.mark.unit
    def test_do_open_program_bad_url(self):
        """do_open_program() should broadcast the fail message when attempting to open a bad URL."""
        pub.subscribe(self.on_fail_open_program_bad_url,
                      'fail_connect_program_database')

        DUT = RAMSTKProgramManager()
        DUT.do_open_program(BaseDatabase(), '/bad_database_url.ramstk')

        pub.unsubscribe(self.on_fail_open_program_bad_url,
                        'fail_connect_program_database')

    @pytest.mark.unit
    def test_do_open_program_unknown_dialect(self):
        """do_open_program() should broadcast the fail message when attempting to open a database of unsupported dialect."""
        pub.subscribe(self.on_fail_open_program_unknown_dialect,
                      'fail_connect_program_database')

        DUT = RAMSTKProgramManager()
        DUT.do_open_program(BaseDatabase(),
                            'http:///www.bad_database_dialect.com')

        pub.unsubscribe(self.on_fail_open_program_unknown_dialect,
                        'fail_connect_program_database')

    @pytest.mark.unit
    def test_do_open_program_non_string_url(self):
        """do_open_program() should broadcast the fail message when attempting to open a non-string URL."""
        pub.subscribe(self.on_fail_open_program_non_string_url,
                      'fail_connect_program_database')

        DUT = RAMSTKProgramManager()

        with pytest.raises(AttributeError):
            DUT.do_open_program(BaseDatabase(), 8742.11)

        pub.unsubscribe(self.on_fail_open_program_non_string_url,
                        'fail_connect_program_database')

    @pytest.mark.unit
    def test_do_close_program(self, test_program_dao):
        """do_close_program() should disconnect from the test program database and broadcast the success message."""
        pub.subscribe(self.on_succeed_close_program,
                      'succeed_disconnect_program_database')

        _database = test_program_dao.database

        DUT = RAMSTKProgramManager()
        DUT.do_open_program(BaseDatabase(), _database)
        DUT.do_close_program()

        assert DUT.program_dao.session is None
        assert DUT.program_dao.database == ''

        pub.unsubscribe(self.on_succeed_close_program,
                        'succeed_disconnect_program_database')

    @pytest.mark.unit
    def test_do_close_program_none_open(self):
        """do_close_program() should broadcast the fail message if it attempts to close a database when not connected."""
        pub.subscribe(self.on_fail_close_program,
                      'fail_disconnect_program_database')

        DUT = RAMSTKProgramManager()
        DUT.do_close_program()

        assert DUT.program_dao is None

        pub.unsubscribe(self.on_fail_close_program,
                        'fail_disconnect_program_database')

    @pytest.mark.unit
    def test_save_program(self, test_program_dao):
        """do_save_program() should cause all workstream modules to execute their save_all() method."""
        pub.subscribe(self.on_request_update_revision,
                      'request_update_all_revisions')
        pub.subscribe(self.on_request_update_function,
                      'request_update_all_functions')
        pub.subscribe(self.on_request_update_requirement,
                      'request_update_all_requirements')
        pub.subscribe(self.on_request_update_stakeholder,
                      'request_update_all_stakeholders')
        pub.subscribe(self.on_request_update_hardware,
                      'request_update_all_hardware')
        pub.subscribe(self.on_request_update_validation,
                      'request_update_all_validation')

        _database = test_program_dao.database

        DUT = RAMSTKProgramManager()
        DUT.do_open_program(BaseDatabase(), _database)
        DUT.do_save_program()

        assert DUT.program_dao.database == _database

        pub.unsubscribe(self.on_request_update_revision,
                        'request_update_all_revisions')
        pub.unsubscribe(self.on_request_update_function,
                        'request_update_all_functions')
        pub.unsubscribe(self.on_request_update_requirement,
                        'request_update_all_requirements')
        pub.unsubscribe(self.on_request_update_stakeholder,
                        'request_update_all_stakeholders')
        pub.unsubscribe(self.on_request_update_hardware,
                        'request_update_all_hardware')
        pub.unsubscribe(self.on_request_update_validation,
                        'request_update_all_validation')

    @pytest.mark.unit
    def test_do_create_program(self, test_toml_user_configuration):
        """do_create_program() should broadcast the success message if it attempts to close a database when not connected."""
        pub.subscribe(self.on_succeed_create_program,
                      'succeed_create_program_database')

        _program_db = BaseDatabase()

        DUT = RAMSTKProgramManager()
        DUT.user_configuration = test_toml_user_configuration
        DUT.do_create_program(_program_db, '/tmp/_ramstk_program_db.ramstk')

        assert os.path.exists('/tmp/_ramstk_program_db.ramstk')

        pub.unsubscribe(self.on_succeed_create_program,
                        'succeed_create_program_database')

        os.remove('/tmp/_ramstk_program_db.ramstk')
