# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecord.baserecord.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Metaclasses for the database Record model."""

# RAMSTK Package Imports
from ramstk.utilities import none_to_default


class RAMSTKBaseRecord:
    """Metaclass for all RAMSTK Record models."""

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
            setattr(
                self,
                _key,
                none_to_default(attributes[_key], self.__defaults__[_key]),
            )
