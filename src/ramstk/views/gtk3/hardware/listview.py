# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.listview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Hardware GTK3 list view."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView


class HardwareRequirement(RAMSTKListView):
    """
    Display all the Hardware::Requirement matrix for the selected Revision.

    The attributes of the Hardware::Requirement Matrix View are:
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'hrdwr_rqrmnt') -> None:
        """
        Initialize the List View for the Hardware package.

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
                        tab_label=_("Hardware::Requirement\nMatrix"),
                        tooltip=_("Displays the Hardware::Requirement matrix "
                                  "for the selected revision."))

        # Subscribe to PyPubSub messages.

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Hardware::Requirement matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='hrdwr_rqrmnt')

    def _do_request_update_all(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Hardware::Requirement matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='hrdwr_rqrmnt')


class HardwareValidation(RAMSTKListView):
    """
    Display all the Hardware::Validation matrix for the selected Revision.

    The attributes of the Hardware::Validation Matrix View are:
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'hrdwr_vldtn') -> None:
        """
        Initialize the List View for the Hardware package.

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
                        tab_label=_("Hardware::Validation\nMatrix"),
                        tooltip=_("Displays the Hardware::Validation matrix "
                                  "for the selected revision."))

        # Subscribe to PyPubSub messages.

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Hardware::Validation matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='hrdwr_vldtn')

    def _do_request_update_all(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Hardware::Validation matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='hrdwr_vldtn')
