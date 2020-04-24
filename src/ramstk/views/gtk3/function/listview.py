# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Definition List View Module."""


# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKListView


class FunctionHardware(RAMSTKListView):
    """
    Display all the Function-Hardware matrix for the selected Revision.

    The attributes of the Function-Hardware Matrix View are:
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'fnctn_hrdwr') -> None:
        """
        Initialize the List View for the Failure Definition package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger, module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui(vtype='matrix',
                        tab_label=_("Function-Hardware\nMatrix"),
                        tooltip=_("Displays the Function-Hardware matrix for "
                                  "the selected revision."))

        # Subscribe to PyPubSub messages.
