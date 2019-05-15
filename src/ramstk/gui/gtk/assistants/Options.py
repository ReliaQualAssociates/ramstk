# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.assistants.Options.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Configuration Options Module."""

# Import other RAMSTK modules.
from ramstk.Utilities import boolean_to_integer, integer_to_boolean
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, GObject, Gtk
from ramstk.gui.gtk import ramstk

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 Doyle "weibullguy" Rowland'


class Options(Gtk.Window):
    """
    An assistant to provide a GUI to set various RAMSTK configuration options.

    RAMSTK options are stored in the RAMSTK Common database and the RAMSTK
    Program database.  RAMSTK options are site-specific or program-specific and
    apply to all users.  Options should not be confused with user-specific
    configurations preferences which are stored in RAMSTK.conf in each user's
    $HOME/.config/RAMSTK directory and are applicable only to that specific
    user.  Configuration preferences are edited with the Preferences assistant.
    """

    def __init__(self, __widget, controller):
        """
        Initialize an instance of the Options assistant.

        :param Gtk.Widget __widget: the Gtk.Widget() that called this class.
        :param controller: the RAMSTK master data controller.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        GObject.GObject.__init__(self)

        # Initialize private dictionary attributes.
        self._dic_icons = {
            'save':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/save.png',
            'cancel':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/cancel.png'
        }

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRAMSTK = controller
        self._dtc_data_controller = controller.dic_controllers['options']
        self._last_id = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.notebook = Gtk.Notebook()
        self.btnSave = ramstk.RAMSTKButton(
            icon=self._dic_icons['save'], height=-1, width=-1)
        self.btnQuit = ramstk.RAMSTKButton(
            icon=self._dic_icons['cancel'], height=-1, width=-1)
        self.chkFunctions = ramstk.RAMSTKCheckButton(
            label=_("Function Module Active"),
            tooltip=_(
                "Activates/deactivates the Function module for this program.")
        )
        self.chkRequirements = ramstk.RAMSTKCheckButton(
            label=_("Requirements Module Active"),
            tooltip=_("Activates/deactivates the Requirements module for "
                      "this program."))
        self.chkHardware = ramstk.RAMSTKCheckButton(
            label=_("Hardware Module Active"),
            tooltip=_(
                "Activates/deactivates the Hardware module for this program.")
        )
        self.chkValidation = ramstk.RAMSTKCheckButton(
            label=_("Validation Module Active"),
            tooltip=_(
                "Activates/deactivates the Validation module for this program."
            ))
        self.chkFMEA = ramstk.RAMSTKCheckButton(
            label=_("(D)FME(C)A Module Active"),
            tooltip=_(
                "Activates/deactivates the (D)FME(C)A module for this program."
            ))

        self.__make_ui()

    def __make_modules_page(self):
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

        return None

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _n_screens = Gdk.Screen.get_default().get_n_monitors()
        _width = Gdk.Screen.width() / _n_screens
        _height = Gdk.Screen.height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))

        self.btnSave.connect('clicked', self._do_request_update)
        self.btnQuit.connect('clicked', self._do_quit)

        self._lst_handler_id.append(
            self.chkFunctions.connect('toggled', self._on_toggled, 0))
        self._lst_handler_id.append(
            self.chkRequirements.connect('toggled', self._on_toggled, 1))
        self._lst_handler_id.append(
            self.chkHardware.connect('toggled', self._on_toggled, 2))
        self._lst_handler_id.append(
            self.chkValidation.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.chkFMEA.connect('toggled', self._on_toggled, 4))

        self.__make_page()

        _vbox = Gtk.HBox()

        _buttonbox = Gtk.VButtonBox()
        _buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        _buttonbox.pack_start(self.btnSave, True, True, 0)
        _buttonbox.pack_start(self.btnQuit, True, True, 0)
        _vbox.pack_start(_buttonbox, False, True, 0)

        _vbox.pack_end(self.notebook, True, True, 0)

        self.add(_vbox)

        self._dtc_data_controller.request_do_select_all(
            site=False, program=True)
        self._load_page()

        self.show_all()

        return None

    def _do_quit(self, __button):
        """
        Quit the options Gtk.Assistant().

        :param Gtk.Button __button: the Gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.destroy()

        return False

    def _do_request_update(self, __button):
        """
        Save the configuration changes made by the user.

        :param __button: the Gtk.Button() that called this method.
        :param __button: :class:`Gtk.Button`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update()

    def _load_page(self):
        """
        Load the current options.

        :return: None
        :rtype: None
        """
        _program_options = self._dtc_data_controller.request_get_options(
            site=False, program=True)

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

        return None

    def _on_toggled(self, togglebutton, index):
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param togglebutton: the RAMSTKToggleButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKToggleButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        togglebutton.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _program_options = self._dtc_data_controller.request_get_options(
                site=False, program=True)

            if index == 0:
                _text = boolean_to_integer(self.chkFunctions.get_active())
                _program_options['function_active'] = _text
            elif index == 1:
                _text = boolean_to_integer(self.chkRequirements.get_active())
                _program_options['requirement_active'] = _text
            elif index == 2:
                _text = boolean_to_integer(self.chkHardware.get_active())
                _program_options['hardware_active'] = _text
            elif index == 3:
                _text = boolean_to_integer(self.chkValidation.get_active())
                _program_options['validation_active'] = _text
            elif index == 4:
                _text = boolean_to_integer(self.chkFMEA.get_active())
                _program_options['fmea_active'] = _text

            self._dtc_data_controller.request_set_options(
                _program_options, site=False, program=True)

        togglebutton.handler_unblock(self._lst_handler_id[index])

        return None
