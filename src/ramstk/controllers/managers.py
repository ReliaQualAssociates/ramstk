# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.AnalysisManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package analysis manager."""

# Standard Library Imports
from collections import OrderedDict
from math import exp

# Third Party Imports
from pubsub import pub


class RAMSTKAnalysisManager():
    """
    Contain the attributes and methods of an analysis manager.

    This class manages the analyses for RAMSTK modules.  Attributes of the
    analysis manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    :ivar tree: the treelib Tree() used to hold a copy of the data manager's
        tree.  This do not remain in-sync automatically.
    :type tree: :class:`treelib.Tree`
    :ivar RAMSTK_CONFIGURATION: the instance of the Configuration class
        associated with this analysis manager.
    :type RAMSTK_CONFIGURATION: :class:`ramstk.configuration.Configuration`
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the hardware analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        # Initialize private dictionary attributes.
        self._attributes = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._tree = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_CONFIGURATION = configuration

    def on_get_all_attributes(self, attributes):
        """
        Set all the attributes for the analysis manager.

        :param dict attributes: the data manager's attributes dict.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def on_get_tree(self, tree):
        """
        Set the analysis manager's treelib Tree().

        :param tree: the data manager's treelib Tree().
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._tree = tree
