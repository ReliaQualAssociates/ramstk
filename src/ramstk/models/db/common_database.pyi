# Standard Library Imports
import gettext
from typing import Dict

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration

# RAMSTK Local Imports
from ..dbrecords import RAMSTKSiteInfoRecord as RAMSTKSiteInfoRecord
from ..dbrecords import RAMSTKUserRecord as RAMSTKUserRecord
from .basedatabase import BaseDatabase as BaseDatabase

_ = gettext.gettext

class RAMSTKCommonDB(BaseDatabase):
    tables: Incomplete
    def __init__(self) -> None: ...
    def _do_add_administrator(self) -> None: ...
    def _do_create_database(
        self, database: Dict[str, str], sql_file: str, license_file: str
    ) -> None: ...
    def _do_load_site_info(self, license_file: str) -> None: ...
