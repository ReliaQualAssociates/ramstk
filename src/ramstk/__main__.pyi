# Standard Library Imports
from typing import Tuple

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration as RAMSTKSiteConfiguration
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.db import BaseDatabase as BaseDatabase
from ramstk.db.common import do_load_variables as do_load_variables
from ramstk.exim import Export as Export
from ramstk.exim import Import as Import
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.models import RAMSTKActionTable as RAMSTKActionTable
from ramstk.models import RAMSTKAllocationTable as RAMSTKAllocationTable
from ramstk.models import RAMSTKCauseTable as RAMSTKCauseTable
from ramstk.models import RAMSTKControlTable as RAMSTKControlTable
from ramstk.models import RAMSTKDesignElectricTable as RAMSTKDesignElectricTable
from ramstk.models import RAMSTKDesignMechanicTable as RAMSTKDesignMechanicTable
from ramstk.models import RAMSTKEnvironmentTable as RAMSTKEnvironmentTable
from ramstk.models import RAMSTKFailureDefinitionTable as RAMSTKFailureDefinitionTable
from ramstk.models import RAMSTKFMEAView as RAMSTKFMEAView
from ramstk.models import RAMSTKFunctionTable as RAMSTKFunctionTable
from ramstk.models import RAMSTKHardwareBoMView as RAMSTKHardwareBoMView
from ramstk.models import RAMSTKHardwareTable as RAMSTKHardwareTable
from ramstk.models import RAMSTKHazardTable as RAMSTKHazardTable
from ramstk.models import RAMSTKMechanismTable as RAMSTKMechanismTable
from ramstk.models import RAMSTKMILHDBK217FTable as RAMSTKMILHDBK217FTable
from ramstk.models import RAMSTKMissionPhaseTable as RAMSTKMissionPhaseTable
from ramstk.models import RAMSTKMissionTable as RAMSTKMissionTable
from ramstk.models import RAMSTKModeTable as RAMSTKModeTable
from ramstk.models import RAMSTKNSWCTable as RAMSTKNSWCTable
from ramstk.models import RAMSTKOpLoadTable as RAMSTKOpLoadTable
from ramstk.models import RAMSTKOpStressTable as RAMSTKOpStressTable
from ramstk.models import RAMSTKPoFView as RAMSTKPoFView
from ramstk.models import RAMSTKProgramDB as RAMSTKProgramDB
from ramstk.models import RAMSTKProgramInfoTable as RAMSTKProgramInfoTable
from ramstk.models import RAMSTKProgramStatusTable as RAMSTKProgramStatusTable
from ramstk.models import RAMSTKReliabilityTable as RAMSTKReliabilityTable
from ramstk.models import RAMSTKRequirementTable as RAMSTKRequirementTable
from ramstk.models import RAMSTKRevisionTable as RAMSTKRevisionTable
from ramstk.models import RAMSTKSimilarItemTable as RAMSTKSimilarItemTable
from ramstk.models import RAMSTKSiteInfoTable as RAMSTKSiteInfoTable
from ramstk.models import RAMSTKStakeholderTable as RAMSTKStakeholderTable
from ramstk.models import RAMSTKTestMethodTable as RAMSTKTestMethodTable
from ramstk.models import RAMSTKUsageProfileView as RAMSTKUsageProfileView
from ramstk.models import RAMSTKValidationTable as RAMSTKValidationTable
from ramstk.utilities import file_exists as file_exists
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import RAMSTKDesktop as RAMSTKDesktop
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKDatabaseSelect as RAMSTKDatabaseSelect

def do_connect_to_site_db(conn_info) -> BaseDatabase: ...
def do_first_run(configuration: RAMSTKSiteConfiguration) -> None: ...
def do_initialize_databases(
    configuration: RAMSTKUserConfiguration, site_db: BaseDatabase
) -> RAMSTKProgramDB: ...
def do_initialize_loggers(log_file: str, log_level: str) -> RAMSTKLogManager: ...
def do_read_site_configuration() -> RAMSTKSiteConfiguration: ...
def do_read_user_configuration() -> Tuple[
    RAMSTKUserConfiguration, RAMSTKLogManager
]: ...
def the_one_ring() -> None: ...
