# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.desktop.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 basebook."""

# Standard Library Imports
import locale
from typing import List, TypeVar

# Third Party Imports
# noinspection PyPackageRequirements
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKSiteConfiguration, RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GdkPixbuf, GObject, Gtk, _
from ramstk.views.gtk3.assistants import (
    CreateProject, EditOptions, EditPreferences,
    ExportProject, ImportProject, OpenProject
)
from ramstk.views.gtk3.books import (
    RAMSTKListBook, RAMSTKModuleBook, RAMSTKWorkBook
)

Tconfiguration = TypeVar('Tconfiguration', RAMSTKUserConfiguration,
                         RAMSTKSiteConfiguration)


def destroy(__widget: Gtk.Widget, __event: Gdk.Event = None) -> None:
    """Quit the RAMSTK application.

    This function quits the RAMSTK application when the X in the upper right
    corner is pressed or if this function is called as a callback.

    :param __widget: the Gtk.Widget() that called this method.
    :keyword __event: the Gdk.Event() that called this method.
    :return: None
    :rtype: None
    """
    Gtk.main_quit()


class RAMSTKDesktop(Gtk.Window):
    """The base view for the RAMSTK Books.

    This is the container class for the List Book, Module Book, and Work Book.
    Attributes of the RAMSTKDesktop are:

    :cvar RAMSTK_USER_CONFIGURATION: the instance of the RAMSTK
        user configuration class.
    :type RAMSTK_USER_CONFIGURATION:
        :class:`ramstk.configuration.RAMSTKUserConfiguration`
    :cvar dict dic_books: dictionary holding a reference to each RAMSTK book.
    :cvar dict dic_tab_pos: dictionary holding the Gtk.PositionType()s for each
        of left, right, top, and bottom.
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

    RAMSTK_SITE_CONFIGURATION: RAMSTKSiteConfiguration = None  # type: ignore
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = None  # type: ignore

    def __init__(self, configuration: Tconfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize an instance of the RAMSTK Book.

        :param configuration: a list containing the RAMSTK user
            configuration and RAMSTK site configuration class instances.
        :param logger: the RAMSTKLogManager class instance.
        """
        # pylint: disable=non-parent-init-called
        GObject.GObject.__init__(self)
        self.RAMSTK_USER_CONFIGURATION = configuration[0]  # type: ignore
        self.RAMSTK_SITE_CONFIGURATION = configuration[1]  # type: ignore

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._logger = logger
        try:
            _screen = Gdk.Screen.get_default()
            _display = _screen.get_display()
            _monitor = _display.get_monitor(0)
            self._height = _monitor.get_geometry().height
            self._n_screens = _display.get_n_monitors()
            self._width = _monitor.get_geometry().width
        except AttributeError:
            # When running on CI servers, there will be no monitor.  We also
            # don't need one.
            self._height = -1
            self._n_screens = 0
            self._width = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.menubar = Gtk.MenuBar()
        self.progressbar = Gtk.ProgressBar()
        self.statusbar = Gtk.Statusbar()
        self.toolbar = Gtk.Toolbar()

        self.icoStatus = Gtk.StatusIcon()

        self.nbkListBook = RAMSTKListBook(self.RAMSTK_USER_CONFIGURATION,
                                          logger)
        self.nbkModuleBook = RAMSTKModuleBook(self.RAMSTK_USER_CONFIGURATION,
                                              logger)
        self.nbkWorkBook = RAMSTKWorkBook(self.RAMSTK_USER_CONFIGURATION,
                                          logger)
        self.nbkWorkBook.RAMSTK_SITE_CONFIGURATION = \
            self.RAMSTK_SITE_CONFIGURATION

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

    def _do_request_options_assistant(self,
                                      __widget: Gtk.ImageMenuItem) -> None:
        """Request the EditOptions assistant be launched.

        :param __widget: the Gtk.ImageMenuItem() that called this class.
        :return: None
        :rtype: None
        """
        _dialog = EditOptions(parent=self)

        # ISSUE: Make Site DB available without connecting to program DB.
        #
        # The site DB should be available without having to connect to a
        # program DB.  Currently the site DAO is a member of the
        # ProgramManager's dict of data managers.  The site DAO needs to be
        # made available out of __main__.py or the ProgramManager needs to
        # be made accessible to the RAMSTKDesktop so site options can be
        # accessed.
        # assignees: weibullguy
        # label: globalbacklog, normal
        if _dialog.do_run() == Gtk.ResponseType.OK:
            print("Need site admin or higher privileges.")

        _dialog.do_destroy()

    def _do_request_preferences_assistant(self,
                                          __widget: Gtk.ImageMenuItem) -> None:
        """Request the EditPreferences assistant be launched.

        :param __widget: the Gtk.ImageMenuItem() that called this class.
        :return: None
        :rtype: None
        """
        _assistant = Gtk.Window()
        _preferences = EditPreferences(self.RAMSTK_USER_CONFIGURATION,
                                       self._logger)

        _n_screens = Gdk.Screen.get_default().get_n_monitors()
        _width = Gdk.Screen.width() / _n_screens
        _height = Gdk.Screen.height()

        _assistant.set_border_width(5)
        _assistant.set_default_size(_width - 450, (4 * _height / 7))
        _assistant.set_modal(True)
        _assistant.set_position(Gtk.WindowPosition.CENTER)
        _assistant.set_resizable(True)
        _assistant.set_transient_for(self)

        _assistant.add(_preferences)

        _assistant.show_all()

    def __make_menu(self) -> None:
        """Make the menu for the Module Book.

        :return: None
        :rtype: None
        """
        self.menubar.append(self.__make_menu_file())
        self.menubar.append(self.__make_menu_edit())
        self.menubar.append(self.__make_menu_tools())

        self.menubar.show_all()

    def __make_menu_edit(self) -> Gtk.MenuItem:
        """Make the Edit menu.

        :return: the Edit menu.
        :rtype: :class:`Gtk.MenuItem`
        """
        _menu = Gtk.Menu()

        _menu_items = self.__make_menu_items(['preferences'], ['_Preferences'])

        for _menu_item in _menu_items:
            _menu.append(_menu_item)

        _menu_items[0].connect('activate',
                               self._do_request_preferences_assistant)

        _menu_item = Gtk.MenuItem(label=_("_Edit"), use_underline=True)
        _menu_item.set_submenu(_menu)

        return _menu_item

    def __make_menu_file(self) -> Gtk.MenuItem:
        """Make the File menu.

        :return: the File menu.
        :rtype: :class:`Gtk.MenuItem`
        """
        _menu = Gtk.Menu()

        _menu_items = self.__make_menu_items(
            ['new', 'open', 'import', 'export', 'save', '', 'exit'], [
                'New _Program', '_Open', '_Import Project', '_Export Project',
                '_Save', '_Close', 'E_xit'
            ])

        for _menu_item in _menu_items:
            _menu.append(_menu_item)

        _menu_items[0].connect('activate', CreateProject,
                               self.RAMSTK_USER_CONFIGURATION, self)
        _menu_items[1].connect('activate', OpenProject,
                               self.RAMSTK_USER_CONFIGURATION, self)
        _menu_items[2].connect('activate', ImportProject,
                               self.RAMSTK_USER_CONFIGURATION, self)
        _menu_items[3].connect('activate', ExportProject,
                               self.RAMSTK_USER_CONFIGURATION, self)
        _menu_items[4].connect('activate', self._do_request_save_project)
        _menu_items[5].connect('activate', self._do_request_close_project)
        _menu_items[6].connect('activate', destroy)

        _menu_item = Gtk.MenuItem()
        _menu_item.set_label(_("_File"))
        _menu_item.set_property('use_underline', True)
        _menu_item.set_submenu(_menu)

        return _menu_item

    def __make_menu_items(self, icons: List[str],
                          labels: List[str]) -> List[Gtk.ImageMenuItem]:
        """Make a list of the menu items for a menu.

        :param icons: the list of icons to display on each menu item.
        :param labels: the list of label text for each menu item.
        :return: _menu_items; the list of menu items to include in the menu.
        """
        _menu_items: List[Gtk.ImageMenuItem] = []

        for _idx, _ico in enumerate(icons):
            if _ico != '':
                _icon = self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + \
                    '/16x16/' + _ico + '.png'
            else:
                _icon = self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + \
                    '/16x16/default.png'

            _menu_item = Gtk.ImageMenuItem()
            _image = Gtk.Image()
            _image.set_from_file(_icon)
            _menu_item.set_label(_(labels[_idx]))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)

            _menu_items.append(_menu_item)

        return _menu_items

    def __make_menu_tools(self) -> Gtk.MenuItem:
        """Make the Tools menu.

        :return: the Tools menu.
        :rtype: :class:`Gtk.MenuItem`
        """
        _menu = Gtk.Menu()

        _menu_items = self.__make_menu_items(['options'], ['_Options'])

        for _menu_item in _menu_items:
            _menu.append(_menu_item)

        _menu_items[0].connect('activate', self._do_request_options_assistant)

        _menu_item = Gtk.MenuItem(label=_("_Tools"), use_underline=True)
        _menu_item.set_submenu(_menu)

        return _menu_item

    def __make_toolbuttons(self, icons: List[str],
                           tooltips: List[str]) -> List[Gtk.ToolButton]:
        """Make the toolbuttons for a toolbar.

        :param icons: the list of icons to display on the toolbutton.
        :param tooltips: the list of tooltips to associate with each
            toolbutton.
        :return: _buttons; the list of toolbuttons to display in the toolbar.
        """
        _buttons: List[Gtk.ToolButton] = []

        for _idx, _ico in enumerate(icons):
            if _ico != '':
                _icon = self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + \
                    '/32x32/' + _ico + '.png'
            else:
                _icon = self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + \
                    '/32x32/default.png'

            _button = Gtk.ToolButton()
            _button.set_tooltip_text(tooltips[_idx])
            _image = Gtk.Image()
            _image.set_from_file(_icon)
            _button.set_icon_widget(_image)

            _buttons.append(_button)

        return _buttons

    def __make_toolbar(self) -> None:
        """Make the toolbar for the Module Book.

        :return: None
        :rtype: None
        """
        _toolbuttons = self.__make_toolbuttons(
            ['new', 'open', 'close', 'save', 'save-exit', 'exit'], [
                _("Create a new RAMSTK Program Database."),
                _("Connect to an existing RAMSTK Program Database."),
                _("Closes the open RAMSTK Program Database."),
                _("Save the currently open RAMSTK Project "
                  "Database."),
                _("Save the currently open RAMSTK Program Database "
                  "then quits."),
                _("Quits without saving the currently open RAMSTK "
                  "Program Database.")
            ])

        for _position, _toolbutton in enumerate(_toolbuttons):
            self.toolbar.insert(_toolbutton, _position)

        self.toolbar.insert(Gtk.SeparatorToolItem(), 3)
        self.toolbar.insert(Gtk.SeparatorToolItem(), 5)

        _toolbuttons[0].connect('clicked', CreateProject,
                                self.RAMSTK_USER_CONFIGURATION, self)
        _toolbuttons[1].connect('clicked', OpenProject,
                                self.RAMSTK_USER_CONFIGURATION, self)
        _toolbuttons[2].connect('clicked', self._do_request_close_project)
        _toolbuttons[3].connect('clicked', self._do_request_save_project)
        _toolbuttons[4].connect('clicked', self._do_request_save_project, True)
        _toolbuttons[5].connect('clicked', destroy)

        self.toolbar.show_all()

    def __make_ui(self) -> None:
        """Build the user interface.

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
        """Set the callbacks for the RAMSTKListBook() and widgets.

        :return: None
        :rtype: None
        """
        self.connect('delete_event', destroy)
        self.connect('window_state_event', self._on_window_state_event)
        self.connect('button_press_event', self._on_button_press)

    def __set_properties(self) -> None:
        """Set properties of the RAMSTKBook and widgets.

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
        """Request to close the open RAMSTK Program.

        :param Gtk.Widget __widget: the Gtk.Widget() that called this method.
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_close_project')

    # noinspection PyDeepBugsSwappedArgs
    def _do_request_save_project(self,
                                 widget: Gtk.Widget,
                                 end: bool = False) -> None:
        """Request to save the open RAMSTK Program.

        :param Gtk.Widget widget: the Gtk.Widget() that called this method.
        :keyword bool end: indicates whether or not to quit RAMSTK after saving
            the project.
        :return: None
        :rtype: None
        """
        _message = _("Saving Program Database {0:s}").format(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        self.statusbar.push(2, _message)

        pub.sendMessage('request_save_project')

        if end:
            destroy(widget)

    def _do_set_status(self, status: str) -> None:
        """Set the status message.

        :param status: the status message to display.
        :return: None
        :rtype: None
        """
        self.statusbar.push(1, status)

    def _do_set_status_icon(self, connected: bool = False) -> None:
        """Set the status icon in the system tay to indicate connection status.

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
        """Handle mouse clicks on the RAMSTKBook.

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
        """Set the status bar and update the progress bar.

        :return: None
        :rtype: None
        """
        _message = _("Opening Program Database {0:s}"). \
            format(self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        # noinspection PyDeepBugsSwappedArgs
        self.statusbar.push(1, _message)
        self.set_title(
            _("RAMSTK - Analyzing {0:s}").format(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database']))

    def _on_select(self, title: str) -> None:
        """Respond to load the Work View Gtk.Notebook() widgets.

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
        """Iconify or deiconify the desktop.

        :return: None
        :rtype: None
        """
        if event.new_window_state == Gdk.WindowState.ICONIFIED:
            window.iconify()
        elif event.new_window_state == 0:
            window.deiconify()
        elif event.new_window_state == Gdk.WindowState.MAXIMIZED:
            window.maximize()
