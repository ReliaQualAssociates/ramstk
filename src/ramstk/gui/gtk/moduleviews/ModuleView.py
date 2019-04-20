# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.ModuleView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKModuleView Module."""

# Import other RAMSTK modules.
from ramstk.gui.gtk.assistants import ExportModule
from ramstk.gui.gtk.ramstk.Widget import gtk
from ramstk.gui.gtk import ramstk


class RAMSTKModuleView(gtk.HBox, ramstk.RAMSTKBaseView):
    """
    Display data in the RAMSTK Module Book.

    This is the meta class for all RAMSTK Module View classes.  Attributes of
    the RAMSTKModuleView are:

    :ivar _img_tab: the :class:`gtk.Image` to display on the tab.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View gtk.TreeView().
    :ivar hbx_tab_label: the :class:`gtk.HBox` used for the label in the
                         ModuleBook.
    :ivar treeview: the :class:`gtk.TreeView` displaying the list of items
                    in the selected module.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the RAMSTKModuleView meta-class.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :py:class:`ramstk.RAMSTK.RAMSTK`
        :param str module: the module that is being loaded.
        """
        gtk.HBox.__init__(self)
        ramstk.RAMSTKBaseView.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_icons['insert_part'] = \
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/insert_part.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._img_tab = gtk.Image()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrolledwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrolledwindow, expand=False, fill=False)

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.show_all()

        self.show_all()

    def do_request_export(self, module):
        """
        Launch the Export assistant.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _tree = self._dtc_data_controller.request_do_select_all(
            revision_id=self._revision_id)
        ExportModule(self._mdcRAMSTK, module, _tree)

        return None
