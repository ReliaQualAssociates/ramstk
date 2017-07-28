#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.revision.Assistants.py is part of The RTK Project
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
##################################
Revision Package Assistants Module
##################################
"""

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
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.gui.gtk.Widgets as Widgets       # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "Weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class AddRevision(object):

    """
    This is the assistant that walks the user through the process of adding
    a new Revision to the open RTK Project database.
    """

    def __init__(self, modulebook):
        """
        Method to initialize on instance of the Add Revision Assistant.

        :param modulebook: the current instance of
                           :py:class:`rtk.revision.ModuleBook`
        """

        # Initialize private scalar attributes.
        self._modulebook = modulebook
        self._controller = modulebook.mdcRTK

        # Initialize public scalar attributes.
        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RTK Revision Addition Assistant"))
        self.assistant.connect('apply', self._add_revision)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _text = _(u"This is the RTK Revision Addition Assistant.  It will "
                  u"help you add a new revision to the database.  Press "
                  u"'Forward' to continue or 'Cancel' to quit the assistant.")
        _label = Widgets.make_label(_text, width=500, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # Create the page to select other information to add.
        y_pos = 5
        self.fxdPageOtherInfo = gtk.Fixed()
        _label = Widgets.make_label(_(u"Select additional information "
                                      u"to copy from old revision..."),
                                    width=300)
        self.fxdPageOtherInfo.put(_label, 5, y_pos)
        y_pos += 30

        self.chkFunction = gtk.CheckButton(_(u"_Functions"))
        self.fxdPageOtherInfo.put(self.chkFunction, 5, y_pos)
        y_pos += 30

        self.chkFunctionMatrix = gtk.CheckButton(_(u"Functional _Matrix"))
        self.fxdPageOtherInfo.put(self.chkFunctionMatrix, 5, y_pos)
        y_pos += 30

        self.chkRequirements = gtk.CheckButton(_(u"_Requirements"))
        self.fxdPageOtherInfo.put(self.chkRequirements, 5, y_pos)
        y_pos += 30

        self.chkHardware = gtk.CheckButton(_(u"_Hardware"))
        self.fxdPageOtherInfo.put(self.chkHardware, 5, y_pos)
        y_pos += 30

        self.chkSoftware = gtk.CheckButton(_(u"_Software"))
        self.fxdPageOtherInfo.put(self.chkSoftware, 5, y_pos)
        y_pos += 30

        self.chkFailureInfo = gtk.CheckButton(_(u"Include reliability "
                                                u"information"))
        self.fxdPageOtherInfo.put(self.chkFailureInfo, 5, y_pos)
        y_pos += 30

        self.chkFMEA = gtk.CheckButton(_(u"Include FMEA information"))
        self.fxdPageOtherInfo.put(self.chkFailureInfo, 5, y_pos)

        self.assistant.append_page(self.fxdPageOtherInfo)
        self.assistant.set_page_type(self.fxdPageOtherInfo,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageOtherInfo,
                                      _(u"Select Additional Information to "
                                        u"Add"))
        self.assistant.set_page_complete(self.fxdPageOtherInfo, True)

        # Create the page for entering the new Revision information.
        self.fxdPageSetValues = gtk.Fixed()
        _label = Widgets.make_label(_(u"Revision Code:"))
        self.txtRevisionCode = Widgets.make_entry(width=100)
        self.txtRevisionCode.set_tooltip_text(_(u"Enter a code for the new "
                                                u"revision.  Leave blank to "
                                                u"use the default revision "
                                                u"code."))
        self.fxdPageSetValues.put(_label, 5, 5)
        self.fxdPageSetValues.put(self.txtRevisionCode, 200, 5)

        _label = Widgets.make_label(_(u"Revision Name:"))
        self.txtRevisionName = Widgets.make_entry()
        self.txtRevisionName.set_tooltip_text(_(u"Enter a name for the new "
                                                u"revision.  Leave blank to "
                                                u"use the default revision "
                                                u"name."))
        self.fxdPageSetValues.put(_label, 5, 35)
        self.fxdPageSetValues.put(self.txtRevisionName, 200, 35)

        _label = Widgets.make_label(_(u"Remarks:"))
        self.txtRemarks = gtk.TextBuffer()
        self.fxdPageSetValues.put(_label, 5, 65)
        _textview = Widgets.make_text_view(txvbuffer=self.txtRemarks,
                                           width=300, height=100)
        self.fxdPageSetValues.put(_textview, 200, 65)

        self.assistant.append_page(self.fxdPageSetValues)
        self.assistant.set_page_type(self.fxdPageSetValues,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageSetValues, _(u"Set Values "
                                                               u"for New "
                                                               u"Revision"))
        self.assistant.set_page_complete(self.fxdPageSetValues, True)

        _fixed = gtk.Fixed()
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Revision: Confirm Addition"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

    def _add_revision(self, __assistant):
        """
        Method to add the new Revision to the open RTK Project database.

        :param gtk.Assistant __assistant: the current instance of the
                                          gtk.Assistant().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # Create the Revision code.
        _code = self.txtRevisionCode.get_text()
        if _code == '' or _code is None:
            _code = '{0:s} {1:s}'.format(str(Configuration.RTK_PREFIX[0]),
                                         str(Configuration.RTK_PREFIX[1]))

            # Increment the Revision index.
            Configuration.RTK_PREFIX[1] += 1

        _name = self.txtRevisionName.get_text()
        if _name == '' or _name is None:
            _name = 'New Revision'

        _remarks = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())

        # Add the new Revision.
        (_results,
         _error_code,
         _revision_id) = self._controller.dtcRevision.add_revision(_code,
                                                                   _name,
                                                                   _remarks)

        if _error_code != 0:
            _prompt = _(u"An error occurred while attempting to add the new "
                        u"revision.")
            Widgets.rtk_error(_prompt)
            _return = True
        else:
            # FIXME: See bug 184.
            if self.chkFunction.get_active():
                _dic_f_xref = self._controller.dtcFunction.copy_function(
                                _revision_id)
                if self.chkFMEA.get_active():
                    for _key in _dic_f_xref.keys():
                        _new_id = _dic_f_xref[_key]
                        self._controller.dtcFMEA.copy_fmea(_new_id, None, _key)

            if self.chkRequirements.get_active():
                self._controller.dtcRequirement.copy_requirements(_revision_id)

            if self.chkHardware.get_active():
                _failure_info = self.chkFailureInfo.get_active()
                _matrices = self.chkFunctionMatrix.get_active()
                self._controller.dtcHardwareBoM.copy_hardware(_revision_id,
                                                              _failure_info,
                                                              _matrices)

            if self.chkSoftware.get_active():
                self._controller.dtcSoftwareBoM.copy_software(_revision_id)

            self._modulebook.request_load_data(self._controller.project_dao)

        return _return

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.assistant.destroy()
