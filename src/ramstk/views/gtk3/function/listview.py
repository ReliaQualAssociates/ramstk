# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Definition List View Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView


class FunctionHardware(RAMSTKListView):
    """
    Display all the Function::Hardware matrix for the selected Revision.

    The attributes of the Function::Hardware Matrix View are:
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'fnctn_hrdwr') -> None:
        """
        Initialize the List View for the Function package.

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
                        tab_label=_("Function::Hardware\nMatrix"),
                        tooltip=_("Displays the Function::Hardware matrix for "
                                  "the selected revision."))

        # Subscribe to PyPubSub messages.

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Function::Hardware matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='fnctn_hrdwr')
        super().do_set_cursor_active()

    def _do_request_update_all(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Function::Hardware matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='fnctn_hrdwr')
        super().do_set_cursor_active()
