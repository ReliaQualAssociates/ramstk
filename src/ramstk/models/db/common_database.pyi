# Standard Library Imports
import gettext
from typing import Dict, Tuple, Union

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration as RAMSTKSiteConfiguration
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.db import BaseDatabase as BaseDatabase
from ramstk.db import do_create_program_db as do_create_program_db
from ramstk.models.dbrecords import RAMSTKCategoryRecord as RAMSTKCategoryRecord
from ramstk.models.dbrecords import RAMSTKFailureModeRecord as RAMSTKFailureModeRecord
from ramstk.models.dbrecords import RAMSTKGroupRecord as RAMSTKGroupRecord
from ramstk.models.dbrecords import RAMSTKHazardsRecord as RAMSTKHazardsRecord
from ramstk.models.dbrecords import RAMSTKLoadHistoryRecord as RAMSTKLoadHistoryRecord
from ramstk.models.dbrecords import RAMSTKManufacturerRecord as RAMSTKManufacturerRecord
from ramstk.models.dbrecords import RAMSTKMeasurementRecord as RAMSTKMeasurementRecord
from ramstk.models.dbrecords import RAMSTKMethodRecord as RAMSTKMethodRecord
from ramstk.models.dbrecords import RAMSTKModelRecord as RAMSTKModelRecord
from ramstk.models.dbrecords import RAMSTKRPNRecord as RAMSTKRPNRecord
from ramstk.models.dbrecords import RAMSTKSiteInfoRecord as RAMSTKSiteInfoRecord
from ramstk.models.dbrecords import RAMSTKStakeholdersRecord as RAMSTKStakeholdersRecord
from ramstk.models.dbrecords import RAMSTKStatusRecord as RAMSTKStatusRecord
from ramstk.models.dbrecords import RAMSTKSubCategoryRecord as RAMSTKSubCategoryRecord
from ramstk.models.dbrecords import RAMSTKTypeRecord as RAMSTKTypeRecord
from ramstk.models.dbrecords import RAMSTKUserRecord as RAMSTKUserRecord

_ = gettext.gettext

class RAMSTKCommonDB:
    dic_tables: Dict[str, object]
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
    def _do_load_action_categories(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_action_status(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_affinity_groups(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_damage_models(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_detection_methods(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_failure_modes(
        self, category_id: int, subcategory_id: int
    ) -> Dict[int, Union[float, str]]: ...
    def _do_load_hardware_variables(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_hazards(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_incident_categories(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_incident_status(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_incident_types(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_load_history(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_manufacturers(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_measureable_parameters(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_measurement_units(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_requirement_types(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_rpn_detection(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_rpn_occurrence(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_rpn_severity(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_stakeholders(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_severity(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    @staticmethod
    def _do_load_stress_limits(
        record: RAMSTKCategoryRecord,
    ) -> Tuple[
        float, float, float, float, float, float, float, float, float, float
    ]: ...
    def _do_load_users(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_validation_types(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
    def _do_load_workgroups(
        self, user_configuration: RAMSTKUserConfiguration
    ) -> RAMSTKUserConfiguration: ...
