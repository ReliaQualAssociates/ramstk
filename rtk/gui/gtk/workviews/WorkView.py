# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.WorkView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
RTK Work View Package Meta Class
###############################################################################
"""

import locale

# Import other RTK modules.
from gui.gtk.rtk.Widget import _, gtk           # pylint: disable=E0401,W0611
from gui.gtk import rtk                         # pylint: disable=E0401,W0611


class RTKWorkView(object):
    """
    This is the meta class for all RTK Work View classes.  Attributes of the
    RTKWorkView are:

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
        self._mdcRTK = controller
        self._mission_time = controller.RTK_CONFIGURATION.RTK_MTIME
        self._notebook = gtk.Notebook()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = '{0:0.' + \
                   str(controller.RTK_CONFIGURATION.RTK_DEC_PLACES) + 'g}'

        # Set the user's preferred gtk.Notebook tab position.
        if controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'left':
            self._notebook.set_tab_pos(gtk.POS_LEFT)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'right':
            self._notebook.set_tab_pos(gtk.POS_RIGHT)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'top':
            self._notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self._notebook.set_tab_pos(gtk.POS_BOTTOM)

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

    @staticmethod
    def _make_assessment_results_page():
        """
        Method to create the gtk.Notebook() page for displaying assessment
        results.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _hbox = gtk.HBox()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the left half of the page.                                    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_left = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fxd_left)
        _frame = rtk.RTKFrame(label=_(u"Reliability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the right half of the page.                                   #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_right = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fxd_right)
        _frame = rtk.RTKFrame(label=_(u"Maintainability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame)

        return _hbox, _fxd_left, _fxd_right

    @staticmethod
    def _make_general_data_page():
        """
        Method to create the gtk.Notebook() page for displaying general data.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _frame = rtk.RTKFrame(label=_(u"General Information"))

        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame.add(_scrollwindow)

        return _frame, _fixed

    def _make_toolbar(self, hierarchical=False):
        """
        Method to create the toolbar for the Work View.  This method creates
        the base toolbar used by all RTK Work Views.  Individual RTK Module
        Work Views will add additional buttons after the Save button.

        :param bool hierarchical: indicates whether or not the RTK Module the
                                  toolbar is being created for is hierarchical.
        :return: _toolbar
        :rtpye: :py:class:`gtk.Toolbar`
        """

        def _make_button(image):
            """
            Function to create a gtk.ToolButton() for the gtk.Toolbar().

            :param str image: the absolute path to the image file to use for
                              the gtk.ToolButton() icon.
            :return: _button
            :rtype: :py:class:`gtk.ToolButton`
            """

            _button = gtk.ToolButton()
            _image = gtk.Image()
            _image.set_from_file(image)
            _button.set_icon_widget(_image)

            return _button

        _toolbar = gtk.Toolbar()

        _position = 0

        # If this toolbar is for an RTK Module that is hierarchical (e.g.,
        # Function, Hardware, Software, etc.) we need to create a button to
        # add a sibling and a button to add a child.  If it is not hierarchical
        # (e.g., Revision), we only need to insert an add button.
        if hierarchical:
            # Add sibling function button.
            _button = _make_button(self._dic_icons['insert_sibling'])
            _toolbar.insert(_button, _position)
            _position += 1

            # Add child function button.
            _button = _make_button(self._dic_icons['insert_child'])
            _toolbar.insert(_button, _position)
            _position += 1

        else:
            _button = _make_button(self._dic_icons['add'])
            _toolbar.insert(_button, _position)
            _position += 1

        # Delete function button
        _button = _make_button(self._dic_icons['remove'])
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Calculate function button.
        _button = _make_button(self._dic_icons['calculate'])
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save function button.
        _button = _make_button(self._dic_icons['save'])
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar
