# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKNSWCRecord


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _nswc_1 = RAMSTKNSWCRecord()
    _nswc_1.revision_id = 1
    _nswc_1.hardware_id = 1
    _nswc_1.Cac = 0.0
    _nswc_1.Calt = 0.0
    _nswc_1.Cb = 0.0
    _nswc_1.Cbl = 0.0
    _nswc_1.Cbt = 0.0
    _nswc_1.Cbv = 0.0
    _nswc_1.Cc = 0.0
    _nswc_1.Ccf = 0.0
    _nswc_1.Ccp = 0.0
    _nswc_1.Ccs = 0.0
    _nswc_1.Ccv = 0.0
    _nswc_1.Ccw = 0.0
    _nswc_1.Cd = 0.0
    _nswc_1.Cdc = 0.0
    _nswc_1.Cdl = 0.0
    _nswc_1.Cdp = 0.0
    _nswc_1.Cds = 0.0
    _nswc_1.Cdt = 0.0
    _nswc_1.Cdw = 0.0
    _nswc_1.Cdy = 0.0
    _nswc_1.Ce = 0.0
    _nswc_1.Cf = 0.0
    _nswc_1.Cg = 0.0
    _nswc_1.Cga = 0.0
    _nswc_1.Cgl = 0.0
    _nswc_1.Cgp = 0.0
    _nswc_1.Cgs = 0.0
    _nswc_1.Cgt = 0.0
    _nswc_1.Cgv = 0.0
    _nswc_1.Ch = 0.0
    _nswc_1.Ci = 0.0
    _nswc_1.Ck = 0.0
    _nswc_1.Cl = 0.0
    _nswc_1.Clc = 0.0
    _nswc_1.Cm = 0.0
    _nswc_1.Cmu = 0.0
    _nswc_1.Cn = 0.0
    _nswc_1.Cnp = 0.0
    _nswc_1.Cnw = 0.0
    _nswc_1.Cp = 0.0
    _nswc_1.Cpd = 0.0
    _nswc_1.Cpf = 0.0
    _nswc_1.Cpv = 0.0
    _nswc_1.Cq = 0.0
    _nswc_1.Cr = 0.0
    _nswc_1.Crd = 0.0
    _nswc_1.Cs = 0.0
    _nswc_1.Csc = 0.0
    _nswc_1.Csf = 0.0
    _nswc_1.Cst = 0.0
    _nswc_1.Csv = 0.0
    _nswc_1.Csw = 0.0
    _nswc_1.Csz = 0.0
    _nswc_1.Ct = 0.0
    _nswc_1.Cv = 0.0
    _nswc_1.Cw = 0.0
    _nswc_1.Cy = 0.0

    _nswc_2 = RAMSTKNSWCRecord()
    _nswc_2.revision_id = 1
    _nswc_2.hardware_id = 2
    _nswc_2.Cac = 0.0
    _nswc_2.Calt = 0.0
    _nswc_2.Cb = 0.0
    _nswc_2.Cbl = 0.0
    _nswc_2.Cbt = 0.0
    _nswc_2.Cbv = 0.0
    _nswc_2.Cc = 0.0
    _nswc_2.Ccf = 0.0
    _nswc_2.Ccp = 0.0
    _nswc_2.Ccs = 0.0
    _nswc_2.Ccv = 0.0
    _nswc_2.Ccw = 0.0
    _nswc_2.Cd = 0.0
    _nswc_2.Cdc = 0.0
    _nswc_2.Cdl = 0.0
    _nswc_2.Cdp = 0.0
    _nswc_2.Cds = 0.0
    _nswc_2.Cdt = 0.0
    _nswc_2.Cdw = 0.0
    _nswc_2.Cdy = 0.0
    _nswc_2.Ce = 0.0
    _nswc_2.Cf = 0.0
    _nswc_2.Cg = 0.0
    _nswc_2.Cga = 0.0
    _nswc_2.Cgl = 0.0
    _nswc_2.Cgp = 0.0
    _nswc_2.Cgs = 0.0
    _nswc_2.Cgt = 0.0
    _nswc_2.Cgv = 0.0
    _nswc_2.Ch = 0.0
    _nswc_2.Ci = 0.0
    _nswc_2.Ck = 0.0
    _nswc_2.Cl = 0.0
    _nswc_2.Clc = 0.0
    _nswc_2.Cm = 0.0
    _nswc_2.Cmu = 0.0
    _nswc_2.Cn = 0.0
    _nswc_2.Cnp = 0.0
    _nswc_2.Cnw = 0.0
    _nswc_2.Cp = 0.0
    _nswc_2.Cpd = 0.0
    _nswc_2.Cpf = 0.0
    _nswc_2.Cpv = 0.0
    _nswc_2.Cq = 0.0
    _nswc_2.Cr = 0.0
    _nswc_2.Crd = 0.0
    _nswc_2.Cs = 0.0
    _nswc_2.Csc = 0.0
    _nswc_2.Csf = 0.0
    _nswc_2.Cst = 0.0
    _nswc_2.Csv = 0.0
    _nswc_2.Csw = 0.0
    _nswc_2.Csz = 0.0
    _nswc_2.Ct = 0.0
    _nswc_2.Cv = 0.0
    _nswc_2.Cw = 0.0
    _nswc_2.Cy = 0.0

    _nswc_3 = RAMSTKNSWCRecord()
    _nswc_3.revision_id = 1
    _nswc_3.hardware_id = 3
    _nswc_3.Cac = 0.0
    _nswc_3.Calt = 0.0
    _nswc_3.Cb = 0.0
    _nswc_3.Cbl = 0.0
    _nswc_3.Cbt = 0.0
    _nswc_3.Cbv = 0.0
    _nswc_3.Cc = 0.0
    _nswc_3.Ccf = 0.0
    _nswc_3.Ccp = 0.0
    _nswc_3.Ccs = 0.0
    _nswc_3.Ccv = 0.0
    _nswc_3.Ccw = 0.0
    _nswc_3.Cd = 0.0
    _nswc_3.Cdc = 0.0
    _nswc_3.Cdl = 0.0
    _nswc_3.Cdp = 0.0
    _nswc_3.Cds = 0.0
    _nswc_3.Cdt = 0.0
    _nswc_3.Cdw = 0.0
    _nswc_3.Cdy = 0.0
    _nswc_3.Ce = 0.0
    _nswc_3.Cf = 0.0
    _nswc_3.Cg = 0.0
    _nswc_3.Cga = 0.0
    _nswc_3.Cgl = 0.0
    _nswc_3.Cgp = 0.0
    _nswc_3.Cgs = 0.0
    _nswc_3.Cgt = 0.0
    _nswc_3.Cgv = 0.0
    _nswc_3.Ch = 0.0
    _nswc_3.Ci = 0.0
    _nswc_3.Ck = 0.0
    _nswc_3.Cl = 0.0
    _nswc_3.Clc = 0.0
    _nswc_3.Cm = 0.0
    _nswc_3.Cmu = 0.0
    _nswc_3.Cn = 0.0
    _nswc_3.Cnp = 0.0
    _nswc_3.Cnw = 0.0
    _nswc_3.Cp = 0.0
    _nswc_3.Cpd = 0.0
    _nswc_3.Cpf = 0.0
    _nswc_3.Cpv = 0.0
    _nswc_3.Cq = 0.0
    _nswc_3.Cr = 0.0
    _nswc_3.Crd = 0.0
    _nswc_3.Cs = 0.0
    _nswc_3.Csc = 0.0
    _nswc_3.Csf = 0.0
    _nswc_3.Cst = 0.0
    _nswc_3.Csv = 0.0
    _nswc_3.Csw = 0.0
    _nswc_3.Csz = 0.0
    _nswc_3.Ct = 0.0
    _nswc_3.Cv = 0.0
    _nswc_3.Cw = 0.0
    _nswc_3.Cy = 0.0

    DAO = MockDAO()
    DAO.table = [
        _nswc_1,
        _nswc_2,
        _nswc_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "Cac": 0.0,
        "Calt": 0.0,
        "Cb": 0.0,
        "Cbl": 0.0,
        "Cbt": 0.0,
        "Cbv": 0.0,
        "Cc": 0.0,
        "Ccf": 0.0,
        "Ccp": 0.0,
        "Ccs": 0.0,
        "Ccv": 0.0,
        "Ccw": 0.0,
        "Cd": 0.0,
        "Cdc": 0.0,
        "Cdl": 0.0,
        "Cdp": 0.0,
        "Cds": 0.0,
        "Cdt": 0.0,
        "Cdw": 0.0,
        "Cdy": 0.0,
        "Ce": 0.0,
        "Cf": 0.0,
        "Cg": 0.0,
        "Cga": 0.0,
        "Cgl": 0.0,
        "Cgp": 0.0,
        "Cgs": 0.0,
        "Cgt": 0.0,
        "Cgv": 0.0,
        "Ch": 0.0,
        "Ci": 0.0,
        "Ck": 0.0,
        "Cl": 0.0,
        "Clc": 0.0,
        "Cm": 0.0,
        "Cmu": 0.0,
        "Cn": 0.0,
        "Cnp": 0.0,
        "Cnw": 0.0,
        "Cp": 0.0,
        "Cpd": 0.0,
        "Cpf": 0.0,
        "Cpv": 0.0,
        "Cq": 0.0,
        "Cr": 0.0,
        "Crd": 0.0,
        "Cs": 0.0,
        "Csc": 0.0,
        "Csf": 0.0,
        "Cst": 0.0,
        "Csv": 0.0,
        "Csw": 0.0,
        "Csz": 0.0,
        "Ct": 0.0,
        "Cv": 0.0,
        "Cw": 0.0,
        "Cy": 0.0,
    }


@pytest.fixture(scope="function")
def test_recordmodel(mock_program_dao):
    """Get a record model instance for each test function."""
    dut = mock_program_dao.do_select_all(RAMSTKNSWCRecord, _all=False)

    yield dut

    # Delete the device under test.
    del dut
