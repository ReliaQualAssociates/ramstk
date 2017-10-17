# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.WorkBook.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
PyGTK Multi-Window Interface Work Book
===============================================================================
"""

# Import modules for localization support.
import gettext

from pubsub import pub                              # pylint: disable=E0401

# Import other RTK modules.
# pylint: disable=E0401
from gui.gtk.rtk import RTKBook
from gui.gtk.workviews import wvwRevision
from gui.gtk.workviews import wvwFunction

_ = gettext.gettext


class WorkBook(RTKBook):                 # pylint: disable=R0904
    """
    This is the Work Book for the pyGTK multiple window interface.
    """

    def __init__(self, controller):
        """
        Initializes an instance of the Work View class.

        :param controller: the RTK master data controller.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKBook.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_work_views = {'revision': wvwRevision(controller),
                               'function': wvwFunction(controller)}

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Set the properties for the ModuleBook and it's widgets.
        self.set_title(_(u"RTK Work Book"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        # On a 1268x1024 screen, the size will be 845x640.
        _width = self._width - 20
        _height = (5 * self._height / 8) - 40

        self.set_default_size(_width, _height)
        self.move((_width / 1), (_height / 2))

        self._on_module_change(module='revision')

        self.show_all()

        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module=''):
        """
        Method to load the correct Work Views for the RTK module that was
        selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        for _child in self.get_children():
            self.remove(_child)

        self.add(self.dic_work_views[module])
        #for _workspace in self.dic_work_views[module]:
        #    self.notebook.insert_page(_workspace, _workspace.hbx_tab_label, -1)

        return _return
