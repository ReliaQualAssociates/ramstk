# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Requirement List View Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView


class RequirementHardware(RAMSTKListView):
    """Display all the Requirement::Hardware matrix for the selected Revision.

    The attributes of the Requirement::Hardware Matrix View are:

    :cvar _module: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private scalar class attributes.
    _module: str = 'rqrmnt_hrdwr'
    _tablabel = "<span weight='bold'>" + _(
        "Requirement::Hardware\nMatrix") + "</span>"
    _tabtooltip = _("Displays the Requirement::Hardware matrix "
                    "for the selected revision.")
    _view_type = 'matrix'

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the List View for the Requirement package.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [self.do_request_update]
        self._lst_icons = ['save']
        self._lst_mnu_labels = [_("Save Matrix")]
        self._lst_tooltips = [
            _("Save changes to the Requirement::Hardware matrix.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()

        # Subscribe to PyPubSub messages.

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """Send message to request updating the Requirement::Hardware matrix.

        :param __button: the Gtk.Button() that call this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        matrix_type='rqrmnt_hrdwr')

    def _do_request_update_all(self, __button: Gtk.Button) -> None:
        """Send message to request updating the Requirement::Hardware matrix.

        :param __button: the Gtk.Button() that call this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        matrix_type='rqrmnt_hrdwr')
