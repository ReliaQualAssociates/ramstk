# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.PoF.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""PoF Work View."""

from sortedcontainers import SortedDict
from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from rtk.gui.gtk.assistants import AddStressMethod
from .WorkView import RTKWorkView


class PoF(RTKWorkView):
    """
    Display PoF attribute data in the Work Book.

    The WorkView displays all the attributes for the Physics of Failure
    Analysis (PoF). The attributes of a PoF Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Functional PoF attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   | tvw_pof `cursor_changed`                  |
    +----------+-------------------------------------------+
    |      1   | tvw_pof `button_press_event`              |
    +----------+-------------------------------------------+
    |      2   | tvw_pof `edited`                          |
    +----------+-------------------------------------------+
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the PoF.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='PoF')

        # Initialize private dictionary attributes.
        self._dic_icons['mode'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/mode.png'
        self._dic_icons['mechanism'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/mechanism.png'
        self._dic_icons['opload'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/load.png'
        self._dic_icons['opstress'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/stress.png'
        self._dic_icons['testmethod'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/method.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_data_controller = None
        self._hardware_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['pof']
        _fmt_path = "/root/tree[@name='PoF']/column"
        _tooltip = _(u"Displays the Physics of Failure (PoF) Analysis for the "
                     u"currently selected hardware item.")

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
            _(u"Damage\nModeling"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays the Physics of Failure (PoF) Analysis for "
                      u"the selected hardware item."))
        self.hbx_tab_label.pack_start(_label)

        self.pack_start(self._make_buttonbox(), False, True)
        self.pack_end(self._make_treeview(), True, True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedHardware')

    def _do_load_page(self, **kwargs):
        """
        Iterate through the tree and load the Physics of Failure RTKTreeView().

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
            self._hardware_id, functional=False)

        _node = _tree.nodes[SortedDict(_tree.nodes).keys()[0]]
        _entity = _node.data
        try:
            if _entity.is_mode:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mode'], 22, 22)
                _data = [
                    _entity.mode_id, _entity.description, _entity.effect_end,
                    _entity.severity_class, _entity.mode_probability, '', '',
                    '', '', 0, _entity.remarks, _icon, _node.identifier
                ]
                _row = None
            elif _entity.is_mechanism:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mechanism'], 22, 22)
                _data = [
                    _entity.mechanism_id, _entity.description, '', '', '', '',
                    '', '', '', 0, '', _icon, _node.identifier
                ]
            elif _entity.is_opload:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['opload'], 22, 22)
                _data = [
                    _entity.load_id, _entity.description, '', '', '',
                    _entity.damage_model, '', '', '', _entity.priority_id, '',
                    _icon, _node.identifier
                ]
            elif _entity.is_opstress and _row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['opstress'], 22, 22)
                _data = [
                    _entity.stress_id, _entity.description, '', '', '', '',
                    _entity.measurable_parameter, _entity.load_history, '', 0,
                    _entity.remarks, _icon, _node.identifier
                ]
            elif _entity.is_testmethod and _row is not None:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['testmethod'], 22, 22)
                _data = [
                    _entity.test_id, _entity.description, '', '', '', '', '',
                    '', _entity.boundary_conditions, 0, _entity.remarks, _icon,
                    _node.identifier
                ]

            try:
                _new_row = _model.append(_row, _data)
            except TypeError:
                _error_code = 1
                _user_msg = _(u"One or more PoF line items had the wrong data "
                              u"type in it's data package and is not "
                              u"displayed in the PoF form.")
                _debug_msg = ("RTK ERROR: Data for PoF ID {0:s} for Hardware "
                              "ID {1:s} is the wrong type for one or more "
                              "columns.".format(
                                  str(_node.identifier),
                                  str(self._hardware_id)))
                _new_row = None
            except ValueError:
                _error_code = 1
                _user_msg = _(
                    u"One or more PoF line items was missing some of it's "
                    u"data and is not displayed in the PoF form.")
                _debug_msg = (
                    "RTK ERROR: Too few fields for PoF ID {0:s} for Hardware "
                    "ID {1:s}.".format(
                        str(_node.identifier), str(self._hardware_id)))
                _new_row = None

        except AttributeError:
            if _node.identifier != 0:
                _error_code = 1
                _user_msg = _(u"One or more PoF line items was missing it's "
                              u"data package and is not displayed in the PoF "
                              u"form.")
                _debug_msg = (
                    "RTK ERROR: There is no data package for PoF ID {0:s} "
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
            self.treeview.headings[self._lst_col_order[10]]
        ]

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 12)
        except (TypeError, ValueError):
            _node_id = 0

        _level = self._get_level(_node_id)

        if _level == 'mode':
            _headings[0] = self.treeview.headings[self._lst_col_order[0]]
            _headings[1] = self.treeview.headings[self._lst_col_order[1]]
            for _idx in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', False)
        elif _level == 'mechanism':
            _headings[0] = _(u"Mechanism ID")
            _headings[1] = _(u"Failure\nMechanism")
            for _idx in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', False)
        elif _level == 'opload':
            _headings[0] = _(u"Operating\nLoad ID")
            _headings[1] = _(u"Damaging\nCondition")
            for _idx in [2, 3, 4, 6, 7, 8]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', False)
            for _idx in [1, 5, 9]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', True)
        elif _level == 'opstress':
            _headings[0] = _(u"Stress ID")
            _headings[1] = _(u"Operating\nStress")
            for _idx in [2, 3, 4, 5, 8, 9]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', False)
            for _idx in [1, 6, 7]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', True)
        elif _level == 'testmethod':
            _headings[0] = _(u"Test ID")
            _headings[1] = _(u"Existing or\nProposed Test")
            for _idx in [2, 3, 4, 5, 6, 7, 9]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', False)
                _cell.set_property('mode', gtk.CELL_RENDERER_MODE_INERT)
            for _idx in [1, 8]:
                _cell = self.treeview.get_column(
                    self._lst_col_order[_idx]).get_cell_renderers()[0]
                _cell.set_property('editable', True)
                _cell.set_property('mode', gtk.CELL_RENDERER_MODE_EDITABLE)

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
        Handle edits of the PoF RTKTreeview().

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

            _entity = self._dtc_data_controller.request_select(model[path][12])

            if _entity.is_opload:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.damage_model = model[path][self._lst_col_order[5]]
                _entity.priority_id = model[path][self._lst_col_order[9]]
                _entity.remarks = model[path][self._lst_col_order[10]]
            elif _entity.is_opstress:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.measurable_parameter = model[path][self._lst_col_order[
                    6]]
                _entity.load_history = model[path][self._lst_col_order[7]]
                _entity.remarks = model[path][self._lst_col_order[10]]
            elif _entity.is_testmethod:
                _entity.description = model[path][self._lst_col_order[1]]
                _entity.boundary_conditions = model[path][self._lst_col_order[
                    8]]
                _entity.remarks = model[path][self._lst_col_order[10]]

        return _return

    def _do_request_delete(self, __button):
        """
        Request to delete the selected entity from the PoF.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 12)

        # Delete the selected entity from the RTK Program database and then
        # refresh the TreeView.
        if not self._dtc_data_controller.request_do_delete(_node_id):
            self._on_select(module_id=self._hardware_id)
        else:
            _return = True

        return _return

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
            _node_id = _model.get_value(_row, 12)
            _level = self._get_level(_node_id)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _node_id = 0
            _level = 'mode'
            _prow = None

        if _sibling:
            if _level == 'opstress' or _level == 'testmethod':
                _choose = True
            try:
                _entity_id = _model.get_value(_prow, 0)
                _parent_id = _model.get_value(_prow, 12)
            except TypeError:
                _entity_id = self._hardware_id
                _parent_id = _node_id

        elif not _sibling:
            if _level == 'mechanism':
                _level = 'opload'
            elif _level == 'opload':
                _choose = True
            elif _level == 'opstress' or _level == 'testmethod':
                _undefined = True
            _entity_id = _model.get_value(_row, 0)
            _parent_id = _node_id

        # Insert the new entity into the RTK Program database and then refresh
        # the TreeView.
        if _undefined:
            _prompt = _(u"A Physics of Failure operating stress or test "
                        u"method cannot have a child entity.")
            _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')

            if _dialog.do_run() == gtk.RESPONSE_OK:
                _dialog.do_destroy()

            _return = True

        if _choose:
            _dialog = AddStressMethod()
            _response = _dialog.do_run()

            if _dialog.do_run() == gtk.RESPONSE_OK:
                _opstress = _dialog.rdoStress.get_active()
                _testmethod = _dialog.rdoMethod.get_active()

                if _opstress:
                    _level = 'opstress'
                elif _testmethod:
                    _level = 'testmethod'

            else:
                _return = True

            _dialog.do_destroy()

        # Insert the new entity into the RTK Program database and then refresh
        # the TreeView.
        if (_undefined or _return
                or self._dtc_data_controller.request_do_insert(
                    entity_id=_entity_id, parent_id=_parent_id, level=_level)):
            _return = True

        if not _return:
            self._on_select(module_id=self._hardware_id)

        return _return

    def _do_request_insert_child(self, __button):
        """
        Request to insert a new entity to the PoF at the next level.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=False)

    def _do_request_insert_sibling(self, __button):
        """
        Request to insert a new entity to the PoF at the same level.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=True)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected entity in the PoF.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 12)

        return self._dtc_data_controller.request_do_update(_node_id)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the PoF.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update_all()

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

    @staticmethod
    def _get_level(node_id):
        """
        Return the level in the PoF FMEA based on the Node ID.

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
            _level = 'opload'
        elif node_id.count('.') == 4 and node_id[-1] == 's':
            _level = 'opstress'
        elif node_id.count('.') == 4 and node_id[-1] == 't':
            _level = 'testmethod'

        return _level

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the PoF class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the PoF Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new PoF entity at the same level as the "
              u"currently selected entity."),
            _(u"Add a new PoF entity one level below the currently "
              u"selected entity."),
            _(u"Remove the selected entity from the PoF."),
            _(u"Save the currently selected item in the PoF to the RTK "
              u"Program database."),
            _(u"Save the PoF to the open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_delete, self._do_request_update,
            self._do_request_update_all
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'remove', 'save', 'save-all'
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
        Make the PoF RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = rtk.RTKFrame(label=_(u"Physics of Failure (PoF) Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        for i in [0, 1, 2, 3, 4]:
            _column = self.treeview.get_column(self._lst_col_order[i])
            if i == 0:
                _cell = _column.get_cell_renderers()[1]
            else:
                _cell = _column.get_cell_renderers()[0]
            _cell.set_property('font', 'normal bold')

        #for i in [1, 5, 6, 7, 8, 9, 10]:
        #    _column = self.treeview.get_column(self._lst_col_order[i])
        #    _cell = _column.get_cell_renderers()[0]
        #    _column.set_attributes(_cell, text=i)

        # Load the damage models into the gtk.CellRendererCombo().
        _model = self._do_get_cell_model(self._lst_col_order[5])
        _model.append(('', ))
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_DAMAGE_MODELS:
            _model.append(
                (self._mdcRTK.RTK_CONFIGURATION.RTK_DAMAGE_MODELS[_item][0], ))

        # Load the measureable parameter into the gtk.CellRendererCombo().
        _model = self._do_get_cell_model(self._lst_col_order[6])
        _model.append(('', ))
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_MEASURABLE_PARAMETERS:
            _model.append(
                (self._mdcRTK.RTK_CONFIGURATION.RTK_MEASURABLE_PARAMETERS[
                    _item][1], ))

        # Load the measureable parameter into the gtk.CellRendererCombo().
        _model = self._do_get_cell_model(self._lst_col_order[7])
        _model.append(('', ))
        for _item in self._mdcRTK.RTK_CONFIGURATION.RTK_LOAD_HISTORY:
            _model.append(
                (self._mdcRTK.RTK_CONFIGURATION.RTK_LOAD_HISTORY[_item][0], ))

        # Set the priority gtk.CellRendererSpin()'s adjustment limits and
        # step increments.
        _cell = self.treeview.get_column(
            self._lst_col_order[9]).get_cell_renderers()[0]
        _adjustment = _cell.get_property('adjustment')
        _adjustment.configure(5, 1, 5, -1, 0, 0)
        _digits = _cell.get_property('digits')
        _digits = 1

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

        return _frame

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the PoF Work View RTKTreeView().

        :param treeview: the PoF TreeView RTKTreeView().
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
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)
        treeview.handler_unblock(self._lst_handler_id[1])

        return _return

    def _on_select(self, **kwargs):
        """
        Respond to `selectedHardware` signal from pypubsub.

        :param int module_id: the ID Of the Hardware item that was selected.
        :return: None
        :rtype: None
        """
        self._hardware_id = kwargs['module_id']

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRTK.dic_controllers['pof']

        _pof = self._dtc_data_controller.request_do_select_all(
            self._function_id, functional=True)
        (_error_code, _user_msg, _debug_msg) = self._do_load_page(
            tree=_pof, row=None)

        RTKWorkView.on_select(
            self,
            title=_(u"Analyzing Physics of Failure for Hardware ID "
                    u"{0:d}").format(self._hardware_id),
            error_code=_error_code,
            user_msg=_user_msg,
            debug_msg=_debug_msg)

        return None
