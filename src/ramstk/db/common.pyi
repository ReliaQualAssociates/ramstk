# Standard Library Imports
import gettext
from typing import Any, Dict, Tuple

# Third Party Imports
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.models.commondb import RAMSTKRPN as RAMSTKRPN
from ramstk.models.commondb import RAMSTKCategory as RAMSTKCategory
from ramstk.models.commondb import RAMSTKCondition as RAMSTKCondition
from ramstk.models.commondb import RAMSTKFailureMode as RAMSTKFailureMode
from ramstk.models.commondb import RAMSTKGroup as RAMSTKGroup
from ramstk.models.commondb import RAMSTKHazards as RAMSTKHazards
from ramstk.models.commondb import RAMSTKLoadHistory as RAMSTKLoadHistory
from ramstk.models.commondb import RAMSTKManufacturer as RAMSTKManufacturer
from ramstk.models.commondb import RAMSTKMeasurement as RAMSTKMeasurement
from ramstk.models.commondb import RAMSTKMethod as RAMSTKMethod
from ramstk.models.commondb import RAMSTKModel as RAMSTKModel
from ramstk.models.commondb import RAMSTKSiteInfo as RAMSTKSiteInfo
from ramstk.models.commondb import RAMSTKStakeholders as RAMSTKStakeholders
from ramstk.models.commondb import RAMSTKStatus as RAMSTKStatus
from ramstk.models.commondb import RAMSTKSubCategory as RAMSTKSubCategory
from ramstk.models.commondb import RAMSTKType as RAMSTKType
from ramstk.models.commondb import RAMSTKUser as RAMSTKUser

_ = gettext.gettext
RAMSTK_CATEGORIES: Any
RAMSTK_CONDITIONS: Any
RAMSTK_GROUPS: Any
RAMSTK_FAILURE_MODES: Any
RAMSTK_HAZARDS: Any
RAMSTK_HISTORIES: Any
RAMSTK_MANUFACTURERS: Any
RAMSTK_MEASUREMENTS: Any
RAMSTK_METHODS: Any
RAMSTK_MODELS: Any
RAMSTK_RPNS: Any
RAMSTK_STAKEHOLDERS: Any
RAMSTK_STATUSES: Any
RAMSTK_SUBCATEGORIES: Any
RAMSTK_TYPES: Dict[int, Tuple[str, str, str]]


def _load_fmea_tables(session: scoped_session) -> None:
    ...


def _load_hazard_analysis_tables(session: scoped_session) -> None:
    ...


def _load_incident_report_tables(session: scoped_session) -> None:
    ...


def _load_miscellaneous_tables(session: scoped_session) -> None:
    ...


def _load_pof_tables(session: scoped_session) -> None:
    ...


def _load_requirements_analysis_tables(session: scoped_session) -> None:
    ...


def _load_site_info(session: scoped_session) -> None:
    ...


def do_add_administrator(session: scoped_session) -> None:
    ...


def do_create_common_db(engine: Engine, session: scoped_session) -> None:
    ...


def do_make_commondb_tables(engine: Engine) -> None:
    ...


def _do_load_action_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_hardware_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_incident_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_miscellaneous_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_pof_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_requirement_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_rpn_variables(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_severity(site_db: BaseDatabase,
                      user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def _do_load_user_workgroups(
        site_db: BaseDatabase,
        user_configuration: RAMSTKUserConfiguration) -> None:
    ...


def do_load_variables(site_db: BaseDatabase,
                      user_configuration: RAMSTKUserConfiguration) -> None:
    ...
