# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Book.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Base RAMSTK Book."""

# Modules for localization support.
import locale

# Import the ramstk.Widget base class.
from .Widget import Gdk, Gtk, GObject


def destroy(__widget, __event=None):
    """
    Quit the RAMSTK application.

    This function quits the RAMSTK application when the X in the upper right
    corner is pressed or if this function is called as a callback.

    :param __widget: the Gtk.Widget() that called this method.
    :type __widget: :py:class:`Gtk.Widget`
    :keyword __event: the Gdk.Event() that called this method.
    :type __event: :py:class:`Gdk.Event`
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """
    Gtk.main_quit()

    return False


class RAMSTKBook(Gtk.Window):  # pylint: disable=R0904
    """
    The base view for the pyGTK multiple window interface Books.

    This is the base class for the List Book, Module Book, and Work Book.
    Attributes of the RAMSTKBook are:

    :ivar list _lst_handler_id:
    :ivar _mdcRAMSTK: the RAMSTK master data controller.
    :type _mdcRAMSTK: :py:class:`ramstk.RAMSTK.RAMSTK`
    :ivar notebook: the Gtk.Notebook() widget used to hold each of the RAMSTK
                    module WorkViews.
    :type notebook: :py:class:`Gtk.Notebook`
    :ivar menubar: the Gtk.MenuBar() for the RAMSTK ModuleBook menu.
    :type menubar: :py:class:`Gtk.MenuBar`
    :ivar toolbar: the Gtk.Toolbar() for the RAMSTK ModuleBook tools.
    :type toolbar: :py:class:`Gtk.Toolbar`
    :ivar statusbar: the Gtk.Statusbar() for displaying messages.
    :type statusbar: :py:class:`Gtk.Statusbar`
    :ivar progressbar: the Gtk.Progressbar() for displaying progress counters.
    :type progressbar: :py:class:`Gtk.Progressbar`
    """

    _left_tab = Gtk.PositionType.LEFT
    _right_tab = Gtk.PositionType.RIGHT
    _top_tab = Gtk.PositionType.TOP
    _bottom_tab = Gtk.PositionType.BOTTOM

    def __init__(self, controller):
        """
        Initialize an instance of the RAMSTK Book.

        :param controller: the RAMSTK master data controller.
        :type controller: :py:class:`ramstk.RAMSTK.RAMSTK`
        """
        GObject.GObject.__init__(self)      # pylint: disable=non-parent-init-called

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRAMSTK = controller
        self._n_screens = Gdk.Screen.get_default().get_n_monitors()
        self._width = Gdk.Screen.width() / self._n_screens
        self._height = Gdk.Screen.height()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.notebook = Gtk.Notebook()

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RAMSTK_CONFIGURATION.RAMSTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Set the common properties for the Book and it's widgets.
        self.set_resizable(True)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.NONE)

        self.connect('delete_event', destroy)

    def _on_module_change(self, module=''):  # pylint: disable=unused-argument
        """
        Load the correct Views for the RAMSTK module selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # We remove any existing pages from the Book.  New pages will be added
        # by the List Book and the Work Book for the module that was just
        # selected.
        _n_pages = self.notebook.get_n_pages()
        if _n_pages > 0:
            for _page in list(range(_n_pages)):  # pylint: disable=E0602
                self.notebook.remove_page(-1)

        return _return
