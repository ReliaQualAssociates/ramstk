# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord

class RAMSTKSimilarItemRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    change_description_1: Any
    change_description_2: Any
    change_description_3: Any
    change_description_4: Any
    change_description_5: Any
    change_description_6: Any
    change_description_7: Any
    change_description_8: Any
    change_description_9: Any
    change_description_10: Any
    change_factor_1: Any
    change_factor_2: Any
    change_factor_3: Any
    change_factor_4: Any
    change_factor_5: Any
    change_factor_6: Any
    change_factor_7: Any
    change_factor_8: Any
    change_factor_9: Any
    change_factor_10: Any
    environment_from_id: Any
    environment_to_id: Any
    function_1: Any
    function_2: Any
    function_3: Any
    function_4: Any
    function_5: Any
    similar_item_method_id: Any
    parent_id: Any
    quality_from_id: Any
    quality_to_id: Any
    result_1: Any
    result_2: Any
    result_3: Any
    result_4: Any
    result_5: Any
    temperature_from: Any
    temperature_to: Any
    user_blob_1: Any
    user_blob_2: Any
    user_blob_3: Any
    user_blob_4: Any
    user_blob_5: Any
    user_float_1: Any
    user_float_2: Any
    user_float_3: Any
    user_float_4: Any
    user_float_5: Any
    user_int_1: Any
    user_int_2: Any
    user_int_3: Any
    user_int_4: Any
    user_int_5: Any
    def get_attributes(self): ...
