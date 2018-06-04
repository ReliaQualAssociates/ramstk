# -*- coding: utf-8 -*-
#
#       rtk.dao.programdb.RTKOpLoad.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKOpLoad Table Module."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKOpLoad(RTK_BASE):
    """
    Class to represent the table rtk_op_load in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mechanism.
    This table shares a One-to-Many relationship with rtk_op_stress.
    This table shares a One-to-Many relationship with rtk_test_method.
    """

    __tablename__ = 'rtk_op_load'
    __table_args__ = {'extend_existing': True}

    mechanism_id = Column(
        'fld_mechanism_id',
        Integer,
        ForeignKey('rtk_mechanism.fld_mechanism_id'),
        nullable=False)
    load_id = Column(
        'fld_load_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    damage_model = Column('fld_damage_model', String(512), default='')
    priority_id = Column('fld_priority_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mechanism = relationship('RTKMechanism', back_populates='op_load')
    op_stress = relationship(
        'RTKOpStress', back_populates='op_load', cascade='all,delete')
    test_method = relationship(
        'RTKTestMethod', back_populates='op_load', cascade='all,delete')

    is_mode = False
    is_mechanism = False
    is_opload = True
    is_opstress = False
    is_testmethod = False

    def get_attributes(self):
        """
        Retrieve the current values of the RTKOpLoad data model attributes.

        :return: {mechanism_id, load_id, description, damage_model,
                  priority_id} pairs
        :rtype: dict
        """

        _attributes = {
            'mechanism_id': self.mechanism_id,
            'load_id': self.load_id,
            'description': self.description,
            'damage_model': self.damage_model,
            'priority_id': self.priority_id
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the RTKOpLoad data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKOpLoad {0:d} attributes.". \
               format(self.load_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.damage_model = str(
                none_to_default(attributes['damage_model'], ''))
            self.priority_id = int(
                none_to_default(attributes['priority_id'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKOpLoad.set_attributes().".format(_err)

        return _error_code, _msg
