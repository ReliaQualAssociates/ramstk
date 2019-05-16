# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Book.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Base RAMSTK Book."""

# Modules for localization support.
import locale

from pubsub import pub

# Import the ramstk.Widget base class.
from .Widget import _, Gdk, Gtk, GObject


def destroy(__widget, __event=None):
    """
    Quit the RAMSTK application.

    This function quits the RAMSTK application when the X in the upper right
    corner is pressed or if this function is called as a callback.

    :param __widget: the Gtk.Widget() that called this method.
    :type __widget: :class:`Gtk.Widget`
    :keyword __event: the Gdk.Event() that called this method.
    :type __event: :class:`Gdk.Event`
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """
    Gtk.main_quit()

    return False


class RAMSTKBook(Gtk.Window):  # pylint: disable=R0904
    """
    The base view for the multiple window interface Books.

    This is the base class for the List Book, Module Book, and Work Book.
    Attributes of the RAMSTKBook are:

    :cvar RAMSTK_CONFIGURATION: the instance of the RAMSTK Configuration class.
    :type RAMSTK_CONFIGURATION: :class:`ramstk.Configuration.Configuration`
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

    RAMSTK_CONFIGURATION = None

    dic_books = {}
    dic_tab_position = {
        'left': Gtk.PositionType.LEFT,
        'right': Gtk.PositionType.RIGHT,
        'top': Gtk.PositionType.TOP,
        'bottom': Gtk.PositionType.BOTTOM
    }

    def __init__(self, configuration):
        """
        Initialize an instance of the RAMSTK Book.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)  # pylint: disable=non-parent-init-called
        self.RAMSTK_CONFIGURATION = configuration

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._n_screens = Gdk.Screen.get_default().get_n_monitors()
        self._height = Gdk.Screen.height()
        self._width = Gdk.Screen.width() / self._n_screens

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
                             self.RAMSTK_CONFIGURATION.RAMSTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Set the common properties for the Book and it's widgets.
        self.set_resizable(True)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.NONE)

        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_request_open, 'requestOpen')

    def __set_callbacks(self):
        """
        Set the callback functions/methods for the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        self.connect('delete_event', destroy)
        self.connect('window_state_event', self._on_window_state_event)

    def on_module_change(self, module=''):  # pylint: disable=unused-argument
        """
        Load the correct Views for the RAMSTK module selected in the Module Book.

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

    def _on_request_open(self):
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

    def _on_window_state_event(self, window, event):
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
