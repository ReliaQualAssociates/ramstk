# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.pof.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK PoF Work View."""

# Standard Library Imports
from typing import List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GdkPixbuf, Gtk, _
#from ramstk.views.gtk3.assistants import AddStressMethod
from ramstk.views.gtk3.widgets import (RAMSTKLabel, RAMSTKMessageDialog,
                                       RAMSTKTreeView, RAMSTKWorkView)


class PoF(RAMSTKWorkView):
    """
    Display PoF attribute data in the Work Book.

    The WorkView displays all the attributes for the Physics of Failure
    Analysis (PoF). The attributes of a PoF Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each Gtk.Widget() associated with an editable
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

    # Define private class dict attributes.
    _dic_headings = {
        'mode': [_("Mode ID"), _("Failure\nMode")],
        'mechanism': [_("Mechanism ID"),
                      _("Failure\nMechanism")],
        'opload': [_("Load ID"), _("Operating\nLoad")],
        'opstress': [_("Stress ID"), _("Operating\nStress")],
        'testmethod': [_("Test ID"), _("Recommended\nTest")]
    }

    # Define private list class attributes.
    _lst_labels: List[str] = []
    _lst_mode_mask: List[bool] = [
        True, True, True, True, True, False, False, False, False, False, False,
        False, False
    ]
    _lst_mechanism_mask: List[bool] = [
        True, True, True, False, False, False, False, False, False, False,
        False, False, False
    ]
    _lst_opload_mask: List[bool] = [
        True, True, True, False, False, True, False, False, False, True, True,
        False, False
    ]
    _lst_opstress_mask: List[bool] = [
        True, True, True, False, False, False, True, True, False, False, True,
        False, False
    ]
    _lst_pof_data = [0, "", "", "", "", "", "", "", "", "", "", None, ""]
    _lst_test_method_mask: List[bool] = [
        True, True, True, False, False, False, False, False, True, False, True,
        False, False
    ]

    # Define private class scalar attributes.
    _pixbuf: bool = True

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'pof') -> None:
        """
        Initialize the Work View for the PoF.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dict attributes.
        self._dic_column_masks = {
            'mode': self._lst_mode_mask,
            'mechanism': self._lst_mechanism_mask,
            'opload': self._lst_opload_mask,
            'opstress': self._lst_opstress_mask,
            'testmethod': self._lst_test_method_mask
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self.do_request_insert_sibling, self.do_request_insert_child,
            self._do_request_delete
        ]
        self._lst_icons = ['insert_sibling', 'insert_child', 'remove']
        self._lst_tooltips = [
            _("Add a new PoF entity at the same level as the "
              "currently selected entity."),
            _("Add a new PoF entity one level below the currently "
              "selected entity."),
            _("Remove the selected entity from the PoF.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_tree, 'succeed_retrieve_pof')
        pub.subscribe(self._on_delete_insert_pof, 'succeed_delete_pof')

    def __do_load_damage_models(self) -> None:
        """
        Load the RAMSTKTreeView() damage model CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[5])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_DAMAGE_MODELS:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_DAMAGE_MODELS[_item][0]
            ])

    def __do_load_load_history(self) -> None:
        """
        Load the RAMSTKTreeView() operating load history CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[7])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOAD_HISTORY:
            _model.append(
                [self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOAD_HISTORY[_item]])

    def __do_load_measureable_parameters(self) -> None:
        """
        Load the RAMSTKTreeView() measureable parameters CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[6])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASURABLE_PARAMETERS:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.
                RAMSTK_MEASURABLE_PARAMETERS[_item][1]
            ])

    def __load_combobox(self) -> None:
        """
        Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.__do_load_damage_models()
        self.__do_load_measureable_parameters()
        self.__do_load_load_history()

    def __make_ui(self) -> None:
        """
        Make the PoF RAMSTKTreeview().

        :return: a Gtk.Frame() containing the instance of Gtk.Treeview().
        :rtype: :class:`Gtk.Frame`
        """
        # This page has the following layout:
        #
        # +-----+---------------------------------------+
        # |  B  |                                       |
        # |  U  |                                       |
        # |  T  |                                       |
        # |  T  |              SPREAD SHEET             |
        # |  O  |                                       |
        # |  N  |                                       |
        # |  S  |                                       |
        # +-----+---------------------------------------+
        #                                    buttons -----+--> self
        #                                                 |
        #             Gtk.ScrolledWindow -->RAMSTKFrame --+
        # Make the buttons.
        super().make_toolbuttons(icons=self._lst_icons,
                                 tooltips=self._lst_tooltips,
                                 callbacks=self._lst_callbacks)
        super().make_ui_with_treeview(
            title=["", _("Physics of Failure (PoF) Analysis")])

        # Set the tab label.
        _label = RAMSTKLabel(_("PoF"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays the Physics of Failure (PoF) Analysis for "
                      "the selected hardware item."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback functions and methods for the PoF widgets.

        :return: None
        :rtype: None
        """
        self.treeview.dic_handler_id['button-press'] = self.treeview.connect(
            'button_press_event', self._on_button_press)

        for i in self._lst_col_order:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cells()

            if isinstance(_cell[0], Gtk.CellRendererPixbuf):
                pass
            else:
                _cell[0].connect('edited',
                                 super().on_cell_edit, 'wvw_editing_pof', i)

    def __set_properties(self):
        """
        Set the properties of the PoF widgets.

        :return: None
        :rtype: None
        """
        # ----- TREEVIEWS
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _("Displays the Physics of Failure (PoF) Analysis for the "
              "currently selected hardware item."))

        # Sets the FMEA carry-over information uneditable and displayed in
        # bold text.
        for i in [0, 1, 2, 3, 4]:
            _column = self.treeview.get_column(self._lst_col_order[i])
            if i == 0:
                _cell = _column.get_cells()[1]
            else:
                _cell = _column.get_cells()[0]
            _cell.set_property('editable', False)
            _cell.set_property('font', 'normal bold')

        # Set the priority Gtk.CellRendererSpin()'s adjustment limits and
        # step increments.
        _cell = self.treeview.get_column(self._lst_col_order[9]).get_cells()[0]
        _adjustment = _cell.get_property('adjustment')
        _adjustment.configure(5, 1, 5, -1, 0, 0)

    def _do_clear_page(self):
        """
        Clear the contents of the PoF page.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

    def _do_load_mechanism(self, node: treelib.Node,
                           row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['mechanism'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "", "", "", "",
            0, "", _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Failure mechanism {0:s} was missing it's data "
                           "package.").format(str(_entity.mechanism_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for failure mechanism ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.mechanism_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "failure mechanism ID {0:s}.".format(
                              str(_entity.mechanism_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_mode(self, node: treelib.Node,
                      row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mode to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self._dic_icons['mode'],
                                                       22, 22)

        _attributes = [
            node.identifier, _entity.description, _entity.effect_end,
            _entity.severity_class, _entity.mode_ratio, "", "", "", "", 0, "",
            _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Failure mode {0:s} was missing it's data "
                           "package.").format(str(_entity.mode_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = ("Data for failure mode ID {0:s} is the wrong "
                          "type for one or more columns.".format(
                              str(_entity.mode_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for Mode ID "
                          "{0:s}.".format(str(_entity.mode_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_opload(self, node: treelib.Node,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['opload'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0,
            _entity.damage_model, "", "", "", _entity.priority_id, "", _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Operating load {0:s} was missing it's data "
                           "package.").format(str(_entity.load_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for operating load ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.load_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "operating load ID {0:s}.".format(
                              str(_entity.load_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_opstress(self, node: treelib.Node,
                          row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['opstress'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "",
            _entity.measurable_parameter, _entity.load_history, "", 0,
            _entity.remarks, _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Operating stress ID {0:s} was missing it's "
                           "data package.").format(str(_entity.stress_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for operating stress ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.stress_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "operating stress ID {0:s}.".format(
                              str(_entity.stress_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_test_method(self, node: treelib.Node,
                             row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['testmethod'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "", "", "",
            _entity.boundary_conditions, 0, _entity.remarks, _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Test method ID {0:s} was missing it's "
                           "data package.").format(str(_entity.test_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for test method ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.test_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "test method ID {0:s}.".format(str(_entity.test_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_row(self, node: treelib.Node,
                     row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Determines which type of row to load and loads the data.

        :param node: the FMEA treelib Node() whose data is to be loaded.
        :type nose: :class:`treelib.Node`
        :param row: the parent row for the row to be loaded.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just added to the FMEA treeview.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # The root node will have no data package, so this indicates the need
        # to clear the tree in preparation for the load.
        if node.tag == 'pof':
            self._do_clear_page()
        else:
            _method = {
                'mode': self._do_load_mode,
                'mechanism': self._do_load_mechanism,
                'opload': self._do_load_opload,
                'opstress': self._do_load_opstress,
                'method': self._do_load_test_method
            }[node.tag]
            # noinspection PyArgumentList
            _new_row = _method(node, row)

        return _new_row

    def _do_load_tree(self,
                      tree: treelib.Tree,
                      row: Gtk.TreeIter = None) -> None:
        """
        Iterate through tree and load the PoF RAMSTKTreeView().

        :param tree: the treelib.Tree() containing the data packages for the
            PoF analysis.
        :type tree: :class:`treelib.Tree`
        :param row: the last row to be loaded with PoF data.
        :type row: :class:`Gtk.TreeIter`
        :return: None
        :rtype: None
        """
        _node = tree.nodes[list(tree.nodes.keys())[0]]

        _new_row = self._do_load_row(_node, row)

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, row=_new_row)

        super().do_expand_tree()

    def _do_request_delete(self, __button):
        """
        Request to delete the selected entity from the PoF.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 0)

        pub.sendMessage('request_delete_pof', node_id=_node_id)

    def _do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']
        _choose = False
        _undefined = False

        # Try to get the information needed to add a new entity at the correct
        # location in the PoF.  If there is nothing in the PoF, by default
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
            if _level in ('opstress', 'testmethod'):
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
            elif _level in ('opstress', 'testmethod'):
                _undefined = True
            _entity_id = _model.get_value(_row, 0)
            _parent_id = _node_id

        # Insert the new entity into the RAMSTK Program database and then refresh
        # the TreeView.
        if _undefined:
            _prompt = _(
                "A Physics of Failure operating stress or test method cannot "
                "have a child entity.", )
            _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['error'],
                                          'error')

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _dialog.do_destroy()

            _return = True

        if _choose:
            #_dialog = AddStressMethod()
            _prompt = _(
                "A Physics of Failure operating stress or test method cannot "
                "have a child entity.", )
            _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['error'],
                                          'error')

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _opstress = _dialog.rdoStress.get_active()
                _testmethod = _dialog.rdoMethod.get_active()

                if _opstress:
                    _level = 'opstress'
                elif _testmethod:
                    _level = 'testmethod'

            else:
                _return = True

            _dialog.do_destroy()

        if not _undefined:
            pub.sendMessage("request_insert_pof",
                            entity_id=_entity_id,
                            parent_id=_parent_id,
                            level=_level)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected entity in the PoF.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 0)

        self.do_set_cursor_busy()
        pub.sendMessage('request_update_pof', node_id=self._record_id)
        self.do_set_cursor_active()

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the PoF.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_all_pof')
        self.do_set_cursor_active()

    def _get_cell_model(self, column):
        """
        Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property('model')
        _model.clear()

        return _model

    def _get_indenture_level(self) -> str:
        """
        Return the level in the PoF FMEA based on the Node ID.

        :return: _level
        :rtype: str
        """
        _level = ''

        if self._record_id.count('.') == 0:
            _level = 'mode'
        elif self._record_id.count('.') == 1:
            _level = 'mechanism'
        elif self._record_id.count('.') == 2:
            _level = 'opload'
        elif self._record_id.count('.') == 4 and self._record_id[-1] == 's':
            _level = 'opstress'
        elif self._record_id.count('.') == 4 and self._record_id[-1] == 't':
            _level = 'testmethod'

        return _level

    # noinspection PyUnusedLocal
    def _on_button_press(self, __treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the PoF Work View RAMSTKTreeView().

        :param __treeview: the PoF TreeView RAMSTKTreeView().
        :type __treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
            important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`.
        :return: None
        :rtype: None
        """
        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            RAMSTKWorkView.on_button_press(self,
                                           event,
                                           icons=self._lst_icons,
                                           tooltips=self._lst_tooltips,
                                           callbacks=self._lst_callbacks)

    # pylint: disable=unused-argument
    def _on_delete_insert_pof(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Update PoF worksheet whenever an element is inserted or deleted.

        :param int node_id: the ID of the inserted/deleted PoF element.
        :param tree: the treelib Tree() containing the PoF module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._do_load_tree(tree)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the PoF Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param treeview: the PoF RAMSTKTreeView().
        :type treeview: :class:`ramstk.views.gtk3.widgets.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        _model, _row = selection.get_selected()

        try:
            self._record_id = _model.get_value(_row, 0)
        except TypeError:
            self._record_id = '0'
            _mission = ""

        _level = self._get_indenture_level()
        _headings = super().do_get_headings(_level)

        self.treeview.headings[self._lst_col_order[0]] = _headings[0]
        self.treeview.headings[self._lst_col_order[1]] = _headings[1]

        _set_visible = self.treeview.visible and self._dic_column_masks[_level]

        _columns = self.treeview.get_columns()
        i = 0
        for _heading in self.treeview.headings:
            _label = RAMSTKLabel(_heading)
            _label.do_set_properties(height=-1,
                                     justify=Gtk.Justification.CENTER,
                                     wrap=True)
            _label.show_all()
            _columns[i].set_widget(_label)
            _columns[i].set_visible(_set_visible[self._lst_col_order[i]])

            i += 1
