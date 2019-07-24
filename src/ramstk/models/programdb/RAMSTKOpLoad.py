# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKOpLoad.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKOpLoad Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKOpLoad(RAMSTK_BASE):
    """
    Class to represent table ramstk_op_load in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mechanism.
    This table shares a One-to-Many relationship with ramstk_op_stress.
    This table shares a One-to-Many relationship with ramstk_test_method.
    """

    __defaults__ = {
        'description': '',
        'damage_model': '',
        'priority_id': 0
    }
    __tablename__ = 'ramstk_op_load'
    __table_args__ = {'extend_existing': True}

    mechanism_id = Column(
        'fld_mechanism_id',
        Integer,
        ForeignKey('ramstk_mechanism.fld_mechanism_id'),
        nullable=False,
    )
    load_id = Column(
        'fld_load_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column('fld_description', String(512), default=__defaults__['description'])
    damage_model = Column('fld_damage_model', String(512), default=__defaults__['damage_model'])
    priority_id = Column('fld_priority_id', Integer, default=__defaults__['priority_id'])

    # Define the relationships to other tables in the RAMSTK Program database.
    mechanism = relationship('RAMSTKMechanism', back_populates='op_load')
    op_stress = relationship(
        'RAMSTKOpStress', back_populates='op_load', cascade='all,delete',
    )
    test_method = relationship(
        'RAMSTKTestMethod', back_populates='op_load', cascade='all,delete',
    )

    is_mode = False
    is_mechanism = False
    is_opload = True
    is_opstress = False
    is_testmethod = False

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKOpLoad data model attributes.

        :return: {mechanism_id, load_id, description, damage_model,
                  priority_id} pairs
        :rtype: dict
        """
        _attributes = {
            'mechanism_id': self.mechanism_id,
            'load_id': self.load_id,
            'description': self.description,
            'damage_model': self.damage_model,
            'priority_id': self.priority_id,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKOpLoad attributes.

        .. note:: you should pop the mechanism ID and load ID entries from
            the attributes dict before passing it to this method.

        :param dict attributes: dict of key:value pairs to assign to the
            instance attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(self, _key,
                    none_to_default(attributes[_key], self.__defaults__[_key]))
