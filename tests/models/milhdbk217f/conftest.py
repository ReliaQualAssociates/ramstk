# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMilHdbkF


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "A1": 0.0,
        "A2": 0.0,
        "B1": 0.0,
        "B2": 0.0,
        "C1": 0.0,
        "C2": 0.0,
        "lambdaBD": 0.0,
        "lambdaBP": 0.0,
        "lambdaCYC": 0.0,
        "lambdaEOS": 0.0,
        "piA": 0.0,
        "piC": 0.0,
        "piCD": 0.0,
        "piCF": 0.0,
        "piCR": 0.0,
        "piCV": 0.0,
        "piCYC": 0.0,
        "piE": 0.0,
        "piF": 0.0,
        "piI": 0.0,
        "piK": 0.0,
        "piL": 0.0,
        "piM": 0.0,
        "piMFG": 0.0,
        "piN": 0.0,
        "piNR": 0.0,
        "piP": 0.0,
        "piPT": 0.0,
        "piQ": 0.0,
        "piR": 0.0,
        "piS": 0.0,
        "piT": 0.0,
        "piTAPS": 0.0,
        "piU": 0.0,
        "piV": 0.0,
    }


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _milhdbk217f_1 = RAMSTKMilHdbkF()
    _milhdbk217f_1.revision_id = 1
    _milhdbk217f_1.hardware_id = 1
    _milhdbk217f_1.A1 = 0.0
    _milhdbk217f_1.A2 = 0.0
    _milhdbk217f_1.B1 = 0.0
    _milhdbk217f_1.B2 = 0.0
    _milhdbk217f_1.C1 = 0.0
    _milhdbk217f_1.C2 = 0.0
    _milhdbk217f_1.lambdaBD = 0.0
    _milhdbk217f_1.lambdaBP = 0.0
    _milhdbk217f_1.lambdaCYC = 0.0
    _milhdbk217f_1.lambdaEOS = 0.0
    _milhdbk217f_1.piA = 0.0
    _milhdbk217f_1.piC = 0.0
    _milhdbk217f_1.piCD = 0.0
    _milhdbk217f_1.piCF = 0.0
    _milhdbk217f_1.piCR = 0.0
    _milhdbk217f_1.piCV = 0.0
    _milhdbk217f_1.piCYC = 0.0
    _milhdbk217f_1.piE = 0.0
    _milhdbk217f_1.piF = 0.0
    _milhdbk217f_1.piI = 0.0
    _milhdbk217f_1.piK = 0.0
    _milhdbk217f_1.piL = 0.0
    _milhdbk217f_1.piM = 0.0
    _milhdbk217f_1.piMFG = 0.0
    _milhdbk217f_1.piN = 0.0
    _milhdbk217f_1.piNR = 0.0
    _milhdbk217f_1.piP = 0.0
    _milhdbk217f_1.piPT = 0.0
    _milhdbk217f_1.piQ = 0.0
    _milhdbk217f_1.piR = 0.0
    _milhdbk217f_1.piS = 0.0
    _milhdbk217f_1.piT = 0.0
    _milhdbk217f_1.piTAPS = 0.0
    _milhdbk217f_1.piU = 0.0
    _milhdbk217f_1.piV = 0.0

    _milhdbk217f_2 = RAMSTKMilHdbkF()
    _milhdbk217f_2.revision_id = 1
    _milhdbk217f_2.hardware_id = 2
    _milhdbk217f_2.A1 = 0.0
    _milhdbk217f_2.A2 = 0.0
    _milhdbk217f_2.B1 = 0.0
    _milhdbk217f_2.B2 = 0.0
    _milhdbk217f_2.C1 = 0.0
    _milhdbk217f_2.C2 = 0.0
    _milhdbk217f_2.lambdaBD = 0.0
    _milhdbk217f_2.lambdaBP = 0.0
    _milhdbk217f_2.lambdaCYC = 0.0
    _milhdbk217f_2.lambdaEOS = 0.0
    _milhdbk217f_2.piA = 0.0
    _milhdbk217f_2.piC = 0.0
    _milhdbk217f_2.piCD = 0.0
    _milhdbk217f_2.piCF = 0.0
    _milhdbk217f_2.piCR = 0.0
    _milhdbk217f_2.piCV = 0.0
    _milhdbk217f_2.piCYC = 0.0
    _milhdbk217f_2.piE = 0.0
    _milhdbk217f_2.piF = 0.0
    _milhdbk217f_2.piI = 0.0
    _milhdbk217f_2.piK = 0.0
    _milhdbk217f_2.piL = 0.0
    _milhdbk217f_2.piM = 0.0
    _milhdbk217f_2.piMFG = 0.0
    _milhdbk217f_2.piN = 0.0
    _milhdbk217f_2.piNR = 0.0
    _milhdbk217f_2.piP = 0.0
    _milhdbk217f_2.piPT = 0.0
    _milhdbk217f_2.piQ = 0.0
    _milhdbk217f_2.piR = 0.0
    _milhdbk217f_2.piS = 0.0
    _milhdbk217f_2.piT = 0.0
    _milhdbk217f_2.piTAPS = 0.0
    _milhdbk217f_2.piU = 0.0
    _milhdbk217f_2.piV = 0.0

    _milhdbk217f_3 = RAMSTKMilHdbkF()
    _milhdbk217f_3.revision_id = 1
    _milhdbk217f_3.hardware_id = 3
    _milhdbk217f_3.A1 = 0.0
    _milhdbk217f_3.A2 = 0.0
    _milhdbk217f_3.B1 = 0.0
    _milhdbk217f_3.B2 = 0.0
    _milhdbk217f_3.C1 = 0.0
    _milhdbk217f_3.C2 = 0.0
    _milhdbk217f_3.lambdaBD = 0.0
    _milhdbk217f_3.lambdaBP = 0.0
    _milhdbk217f_3.lambdaCYC = 0.0
    _milhdbk217f_3.lambdaEOS = 0.0
    _milhdbk217f_3.piA = 0.0
    _milhdbk217f_3.piC = 0.0
    _milhdbk217f_3.piCD = 0.0
    _milhdbk217f_3.piCF = 0.0
    _milhdbk217f_3.piCR = 0.0
    _milhdbk217f_3.piCV = 0.0
    _milhdbk217f_3.piCYC = 0.0
    _milhdbk217f_3.piE = 0.0
    _milhdbk217f_3.piF = 0.0
    _milhdbk217f_3.piI = 0.0
    _milhdbk217f_3.piK = 0.0
    _milhdbk217f_3.piL = 0.0
    _milhdbk217f_3.piM = 0.0
    _milhdbk217f_3.piMFG = 0.0
    _milhdbk217f_3.piN = 0.0
    _milhdbk217f_3.piNR = 0.0
    _milhdbk217f_3.piP = 0.0
    _milhdbk217f_3.piPT = 0.0
    _milhdbk217f_3.piQ = 0.0
    _milhdbk217f_3.piR = 0.0
    _milhdbk217f_3.piS = 0.0
    _milhdbk217f_3.piT = 0.0
    _milhdbk217f_3.piTAPS = 0.0
    _milhdbk217f_3.piU = 0.0
    _milhdbk217f_3.piV = 0.0

    DAO = MockDAO()
    DAO.table = [
        _milhdbk217f_1,
        _milhdbk217f_2,
        _milhdbk217f_3,
    ]

    yield DAO
