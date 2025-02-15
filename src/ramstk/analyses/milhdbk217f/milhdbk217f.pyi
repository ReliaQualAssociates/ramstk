# Standard Library Imports
from typing import Callable, Dict, Optional, Union

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

def do_predict_active_hazard_rate(
    attributes: Dict[str, Union[float, int, str]]
) -> float: ...
def _do_calculate_part_count(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _do_calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
def _do_handle_prediction_failure(
    error_type: str,
    attributes: Dict[str, Union[float, int, str]],
    additional_info: str = "",
) -> None: ...
def _get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float: ...
def _get_function(
    func_dict: Dict, category_id: int, subcategory_id: Optional[int] = None
) -> Callable: ...
def _get_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float: ...
def _get_quality_factor(attributes: Dict[str, Union[float, int, str]]) -> float: ...
def _set_default_values(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]: ...
