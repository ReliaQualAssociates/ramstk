# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.FMEA.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""FMEA Work View."""

from datetime import datetime
from sortedcontainers import SortedDict
from pubsub import pub

# Import other RTK modules.
from rtk.Configuration import RTK_CONTROL_TYPES, RTK_FAILURE_PROBABILITY
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from rtk.gui.gtk.assistants import AddControlAction
from .WorkView import RTKWorkView


class FMEA(RTKWorkView):
    """
    Display FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (FMEA). The attributes of a FMEA Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Functional FMEA attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   | tvw_fmea `cursor_changed`                 |
    +----------+-------------------------------------------+
    |      1   | tvw_fmea `button_press_event`             |
    +----------+-------------------------------------------+
    |      2   | tvw_fmea `edited`                         |
    +----------+-------------------------------------------+
    """

    _lst_control_type = [_(u"Prevention"), _(u"Detection")]

    def __init__(self, controller, **kwargs):
        """
        Initialize the Work View for the FMEA.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        _module = kwargs['module']
        RTKWorkView.__init__(self, controller, module=_module)

        # Initialize private dictionary attributes.
        self._dic_icons['mode'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/mode.png'
        self._dic_icons['mechanism'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/mechanism.png'
        self._dic_icons['cause'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/cause.png'
        self._dic_icons['control'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/control.png'
        self._dic_icons['action'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/action.png'

        self._dic_missions = {}
        self._dic_mission_phases = {'': []}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._functional = bool(_module == 'FFMEA')
        self._item_hazard_rate = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkCriticality = rtk.RTKCheckButton(
            label=_(u"Calculate Criticality"),
            tooltip=_(
                u"Select this option to calculate the (D)FME(C)A MIL-STD-1629, "
                u"Task 102 criticality analysis."))
        self.chkRPN = rtk.RTKCheckButton(
            label=_(u"Calculate RPNs"),
            tooltip=_(
                u"Select this option to calculate the (D)FME(C)A risk priority "
                u"numbers (RPN)."))
        self.txtItemCriticality = rtk.RTKTextView(
            gtk.TextBuffer(),
            height=75,
            tooltip=_(
                u"Displays the MIL-SD-1629, Taks 102 item criticality for the "
                u"selected hardware item."))
        self.txtItemCriticality.set_editable(False)
        _bg_color = gtk.gdk.Color('#ADD8E6')
        self.txtItemCriticality.modify_base(gtk.STATE_NORMAL, _bg_color)
        self.txtItemCriticality.modify_base(gtk.STATE_ACTIVE, _bg_color)
        self.txtItemCriticality.modify_base(gtk.STATE_PRELIGHT, _bg_color)
        self.txtItemCriticality.modify_base(gtk.STATE_SELECTED, _bg_color)
        self.txtItemCriticality.modify_base(gtk.STATE_INSENSITIVE, _bg_color)

    def _get_cell_model(self, column):
        """
        Retrieve the gtk.CellRendererCombo() gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cell_renderers()[0]
        _model = _cell.get_property('model')
        _model.clear()

        return _model

    def _do_refresh_view(self, row):
        """
        Refresh the (D)FME(C)A Work View after a successful calculation.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = self.treeview.get_model()

        if row is not None:
            if self._functional:
                _node_id = _model.get_value(row, 18)
            else:
                _node_id = _model.get_value(row, 43)
            _level = self._get_level(_node_id)
            _node = self._dtc_data_controller.request_do_select(_node_id)

            if _level == 'mode':
                _model.set_value(row, self._lst_col_order[17],
                                 _node.mode_hazard_rate)
                _model.set_value(row, self._lst_col_order[19],
                                 _node.mode_criticality)
            elif _level == 'mechanism' or _level == 'cause':
                _model.set_value(row, self._lst_col_order[24], _node.rpn)
                _model.set_value(row, self._lst_col_order[37], _node.rpn_new)

            if _model.iter_has_child(row) and _level != 'cause':
                _row = _model.iter_children(row)
            else:
                _row = _model.iter_next(row)

            self._do_refresh_view(_row)

        # For hardware FMECA needs to display the item criticality.
        if not self._functional:
            _str_item_crit = ""
            _dic_item_crit = self._dtc_data_controller.request_item_criticality(
            )
            for _key in _dic_item_crit:
                _str_item_crit = (_str_item_crit + _(u"{0:s}: {1:g}\n").format(
                    _key, _dic_item_crit[_key]))

            self.txtItemCriticality.do_get_buffer().set_text(
                str(_str_item_crit))

        return _return

    def _do_request_calculate(self, __button):
        """
        Calculate the FFMEA RPN or criticality.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _criticality = self.chkCriticality.get_active()
        _rpn = self.chkRPN.get_active()
        if not self._dtc_data_controller.request_do_calculate(
                self._item_hazard_rate, criticality=_criticality, rpn=_rpn):
            _model = self.treeview.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                self._do_refresh_view(_row)
                _row = _model.iter_next(_row)
        else:
            _return = True

        return _return

    def _do_request_delete(self, __button):
        """
        Request to delete the selected entity from the FMEA.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        if self._functional:
            _node_id = _model.get_value(_row, 18)
        else:
            _node_id = _model.get_value(_row, 43)

        # Delete the selected entity from the RTK Program database and then
        # refresh the TreeView.
        if not self._dtc_data_controller.request_do_delete(_node_id):
            if self._functional:
                self._on_select(module_id=self._function_id)
            else:
                self._on_select(module_id=self._hardware_id)
        else:
            _return = True

        return _return

    def do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the FMEA.

        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _entity_id = kwargs['entity_id']
        _parent_id = kwargs['parent_id']
        _level = kwargs['level']
        _choose = kwargs['choose']
        _undefined = kwargs['undefined']

        if _undefined:
            _prompt = _(u"A FMEA control or an action cannot have a "
                        u"child entity.")
            _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')

            if _dialog.do_run() == gtk.RESPONSE_OK:
                _dialog.do_destroy()

            _return = True

        if _choose:
            _dialog = AddControlAction()
            _response = _dialog.do_run()

            if _dialog.do_run() == gtk.RESPONSE_OK:
                _control = _dialog.rdoControl.get_active()
                _action = _dialog.rdoAction.get_active()

                if _control:
                    _level = 'control'
                elif _action:
                    _level = 'action'

            else:
                _return = True

            _dialog.do_destroy()

        # Insert the new entity into the RTK Program database and then refresh
        # the TreeView.
        if (_undefined or _return
                or self._dtc_data_controller.request_do_insert(
                    entity_id=_entity_id, parent_id=_parent_id, level=_level)):
            _return = True

        return _return

    def _do_request_insert_child(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Request to insert a new entity to the FMEA at the next level.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=False)

    def _do_request_insert_sibling(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Request to insert a new entity to the FMEA at the same level.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=True)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected entity in the FMEA.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model, _row = self.treeview.get_selection().get_selected()
        if self._functional:
            _node_id = _model.get_value(_row, 18)
        else:
            _node_id = _model.get_value(_row, 43)

        return self._dtc_data_controller.request_do_update(_node_id)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the FMEA.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update_all()

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the FMEA class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the FMEA Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new FMEA entity at the same level as the "
              u"currently selected entity."),
            _(u"Add a new FMEA entity one level below the currently "
              u"selected entity."),
            _(u"Remove the selected entity from the FMEA."),
            _(u"Calculate the FMEA."),
            _(u"Save the FMEA to the open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_delete, self._do_request_calculate,
            self._do_request_update_all
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'remove', 'calculate', 'save'
        ]

        _buttonbox = RTKWorkView._make_buttonbox(
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
        Make the FMEA RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = rtk.RTKFrame(
            label=_(u"Failure Mode and Effects Analysis (FMEA)"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return _frame

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the FMEA Work View RTKTreeView().

        :param treeview: the FMEA TreeView RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`.
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`gtk.gdk.Event`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _menu = gtk.Menu()
            _menu.popup(None, None, None, event.button, event.time)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_sibling'])
            _menu_item.set_label(_(u"Add Sibling"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert_sibling)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_child'])
            _menu_item.set_label(_(u"Add Child"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert_child)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['calculate'])
            _menu_item.set_label(_(u"Calculate FMEA"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_calculate)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return _return


class FFMEA(FMEA):
    """
    Display Functional FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Functional Failure Mode
    and Effects Analysis (FFMEA). The attributes of a FFMEA Work View are:
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Functional FMEA.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        FMEA.__init__(self, controller, module='FFMEA')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _fmt_file = (controller.RTK_CONFIGURATION.RTK_CONF_DIR + '/layouts/' +
                     controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['ffmea'])
        _fmt_path = "/root/tree[@name='FFMEA']/column"
        _tooltip = _(u"Displays the Functional Failure Mode and Effects "
                     u"Analysis (FFMEA) for the currently selected "
                     u"Function.")

        self.treeview = rtk.RTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            '#FFFFFF',
            '#000000',
            pixbuf=True,
            indexed=True)
        self._lst_col_order = self.treeview.order
        self.treeview.set_tooltip_text(_tooltip)

        _label = rtk.RTKLabel(
            _(u"FMEA"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays the Functional Failure Mode and Effects "
                      u"Analysis (FFMEA) for the selected function."))
        self.hbx_tab_label.pack_start(_label)

        self.pack_start(self._make_buttonbox(), False, True)
        self.pack_end(self._make_page(), True, True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedFunction')

    def _do_change_row(self, treeview):
        """
        Handle events for the Functional FMEA Work View RTKTreeView().

        This method is called whenever a RTKTreeView() row is activated.

        :param treeview: the FMEA RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.RTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 18)
        except TypeError:
            _node_id = 0

        _level = self._get_level(_node_id)
        if _level == 'mode':
            _headings = [
                _(u"Mode ID"), self.treeview.headings[self._lst_col_order[1]],
                self.treeview.headings[self._lst_col_order[2]],
                self.treeview.headings[self._lst_col_order[3]],
                self.treeview.headings[self._lst_col_order[4]],
                self.treeview.headings[self._lst_col_order[5]],
                self.treeview.headings[self._lst_col_order[6]],
                self.treeview.headings[self._lst_col_order[7]], '', '', '', '',
                '', '', '', '', self.treeview.headings[self._lst_col_order[16]]
            ]
        elif _level == 'cause':
            _headings = [
                _(u"Cause ID"),
                _(u"Failure\nCause"), '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', ''
            ]
        elif _level == 'control':
            _headings = [
                _(u"Control ID"),
                _(u"Existing\nControl"), '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', ''
            ]
        elif _level == 'action':
            _headings = [
                _(u"Action ID"),
                _(u"Recommended\nAction"), '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[8]],
                self.treeview.headings[self._lst_col_order[9]],
                self.treeview.headings[self._lst_col_order[10]],
                self.treeview.headings[self._lst_col_order[11]],
                self.treeview.headings[self._lst_col_order[12]],
                self.treeview.headings[self._lst_col_order[13]],
                self.treeview.headings[self._lst_col_order[14]],
                self.treeview.headings[self._lst_col_order[15]], ''
            ]
        else:
            _headings = []

        _columns = self.treeview.get_columns()

        i = 0
        for _heading in _headings:
            _label = rtk.RTKLabel(
                _heading, justify=gtk.JUSTIFY_CENTER, wrap=True)
            _label.show_all()
            _columns[i].set_widget(_label)
            if _heading == '':
                _columns[i].set_visible(False)
            else:
                _columns[i].set_visible(True)

            i += 1

        treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the FMEA Work View RTKTreeview().

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :class:`gtk.CellRenderer`.
        :param str path: the path that was edited.
        :param str __new_text: the edited text.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):

            _entity = self._dtc_data_controller.request_do_select(
                model[path][18])

            if _entity.is_mode:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.effect_local = model[path][self._lst_col_order[2]]
                _entity.effect_next = model[path][self._lst_col_order[3]]
                _entity.effect_end = model[path][self._lst_col_order[4]]
                _entity.design_provisions = model[path][self._lst_col_order[5]]
                _entity.operator_actions = model[path][self._lst_col_order[6]]
                _entity.severity_class = model[path][self._lst_col_order[7]]
                _entity.remarks = model[path][self._lst_col_order[16]]
            elif _entity.is_control:
                _entity.description = model[path][self._lst_col_order[1]]
            elif _entity.is_action:
                _entity.action_recommended = model[path][self._lst_col_order[
                    1]]
                _entity.action_owner = model[path][self._lst_col_order[8]]
                _entity.action_due_date = datetime.strptime(
                    model[path][self._lst_col_order[9]], '%Y-%m-%d')
                _entity.action_status = model[path][self._lst_col_order[10]]
                _entity.action_taken = model[path][self._lst_col_order[11]]
                _entity.action_approved = model[path][self._lst_col_order[12]]
                _entity.action_approve_date = datetime.strptime(
                    model[path][self._lst_col_order[13]], '%Y-%m-%d')
                _entity.action_closed = model[path][self._lst_col_order[14]]
                _entity.action_close_date = datetime.strptime(
                    model[path][self._lst_col_order[15]], '%Y-%m-%d')

        return _return

    def _do_load_page(self, **kwargs):
        """
        Iterate through the tree and load the Functional FMEA RTKTreeView().

        :return: (_error_code, _user_msg, _debug_msg); the error code, message
                 to be displayed to the user, and the message to be written to
                 the debug log.
        :rtype: (int, str, str)
        """
        _tree = kwargs['tree']
        _row = kwargs['row']
        _error_code = 0
        _debug_msg = ''
        _user_msg = ''

        _data = []
        _model = self.treeview.get_model()
        _model.clear()

        _node = _tree.nodes[SortedDict(_tree.nodes).keys()[0]]
        _entity = _node.data
        try:
            if _entity.is_mode:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mode'], 22, 22)
                _data = [
                    _entity.mode_id, _entity.description, _entity.effect_local,
                    _entity.effect_next, _entity.effect_end,
                    _entity.design_provisions, _entity.operator_actions,
                    _entity.severity_class, '', '', '', '', 0, '', 0, '',
                    _entity.remarks, _icon, _node.identifier
                ]
                _row = None
            elif _entity.is_cause and _row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['cause'], 22, 22)
                _data = [
                    _entity.cause_id, _entity.description, '', '', '', '', '',
                    '', '', '', '', '', 0, '', 0, '', '', _icon,
                    _node.identifier
                ]
            elif _entity.is_control and _row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['control'], 22, 22)
                _data = [
                    _entity.control_id, _entity.description, '', '', '', '',
                    '', '', '', '', '', '', 0, '', 0, '', '', _icon,
                    _node.identifier
                ]
            elif _entity.is_action and _row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['action'], 22, 22)
                _data = [
                    _entity.action_id, _entity.action_recommended, '', '', '',
                    '', '', '', _entity.action_owner, _entity.action_due_date,
                    _entity.action_status, _entity.action_taken,
                    _entity.action_approved, _entity.action_approve_date,
                    _entity.action_closed, _entity.action_close_date, '',
                    _icon, _node.identifier
                ]

            try:
                _new_row = _model.append(_row, _data)
            except TypeError:
                _error_code = 1
                _user_msg = _(u"One or more Functional FMEA line items had "
                              u"the wrong data type in it's data package and "
                              u"is not displayed in the FMEA form.")
                _debug_msg = ("RTK ERROR: Data for FMEA ID {0:s} for Function "
                              "ID {1:s} is the wrong type for one or more "
                              "columns.".format(
                                  str(_node.identifier),
                                  str(self._function_id)))
                _new_row = None
            except ValueError:
                _error_code = 1
                _user_msg = _(
                    u"One or more Functional FMEA line items was missing some "
                    u"of it's data and is not displayed in the FMEA form.")
                _debug_msg = (
                    "RTK ERROR: Too few fields for FMEA ID {0:s} for Function "
                    "ID {1:s}.".format(
                        str(_node.identifier), str(self._function_id)))
                _new_row = None

        except AttributeError:
            if _node.identifier != 0:
                _error_code = 1
                _user_msg = _(u"One or more Functional FMEA line items was "
                              u"missing it's data package and is not "
                              u"displayed in the FMEA form.")
                _debug_msg = (
                    "RTK ERROR: There is no data package for FMEA ID {0:s} "
                    "for Function ID {1:s}.".format(
                        str(_node.identifier), str(self._function_id)))

            _new_row = None

        for _n in _tree.children(_node.identifier):
            _child_tree = _tree.subtree(_n.identifier)
            self._do_load_page(tree=_child_tree, row=_new_row)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

        return (_error_code, _user_msg, _debug_msg)

    def _do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the Functional FMEA.

        :param bool sibling: indicator variable that determines whether a
                             sibling entity be added (default) or a child
                             entity be added to the currently selected entity.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _sibling = kwargs['sibling']
        _return = False
        _choose = False
        _undefined = False

        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 18)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _node_id = 0
            _prow = None

        # The _entity_id is the RTK Program database Function ID, or Mode ID,
        # to add the new entity to.  The _parent_id is the Node ID of the
        # parent node in the treelib Tree().
        _level = self._get_level(_node_id)
        if _sibling:
            if _level == 'mode':
                _entity_id = self._function_id
                _parent_id = 0
            else:
                _entity_id = _model.get_value(_prow, 0)
                _parent_id = _model.get_value(_prow, 18)
            if _level == 'control' or _level == 'action':
                _choose = True
        elif not _sibling:
            if _level == 'mode':
                _level = 'cause'
            elif _level == 'cause':
                _choose = True
            elif _level == 'control' or _level == 'action':
                _undefined = True
            _entity_id = _model.get_value(_row, 0)
            _parent_id = _node_id

        # Insert the new entity into the RTK Program database and then refresh
        # the TreeView.
        if not FMEA.do_request_insert(
                self,
                entity_id=_entity_id,
                parent_id=_parent_id,
                level=_level,
                choose=_choose,
                undefined=_undefined):
            self._on_select(module_id=self._function_id)
        else:
            _return = True

        return _return

    @staticmethod
    def _get_level(node_id):
        """
        Return the level in the Functional FMEA based on the Node ID.

        :param str node_id: the Node ID of the selected Node in the Functional
                            FMEA Tree().
        :return: _level
        :rtype: str
        """
        _level = None

        if node_id.count('.') == 1:
            _level = 'mode'
        elif node_id.count('.') == 2:
            _level = 'cause'
        elif node_id.count('.') == 3 and node_id[-1] == 'c':
            _level = 'control'
        elif node_id.count('.') == 3 and node_id[-1] == 'a':
            _level = 'action'

        return _level

    def _make_page(self):
        """
        Make the (D)FME(C)A RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        # Load the severity classes into the gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[7])
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_SEVERITY:
            _severity = self._mdcRTK.RTK_CONFIGURATION.RTK_SEVERITY[_item][1]
            _model.append((_severity, ))

        # Load the users into the gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[8])
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_USERS:
            _user = self._mdcRTK.RTK_CONFIGURATION.RTK_USERS[_item][0] + ', ' \
                    + self._mdcRTK.RTK_CONFIGURATION.RTK_USERS[_item][1]
            _model.append((_user, ))

        # Load the status values into the gtk.CellRendererCombo()
        _model = self._get_cell_model(self._lst_col_order[10])
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_ACTION_STATUS:
            _status = \
                self._mdcRTK.RTK_CONFIGURATION.RTK_ACTION_STATUS[_item][0]
            _model.append((_status, ))

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        for i in self._lst_col_order:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()

            if isinstance(_cell[0], gtk.CellRendererPixbuf):
                pass
            elif isinstance(_cell[0], gtk.CellRendererToggle):
                _cell[0].connect('toggled', self._do_edit_cell, None, i,
                                 self.treeview.get_model())
            elif isinstance(_cell[0], gtk.CellRendererCombo):
                _cell[0].connect('edited', self._do_edit_cell, i,
                                 self.treeview.get_model())
            else:
                _cell[0].connect('edited', self._do_edit_cell, i,
                                 self.treeview.get_model())

        return FMEA._make_page(self)

    def _on_select(self, module_id, **kwargs):  # pylint: disable=unused-argument
        """
        Respond to selectedFunction signal from pypubsub.

        :return: None
        :rtype: None
        """
        self._function_id = module_id

        _model = self.treeview.get_model()
        _model.clear()

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRTK.dic_controllers['ffmea']

        _fmea = self._dtc_data_controller.request_do_select_all(
            parent_id=self._function_id, functional=True)
        (_error_code, _user_msg, _debug_msg) = self._do_load_page(
            tree=_fmea, row=None)

        RTKWorkView.on_select(
            self,
            title=_(u"Analyzing Failure Modes for Function ID {0:d}").format(
                self._function_id),
            error_code=_error_code,
            user_msg=_user_msg,
            debug_msg=_debug_msg)

        return None


class DFMECA(FMEA):
    """
    Display Hardware (D)FME(C)A attribute data in the Work Book.

    The WorkView displays all the attributes for the Hardware (Design) Failure
    Mode and Effects (and Criticality) Analysis [(D)FME(C)A]. The attributes of
    a (D)FME(C)A Work View are:
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Hardware (D)FME(C)A.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        FMEA.__init__(self, controller, module='DFMECA')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._n_columns = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _fmt_file = (controller.RTK_CONFIGURATION.RTK_CONF_DIR + '/layouts/' +
                     controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['dfmeca'])
        _fmt_path = "/root/tree[@name='DFMECA']/column"
        _tooltip = _(u"Displays the (Design) Failure Mode and Effects "
                     u"(and Criticality) Analysis [(D)FME(C)A] for the "
                     u"currently selected Hardware item.")

        self.treeview = rtk.RTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            '#FFFFFF',
            '#000000',
            pixbuf=True,
            indexed=True)
        self._lst_col_order = self.treeview.order
        self.treeview.set_tooltip_text(_tooltip)

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        _label = rtk.RTKLabel(
            _(u"FMEA"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays the Design Failure Mode, Effects, (and "
                      u"Criticality) Analysis [(D)FME(C)A] for the selected "
                      u"Hardware item."))
        self.hbx_tab_label.pack_start(_label)

        self.pack_start(self._make_buttonbox(), False, True)
        self.pack_end(self._make_methodbox(), True, True)
        self.show_all()

        pub.subscribe(self._do_load_missions, 'selectedRevision')
        pub.subscribe(self._on_select, 'selectedHardware')
        pub.subscribe(self._do_load_missions, 'editedUsage')

    def _do_change_row(self, treeview):
        """
        Handle 'cursor-changed' event for the (D)FME(C)A RTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the FMEA RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeViewRTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            _mission = _model.get_value(_row, 2)
            _node_id = _model.get_value(_row, 43)
        except TypeError:
            _mission = ''
            _node_id = 0

        _level = self._get_level(_node_id)

        if _level == 'mode':
            _headings = [
                self.treeview.headings[self._lst_col_order[0]],
                self.treeview.headings[self._lst_col_order[1]],
                self.treeview.headings[self._lst_col_order[2]],
                self.treeview.headings[self._lst_col_order[3]],
                self.treeview.headings[self._lst_col_order[4]],
                self.treeview.headings[self._lst_col_order[5]],
                self.treeview.headings[self._lst_col_order[6]],
                self.treeview.headings[self._lst_col_order[7]],
                self.treeview.headings[self._lst_col_order[8]],
                self.treeview.headings[self._lst_col_order[9]],
                self.treeview.headings[self._lst_col_order[10]],
                self.treeview.headings[self._lst_col_order[11]],
                self.treeview.headings[self._lst_col_order[12]],
                self.treeview.headings[self._lst_col_order[13]],
                self.treeview.headings[self._lst_col_order[14]],
                self.treeview.headings[self._lst_col_order[15]],
                self.treeview.headings[self._lst_col_order[16]],
                self.treeview.headings[self._lst_col_order[17]],
                self.treeview.headings[self._lst_col_order[18]],
                self.treeview.headings[self._lst_col_order[19]], '',
                self.treeview.headings[self._lst_col_order[21]], '', '', '',
                '', '', '', '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[34]], '', '', '',
                self.treeview.headings[self._lst_col_order[38]],
                self.treeview.headings[self._lst_col_order[39]], '',
                self.treeview.headings[self._lst_col_order[41]]
            ]
            self._do_load_mission_phases(_mission)
        elif _level == 'mechanism':
            _headings = [
                _(u"Mechanism ID"),
                _(u"Failure\nMechanism"), '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[22]],
                self.treeview.headings[self._lst_col_order[23]],
                self.treeview.headings[self._lst_col_order[24]], '', '', '',
                '', '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[35]],
                self.treeview.headings[self._lst_col_order[36]],
                self.treeview.headings[self._lst_col_order[37]], '', '',
                self.treeview.headings[self._lst_col_order[40]], ''
            ]
        elif _level == 'cause':
            _headings = [
                _(u"Cause ID"),
                _(u"Failure\nCause"), '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[22]],
                self.treeview.headings[self._lst_col_order[23]],
                self.treeview.headings[self._lst_col_order[24]], '', '', '',
                '', '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[35]],
                self.treeview.headings[self._lst_col_order[36]],
                self.treeview.headings[self._lst_col_order[37]], '', '', '', ''
            ]
        elif _level == 'control':
            _headings = [
                _(u"Control ID"),
                _(u"Existing\nControl"), '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[20]], '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', ''
            ]
        elif _level == 'action':
            _headings = [
                _(u"Action ID"),
                _(u"Recommended\nAction"), '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                self.treeview.headings[self._lst_col_order[25]],
                self.treeview.headings[self._lst_col_order[26]],
                self.treeview.headings[self._lst_col_order[27]],
                self.treeview.headings[self._lst_col_order[28]],
                self.treeview.headings[self._lst_col_order[29]],
                self.treeview.headings[self._lst_col_order[30]],
                self.treeview.headings[self._lst_col_order[31]],
                self.treeview.headings[self._lst_col_order[32]],
                self.treeview.headings[self._lst_col_order[33]], '', '', '',
                '', '', '', '', ''
            ]
        else:
            _headings = []

        _columns = self.treeview.get_columns()

        i = 0
        for _heading in _headings:
            _label = rtk.RTKLabel(
                _heading, height=-1, justify=gtk.JUSTIFY_CENTER, wrap=True)
            _label.show_all()
            _columns[i].set_widget(_label)
            if _heading == '':
                _columns[i].set_visible(False)
            else:
                _columns[i].set_visible(True)

            i += 1

        treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the (D)FME(C)A RTKTreeview().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the RTKTreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):

            _entity = self._dtc_data_controller.request_do_select(
                model[path][43])

            if _entity.is_mode:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.mission = model[path][self._lst_col_order[2]]
                _entity.mission_phase = model[path][self._lst_col_order[3]]
                _entity.effect_local = model[path][self._lst_col_order[4]]
                _entity.effect_next = model[path][self._lst_col_order[5]]
                _entity.effect_end = model[path][self._lst_col_order[6]]
                _entity.detection_method = model[path][self._lst_col_order[7]]
                _entity.other_indications = model[path][self._lst_col_order[8]]
                _entity.isolation_method = model[path][self._lst_col_order[9]]
                _entity.design_provisions = model[path][self._lst_col_order[
                    10]]
                _entity.operator_actions = model[path][self._lst_col_order[11]]
                _entity.severity_class = model[path][self._lst_col_order[12]]
                _entity.hazard_rate_source = model[path][self._lst_col_order[
                    13]]
                _entity.mode_probability = model[path][self._lst_col_order[14]]
                _entity.effect_probability = model[path][self._lst_col_order[
                    15]]
                _entity.mode_ratio = model[path][self._lst_col_order[16]]
                _entity.mode_hazard_rate = model[path][self._lst_col_order[17]]
                _entity.mode_op_time = model[path][self._lst_col_order[18]]
                _entity.mode_criticality = model[path][self._lst_col_order[19]]
                _entity.rpn_severity = self._get_rpn_severity(
                    model[path][self._lst_col_order[21]])
                _entity.rpn_severity_new = self._get_rpn_severity(
                    model[path][self._lst_col_order[34]])
                _entity.critical_item = model[path][self._lst_col_order[38]]
                _entity.single_point = model[path][self._lst_col_order[39]]
                _entity.remarks = model[path][self._lst_col_order[41]]
                if position == self._lst_col_order[2]:
                    self._do_load_mission_phases(_entity.mission)
            elif _entity.is_mechanism:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.rpn = model[path][self._lst_col_order[24]]
                _entity.rpn_new = model[path][self._lst_col_order[37]]
                _entity.rpn_occurrence = self._get_rpn_occurrence(
                    model[path][self._lst_col_order[22]])
                _entity.rpn_detection = self._get_rpn_detection(
                    model[path][self._lst_col_order[23]])
                _entity.rpn_occurrence_new = self._get_rpn_occurrence(
                    model[path][self._lst_col_order[35]])
                _entity.rpn_detection_new = self._get_rpn_detection(
                    model[path][self._lst_col_order[36]])
                _entity.pof_include = model[path][self._lst_col_order[40]]
            elif _entity.is_cause:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.rpn_occurrence = self._get_rpn_occurrence(
                    model[path][self._lst_col_order[22]])
                _entity.rpn_detection = self._get_rpn_detection(
                    model[path][self._lst_col_order[23]])
                _entity.rpn = model[path][self._lst_col_order[24]]
                _entity.rpn_occurrence_new = self._get_rpn_occurrence(
                    model[path][self._lst_col_order[35]])
                _entity.rpn_detection_new = self._get_rpn_detection(
                    model[path][self._lst_col_order[36]])
                _entity.rpn_new = model[path][self._lst_col_order[37]]
            elif _entity.is_control:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.type_id = model[path][self._lst_col_order[20]]
            elif _entity.is_action:
                _entity.action_recommended = model[path][self._lst_col_order[
                    1]]
                _entity.action_category = model[path][self._lst_col_order[25]]
                _entity.action_owner = model[path][self._lst_col_order[26]]
                _entity.action_due_date = datetime.strptime(
                    model[path][self._lst_col_order[27]], '%Y-%m-%d')
                _entity.action_status = model[path][self._lst_col_order[28]]
                _entity.action_taken = model[path][self._lst_col_order[29]]
                _entity.action_approved = model[path][self._lst_col_order[30]]
                _entity.action_approve_date = datetime.strptime(
                    model[path][self._lst_col_order[31]], '%Y-%m-%d')
                _entity.action_closed = model[path][self._lst_col_order[32]]
                _entity.action_close_date = datetime.strptime(
                    model[path][self._lst_col_order[33]], '%Y-%m-%d')

        return _return

    def _do_load_mission_phases(self, mission):
        """
        Load the mission phase gtk.CellRendererCombo().

        :param str mission: the mission that was selected.
        :return False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = self._get_cell_model(self._lst_col_order[3])
        _model.clear()
        _model.append(('', ))

        try:
            for _phase in self._dic_mission_phases[mission]:
                _model.append((_phase, ))
        except KeyError:
            pass

        return _return

    def _do_load_missions(self, module_id):
        """
        Respond to `selectedRevision` signal from pypubsub.

        :param int module_id: the ID of the Revision that was selected.
        :return: False if successful or True if and error is encountered.
        :rtype: bool
        """
        _return = False

        _tree = self._mdcRTK.dic_controllers['profile'].request_do_select_all(
            revision_id=module_id)

        _missions = _tree.children(0)
        for _mission in _missions:
            self._dic_missions[
                _mission.data.description] = _mission.data.mission_time
            _phases = []
            for _phase in _tree.children(_mission.identifier):
                _phases.append(_phase.data.description)
            self._dic_mission_phases[_mission.data.description] = _phases

        _model = self._get_cell_model(self._lst_col_order[2])
        _model.clear()
        _model.append(('', ))

        try:
            for _mission in self._dic_missions:
                _model.append((_mission, ))
        except KeyError:
            pass

        return _return

    def _do_load_page(self, **kwargs):
        """
        Iterate through the tree and load the Hardware FMEA RTKTreeView().

        :return: (_error_code, _user_msg, _debug_msg); the error code, message
                 to be displayed to the user, and the message to be written to
                 the debug log.
        :rtype: (int, str, str)
        """
        _tree = kwargs['tree']
        _row = kwargs['row']
        _error_code = 0
        _user_msg = ""
        _debug_msg = ""

        _data = []
        _model = self.treeview.get_model()
        _model.clear()

        _tree = self._dtc_data_controller.request_do_select_all(
            parent_id=self._hardware_id, functional=False)

        _node = _tree.nodes[SortedDict(_tree.nodes).keys()[0]]
        _entity = _node.data
        if _entity is not None:
            try:
                _severity = self._get_rpn_severity(
                    _entity.rpn_severity, score=False)
                _severity_new = self._get_rpn_severity(
                    _entity.rpn_severity_new, score=False)
            except AttributeError:
                _severity = ''
                _severity_new = ''

            try:
                _occurrence = self._get_rpn_occurrence(
                    _entity.rpn_occurrence, score=False)
                _occurrence_new = self._get_rpn_occurrence(
                    _entity.rpn_occurrence_new, score=False)
            except AttributeError:
                _occurrence = ''
                _occurrence_new = ''

            try:
                _detection = self._get_rpn_detection(
                    _entity.rpn_detection, score=False)
                _detection_new = self._get_rpn_detection(
                    _entity.rpn_detection_new, score=False)
            except AttributeError:
                _detection = ''
                _detection_new = ''

        try:
            if _entity.is_mode:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mode'], 22, 22)
                try:
                    self._dic_missions[_entity.mission]
                except KeyError:
                    _entity.mission = ''

                _data = [
                    _entity.mode_id, _entity.description, _entity.mission,
                    _entity.mission_phase, _entity.effect_local,
                    _entity.effect_next, _entity.effect_end,
                    _entity.detection_method, _entity.other_indications,
                    _entity.isolation_method, _entity.design_provisions,
                    _entity.operator_actions, _entity.severity_class,
                    _entity.hazard_rate_source, _entity.mode_probability,
                    _entity.effect_probability, _entity.mode_ratio,
                    _entity.mode_hazard_rate, _entity.mode_op_time,
                    _entity.mode_criticality, '', _severity, _occurrence,
                    _detection, 0, '', '', '', '', '', 0, '', 0, '',
                    _severity_new, _occurrence_new, _detection_new, 0,
                    _entity.critical_item, _entity.single_point, 0,
                    _entity.remarks, _icon, _node.identifier
                ]
                _row = None
            elif _entity.is_mechanism:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mechanism'], 22, 22)
                _data = [
                    _entity.mechanism_id, _entity.description, '', '', '', '',
                    '', '', '', '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0,
                    0.0, '', _severity, _occurrence, _detection, _entity.rpn,
                    '', '', '', '', '', 0, '', 0, '', _severity_new,
                    _occurrence_new, _detection_new, _entity.rpn_new, 0, 0,
                    _entity.pof_include, '', _icon, _node.identifier
                ]
            elif _entity.is_cause:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['cause'], 22, 22)
                _data = [
                    _entity.cause_id, _entity.description, '', '', '', '', '',
                    '', '', '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0,
                    '', _severity, _occurrence, _detection, _entity.rpn, '',
                    '', '', '', '', 0, '', 0, '', _severity_new,
                    _occurrence_new, _detection_new, _entity.rpn_new, 0, 0, 0,
                    '', _icon, _node.identifier
                ]
            elif _entity.is_control and _row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['control'], 22, 22)
                _data = [
                    _entity.control_id, _entity.description, '', '', '', '',
                    '', '', '', '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0,
                    0.0, _entity.type_id, _severity, _occurrence, _detection,
                    0, '', '', '', '', '', 0, '', 0, '', _severity_new,
                    _occurrence_new, _detection_new, 0, 0, 0, 0, '', _icon,
                    _node.identifier
                ]
            elif _entity.is_action and _row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['action'], 22, 22)
                _data = [
                    _entity.action_id, _entity.action_recommended, '', '', '',
                    '', '', '', '', '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0,
                    0.0, '', _severity, _occurrence, _detection, 0,
                    _entity.action_category, _entity.action_owner,
                    _entity.action_due_date, _entity.action_status,
                    _entity.action_taken, _entity.action_approved,
                    _entity.action_approve_date, _entity.action_closed,
                    _entity.action_close_date, _severity_new, _occurrence_new,
                    _detection_new, 0, 0, 0, 0, '', _icon, _node.identifier
                ]

            try:
                _new_row = _model.append(_row, _data)
            except TypeError:
                _error_code = 1
                _user_msg = _(u"One or more Hardware FMEA line items had "
                              u"the wrong data type in it's data package and "
                              u"is not displayed in the FMEA form.")
                _debug_msg = ("RTK ERROR: Data for FMEA ID {0:s} for Hardware "
                              "ID {1:s} is the wrong type for one or more "
                              "columns.".format(
                                  str(_node.identifier),
                                  str(self._hardware_id)))
                _new_row = None
            except ValueError:
                _error_code = 1
                _user_msg = _(
                    u"One or more Hardware FMEA line items was missing some "
                    u"of it's data and is not displayed in the FMEA form.")
                _debug_msg = (
                    "RTK ERROR: Too few fields for FMEA ID {0:s} for Hardware "
                    "ID {1:s}.".format(
                        str(_node.identifier), str(self._hardware_id)))
                _new_row = None

        except AttributeError:
            if _node.identifier != 0:
                _error_code = 1
                _user_msg = _(u"One or more Hardware FMEA line items was "
                              u"missing it's data package and is not "
                              u"displayed in the FMEA form.")
                _debug_msg = (
                    "RTK ERROR: There is no data package for FMEA ID {0:s} "
                    "for Hardware ID {1:s}.".format(
                        str(_node.identifier), str(self._hardware_id)))
            _new_row = None

        for _n in _tree.children(_node.identifier):
            _child_tree = _tree.subtree(_n.identifier)
            self._do_load_page(tree=_child_tree, row=_new_row)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

        return (_error_code, _user_msg, _debug_msg)

    def _do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the FMEA.

        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _sibling = kwargs['sibling']
        _return = False
        _choose = False
        _undefined = False

        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 43)
            _level = self._get_level(_node_id)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _node_id = 0
            _level = 'mode'
            _prow = None

        if _sibling:
            if _level == 'control' or _level == 'action':
                _choose = True
            try:
                _entity_id = _model.get_value(_prow, 0)
                _parent_id = _model.get_value(_prow, 43)
            except TypeError:
                _entity_id = self._hardware_id
                _parent_id = _node_id

        elif not _sibling:
            if _level == 'mode':
                _level = 'mechanism'
            elif _level == 'mechanism':
                _level = 'cause'
            elif _level == 'cause':
                _choose = True
            elif _level == 'control' or _level == 'action':
                _undefined = True
            _entity_id = _model.get_value(_row, 0)
            _parent_id = _node_id

        # Insert the new entity into the RTK Program database and then refresh
        # the TreeView.
        if not FMEA.do_request_insert(
                self,
                entity_id=_entity_id,
                parent_id=_parent_id,
                level=_level,
                choose=_choose,
                undefined=_undefined):
            self._on_select(module_id=self._hardware_id)
        else:
            _return = True

        return _return

    @staticmethod
    def _get_level(node_id):
        """
        Return the level in the Hardware FMEA based on the Node ID.

        :param str node_id: the Node ID of the selected Node in the Functional
                            FMEA Tree().
        :return: _level
        :rtype: str
        """
        _level = None

        if node_id.count('.') == 1:
            _level = 'mode'
        elif node_id.count('.') == 2:
            _level = 'mechanism'
        elif node_id.count('.') == 3:
            _level = 'cause'
        elif node_id.count('.') == 4 and node_id[-1] == 'c':
            _level = 'control'
        elif node_id.count('.') == 4 and node_id[-1] == 'a':
            _level = 'action'

        return _level

    def _get_rpn_severity(self, severity, score=True):
        """
        Retrieve the corresponding value of the RPN Severity score.

        :param str,int severity: the noun name given to the RPN Severity score (score=True) or the integer value of the RPN Severity score.
        :keyword bool score: indicates whether to return the RPN Severity score for passed noun name (default) or the noun name of the passed RPN Severity score.
        :return: _rpn_severity
        :rtype: int or str depending on value of keyword score.
        """
        _rpn_severity = 0

        if score:
            try:
                _rpn_severity = [
                    x[4] for x in
                    self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_SEVERITY.values()
                    if x[1] == severity
                ][0]
            except IndexError:
                _rpn_severity = 0
        else:
            try:
                _rpn_severity = self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_SEVERITY[
                    severity][1]
            except (AttributeError, KeyError):
                _rpn_severity = ''

        return _rpn_severity

    def _get_rpn_occurrence(self, occurrence, score=True):
        """
        Retrieve the integer value of the RPN Occurence score based on name.

        :param str,int occurrence: the noun name given to the RPN Occurence score (score=True) or the integer value of the RPN Occurrence score.
        :keyword bool score: indicates whether to return the RPN Occurrence score for passed noun name (default) or the noun name of the passed RPN Occurence score.
        :return: _rpn_occurrence
        :rtype: int or str depending on value of keyword score.
        """
        _rpn_occurrence = 0

        if score:
            try:
                _rpn_occurrence = [
                    x[4] for x in
                    self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_OCCURRENCE.values()
                    if x[1] == occurrence
                ][0]
            except IndexError:
                _rpn_occurrence = 0
        else:
            try:
                _rpn_occurrence = self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_OCCURRENCE[
                    occurrence][1]
            except (AttributeError, KeyError):
                _rpn_occurrence = ''

        return _rpn_occurrence

    def _get_rpn_detection(self, detection, score=True):
        """
        Retrieve the integer value of the RPN Occurence score based on name.

        :param str,int detection: the noun name given to the RPN Occurence
                                  score (score=True) or the integer value of
                                  the RPN Detection score.
        :keyword bool score: indicates whether to return the RPN Detection
                             score for passed noun name (default) or the noun
                             name of the passed RPN Occurence score.
        :return: _rpn_detection
        :rtype: int or str depending on value of keyword score.
        """
        _rpn_detection = 0

        if score:
            try:
                _rpn_detection = [
                    x[4] for x in
                    self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_DETECTION.values()
                    if x[1] == detection
                ][0]
            except IndexError:
                _rpn_detection = 0
        else:
            try:
                _rpn_detection = self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_DETECTION[
                    detection][1]
            except (AttributeError, KeyError):
                _rpn_detection = ''

        return _rpn_detection

    def _make_methodbox(self):
        """
        Make the (D)FME(C)A option box.

        :return: _vbox
        :rtype: :class:`gtk.VBox`
        """
        _vbox = gtk.VBox()

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, True)

        _fixed.put(self.chkCriticality, 5, 5)
        _fixed.put(self.chkRPN, 5, 35)
        _fixed.put(self.txtItemCriticality.scrollwindow, 550, 5)

        _vbox.pack_end(self._make_page(), True, True)

        # By default, calculate both Task 102 and RPN.
        self.chkCriticality.set_active(True)
        self.chkRPN.set_active(True)

        return _vbox

    def _make_page(self):
        """
        Make the (D)FME(C)A RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        # Load the severity classes into the gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[12])
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_SEVERITY:
            _model.append(
                (self._mdcRTK.RTK_CONFIGURATION.RTK_SEVERITY[_item][1], ))

        # Load the RPN severity classes into the gtk.CellRendererCombo().
        for _position in [21, 34]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append(('', ))
            for _item in sorted(
                    self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_SEVERITY):
                _model.append(
                    (self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_SEVERITY[_item][1],
                     ))

        # Load the RPN occurrence classes into the gtk.CellRendererCombo().
        for _position in [22, 35]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append(('', ))
            for _item in sorted(
                    self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_OCCURRENCE):
                _model.append(
                    (self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_OCCURRENCE[_item][
                        1], ))

        # Load the RPN detection classes into the gtk.CellRendererCombo().
        for _position in [23, 36]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append(('', ))
            for _item in sorted(
                    self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_DETECTION):
                _model.append(
                    (self._mdcRTK.RTK_CONFIGURATION.RTK_RPN_DETECTION[_item][
                        1], ))

        # Load the failure probabilities into the gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[14])
        for _item in RTK_FAILURE_PROBABILITY:
            _model.append((_item[0], ))

        # Load the control type gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[20])
        for _item in RTK_CONTROL_TYPES:
            _model.append((_item, ))

        # Load the action category gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[25])
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_ACTION_CATEGORY:
            _model.append(
                (self._mdcRTK.RTK_CONFIGURATION.RTK_ACTION_CATEGORY[_item][0],
                 ))

        # Load the users into the gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[26])
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_USERS:
            _user = self._mdcRTK.RTK_CONFIGURATION.RTK_USERS[_item][0] + \
                    ', ' + self._mdcRTK.RTK_CONFIGURATION.RTK_USERS[_item][1]
            _model.append((_user, ))

        # Load the status values into the gtk.CellRendererCombo()
        _model = self._get_cell_model(self._lst_col_order[28])
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_ACTION_STATUS:
            _model.append(
                (self._mdcRTK.RTK_CONFIGURATION.RTK_ACTION_STATUS[_item][0], ))

        for i in self._lst_col_order:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()

            if isinstance(_cell[0], gtk.CellRendererPixbuf):
                pass
            elif isinstance(_cell[0], gtk.CellRendererToggle):
                _cell[0].connect('toggled', self._do_edit_cell, None, i,
                                 self.treeview.get_model())
            elif isinstance(_cell[0], gtk.CellRendererCombo):
                _cell[0].connect('edited', self._do_edit_cell, i,
                                 self.treeview.get_model())
            else:
                _cell[0].connect('edited', self._do_edit_cell, i,
                                 self.treeview.get_model())

        return FMEA._make_page(self)

    def _on_select(self, **kwargs):
        """
        Respond to `selectedHardware` signal from pypubsub.

        :param int module_id: the ID Of the Hardware item that was selected.
        :return: None
        :rtype: None
        """
        self._hardware_id = kwargs['module_id']
        self._item_hazard_rate = self._mdcRTK.dic_controllers[
            'hardware'].request_do_select(
                node_id=self._hardware_id,
                table='reliability').hazard_rate_logistics

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRTK.dic_controllers['dfmeca']

        _fmea = self._dtc_data_controller.request_do_select_all(
            parent_id=self._hardware_id, functional=False)
        (_error_code, _user_msg, _debug_msg) = self._do_load_page(
            tree=_fmea, row=None)

        RTKWorkView.on_select(
            self,
            title=_(u"Analyzing Failure Modes for Hardware ID "
                    u"{0:d}").format(self._hardware_id),
            error_code=_error_code,
            user_msg=_user_msg,
            debug_msg=_debug_msg)

        return None
