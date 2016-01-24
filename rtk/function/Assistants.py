#!/usr/bin/env python
"""
##################################
Function Package Assistants Module
##################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.function.Assistants.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import sys

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class AddFunction(object):
    """
    This is the assistant that walks the user through the process of adding
    a new Function to the open RTK Project database.
    """

    def __init__(self, modulebook, level, revision_id, parent_id=None):
        """
        Initialize on instance of the Add Function Assistant.

        :param modulebook: the current instance of
                           :py:class:`rtk.function.ModuleBook`
        :param int level: the level of the new Function to add
                          (0 = sibling, 1 = child).
        :param int revision_id: the ID of the Revision to add the new
                                Function(s) to.
        :keyword int parent_id: the ID of the parent Function to add the new
                                Function(s) to.
        """

        # Initialize private scalar attributes.
        self._modulebook = modulebook
        self._controller = modulebook.mdcRTK
        if level == 0:
            self._level = "sibling"
        else:
            self._level = "child"
        self._revision_id = revision_id
        self._parent_id = parent_id

        # Initialize public scalar attributes.
        self.assistant = gtk.Assistant()

        self.txtQuantity = _widg.make_entry(width=50)
        self.txtFunctionCode = _widg.make_entry(width=100)
        self.txtFunctionName = _widg.make_entry()
        self.txtRemarks = gtk.TextBuffer()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the introduction page.
        _fixed = gtk.Fixed()
        _text = _(u"This is the RTK Function Addition Assistant.  It will "
                  u"help you add a new sibling or child function to the "
                  u"database.  Press 'Forward' to continue or 'Cancel' to "
                  u"quit the assistant.")
        _label = _widg.make_label(_text, width=500, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # Create the page for selecting whether to add a sibling or child
        # Function and how many.
        _fixed = gtk.Fixed()

        self.txtQuantity.set_tooltip_text(_(u"Enter the number of functions "
                                            u"to add."))

        _label = _widg.make_label(_(u"Select the number of {0:s} functions "
                                    u"to add...".format(self._level)),
                                  width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        _labels = [_(u"Number of {0:s} functions to add:").format(self._level)]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, _y_pos)
        _x_pos += 50
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[0])
        self.txtQuantity.set_text("1")

        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_fixed, _(u"Select Number of New "
                                                u"Functions to Add"))
        self.assistant.set_page_complete(_fixed, True)

        # Create the new Function information page.
        _fixed = gtk.Fixed()

        _labels = [_(u"Function Code:"), _(u"Function Name:"), _(u"Remarks:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 50

        self.txtFunctionCode.set_tooltip_text(_(u"Enter a code for the new "
                                                u"function.  Leave blank to "
                                                u"use the default function "
                                                u"code."))
        self.txtFunctionName.set_tooltip_text(_(u"Enter a name for the new "
                                                u"function.  Leave blank to "
                                                u"use the default function "
                                                u"name."))

        _fixed.put(self.txtFunctionCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtFunctionName, _x_pos, _y_pos[1])
        _textview_ = _widg.make_text_view(txvbuffer=self.txtRemarks,
                                          width=300, height=100)
        _fixed.put(_textview_, _x_pos, _y_pos[2])

        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_fixed, _(u"Set Values for the New "
                                                u"Function(s)."))
        self.assistant.set_page_complete(_fixed, True)

        # Create the confirmation page.
        _fixed = gtk.Fixed()
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Function: Confirm Addition"))
        self.assistant.set_page_complete(_fixed, True)

        # Connect to callback methods.
        self.assistant.connect('apply', self._add_function)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        self.assistant.show_all()

    def _add_function(self, __assistant):
        """
        Method to add the new Function to the open RTK Project database.

        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
        """

        # Find out how many Functions to add.  Defaults to one Function if the
        # user hasn't entered and value.
        try:
            _n_functions = int(self.txtQuantity.get_text())
        except ValueError:
            _n_functions = 1

        _basecode = self.txtFunctionCode.get_text()
        if _basecode == '' or _basecode is None:
            _basecode = str(_conf.RTK_PREFIX[2])

        # If specified, the same name will be used for _n_function newly added
        # Functions.
        _name = self.txtFunctionName.get_text()

        # The same remarks will be used for _n_function newly added Functions.
        _remarks = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())

        # By default we add the new function as a top-level function.
        if self._parent_id is None:
            self._parent_id = -1

        for i in range(_n_functions):
            # Create the Function code for the new Function.
            _code = '{0:s}-{1:d}'.format(_basecode, _conf.RTK_PREFIX[3])

            # Create the Function name if one hasn't been specified.
            if _name == '' or _name is None:
                _name = 'New Function {0:d}'.format(i + 1)

            # Add the new Function.
            (_results,
             _error_code,
             _function_id) = self._controller.dtcFunction.add_function(
                 self._revision_id, self._parent_id, _code, _name, _remarks)

            # Increment the Function index.
            _conf.RTK_PREFIX[3] += 1

        # TODO: Add FMEA mode for new Function.
        self._modulebook.request_load_data(self._controller.project_dao,
                                           self._revision_id)

        return False

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.assistant.destroy()
