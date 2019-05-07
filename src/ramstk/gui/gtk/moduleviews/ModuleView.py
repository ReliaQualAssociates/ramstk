# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.ModuleView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKModuleView Module."""

# Import other RAMSTK modules.
from ramstk.gui.gtk.assistants import ExportModule
from ramstk.gui.gtk.ramstk.Widget import GObject, Gtk
from ramstk.gui.gtk import ramstk


class RAMSTKModuleView(Gtk.HBox, ramstk.RAMSTKBaseView):
    """
    Display data in the RAMSTK Module Book.

    This is the meta class for all RAMSTK Module View classes.  Attributes of
    the RAMSTKModuleView are:

    :ivar _img_tab: the :class:`Gtk.Image` to display on the tab.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View Gtk.TreeView().
    :ivar hbx_tab_label: the :class:`Gtk.HBox` used for the label in the
                         ModuleBook.
    :ivar treeview: the :class:`Gtk.TreeView` displaying the list of items
                    in the selected module.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the RAMSTKModuleView meta-class.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :py:class:`ramstk.RAMSTK.RAMSTK`
        :param str module: the module that is being loaded.
        """
        GObject.GObject.__init__(self)
        ramstk.RAMSTKBaseView.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_icons['insert_part'] = \
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/insert_part.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._img_tab = Gtk.Image()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def _make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self._img_tab.set_from_file(self._dic_icons['tab'])

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrolledwindow, False, False, 0)

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)
        self.pack_end(_scrolledwindow, True, True, 0)

        self.hbx_tab_label.pack_start(self._img_tab, True, True, 0)
        self.hbx_tab_label.show_all()

        self.show_all()

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        return None

    def do_request_export(self, module):
        """
        Launch the Export assistant.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _tree = self._dtc_data_controller.request_do_select_all(
            revision_id=self._revision_id)
        ExportModule(self._mdcRAMSTK, module, _tree)

        return None
