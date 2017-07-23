#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKOpLoad.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKOpLoad Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKOpLoad(Base):
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
            self.description = str(attributes[0])
            self.damage_model = int(attributes[1])
            self.priority_id = int(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKOpLoad.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKOpLoad attributes."

        return _error_code, _msg
