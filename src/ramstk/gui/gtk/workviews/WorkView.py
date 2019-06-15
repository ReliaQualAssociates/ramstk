# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.WorkView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKWorkView Meta-Class Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import (
    RAMSTKBaseView, RAMSTKFrame, RAMSTKScrolledWindow,
    do_make_buttonbox, do_make_label_group,
)
from ramstk.gui.gtk.ramstk.Widget import GObject, Gtk, _


class RAMSTKWorkView(Gtk.HBox, RAMSTKBaseView):
    """
    Class to display data in the RAMSTK Work Book.

    This is the meta class for all RAMSTK Work View classes.  Attributes of the
    RAMSTKWorkView are:

    :ivar str _module: the all capitalized name of the RAMSKT module the View
    is for.
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize the RAMSTKWorkView meta-class.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        _module = kwargs['module']
        GObject.GObject.__init__(self)
        RAMSTKBaseView.__init__(self, configuration, module=_module)

        self._module = None
        for __, char in enumerate(_module):
            if char.isalpha():
                self._module = _module.capitalize()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_select_revision, 'selected_revision')

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

    def _make_buttonbox(self, **kwargs):
        """
        Create the Gtk.ButtonBox() for the Work Views.

        :return: _buttonbox; the Gtk.ButtonBox() for the Work View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _icons = kwargs['icons']
        _tooltips = kwargs['tooltips']
        _callbacks = kwargs['callbacks']

        # do_make_buttonbox always adds the save and save-all options to the
        # end of the list of callbacks, icons, and tooltips that are passed to
        # this method.
        _buttonbox = do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1,
        )

        return _buttonbox

    def _on_select_revision(self, attributes):
        """
        Respond to the `selected_revision` signal from pypubsub.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

    def make_ui(self, **kwargs):
        """
        Make the Function class Gtk.Notebook() general data page.

        :return: (_x_pos, _y_pos, _fixed); the x-position of the left edge of
        each widget, the list of y-positions of the top of each widget, and the
        Gtk.Fixed() that all the widgets are placed on.
        :rtype: (int, list, :class:`Gtk.Fixed`)
        """
        _icons = kwargs['icons']
        _tooltips = kwargs['tooltips']
        _callbacks = kwargs['callbacks']

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrolledwindow.add_with_viewport(
            self._make_buttonbox(
                icons=_icons, tooltips=_tooltips, callbacks=_callbacks,
            ),
        )
        self.pack_start(_scrolledwindow, False, False, 0)

        _fixed = Gtk.Fixed()

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame(label=_("General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = do_make_label_group(self._lst_labels, _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])

        self.pack_start(_frame, True, True, 0)

        return(_x_pos, _y_pos, _fixed)

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
            _icons.extend(['save', 'save-all'])
            _labels.extend([_("Save Selected"), _("Save All")])
            _callbacks.extend([
                self._do_request_update,
                self._do_request_update_all,
            ])
        except AttributeError:
            pass

        RAMSTKBaseView.on_button_press(
            self, event, icons=_icons, labels=_labels, callbacks=_callbacks,
        )
