# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Revision.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Revision Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .WorkView import RAMSTKWorkView

# from Assistants import AddRevision


class GeneralData(RAMSTKWorkView):
    """
    Display general Revision attribute data in the RAMSTK Work Book.

    The Revision Work View displays all the general data attributes for the
    selected Revision. The attributes of a Revision General Data Work View are:

    :ivar int _revision_id: the ID of the Revision currently being displayed.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCode `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     1    | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     2    | txtRemarks `changed`                      |
    +----------+-------------------------------------------+
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Revision Work View general data page.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :py:class:`rtk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='revision')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_gendata_labels = [
            _(u"Revision Code:"),
            _(u"Revision Name:"),
            _(u"Remarks:")
        ]

        # Initialize private scalar attributes.
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtCode = rtk.RAMSTKEntry(
            width=125, tooltip=_(u"A unique code for the selected revision."))
        self.txtName = rtk.RAMSTKEntry(
            width=800, tooltip=_(u"The name of the selected revision."))
        self.txtRemarks = rtk.RAMSTKTextView(
            gtk.TextBuffer(),
            width=800,
            tooltip=_(u"Enter any remarks associated with the "
                      u"selected revision."))

        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._on_focus_out, 2))

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_end(self._make_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedRevision')
        pub.subscribe(self._on_edit, 'mvwEditedRevision')
        pub.subscribe(self._do_clear_page, 'closedProgram')

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtName.handler_block(self._lst_handler_id[0])
        self.txtName.set_text('')
        self.txtName.handler_unblock(self._lst_handler_id[0])
        _buffer = self.txtRemarks.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[1])
        _buffer.set_text('')
        _buffer.handler_block(self._lst_handler_id[1])
        self.txtCode.handler_block(self._lst_handler_id[2])
        self.txtCode.set_text('')
        self.txtCode.handler_unblock(self._lst_handler_id[2])

        return None

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Revision General Data page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _revision = self._dtc_data_controller.request_do_select(
            self._revision_id)

        self.txtCode.handler_block(self._lst_handler_id[2])
        self.txtCode.set_text(str(_revision.revision_code))
        self.txtCode.handler_unblock(self._lst_handler_id[2])
        self.txtName.handler_block(self._lst_handler_id[0])
        self.txtName.set_text(_revision.name)
        self.txtName.handler_unblock(self._lst_handler_id[0])
        _buffer = self.txtRemarks.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[1])
        _buffer.set_text(_revision.remarks)
        _buffer.handler_unblock(self._lst_handler_id[1])

        return _return

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Revision.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update(
            self._revision_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to save all the Revisions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create the Revision Work View gtk.ButtonBox().

        :return: _buttonbox; the gtk.ButtonBox() for the Revision class Work
                 View.
        :rtype: :py:class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Saves the currently selected Revision to the open "
              u"RAMSTK Program database."),
            _(u"Save all Revisions to the open RAMSTK Program database.")
        ]
        _callbacks = [self._do_request_update, self._do_request_update_all]

        _icons = ['save', 'save-all']

        _buttonbox = RAMSTKWorkView._make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _make_page(self):
        """
        Create the Revision Work View general data page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RAMSTKScrolledWindow(_fixed)
        _frame = rtk.RAMSTKFrame(label=_(u"General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels, _fixed,
                                              5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])

        _fixed.show_all()

        _label = rtk.RAMSTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays general information for the selected "
                      u"revision."))
        self.hbx_tab_label.pack_start(_label)

        return _frame

    def _on_edit(self, index, new_text):
        """
        Update the Revision Work View gtk.Widgets().

        This method updates the Revision Work View gtk.Widgets() with changes
        to the Revision data model attributes.  This method is called whenever
        an attribute is edited in a different RAMSTK View.

        :param int index: the index in the Revision attributes list of the
                          attribute that was edited.
        :param str new_text: the new text to update the gtk.Widget() with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if index == 17:
            self.txtName.handler_block(self._lst_handler_id[0])
            self.txtName.set_text(new_text)
            self.txtName.handler_unblock(self._lst_handler_id[0])
        elif index == 20:
            _textbuffer = self.txtRemarks.do_get_buffer()
            _textbuffer.handler_block(self._lst_handler_id[1])
            _textbuffer.set_text(new_text)
            _textbuffer.handler_unblock(self._lst_handler_id[1])
        elif index == 22:
            self.txtCode.handler_block(self._lst_handler_id[2])
            self.txtCode.set_text(str(new_text))
            self.txtCode.handler_unblock(self._lst_handler_id[2])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve gtk.Entry() changes and assign the new data.

        This method takes the new data from the gtk.Entry() and assigns it to
        the appropriate Revision data model attribute.

        :param entry: the gtk.Entry() that called the method.
        :type entry: :class:`gtk.Entry`
        :param int index: the position in the Revision class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _index = -1
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _revision = self._dtc_data_controller.request_do_select(
                self._revision_id)

            if index == 0:
                _index = 17
                _text = entry.get_text()
                _revision.name = _text
            elif index == 1:
                _index = 20
                _text = self.txtRemarks.do_get_text()
                _revision.remarks = _text
            elif index == 2:
                _index = 22
                _text = entry.get_text()
                _revision.revision_code = _text

            pub.sendMessage(
                'wvwEditedRevision', position=_index, new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id):
        """
        Load the Revision Work View General Data page gtk.Widget()s.

        :param int revision_id: the ID of the newly selected Revision.
        :param str title: the title to display on the Work Book titlebar.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._revision_id = module_id
        _return = False

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers['revision']
        self._do_load_page()

        return _return


