# Standard Library Imports
import gettext
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration as RAMSTKSiteConfiguration
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.db import BaseDatabase as BaseDatabase
from ramstk.db import do_create_program_db as do_create_program_db
from ramstk.models import RAMSTKCategoryRecord as RAMSTKCategoryRecord
from ramstk.models import RAMSTKSiteInfoRecord as RAMSTKSiteInfoRecord
from ramstk.models import RAMSTKSubCategoryRecord as RAMSTKSubCategoryRecord
from ramstk.models.commondb import RAMSTKRPN as RAMSTKRPN
from ramstk.models.commondb import RAMSTKFailureMode as RAMSTKFailureMode
from ramstk.models.commondb import RAMSTKGroup as RAMSTKGroup
from ramstk.models.commondb import RAMSTKHazards as RAMSTKHazards
from ramstk.models.commondb import RAMSTKLoadHistory as RAMSTKLoadHistory
from ramstk.models.commondb import RAMSTKManufacturer as RAMSTKManufacturer
from ramstk.models.commondb import RAMSTKMeasurement as RAMSTKMeasurement
from ramstk.models.commondb import RAMSTKMethod as RAMSTKMethod
from ramstk.models.commondb import RAMSTKModel as RAMSTKModel
from ramstk.models.commondb import RAMSTKStakeholders as RAMSTKStakeholders
from ramstk.models.commondb import RAMSTKStatus as RAMSTKStatus
from ramstk.models.commondb import RAMSTKType as RAMSTKType
from ramstk.models.commondb import RAMSTKUser as RAMSTKUser

_ = gettext.gettext

class RAMSTKCommonDB:
    site_configuration: RAMSTKSiteConfiguration
    common_dao: BaseDatabase
    def __init__(self) -> None: ...
    def do_create_common(
        self, common_db: BaseDatabase, database: Dict[str, str], license_file: str
    ) -> None: ...
    def do_add_administrator(self) -> None: ...
    def do_load_site_info(self, license_file: str) -> None: ...
    def do_load_site_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_action_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_hardware_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_incident_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_miscellaneous_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_pof_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_requirement_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_rpn_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_severity(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_user_workgroups(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
