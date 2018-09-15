# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.View.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseView Module."""

import locale

# Import other RAMSTK Widget classes.
from ramstk.gui.gtk.ramstk import RAMSTKTreeView
from .Widget import gtk


class RAMSTKBaseView(object):
    """
    Meta class for all RAMSTK ListView, ModuleView, and WorkView classes.

    Attributes of the RAMSTKBaseView are:

    :ivar dict _dic_icons: dictionary containing icon name and absolute path
                           key:value pairs.
    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable attribute.
    :ivar _mdcRAMSTK: the :py:class:`ramstk.RAMSTK.RAMSTK` master data controller.
    :ivar float _mission_time: the mission time for the open RAMSTK Program.
    :ivar _notebook: the :py:class:`gtk.Notebook` to hold all the pages of
                     information to be displayed.
    :ivar str fmt: the formatting code for numerical displays.
    """

    _response_ok = gtk.RESPONSE_OK

    _left_tab = gtk.POS_LEFT
    _right_tab = gtk.POS_RIGHT
    _top_tab = gtk.POS_TOP
    _bottom_tab = gtk.POS_BOTTOM

    def __init__(self, controller, **kwargs):
        """
        Initialize the RAMSTK Base View.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        _module = kwargs['module']

        # Initialize private dictionary attributes.
        self._dic_icons = {
            'calculate':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/calculate.png',
            'calculate_all':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/calculate-all.png',
            'add':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/add.png',
            'remove':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/remove.png',
            'reports':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/reports.png',
            'save':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/save.png',
            'save-all':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/save-all.png',
            'important':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/important.png',
            'error':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/error.png',
            'question':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/question.png',
            'insert_sibling':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/insert_sibling.png',
            'insert_child':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/insert_child.png',
            'cancel':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/cancel.png',
            'export':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/export.png',
            'warning':
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/warning.png',
        }

        # Initialize private list attributes.
        self._lst_col_order = []
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = None
        self._mdcRAMSTK = controller
        self._mission_time = float(
            controller.RAMSTK_CONFIGURATION.RAMSTK_MTIME)
        self._notebook = gtk.Notebook()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        if _module is None:
            self.treeview = None
        else:
            try:
                _bg_color = controller.RAMSTK_CONFIGURATION.RAMSTK_COLORS[
                    _module + 'bg']
                _fg_color = controller.RAMSTK_CONFIGURATION.RAMSTK_COLORS[
                    _module + 'fg']
                _fmt_file = (
                    controller.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR +
                    '/layouts/' +
                    controller.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE[_module]
                )
                _fmt_path = "/root/tree[@name='" + _module.title() + "']/column"

                self.treeview = RAMSTKTreeView(_fmt_path, 0, _fmt_file,
                                               _bg_color, _fg_color)
                self._lst_col_order = self.treeview.order
            except KeyError:
                self.treeview = gtk.TreeView()

        self.fmt = '{0:0.' + \
                   str(controller.RAMSTK_CONFIGURATION.RAMSTK_DEC_PLACES) + 'G}'
        self.hbx_tab_label = gtk.HBox()

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RAMSTK_CONFIGURATION.RAMSTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

    def _make_buttonbox(self, **kwargs):
        """
        Create the buttonbox for RAMSTK Views.

        This method creates the base buttonbox used by all RAMSTK View.  Use a
        buttonbox for an RAMSTK View if there are only buttons to be added.

        :return: _buttonbox
        :rtype: :py:class:`gtk.ButtonBox`
        """
        _icons = kwargs['icons']
        _tooltips = kwargs['tooltips']
        _callbacks = kwargs['callbacks']
        _orientation = kwargs['orientation']
        _height = kwargs['height']
        _width = kwargs['width']

        if _orientation == 'horizontal':
            _buttonbox = gtk.HButtonBox()
        else:
            _buttonbox = gtk.VButtonBox()

        _buttonbox.set_layout(gtk.BUTTONBOX_START)

        i = 0
        for _icon in _icons:
            _image = gtk.Image()
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                self._dic_icons[_icon], _height, _width)
            _image.set_from_pixbuf(_icon)

            _button = gtk.Button()
            _button.set_image(_image)

            _button.props.width_request = _width
            _button.props.height_request = _height

            try:
                _button.set_tooltip_markup(_tooltips[i])
            except IndexError:
                _button.set_tooltip_markup("")

            try:
                _button.connect('clicked', _callbacks[i])
            except IndexError:
                _button.set_sensitive(False)

            _buttonbox.pack_start(_button)

            i += 1

        return _buttonbox

    def _make_toolbar(self,
                      icons,
                      orientation='horizontal',
                      height=60,
                      width=60):
        """
        Create the toolbar for RAMSTK Views.

        This method creates the base toolbar used by all RAMSTK Views.  Use a
        toolbar for an RAMSTK View if there are other than buttons to be added.

        :param list icons: list of icon names to place on the toolbuttons.
                           The items in the list are keys in _dic_icons.
        :return: _toolbar, _position
        :rtype: (:py:class:`gtk.Toolbar`, int)
        """
        _toolbar = gtk.Toolbar()

        if orientation == 'horizontal':
            _toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
            _scale = 0.58
        else:
            _toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
            _scale = 0.4

        _position = 0
        for _icon in icons:
            if _icon is None:
                _toolbar.insert(gtk.SeparatorToolItem(), _position)
            else:
                _image = gtk.Image()
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons[_icon], int(_scale * height),
                    int(_scale * width))
                _image.set_from_pixbuf(_icon)

                _button = gtk.ToolButton()
                _button.set_property("height_request", height)
                _button.set_property("width_request", width)
                _button.set_icon_widget(_image)
                _button.show()
                _toolbar.insert(_button, _position)

            _position += 1

        _toolbar.show()

        # Return the toolbar and the next position to place an gtk.ToolBar()
        # item.  The _position variable can be used by derived classes to
        # add additional items to the gtk.ToolBar().
        return _toolbar, _position

    def on_select_revision(self, **kwargs):
        """
        Load the RAMSTK View gtk.TreeModel() when a Revision is selected.

        :param tree: the treelib Tree() that should be loaded into the View's
                     RAMSTKTreeView.
        :type tree: :class:`treelib.Tree`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _tree = kwargs['tree']
        _return = False

        _model = self.treeview.get_model()
        _model.clear()

        try:
            _return = self.treeview.do_load_tree(_tree)
        except AttributeError:
            for _node in _tree.nodes.values()[1:]:
                _entity = _node.data

                _attributes = []
                if _entity is not None:
                    _temp = _entity.get_attributes()

                    for _key in _temp:
                        _attributes.append(_temp[_key])

                try:
                    _row = _model.append(_attributes[:2])
                except ValueError:
                    _row = None
                    _return = True

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

        return _return

    def set_cursor(self, cursor):
        """
        Set the cursor for the Module, List, and Work Book gtk.gdk.Window().

        :param controller: the RAMSTK master data controller.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        :param gtk.gdk.Cursor cursor: the gtk.gdk.Cursor() to set.  Only
                                      handles one of the following:
                                        - gtk.gdk.X_CURSOR
                                        - gtk.gdk.ARROW
                                        - gtk.gdk.CENTER_PTR
                                        - gtk.gdk.CIRCLE
                                        - gtk.gdk.CROSS
                                        - gtk.gdk.CROSS_REVERSE
                                        - gtk.gdk.CROSSHAIR
                                        - gtk.gdk.DIAMOND_CROSS
                                        - gtk.gdk.DOUBLE_ARROW
                                        - gtk.gdk.DRAFT_LARGE
                                        - gtk.gdk.DRAFT_SMALL
                                        - gtk.gdk.EXCHANGE
                                        - gtk.gdk.FLEUR
                                        - gtk.gdk.GUMBY
                                        - gtk.gdk.HAND1
                                        - gtk.gdk.HAND2
                                        - gtk.gdk.LEFT_PTR - non-busy cursor
                                        - gtk.gdk.PENCIL
                                        - gtk.gdk.PLUS
                                        - gtk.gdk.QUESTION_ARROW
                                        - gtk.gdk.RIGHT_PTR
                                        - gtk.gdk.SB_DOWN_ARROW
                                        - gtk.gdk.SB_H_DOUBLE_ARROW
                                        - gtk.gdk.SB_LEFT_ARROW
                                        - gtk.gdk.SB_RIGHT_ARROW
                                        - gtk.gdk.SB_UP_ARROW
                                        - gtk.gdk.SB_V_DOUBLE_ARROW
                                        - gtk.gdk.TCROSS
                                        - gtk.gdk.TOP_LEFT_ARROW
                                        - gtk.gdk.WATCH - when application is busy
                                        - gtk.gdk.XTERM - selection bar
        :return: None
        :rtype: None
        """
        self._mdcRAMSTK.dic_books['listbook'].get_window().set_cursor(
            gtk.gdk.Cursor(cursor))
        self._mdcRAMSTK.dic_books['modulebook'].get_window().set_cursor(
            gtk.gdk.Cursor(cursor))
        self._mdcRAMSTK.dic_books['workbook'].get_window().set_cursor(
            gtk.gdk.Cursor(cursor))

        gtk.gdk.flush()

        return None
