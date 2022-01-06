# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.database.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK program Database model."""

# Standard Library Imports
import gettext
from datetime import date, datetime, timedelta
from typing import Dict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration
from ramstk.db import BaseDatabase, do_create_program_db
from ramstk.models import RAMSTKSiteInfoRecord
from ramstk.models.commondb import RAMSTKUser

_ = gettext.gettext


class RAMSTKCommonDB:
    """The RAMSTK common database manager class.

    The RAMSTK common database manager is responsible for managing all the analysis,
    data, and matrix managers associated with the RAMSTK common database that
    is currently open.  The attributes of a RAMSTK common database manager are:

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

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.site_configuration: RAMSTKSiteConfiguration = RAMSTKSiteConfiguration()
        self.common_dao: BaseDatabase = BaseDatabase()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_create_common, "request_create_common")
        # pub.subscribe(self.do_open_program, "request_open_program")
        # pub.subscribe(self.do_open_program, "succeed_create_program_database")
        # pub.subscribe(self.do_close_program, "request_close_program")
        # pub.subscribe(self.do_save_program, "request_update_program")

    def do_create_common(
        self,
        common_db: BaseDatabase,
        database: Dict[str, str],
        license_file: str,
    ) -> None:
        """Create a new RAMSTK Common database.

        :param common_db: the BaseDatabase() that is to be used to create and connect to
            the new RAMSTK common database.
        :param database: a dict containing the database connection arguments.
        :param license_file: the absolute path to the license file.
        :return: None
        :rtype: None
        """
        with open(
            self.site_configuration.RAMSTK_SITE_DIR
            + f'/{database["dialect"]}_common_db.sql',
            "r",
        ) as _sql_file:
            self.common_dao = common_db
            do_create_program_db(database, _sql_file)
            self.common_dao.do_connect(database)
            self.do_load_site_info(license_file)

            _yn = (
                input(_("Would you like to add a RAMSTK Administrator? ([y]/n): "))
                or "y"
            )
            if _yn.lower() == "y":
                self.do_add_administrator()

            self.common_dao.do_disconnect()

            pub.sendMessage(
                "succeed_create_common_database",
                common_db=self.common_dao,
                database=database,
            )

    def do_add_administrator(self) -> None:
        """Add a new administrator to the RAMSTK pool."""
        _user = RAMSTKUser()
        _user.user_id = 0
        _user.user_group_id = 1

        _user.user_lname = input(  # nosec
            _("Enter the RAMSTK Administrator's last name (surname): ")
        )
        _user.user_fname = input(  # nosec
            _("Enter the RAMSTK Administrator's first name (given name): ")
        )
        _user.user_email = input(  # nosec
            _("Enter the RAMSTK Administrator's e-mail address: ")
        )
        _user.user_phone = input(  # nosec
            _("Enter the RAMSTK Administrator's phone number: ")
        )

        self.common_dao.session.add(_user)
        self.common_dao.session.commit()

    def do_load_site_info(self, license_file: str) -> None:
        """Load the Site Information table.

        :param license_file: the absolute path to the license file.
        :return: None
        :rtype: None
        """
        _dic_site_info: Dict[str, Union[date, int, str]] = {
            "site_name": "DEMO",
            "product_key": "DEMO",
            "expire_on": date.today() + timedelta(days=30),
            "function_enabled": 1,
            "requirement_enabled": 1,
            "hardware_enabled": 1,
            "software_enabled": 0,
            "rcm_enabled": 0,
            "testing_enabled": 0,
            "incident_enabled": 0,
            "survival_enabled": 0,
            "vandv_enabled": 1,
            "hazard_enabled": 1,
            "stakeholder_enabled": 1,
            "allocation_enabled": 1,
            "similar_item_enabled": 1,
            "fmea_enabled": 1,
            "pof_enabled": 1,
            "rbd_enabled": 0,
            "fta_enabled": 0,
        }
        _site_id: int = -1

        try:
            with open(license_file, "r") as _license_file:
                _contents = _license_file.readlines()
                _site_id = int(_contents[0].strip("\n"))
                _dic_site_info["product_key"] = _contents[1].strip("\n")
                _dic_site_info["expire_on"] = datetime.strptime(
                    _contents[2].strip("\n"), "%Y-%m-%d"
                )
                _dic_site_info["function_enabled"] = int(_contents[3].strip("\n"))
                _dic_site_info["requirement_enabled"] = int(_contents[4].strip("\n"))
                _dic_site_info["hardware_enabled"] = int(_contents[5].strip("\n"))
                _dic_site_info["software_enabled"] = int(_contents[6].strip("\n"))
                _dic_site_info["rcm_enabled"] = int(_contents[7].strip("\n"))
                _dic_site_info["testing_enabled"] = int(_contents[8].strip("\n"))
                _dic_site_info["incident_enabled"] = int(_contents[9].strip("\n"))
                _dic_site_info["survival_enabled"] = int(_contents[10].strip("\n"))
                _dic_site_info["vandv_enabled"] = int(_contents[11].strip("\n"))
                _dic_site_info["hazard_enabled"] = int(_contents[12].strip("\n"))
                _dic_site_info["stakeholder_enabled"] = int(_contents[13].strip("\n"))
                _dic_site_info["allocation_enabled"] = int(_contents[14].strip("\n"))
                _dic_site_info["similar_item_enabled"] = int(_contents[15].strip("\n"))
                _dic_site_info["fmea_enabled"] = int(_contents[16].strip("\n"))
                _dic_site_info["pof_enabled"] = int(_contents[17].strip("\n"))
                _dic_site_info["rbd_enabled"] = int(_contents[18].strip("\n"))
                _dic_site_info["fta_enabled"] = int(_contents[19].strip("\n"))
                _dic_site_info["site_name"] = _contents[20].strip("\n")
        except IOError:
            _error_msg = (
                "Unable to read license key file.  Defaulting to a 30-day demo license."
            )
            pub.sendMessage("fail_read_license", error_message=_error_msg)

        _site_info = RAMSTKSiteInfoRecord()
        _site_info.site_id = _site_id
        _site_info.set_attributes(_dic_site_info)

        self.common_dao.session.add(_site_info)
        self.common_dao.session.commit()
