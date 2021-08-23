# Third Party Imports
from sqlalchemy.engine import Engine as Engine
from sqlalchemy.orm import scoped_session as scoped_session

# RAMSTK Package Imports
from ramstk.models import RAMSTKAllocationRecord as RAMSTKAllocationRecord
from ramstk.models import RAMSTKDesignElectricRecord as RAMSTKDesignElectricRecord
from ramstk.models import RAMSTKDesignMechanicRecord as RAMSTKDesignMechanicRecord
from ramstk.models import RAMSTKEnvironmentRecord as RAMSTKEnvironmentRecord
from ramstk.models import RAMSTKFailureDefinitionRecord as RAMSTKFailureDefinitionRecord
from ramstk.models import RAMSTKFunctionRecord as RAMSTKFunctionRecord
from ramstk.models import RAMSTKHardwareRecord as RAMSTKHardwareRecord
from ramstk.models import RAMSTKHazardRecord as RAMSTKHazardRecord
from ramstk.models import RAMSTKMilHdbk217FRecord as RAMSTKMilHdbk217FRecord
from ramstk.models import RAMSTKMissionPhaseRecord as RAMSTKMissionPhaseRecord
from ramstk.models import RAMSTKMissionRecord as RAMSTKMissionRecord
from ramstk.models import RAMSTKNSWCRecord as RAMSTKNSWCRecord
from ramstk.models import RAMSTKReliabilityRecord as RAMSTKReliabilityRecord
from ramstk.models import RAMSTKRequirementRecord as RAMSTKRequirementRecord
from ramstk.models import RAMSTKRevisionRecord as RAMSTKRevisionRecord
from ramstk.models import RAMSTKSimilarItemRecord as RAMSTKSimilarItemRecord
from ramstk.models import RAMSTKStakeholderRecord as RAMSTKStakeholderRecord
from ramstk.models import RAMSTKValidationRecord as RAMSTKValidationRecord
from ramstk.models.programdb import RAMSTKAction as RAMSTKAction
from ramstk.models.programdb import RAMSTKCause as RAMSTKCause
from ramstk.models.programdb import RAMSTKControl as RAMSTKControl
from ramstk.models.programdb import RAMSTKMechanism as RAMSTKMechanism
from ramstk.models.programdb import RAMSTKMode as RAMSTKMode
from ramstk.models.programdb import RAMSTKOpLoad as RAMSTKOpLoad
from ramstk.models.programdb import RAMSTKOpStress as RAMSTKOpStress
from ramstk.models.programdb import RAMSTKProgramInfo as RAMSTKProgramInfo
from ramstk.models.programdb import RAMSTKProgramStatus as RAMSTKProgramStatus
from ramstk.models.programdb import RAMSTKTestMethod as RAMSTKTestMethod

def do_make_programdb_tables(engine: Engine) -> None: ...
def do_create_program_db(engine: Engine, session: scoped_session) -> None: ...
