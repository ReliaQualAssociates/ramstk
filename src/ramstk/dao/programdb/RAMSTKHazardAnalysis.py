# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKHazardAnalysis.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKHazardAnalysis Table."""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKHazardAnalysis(RAMSTK_BASE):
    """
    Class to represent ramstk_hazard_analysis table in the Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a Many-to-One relationship with ramstk_hardware.
    """

    __tablename__ = 'ramstk_hazard_analysis'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        nullable=False)
    hazard_id = Column(
        'fld_hazard_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    potential_hazard = Column('fld_potential_hazard', String(256), default='')
    potential_cause = Column('fld_potential_cause', String(512), default='')
    assembly_effect = Column('fld_assembly_effect', String(512), default='')
    assembly_severity = Column(
        'fld_assembly_severity', String(256), default='Major')
    assembly_probability = Column(
        'fld_assembly_probability', String(256), default='Level A - Frequent')
    assembly_hri = Column('fld_assembly_hri', Integer, default=20)
    assembly_mitigation = Column('fld_assembly_mitigation', BLOB, default=b'')
    assembly_severity_f = Column(
        'fld_assembly_severity_f', String(256), default='Major')
    assembly_probability_f = Column(
        'fld_assembly_probability_f',
        String(256),
        default='Level A - Frequent')
    assembly_hri_f = Column('fld_assembly_hri_f', Integer, default=20)
    function_1 = Column('fld_function_1', String(128), default='')
    function_2 = Column('fld_function_2', String(128), default='')
    function_3 = Column('fld_function_3', String(128), default='')
    function_4 = Column('fld_function_4', String(128), default='')
    function_5 = Column('fld_function_5', String(128), default='')
    remarks = Column('fld_remarks', BLOB, default=b'')
    result_1 = Column('fld_result_1', Float, default=0.0)
    result_2 = Column('fld_result_2', Float, default=0.0)
    result_3 = Column('fld_result_3', Float, default=0.0)
    result_4 = Column('fld_result_4', Float, default=0.0)
    result_5 = Column('fld_result_5', Float, default=0.0)
    system_effect = Column('fld_system_effect', String(512), default='')
    system_severity = Column(
        'fld_system_severity', String(256), default='Major')
    system_probability = Column(
        'fld_system_probability', String(256), default='Level A - Frequent')
    system_hri = Column('fld_system_hri', Integer, default=20)
    system_mitigation = Column('fld_system_mitigation', BLOB, default=b'')
    system_severity_f = Column(
        'fld_system_severity_f', String(256), default='Major')
    system_probability_f = Column(
        'fld_system_probability_f', String(256), default='Level A - Frequent')
    system_hri_f = Column('fld_system_hri_f', Integer, default=20)
    user_blob_1 = Column('fld_user_blob_1', BLOB, default=b'')
    user_blob_2 = Column('fld_user_blob_2', BLOB, default=b'')
    user_blob_3 = Column('fld_user_blob_3', BLOB, default=b'')
    user_float_1 = Column('fld_user_float_1', Float, default=0.0)
    user_float_2 = Column('fld_user_float_2', Float, default=0.0)
    user_float_3 = Column('fld_user_float_3', Float, default=0.0)
    user_int_1 = Column('fld_user_int_1', Integer, default=0)
    user_int_2 = Column('fld_user_int_2', Integer, default=0)
    user_int_3 = Column('fld_user_int_3', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='hazard')
    hardware = relationship('RAMSTKHardware', back_populates='hazard')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKHazardAnalysis data model attributes.

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
            'hardware_id': self.hardware_id,
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
            'user_int_3': self.user_int_3
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the RAMSTKHazardAnalysis data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKHazardAnalysis {0:d} attributes.". \
               format(self.hazard_id)

        try:
            self.potential_hazard = str(
                none_to_default(attributes['potential_hazard'], ''))
            self.potential_cause = str(
                none_to_default(attributes['potential_cause'], ''))
            self.assembly_effect = str(
                none_to_default(attributes['assembly_effect'], ''))
            self.assembly_severity = str(
                none_to_default(attributes['assembly_severity'], ''))
            self.assembly_probability = str(
                none_to_default(attributes['assembly_probability'], ''))
            self.assembly_hri = int(
                none_to_default(attributes['assembly_hri'], 0))
            self.assembly_mitigation = none_to_default(
                attributes['assembly_mitigation'], b'')
            self.assembly_severity_f = str(
                none_to_default(attributes['assembly_severity_f'], ''))
            self.assembly_probability_f = str(
                none_to_default(attributes['assembly_probability_f'], ''))
            self.assembly_hri_f = int(
                none_to_default(attributes['assembly_hri_f'], 0))
            self.system_effect = str(
                none_to_default(attributes['system_effect'], ''))
            self.system_severity = str(
                none_to_default(attributes['system_severity'], ''))
            self.system_probability = str(
                none_to_default(attributes['system_probability'], ''))
            self.system_hri = int(none_to_default(attributes['system_hri'], 0))
            self.system_mitigation = none_to_default(
                attributes['system_mitigation'], b'')
            self.system_severity_f = str(
                none_to_default(attributes['system_severity_f'], ''))
            self.system_probability_f = str(
                none_to_default(attributes['system_probability_f'], ''))
            self.system_hri_f = int(
                none_to_default(attributes['system_hri_f'], 0))
            self.remarks = str(none_to_default(attributes['remarks'], ''))
            self.function_1 = str(
                none_to_default(attributes['function_1'], ''))
            self.function_2 = str(
                none_to_default(attributes['function_2'], ''))
            self.function_3 = str(
                none_to_default(attributes['function_3'], ''))
            self.function_4 = str(
                none_to_default(attributes['function_4'], ''))
            self.function_5 = str(
                none_to_default(attributes['function_5'], ''))
            self.result_1 = float(none_to_default(attributes['result_1'], 0.0))
            self.result_2 = float(none_to_default(attributes['result_2'], 0.0))
            self.result_3 = float(none_to_default(attributes['result_3'], 0.0))
            self.result_4 = float(none_to_default(attributes['result_4'], 0.0))
            self.result_5 = float(none_to_default(attributes['result_5'], 0.0))
            self.user_blob_1 = none_to_default(attributes['user_blob_1'], b'')
            self.user_blob_2 = none_to_default(attributes['user_blob_2'], b'')
            self.user_blob_3 = none_to_default(attributes['user_blob_3'], b'')
            self.user_float_1 = float(
                none_to_default(attributes['user_float_1'], 0.0))
            self.user_float_2 = float(
                none_to_default(attributes['user_float_2'], 0.0))
            self.user_float_3 = float(
                none_to_default(attributes['user_float_3'], 0.0))
            self.user_int_1 = int(none_to_default(attributes['user_int_1'], 0))
            self.user_int_2 = int(none_to_default(attributes['user_int_2'], 0))
            self.user_int_3 = int(none_to_default(attributes['user_int_3'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKHazardAnalysis.set_attributes().".format(str(_err))

        return _error_code, _msg

    def calculate(self):
        """
        Calculate the hazard analysis.

        This method calculate the initial assembly hazard risk index (HRI), the
        final assembly HRI, the initial system HRI, and the final system HRI.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _severity = {
            'Insignificant': 1,
            'Slight': 2,
            'Low': 3,
            'Medium': 4,
            'High': 5,
            'Major': 6
        }
        _probability = {
            'Level E - Extremely Unlikely': 1,
            'Level D - Remote': 2,
            'Level C - Occasional': 3,
            'Level B - Reasonably Probable': 4,
            'Level A - Frequent': 5
        }

        # Create list of safe functions.
        _safe_list = [
            'uf1', 'uf2', 'uf3', 'ui1', 'ui2', 'ui3', 'equation1', 'equation2',
            'equation3', 'equation4', 'equation5', 'res1', 'res2', 'res3',
            'res4', 'res5'
        ]

        # Use the list to filter the local namespace
        _calculations = dict([(k, locals().get(k, None)) for k in _safe_list])

        # Calculate the MIL-STD-882 hazard risk indices.
        try:
            self.assembly_hri = (_probability[self.assembly_probability] *
                                 _severity[self.assembly_severity])
        except KeyError:
            self.assembly_hri = 30
            _return = True

        try:
            self.assembly_hri_f = (_probability[self.assembly_probability_f] *
                                   _severity[self.assembly_severity_f])
        except KeyError:
            self.assembly_hri_f = 30
            _return = True

        try:
            self.system_hri = (_probability[self.system_probability] *
                               _severity[self.system_severity])
        except KeyError:
            self.system_hri = 30
            _return = True

        try:
            self.system_hri_f = (_probability[self.system_probability_f] *
                                 _severity[self.system_severity_f])
        except KeyError:
            self.system_hri_f = 30
            _return = True

        # Get the user-defined float and integer values.
        _calculations['uf1'] = self.user_float_1
        _calculations['uf2'] = self.user_float_2
        _calculations['uf3'] = self.user_float_3
        _calculations['ui1'] = self.user_int_1
        _calculations['ui2'] = self.user_int_2
        _calculations['ui3'] = self.user_int_3

        # Get the user-defined functions.
        _calculations['equation1'] = self.function_1
        _calculations['equation2'] = self.function_2
        _calculations['equation3'] = self.function_3
        _calculations['equation4'] = self.function_4
        _calculations['equation5'] = self.function_5

        # Get the existing results.  This allows the use of the results
        # fields to be manually set to a float values by the user.
        # Essentially creating five more user-defined float values.
        _calculations['res1'] = self.result_1
        _calculations['res2'] = self.result_2
        _calculations['res3'] = self.result_3
        _calculations['res4'] = self.result_4
        _calculations['res5'] = self.result_5

        _keys = list(_calculations.keys())
        _values = list(_calculations.values())

        for _index, _key in enumerate(_keys):
            vars()[_key] = _values[_index]

        try:
            self.result_1 = eval(_calculations['equation1'],
                                 {"__builtins__": None}, _calculations)
        except SyntaxError:
            self.result_1 = _calculations['res1']
            if _calculations['equation1'] != '':
                _return = True

        try:
            self.result_2 = eval(_calculations['equation2'],
                                 {"__builtins__": None}, _calculations)
        except SyntaxError:
            self.result_2 = _calculations['res2']
            if _calculations['equation2'] != '':
                _return = True

        try:
            self.result_3 = eval(_calculations['equation3'],
                                 {"__builtins__": None}, _calculations)
        except SyntaxError:
            self.result_3 = _calculations['res3']
            if _calculations['equation3'] != '':
                _return = True

        try:
            self.result_4 = eval(_calculations['equation4'],
                                 {"__builtins__": None}, _calculations)
        except SyntaxError:
            self.result_4 = _calculations['res4']
            if _calculations['equation4'] != '':
                _return = True

        try:
            self.result_5 = eval(_calculations['equation5'],
                                 {"__builtins__": None}, _calculations)
        except SyntaxError:
            self.result_5 = _calculations['res5']
            if _calculations['equation5'] != '':
                _return = True

        return _return
