# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.options.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Configuration Options Module."""

# Standard Library Imports
from typing import Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import integer_to_boolean
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.views.gtk3 import Gdk, GObject, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKButton, RAMSTKCheckButton


class EditOptions(Gtk.Window):
    """
    An assistant to provide a GUI to set various RAMSTK configuration options.

    RAMSTK options are stored in the RAMSTK Common database and the RAMSTK
    Program database.  RAMSTK options are site-specific or program-specific and
    apply to all users.  Options should not be confused with user-specific
    configurations preferences which are stored in RAMSTK.conf in each user's
    $HOME/.config/RAMSTK directory and are applicable only to that specific
    user.  Configuration preferences are edited with the Preferences assistant.

    Attributes of the EditOptions are:

    :cvar RAMSTK_USER_CONFIGURATION: the instance of the RAMSTK Configuration
        class.
    :type RAMSTK_USER_CONFIGURATION: :class:`ramstk.Configuration.Configuration`

    :ivar dict _dic_icons: dictionary containing icon name and absolute path
        key:value pairs.
    """
    # Define private dictionary class attributes.
    _dic_keys = {0: 'function_active', 1: 'requirement_active',
                 2: 'hardware_active', 3: 'vandv_active', 4: 'fmea_active',
                 5: 'pof_active'}

    # Define public class scalar attributes.
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = None

    def __init__(self, configuration: RAMSTKUserConfiguration) -> None:
        """
        Initialize an instance of the Options assistant.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        """
        GObject.GObject.__init__(self)

        self.RAMSTK_USER_CONFIGURATION = configuration

        # Initialize private dictionary attributes.
        self._dic_icons: Dict[str, str] = dict(
            save=self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/save.png',
            cancel=self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/cancel.png')

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.notebook: Gtk.Notebook = Gtk.Notebook()
        self.btnQuit: RAMSTKButton = RAMSTKButton()
        self.btnSave: RAMSTKButton = RAMSTKButton()
        self.chkFunctions: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function Module Active"))
        self.chkRequirements: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirements Module Active"))
        self.chkHardware: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Hardware Module Active"))
        self.chkValidation: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Validation Module Active"))
        self.chkFMEA: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("(D)FME(C)A Module Active"))
        self.chkPoF: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Physics of Failure (PoF) Module Active"))

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'succeed_get_options_tree')

    def __make_modules_page(self) -> None:
        """
        Make the Option class Gtk.Notebook() active modules page.

        :return: None
        :rtype: None
        """
        _fixed = Gtk.Fixed()

        _fixed.put(self.chkFunctions, 5, 5)
        _fixed.put(self.chkRequirements, 5, 35)
        _fixed.put(self.chkHardware, 5, 65)
        _fixed.put(self.chkValidation, 5, 95)
        _fixed.put(self.chkFMEA, 5, 125)

        _label = Gtk.Label(label=_("Active RAMSTK Modules"))
        _label.set_tooltip_text(_("Select active RAMSTK modules."))
        self.notebook.insert_page(_fixed, tab_label=_label, position=-1)

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _n_screens = Gdk.Screen.get_default().get_n_monitors()
        _width = Gdk.Screen.width() / _n_screens
        _height = Gdk.Screen.height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))

        self.__make_modules_page()

        _vbox = Gtk.HBox()

        _buttonbox = Gtk.VButtonBox()
        _buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        _buttonbox.pack_start(self.btnSave, True, True, 0)
        _buttonbox.pack_start(self.btnQuit, True, True, 0)
        _vbox.pack_start(_buttonbox, False, True, 0)

        _vbox.pack_end(self.notebook, True, True, 0)

        self.add(_vbox)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set EditOption widgets callback methods.

        :return: None
        :rtype: None
        """
        self.btnSave.connect('clicked', self._do_request_update)
        self.btnQuit.connect('clicked', self._do_quit)

        self.chkFunctions.dic_handler_id[
            'toggled'] = self.chkFunctions.connect('toggled',
                                                   self._on_toggled, 0)
        self.chkRequirements.dic_handler_id[
            'toggled'] = self.chkRequirements.connect('toggled',
                                                      self._on_toggled, 1)
        self.chkHardware.dic_handler_id['toggled'] = self.chkHardware.connect(
            'toggled', self._on_toggled, 2)
        self.chkValidation.dic_handler_id[
            'toggled'] = self.chkValidation.connect('toggled',
                                                    self._on_toggled, 3)
        self.chkFMEA.dic_handler_id['toggled'] = self.chkFMEA.connect(
            'toggled', self._on_toggled, 4)

    def __set_properties(self) -> None:
        """
        Set the properties of the Options assistance widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnQuit.do_set_properties(icon=self._dic_icons['cancel'],
                                       tooltip=_(""),
                                       width=-1)
        self.btnSave.do_set_properties(icon=self._dic_icons['save'],
                                       tooltip=_(""),
                                       width=-1)

        # ----- CHECKBUTTONS
        self.chkFunctions.do_set_properties(tooltip=_(
            "Activates/deactivates the Function module for this program."),
                                            width=500)
        self.chkRequirements.do_set_properties(tooltip=_(
            "Activates/deactivates the Requirements module for "
            "this program."),
                                               width=500)
        self.chkHardware.do_set_properties(tooltip=_(
            "Activates/deactivates the Hardware module for this program."),
                                           width=500)
        self.chkValidation.do_set_properties(tooltip=_(
            "Activates/deactivates the Validation module for this program."),
                                             width=500)
        self.chkFMEA.do_set_properties(tooltip=_(
            "Activates/deactivates the (D)FME(C)A module for this program."),
                                       width=500)

    def _do_load_page(self, tree: Tree) -> None:
        """
        Load the current options.

        :return: None
        :rtype: None
        """
        _program_options = tree.get_node(
            'programinfo').data['programinfo'].get_attributes()

        self.chkFunctions.set_active(
            integer_to_boolean(_program_options['function_active']))
        self.chkRequirements.set_active(
            integer_to_boolean(_program_options['requirement_active']))
        self.chkHardware.set_active(
            integer_to_boolean(_program_options['hardware_active']))
        self.chkValidation.set_active(
            integer_to_boolean(_program_options['vandv_active']))
        self.chkFMEA.set_active(
            integer_to_boolean(_program_options['fmea_active']))

    def _do_quit(self, __button: Gtk.Button) -> None:
        """
        Quit the options Gtk.Assistant().

        :param Gtk.Button __button: the Gtk.Button() that called this method.
        :return: None
        :rtype: None
        """
        self.destroy()

    @staticmethod
    def _do_request_update(__button: Gtk.Button) -> None:
        """
        Save the configuration changes made by the user.

        :param __button: the Gtk.Button() that called this method.
        :param __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_update_option', node_id='programinfo')
        pub.sendMessage('request_update_option', node_id='siteinfo')

    def _on_toggled(self, checkbutton: RAMSTKCheckButton, index: int) -> None:
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param togglebutton: the RAMSTKCheckButton() that called this method.
        :type: :class:`gui.gtk.ramstk.Button.RAMSTKToggleButton`
        :param int index: the index of the Gtk.CheckButton() in the list
            handler list.
        :return: None
        :rtype: None
        """
        #// TODO: Add code to record user creating program database.
        #//
        #// There should be code to record in the RAMSTKProgramInfo table
        #// the logged in user who creates the database.  This will require
        #// a function/method to identify the logged in user as well as a
        #// function/method to write this to the new database.

        #// TODO: Add code to record user updating program database.
        #//
        #// There should be code to record in the RAMSTKProgramInfo table
        #// the logged in user who is updating the database.  This will
        #// require a function/method to identify the logged in user as well
        #// as a function/method to write this to the database everytime a
        #// datamanager successfully updates a database table.
        try:
            _key = self._dic_keys[index]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        _new_text = int(checkbutton.get_active())

        checkbutton.do_update(_new_text, signal='toggled')

        pub.sendMessage('request_set_option_attributes',
                        node_id=['programinfo', -1],
                        package={_key: _new_text})
