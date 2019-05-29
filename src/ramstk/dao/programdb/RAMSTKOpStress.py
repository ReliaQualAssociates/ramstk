# -*- coding: utf-8 -*-
#
#       ramstk.dao.programdb.RAMSTKOpStress.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKOpStress Table."""

from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKOpStress(RAMSTK_BASE):
    """
    Class to represent the table ramstk_op_stress in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_op_load.
    """

    __tablename__ = 'ramstk_op_stress'
    __table_args__ = {'extend_existing': True}

    load_id = Column(
        'fld_load_id',
        Integer,
        ForeignKey('ramstk_op_load.fld_load_id'),
        nullable=False)
    stress_id = Column(
        'fld_stress_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    load_history = Column('fld_load_history', String(512), default='')
    measurable_parameter = Column(
        'fld_measurable_parameter', String(512), default='')
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RAMSTK Program database.
    op_load = relationship('RAMSTKOpLoad', back_populates='op_stress')

    is_mode = False
    is_mechanism = False
    is_opload = False
    is_opstress = True
    is_testmethod = False

    def get_attributes(self):
        """
        Retrieve the current values of the Op Stress data model attributes.

        :return: {load_id, stress_id, description, load_history,
                  measurable_parameter, remarks} pairs
        :rtype: tuple
        """
        _attributes = {
            'load_id': self.load_id,
            'stress_id': self.stress_id,
            'description': self.description,
            'load_history': self.load_history,
            'measurable_parameter': self.measurable_parameter,
            'remarks': self.remarks
        }

        return _attributes

    def set_attributes(self, values):
        """
        Set the Stress data model attributes.

        :param dict values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKOpStress {0:d} attributes.". \
               format(self.stress_id)

        try:
            self.description = str(none_to_default(values['description'], ''))
            self.load_history = str(
                none_to_default(values['load_history'], ''))
            self.measurable_parameter = str(
                none_to_default(values['measurable_parameter'], ''))
            self.remarks = str(none_to_default(values['remarks'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKOpStress.set_attributes().".format(_err)

        return _error_code, _msg
