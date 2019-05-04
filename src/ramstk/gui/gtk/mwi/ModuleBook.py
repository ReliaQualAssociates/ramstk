# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.mwi.ModuleBook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Module Book Module."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk import RAMSTKBook, destroy
from ramstk.gui.gtk.moduleviews import mvwRevision
from ramstk.gui.gtk.moduleviews import mvwFunction
from ramstk.gui.gtk.moduleviews import mvwRequirement
from ramstk.gui.gtk.moduleviews import mvwHardware
from ramstk.gui.gtk.moduleviews import mvwValidation
from ramstk.gui.gtk.assistants import (CreateProject, OpenProject, Options,
                                       Preferences, ImportProject)
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, Gtk


class ModuleBook(RAMSTKBook):  # pylint: disable=R0904
    """
    Display Module Views for the RAMSTK modules.

    Attributes of the Module Book are:

    :ivar list _lst_handler_id:
    :ivar _mdcRAMSTK: the RAMSTK master data controller.
    :type _mdcRAMSTK: :class:`ramstk.RAMSTK.RAMSTK`
    :ivar notebook: the Gtk.Notebook() widget used to hold each of the RAMSTK
                    module WorkViews.
    :type notebook: :class:`Gtk.Notebook`
    :ivar menubar: the Gtk.MenuBar() for the RAMSTK ModuleBook menu.
    :type menubar: :class:`Gtk.MenuBar`
    :ivar toolbar: the Gtk.Toolbar() for the RAMSTK ModuleBook tools.
    :type toolbar: :class:`Gtk.Toolbar`
    :ivar statusbar: the Gtk.Statusbar() for displaying messages.
    :type statusbar: :class:`Gtk.Statusbar`
    :ivar progressbar: the Gtk.Progressbar() for displaying progress counters.
    :type progressbar: :class:`Gtk.Progressbar`
    """

    def __init__(self, controller):
        """
        Initialize an instance of the Module Book class.

        :param controller: the RAMSTK master data controller.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKBook.__init__(self, controller)

        # Initialize private dictionary attributes.
        self._dic_module_views = {
            'revision': mvwRevision(controller),
            'requirement': mvwRequirement(controller),
            'function': mvwFunction(controller),
            'hardware': mvwHardware(controller),
            'validation': mvwValidation(controller)
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.progressbar = Gtk.ProgressBar(adjustment=None)
        self.statusbar = Gtk.Statusbar()

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_request_open, 'requestOpen')
        pub.subscribe(self._on_open, 'retrieved_revisions')
        pub.subscribe(self._on_close, 'closedProgram')

    def __make_menu(self):
        """
        Make the menu for the Module Book.

        :return _menubar: the Gtk.MenuBar() for the RAMSTK ModuleBook.
        :type _menubar: :class:`Gtk.MenuBar`
        """
        _icon_dir = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR

        _menu = Gtk.Menu()

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/new.png')
        _menu_item.set_label(_(u"New _Program"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', CreateProject, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/open.png')
        _menu_item.set_label(_(u"_Open"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', OpenProject, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/import.png')
        _menu_item.set_label(_(u"_Import Project"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', ImportProject, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/save.png')
        _menu_item.set_label(_(u"_Save"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', self._request_save_project)
        _menu.append(_menu_item)

        _menu_item = Gtk.MenuItem(label=_(u"_Close"), use_underline=True)
        _menu_item.connect('activate', self._do_request_close_project)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/exit.png')
        _menu_item.set_label(_(u"E_xit"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', destroy)
        _menu.append(_menu_item)

        _mnuFile = Gtk.MenuItem(label=_(u"_File"), use_underline=True)
        _mnuFile.set_submenu(_menu)

        # Create the Edit menu.
        _menu = Gtk.Menu()

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/preferences.png')
        _menu_item.set_label(_(u"_Preferences"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', Preferences, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _mnuEdit = Gtk.MenuItem(label=_(u"_Edit"), use_underline=True)
        _mnuEdit.set_submenu(_menu)

        # Create the Tools menu.
        _menu = Gtk.Menu()
        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/options.png')
        _menu_item.set_label(_(u"_Options"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', Options, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _mnuTools = Gtk.MenuItem(label=_(u"_Tools"), use_underline=True)
        _mnuTools.set_submenu(_menu)

        _menubar = Gtk.MenuBar()
        _menubar.append(_mnuFile)
        _menubar.append(_mnuEdit)
        _menubar.append(_mnuTools)

        _menubar.show_all()

        return _menubar

    def __make_toolbar(self):
        """
        Make the toolbar for the Module Book.

        :return _toolbar: the Gtk.Toolbar() for the RAMSTK ModuleBook.
        :type _toolbar: :class:`Gtk.Toolbar`
        """
        _icon_dir = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR

        _toolbar = Gtk.Toolbar()

        _position = 0

        # New file button.
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(_(u"Create a new RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/new.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', CreateProject, self._mdcRAMSTK)
        _toolbar.insert(_button, _position)
        _position += 1

        # Connect button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Connect to an existing RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/open.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', OpenProject, self._mdcRAMSTK)
        _toolbar.insert(_button, _position)
        _position += 1

        # Close button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Closes the open RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/close.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_close_project)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(Gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Save the currently open RAMSTK Project "
              u"Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_project)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(Gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save and quit button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Save the currently open RAMSTK Program "
              u"Database then quits."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/save-exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_project, True)
        _toolbar.insert(_button, _position)
        _position += 1

        # Quit without saving button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Quits without saving the currently open "
              u"RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', destroy)
        _toolbar.insert(_button, _position)

        _toolbar.show_all()

        return _toolbar

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.set_title(_(u"RAMSTK Module Book"))

        if self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_OS == 'Linux':
            _width = (2 * self._width / 3) - 10
            _height = 2 * self._height / 7
        elif self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_OS == 'Windows':
            _width = (2 * self._width / 3) - 30
            _height = 2 * self._height / 7

        self.set_default_size(_width, _height)
        self.move(0, 0)

        if self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'modulebook'].lower() == 'left':
            self.notebook.set_tab_pos(self._left_tab)
        elif self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'modulebook'].lower() == 'right':
            self.notebook.set_tab_pos(self._right_tab)
        elif self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'modulebook'].lower() == 'top':
            self.notebook.set_tab_pos(self._top_tab)
        else:
            self.notebook.set_tab_pos(self._bottom_tab)

        self.progressbar.set_pulse_step(0.25)
        self.statusbar.add(self.progressbar)

        self._lst_handler_id.append(
            self.notebook.connect('select-page', self._on_switch_page))
        self._lst_handler_id.append(
            self.notebook.connect('switch-page', self._on_switch_page))

        # Insert a page for the Revision Module.
        _page = mvwRevision(self._mdcRAMSTK)
        self.notebook.insert_page(
            _page, tab_label=_page.hbx_tab_label, position=0)

        _vbox = Gtk.VBox()
        _vbox.pack_start(self.__make_menu(), expand=False, fill=False)
        _vbox.pack_start(self.__make_toolbar(), expand=False, fill=False)
        _vbox.pack_start(self.notebook, expand=True, fill=True)
        _vbox.pack_start(self.statusbar, expand=False, fill=False)

        self.connect('window_state_event', self._on_window_state_event)

        self.add(_vbox)

        self.show_all()
        self.notebook.set_current_page(0)

        self.statusbar.push(1, _(u"Ready"))

        return None

    def _on_request_open(self):
        """
        Set the status bar and update the progress bar.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _message = _(u"Opening Program Database {0:s}"). \
            format(self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        self.statusbar.push(1, _message)
        self.set_title(
            _(u"RAMSTK - Analyzing {0:s}").format(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                RAMSTK_PROG_INFO['database']))

        return _return

    def _on_close(self):
        """
        Update the Module View when a RAMSTK Program database is closed.

        :return: None
        :rtype: None
        """
        # Remove all the non-Revision pages.
        _n_pages = self.notebook.get_n_pages()
        for _page in xrange(_n_pages - 1):
            self.notebook.remove_page(-1)

        # Clear the Revision page treeview.
        _model = self._dic_module_views['revision'].treeview.get_model()
        _model.clear()

        return None

    def _on_open(self, tree):   # pylint: disable=unused-argument
        """
        Update the status bar and clear the progress bar.

        :return: None
        :rtype: None
        """
        # Insert a page for each of the active RAMSTK Modules.
        for _key in self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PAGE_NUMBER:
            _mkey = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PAGE_NUMBER[
                _key]
            _module = self._dic_module_views[_mkey]
            self.notebook.insert_page(
                _module, tab_label=_module.hbx_tab_label, position=_key)

        self.statusbar.pop(1)

        return None

    def _on_switch_page(self, __notebook, __page, page_num):
        """
        Handle page changes in the Module Book Gtk.Notebook().

        :param __notebook: the Tree Book notebook widget.
        :type __notebook: :class:`Gtk.Notebook`
        :param __page: the newly selected page's child widget.
        :type __page: :class:`Gtk.Widget`
        :param int page_num: the newly selected page number.

                             0 = Revision Tree
                             1 = Requirements Tree
                             2 = Function Tree
                             3 = Hardware Tree
                             4 = Software Tree
                             5 = Testing Tree
                             6 = Validation Tree
                             7 = Incident Tree
                             8 = Survival Analyses Tree

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Key errors occur when no RAMSTK Program database has been loaded.  In
        # that case, select the Revision page to load.
        try:
            _module = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PAGE_NUMBER[
                page_num]
        except KeyError:
            _module = 'revision'

        pub.sendMessage('mvwSwitchedPage', module=_module)

        return False

    def _on_window_state_event(self, window, event):
        """
        Iconify or deiconify all three books together.

        :return: None
        :rtype: None
        """
        if event.new_window_state == Gdk.WindowState.ICONIFIED:
            for _window in ['listbook', 'modulebook', 'workbook']:
                self._mdcRAMSTK.dic_books[_window].iconify()
        elif event.new_window_state == 0:
            for _window in ['listbook', 'modulebook', 'workbook']:
                self._mdcRAMSTK.dic_books[_window].deiconify()
        elif event.new_window_state == Gdk.WindowState.MAXIMIZED:
            window.maximize()

        return None

    def _request_save_project(self, __widget, end=False):
        """
        Request to save the open RAMSTK Program.

        :param Gtk.Widget __widget: the Gtk.Widget() that called this method.
        :keyword bool end: indicates whether or not to quit RAMSTK after saving
                           the project.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._mdcRAMSTK.save_project()

        if end:
            destroy(__widget)

        return False

    def _do_request_close_project(self, __widget):
        """
        Request to close the open RAMSTK Program.

        :param Gtk.Widget __widget: the Gtk.Widget() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._mdcRAMSTK.request_do_close_program()

        return False
