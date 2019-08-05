# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.tests.configuration.test_siteconfiguration.py is part of The
#       RAMSTK Project
#
# All rights reserved.
"""Test class for the Site Configuration module algorithms and models."""

# Standard Library Imports
import glob
import sys
from os import environ, getenv

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration

try:
    VIRTUAL_ENV = glob.glob(environ['VIRTUAL_ENV'])[0]
except KeyError:
    if sys.platform == 'Linux':
        VIRTUAL_ENV = getenv('HOME') + '/.local'
    elif sys.platform == 'Windows':
        VIRTUAL_ENV = getenv('TEMP')
    else:
        print(("The {0:s} system platform is not "
               "supported.").format(sys.platform))
        sys.exit(1)


@pytest.mark.usefixtures('make_shibboly')
class TestCreateSiteConfiguration():
    """Class for testing the site configuration module."""
    def on_create_site_configuration(self):
        print(
            "\033[36m\nsucceed_create_site_configuration topic was broadcast.")

    @pytest.mark.unit
    def test_initialize_configuration(self):
        """ __init__() should create an instance of the site configuration class. """
        DUT = RAMSTKSiteConfiguration()

        assert isinstance(DUT, RAMSTKSiteConfiguration)
        assert DUT.RAMSTK_COM_INFO == {}
        assert DUT.RAMSTK_ACTION_CATEGORY == {}
        assert DUT.RAMSTK_ACTION_STATUS == {}
        assert DUT.RAMSTK_AFFINITY_GROUPS == {}
        assert DUT.RAMSTK_CATEGORIES == {}
        assert DUT.RAMSTK_DAMAGE_MODELS == {}
        assert DUT.RAMSTK_DETECTION_METHODS == {}
        assert DUT.RAMSTK_FAILURE_MODES == {}
        assert DUT.RAMSTK_HAZARDS == {}
        assert DUT.RAMSTK_INCIDENT_CATEGORY == {}
        assert DUT.RAMSTK_INCIDENT_STATUS == {}
        assert DUT.RAMSTK_INCIDENT_TYPE == {}
        assert DUT.RAMSTK_LOAD_HISTORY == {}
        assert DUT.RAMSTK_MANUFACTURERS == {}
        assert DUT.RAMSTK_MEASURABLE_PARAMETERS == {}
        assert DUT.RAMSTK_MEASUREMENT_UNITS == {}
        assert DUT.RAMSTK_MODULES == {}
        assert DUT.RAMSTK_PAGE_NUMBER == {}
        assert DUT.RAMSTK_REQUIREMENT_TYPE == {}
        assert DUT.RAMSTK_RPN_DETECTION == {}
        assert DUT.RAMSTK_RPN_OCCURRENCE == {}
        assert DUT.RAMSTK_RPN_SEVERITY == {}
        assert DUT.RAMSTK_SEVERITY == {}
        assert DUT.RAMSTK_STAKEHOLDERS == {}
        assert DUT.RAMSTK_STRESS_LIMITS == {}
        assert DUT.RAMSTK_SUBCATEGORIES == {}
        assert DUT.RAMSTK_USERS == {}
        assert DUT.RAMSTK_VALIDATION_TYPE == {}
        assert DUT.RAMSTK_WORKGROUPS == {}
        assert DUT.RAMSTK_COM_BACKEND == ''

    @pytest.mark.unit
    def test_create_site_configuration(self):
        """do_create_site_configuration() should broadcast the succcess message on success."""
        pub.subscribe(self.on_create_site_configuration,
                      'succeed_create_site_configuration')

        DUT = RAMSTKSiteConfiguration()

        DUT.RAMSTK_SITE_DIR = VIRTUAL_ENV + '/share/RAMSTK'
        DUT.RAMSTK_SITE_CONF = DUT.RAMSTK_SITE_DIR + '/RAMSTK.toml'

        assert DUT._do_create_site_configuration() is None

        pub.unsubscribe(self.on_create_site_configuration,
                        'succeed_create_site_configuration')


