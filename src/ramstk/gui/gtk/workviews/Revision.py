# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Revision.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
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
        :type controller: :py:class:`ramstk.RAMSTK.RAMSTK`
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

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtCode = ramstk.RAMSTKEntry(
            width=125, tooltip=_(u"A unique code for the selected revision."))
        self.txtName = ramstk.RAMSTKEntry(
            width=800, tooltip=_(u"The name of the selected revision."))
        self.txtRemarks = ramstk.RAMSTKTextView(
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

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_revision')
        pub.subscribe(self._on_edit, 'mvw_editing_revision')

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

    def _do_load_page(self, attributes):
        """
        Load the Revision General Data page.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        RAMSTKWorkView.on_select(
            self,
            title=_(u"Analyzing Revision {0:s} - {1:s}").format(
                str(attributes['revision_code']), str(attributes['name'])))

        self.txtCode.handler_block(self._lst_handler_id[2])
        self.txtCode.set_text(str(attributes['revision_code']))
        self.txtCode.handler_unblock(self._lst_handler_id[2])

        self.txtName.handler_block(self._lst_handler_id[0])
        self.txtName.set_text(str(attributes['name']))
        self.txtName.handler_unblock(self._lst_handler_id[0])

        _buffer = self.txtRemarks.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[1])
        _buffer.set_text(str(attributes['remarks']))
        _buffer.handler_unblock(self._lst_handler_id[1])

        return None

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Revision.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_revision', node_id=self._revision_id)
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to save all the Revisions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_revisions')
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create the Revision Work View gtk.ButtonBox().

        :return: _buttonbox; the gtk.ButtonBox() for the Revision class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = []
        _callbacks = []
        _icons = []

        _buttonbox = ramstk.do_make_buttonbox(
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

        :return: _frame; the gtk.Frame() to embed in the notebook page.
        :rtype: :class:`gtk.Frame`
        """
        (_frame, __, __, __) = RAMSTKWorkView.make_general_data_page(self)

        return _frame

    def _on_edit(self, module_id, key, value):
        """
        Update the Revision Work View gtk.Widgets().

        This method updates the Revision Work View gtk.Widgets() with changes
        to the Revision data model attributes.  This method is called whenever
        an attribute is edited in a different RAMSTK View.

        :param int module_id: the ID of the Revision being edited.  This
                              parameter is required to allow the PyPubSub
                              signals to call this method and the
                              request_set_attributes() method in the
                              RAMSTKDataController.
        :param str key: the key in the Revision attributes list of the
                        attribute that was edited.
        :param str value: the new text to update the gtk.Widget() with.
        :return: None
        :rtype: None
        """
        if key == 'name':
            self.txtName.handler_block(self._lst_handler_id[17])
            self.txtName.set_text(str(value))
            self.txtName.handler_unblock(self._lst_handler_id[17])
        elif key == 'remarks':
            _textbuffer = self.txtRemarks.do_get_buffer()
            _textbuffer.handler_block(self._lst_handler_id[20])
            _textbuffer.set_text(str(value))
            _textbuffer.handler_unblock(self._lst_handler_id[20])
        elif key == 'revision_code':
            self.txtCode.handler_block(self._lst_handler_id[22])
            self.txtCode.set_text(str(value))
            self.txtCode.handler_unblock(self._lst_handler_id[22])

        return None

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
        :return: None
        :rtype: None
        """
        _key = ''
        _new_text = ''

        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            _key = 'name'
            _new_text = str(entry.get_text())
        elif index == 1:
            _key = 'remarks'
            _new_text = self.txtRemarks.do_get_text()
        elif index == 2:
            _key = 'code'
            _new_text = str(entry.get_text())

        pub.sendMessage(
            'wvw_editing_revision',
            module_id=self._revision_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None
