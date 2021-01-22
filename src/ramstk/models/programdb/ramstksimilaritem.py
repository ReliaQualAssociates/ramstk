# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.data.storage.programdb.RAMSTKSimilarItem.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKSimilarItem Table."""

# Third Party Imports
# noinspection PyPackageRequirements
from sqlalchemy import Column, Float, ForeignKey, Integer, String
# noinspection PyPackageRequirements
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


# pylint: disable=R0902
class RAMSTKSimilarItem(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_similar_item table in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_hardware.
    """

    __defaults__ = {
        'change_description_1': '',
        'change_description_2': '',
        'change_description_3': '',
        'change_description_4': '',
        'change_description_5': '',
        'change_description_6': '',
        'change_description_7': '',
        'change_description_8': '',
        'change_description_9': '',
        'change_description_10': '',
        'change_factor_1': 1.0,
        'change_factor_2': 1.0,
        'change_factor_3': 1.0,
        'change_factor_4': 1.0,
        'change_factor_5': 1.0,
        'change_factor_6': 1.0,
        'change_factor_7': 1.0,
        'change_factor_8': 1.0,
        'change_factor_9': 1.0,
        'change_factor_10': 1.0,
        'environment_from_id': 0,
        'environment_to_id': 0,
        'function_1': '0',
        'function_2': '0',
        'function_3': '0',
        'function_4': '0',
        'function_5': '0',
        'similar_item_method_id': 1,
        'parent_id': 0,
        'quality_from_id': 0,
        'quality_to_id': 0,
        'result_1': 0.0,
        'result_2': 0.0,
        'result_3': 0.0,
        'result_4': 0.0,
        'result_5': 0.0,
        'temperature_from': 30.0,
        'temperature_to': 30.0,
        'user_blob_1': '',
        'user_blob_2': '',
        'user_blob_3': '',
        'user_blob_4': '',
        'user_blob_5': '',
        'user_float_1': 0.0,
        'user_float_2': 0.0,
        'user_float_3': 0.0,
        'user_float_4': 0.0,
        'user_float_5': 0.0,
        'user_int_1': 0,
        'user_int_2': 0,
        'user_int_3': 0,
        'user_int_4': 0,
        'user_int_5': 0
    }
    __tablename__ = 'ramstk_similar_item'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id',
                         Integer,
                         ForeignKey('ramstk_revision.fld_revision_id'),
                         nullable=False)
    hardware_id = Column('fld_hardware_id',
                         Integer,
                         ForeignKey('ramstk_hardware.fld_hardware_id'),
                         primary_key=True,
                         nullable=False)

    change_description_1 = Column('fld_change_description_1',
                                  String,
                                  default=__defaults__['change_description_1'])
    change_description_2 = Column('fld_change_description_2',
                                  String,
                                  default=__defaults__['change_description_2'])
    change_description_3 = Column('fld_change_description_3',
                                  String,
                                  default=__defaults__['change_description_3'])
    change_description_4 = Column('fld_change_description_4',
                                  String,
                                  default=__defaults__['change_description_4'])
    change_description_5 = Column('fld_change_description_5',
                                  String,
                                  default=__defaults__['change_description_5'])
    change_description_6 = Column('fld_change_description_6',
                                  String,
                                  default=__defaults__['change_description_6'])
    change_description_7 = Column('fld_change_description_7',
                                  String,
                                  default=__defaults__['change_description_7'])
    change_description_8 = Column('fld_change_description_8',
                                  String,
                                  default=__defaults__['change_description_8'])
    change_description_9 = Column('fld_change_description_9',
                                  String,
                                  default=__defaults__['change_description_9'])
    change_description_10 = Column(
        'fld_change_description_10',
        String,
        default=__defaults__['change_description_10'])
    change_factor_1 = Column('fld_change_factor_1',
                             Float,
                             default=__defaults__['change_factor_1'])
    change_factor_2 = Column('fld_change_factor_2',
                             Float,
                             default=__defaults__['change_factor_2'])
    change_factor_3 = Column('fld_change_factor_3',
                             Float,
                             default=__defaults__['change_factor_3'])
    change_factor_4 = Column('fld_change_factor_4',
                             Float,
                             default=__defaults__['change_factor_4'])
    change_factor_5 = Column('fld_change_factor_5',
                             Float,
                             default=__defaults__['change_factor_5'])
    change_factor_6 = Column('fld_change_factor_6',
                             Float,
                             default=__defaults__['change_factor_6'])
    change_factor_7 = Column('fld_change_factor_7',
                             Float,
                             default=__defaults__['change_factor_7'])
    change_factor_8 = Column('fld_change_factor_8',
                             Float,
                             default=__defaults__['change_factor_8'])
    change_factor_9 = Column('fld_change_factor_9',
                             Float,
                             default=__defaults__['change_factor_9'])
    change_factor_10 = Column('fld_change_factor_10',
                              Float,
                              default=__defaults__['change_factor_10'])
    environment_from_id = Column('fld_environment_from_id',
                                 Integer,
                                 default=__defaults__['environment_from_id'])
    environment_to_id = Column('fld_environment_to_id',
                               Integer,
                               default=__defaults__['environment_to_id'])
    function_1 = Column('fld_function_1',
                        String(128),
                        default=__defaults__['function_1'])
    function_2 = Column('fld_function_2',
                        String(128),
                        default=__defaults__['function_2'])
    function_3 = Column('fld_function_3',
                        String(128),
                        default=__defaults__['function_3'])
    function_4 = Column('fld_function_4',
                        String(128),
                        default=__defaults__['function_4'])
    function_5 = Column('fld_function_5',
                        String(128),
                        default=__defaults__['function_5'])
    similar_item_method_id = Column(
        'fld_similar_item_method_id',
        Integer,
        default=__defaults__['similar_item_method_id'])
    parent_id = Column('fld_parent_id',
                       Integer,
                       default=__defaults__['parent_id'])
    quality_from_id = Column('fld_quality_from_id',
                             Integer,
                             default=__defaults__['quality_from_id'])
    quality_to_id = Column('fld_quality_to_id',
                           Integer,
                           default=__defaults__['quality_to_id'])
    result_1 = Column('fld_result_1', Float, default=__defaults__['result_1'])
    result_2 = Column('fld_result_2', Float, default=__defaults__['result_2'])
    result_3 = Column('fld_result_3', Float, default=__defaults__['result_3'])
    result_4 = Column('fld_result_4', Float, default=__defaults__['result_4'])
    result_5 = Column('fld_result_5', Float, default=__defaults__['result_5'])
    temperature_from = Column('fld_temperature_from',
                              Float,
                              default=__defaults__['temperature_from'])
    temperature_to = Column('fld_temperature_to',
                            Float,
                            default=__defaults__['temperature_to'])
    user_blob_1 = Column('fld_user_blob_1',
                         String,
                         default=__defaults__['user_blob_1'])
    user_blob_2 = Column('fld_user_blob_2',
                         String,
                         default=__defaults__['user_blob_2'])
    user_blob_3 = Column('fld_user_blob_3',
                         String,
                         default=__defaults__['user_blob_3'])
    user_blob_4 = Column('fld_user_blob_4',
                         String,
                         default=__defaults__['user_blob_4'])
    user_blob_5 = Column('fld_user_blob_5',
                         String,
                         default=__defaults__['user_blob_5'])
    user_float_1 = Column('fld_user_float_1',
                          Float,
                          default=__defaults__['user_float_1'])
    user_float_2 = Column('fld_user_float_2',
                          Float,
                          default=__defaults__['user_float_2'])
    user_float_3 = Column('fld_user_float_3',
                          Float,
                          default=__defaults__['user_float_3'])
    user_float_4 = Column('fld_user_float_4',
                          Float,
                          default=__defaults__['user_float_4'])
    user_float_5 = Column('fld_user_float_5',
                          Float,
                          default=__defaults__['user_float_5'])
    user_int_1 = Column('fld_user_int_1',
                        Integer,
                        default=__defaults__['user_int_1'])
    user_int_2 = Column('fld_user_int_2',
                        Integer,
                        default=__defaults__['user_int_2'])
    user_int_3 = Column('fld_user_int_3',
                        Integer,
                        default=__defaults__['user_int_3'])
    user_int_4 = Column('fld_user_int_4',
                        Integer,
                        default=__defaults__['user_int_4'])
    user_int_5 = Column('fld_user_int_5',
                        Integer,
                        default=__defaults__['user_int_5'])

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware: relationship = relationship(
        'RAMSTKHardware',
        back_populates='sia',
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKSimilarItem data model attributes.

        :return: {hardware_id, change_description_1, change_description_2,
                  change_description_3, change_description_4,
                  change_description_5, change_description_6,
                  change_description_7, change_description_8,
                  change_description_9, change_description_10, change_factor_1,
                  change_factor_2, change_factor_3, change_factor_4,
                  change_factor_5, change_factor_6, change_factor_7,
                  change_factor_8, change_factor_9, change_factor_10,
                  environment_from_id, environment_to_id, function_1,
                  function_2, function_3, function_4, function_5,
                  similar_item_method_id, parent_id, quality_from_id,
                  quality_to_id, result_1, result_2, result_3, result_4,
                  result_5, temperature_from, temperature_to, user_blob_1,
                  user_blob_2, user_blob_3, user_blob_4, user_blob_5,
                  user_float_1, user_float_2, user_float_3, user_float_4,
                  user_float_5, user_int_1, user_int_2, user_int_3, user_int_4,
                  user_int_5}
        :rtype: tuple
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'change_description_1': self.change_description_1,
            'change_description_2': self.change_description_2,
            'change_description_3': self.change_description_3,
            'change_description_4': self.change_description_4,
            'change_description_5': self.change_description_5,
            'change_description_6': self.change_description_6,
            'change_description_7': self.change_description_7,
            'change_description_8': self.change_description_8,
            'change_description_9': self.change_description_9,
            'change_description_10': self.change_description_10,
            'change_factor_1': self.change_factor_1,
            'change_factor_2': self.change_factor_2,
            'change_factor_3': self.change_factor_3,
            'change_factor_4': self.change_factor_4,
            'change_factor_5': self.change_factor_5,
            'change_factor_6': self.change_factor_6,
            'change_factor_7': self.change_factor_7,
            'change_factor_8': self.change_factor_8,
            'change_factor_9': self.change_factor_9,
            'change_factor_10': self.change_factor_10,
            'environment_from_id': self.environment_from_id,
            'environment_to_id': self.environment_to_id,
            'function_1': self.function_1,
            'function_2': self.function_2,
            'function_3': self.function_3,
            'function_4': self.function_4,
            'function_5': self.function_5,
            'similar_item_method_id': self.similar_item_method_id,
            'parent_id': self.parent_id,
            'quality_from_id': self.quality_from_id,
            'quality_to_id': self.quality_to_id,
            'result_1': self.result_1,
            'result_2': self.result_2,
            'result_3': self.result_3,
            'result_4': self.result_4,
            'result_5': self.result_5,
            'temperature_from': self.temperature_from,
            'temperature_to': self.temperature_to,
            'user_blob_1': self.user_blob_1,
            'user_blob_2': self.user_blob_2,
            'user_blob_3': self.user_blob_3,
            'user_blob_4': self.user_blob_4,
            'user_blob_5': self.user_blob_5,
            'user_float_1': self.user_float_1,
            'user_float_2': self.user_float_2,
            'user_float_3': self.user_float_3,
            'user_float_4': self.user_float_4,
            'user_float_5': self.user_float_5,
            'user_int_1': self.user_int_1,
            'user_int_2': self.user_int_2,
            'user_int_3': self.user_int_3,
            'user_int_4': self.user_int_4,
            'user_int_5': self.user_int_5
        }

        return _attributes
