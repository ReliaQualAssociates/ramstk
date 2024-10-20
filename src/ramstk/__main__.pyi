# Standard Library Imports
from typing import Dict, List, Tuple, Union

# Third Party Imports
from sqlalchemy import Select as Select

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration as RAMSTKSiteConfiguration
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.exim import Export as Export
from ramstk.exim import Import as Import
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.models.db import BaseDatabase as BaseDatabase
from ramstk.models.db import RAMSTKCommonDB as RAMSTKCommonDB
from ramstk.models.db import RAMSTKProgramDB as RAMSTKProgramDB
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
from ramstk.models.dbrecords import RAMSTKStakeholdersRecord as RAMSTKStakeholdersRecord
from ramstk.models.dbrecords import RAMSTKStatusRecord as RAMSTKStatusRecord
from ramstk.models.dbrecords import RAMSTKSubCategoryRecord as RAMSTKSubCategoryRecord
from ramstk.models.dbrecords import RAMSTKTypeRecord as RAMSTKTypeRecord
from ramstk.models.dbrecords import RAMSTKUserRecord as RAMSTKUserRecord
from ramstk.models.dbtables import RAMSTKActionTable as RAMSTKActionTable
from ramstk.models.dbtables import RAMSTKAllocationTable as RAMSTKAllocationTable
from ramstk.models.dbtables import RAMSTKCauseTable as RAMSTKCauseTable
from ramstk.models.dbtables import RAMSTKControlTable as RAMSTKControlTable
from ramstk.models.dbtables import (
    RAMSTKDesignElectricTable as RAMSTKDesignElectricTable,
)
from ramstk.models.dbtables import (
    RAMSTKDesignMechanicTable as RAMSTKDesignMechanicTable,
)
from ramstk.models.dbtables import RAMSTKEnvironmentTable as RAMSTKEnvironmentTable
from ramstk.models.dbtables import (
    RAMSTKFailureDefinitionTable as RAMSTKFailureDefinitionTable,
)
from ramstk.models.dbtables import RAMSTKFunctionTable as RAMSTKFunctionTable
from ramstk.models.dbtables import RAMSTKHardwareTable as RAMSTKHardwareTable
from ramstk.models.dbtables import RAMSTKHazardTable as RAMSTKHazardTable
from ramstk.models.dbtables import RAMSTKMechanismTable as RAMSTKMechanismTable
from ramstk.models.dbtables import RAMSTKMILHDBK217FTable as RAMSTKMILHDBK217FTable
from ramstk.models.dbtables import RAMSTKMissionPhaseTable as RAMSTKMissionPhaseTable
from ramstk.models.dbtables import RAMSTKMissionTable as RAMSTKMissionTable
from ramstk.models.dbtables import RAMSTKModeTable as RAMSTKModeTable
from ramstk.models.dbtables import RAMSTKNSWCTable as RAMSTKNSWCTable
from ramstk.models.dbtables import RAMSTKOpLoadTable as RAMSTKOpLoadTable
from ramstk.models.dbtables import RAMSTKOpStressTable as RAMSTKOpStressTable
from ramstk.models.dbtables import RAMSTKProgramInfoTable as RAMSTKProgramInfoTable
from ramstk.models.dbtables import RAMSTKProgramStatusTable as RAMSTKProgramStatusTable
from ramstk.models.dbtables import RAMSTKReliabilityTable as RAMSTKReliabilityTable
from ramstk.models.dbtables import RAMSTKRequirementTable as RAMSTKRequirementTable
from ramstk.models.dbtables import RAMSTKRevisionTable as RAMSTKRevisionTable
from ramstk.models.dbtables import RAMSTKSimilarItemTable as RAMSTKSimilarItemTable
from ramstk.models.dbtables import RAMSTKSiteInfoTable as RAMSTKSiteInfoTable
from ramstk.models.dbtables import RAMSTKStakeholderTable as RAMSTKStakeholderTable
from ramstk.models.dbtables import RAMSTKTestMethodTable as RAMSTKTestMethodTable
from ramstk.models.dbtables import RAMSTKValidationTable as RAMSTKValidationTable
from ramstk.models.dbviews import RAMSTKFMEAView as RAMSTKFMEAView
from ramstk.models.dbviews import RAMSTKHardwareBoMView as RAMSTKHardwareBoMView
from ramstk.models.dbviews import RAMSTKPoFView as RAMSTKPoFView
from ramstk.models.dbviews import RAMSTKUsageProfileView as RAMSTKUsageProfileView
from ramstk.utilities import file_exists as file_exists
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import RAMSTKDesktop as RAMSTKDesktop
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKDatabaseSelect as RAMSTKDatabaseSelect

def do_connect_to_site_db(conn_info) -> RAMSTKCommonDB: ...
def do_first_run(configuration: RAMSTKSiteConfiguration) -> None: ...
def do_initialize_databases(
    configuration: RAMSTKUserConfiguration, site_db: RAMSTKCommonDB
) -> Tuple[RAMSTKProgramDB, RAMSTKCommonDB]: ...
def do_initialize_loggers(log_file: str, log_level: str) -> RAMSTKLogManager: ...
def do_load_configuration_list(
    config_list: (
        List[str]
        | Dict[
            int,
            Tuple[float, float, float, float, float, float, float, float, float, float],
        ]
    ),
    database: BaseDatabase,
    query: Select,
    key_column: str,
    fields: List[str],
) -> None: ...
def do_load_failure_modes(
    database: RAMSTKCommonDB, category_id: int, subcategory_id: int
) -> Dict[int, Union[float, str]]: ...
def do_read_site_configuration() -> RAMSTKSiteConfiguration: ...
def do_read_user_configuration() -> (
    Tuple[RAMSTKUserConfiguration, RAMSTKLogManager]
): ...
def the_one_ring() -> None: ...
