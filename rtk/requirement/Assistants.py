#!/usr/bin/env python
"""
#####################################
Requirement Package Assistants Module
#####################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.requirement.Assistants.py is part of The RTK Project
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
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class AddRequirement(gtk.Assistant):
    """
    This is the assistant that walks the user through the process of adding
    a new Requirement to the open RTK Project database.  The attributes of an
    Add Requirement Assistant are:

    :ivar _modulebook: the :py:class:`rtk.requirement.ModuleBook` associated
                       with this assistant.
    :ivar _controller: the :py:class:`rtk.RTK.RTK` master data controller to
                       use with this assistant.
    :ivar str _level: the level of the requirement (top-level or derived).
    :ivar int _revision_id: the id of the
                            :py:class:`rtk.revision.Revision.Model` to
                            associate the new Requirement with.
    :ivar int _parent_id: the id of the
                          :py:class:`rtk.requirement.Requirement.Model` that is
                          a parent of the new Requirement.
    :ivar str _code: the string code for the new Requirement.
    :ivar gtk.ComboBox cmbOwner: the gtk.ComboBox() used to selectthe owner of
                                 the new Requirement.
    :ivar gtk.ComboBox cmbRqmtType: the gtk.ComboBox() used to select the type
                                    of the new Requirement.
    :ivar gtk.ComboBox cmbPriority: the gtk.ComboBox() used to select the
                                    priority of the new Requirement.
    :ivar gtk.Entry txtQuantity: the gtk.Entry() used to enter the number of
                                 new Requirements to add.
    :ivar gtk.Entry txtDescription: the gtk.Entry() to enter the description of
                                    the new Requirement(s).
    :ivar gtk.Entry txtSpecification: the gtk.Entry() to enter the engineering
                                      specification associated with the new
                                      Requirement.
    :ivar gtk.Entry txtPageNumber: the gtk.Entry() to enter the page number in
                                   the specification associated the new
                                   Requirement.
    :ivar gtk.Entry txtFigureNumber: the gtk.Entry() to enter the figure number
                                     in the specification associated the new
                                     Requirement.
    """

    def __init__(self, modulebook, level, revision_id, parent_id=None):
        """
        Method to initialize an instance of the Add Requirement Assistant.

        :param modulebook: the current instance of
                           :py:class:`rtk.requirement.ModuleBook`
        :param int level: the level of the new Requirement to add
                          (0 = top-level, 1 = derived).
        :param int revision_id: the ID of the Revision to add the new
                                Requirement(s) to.
        :keyword int parent_id: the ID of the parent Requirement to add the new
                                Requirement(s) to.
        """

        gtk.Assistant.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._modulebook = modulebook
        self._controller = modulebook.mdcRTK
        if level == 0:
            self._level = "top-level"
        else:
            self._level = "derived"
        self._revision_id = revision_id
        self._parent_id = parent_id

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbOwner = Widgets.make_combo(simple=False)
        self.cmbRqmtType = Widgets.make_combo(simple=False)
        self.cmbPriority = Widgets.make_combo(width=50, simple=True)

        self.txtQuantity = Widgets.make_entry(width=50)
        self.txtDescription = gtk.TextBuffer()
        self.txtSpecification = Widgets.make_entry()
        self.txtPageNumber = Widgets.make_entry()
        self.txtFigureNumber = Widgets.make_entry()

        self.set_title(_(u"RTK Add Requirement Assistant"))
        self.set_transient_for(modulebook.mdcRTK.work_book)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        # Load the requirement type gtk.ComboBox().
        _model = self.cmbRqmtType.get_model()
        _model.clear()
        _model.append(None, ["", "", ""])
        # Each _type is [Description, Code, ID]
        for __, _type in enumerate(Configuration.RTK_REQUIREMENT_TYPES):
            _model.append(None, [_type[0], _type[1], ""])

        # Load the owner gtk.ComboBox().
        _model = self.cmbOwner.get_model()
        _owners = self._modulebook.dicOwners.keys()
        _owners.sort()
        _model.clear()
        _model.append(None, ["", "", ""])
        for _owner in _owners:
            _model.append(None, [_owner, "", ""])

        # Load the priority gtk.Combo().
        _results = [['1'], ['2'], ['3'], ['4'], ['5']]
        _model = self.cmbPriority.get_model()
        Widgets.load_combo(self.cmbPriority, _results)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the introduction page.
        _fixed = gtk.Fixed()

        _text = _(u"This is the RTK Requirement Addition Assistant.  It will "
                  u"help you add a new top-level or derived requirement to "
                  u"the database.  Press 'Forward' to continue or 'Cancel' to "
                  u"quit the assistant.")
        _label = Widgets.make_label(_text, width=500, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)

        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(_fixed, _(u"Introduction"))
        self.set_page_complete(_fixed, True)

        # Create the page for selecting whether to add a sibling or child
        # Function and how many.
        _fixed = gtk.Fixed()

        self.txtQuantity.set_tooltip_text(
            _(u"Enter the number of "
              u"requirements to add."))

        _label = Widgets.make_label(
            _(u"Select the number of {0:s} "
              u"requirements to "
              u"add...".format(self._level)),
            width=600,
            height=-1,
            wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        _labels = [
            _(u"Number of {0:s} requirements to "
              u"add:").format(self._level)
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, _y_pos)
        _x_pos += 55
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[0])
        self.txtQuantity.set_text("1")

        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_fixed,
                            _(u"Select Number of New Requirements to "
                              u"Add"))
        self.set_page_complete(_fixed, True)

        # Create the new Requirement information page.
        _fixed = gtk.Fixed()

        self.cmbOwner.set_tooltip_text(
            _(u"Select the owner for new "
              u"requirement."))
        self.cmbRqmtType.set_tooltip_text(
            _(u"Select the type for the new "
              u"requirement."))
        self.cmbPriority.set_tooltip_text(
            _(u"Select the priority of the new "
              u"requirement."))

        # self.txtDescription.set_tooltip_text(_(u"Enter a description of the "
        #                                        u"new requirement."))
        self.txtSpecification.set_tooltip_text(
            _(u"Enter the governing "
              u"specification for the new "
              u"requirement, if any."))
        self.txtPageNumber.set_tooltip_text(
            _(u"Enter the page number in the "
              u"governing specificaiton that "
              u"applies to the new "
              u"requirement, if any."))
        self.txtFigureNumber.set_tooltip_text(
            _(u"Enter the figure number in "
              u"the governing specificaiton "
              u"that applies to the new "
              u"requirement, if any."))

        _labels = [_(u"Requirement:")]
        (_x_pos1, _y_pos1) = Widgets.make_labels(_labels, _fixed, 5, 5)

        _labels = [
            _(u"Requirement Type:"),
            _(u"Specification:"),
            _(u"Page Number:"),
            _(u"Figure Number:"),
            _(u"Owner:"),
            _(u"Priority:")
        ]
        (_x_pos2, _y_pos2) = Widgets.make_labels(_labels, _fixed, 5,
                                                 _y_pos1[0] + 100)
        _x_pos = max(_x_pos1, _x_pos2) + 50

        _textview = Widgets.make_text_view(
            txvbuffer=self.txtDescription, width=400)
        _fixed.put(_textview, _x_pos, _y_pos1[0])
        _fixed.put(self.cmbRqmtType, _x_pos, _y_pos2[0])
        _fixed.put(self.txtSpecification, _x_pos, _y_pos2[1])
        _fixed.put(self.txtPageNumber, _x_pos, _y_pos2[2])
        _fixed.put(self.txtFigureNumber, _x_pos, _y_pos2[3])
        _fixed.put(self.cmbOwner, _x_pos, _y_pos2[4])
        _fixed.put(self.cmbPriority, _x_pos, _y_pos2[5])

        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_fixed,
                            _(u"Set Values for the New "
                              u"Requirement(s)."))
        self.set_page_complete(_fixed, True)

        # Create the confirmation page.
        _fixed = gtk.Fixed()
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(_fixed, _(u"Requirement: Confirm Addition"))
        self.set_page_complete(_fixed, True)

        # Connect to callback methods.
        self.connect('apply', self._add_requirement)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        self.show_all()

    def _add_requirement(self, __assistant):
        """
        Method to add the new Requirement to the open RTK Project database.

        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
        :return: False
        :rtype: bool
        """

        # Find out how many Requirement to add.  Defaults to one Requirement if
        # the user hasn't entered any value.
        try:
            _n_requirements = int(self.txtQuantity.get_text())
        except ValueError:
            _n_requirements = 1

        # If specified, the same information will be used for all
        # _n_requirements to be added.
        _args = self._read_inputs()

        _error_codes = []
        for i in range(_n_requirements):
            # Create the Requirement description if one hasn't been specified.
            if _args[0] == '' or _args[0] is None:
                _args[0] = 'New Requirement {0:d}'.format(i + 1)

            # Add the new Requirement.  If there was an error adding the
            # requirement update the error_codes list with a tuple (Iteration,
            # Error Code) otherwise add the new Requirement to each of the
            # requiremental Matrix.
            (_requirement, _error_code, _requirement_id
             ) = self._controller.dtcRequirement.add_requirement(
                 self._revision_id, self._parent_id, _args)

            if _error_code != 0:
                _error_codes.append((i, _error_code))
            else:
                _requirement = self._controller.dtcRequirement.dicRequirements[
                    _requirement_id]

                # Update the attributes of the newly added Requirement.
                _requirement.code = self._create_code(_requirement_id)
                _requirement.description = _args[0]
                _requirement.requirement_type = _args[1]
                _requirement.specification = _args[2]
                _requirement.page_number = _args[3]
                _requirement.figure_number = _args[4]
                _requirement.owner = _args[5]
                _requirement.priority = _args[6]
                _requirement.derived = _args[7]

                # Add the new Requirement to each of the Requirement matrices.
                for _matrix_id in [3, 4, 5]:
                    self._controller.dtcMatrices.add_row(
                        _matrix_id,
                        self._parent_id,
                        _requirement_id,
                        val1=_requirement.code,
                        val2=_requirement.description)

        # Handle any errors returned.  Write each of them to the debug log and
        # then raise an error dialog.
        for __, _code in enumerate(_error_codes):
            _content = "rtk.requirement.Assistant._add_requirement: " \
                       "Received error code {1:d} while adding requirement " \
                       "{0:d} of {3:d}.".format(_code[0], _code[1],
                                                _n_requirements)
            self._modulebook.mdcRTK.debug_log.error(_content)

        if len(_error_codes) > 0:
            _prompt = _(u"An error occurred while attempting to add one or "
                        u"more requirements.")
            Utilities.rtk_error(_prompt)

        self._modulebook.request_load_data()

        return False

    def _read_inputs(self):
        """
        Method to read the input gtk.Widgets() and pack the values into a list
        to pass as *args to the add_requirement method.

        :return: [_description, _rqmt_type, _specification, _page_number,
                  _figure_number, _owner, _priority, _derived]
        :rtype: list
        """

        _description = self.txtDescription.get_text(
            *self.txtDescription.get_bounds())

        _model = self.cmbRqmtType.get_model()
        _row = self.cmbRqmtType.get_active_iter()
        try:
            _rqmt_type = _model.get_value(_row, 0)
        except TypeError:
            _rqmt_type = ''

        _specification = self.txtSpecification.get_text()
        _page_number = self.txtPageNumber.get_text()
        _figure_number = self.txtFigureNumber.get_text()

        _model = self.cmbOwner.get_model()
        _row = self.cmbOwner.get_active_iter()
        try:
            _owner = _model.get_value(_row, 0)
        except TypeError:
            _owner = ''

        try:
            _priority = int(self.cmbPriority.get_active_text())
        except TypeError:
            _priority = 1

        if self._level == 'derived':
            _derived = 1
        else:
            _derived = 0

        return ([
            _description, _rqmt_type, _specification, _page_number,
            _figure_number, _owner, _priority, _derived
        ])

    def _create_code(self, requirement_id):
        """
        Method to retrieve the Requirement type gtk.ComboBox() value and new
        Requirement ID to create the code for the new Requirement.

        :param int requirement_id: the ID of the newly added Requirement.
        :return: _code
        :rtype: str
        """

        _model = self.cmbRqmtType.get_model()
        _row = self.cmbRqmtType.get_active_iter()

        try:
            _prefix = _model.get_value(_row, 1)
        except TypeError:
            _prefix = 'RQMT'

        _suffix = requirement_id

        _zeds = 4 - len(str(_suffix))
        _pad = '0' * _zeds
        _code = '{0:s}-{1:s}{2:d}'.format(_prefix, _pad, _suffix)

        return _code

    def _cancel(self, __assistant):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
        """

        self.destroy()
