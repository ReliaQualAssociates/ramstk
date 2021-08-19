# Third Party Imports
from sqlalchemy.engine import Engine as Engine
from sqlalchemy.orm import scoped_session as scoped_session

# RAMSTK Package Imports
from ramstk.models import RAMSTKDesignElectricRecord as RAMSTKDesignElectricRecord
from ramstk.models import RAMSTKDesignMechanicRecord as RAMSTKDesignMechanicRecord
from ramstk.models import RAMSTKHardwareRecord as RAMSTKHardwareRecord
from ramstk.models import RAMSTKMilHdbk217FRecord as RAMSTKMilHdbk217FRecord
from ramstk.models import RAMSTKNSWCRecord as RAMSTKNSWCRecord
from ramstk.models.programdb import RAMSTKAction as RAMSTKAction
from ramstk.models.programdb import RAMSTKAllocation as RAMSTKAllocation
from ramstk.models.programdb import RAMSTKCause as RAMSTKCause
from ramstk.models.programdb import RAMSTKControl as RAMSTKControl
from ramstk.models.programdb import RAMSTKEnvironment as RAMSTKEnvironment
from ramstk.models.programdb import RAMSTKFailureDefinition as RAMSTKFailureDefinition
from ramstk.models.programdb import RAMSTKFunction as RAMSTKFunction
from ramstk.models.programdb import RAMSTKHazardAnalysis as RAMSTKHazardAnalysis
from ramstk.models.programdb import RAMSTKMechanism as RAMSTKMechanism
from ramstk.models.programdb import RAMSTKMission as RAMSTKMission
from ramstk.models.programdb import RAMSTKMissionPhase as RAMSTKMissionPhase
from ramstk.models.programdb import RAMSTKMode as RAMSTKMode
from ramstk.models.programdb import RAMSTKOpLoad as RAMSTKOpLoad
from ramstk.models.programdb import RAMSTKOpStress as RAMSTKOpStress
from ramstk.models.programdb import RAMSTKProgramInfo as RAMSTKProgramInfo
from ramstk.models.programdb import RAMSTKProgramStatus as RAMSTKProgramStatus
from ramstk.models.programdb import RAMSTKReliability as RAMSTKReliability
from ramstk.models.programdb import RAMSTKRequirement as RAMSTKRequirement
from ramstk.models.programdb import RAMSTKRevision as RAMSTKRevision
from ramstk.models.programdb import RAMSTKSimilarItem as RAMSTKSimilarItem
from ramstk.models.programdb import RAMSTKStakeholder as RAMSTKStakeholder
from ramstk.models.programdb import RAMSTKTestMethod as RAMSTKTestMethod
from ramstk.models.programdb import RAMSTKValidation as RAMSTKValidation

def do_make_programdb_tables(engine: Engine) -> None: ...
def do_create_program_db(engine: Engine, session: scoped_session) -> None: ...
