# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Validation List View Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView


class ValidationRequirement(RAMSTKListView):
    """
    Display all the Validation::Requirement matrix for the selected Revision.

    The attributes of the Validation::Requirement Matrix View are:
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'vldtn_rqrmnt') -> None:
        """
        Initialize the List View for the Validation package.

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
                        tab_label=_("VValidation::Requirement\nMatrix"),
                        tooltip=_("Displays the Validation::Requirement "
                                  "matrix for the selected revision."))

        # Subscribe to PyPubSub messages.

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Validation::Requirement matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='vldtn_rqrmnt')
        super().do_set_cursor_active()

    def _do_request_update_all(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Validation::Requirement matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='vldtn_rqrmnt')
        super().do_set_cursor_active()
