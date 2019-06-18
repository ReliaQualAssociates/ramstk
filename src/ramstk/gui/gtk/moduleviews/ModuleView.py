# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.ModuleView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKModuleView Module."""

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKBaseView
#from ramstk.gui.gtk.assistants import ExportModule
from ramstk.gui.gtk.ramstk.Widget import GObject, Gtk


class RAMSTKModuleView(Gtk.HBox, RAMSTKBaseView):
    """
    Display data in the RAMSTK Module Book.

    This is the meta class for all RAMSTK Module View classes.  Attributes of
    the RAMSTKModuleView are:

    :ivar _img_tab: the :class:`Gtk.Image` to display on the tab.
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize the RAMSTKModuleView meta-class.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        _module = kwargs['module']

        GObject.GObject.__init__(self)
        RAMSTKBaseView.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_icons['insert_part'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/insert_part.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._img_tab = Gtk.Image()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__set_callbacks()

    def __set_callbacks(self):
        """
        Set common callback methods for the ModuleView and widgets.

        :return: None
        :rtype: None
        """
        try:
            self._lst_handler_id.append(
                self.treeview.connect('cursor_changed', self._on_row_change),
            )
        except AttributeError:
            pass

        try:
            self._lst_handler_id.append(
                self.treeview.connect('button_press_event', self._on_button_press),
            )
        except AttributeError:
            pass

    def __set_properties(self):
        """
        Set common properties of the ModuleView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_rubber_banding(True)

    def do_request_export(self, module):
        """
        Launch the Export assistant.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        #_tree = self._dtc_data_controller.request_do_select_all(
        #    revision_id=self._revision_id)
        #ExportModule(self._mdcRAMSTK, module, _tree)

    def make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self._img_tab.set_from_file(self._dic_icons['tab'])

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)
        self.pack_end(_scrolledwindow, True, True, 0)

        self.hbx_tab_label.pack_start(self._img_tab, True, True, 0)
        self.hbx_tab_label.show_all()

        self.show_all()

    def on_button_press(self, event, **kwargs):
        """
        Handle mouse clicks on the Module View RAMSTKTreeView().

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
        _icons = kwargs['icons']
        _labels = kwargs['labels']
        _callbacks = kwargs['callbacks']

        # Append the default save and save-all buttons found on all Module View
        # pop-up menus.
        try:
            _icons.extend(['remove', 'save', 'save-all'])
            _callbacks.extend([
                self._do_request_delete, self._do_request_update,
                self._do_request_update_all,
            ])
        except AttributeError:
            pass

        RAMSTKBaseView.on_button_press(
            self, event, icons=_icons, labels=_labels, callbacks=_callbacks,
        )
