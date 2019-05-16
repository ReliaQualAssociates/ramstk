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
from ramstk.gui.gtk.moduleviews import (
    mvwRevision, mvwFunction, mvwRequirement, mvwHardware, mvwValidation)
from ramstk.gui.gtk.assistants import (CreateProject, OpenProject, Options,
                                       Preferences, ImportProject)
from ramstk.gui.gtk.ramstk.Widget import _, Gtk


class ModuleBook(RAMSTKBook):  # pylint: disable=R0904
    """
    Display Module Views for the RAMSTK modules.

    Attributes of the Module Book are:

    :ivar dict _dic_module_views: dictionary containing the Module View to
                                  load into the RAMSTK Module Book for each
                                  RAMSTK module.  Key is the RAMSTK module
                                  name; value is the View associated with
                                  that RAMSTK module.
    """

    def __init__(self, controller, configuration):
        """
        Initialize an instance of the Module Book class.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKBook.__init__(self, configuration)
        self.dic_books['modulebook'] = self

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

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_open, 'retrieved_revisions')
        pub.subscribe(self._on_close, 'closed_program')

    def __make_menu(self):
        """
        Make the menu for the Module Book.

        :return None
        :type None
        """
        _icon_dir = self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR

        _menu = Gtk.Menu()

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/new.png')
        _menu_item.set_label(_("New _Program"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        #_menu_item.connect('activate', CreateProject, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/open.png')
        _menu_item.set_label(_("_Open"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        #_menu_item.connect('activate', OpenProject, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/import.png')
        _menu_item.set_label(_("_Import Project"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        #_menu_item.connect('activate', ImportProject, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/save.png')
        _menu_item.set_label(_("_Save"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', self._do_request_save_project)
        _menu.append(_menu_item)

        _menu_item = Gtk.MenuItem(label=_("_Close"), use_underline=True)
        _menu_item.connect('activate', self._do_request_close_project)
        _menu.append(_menu_item)

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/exit.png')
        _menu_item.set_label(_("E_xit"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        _menu_item.connect('activate', destroy)
        _menu.append(_menu_item)

        _mnuFile = Gtk.MenuItem(label=_("_File"), use_underline=True)
        _mnuFile.set_submenu(_menu)

        # Create the Edit menu.
        _menu = Gtk.Menu()

        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/preferences.png')
        _menu_item.set_label(_("_Preferences"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        #_menu_item.connect('activate', Preferences, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _mnuEdit = Gtk.MenuItem(label=_("_Edit"), use_underline=True)
        _mnuEdit.set_submenu(_menu)

        # Create the Tools menu.
        _menu = Gtk.Menu()
        _menu_item = Gtk.ImageMenuItem()
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/16x16/options.png')
        _menu_item.set_label(_("_Options"))
        _menu_item.set_image(_image)
        _menu_item.set_property('use_underline', True)
        #_menu_item.connect('activate', Options, self._mdcRAMSTK)
        _menu.append(_menu_item)

        _mnuTools = Gtk.MenuItem(label=_("_Tools"), use_underline=True)
        _mnuTools.set_submenu(_menu)

        self.menubar.append(_mnuFile)
        self.menubar.append(_mnuEdit)
        self.menubar.append(_mnuTools)

        self.menubar.show_all()

    def __make_toolbar(self):
        """
        Make the toolbar for the Module Book.

        :return _toolbar: the Gtk.Toolbar() for the RAMSTK ModuleBook.
        :type _toolbar: :class:`Gtk.Toolbar`
        """
        _icon_dir = self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR

        _position = 0

        # New file button.
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(_("Create a new RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/new.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', CreateProject, self._mdcRAMSTK)
        self.toolbar.insert(_button, _position)
        _position += 1

        # Connect button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _("Connect to an existing RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/open.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', OpenProject, self._mdcRAMSTK)
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
            _("Save the currently open RAMSTK Project "
              "Database."))
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
            _("Save the currently open RAMSTK Program "
              "Database then quits."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/save-exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._do_request_save_project, True)
        self.toolbar.insert(_button, _position)
        _position += 1

        # Quit without saving button
        _button = Gtk.ToolButton()
        _button.set_tooltip_text(
            _("Quits without saving the currently open "
              "RAMSTK Program Database."))
        _image = Gtk.Image()
        _image.set_from_file(_icon_dir + '/32x32/exit.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', destroy)
        self.toolbar.insert(_button, _position)

        self.toolbar.show_all()

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.__make_menu()
        self.__make_toolbar()

        self.notebook.insert_page(
            self._dic_module_views['revision'],
            tab_label=self._dic_module_views['revision'].hbx_tab_label,
            position=0)

        self.statusbar.add(self.progressbar)
        _vbox = Gtk.VBox()
        _vbox.pack_start(self.menubar, False, False, 0)
        _vbox.pack_start(self.toolbar, False, False, 0)
        _vbox.pack_start(self.notebook, True, True, 0)
        _vbox.pack_start(self.statusbar, False, False, 0)

        self.add(_vbox)

        self.show_all()
        self.notebook.set_current_page(0)

        self.statusbar.push(1, _("Ready"))

    def __set_properties(self):
        """
        Set properties of the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        try:
            _tab_position = self.dic_tab_position[
                self.RAMSTK_CONFIGURATION.RAMSTK_TABPOS['modulebook'].lower()]
        except KeyError:
            _tab_position = self._bottom_tab
        self.notebook.set_tab_pos(_tab_position)

        self.set_title(_("RAMSTK Module Book"))

        self.progressbar.set_pulse_step(0.25)

        if self.RAMSTK_CONFIGURATION.RAMSTK_OS == 'Linux':
            _width = (2 * self._width / 3) - 10
            _height = 2 * self._height / 7
        elif self.RAMSTK_CONFIGURATION.RAMSTK_OS == 'Windows':
            _width = (2 * self._width / 3) - 30
            _height = 2 * self._height / 7

        self.resize(_width, _height)
        self.move(0, 0)

    def __set_callbacks(self):
        """
        Set the callback functions/methods for the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.notebook.connect('select-page', self._on_switch_page))
        self._lst_handler_id.append(
            self.notebook.connect('switch-page', self._on_switch_page))

    def _on_close(self):
        """
        Update the Module View when a RAMSTK Program database is closed.

        :return: None
        :rtype: None
        """
        # Remove all the non-Revision pages.
        _n_pages = self.notebook.get_n_pages()
        for _page in range(_n_pages - 1):
            self.notebook.remove_page(-1)

        # Clear the Revision page treeview.
        _model = self._dic_module_views['revision'].treeview.get_model()
        _model.clear()

    def _on_open(self, tree):  # pylint: disable=unused-argument
        """
        Update the status bar and clear the progress bar.

        :return: None
        :rtype: None
        """
        # Insert a page for each of the active RAMSTK Modules.
        for _key in self.RAMSTK_CONFIGURATION.RAMSTK_PAGE_NUMBER:
            _mkey = self.RAMSTK_CONFIGURATION.RAMSTK_PAGE_NUMBER[_key]
            _module = self._dic_module_views[_mkey]
            self.notebook.insert_page(
                _module, tab_label=_module.hbx_tab_label, position=_key)

        self.statusbar.pop(1)

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

        :return: None
        :rtype: None
        """
        # Key errors occur when no RAMSTK Program database has been loaded.  In
        # that case, select the Revision page to load.
        try:
            _module = self.RAMSTK_CONFIGURATION.RAMSTK_PAGE_NUMBER[
                page_num]
        except KeyError:
            _module = 'revision'

        pub.sendMessage('mvwSwitchedPage', module=_module)

    @staticmethod
    def _do_request_save_project(widget, end=False):
        """
        Request to save the open RAMSTK Program.

        :param Gtk.Widget widget: the Gtk.Widget() that called this method.
        :keyword bool end: indicates whether or not to quit RAMSTK after saving
                           the project.
        :return: None
        :rtype: None
        """
        _message = _("Saving Program Database {0:s}"). \
            format(self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        self.statusbar.push(2, _message)

        pub.sendMessage('request_save_project')

        self.dic_books['modulebook'].statusbar.pop(2)

        if end:
            destroy(widget)

    @staticmethod
    def _do_request_close_project(__widget):
        """
        Request to close the open RAMSTK Program.

        :param Gtk.Widget __widget: the Gtk.Widget() that called this method.
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_close_project')
