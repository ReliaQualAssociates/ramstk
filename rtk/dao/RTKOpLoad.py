# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKOpLoad.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKOpLoad Table
===============================================================================
"""

from sqlalchemy import Column, ForeignKey, \
                       Integer, String              # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKOpLoad(RTK_BASE):
    """
    Class to represent the table rtk_op_load in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mechanism.
    This table shares a One-to-Many relationship with rtk_op_stress.
    """

    __tablename__ = 'rtk_op_load'
    __table_args__ = {'extend_existing': True}

    mechanism_id = Column('fld_mechanism_id', Integer,
                          ForeignKey('rtk_mechanism.fld_mechanism_id'),
                          nullable=False)
    load_id = Column('fld_load_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    damage_model = Column('fld_damage_model', Integer, default=0)
    priority_id = Column('fld_priority_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mechanism = relationship('RTKMechanism', back_populates='op_load')
    op_stress = relationship('RTKOpStress', back_populates='op_load')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKOpLoad data model
        attributes.

        :return: (mechanism_id, load_id, description, damage_model,
                  priority_id)
        :rtype: tuple
        """

        _attributes = (self.mechanism_id, self.load_id, self.description,
                       self.damage_model, self.priority_id)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKOpLoad data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKOpLoad {0:d} attributes.". \
               format(self.load_id)

        try:
            self.description = str(none_to_default(attributes[0], ''))
            self.damage_model = int(none_to_default(attributes[1], 0))
            self.priority_id = int(none_to_default(attributes[2], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKOpLoad.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKOpLoad attributes."

        return _error_code, _msg
