# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.basebook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 basebook."""

# Standard Library Imports
import locale
from typing import Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.views.gtk3 import Gdk, GObject, Gtk, _


def destroy(__widget: Gtk.Widget, __event: Gdk.Event = None) -> None:
    """
    Quit the RAMSTK application.

    This function quits the RAMSTK application when the X in the upper right
    corner is pressed or if this function is called as a callback.

    :param __widget: the Gtk.Widget() that called this method.
    :type __widget: :class:`Gtk.Widget`
    :keyword __event: the Gdk.Event() that called this method.
    :type __event: :class:`Gdk.Event`
    :return: None
    :rtype: None
    """
    Gtk.main_quit()


class RAMSTKBook(Gtk.Window):
    """
    The base view for the multiple window interface Books.

    This is the base class for the List Book, Module Book, and Work Book.
    Attributes of the RAMSTKBook are:

    :cvar RAMSTK_CONFIGURATION: the instance of the RAMSTK Configuration class.
    :type RAMSTK_CONFIGURATION: :class:`ramstk.configuration.RAMSTKUserConfiguration`
    :cvar dict dic_books: dictionary holding a reference to each RAMSTK book.
    :cvar dict dic_tab_pos: dictionary holding the Gtk.PositionType()s for each
        of left, right, top, and botton.
    :ivar list _lst_handler_id: the list of widget callback handler IDs.
    :ivar int _n_screens: the number of monitors attached to the machine
        running RAMSTK.
    :ivar float _height: the height of the monitors attached to the machine
        running RAMSTK.
    :ivar float _width: the average width of each monitor attached to the
        machine running RAMSTK.
    :ivar notebook: the Gtk.Notebook() widget used to hold each of the RAMSTK
        module WorkViews.
    :type notebook: :class:`Gtk.Notebook`
    :ivar menubar: the Gtk.MenuBar() for the RAMSTK ModuleBook menu.
    :type menubar: :class:`Gtk.MenuBar`
    :ivar progressbar: the Gtk.Progressbar() for displaying progress counters.
    :type progressbar: :class:`Gtk.Progressbar`
    :ivar statusbar: the Gtk.Statusbar() for displaying messages.
    :type statusbar: :class:`Gtk.Statusbar`
    :ivar toolbar: the Gtk.Toolbar() for the RAMSTK ModuleBook tools.
    :type toolbar: :class:`Gtk.Toolbar`
    """

    RAMSTK_USER_CONFIGURATION = None

    dic_books: Dict[str, object] = {}
    dic_tab_position = {
        'left': Gtk.PositionType.LEFT,
        'right': Gtk.PositionType.RIGHT,
        'top': Gtk.PositionType.TOP,
        'bottom': Gtk.PositionType.BOTTOM
    }

    def __init__(self, configuration: RAMSTKUserConfiguration) -> None:
        """
        Initialize an instance of the RAMSTK Book.

        :param configuration: the RAMSTK user configuration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        """
        GObject.GObject.__init__(self)  # pylint: disable=non-parent-init-called
        self.RAMSTK_USER_CONFIGURATION = configuration

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id: List[int] = []

        # Initialize private scalar attributes.
        try:
            _screen = Gdk.Screen.get_default()
            _display = _screen.get_display()
            _monitor = _display.get_monitor(0)
            self._n_screens = _display.get_n_monitors()
            self._height = _monitor.get_geometry().height
            self._width = _monitor.get_geometry().width
        except AttributeError:
            # When running on CI servers, there will be no monitor.  We also
            # don't need one.
            self._n_screens = 0
            self._height = -1
            self._width = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.menubar = Gtk.MenuBar()
        self.notebook = Gtk.Notebook()
        self.progressbar = Gtk.ProgressBar()
        self.statusbar = Gtk.Statusbar()
        self.toolbar = Gtk.Toolbar()

        try:
            locale.setlocale(locale.LC_ALL,
                             self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Set the common properties for the Book and it's widgets.
        self.set_resizable(True)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.NONE)

        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_request_open, 'request_open_program ')

    def __set_callbacks(self) -> None:
        """
        Set the callback functions/methods for the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        self.connect('delete_event', destroy)
        self.connect('window_state_event', self._on_window_state_event)

    def on_module_change(self) -> None:
        """
        Load correct Views for the RAMSTK module selected in the Module Book.

        :return: None
        :rtype: None
        """
        # We remove any existing pages from the Book.  New pages will be added
        # by the List Book and the Work Book for the module that was just
        # selected.
        _n_pages = self.notebook.get_n_pages()
        if _n_pages > 0:
            for _page in list(range(_n_pages)):
                self.notebook.remove_page(-1)

    def _on_request_open(self) -> None:
        """
        Set the status bar and update the progress bar.

        :return: None
        :rtype: None
        """
        _message = _("Opening Program Database {0:s}"). \
            format(self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        self.statusbar.push(1, _message)
        self.set_title(
            _("RAMSTK - Analyzing {0:s}").format(
                self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database']))

    def _on_window_state_event(self, window: Gtk.Window,
                               event: Gdk.EventWindowState) -> None:
        """
        Iconify or deiconify all three books together.

        :return: None
        :rtype: None
        """
        if event.new_window_state == Gdk.WindowState.ICONIFIED:
            for _window in self.dic_books.items():
                _window[1].iconify()
        elif event.new_window_state == 0:
            for _window in self.dic_books.items():
                _window[1].deiconify()
        elif event.new_window_state == Gdk.WindowState.MAXIMIZED:
            window.maximize()
