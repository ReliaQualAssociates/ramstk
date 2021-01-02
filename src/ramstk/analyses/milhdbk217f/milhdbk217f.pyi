# Standard Library Imports
from typing import Any, Dict

# RAMSTK Local Imports
from .models import capacitor as capacitor
from .models import connection as connection
from .models import crystal as crystal
from .models import efilter as efilter
from .models import fuse as fuse
from .models import inductor as inductor
from .models import integratedcircuit as integratedcircuit
from .models import lamp as lamp
from .models import meter as meter
from .models import relay as relay
from .models import resistor as resistor
from .models import semiconductor as semiconductor
from .models import switch as switch

def _do_calculate_part_count(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def _do_calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    ...


def _get_environment_factor(category_id: int,
                            environment_active_id: int,
                            subcategory_id: int = ...,
                            quality_id: int = ...) -> float:
    ...


def _get_part_count_quality_factor(category_id: int, subcategory_id: int,
                                   quality_id: int) -> float:
    ...


def _get_part_stress_quality_factor(category_id: int, subcategory_id: int,
                                    quality_id: int) -> float:
    ...


def do_predict_active_hazard_rate(**attributes: Dict[str, Any]) -> float:
    ...
