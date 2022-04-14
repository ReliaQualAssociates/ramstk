# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Local Imports
from .models import capacitor as capacitor
from .models import connection as connection
from .models import inductor as inductor
from .models import integratedcircuit as integratedcircuit
from .models import lamp as lamp
from .models import relay as relay
from .models import resistor as resistor
from .models import semiconductor as semiconductor
from .models import switch as switch

def do_check_overstress(
    category: str,
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]: ...
