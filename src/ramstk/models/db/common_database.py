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
from typing import Dict, Tuple, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration, RAMSTKUserConfiguration

# RAMSTK Local Imports
from ..dbrecords import (
    RAMSTKCategoryRecord,
    RAMSTKFailureModeRecord,
    RAMSTKGroupRecord,
    RAMSTKHazardsRecord,
    RAMSTKLoadHistoryRecord,
    RAMSTKManufacturerRecord,
    RAMSTKMeasurementRecord,
    RAMSTKMethodRecord,
    RAMSTKModelRecord,
    RAMSTKRPNRecord,
    RAMSTKSiteInfoRecord,
    RAMSTKStakeholdersRecord,
    RAMSTKStatusRecord,
    RAMSTKSubCategoryRecord,
    RAMSTKTypeRecord,
    RAMSTKUserRecord,
)
from .basedatabase import BaseDatabase, do_create_program_db

_ = gettext.gettext


class RAMSTKCommonDB:
    """The RAMSTK common database manager model.

    The attributes of a RAMSTK common database manager are:

    :ivar dic_tables: a dict containing the instances of all the database table
        models this program database model is managing.
    :ivar site_configuration: the RAMSTKSiteConfiguration instance associated with
        this common database model.
    :ivar common_dao: the BaseDatabase() object that will connect to the
        RAMSTK common database.
    """

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTK common database model."""

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
        _user = RAMSTKUserRecord()
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

        user_configuration = self._do_load_action_categories(user_configuration)
        user_configuration = self._do_load_action_status(user_configuration)
        user_configuration = self._do_load_affinity_groups(user_configuration)
        user_configuration = self._do_load_damage_models(user_configuration)
        user_configuration = self._do_load_detection_methods(user_configuration)
        user_configuration = self._do_load_hardware_variables(user_configuration)
        user_configuration = self._do_load_hazards(user_configuration)
        user_configuration = self._do_load_incident_categories(user_configuration)
        user_configuration = self._do_load_incident_status(user_configuration)
        user_configuration = self._do_load_incident_types(user_configuration)
        user_configuration = self._do_load_load_history(user_configuration)
        user_configuration = self._do_load_manufacturers(user_configuration)
        user_configuration = self._do_load_measureable_parameters(user_configuration)
        user_configuration = self._do_load_measurement_units(user_configuration)
        user_configuration = self._do_load_requirement_types(user_configuration)
        user_configuration = self._do_load_rpn_detection(user_configuration)
        user_configuration = self._do_load_rpn_occurrence(user_configuration)
        user_configuration = self._do_load_rpn_severity(user_configuration)
        user_configuration = self._do_load_severity(user_configuration)
        user_configuration = self._do_load_stakeholders(user_configuration)
        user_configuration = self._do_load_users(user_configuration)
        user_configuration = self._do_load_validation_types(user_configuration)
        user_configuration = self._do_load_workgroups(user_configuration)

        pub.sendMessage(
            "do_log_info_msg",
            logger_name="INFO",
            message="Loaded global RAMSTK configuration variables.",
        )

        return user_configuration

    def _do_load_action_categories(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the action category dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKCategoryRecord)
            .filter(RAMSTKCategoryRecord.category_type == "action")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_ACTION_CATEGORY[_record.category_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["category_type"],
                _attributes["value"],
            )

        return user_configuration

    def _do_load_action_status(
        self,
        user_configuration: RAMSTKUserConfiguration,
    ) -> RAMSTKUserConfiguration:
        """Load the action status dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKStatusRecord)
            .filter(RAMSTKStatusRecord.status_type == "action")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_ACTION_STATUS[_record.status_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["status_type"],
            )

        return user_configuration

    def _do_load_affinity_groups(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the affinity group dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKGroupRecord)
            .filter(RAMSTKGroupRecord.group_type == "affinity")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_AFFINITY_GROUPS[_record.group_id] = (
                _attributes["description"],
                _attributes["group_type"],
            )

        return user_configuration

    def _do_load_damage_models(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the damage model dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKModelRecord)
            .filter(RAMSTKModelRecord.model_type == "damage")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_DAMAGE_MODELS[_record.model_id] = _attributes[
                "description"
            ]

        return user_configuration

    def _do_load_detection_methods(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RPN detection methods dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKMethodRecord)
            .filter(RAMSTKMethodRecord.method_type == "detection")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_DETECTION_METHODS[_record.method_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["method_type"],
            )

        return user_configuration

    def _do_load_failure_modes(
        self, category_id: int, subcategory_id: int
    ) -> Dict[int, Union[float, str]]:
        """Load dict of failure modes.

        :param category_id: the category ID for the failure modes to load.
        :param subcategory_id: the subcategory ID for the failure modes to load.
        :return: the dict of failures modes for the passed category ID, subcategory
            ID pair.
        :rtype: dict
        """
        return {
            _mode.mode_id: [  # type: ignore
                _mode.description,
                _mode.mode_ratio,
                _mode.source,
            ]
            for _mode in (
                self.common_dao.session.query(RAMSTKFailureModeRecord)
                .filter(RAMSTKFailureModeRecord.category_id == category_id)
                .filter(RAMSTKFailureModeRecord.subcategory_id == subcategory_id)
                .all()
            )
        }

    def _do_load_hardware_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load variables associated with hardware categories and failure modes.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKCategoryRecord)
            .filter(RAMSTKCategoryRecord.category_type == "hardware")
            .all()
        ):

            _subcats = {}
            user_configuration.RAMSTK_FAILURE_MODES[_record.category_id] = {}
            user_configuration.RAMSTK_STRESS_LIMITS[
                _record.category_id
            ] = self._do_load_stress_limits(_record)

            for _subcat in (
                self.common_dao.session.query(RAMSTKSubCategoryRecord)
                .filter(RAMSTKSubCategoryRecord.category_id == _record.category_id)
                .all()
            ):
                _subcats[_subcat.subcategory_id] = _subcat.description

                user_configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id
                ] = {}
                user_configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id
                ] = self._do_load_failure_modes(
                    _record.category_id, _subcat.subcategory_id
                )

            user_configuration.RAMSTK_CATEGORIES[
                _record.category_id
            ] = _record.description
            user_configuration.RAMSTK_SUBCATEGORIES[_record.category_id] = _subcats

        return user_configuration

    def _do_load_hazards(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the hazards dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in self.common_dao.session.query(RAMSTKHazardsRecord).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_HAZARDS[_record.hazard_id] = (
                _attributes["hazard_category"],
                _attributes["hazard_subcategory"],
            )

        return user_configuration

    def _do_load_incident_categories(
        self,
        user_configuration: RAMSTKUserConfiguration,
    ) -> RAMSTKUserConfiguration:
        """Load the incident category dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKCategoryRecord)
            .filter(RAMSTKCategoryRecord.category_type == "incident")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_INCIDENT_CATEGORY[_record.category_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["category_type"],
                _attributes["value"],
            )

        return user_configuration

    def _do_load_incident_status(
        self,
        user_configuration: RAMSTKUserConfiguration,
    ) -> RAMSTKUserConfiguration:
        """Load the incident status dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKStatusRecord)
            .filter(RAMSTKStatusRecord.status_type == "incident")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_INCIDENT_STATUS[_record.status_id] = (
                _attributes["name"],
                _attributes["description"],
                _attributes["status_type"],
            )

        return user_configuration

    def _do_load_incident_types(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load incident type dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKTypeRecord)
            .filter(RAMSTKTypeRecord.type_type == "incident")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_INCIDENT_TYPE[_record.type_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["type_type"],
            )

        return user_configuration

    def _do_load_load_history(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the load history dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in self.common_dao.session.query(RAMSTKLoadHistoryRecord).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_LOAD_HISTORY[_record.history_id] = _attributes[
                "description"
            ]

        return user_configuration

    def _do_load_manufacturers(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the manufacturer dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in self.common_dao.session.query(RAMSTKManufacturerRecord).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_MANUFACTURERS[_record.manufacturer_id] = (
                _attributes["description"],
                _attributes["location"],
                _attributes["cage_code"],
            )

        return user_configuration

    def _do_load_measureable_parameters(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the measureable parameters dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKMeasurementRecord)
            .filter(RAMSTKMeasurementRecord.measurement_type == "damage")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_MEASURABLE_PARAMETERS[_record.measurement_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["measurement_type"],
            )

        return user_configuration

    def _do_load_measurement_units(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the measurement units dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKMeasurementRecord)
            .filter(RAMSTKMeasurementRecord.measurement_type == "unit")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_MEASUREMENT_UNITS[_record.measurement_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["measurement_type"],
            )

        return user_configuration

    def _do_load_requirement_types(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the requirement type dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKTypeRecord)
            .filter(RAMSTKTypeRecord.type_type == "requirement")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_REQUIREMENT_TYPE[_record.type_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["type_type"],
            )

        return user_configuration

    def _do_load_rpn_detection(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RPN detection dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKRPNRecord)
            .filter(RAMSTKRPNRecord.rpn_type == "detection")
            .all()
        ):
            user_configuration.RAMSTK_RPN_DETECTION[
                _record.value
            ] = _record.get_attributes()

        return user_configuration

    def _do_load_rpn_occurrence(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RPN occurremce dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKRPNRecord)
            .filter(RAMSTKRPNRecord.rpn_type == "occurrence")
            .all()
        ):
            user_configuration.RAMSTK_RPN_OCCURRENCE[
                _record.value
            ] = _record.get_attributes()

        return user_configuration

    def _do_load_rpn_severity(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RPN severity dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKRPNRecord)
            .filter(RAMSTKRPNRecord.rpn_type == "severity")
            .all()
        ):
            user_configuration.RAMSTK_RPN_SEVERITY[
                _record.value
            ] = _record.get_attributes()

        return user_configuration

    def _do_load_stakeholders(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the stakeholders dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in self.common_dao.session.query(RAMSTKStakeholdersRecord).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_STAKEHOLDERS[
                _record.stakeholders_id
            ] = _attributes["stakeholder"]

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
            self.common_dao.session.query(RAMSTKCategoryRecord)
            .filter(RAMSTKCategoryRecord.category_type == "risk")
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

    @staticmethod
    def _do_load_stress_limits(
        record: RAMSTKCategoryRecord,
    ) -> Tuple[float, float, float, float, float, float, float, float, float, float]:
        """Load the electrical stress limits for hardware categories.

        :param record: the RAMSTKCategoryRecord with the stress limit information.
        :return: tuple of stress limits.
        :rtype: tuple
        """
        return (
            record.harsh_ir_limit,
            record.mild_ir_limit,
            record.harsh_pr_limit,
            record.mild_pr_limit,
            record.harsh_vr_limit,
            record.mild_vr_limit,
            record.harsh_deltat_limit,
            record.mild_deltat_limit,
            record.harsh_maxt_limit,
            record.mild_maxt_limit,
        )

    def _do_load_users(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTK user dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in self.common_dao.session.query(RAMSTKUserRecord).all():
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_USERS[_record.user_id] = (
                _attributes["user_lname"],
                _attributes["user_fname"],
                _attributes["user_email"],
                _attributes["user_phone"],
                _attributes["user_group_id"],
            )

        return user_configuration

    def _do_load_validation_types(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load validation types dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """

        for _record in (
            self.common_dao.session.query(RAMSTKTypeRecord)
            .filter(RAMSTKTypeRecord.type_type == "validation")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_VALIDATION_TYPE[_record.type_id] = (
                _attributes["code"],
                _attributes["description"],
                _attributes["type_type"],
            )

        return user_configuration

    def _do_load_workgroups(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration:
        """Load the RAMSTK workgroup dict.

        :param user_configuration: the RAMSTKUserConfiguration instance whose
            variable is to be loaded.
        :return: user_configuration
        :rtype: RAMSTKUserConfiguration
        """
        for _record in (
            self.common_dao.session.query(RAMSTKGroupRecord)
            .filter(RAMSTKGroupRecord.group_type == "workgroup")
            .all()
        ):
            _attributes = _record.get_attributes()
            user_configuration.RAMSTK_WORKGROUPS[_record.group_id] = (
                _attributes["description"],
                _attributes["group_type"],
            )

        return user_configuration
