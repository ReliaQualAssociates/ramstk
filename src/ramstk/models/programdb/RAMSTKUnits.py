# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKUnit.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKUnit Table"""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import error_handler, none_to_default


class RAMSTKUnits(RAMSTK_BASE):
    """
    Class to represent the table ramstk_unit in the RAMSTK Common database.
    """

    __tablename__ = 'ramstk_unit'
    __table_args__ = {'extend_existing': True}

    unit_id = Column(
        'fld_unit_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    code = Column('fld_code', String(256), default='Unit Code')
    description = Column(
        'fld_description', String(512), default='Unit Description',
    )
    unit_type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RAMSTKUnit data model
        attributes.

        :return: (unit_id, code, description, unit_type)
        :rtype: tuple
        """

        _values = (self.unit_id, self.code, self.description, self.unit_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RAMSTKUnit data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKUnit {0:d} attributes.". \
            format(self.unit_id)

        try:
            self.code = str(none_to_default(attributes[0], 'Unit Code'))
            self.description = str(
                none_to_default(attributes[2], 'Unit Description'),
            )
            self.unit_type = str(none_to_default(attributes[2], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKUnit.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKUnit attributes."

        return _error_code, _msg