@pytest.mark.usefixtures('test_toml_site_configuration', 'make_shibboly', 'make_config_dir')
class TestGetterSetter():
    """Class for testing that the site configuration module can be read."""
    def on_fail_get_site_configuration(self, error_message):
        assert error_message == (
            "Failed to read Site configuration file "
            "{0:s}/share/RAMSTK/Sitetoml.toml."
        ).format(VIRTUAL_ENV)
        print("\033[35m\nfail_get_site_configuration topic was broadcast.")

    def on_succeed_set_site_configuration(self, configuration):
        assert isinstance(configuration, str)
        print("\033[36m\nsucceed_set_site_configuration topic was broadcast.")

    @pytest.mark.unit
    def test_get_site_configuration(self):
        """get_site_configuration() should broadcast the succcess message on success."""
        DUT = RAMSTKSiteConfiguration()
        DUT.RAMSTK_SITE_CONF = VIRTUAL_ENV + '/share/RAMSTK/Site.toml'

        assert DUT.get_site_configuration() is None
        assert DUT.RAMSTK_COM_BACKEND == 'sqlite'
        assert DUT.RAMSTK_COM_INFO["host"] == 'localhost'
        assert DUT.RAMSTK_COM_INFO["socket"] == '3306'
        assert DUT.RAMSTK_COM_INFO["database"] == ''
        assert DUT.RAMSTK_COM_INFO["user"] == 'johnny.tester'
        assert DUT.RAMSTK_COM_INFO["password"] == 'clear.text.password'

    @pytest.mark.unit
    def test_get_site_configuration_no_conf_file(self):
        """get_site_configuration() should broadcast the fail message when attempting to read a non-existent site configuration."""
        pub.subscribe(self.on_fail_get_site_configuration,
                      'fail_get_site_configuration')

        DUT = RAMSTKSiteConfiguration()
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + '/share/RAMSTK/Sitetoml.toml'

        assert DUT.get_site_configuration() is None

        pub.unsubscribe(self.on_fail_get_site_configuration,
                        'fail_get_site_configuration')

    @pytest.mark.unit
    def test_set_site_directories_no_home_config(self):
        """set_site_directories() should set directory paths to system directories when no $HOME configuration directory exists."""
        DUT = RAMSTKSiteConfiguration()
        DUT.RAMSTK_HOME_DIR = '/tmp/shibboly'

        assert DUT.set_site_directories() is None
        assert DUT.RAMSTK_SITE_DIR == VIRTUAL_ENV + "/share/RAMSTK"
        assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_SITE_DIR
        assert DUT.RAMSTK_DATA_DIR == DUT.RAMSTK_CONF_DIR + '/layouts'
        assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_CONF_DIR + '/icons'
        assert DUT.RAMSTK_LOG_DIR == '/var/log/RAMSTK'
        assert DUT.RAMSTK_SITE_CONF == DUT.RAMSTK_CONF_DIR + "/Site.conf"

    @pytest.mark.unit
    def test_set_site_directories_with_home_config(self):
        """set_site_directories() should set directory paths to $HOME directories when a $HOME configuration directory exists."""
        DUT = RAMSTKSiteConfiguration()
        DUT.RAMSTK_HOME_DIR = VIRTUAL_ENV

        assert DUT.set_site_directories() is None
        assert DUT.RAMSTK_SITE_DIR == VIRTUAL_ENV + "/share/RAMSTK"
        assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_HOME_DIR + "/.config/RAMSTK"
        assert DUT.RAMSTK_DATA_DIR == DUT.RAMSTK_HOME_DIR + "/.config/RAMSTK/layouts"
        assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_HOME_DIR + "/.config/RAMSTK/icons"
        assert DUT.RAMSTK_LOG_DIR == DUT.RAMSTK_HOME_DIR + "/.config/RAMSTK/logs"
        assert DUT.RAMSTK_SITE_CONF == DUT.RAMSTK_CONF_DIR + "/Site.conf"