class AssessmentResults(RAMSTKWorkView):
    """
    Display assessment results Revision attribute data in the RAMSTK Work Book.

    The Revision Assessment Results view displays all the assessment results
    for the selected Revision.  The attributes of a Revision Assessment Results
    View are:

    :ivar int _revision_id: the ID of the Revision currently being displayed.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Revision Work View assessment results page.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :py:class:`rtk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Revision')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.pack_end(self._make_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedRevision')

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Revision Assessment Results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _revision = self._dtc_data_controller.request_do_select(
            self._revision_id)

        self.txtAvailability.set_text(
            str(self.fmt.format(_revision.availability_logistics)))
        self.txtMissionAt.set_text(
            str(self.fmt.format(_revision.availability_mission)))
        self.txtActiveHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_active)))
        self.txtDormantHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_dormant)))
        self.txtMissionHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_mission)))
        self.txtPredictedHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_logistics)))
        self.txtSoftwareHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_software)))
        self.txtMMT.set_text(str(self.fmt.format(_revision.mmt)))
        self.txtMCMT.set_text(str(self.fmt.format(_revision.mcmt)))
        self.txtMPMT.set_text(str(self.fmt.format(_revision.mpmt)))
        self.txtMissionMTBF.set_text(
            str(self.fmt.format(_revision.mtbf_mission)))
        self.txtMTBF.set_text(str(self.fmt.format(_revision.mtbf_logistics)))
        self.txtMTTR.set_text(str(self.fmt.format(_revision.mttr)))
        self.txtMissionRt.set_text(
            str(self.fmt.format(_revision.reliability_mission)))
        self.txtReliability.set_text(
            str(self.fmt.format(_revision.reliability_logistics)))

        _title = _(u"RAMSTK Work Book: Revision "
                   u"(Analyzing {0:s})").format(_revision.name)
        RAMSTKWorkView.on_select(
            self, title=_title, error_code=0, user_msg='', debug_msg='')

        return _return

    def _make_page(self):
        """
        Create the Revision Work View assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        (_hbx_page, __, __, __, __, __,
         __) = RAMSTKWorkView._make_assessment_results_page(self)

        return _hbx_page

    def _on_select(self, **kwargs):
        """
        Load the Revision Work View assessment results page gtk.Widget()s.

        :param int revision_id: the ID of the newly selected Revision.
        :param str title: the title to display on the Work Book titlebar.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._revision_id = kwargs['module_id']

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers['revision']
        self._do_load_page()

        return _return
