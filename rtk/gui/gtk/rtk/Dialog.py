# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Dialog.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
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
    from gtk import Dialog, MessageDialog, Image, DIALOG_MODAL, \
                    DIALOG_DESTROY_WITH_PARENT, STOCK_OK, STOCK_CANCEL, \
                    RESPONSE_OK, RESPONSE_CANCEL, MESSAGE_ERROR, BUTTONS_OK, \
                    MESSAGE_WARNING, MESSAGE_INFO, MESSAGE_QUESTION, \
                    BUTTONS_YES_NO
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class RTKDialog(Dialog):
    """
    This is the RTK Dialog class.
    """

    def __init__(self, dlgtitle, dlgparent=None,
                 dlgflags=(DIALOG_MODAL | DIALOG_DESTROY_WITH_PARENT),
                 dlgbuttons=(STOCK_OK, RESPONSE_OK,
                             STOCK_CANCEL, RESPONSE_CANCEL)):
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


class RTKMessageDialog(MessageDialog):
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

        _image = Image()
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
            _criticality = MESSAGE_ERROR
            _buttons = BUTTONS_OK
        elif criticality == 'warning':
            _criticality = MESSAGE_WARNING
            _buttons = BUTTONS_OK
        elif criticality == 'information':
            _criticality = MESSAGE_INFO
            _buttons = BUTTONS_OK
        elif criticality == 'question':
            _criticality = MESSAGE_QUESTION
            _buttons = BUTTONS_YES_NO

        MessageDialog.__init__(self, parent, DIALOG_DESTROY_WITH_PARENT,
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
