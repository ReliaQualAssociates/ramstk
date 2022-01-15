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
from ramstk.configuration import RAMSTKSiteConfiguration, RAMSTKUserConfiguration
from ramstk.db import BaseDatabase, do_create_program_db
from ramstk.models import RAMSTKSiteInfoRecord
from ramstk.models.commondb import (
    RAMSTKRPN,
    RAMSTKCategory,
    RAMSTKFailureMode,
    RAMSTKGroup,
    RAMSTKHazards,
    RAMSTKLoadHistory,
    RAMSTKManufacturer,
    RAMSTKMeasurement,
    RAMSTKMethod,
    RAMSTKModel,
    RAMSTKStakeholders,
    RAMSTKStatus,
    RAMSTKSubCategory,
    RAMSTKType,
    RAMSTKUser,
)

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
        self.dic_tables: Dict[str, object] = {
            "options": object,
        }

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
            encoding="utf-8",
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
            with open(
                license_file,
                "r",
                encoding="UTF-8",
            ) as _license_file:
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

    def do_load_site_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTKUserConfiguration global variables from the site db.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        pub.sendMessage(
            "do_log_info_msg",
            logger_name="INFO",
            message="Loading global RAMSTK configuration variables.",
        )

        user_configuration = self._do_load_action_variables(user_configuration)
        user_configuration = self._do_load_hardware_variables(user_configuration)
        user_configuration = self._do_load_incident_variables(user_configuration)
        user_configuration = self._do_load_miscellaneous_variables(user_configuration)
        user_configuration = self._do_load_pof_variables(user_configuration)
        user_configuration = self._do_load_requirement_variables(user_configuration)
        user_configuration = self._do_load_rpn_variables(user_configuration)
        user_configuration = self._do_load_severity(user_configuration)
        user_configuration = self._do_load_user_workgroups(user_configuration)

        pub.sendMessage(
            "do_log_info_msg",
            logger_name="INFO",
            message="Loaded global RAMSTK configuration variables.",
        )

        return user_configuration

    def _do_load_action_variables(
        self,
        user_configuration: RAMSTKUserConfiguration,
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTK_ACTION_CATEGORY variable.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKCategory)
            .filter(RAMSTKCategory.category_type == "action")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_ACTION_CATEGORY[_record.category_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["category_type"],
                _attributes["value"],
            )
        for _record in (
            self.common_dao.session.query(RAMSTKStatus)
            .filter(RAMSTKStatus.status_type == "action")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_ACTION_STATUS[_record.status_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["status_type"],
            )

        return user_configuration

    def _do_load_hardware_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load variables associated with hardware categories and failure modes.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :param site_db: the RAMSTK Site Database to read the values of the
            global variables.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKCategory)
            .filter(RAMSTKCategory.category_type == "hardware")
            .all()
        ):

            _subcats = {}
            user_configuration.RAMSTK_FAILURE_MODES[_record.category_id] = {}
            user_configuration.RAMSTK_STRESS_LIMITS[_record.category_id] = (
                _record.harsh_ir_limit,
                _record.mild_ir_limit,
                _record.harsh_pr_limit,
                _record.mild_pr_limit,
                _record.harsh_vr_limit,
                _record.mild_vr_limit,
                _record.harsh_deltat_limit,
                _record.mild_deltat_limit,
                _record.harsh_maxt_limit,
                _record.mild_maxt_limit,
            )
            for _subcat in (
                self.common_dao.session.query(RAMSTKSubCategory)
                .filter(RAMSTKSubCategory.category_id == _record.category_id)
                .all()
            ):
                _subcats[_subcat.subcategory_id] = _subcat.description

                user_configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id
                ] = {}
                _modes = {_mode.mode_id: [
                        _mode.description,
                        _mode.mode_ratio,
                        _mode.source,
                    ] for _mode in (
                    self.common_dao.session.query(RAMSTKFailureMode)
                    .filter(RAMSTKFailureMode.category_id == _record.category_id)
                    .filter(RAMSTKFailureMode.subcategory_id == _subcat.subcategory_id)
                    .all()
                )}
                user_configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id
                ] = _modes

            user_configuration.RAMSTK_CATEGORIES[
                _record.category_id
            ] = _record.description
            user_configuration.RAMSTK_SUBCATEGORIES[_record.category_id] = _subcats

        return user_configuration

    def _do_load_incident_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTK_INCIDENT_CATEGORY variable.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKCategory)
            .filter(RAMSTKCategory.category_type == "incident")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_INCIDENT_CATEGORY[_record.category_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["category_type"],
                _attributes["value"],
            )
        for _record in (
            self.common_dao.session.query(RAMSTKStatus)
            .filter(RAMSTKStatus.status_type == "incident")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_INCIDENT_STATUS[_record.status_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["status_type"],
            )
        for _record in (
            self.common_dao.session.query(RAMSTKType)
            .filter(RAMSTKType.type_type == "incident")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_INCIDENT_TYPE[_record.type_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["type_type"],
            )

        return user_configuration

    def _do_load_miscellaneous_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load miscellaneous variables that don't fit in another grouping.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKMethod)
            .filter(RAMSTKMethod.method_type == "detection")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_DETECTION_METHODS[_record.method_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["method_type"],
            )
        for _record in self.common_dao.session.query(RAMSTKHazards).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_HAZARDS[_record.hazard_id] = (
                _attributes["hazard_category"],
                _attributes["hazard_subcategory"],
            )
        for _record in self.common_dao.session.query(RAMSTKManufacturer).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_MANUFACTURERS[_record.manufacturer_id] = (
                _attributes["description"],
                _attributes["location"],
                _attributes["cage_code"],
            )
        for _record in (
            self.common_dao.session.query(RAMSTKMeasurement)
            .filter(RAMSTKMeasurement.measurement_type == "unit")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_MEASUREMENT_UNITS[_record.measurement_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["measurement_type"],
            )
        for _record in (
            self.common_dao.session.query(RAMSTKType)
            .filter(RAMSTKType.type_type == "validation")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_VALIDATION_TYPE[_record.type_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["type_type"],
            )

        return user_configuration

    def _do_load_pof_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTK_DAMAGE_MODELS variable.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKModel)
            .filter(RAMSTKModel.model_type == "damage")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_DAMAGE_MODELS[_record.model_id] = _attributes[
                "description"
            ]
        for _record in self.common_dao.session.query(RAMSTKLoadHistory).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_LOAD_HISTORY[_record.history_id] = _attributes[
                "description"
            ]
        for _record in (
            self.common_dao.session.query(RAMSTKMeasurement)
            .filter(RAMSTKMeasurement.measurement_type == "damage")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_MEASURABLE_PARAMETERS[_record.measurement_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["measurement_type"],
            )

        return user_configuration

    def _do_load_requirement_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load variables related to requiremetents and stakeholders.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKGroup)
            .filter(RAMSTKGroup.group_type == "affinity")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_AFFINITY_GROUPS[_record.group_id] = (
                _attributes["description"],
                _attributes["group_type"],
            )
        for _record in (
            self.common_dao.session.query(RAMSTKType)
            .filter(RAMSTKType.type_type == "requirement")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_REQUIREMENT_TYPE[_record.type_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["type_type"],
            )
        for _record in self.common_dao.session.query(RAMSTKStakeholders).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_STAKEHOLDERS[
                _record.stakeholders_id
            ] = _attributes["stakeholder"]

        return user_configuration

    def _do_load_rpn_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RPN detection, occurremce, and severity variables.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKRPN)
            .filter(RAMSTKRPN.rpn_type == "detection")
            .all()
        ):
            user_configuration.RAMSTK_RPN_DETECTION[
                _record.value
            ] = _record.get_attributes()

        for _record in (
            self.common_dao.session.query(RAMSTKRPN)
            .filter(RAMSTKRPN.rpn_type == "occurrence")
            .all()
        ):
            user_configuration.RAMSTK_RPN_OCCURRENCE[
                _record.value
            ] = _record.get_attributes()

        for _record in (
            self.common_dao.session.query(RAMSTKRPN)
            .filter(RAMSTKRPN.rpn_type == "severity")
            .all()
        ):
            user_configuration.RAMSTK_RPN_SEVERITY[
                _record.value
            ] = _record.get_attributes()

        return user_configuration

    def _do_load_severity(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTK_SEVERITY variable.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKCategory)
            .filter(RAMSTKCategory.category_type == "risk")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_SEVERITY[_record.category_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["category_type"],
                _attributes["value"],
            )

        return user_configuration

    def _do_load_user_workgroups(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTK_USERS and RAMSTK_WORKGROUPS variables.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in self.common_dao.session.query(RAMSTKUser).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_USERS[_record.user_id] = (
                _attributes["user_lname"],
                _attributes["user_fname"],
                _attributes["user_email"],
                _attributes["user_phone"],
                _attributes["user_group_id"],
            )
        for _record in (
            self.common_dao.session.query(RAMSTKGroup)
            .filter(RAMSTKGroup.group_type == "workgroup")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_WORKGROUPS[_record.group_id] = (
                _attributes["description"],
                _attributes["group_type"],
            )

        return user_configuration
