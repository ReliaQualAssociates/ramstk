# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Function List View Module."""

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKListView


class FunctionHardware(RAMSTKListView):
    """
    Display all the Function::Hardware matrix for the selected Revision.

    The attributes of the Function::Hardware Matrix View are:

    :cvar str _module: the name of the module.
    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private scalar class attributes.
    _module: str = 'fnctn_hrdwr'
    _tablabel = "<span weight='bold'>" + _(
        "Function::Hardware\nMatrix") + "</span>"
    _tabtooltip = _("Displays the Function::Hardware matrix "
                    "for the selected revision.")
    _view_type: str = 'matrix'

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the List View for the Function package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._lst_callbacks = [self.do_request_update]
        self._lst_icons = ['save']
        self._lst_mnu_labels = [_("Save Matrix")]
        self._lst_tooltips = [
            _("Save changes to the Function::Hardware matrix.")
        ]

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()

        # Subscribe to PyPubSub messages.
