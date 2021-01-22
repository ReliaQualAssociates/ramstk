# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKHazardAnalysis.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKHazardAnalysis Table."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKHazardAnalysis(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_hazard_analysis table in the Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a Many-to-One relationship with ramstk_function.
    """

    __defaults__ = {
        'potential_hazard': '',
        'potential_cause': '',
        'assembly_effect': '',
        'assembly_severity': 'Major',
        'assembly_probability': 'Level A - Frequent',
        'assembly_hri': 20,
        'assembly_mitigation': '',
        'assembly_severity_f': 'Major',
        'assembly_probability_f': 'Level A - Frequent',
        'assembly_hri_f': 20,
        'function_1': '',
        'function_2': '',
        'function_3': '',
        'function_4': '',
        'function_5': '',
        'remarks': '',
        'result_1': 0.0,
        'result_2': 0.0,
        'result_3': 0.0,
        'result_4': 0.0,
        'result_5': 0.0,
        'system_effect': '',
        'system_severity': 'Major',
        'system_probability': 'Level A - Frequent',
        'system_hri': 20,
        'system_mitigation': '',
        'system_severity_f': 'Major',
        'system_probability_f': 'Level A - Frequent',
        'system_hri_f': 20,
        'user_blob_1': '',
        'user_blob_2': '',
        'user_blob_3': '',
        'user_float_1': 0.0,
        'user_float_2': 0.0,
        'user_float_3': 0.0,
        'user_int_1': 0,
        'user_int_2': 0,
        'user_int_3': 0
    }
    __tablename__ = 'ramstk_hazard_analysis'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    function_id = Column(
        'fld_function_id',
        Integer,
        ForeignKey('ramstk_function.fld_function_id'),
        nullable=False,
    )
    hazard_id = Column(
        'fld_hazard_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        info={"identity": (0, 1)},
    )

    potential_hazard = Column('fld_potential_hazard',
                              String(256),
                              default=__defaults__['potential_hazard'])
    potential_cause = Column('fld_potential_cause',
                             String(512),
                             default=__defaults__['potential_cause'])
    assembly_effect = Column('fld_assembly_effect',
                             String(512),
                             default=__defaults__['assembly_effect'])
    assembly_severity = Column('fld_assembly_severity',
                               String(256),
                               default=__defaults__['assembly_severity'])
    assembly_probability = Column('fld_assembly_probability',
                                  String(256),
                                  default=__defaults__['assembly_probability'])
    assembly_hri = Column('fld_assembly_hri',
                          Integer,
                          default=__defaults__['assembly_hri'])
    assembly_mitigation = Column('fld_assembly_mitigation',
                                 String,
                                 default=__defaults__['assembly_mitigation'])
    assembly_severity_f = Column('fld_assembly_severity_f',
                                 String(256),
                                 default=__defaults__['assembly_severity_f'])
    assembly_probability_f = Column(
        'fld_assembly_probability_f',
        String(256),
        default=__defaults__['assembly_probability_f'])
    assembly_hri_f = Column('fld_assembly_hri_f',
                            Integer,
                            default=__defaults__['assembly_hri_f'])
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
    remarks = Column('fld_remarks', String, default=__defaults__['remarks'])
    result_1 = Column('fld_result_1', Float, default=__defaults__['result_1'])
    result_2 = Column('fld_result_2', Float, default=__defaults__['result_2'])
    result_3 = Column('fld_result_3', Float, default=__defaults__['result_3'])
    result_4 = Column('fld_result_4', Float, default=__defaults__['result_4'])
    result_5 = Column('fld_result_5', Float, default=__defaults__['result_5'])
    system_effect = Column('fld_system_effect',
                           String(512),
                           default=__defaults__['system_effect'])
    system_severity = Column('fld_system_severity',
                             String(256),
                             default=__defaults__['system_severity'])
    system_probability = Column('fld_system_probability',
                                String(256),
                                default=__defaults__['system_probability'])
    system_hri = Column('fld_system_hri',
                        Integer,
                        default=__defaults__['system_hri'])
    system_mitigation = Column('fld_system_mitigation',
                               String,
                               default=__defaults__['system_mitigation'])
    system_severity_f = Column('fld_system_severity_f',
                               String(256),
                               default=__defaults__['system_severity_f'])
    system_probability_f = Column('fld_system_probability_f',
                                  String(256),
                                  default=__defaults__['system_probability_f'])
    system_hri_f = Column('fld_system_hri_f',
                          Integer,
                          default=__defaults__['system_hri_f'])
    user_blob_1 = Column('fld_user_blob_1',
                         String,
                         default=__defaults__['user_blob_1'])
    user_blob_2 = Column('fld_user_blob_2',
                         String,
                         default=__defaults__['user_blob_2'])
    user_blob_3 = Column('fld_user_blob_3',
                         String,
                         default=__defaults__['user_blob_3'])
    user_float_1 = Column('fld_user_float_1',
                          Float,
                          default=__defaults__['user_float_1'])
    user_float_2 = Column('fld_user_float_2',
                          Float,
                          default=__defaults__['user_float_2'])
    user_float_3 = Column('fld_user_float_3',
                          Float,
                          default=__defaults__['user_float_3'])
    user_int_1 = Column('fld_user_int_1',
                        Integer,
                        default=__defaults__['user_int_1'])
    user_int_2 = Column('fld_user_int_2',
                        Integer,
                        default=__defaults__['user_int_2'])
    user_int_3 = Column('fld_user_int_3',
                        Integer,
                        default=__defaults__['user_int_3'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship(  # type: ignore
        'RAMSTKRevision', back_populates='hazard')
    function = relationship(  # type: ignore
        'RAMSTKFunction', back_populates='hazard')

    def get_attributes(self):
        """Retrieve current values of RAMSTKHazardAnalysis model attributes.

        :return: {revision_id, hardware_id, hazard_id, potential_hazard,
                  potential_cause, assembly_effect, assembly_severity_id,
                  assembly_probability_id, assembly_hri, assembly_mitigation,
                  assembly_severity_id_f, assembly_probability_id_f,
                  assembly_hri_f, system_effect, system_severity_id,
                  system_probability_id, system_hri, system_mitigation,
                  system_severity_id_f, system_probability_id_f,
                  system_hri_f, remarks, function_1, function_2, function_3,
                  function_4, function_5, result_1, result_2, result_3,
                  result_4, result_5, user_blob_1, user_blob_2, user_blob_3,
                  user_float_1, user_float_2, user_float_3, user_int_1,
                  user_int_2, user_int_3} pairs
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'function_id': self.function_id,
            'hazard_id': self.hazard_id,
            'potential_hazard': self.potential_hazard,
            'potential_cause': self.potential_cause,
            'assembly_effect': self.assembly_effect,
            'assembly_severity': self.assembly_severity,
            'assembly_probability': self.assembly_probability,
            'assembly_hri': self.assembly_hri,
            'assembly_mitigation': self.assembly_mitigation,
            'assembly_severity_f': self.assembly_severity_f,
            'assembly_probability_f': self.assembly_probability_f,
            'assembly_hri_f': self.assembly_hri_f,
            'system_effect': self.system_effect,
            'system_severity': self.system_severity,
            'system_probability': self.system_probability,
            'system_hri': self.system_hri,
            'system_mitigation': self.system_mitigation,
            'system_severity_f': self.system_severity_f,
            'system_probability_f': self.system_probability_f,
            'system_hri_f': self.system_hri_f,
            'remarks': self.remarks,
            'function_1': self.function_1,
            'function_2': self.function_2,
            'function_3': self.function_3,
            'function_4': self.function_4,
            'function_5': self.function_5,
            'result_1': self.result_1,
            'result_2': self.result_2,
            'result_3': self.result_3,
            'result_4': self.result_4,
            'result_5': self.result_5,
            'user_blob_1': self.user_blob_1,
            'user_blob_2': self.user_blob_2,
            'user_blob_3': self.user_blob_3,
            'user_float_1': self.user_float_1,
            'user_float_2': self.user_float_2,
            'user_float_3': self.user_float_3,
            'user_int_1': self.user_int_1,
            'user_int_2': self.user_int_2,
            'user_int_3': self.user_int_3,
        }

        return _attributes
