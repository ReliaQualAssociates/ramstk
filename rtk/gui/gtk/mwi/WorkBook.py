#!/usr/bin/env python
"""
===========================================
PyGTK Multi-Window Interface Work Book View
===========================================
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       WorkBook.py is part of The RTK Project
#
# All rights reserved.

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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
except ImportError:
    import rtk.configuration as _conf

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.Window):                 # pylint: disable=R0904
    """
    This is the Work View for the pyGTK multiple window interface.
    """

    RTK_MANUFACTURERS = {}

    RTK_HR_TYPE = {}
    RTK_HR_MODEL = {}
    RTK_S_DIST = {}
    RTK_ACTIVE_ENVIRON = {}
    RTK_DORMANT_ENVIRON = {}

    RTK_MTTR_TYPE = {}

    RTK_COST_TYPE = {}

    RTK_SW_LEVELS = {}
    RTK_SW_APPLICATION = {}
    RTK_SW_DEV_PHASES = {}

    def __init__(self, dao):
        """
        Initializes an instance of the Work View class.

        :param rtk.dao.DAO dao: the RTK Site data access object.
        """

        self.site_dao = dao

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_title(_(u"RTK Work Book"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        # On a 1268x1024 screen, the size will be 845x640.
        if _conf.OS == 'Linux':
            _width = _width - 20
            _height = (5 * _height / 8)
        elif _conf.OS == 'Windows':
            _width = _width - 20
            _height = (5 * _height / 8) - 40

        self.set_default_size(_width, _height)
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((_width / 2), (_height / 3))

        self.connect('delete_event', self.destroy)

        self._load_globals()

        self.show_all()

    def _load_globals(self):
        """
        Loads the globally used dictionaries from the RTK Site database.
        """

        _query = "SELECT * FROM tbl_category \
                  ORDER BY fld_category_noun ASC"
        (_cats, _error_code, __) = self.site_dao.execute(_query, commit=False)
        try:
            _n_cats = len(_cats)
        except TypeError:
            _n_cats = 0

        _query = "SELECT * FROM tbl_subcategory \
                  ORDER BY fld_category_id ASC"
        (_subcats, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)

        for i in range(_n_cats):
            _conf.RTK_CATEGORIES[i + 1] = [_cats[i][1], _cats[i][0]]
            _conf.RTK_SUBCATEGORIES[i + 1] = [x[1:] for x in _subcats
                                              if x[0] == i + 1]

        _query = "SELECT fld_manufacturers_noun, fld_location, fld_cage_code \
                  FROM tbl_manufacturers \
                  ORDER BY fld_manufacturers_noun ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_MANUFACTURERS[i] = [_results[i][0], _results[i][1],
                                         _results[i][2]]

        _query = "SELECT fld_hr_type_noun FROM tbl_hr_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_HR_TYPE[i] = _results[i][0]

        _query = "SELECT fld_model_noun FROM tbl_calculation_model"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_HR_MODEL[i] = _results[i][0]

        _query = "SELECT fld_distribution_noun FROM tbl_distributions"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_S_DIST[i] = _results[i][0]

        _query = "SELECT fld_active_environ_code, fld_active_environ_noun \
                  FROM tbl_active_environs"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_ACTIVE_ENVIRON[i] = [_results[i][1], _results[i][0]]

        _query = "SELECT fld_dormant_environ_noun \
                  FROM tbl_dormant_environs"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_DORMANT_ENVIRON[i] = _results[i][0]

        _query = "SELECT fld_mttr_type_noun FROM tbl_mttr_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_MTTR_TYPE[i] = _results[i][0]

        _query = "SELECT fld_cost_type_noun FROM tbl_cost_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_COST_TYPE[i] = _results[i][0]

        _query = "SELECT fld_level_desc, fld_level_id FROM tbl_software_level"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_SW_LEVELS[i] = _results[i][0]

        _query = "SELECT fld_category_name, fld_category_id, \
                         fld_category_description \
                  FROM tbl_software_category"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_SW_APPLICATION[i] = _results[i][0]

        _query = "SELECT fld_phase_desc, fld_phase_id \
                  FROM tbl_development_phase"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        try:
            _n_results = len(_results)
        except TypeError:
            _n_results = 0

        for i in range(_n_results):
            self.RTK_SW_DEV_PHASES[i] = _results[i][0]

        return False

    def destroy(self, __widget, __event=None):
        """
        Quits the RTK application when the X in the upper right corner is
        pressed.

        :param gtk.Widget __widget: the gtk.Widget() that called this method.
        :keyword gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        gtk.main_quit()

        return False
