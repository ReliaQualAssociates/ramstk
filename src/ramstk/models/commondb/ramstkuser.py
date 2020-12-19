# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKUser.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKUser Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKUser(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent the table ramstk_user in the RAMSTK Common database.

    This table shares a One-to-Many relationship with ramstk_workgroup.
    """

    __defaults__ = {
        'user_lname': 'Last Name',
        'user_fname': 'First Name',
        'user_email': 'EMail',
        'user_phone': '867.5309',
        'user_group_id': '0'
    }
    __tablename__ = 'ramstk_user'
    __table_args__ = {'extend_existing': True}

    user_id = Column(
        'fld_user_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    user_lname = Column('fld_user_lname',
                        String(256),
                        default=__defaults__['user_lname'])
    user_fname = Column('fld_user_fname',
                        String(256),
                        default=__defaults__['user_fname'])
    user_email = Column('fld_user_email',
                        String(256),
                        default=__defaults__['user_email'])
    user_phone = Column('fld_user_phone',
                        String(256),
                        default=__defaults__['user_phone'])
    user_group_id = Column('fld_user_group_id',
                           String(256),
                           default=__defaults__['user_group_id'])

    def get_attributes(self):
        """Retrieve the current values of the RAMSTKUser data model attributes.

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
