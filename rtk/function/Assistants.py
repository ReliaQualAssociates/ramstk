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
<<<<<<< HEAD
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg
=======
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# Add localization support.
try:
<<<<<<< HEAD
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


<<<<<<< HEAD
class AddFunction(object):
=======
class AddFunction(gtk.Assistant):
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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

<<<<<<< HEAD
        # Initialize private scalar attributes.
=======
        gtk.Assistant.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self._modulebook = modulebook
        self._controller = modulebook.mdcRTK
        if level == 0:
            self._level = "sibling"
        else:
            self._level = "child"
        self._revision_id = revision_id
        self._parent_id = parent_id

<<<<<<< HEAD
        # Initialize public scalar attributes.
        self.assistant = gtk.Assistant()

        self.txtQuantity = _widg.make_entry(width=50)
        self.txtFunctionCode = _widg.make_entry(width=100)
        self.txtFunctionName = _widg.make_entry()
=======
        self.set_title(_(u"RTK Add Function Assistant"))
        self.set_transient_for(modulebook.mdcRTK.work_book)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.txtQuantity = Widgets.make_entry(width=50)
        self.txtFunctionCode = Widgets.make_entry(width=100)
        self.txtFunctionName = Widgets.make_entry()
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
        _label = _widg.make_label(_text, width=500, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)
=======
        _label = Widgets.make_label(_text, width=500, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(_fixed, _(u"Introduction"))
        self.set_page_complete(_fixed, True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        # Create the page for selecting whether to add a sibling or child
        # Function and how many.
        _fixed = gtk.Fixed()

        self.txtQuantity.set_tooltip_text(_(u"Enter the number of functions "
                                            u"to add."))

<<<<<<< HEAD
        _label = _widg.make_label(_(u"Select the number of {0:s} functions "
                                    u"to add...".format(self._level)),
                                  width=600, height=-1, wrap=True)
=======
        _label = Widgets.make_label(_(u"Select the number of {0:s} functions "
                                      u"to add...".format(self._level)),
                                    width=600, height=-1, wrap=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        _labels = [_(u"Number of {0:s} functions to add:").format(self._level)]
<<<<<<< HEAD
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, _y_pos)
=======
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, _y_pos)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _x_pos += 50
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[0])
        self.txtQuantity.set_text("1")

<<<<<<< HEAD
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_fixed, _(u"Select Number of New "
                                                u"Functions to Add"))
        self.assistant.set_page_complete(_fixed, True)
=======
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_fixed, _(u"Select Number of New Functions to "
                                      u"Add"))
        self.set_page_complete(_fixed, True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        # Create the new Function information page.
        _fixed = gtk.Fixed()

        _labels = [_(u"Function Code:"), _(u"Function Name:"), _(u"Remarks:")]
<<<<<<< HEAD
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
=======
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
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
=======
        _textview_ = Widgets.make_text_view(txvbuffer=self.txtRemarks,
                                            width=300, height=100)
        _fixed.put(_textview_, _x_pos, _y_pos[2])

        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_fixed, _(u"Set Values for the New "
                                      u"Function(s)."))
        self.set_page_complete(_fixed, True)

        # Create the confirmation page.
        _fixed = gtk.Fixed()
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(_fixed, _(u"Function: Confirm Addition"))
        self.set_page_complete(_fixed, True)

        # Connect to callback methods.
        self.connect('apply', self._add_function)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        self.show_all()
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    def _add_function(self, __assistant):
        """
        Method to add the new Function to the open RTK Project database.

        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
<<<<<<< HEAD
        """

=======
        :return: False
        :rtype: bool
        """
# TODO: Re-write _add_function; current McCabe metric = 11
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        # Find out how many Functions to add.  Defaults to one Function if the
        # user hasn't entered and value.
        try:
            _n_functions = int(self.txtQuantity.get_text())
        except ValueError:
            _n_functions = 1

<<<<<<< HEAD
        _basecode = self.txtFunctionCode.get_text()
        if _basecode == '' or _basecode is None:
            _basecode = str(_conf.RTK_PREFIX[2])

        # If specified, the same name will be used for _n_function newly added
        # Functions.
=======
        # If specified, the same base code will be used for _n_function newly
        # added Functions.
        _basecode = self.txtFunctionCode.get_text()

        # If specified, the same base name will be used for _n_function newly
        # added Functions.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _name = self.txtFunctionName.get_text()

        # The same remarks will be used for _n_function newly added Functions.
        _remarks = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())

        # By default we add the new function as a top-level function.
        if self._parent_id is None:
            self._parent_id = -1

<<<<<<< HEAD
        for i in range(_n_functions):
            # Create the Function code for the new Function.
            _code = '{0:s}-{1:d}'.format(_basecode, _conf.RTK_PREFIX[3])
=======
        _error_codes = []
        for i in range(_n_functions):
            # Create the Function code for the new Function.
            if _basecode == '' or _basecode is None:
                _code = '{0:s}-{1:d}'.format(str(Configuration.RTK_PREFIX[2]),
                                             Configuration.RTK_PREFIX[3])
            else:
                _code = '{0:s}-{1:d}'.format(_basecode,
                                             Configuration.RTK_PREFIX[3])
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the Function name if one hasn't been specified.
            if _name == '' or _name is None:
                _name = 'New Function {0:d}'.format(i + 1)

<<<<<<< HEAD
            # Add the new Function.
=======
            # Add the new Function.  If there was an error adding the function
            # update the error_codes list with a tuple (Iteration, Error Code)
            # otherwise add a new functional FMEA for new Function and add the
            # new Function to each of the functional Matrix.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            (_results,
             _error_code,
             _function_id) = self._controller.dtcFunction.add_function(
                 self._revision_id, self._parent_id, _code, _name, _remarks)

<<<<<<< HEAD
            # Increment the Function index.
            _conf.RTK_PREFIX[3] += 1

        # TODO: Add FMEA mode for new Function.
=======
            if _error_code != 0:
                _error_codes.append((i, _error_code))
            else:
                # Add a FMEA with one failure mode to the new Function.
                self._controller.dtcFMEA.add_fmea(None, _function_id)
                self._controller.dtcFMEA.add_mode(None, _function_id)

                # Add the new Function to each of the Function matrices.
                for _matrix_id in [0, 1, 2]:
                    self._controller.dtcMatrices.add_row(_matrix_id,
                                                         self._parent_id,
                                                         _function_id,
                                                         val1=_code,
                                                         val2=_name)

            # Increment the Function index.
            Configuration.RTK_PREFIX[3] += 1

        # Handle any errors returned.  Write each of them to the debug log and
        # then raise an error dialog.
        for __, _code in enumerate(_error_codes):
            _content = "rtk.function.Assistant._add_function: " \
                       "Received error code {1:d} while adding function " \
                       "{0:d} of {3:d}.".format(_code[0], _code[1],
                                                _n_functions)
            self._modulebook.mdcRTK.debug_log.error(_content)

        if len(_error_codes) > 0:
            _prompt = _(u"An error occurred while attempting to add one or "
                        u"more functions.")
            Utilities.rtk_error(_prompt)

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self._modulebook.request_load_data(self._controller.project_dao,
                                           self._revision_id)

        return False

<<<<<<< HEAD
    def _cancel(self, __button):
=======
    def _cancel(self, __assistant):
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

<<<<<<< HEAD
        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.assistant.destroy()
=======
        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
        """

        self.destroy()
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
