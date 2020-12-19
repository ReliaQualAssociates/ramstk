# -*- coding: utf-8 -*-
#
#       ramstk.models.tables.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKBaseTable Module."""

# RAMSTK Package Imports
from ramstk.utilities import none_to_default


class RAMSTKBaseTable:
    """Meta-class for RAMSTK Common and Program database tables."""
    def set_attributes(self, attributes):
        """Set one or more RAMSTK<Table> attributes.

        .. note:: you should pop the primary and foreign key entries from the
            attributes dict before passing it to this method.

        :param attributes: dict of key:value pairs to assign to the
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
