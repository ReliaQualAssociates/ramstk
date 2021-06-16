# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.environment.environment_integration_test.py is part
#       of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Environment module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmEnvironment


class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            'do_insert: Database error when attempting to add a record.  '
            'Database returned:\n\tKey (fld_revision_id)=(4) is not present '
            'in table "ramstk_revision".')
        print("\033[35m\nfail_insert_environment topic was broadcast")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        pub.subscribe(self.on_fail_insert_no_revision,
                      'fail_insert_environment')

        DUT = dmEnvironment()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 4
        DUT._do_insert_environment(1)

        pub.unsubscribe(self.on_fail_insert_no_revision,
                        'fail_insert_environment')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data['environment'].name == (
            'Big test environment')
        print("\033[36m\nsucceed_update_environment topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for environment '
            'ID 1 was the wrong type.')
        print("\033[35m\nfail_update_usage_profile topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update_usage_profile() should broadcast the succeed message on
        success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_environment')

        DUT = dmEnvironment()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _environment = DUT.do_select(1, table='environment')
        _environment.name = 'Big test environment'

        DUT.do_update(1, table='environment')

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_environment')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_usage_profile() should broadcast the succeed message on
        success."""
        DUT = dmEnvironment()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_update_all_environments')

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_environment')

        DUT = dmEnvironment()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _environment = DUT.do_select(1, table='environment')
        _environment.name = {1: 2}

        DUT.do_update(1, table='environment')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_environment')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        DUT = dmEnvironment()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _environment = DUT.do_select(1, table='environment')
        _environment.name = {1: 2}

        DUT.do_update(0, table='environment')