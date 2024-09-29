# -*- coding: utf-8 -*-
#
#       ramstk.models.db.common_database.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK common database model."""

# Standard Library Imports
import gettext
from datetime import date, datetime, timedelta
from typing import Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Local Imports
from ..dbrecords import RAMSTKSiteInfoRecord, RAMSTKUserRecord
from .basedatabase import BaseDatabase

_ = gettext.gettext


class RAMSTKCommonDB(BaseDatabase):
    """The RAMSTK common database manager model.

    The attributes of a RAMSTK common database manager are:

    :ivar tables: a dict containing the instances of all the database table
        models this program database model is managing.
    """

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTK common database model."""
        super().__init__()

        # Initialize public dictionary attributes.
        self.tables: Dict[str, object] = {
            "options": object,
        }

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_create_database, "request_create_common")

    def _do_add_administrator(self) -> None:
        """Add a new administrator to the RAMSTK pool."""
        _user = RAMSTKUserRecord()
        _user.user_id = 0
        _user.user_group_id = 1

        _user.user_lname = input(
            _("Enter the RAMSTK Administrator's last name (surname): ")
        )
        _user.user_fname = input(
            _("Enter the RAMSTK Administrator's first name (given name): ")
        )
        _user.user_email = input(_("Enter the RAMSTK Administrator's e-mail address: "))
        _user.user_phone = input(_("Enter the RAMSTK Administrator's phone number: "))

        self.session.add(_user)
        self.session.commit()

    def _do_create_database(
        self, database: Dict[str, str], sql_file: str, license_file: str
    ) -> None:
        """Create a new RAMSTK Common database.

        :param database: Dictionary with database connection arguments.
        :param sql_file: Path to the SQL file containing the SQL statements for creating the database.
        :param license_file: Path to the license file.
        :return: None
        """
        self.do_create_database(database, sql_file)
        self._do_load_site_info(license_file)

        _yn: str = (
            input(_("Would you like to add a RAMSTK Administrator? ([y]/n): ")) or "y"
        )
        if _yn.lower() == "y":
            self._do_add_administrator()

        self.do_disconnect()

        pub.sendMessage(
            "succeed_create_common_database",
            common_db=self,
            database=database,
        )

    def _do_load_site_info(self, license_file: str) -> None:
        """Load the Site Information table.

        :param license_file: Path to the license file.
        :return: None
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
            with open(license_file, "r", encoding="UTF-8") as _license_file:
                _contents: List[str] = _license_file.readlines()
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
            _error_msg: str = (
                "Unable to read license key file.  Defaulting to a 30-day demo license."
            )
            pub.sendMessage("fail_read_license", error_message=_error_msg)

        _site_info = RAMSTKSiteInfoRecord()
        _site_info.site_id = _site_id
        _site_info.set_attributes(_dic_site_info)

        self.session.add(_site_info)
        self.session.commit()
