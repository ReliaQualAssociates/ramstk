# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.View.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
RTKBaseView Module
-------------------------------------------------------------------------------

This module contains the base class for all the RTK data model views.  It
provides the basis for the RTKListView, RTKModuleView, and RTKWorkView.
"""

import locale

# Import other RTK Widget classes.
from .Widget import gtk                         # pylint: disable=E0401


class RTKBaseView(object):
    """
    This is the meta class for all RTK ListView, ModuleView, and WorkView
    classes.  Attributes of the RTKBaseView are:

    :ivar dict _dic_icons: dictionary containing icon name and absolute path
                           key:value pairs.
    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable attribute.
    :ivar _mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller.
    :ivar float _mission_time: the mission time for the open RTK Program.
    :ivar _notebook: the :py:class:`gtk.Notebook` to hold all the pages of
                     information to be displayed.
    :ivar str fmt: the formatting code for numerical displays.
    """

    _response_ok = gtk.RESPONSE_OK

    _left_tab = gtk.POS_LEFT
    _right_tab = gtk.POS_RIGHT
    _top_tab = gtk.POS_TOP
    _bottom_tab = gtk.POS_BOTTOM

    def __init__(self, controller):
        """
        Method to initialize the Work View.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        # Initialize private dictionary attributes.
        self._dic_icons = {'calculate':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/calculate.png',
                           'add':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/add.png',
                           'remove':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/remove.png',
                           'reports':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/reports.png',
                           'save':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/save.png',
                           'save-all':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/save-all.png',
                           'error':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/error.png',
                           'question':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/question.png',
                           'insert_sibling':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/insert_sibling.png',
                           'insert_child':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/insert_child.png'}

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = None
        self._mdcRTK = controller
        self._mission_time = float(controller.RTK_CONFIGURATION.RTK_MTIME)
        self._notebook = gtk.Notebook()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = '{0:0.' + \
                   str(controller.RTK_CONFIGURATION.RTK_DEC_PLACES) + 'g}'
        self.hbx_tab_label = gtk.HBox()

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

    # pylint: disable=too-many-arguments
    def _make_buttonbox(self, icons, tooltips, callbacks,
                        orientation='horizontal', height=-1, width=-1):
        """
        Method to create the buttonbox for RTK Views.  This method creates the
        base buttonbox used by all RTK View.  Use a buttonbox for an RTK View
        if there are only buttons to be added.

        :param list icons: list of icon names to place on the toolbuttons.
                           The items in the list are keys in _dic_icons.
        :return: _buttonbox
        :rtype: :py:class:`gtk.ButtonBox`
        """

        if orientation == 'horizontal':
            _buttonbox = gtk.HButtonBox()
        else:
            _buttonbox = gtk.VButtonBox()

        _buttonbox.set_layout(gtk.BUTTONBOX_START)

        i = 0
        for _icon in icons:
            _image = gtk.Image()
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                self._dic_icons[_icon], height, width)
            _image.set_from_pixbuf(_icon)

            _button = gtk.Button()
            _button.set_image(_image)

            _button.props.width_request = width
            _button.props.height_request = height

            try:
                _button.set_tooltip_markup(tooltips[i])
            except IndexError:
                _button.set_tooltip_markup("")

            try:
                _button.connect('clicked', callbacks[i])
            except IndexError:
                _button.set_sensitive(False)

            _buttonbox.pack_start(_button)

            i += 1

        return _buttonbox

    def _make_toolbar(self, icons, orientation='horizontal', height=60,
                      width=60):
        """
        Method to create the toolbar for RTK Views.  This method creates the
        base toolbar used by all RTK Views.  Use a toolbar for an RTK View if
        there are other than buttons to be added.

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
