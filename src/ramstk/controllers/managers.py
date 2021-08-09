# -*- coding: utf-8 -*-
#
#       ramstk.models.manager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package managers."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
# noinspection PyPackageRequirements
import treelib

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration


class RAMSTKAnalysisManager:
    """Contain the attributes and methods of an analysis manager.

    This class manages the analyses for RAMSTK modules.  Attributes of the
    analysis manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    :ivar tree: the treelib Tree() used to hold a copy of the data manager's
        tree.  This do not remain in-sync automatically.
    :type tree: :class:`treelib.Tree`
    :ivar RAMSTK_USER_CONFIGURATION: the instance of the
        RAMSTKUserConfiguration class associated with this analysis manager.
    :type RAMSTK_USER_CONFIGURATION: :class:`ramstk.RAMSTKUserConfiguration`
    """

    RAMSTK_USER_CONFIGURATION = None

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(
        self, configuration: RAMSTKUserConfiguration, **kwargs: Dict[str, Any]
    ) -> None:
        """Initialize an instance of the hardware analysis manager.

        :param configuration: the RAMSTKUserConfiguration instance associated
            with the current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.RAMSTKUserConfiguration`
        """
        # Initialize private dictionary attributes.
        self._attributes: Dict[str, Any] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

    def on_get_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes for the analysis manager.

        :param attributes: the data manager's attributes dict.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def on_get_tree(self, tree: treelib.Tree) -> None:
        """Set the analysis manager's treelib Tree().

        :param tree: the data manager's treelib Tree().
        :return: None
        :rtype: None
        """
        self._tree = tree
