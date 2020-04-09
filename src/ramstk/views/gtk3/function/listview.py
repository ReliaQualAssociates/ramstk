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
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView, do_make_buttonbox


class FunctionHardware(RAMSTKListView):
    """
    Display all the Function-Hardware matrix for the selected Revision.

    The attributes of the Function-Hardware Matrix View are:
    """
    def __init__(self, configuration, logger, module='fnctn_hrdwr') -> None:
        """
        Initialize the List View for the Failure Definition package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger, module)
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_matrix, 'retrieved_matrix')

    def __make_buttonbox(self) -> Gtk.ButtonBox:
        """
        Make the buttonbox for the Failure Definition List View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Failure Definition
            List View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _("Refresh the matrix view.")
        ]
        _callbacks = [self._do_request_refresh]
        _icons = ['refresh-view']

        _buttonbox = do_make_buttonbox(self,
                                       icons=_icons,
                                       tooltips=_tooltips,
                                       callbacks=_callbacks,
                                       orientation='vertical',
                                       height=-1,
                                       width=-1)

        return _buttonbox

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.tab_label.set_markup("<span weight='bold'>"
                                  + _("Function-Hardware\nMatrix") + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays the Function-Hardware matrix for the selected "
              "revision."))

        self.pack_start(self.__make_buttonbox(), False, False, 0)

        super().make_ui(vtype='matrix')

    def __set_properties(self) -> None:
        """
        Set properties of the Function::Hardware Matrix View and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_tooltip_text(
            _("Displays the Function-Hardware matrix for the selected "
              "revision."))

    @staticmethod
    def _do_load_matrix() -> None:
        """
        Load the RAMSTKMatrixView() with matrix data.

        :return: None
        :rtype: None
        """
        pub.sendMessage('request_create_matrix')

    @staticmethod
    def _do_request_refresh(__button: Gtk.Button) -> None:
        """
        Refresh the RAMSTKMatrixView().

        :return: None
        :rtype: None
        """
        pub.sendMessage('request_create_matrix')
