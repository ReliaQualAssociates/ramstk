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
from ramstk.gui.gtk.ramstk import RAMSTKBaseView, do_make_buttonbox
from ramstk.gui.gtk.ramstk.Widget import GObject, Gtk


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

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_select_revision, 'selected_revision')

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

    def _on_select_revision(self, **kwargs):
        """
        Respond to the `selected_revision` signal from pypubsub.

        :return: None
        :rtype: None
        """
        self._revision_id = kwargs['module_id']
