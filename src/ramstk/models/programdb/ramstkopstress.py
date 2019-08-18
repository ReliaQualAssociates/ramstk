# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKOpStress.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKOpStress Table."""

# Third Party Imports
from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKOpStress(RAMSTK_BASE, RAMSTKBaseTable):
    """
    Class to represent table ramstk_op_stress in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_op_load.
    """

    __defaults__ = {
        'description': '',
        'load_history': '',
        'measurable_parameter': '',
        'remarks': b''
    }
    __tablename__ = 'ramstk_op_stress'
    __table_args__ = {'extend_existing': True}

    load_id = Column(
        'fld_load_id',
        Integer,
        ForeignKey('ramstk_op_load.fld_load_id'),
        nullable=False,
    )
    stress_id = Column(
        'fld_stress_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    load_history = Column('fld_load_history',
                          String(512),
                          default=__defaults__['load_history'])
    measurable_parameter = Column('fld_measurable_parameter',
                                  String(512),
                                  default=__defaults__['measurable_parameter'])
    remarks = Column('fld_remarks', BLOB, default=__defaults__['remarks'])

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
            'remarks': self.remarks,
        }

        return _attributes
