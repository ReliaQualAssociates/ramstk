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
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKDialog, RAMSTKLabel
)


class EditOptions(RAMSTKDialog):
    """Provide a GUI to set various RAMSTK configuration options.

    RAMSTK options are stored in the RAMSTK Common database and the RAMSTK
    Program database.  RAMSTK options are site-specific or program-specific and
    apply to all users.  Options should not be confused with user-specific
    configurations preferences which are stored in RAMSTK.conf in each user's
    $HOME/.config/RAMSTK directory and are applicable only to that specific
    user.  Configuration preferences are edited with the Preferences assistant.

    Attributes of the EditOptions are:
    """
    # Define private dict class attributes.
    _dic_keys: Dict[int, str] = {
        0: 'function_active',
        1: 'requirement_active',
        2: 'hardware_active',
        3: 'vandv_active',
        4: 'fmea_active',
        5: 'pof_active'
    }

    def __init__(self, parent: object = None) -> None:
        """Initialize an instance of the Options assistant.

        :param parent: the parent window for this assistant.
        """
        super().__init__(_("RAMSTK Program Options Assistant"),
                         dlgparent=parent)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
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

        self.lst_widgets = [
            self.chkFunctions, self.chkRequirements, self.chkHardware,
            self.chkValidation, self.chkFMEA, self.chkPoF
        ]

        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'succeed_get_options_tree')

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        self.set_default_size(250, -1)

        _fixed = Gtk.Fixed()

        _label = RAMSTKLabel(
            _("This is the RAMSTK Program options editor.  This assistant "
              "will allow you to select the work stream modules to use in "
              "the open RAMSTK Program.  Keep in mind that the active work "
              "stream modules are Revision dependent."))
        _label.do_set_properties(width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)

        _y_pos: int = _label.get_preferred_size()[0].height + 50

        _fixed.put(self.chkFunctions, 10, _y_pos)
        _fixed.put(self.chkRequirements, 10, _y_pos + 35)
        _fixed.put(self.chkHardware, 10, _y_pos + 65)
        _fixed.put(self.chkValidation, 10, _y_pos + 95)
        _fixed.put(self.chkFMEA, 10, _y_pos + 125)

        self.vbox.pack_start(_fixed, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """Set EditOption widgets callback methods.

        :return: None
        :rtype: None
        """
        self.chkFunctions.dic_handler_id[
            'toggled'] = self.chkFunctions.connect('toggled', self._on_toggled,
                                                   0)
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
        self.chkPoF.dic_handler_id['toggled'] = self.chkPoF.connect(
            'toggled', self._on_toggled, 5)

    def _cancel(self, __button: Gtk.Button):
        """Destroy the assistant when the 'Cancel' button is pressed.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        """
        self.do_destroy()

    def _do_load_page(self, tree: Tree) -> None:
        """Load the current options.

        :return: None
        :rtype: None
        """
        try:
            _program_options = tree.get_node(
                'programinfo').data['programinfo'].get_attributes()
        except AttributeError:
            _program_options = dict(function_active=0,
                                    requirement_active=0,
                                    hardware_active=0,
                                    vandv_active=0,
                                    fmea_active=0,
                                    pof_active=0)

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

    def _on_toggled(self, checkbutton: RAMSTKCheckButton, index: int) -> None:
        """Handle RAMSTKCheckButton() 'toggle' signals.

        :param checkbutton: the RAMSTKCheckButton() that called this method.
        :type: :class:`gui.gtk.ramstk.Button.RAMSTKToggleButton`
        :param index: the index of the Gtk.CheckButton() in the list
            handler list.
        :return: None
        :rtype: None
        """
        # ISSUE: Add code to record user creating program database.
        # //
        # // There should be code to record in the RAMSTKProgramInfo table
        # // the logged in user who creates the database.  This will require
        # // a function/method to identify the logged in user as well as a
        # // function/method to write this to the new database.
        # //
        # // labels: status:globalbacklog, severity:normal, type:enhancement

        # ISSUE: Add code to record user updating program database.
        # //
        # // There should be code to record in the RAMSTKProgramInfo table
        # // the logged in user who is updating the database.  This will
        # // require a function/method to identify the logged in user as well
        # // as a function/method to write this to the database everytime a
        # // datamanager successfully updates a database table.
        # //
        # // labels: status:globalbacklog, severity:normal, type:enhancement
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
