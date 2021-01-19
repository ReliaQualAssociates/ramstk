# Standard Library Imports
from typing import Any, Tuple

# RAMSTK Package Imports
from ramstk import RAMSTKProgramManager as RAMSTKProgramManager
from ramstk.configuration import (
    RAMSTKSiteConfiguration as RAMSTKSiteConfiguration
)
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.controllers import amAllocation as amAllocation
from ramstk.controllers import amFMEA as amFMEA
from ramstk.controllers import amHardware as amHardware
from ramstk.controllers import amHazards as amHazards
from ramstk.controllers import amSimilarItem as amSimilarItem
from ramstk.controllers import amStakeholder as amStakeholder
from ramstk.controllers import amValidation as amValidation
from ramstk.controllers import dmAllocation as dmAllocation
from ramstk.controllers import dmFailureDefinition as dmFailureDefinition
from ramstk.controllers import dmFMEA as dmFMEA
from ramstk.controllers import dmFunction as dmFunction
from ramstk.controllers import dmHardware as dmHardware
from ramstk.controllers import dmHazards as dmHazards
from ramstk.controllers import dmOptions as dmOptions
from ramstk.controllers import dmPoF as dmPoF
from ramstk.controllers import dmPreferences as dmPreferences
from ramstk.controllers import dmProgramStatus as dmProgramStatus
from ramstk.controllers import dmRequirement as dmRequirement
from ramstk.controllers import dmRevision as dmRevision
from ramstk.controllers import dmSimilarItem as dmSimilarItem
from ramstk.controllers import dmStakeholder as dmStakeholder
from ramstk.controllers import dmUsageProfile as dmUsageProfile
from ramstk.controllers import dmValidation as dmValidation
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.db.common import do_load_variables as do_load_variables
from ramstk.exim import Export as Export
from ramstk.exim import Import as Import
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.utilities import file_exists as file_exists
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import RAMSTKDesktop as RAMSTKDesktop
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import (
    RAMSTKDatabaseSelect as RAMSTKDatabaseSelect
)

def do_connect_to_site_db(conn_info: Any) -> BaseDatabase:
    ...


def do_first_run(configuration: RAMSTKSiteConfiguration) -> None:
    ...


def do_initialize_loggers(log_file: str, log_level: str) -> RAMSTKLogManager:
    ...


def do_read_site_configuration() -> RAMSTKSiteConfiguration:
    ...


def do_read_user_configuration(
) -> Tuple[RAMSTKUserConfiguration, RAMSTKLogManager]:
    ...


def the_one_ring() -> None:
    ...
