# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKNSWCRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    Cac: Any
    Calt: Any
    Cb: Any
    Cbl: Any
    Cbt: Any
    Cbv: Any
    Cc: Any
    Ccf: Any
    Ccp: Any
    Ccs: Any
    Ccv: Any
    Ccw: Any
    Cd: Any
    Cdc: Any
    Cdl: Any
    Cdp: Any
    Cds: Any
    Cdt: Any
    Cdw: Any
    Cdy: Any
    Ce: Any
    Cf: Any
    Cg: Any
    Cga: Any
    Cgl: Any
    Cgp: Any
    Cgs: Any
    Cgt: Any
    Cgv: Any
    Ch: Any
    Ci: Any
    Ck: Any
    Cl: Any
    Clc: Any
    Cm: Any
    Cmu: Any
    Cn: Any
    Cnp: Any
    Cnw: Any
    Cp: Any
    Cpd: Any
    Cpf: Any
    Cpv: Any
    Cq: Any
    Cr: Any
    Crd: Any
    Cs: Any
    Csc: Any
    Csf: Any
    Cst: Any
    Csv: Any
    Csw: Any
    Csz: Any
    Ct: Any
    Cv: Any
    Cw: Any
    Cy: Any
    def get_attributes(self): ...
