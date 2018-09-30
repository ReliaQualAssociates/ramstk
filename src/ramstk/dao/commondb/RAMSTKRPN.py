# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKRPN.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKRPN Table"""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import error_handler, none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKRPN(RAMSTK_BASE):
    """
    Class to represent the table ramstk_rpn in the RAMSTK Common database.
    """

    __tablename__ = 'ramstk_rpn'
    __table_args__ = {'extend_existing': True}

    rpn_id = Column(
        'fld_rpn_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    name = Column('fld_name', String(512), default='RPN Name')
    description = Column(
        'fld_description', String(512), default='RPN Description')
    rpn_type = Column('fld_type', String(256), default='')
    value = Column('fld_value', Integer, default=0)

    def get_attributes(self):
        """
        RPN to retrieve the current values of the RAMSTKRPN data
        model attributes.

        :return: (rpn_id, name, description, rpn_type, value)
        :rtype: tuple
        """

        _values = (self.rpn_id, self.name, self.description, self.rpn_type,
                   self.value)

        return _values

    def set_attributes(self, attributes):
        """
        RPN to set the current values of the RAMSTKRPN data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKRPN {0:d} attributes.". \
            format(self.rpn_id)

        try:
            self.name = str(none_to_default(attributes[0], 'RPN Name'))
            self.description = str(
                none_to_default(attributes[1], 'RPN Description'))
            self.rpn_type = str(none_to_default(attributes[2], ''))
            self.value = int(none_to_default(attributes[3], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKRPN.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKRPN attributes."

        return _error_code, _msg
