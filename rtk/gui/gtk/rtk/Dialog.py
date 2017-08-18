#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Dialog.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is specific to dialog widgets.
"""

import gettext
import sys

# Modules required for the GUI.
try:
    from pygtk import require
    require('2.0')
except ImportError:
    sys.exit(1)
try:
    from gtk import Dialog, MessageDialog
except ImportError:
    sys.exit(1)
try:
    import gtk.glade  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class RTKDialog(gtk.Dialog):
    """
    This is the RTK Dialog class.
    """

    def __init__(self, dlgtitle, dlgparent=None,
                 dlgflags=(gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT),
                 dlgbuttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)):
        """
        Method to create a RTK Dialog widget.

        :param str dlgtitle: the title text for the gtk.Dialog().
        :keyword gtk.Window dlgparent: the parent window to associate the
                                       gtk.Dialog() with.
        :keyword tuple dlgflags: the flags that control the operation of the
                                 gtk.Dialog().  Defaults to gtk.DIALOG_MODAL
                                 and gtk.DIALOG_DESTROY_WITH_PARENT.
        :keyword tuple dlgbuttons: the buttons to display and their response
                                   values.  Defaults to:
                                   gtk.STOCK_OK <==> gtk.RESPONSE_ACCEPT
                                   gtk.STOCK_CANCEL <==> gtk.RESPONSE_REJECT
        :return: _dialog
        :rtype: gtk.Dialog
        """

        gtk.Dialog.__init__(self, title=dlgtitle, parent=dlgparent,
                            flags=dlgflags, buttons=dlgbuttons)

        self.set_has_separator(True)


class RTKMessageDialog(gtk.MessageDialog):
    """
    This is the RTK Message Dialog class.  It used for RTK error, warning, and
    information messages.
    """

    def __init__(self, prompt, icon, criticality, parent=None):
        """
        Method to initialize runtime error, warning, and information dialogs.

        :param str prompt: the prompt to display in the dialog.
        :param str icon: the absolute path to the icon to display on the
                         dialog.
        :param str criticality: the criticality level of the dialog.
                                Criticality is one of:

                                * 'error'
                                * 'warning'
                                * 'information'

        :keyword gtk.Window _parent: the parent gtk.Window(), if any, for the
                                     dialog.
        """

        _image = gtk.Image()
        _image.set_from_file(icon)

        if criticality == 'error':
            # Set the prompt to bold text with a hyperlink to the RTK bugs
            # e-mail address.
            _hyper = "<a href='mailto:bugs@reliaqual.com?subject=RTK BUG " \
                     "REPORT: <ADD SHORT PROBLEM DESCRIPTION>&amp;" \
                     "body=RTK MODULE:%0d%0a%0d%0a" \
                     "RTK VERSION:%20%0d%0a%0d%0a" \
                     "YOUR HARDWARE:%20%0d%0a%0d%0a" \
                     "YOUR OS:%20%0d%0a%0d%0a" \
                     "DETAILED PROBLEM DESCRIPTION:%20%0d%0a'>"
            prompt = '<b>' \
                     + prompt \
                     + _(u"  Check the error log for additional information "
                         u"(if any).  Please e-mail <span foreground='blue' "
                         u"underline='single'>") \
                     + _hyper \
                     + _(u"bugs@reliaqual.com</a></span> with a detailed "
                         u"description of the problem, the workflow you are "
                         u"using and the error log attached if the problem "
                         u"persists.</b>")
            _criticality = gtk.MESSAGE_ERROR
            _buttons = gtk.BUTTONS_OK
        elif criticality == 'warning':
            _criticality = gtk.MESSAGE_WARNING
            _buttons = gtk.BUTTONS_OK
        elif criticality == 'information':
            _criticality = gtk.MESSAGE_INFO
            _buttons = gtk.BUTTONS_OK
        elif criticality == 'question':
            _criticality = gtk.MESSAGE_QUESTION
            _buttons = gtk.BUTTONS_YES_NO

        gtk.MessageDialog.__init__(self, parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT,
                                   _criticality, _buttons)

        self.set_markup(prompt)
        self.set_image(_image)
        self.show_all()

    def do_run(self):
        """
        Method to run the RTK Message Dialog.
        """

        return self.run()

    def do_destroy(self):
        """
        Method to destroy the RTK Message Dialog.
        """

        self.destroy()
