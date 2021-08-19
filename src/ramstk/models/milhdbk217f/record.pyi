# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKMilHdbk217FRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    A1: Any
    A2: Any
    B1: Any
    B2: Any
    C1: Any
    C2: Any
    lambdaBD: Any
    lambdaBP: Any
    lambdaCYC: Any
    lambdaEOS: Any
    piA: Any
    piC: Any
    piCD: Any
    piCF: Any
    piCR: Any
    piCV: Any
    piCYC: Any
    piE: Any
    piF: Any
    piI: Any
    piK: Any
    piL: Any
    piM: Any
    piMFG: Any
    piN: Any
    piNR: Any
    piP: Any
    piPT: Any
    piQ: Any
    piR: Any
    piS: Any
    piT: Any
    piTAPS: Any
    piU: Any
    piV: Any
    def get_attributes(self): ...
