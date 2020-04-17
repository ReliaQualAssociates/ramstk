# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.desktop.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 basebook."""

# Standard Library Imports
import locale
from typing import TypeVar

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_FAILURE_PROBABILITY,
    RAMSTKSiteConfiguration, RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GdkPixbuf, GObject, Gtk, _
from ramstk.views.gtk3.assistants import CreateProject, OpenProject
from ramstk.views.gtk3.books import (
    RAMSTKListBook, RAMSTKModuleBook, RAMSTKWorkBook
)

Tconfiguration = TypeVar('Tconfiguration', RAMSTKUserConfiguration,
                         RAMSTKSiteConfiguration)


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


class RAMSTKDesktop(Gtk.Window):
    """
    The base view for the RAMSTK Books.

    This is the container class for the List Book, Module Book, and Work Book.
    Attributes of the RAMSTKDesktop are:

    :cvar RAMSTK_USER_CONFIGURATION: the instance of the RAMSTK
        user configuration class.
    :type RAMSTK_USER_CONFIGURATION: :class:`ramstk.configuration.RAMSTKUserConfiguration`
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

    def __init__(self, configuration: Tconfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the RAMSTK Book.

        :param list configuration: a list containing the RAMSTK user
            configuration and RAMSTK site configuration class instances.
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        GObject.GObject.__init__(self)  # pylint: disable=non-parent-init-called
        self.RAMSTK_USER_CONFIGURATION = configuration[0]

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

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
        self.progressbar = Gtk.ProgressBar()
        self.statusbar = Gtk.Statusbar()
        self.toolbar = Gtk.Toolbar()

        self.icoStatus = Gtk.StatusIcon()

        self.nbkListBook = RAMSTKListBook(configuration[0], logger)
        self.nbkModuleBook = RAMSTKModuleBook(configuration[0], logger)
        self.nbkWorkBook = RAMSTKWorkBook(configuration[0], logger)
        self.nbkWorkBook.RAMSTK_SITE_CONFIGURATION = configuration[1]

        self.nbkWorkBook.dic_work_views['function'][1].do_load_combobox(
            self.nbkWorkBook.RAMSTK_SITE_CONFIGURATION.RAMSTK_HAZARDS,
            self.nbkWorkBook.RAMSTK_SITE_CONFIGURATION.RAMSTK_SEVERITY,
            RAMSTK_FAILURE_PROBABILITY)

        try:
            locale.setlocale(locale.LC_ALL,
                             self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_request_open, 'request_open_program ')
        pub.subscribe(self._on_select, 'request_set_title')
        pub.subscribe(self._do_set_status, 'request_set_status')

    def __make_menu(self) -> None:
        """
        Make the menu for the Module Book.

        :return: None
        :rtype: None
        """
        self.menubar.append(self.__make_menu_file())
        self.menubar.append(self.__make_menu_edit())
        self.menubar.append(self.__make_menu_tools())

        self.menubar.show_all()

    def __make_menu_edit(self) -> Gtk.MenuItem:
        """
        Make the Edit menu.

        :return: the Edit menu.
        :rtype: :class:`Gtk.MenuItem`
        """
        _menu = Gtk.Menu()

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                             + '/16x16/preferences.png')
        _menu_item.set_label(_("_Preferences"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', Preferences,
        # self.RAMSTK_USER_CONFIGURATION)
        _menu.append(_menu_item)

        _menu_item = Gtk.MenuItem(label=_("_Edit"), use_underline=True)
        _menu_item.set_submenu(_menu)

        return _menu_item

    def __make_menu_file(self) -> Gtk.MenuItem:
        """
        Make the File menu.

        :return: the Tools menu.
        :rtype: :class:`Gtk.MenuItem`
        """
        _menu = Gtk.Menu()

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                             + '/16x16/new.png')
        _menu_item.set_label(_("New _Program"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', CreateProject,
                           self.RAMSTK_USER_CONFIGURATION)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                             + '/16x16/open.png')
        _menu_item.set_label(_("_Open"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', OpenProject,
                           self.RAMSTK_USER_CONFIGURATION)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                             + '/16x16/import.png')
        _menu_item.set_label(_("_Import Project"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', ImportProject,
        # self.RAMSTK_USER_CONFIGURATION)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                             + '/16x16/save.png')
        _menu_item.set_label(_("_Save"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', self._do_request_save_project)
        _menu.append(_menu_item)

        _menu_item = Gtk.MenuItem()
        _menu_item.set_label(_("_Close"))
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', self._do_request_close_project)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                             + '/16x16/exit.png')
        _menu_item.set_label(_("E_xit"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', destroy)
        _menu.append(_menu_item)

        _menu_item = Gtk.MenuItem()
        _menu_item.set_label(_("_File"))
        _menu_item.set_property('use_underline', True)
        _menu_item.set_submenu(_menu)

        return _menu_item

    def __make_menu_tools(self) -> Gtk.MenuItem:
        """
        Make the Tools menu.

        :return: the Tools menu.
        :rtype: :class:`Gtk.MenuItem`
        """
        _menu = Gtk.Menu()

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                             + '/16x16/options.png')
        _menu_item.set_label(_("_Options"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        # _menu_item.connect('activate', Options,
        # self.RAMSTK_USER_CONFIGURATION)
        _menu.append(_menu_item)

        _menu_item = Gtk.MenuItem(label=_("_Tools"), use_underline=True)
        _menu_item.set_submenu(_menu)

        return _menu_item

    def __make_toolbar(self) -> None:
        """
        Make the toolbar for the Module Book.

        :return: None
        :rtype: None
        """
        _icon_dir = self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR

        _position = 0

        # New file button.
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(_("Create a new RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/new.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', CreateProject,
                        self.RAMSTK_USER_CONFIGURATION)
        self.toolbar.insert(_button, _position)
        _position += 1

        # Connect button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _("Connect to an existing RAMSTK Program Database."), )
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/open.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', OpenProject, self.RAMSTK_USER_CONFIGURATION,
                        self)
        self.toolbar.insert(_button, _position)
        _position += 1

        # Close button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(_("Closes the open RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/close.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_close_project)
        self.toolbar.insert(_button, _position)
        _position += 1

        self.toolbar.insert(Gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _("Save the currently open RAMSTK Project Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_save_project)
        self.toolbar.insert(_button, _position)
        _position += 1

        self.toolbar.insert(Gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save and quit button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _("Save the currently open RAMSTK Program Database then quits."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/save-exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_save_project, True)
        self.toolbar.insert(_button, _position)
        _position += 1

        # Quit without saving button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _("Quits without saving the currently open RAMSTK Program "
              "Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', destroy)
        self.toolbar.insert(_button, _position)

        self.toolbar.show_all()

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.__make_menu()
        self.__make_toolbar()

        _vbox = Gtk.VBox()
        _vbox.pack_start(self.menubar, False, False, 0)
        _vbox.pack_start(self.toolbar, False, False, 0)

        _hpaned = Gtk.HPaned()
        _hpaned.pack1(self.nbkModuleBook, True, False)
        _hpaned.pack2(self.nbkListBook, True, False)

        _vpaned = Gtk.VPaned()
        _vpaned.pack1(_hpaned)
        _vpaned.pack2(self.nbkWorkBook, True, False)

        _vbox.pack_start(_vpaned, True, True, 0)
        _vbox.pack_start(self.statusbar, False, False, 0)

        self.add(_vbox)
        self.show_all()

        self.nbkModuleBook.set_current_page(0)

        self.statusbar.push(1, _("Ready"))
        self._do_set_status_icon()

    def __set_callbacks(self) -> None:
        """
        Set the callback functions/methods for the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        self.connect('delete_event', destroy)
        self.connect('window_state_event', self._on_window_state_event)
        self.connect('button_press_event', self._on_button_press)

    def __set_properties(self) -> None:
        """
        Set properties of the RAMSTKBook and widgets.

        :return: None
        :rtype: None
        """
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.NONE)
        self.set_resizable(True)

        _width = 15 * self._width / 16
        _height = 15 * self._height / 16
        self.resize(_width, _height)
        self.move(50, 5)

    @staticmethod
    def _do_request_close_project(__widget: Gtk.Widget) -> None:
        """
        Request to close the open RAMSTK Program.

        :param Gtk.Widget __widget: the Gtk.Widget() that called this method.
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_close_project')

    # noinspection PyDeepBugsSwappedArgs
    def _do_request_save_project(self, widget: Gtk.Widget,
                                 end: bool = False) -> None:
        """
        Request to save the open RAMSTK Program.

        :param Gtk.Widget widget: the Gtk.Widget() that called this method.
        :keyword bool end: indicates whether or not to quit RAMSTK after saving
            the project.
        :return: None
        :rtype: None
        """
        _message = _("Saving Program Database {0:s}"). \
            format(self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        self.statusbar.push(2, _message)

        pub.sendMessage('request_save_project')

        self.dic_books['modulebook'].statusbar.pop(2)

        if end:
            destroy(widget)

    def _do_set_status(self, status: str) -> None:
        """
        Set the status message.

        :param str status: the status message to display.
        :return: None
        :rtype: None
        """
        self.statusbar.push(1, status)

    def _do_set_status_icon(self, connected: bool = False) -> None:
        """
        Set the status icon in the system tay to indicate connection status.

        :param bool connected: whether or not RAMSTK is connected to a program
            database.
        :return: None
        :rtype: None
        """
        if connected:
            _icon = (self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                     + '/32x32/db-connected.png')
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(_icon, 22, 22)
            self.icoStatus.set_from_pixbuf(_icon)
            self.icoStatus.set_tooltip_markup(
                _(u"RAMSTK is connected to program database "
                  u"{0:s}.".format(self.RAMSTK_USER_CONFIGURATION.
                                   RAMSTK_PROG_INFO['database'])))
        else:
            _icon = (self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                     + '/32x32/db-disconnected.png')
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(_icon, 22, 22)
            self.icoStatus.set_from_pixbuf(_icon)
            self.icoStatus.set_tooltip_markup(
                _(u"RAMSTK is not currently connected to a "
                  u"project database."))

    def _on_button_press(self, __book: object, event: Gdk.EventButton) -> None:
        """
        Handle mouse clicks on the RAMSTKBook.

        :param __book: the RAMSTKBook that was 'clicked'.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backward
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`
        :return: None
        :rtype: None
        """
        if event.button == 1:
            self.present()

    def _on_request_open(self) -> None:
        """
        Set the status bar and update the progress bar.

        :return: None
        :rtype: None
        """
        _message = _("Opening Program Database {0:s}"). \
            format(self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        # noinspection PyDeepBugsSwappedArgs
        self.statusbar.push(1, _message)
        self.set_title(
            _("RAMSTK - Analyzing {0:s}").format(
                self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database']))

    def _on_select(self, title: str) -> None:
        """
        Respond to load the Work View Gtk.Notebook() widgets.

        This method handles the results of the an individual module's
        _on_select() method.  It sets the title of the RAMSTK Work Book and
        raises an error dialog if needed.

        :return: None
        :rtype: None
        """
        try:
            self.set_title(title)
        except AttributeError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)
            self.do_raise_dialog(severity='warning', user_msg=_error)

    @staticmethod
    def _on_window_state_event(window: Gtk.Window,
                               event: Gdk.EventWindowState) -> None:
        """
        Iconify or deiconify the desktop.

        :return: None
        :rtype: None
        """
        if event.new_window_state == Gdk.WindowState.ICONIFIED:
            window.iconify()
        elif event.new_window_state == 0:
            window.deiconify()
        elif event.new_window_state == Gdk.WindowState.MAXIMIZED:
            window.maximize()
