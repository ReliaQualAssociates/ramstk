# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKUser.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKUser Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKUser(RAMSTK_BASE):
    """
    Class to represent the table ramstk_user in the RAMSTK Common database.

    This table shares a One-to-Many relationship with ramstk_workgroup.
    """

    __tablename__ = 'ramstk_user'
    __table_args__ = {'extend_existing': True}

    user_id = Column(
        'fld_user_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    user_lname = Column('fld_user_lname', String(256), default='Last Name')
    user_fname = Column('fld_user_fname', String(256), default='First Name')
    user_email = Column('fld_user_email', String(256), default='EMail')
    user_phone = Column('fld_user_phone', String(256), default='867.5309')
    user_group_id = Column('fld_user_group', String(256), default='0')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKUser data model attributes.

        :return: {user_id, user_lname, user_fname, user_email, user_phone,
                  user_group_id} pairs.
        :rtype: dict
        """
        _attributes = {
            'user_id': self.user_id,
            'user_lname': self.user_lname,
            'user_fname': self.user_fname,
            'user_email': self.user_email,
            'user_phone': self.user_phone,
            'user_group_id': self.user_group_id,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKUser data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKUser {0:d} attributes.".\
            format(self.user_id)

        try:
            self.user_lname = str(
                none_to_default(attributes['user_lname'], 'Last Name'),
            )
            self.user_fname = str(
                none_to_default(attributes['user_fname'], 'First Name'),
            )
            self.user_email = str(
                none_to_default(attributes['user_email'], 'EMail'),
            )
            self.user_phone = str(
                none_to_default(attributes['user_phone'], '867.5309'),
            )
            self.user_group_id = str(
                none_to_default(attributes['user_group_id'], '0'),
            )
        except KeyError as _err:
            _error_code = 40
            _msg = (
                "RAMSTK ERROR: Missing attribute {0:s} in attribute "
                "dictionary passed to "
                "{1:s}.set_attributes()."
            ).format(
                str(_err),
                self.__class__.__name__,
            )

        return _error_code, _msg
