#!/usr/bin/env python
"""
###############################################
Software Package Bill of Materials (BoM) Module
###############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.BoM.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    from software.Software import Model as Software
    from software.CSCI import Model as CSCI
    from software.Unit import Model as Unit
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    from rtk.software.Software import Model as Software
    from rtk.software.CSCI import Model as CSCI
    from rtk.software.Unit import Model as Unit

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ParentError(Exception):
    """
    Exception raised when a revision ID is not passed or when initializing an
    instance of the BoM model.
    """

    pass


class BoM(object):
    """
    The BoM data controller provides an interface between the BoM data model
    and an RTK view model.  A single BoM data controller can manage one or more
    BoM data models.  The attributes of a BoM data controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar _last_id: the last Software ID used in the RTK Project database.
    :ivar dicSoftware: Dictionary of the Software data models managed.  Key is
                       the Software ID; value is a pointer to the Software data
                       model instance.
    """

    def __init__(self):
        """
        Initializes a Software BoM data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicSoftware = {}

    def request_bom(self, dao, revision_id):
        """
        Reads the RTK Project database and loads all the Software associated
        with the selected Revision.  For each software item returned:

        #. Retrieve the software CSCI and units from the RTK Project database.
        #. Create a CSCI or Unit data model instance as appropriate.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of software being managed
           by this controller.

        :param dao: the :py:class:`rtk.dao.DAO` object to use for communicating
                    with the RTK Project database.
        :param int revision_id: the Revision ID to select the requirements for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_software')[0]

        # Select everything from the software table.
        _query = "SELECT t1.fld_revision_id, t1.fld_software_id, \
                         t1.fld_level_id, t1.fld_description, \
                         t1.fld_application_id, t1.fld_development_id, \
                         t1.fld_a, t1.fld_do, t1.fld_dd, t1.fld_dc, t1.fld_d, \
                         t1.fld_am, t1.fld_sa, t1.fld_st, t1.fld_dr, \
                         t1.fld_sq, t1.fld_s1, t1.fld_hloc, t1.fld_aloc, \
                         t1.fld_loc, t1.fld_sl, t1.fld_ax, t1.fld_bx, \
                         t1.fld_cx, t1.fld_nm, t1.fld_sx, t1.fld_um, \
                         t1.fld_wm, t1.fld_xm, t1.fld_sm, t1.fld_df, \
                         t1.fld_sr, t1.fld_s2, t1.fld_rpfom, \
                         t1.fld_parent_id, t1.fld_dev_assess_type, \
                         t1.fld_phase_id, t1.fld_tcl, t1.fld_test_path, \
                         t1.fld_category, t1.fld_test_effort, \
                         t1.fld_test_approach, t1.fld_labor_hours_test, \
                         t1.fld_labor_hours_dev, t1.fld_budget_test, \
                         t1.fld_budget_dev, t1.fld_schedule_test, \
                         t1.fld_schedule_dev, t1.fld_branches, \
                         t1.fld_branches_test, t1.fld_inputs, \
                         t1.fld_inputs_test, t1.fld_nm_test, \
                         t1.fld_interfaces, t1.fld_interfaces_test, \
                         t1.fld_te, t1.fld_tm, t1.fld_tc, t1.fld_t, \
                         t1.fld_ft1, t1.fld_ft2, t1.fld_ren_avg, \
                         t1.fld_ren_eot, t1.fld_ec, t1.fld_ev, t1.fld_et, \
                         t1.fld_os, t1.fld_ew, t1.fld_e, t1.fld_f, t1.fld_cb, \
                         t1.fld_ncb, t1.fld_dr_test, t1.fld_test_time, \
                         t1.fld_dr_eot, t1.fld_test_time_eot \
                  FROM rtk_software AS t1 \
                  WHERE t1.fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_modules = len(_results)
        except TypeError:
            _n_modules = 0

        for i in range(_n_modules):
            if _results[i][2] == 1:         # System
                _software = Software()
            elif _results[i][2] == 2:       # CSCI
                _software = CSCI()
            elif _results[i][2] == 3:       # Unit
                _software = Unit()
            _software.set_attributes(_results[i])
            self.dicSoftware[_software.software_id] = _software

        for _key in self.dicSoftware.keys():
            _software = self.dicSoftware[_key]
            for _key2 in self.dicSoftware.keys():
                _software2 = self.dicSoftware[_key2]
                if(_software2.parent_id == _software.software_id and
                   _software2.level_id == 2):
                    try:
                        _software.dicCSCI[_software.software_id].append(_software2)
                    except KeyError:
                        _software.dicCSCI[_software.software_id] = [_software2]
                elif(_software2.parent_id == _software.software_id and
                     _software2.level_id == 3):
                    try:
                        _software.dicUnits[_software.software_id].append(_software2)
                    except KeyError:
                        _software.dicUnits[_software.software_id] = [_software2]

            self._load_development_questions(_software)
            self._load_srr_questions(_software)
            self._load_pdr_questions(_software)
            self._load_cdr_questions(_software)
            self._load_trr_questions(_software)
            self._load_test_matrix(_software)

        return(_results, _error_code)

    def _load_development_questions(self, software):
        """
        Method to retrieve the Development Environment Risk Analysis answers
        from the RTK database and load the Software data model list.

        :param software: the :py:class:`rtk.software.Software` data model to
                         load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _query = "SELECT fld_y FROM rtk_software_development \
                  WHERE fld_software_id={0:d}".format(software.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_questions = len(_results)
        except TypeError:
            _n_questions = 0

        for i in range(_n_questions):
            software.lst_development[i] = _results[i][0]

        return False

    def _load_srr_questions(self, software):
        """
        Method to retrieve the Requirements Review Risk Analysis answers
        from the RTK database and load the Software data model list.

        :param software: the :py:class:`rtk.software.Software` data model to
                         load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _query = "SELECT fld_y, fld_value FROM rtk_srr_ssr \
                  WHERE fld_software_id={0:d}".format(software.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_questions = len(_results)
        except TypeError:
            _n_questions = 0

        for i in range(_n_questions):
            if i in [0, 1, 2, 3, 5, 6]:
                software.lst_anomaly_mgmt[0][i] = _results[i][1]
            elif i in [4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                       21]:
                software.lst_anomaly_mgmt[0][i] = _results[i][0]

            software.lst_traceability[0][0] = _results[22][0]

            if i in [31, 32, 33, 34]:
                software.lst_sftw_quality[0][i - 23] = _results[i][1]
            elif i in [23, 24, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40,
                       41, 42, 43, 44, 45, 46, 47, 48, 49]:
                software.lst_sftw_quality[0][i - 23] = _results[i][0]

        return False

    def _load_pdr_questions(self, software):
        """
        Method to retrieve the Preliminary Design Review Risk Analysis answers
        from the RTK database and load the Software data model list.

        :param software: the :py:class:`rtk.software.Software` data model to
                         load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _query = "SELECT fld_y, fld_value FROM rtk_pdr \
                  WHERE fld_software_id={0:d}".format(software.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_questions = len(_results)
        except TypeError:
            _n_questions = 0

        for i in range(_n_questions):
            if i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                software.lst_anomaly_mgmt[1][i] = _results[i][0]

            software.lst_traceability[1][0] = _results[14][0]

            if i in [17, 18, 21, 22, 23, 24, 25, 26]:
                software.lst_sftw_quality[1][i - 15] = _results[i][1]
            elif i in [15, 16, 19, 20, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]:
                software.lst_sftw_quality[1][i - 15] = _results[i][0]

        return False

    def _load_cdr_questions(self, software):
        """
        Method to retrieve the Critical Design Review Risk Analysis answers
        from the RTK database and load the Software data model list.

        :param software: the :py:class:`rtk.software.Software` data model to
                         load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _query = "SELECT fld_y, fld_value FROM rtk_cdr \
                  WHERE fld_software_id={0:d}".format(software.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_questions = len(_results)
        except TypeError:
            _n_questions = 0

        if software.level_id == 1:          # System
            _am_check = []
            _am_value = []
            _tr_check = []
            _qc_check = []
            _qc_value = []
        elif software.level_id == 2:        # CSCI
            _am_check = [2, 3, 4, 5, 6, 8, 9, 10]
            _am_value = [0, 1, 7]
            _tr_check = [11, 12]
            _qc_check = []
            _qc_value = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                         26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
        elif software.level_id == 3:        # Unit
            _am_check = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            _am_value = []
            _tr_check = [10]
            _qc_check = [13, 16, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34]
            _qc_value = [11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 25, 26]

        for i in range(_n_questions):
            if i in _am_check:
                software.lst_anomaly_mgmt[2][i] = _results[i][0]
            elif i in _am_value:
                software.lst_anomaly_mgmt[2][i] = _results[i][1]

            if i in _tr_check:
                if software.level_id == 2:      # CSCI
                    software.lst_traceability[2][i - 11] = _results[i][0]
                elif software.level_id == 3:    # Unit
                    software.lst_traceability[2][i - 10] = _results[i][0]

            if i in _qc_value:
                if software.level_id == 2:
                    software.lst_sftw_quality[2][i - 13] = _results[i][1]
                elif software.level_id == 3:
                    software.lst_sftw_quality[2][i - 11] = _results[i][1]
            elif i in _qc_check:
                if software.level_id == 2:
                    software.lst_sftw_quality[2][i - 13] = _results[i][0]
                elif software.level_id == 3:
                    software.lst_sftw_quality[2][i - 11] = _results[i][0]

        return False

    def _load_trr_questions(self, software):
        """
        Method to retrieve the Test Readiness Review Risk Analysis answers
        from the RTK database and load the Software data model list.

        :param software: the :py:class:`rtk.software.Software` data model to
                         load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _query = "SELECT fld_y, fld_value FROM rtk_trr \
                  WHERE fld_software_id={0:d}".format(software.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_questions = len(_results)
        except TypeError:
            _n_questions = 0

        if software.level_id == 1:          # System
            _am_check = []
            _qc_check = []
            _lt_value = []
        elif software.level_id == 2:        # CSCI
            _am_check = []
            _qc_check = []
            _lt_value = [0, 1, 2, 3]
        elif software.level_id == 3:        # Unit
            _am_check = [3, 4]
            _qc_check = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
            _lt_value = [0, 1, 2]

        for i in range(_n_questions):
            if i in _lt_value:
                software.lst_modularity[i] = _results[i][1]

            if i in _am_check:
                software.lst_anomaly_mgmt[3][i - 3] = _results[i][1]

            if i in _qc_check:
                software.lst_sftw_quality[3][i - 5] = _results[i][0]

        return False

    def _load_test_matrix(self, software):
        """
        Method to retrieve the Test Matrix from the RTK database and load the
        Software data model list.

        :param software: the :py:class:`rtk.software.Software` data model to
                         load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _query = "SELECT fld_technique_id, fld_recommended, fld_used \
                  FROM rtk_software_tests \
                  WHERE fld_software_id={0:d} \
                  ORDER BY fld_technique_id".format(software.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_selections = len(_results)
        except TypeError:
            _n_selections = 0

        for i in range(_n_selections):
            software.lst_test_selection[i][0] = _results[i][1]
            software.lst_test_selection[i][1] = _results[i][2]

        return False

    def add_software(self, revision_id, software_type, parent_id=None):
        """
        Adds a new Software item to the RTK Project for the selected Revision.

        :param int revision_id: the Revision ID to add the new Software
                                item(s).
        :param int software_type: the type of Software item to add.
                                  * 1 = CSCI
                                  * 2 = Unit
        :keyword int parent_id: the Software ID of the parent software item.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # By default we add the new Software item as an immediate child of the
        # top-level assembly.
        if parent_id is None:
# TODO: Replace this with an RTK error or warning dialog and then return.
            parent_id = 0

        if software_type == 1:
            _description = 'CSCI'
        elif software_type == 2:
            _description = 'Unit'

        _query = "INSERT INTO rtk_software \
                  (fld_revision_id, fld_description, fld_parent_id, \
                   fld_level_id) \
                  VALUES({0:d}, '{1:s}', {2:d}, {3:d})".format(revision_id,
                                                               _description,
                                                               parent_id,
                                                               software_type + 1)
        (_results, _error_code, _software_id) = self._dao.execute(_query,
                                                                  commit=True)

        # If the new software item was added successfully to the RTK Project
        # database, add a record to the development environment risk analysis
        # table in the RTK Project database.
        if _results:
            for i in range(43):
                _query = "INSERT INTO rtk_software_development \
                          (fld_software_id, fld_question_id) \
                          VALUES({0:d}, {1:d})".format(_software_id, i)
                (_results,
                 _error_code, _) = self._dao.execute(_query, commit=True)

        # If the record was successfully added to the development environment
        # table, add a record to the requirements review table.
        if _results:
            for i in range(50):
                _query = "INSERT INTO rtk_srr_ssr \
                          (fld_software_id, fld_question_id) \
                          VALUES({0:d}, {1:d})".format(_software_id, i)
                (_results,
                 _error_code, _) = self._dao.execute(_query, commit=True)

        # If the record was successfully added to the requirements review
        # table, add a record to the preliminary design review table.
        if _results:
            for i in range(39):
                _query = "INSERT INTO rtk_pdr \
                          (fld_software_id, fld_question_id) \
                          VALUES({0:d}, {1:d})".format(_software_id, i)
                (_results,
                 _error_code, _) = self._dao.execute(_query, commit=True)

        # If the record was successfully added to the preliminary design review
        # table, add a record to the critical design review table.
        if _results:
            for i in range(72):
                _query = "INSERT INTO rtk_cdr \
                          (fld_software_id, fld_question_id) \
                          VALUES({0:d}, {1:d})".format(_software_id, i)
                (_results,
                 _error_code, _) = self._dao.execute(_query, commit=True)

        # If the record was successfully added to the critical design review
        # table, add a record to the test readiness review table.
        if _results:
            for i in range(24):
                _query = "INSERT INTO rtk_trr \
                          (fld_software_id, fld_question_id) \
                          VALUES({0:d}, {1:d})".format(_software_id, i)
                (_results,
                 _error_code, _) = self._dao.execute(_query, commit=True)

        # If the record was successfully added to the test readiness review
        # table, add a record to the test planning table.
        if _results:
            for i in range(21):
                _query = "INSERT INTO rtk_software_tests \
                          (fld_software_id, fld_technique_id) \
                          VALUES({0:d}, {1:d})".format(_software_id, i)
                (_results,
                 _error_code, _) = self._dao.execute(_query, commit=True)

        # If the new software item was added successfully to all the tables in
        # the RTK Project database:
        #   1. Retrieve the ID of the newly inserted software item.
        #   2. Create a new Assembly or Component data model instance.
        #   3. Set the attributes of the new Assembly or Component data model
        #      instance.
        #   4. Add the new Assembly or Component model to the controller
        #      dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_software')[0]
            if software_type == 1:
                _software = CSCI()
            elif software_type == 2:
                _software = Unit()
            _software.set_attributes((revision_id, self._last_id,
                                      software_type, _description, 0, 0, 0.0,
                                      0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0.0,
                                      0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      parent_id, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0,
                                      0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0,
                                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0,
                                      0))
            self.dicSoftware[_software.software_id] = _software

        return(_software, _error_code)

    def delete_software(self, software_id):
        """
        Deletes a Software item from the RTK Project.

        :param int software_id: the Software ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Delete all the child software, if any.
        _query = "DELETE FROM rtk_software \
                  WHERE fld_parent_id={0:d}".format(software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Then delete the parent software.
        _query = "DELETE FROM rtk_software \
                  WHERE fld_software_id={0:d}".format(software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        self.dicSoftware.pop(software_id)

        return(_results, _error_code)

    def save_software_item(self, software_id):
        """
        Saves the Software CSCI or Software Unit attributes to the RTK Project
        database.

        :param int software_id: the ID of the software to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _software = self.dicSoftware[software_id]

        # Save the Software model.
        _query = "UPDATE rtk_software \
                  SET fld_description='{0:s}', fld_application_id={1:d}, \
                      fld_development_id={2:d}, fld_a={3:f}, fld_do={4:f}, \
                      fld_dd={5:d}, fld_dc={6:f}, fld_d={7:f}, fld_am={8:f}, \
                      fld_sa={9:f}, fld_st={10:f}, fld_dr={11:f}, \
                      fld_sq={12:f}, fld_s1={13:f}, fld_hloc={14:d}, \
                      fld_aloc={15:d}, fld_loc={16:d}, fld_sl={17:f}, \
                      fld_ax={18:d}, fld_bx={19:d}, fld_cx={20:d}, \
                      fld_nm={21:d}, fld_sx={22:f}, fld_um={23:d}, \
                      fld_wm={24:d}, fld_xm={25:d}, fld_sm={26:f}, \
                      fld_df={27:f}, fld_sr={28:f}, fld_s2={29:f}, \
                      fld_rpfom={30:f}, fld_parent_id={31:d}, \
                      fld_dev_assess_type={32:d}, fld_phase_id={33:d}, \
                      fld_tcl={34:d}, fld_test_path={35:d}, \
                      fld_category={36:d}, fld_test_effort={37:d}, \
                      fld_test_approach={38:d}, fld_labor_hours_test={39:f}, \
                      fld_labor_hours_dev={40:f}, fld_budget_test={41:f}, \
                      fld_budget_dev={42:f}, fld_schedule_test={43:f}, \
                      fld_schedule_dev={44:f}, fld_branches={45:d}, \
                      fld_branches_test={46:d}, fld_inputs={47:d}, \
                      fld_inputs_test={48:d}, fld_nm_test={49:d}, \
                      fld_interfaces={50:d}, fld_interfaces_test={51:d}, \
                      fld_te={52:f}, fld_tm={53:f}, fld_tc={54:f}, \
                      fld_t={55:f}, fld_ft1={56:f}, fld_ft2={57:f}, \
                      fld_ren_avg={58:f}, fld_ren_eot={59:f}, fld_ec={60:f}, \
                      fld_ev={61:f}, fld_et={62:f}, fld_os={63:f}, \
                      fld_ew={64:f}, fld_e={65:f}, fld_f={66:f}, \
                      fld_cb={67:d}, fld_ncb={68:d}, fld_dr_test={69:d}, \
                      fld_test_time={70:f}, fld_dr_eot={71:d}, \
                      fld_test_time_eot={72:f}".format(
                          _software.description, _software.application_id,
                          _software.development_id, _software.a_risk,
                          _software.do, _software.dd, _software.dc,
                          _software.d_risk, _software.am, _software.sa,
                          _software.st, _software.dr, _software.sq,
                          _software.s1, _software.hloc, _software.aloc,
                          _software.sloc, _software.sl, _software.ax,
                          _software.bx, _software.cx, _software.nm,
                          _software.sx, _software.um, _software.wm,
                          _software.xm, _software.sm, _software.df,
                          _software.sr, _software.s2, _software.rpfom,
                          _software.parent_id, _software.dev_assess_type,
                          _software.phase_id, _software.tcl,
                          _software.test_path, _software.category,
                          _software.test_effort, _software.test_approach,
                          _software.labor_hours_test,
                          _software.labor_hours_dev, _software.budget_test,
                          _software.budget_dev, _software.schedule_test,
                          _software.schedule_dev, _software.branches,
                          _software.branches_test, _software.inputs,
                          _software.inputs_test, _software.nm_test,
                          _software.interfaces, _software.interfaces_test,
                          _software.te, _software.tm, _software.tc,
                          _software.t_risk, _software.ft1, _software.ft2,
                          _software.ren_avg, _software.ren_eot, _software.ec,
                          _software.ev, _software.et, _software.os,
                          _software.ew, _software.e_risk,
                          _software.failure_rate, _software.cb, _software.ncb,
                          _software.dr_test, _software.test_time,
                          _software.dr_eot, _software.test_time_eot)

        _query = _query + " WHERE fld_revision_id={0:d} \
                            AND fld_software_id={1:d}".format(
                                _software.revision_id, software_id)

        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

# TODO: Handle errors.
        return (_results, _error_code)

    def save_bom(self):
        """
        Saves all Assembly and Component data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _software in self.dicSoftware.values():
            (_results,
             _error_code) = self.save_software_item(_software.software_id)

        return False

    def save_development_risk(self, software_id):
        """
        Method to save the Development Environment risk analysis answers to the
        open RTK database.

        :param int software_id: the ID of the software item to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _sftwr = self.dicSoftware[software_id]

        # Save the risk analysis answers.
        _query = "UPDATE rtk_software_development \
                  SET fld_y=CASE fld_question_id \
                        WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} WHEN 2 THEN {2:d} \
                        WHEN 3 THEN {3:d} WHEN 4 THEN {4:d} WHEN 5 THEN {5:d} \
                        WHEN 6 THEN {6:d} WHEN 7 THEN {7:d} WHEN 8 THEN {8:d} \
                        WHEN 9 THEN {9:d} WHEN 10 THEN {10:d} \
                        WHEN 11 THEN {11:d} WHEN 12 THEN {12:d} \
                        WHEN 13 THEN {13:d} WHEN 14 THEN {14:d} \
                        WHEN 15 THEN {15:d} WHEN 16 THEN {16:d} \
                        WHEN 17 THEN {17:d} WHEN 18 THEN {18:d} \
                        WHEN 19 THEN {19:d} WHEN 20 THEN {20:d} \
                        WHEN 21 THEN {21:d} WHEN 22 THEN {22:d} \
                        WHEN 23 THEN {23:d} WHEN 24 THEN {24:d} \
                        WHEN 25 THEN {25:d} WHEN 26 THEN {26:d} \
                        WHEN 27 THEN {27:d} WHEN 28 THEN {28:d} \
                        WHEN 29 THEN {29:d} WHEN 30 THEN {30:d} \
                        WHEN 31 THEN {31:d} WHEN 32 THEN {32:d} \
                        WHEN 33 THEN {33:d} WHEN 34 THEN {34:d} \
                        WHEN 35 THEN {35:d} WHEN 36 THEN {36:d} \
                        WHEN 37 THEN {37:d} WHEN 38 THEN {38:d} \
                        WHEN 39 THEN {39:d} WHEN 40 THEN {40:d} \
                        WHEN 41 THEN {41:d} WHEN 42 THEN {42:d} \
                    END \
                  WHERE fld_question_id IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, \
                                            11, 12, 13, 14, 15, 16, 17, 18, \
                                            19, 20, 21, 22, 23, 24, 25, 26, \
                                            27, 28, 29, 30, 31, 32, 33, 34, \
                                            35, 36, 37, 38, 39, 40, 41, 42) \
                  AND fld_software_id={43:d}".format(
                      _sftwr.lst_development[0], _sftwr.lst_development[1],
                      _sftwr.lst_development[2], _sftwr.lst_development[3],
                      _sftwr.lst_development[4], _sftwr.lst_development[5],
                      _sftwr.lst_development[6], _sftwr.lst_development[7],
                      _sftwr.lst_development[8], _sftwr.lst_development[9],
                      _sftwr.lst_development[10], _sftwr.lst_development[11],
                      _sftwr.lst_development[12], _sftwr.lst_development[13],
                      _sftwr.lst_development[14], _sftwr.lst_development[15],
                      _sftwr.lst_development[16], _sftwr.lst_development[17],
                      _sftwr.lst_development[18], _sftwr.lst_development[19],
                      _sftwr.lst_development[20], _sftwr.lst_development[21],
                      _sftwr.lst_development[22], _sftwr.lst_development[23],
                      _sftwr.lst_development[24], _sftwr.lst_development[25],
                      _sftwr.lst_development[26], _sftwr.lst_development[27],
                      _sftwr.lst_development[28], _sftwr.lst_development[29],
                      _sftwr.lst_development[30], _sftwr.lst_development[31],
                      _sftwr.lst_development[32], _sftwr.lst_development[33],
                      _sftwr.lst_development[34], _sftwr.lst_development[35],
                      _sftwr.lst_development[36], _sftwr.lst_development[37],
                      _sftwr.lst_development[38], _sftwr.lst_development[39],
                      _sftwr.lst_development[40], _sftwr.lst_development[41],
                      _sftwr.lst_development[42], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

# TODO: Handle errors.
        return (_results, _error_code)

    def save_srr_risk(self, software_id):
        """
        Method to save the Requirements Review risk analysis answers to the
        open RTK database.

        :param int software_id: the ID of the software item to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _sftwr = self.dicSoftware[software_id]

        _query = "UPDATE rtk_srr_ssr \
                  SET fld_y=CASE fld_question_id \
                        WHEN 4 THEN {0:d} WHEN 7 THEN {1:d} WHEN 8 THEN {2:d} \
                        WHEN 9 THEN {3:d} WHEN 10 THEN {4:d} \
                        WHEN 11 THEN {5:d} WHEN 12 THEN {6:d} \
                        WHEN 13 THEN {7:d} WHEN 14 THEN {8:d} \
                        WHEN 15 THEN {9:d} WHEN 16 THEN {10:d} \
                        WHEN 17 THEN {11:d} WHEN 18 THEN {12:d} \
                        WHEN 19 THEN {13:d} WHEN 20 THEN {14:d} \
                        WHEN 21 THEN {15:d} \
                    END \
                  WHERE fld_question_id IN (4, 7, 8, 9, 10, 11, 12, 13, 14, \
                                            15, 16, 17, 18, 19, 20, 21) \
                  AND fld_software_id={16:d}".format(
                      _sftwr.lst_anomaly_mgmt[0][4],
                      _sftwr.lst_anomaly_mgmt[0][7],
                      _sftwr.lst_anomaly_mgmt[0][8],
                      _sftwr.lst_anomaly_mgmt[0][9],
                      _sftwr.lst_anomaly_mgmt[0][10],
                      _sftwr.lst_anomaly_mgmt[0][11],
                      _sftwr.lst_anomaly_mgmt[0][12],
                      _sftwr.lst_anomaly_mgmt[0][13],
                      _sftwr.lst_anomaly_mgmt[0][14],
                      _sftwr.lst_anomaly_mgmt[0][15],
                      _sftwr.lst_anomaly_mgmt[0][16],
                      _sftwr.lst_anomaly_mgmt[0][17],
                      _sftwr.lst_anomaly_mgmt[0][18],
                      _sftwr.lst_anomaly_mgmt[0][19],
                      _sftwr.lst_anomaly_mgmt[0][20],
                      _sftwr.lst_anomaly_mgmt[0][21], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        _query = "UPDATE rtk_srr_ssr \
                  SET fld_value=CASE fld_question_id \
                        WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} WHEN 2 THEN {2:d} \
                        WHEN 3 THEN {3:d} WHEN 5 THEN {4:d} WHEN 6 THEN {5:d} \
                    END \
                  WHERE fld_question_id IN (0, 1, 2, 3, 5, 6) \
                  AND fld_software_id={6:d}".format(
                      _sftwr.lst_anomaly_mgmt[0][0],
                      _sftwr.lst_anomaly_mgmt[0][1],
                      _sftwr.lst_anomaly_mgmt[0][2],
                      _sftwr.lst_anomaly_mgmt[0][3],
                      _sftwr.lst_anomaly_mgmt[0][5],
                      _sftwr.lst_anomaly_mgmt[0][6], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        _query = "UPDATE rtk_srr_ssr \
                  SET fld_y={0:d} \
                  WHERE fld_software_id={1:d} \
                  AND fld_question_id=22".format(
                      _sftwr.lst_traceability[0][0], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        _query = "UPDATE rtk_srr_ssr \
                  SET fld_y=CASE fld_question_id \
                        WHEN 23 THEN {0:d} WHEN 24 THEN {1:d} \
                        WHEN 25 THEN {2:d} WHEN 26 THEN {3:d} \
                        WHEN 27 THEN {4:d} WHEN 28 THEN {5:d} \
                        WHEN 29 THEN {6:d} WHEN 30 THEN {7:d} \
                        WHEN 35 THEN {8:d} WHEN 36 THEN {9:d} \
                        WHEN 37 THEN {10:d} WHEN 38 THEN {11:d} \
                        WHEN 39 THEN {12:d} WHEN 40 THEN {13:d} \
                        WHEN 41 THEN {14:d} WHEN 42 THEN {15:d} \
                        WHEN 43 THEN {16:d} WHEN 44 THEN {17:d} \
                        WHEN 45 THEN {18:d} WHEN 46 THEN {19:d} \
                        WHEN 47 THEN {20:d} WHEN 48 THEN {21:d} \
                        WHEN 49 THEN {22:d} \
                    END \
                  WHERE fld_question_id IN (23, 24, 25, 26, 27, 28, 29, 30, \
                                            35, 36, 37, 38, 39, 40, 41, 42, \
                                            43, 44, 45, 46, 47, 48, 49) \
                  AND fld_software_id={23:d}".format(
                      _sftwr.lst_sftw_quality[0][0],
                      _sftwr.lst_sftw_quality[0][1],
                      _sftwr.lst_sftw_quality[0][2],
                      _sftwr.lst_sftw_quality[0][3],
                      _sftwr.lst_sftw_quality[0][4],
                      _sftwr.lst_sftw_quality[0][5],
                      _sftwr.lst_sftw_quality[0][6],
                      _sftwr.lst_sftw_quality[0][7],
                      _sftwr.lst_sftw_quality[0][12],
                      _sftwr.lst_sftw_quality[0][13],
                      _sftwr.lst_sftw_quality[0][14],
                      _sftwr.lst_sftw_quality[0][15],
                      _sftwr.lst_sftw_quality[0][16],
                      _sftwr.lst_sftw_quality[0][17],
                      _sftwr.lst_sftw_quality[0][18],
                      _sftwr.lst_sftw_quality[0][19],
                      _sftwr.lst_sftw_quality[0][20],
                      _sftwr.lst_sftw_quality[0][21],
                      _sftwr.lst_sftw_quality[0][22],
                      _sftwr.lst_sftw_quality[0][23],
                      _sftwr.lst_sftw_quality[0][24],
                      _sftwr.lst_sftw_quality[0][25],
                      _sftwr.lst_sftw_quality[0][26], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        _query = "UPDATE rtk_srr_ssr \
                  SET fld_value=CASE fld_question_id \
                        WHEN 31 THEN {0:d} WHEN 32 THEN {1:d} \
                        WHEN 33 THEN {2:d} WHEN 34 THEN {3:d} \
                    END \
                  WHERE fld_question_id IN (31, 32, 33, 34) \
                  AND fld_software_id={4:d}".format(
                      _sftwr.lst_sftw_quality[0][8],
                      _sftwr.lst_sftw_quality[0][9],
                      _sftwr.lst_sftw_quality[0][10],
                      _sftwr.lst_sftw_quality[0][11], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

# TODO: Handle errors.
        return (_results, _error_code)

    def save_pdr_risk(self, software_id):
        """
        Method to save the Preliminary Design Review risk analysis answers to
        the open RTK database.

        :param int software_id: the ID of the software item to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _sftwr = self.dicSoftware[software_id]

        # Save the risk analysis answers.
        _query = "UPDATE rtk_pdr \
                  SET fld_y=CASE fld_question_id \
                        WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} WHEN 2 THEN {2:d} \
                        WHEN 3 THEN {3:d} WHEN 4 THEN {4:d} WHEN 5 THEN {5:d} \
                        WHEN 6 THEN {6:d} WHEN 7 THEN {7:d} WHEN 8 THEN {8:d} \
                        WHEN 9 THEN {9:d} WHEN 10 THEN {10:d} \
                        WHEN 11 THEN {11:d} WHEN 12 THEN {12:d} \
                        WHEN 13 THEN {13:d} WHEN 14 THEN {14:d} \
                        WHEN 15 THEN {15:d} WHEN 16 THEN {16:d} \
                        WHEN 17 THEN {17:d} WHEN 18 THEN {18:d} \
                        WHEN 19 THEN {19:d} WHEN 20 THEN {20:d} \
                        WHEN 21 THEN {21:d} WHEN 22 THEN {22:d} \
                        WHEN 23 THEN {23:d} WHEN 24 THEN {24:d} \
                        WHEN 25 THEN {25:d} WHEN 26 THEN {26:d} \
                        WHEN 27 THEN {27:d} WHEN 28 THEN {28:d} \
                    END \
                  WHERE fld_question_id IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, \
                                            11, 12, 13, 14, 15, 16, 17, 18, \
                                            19, 20, 21, 22, 23, 24, 25, 26, \
                                            27, 28) \
                  AND fld_software_id={29:d}".format(
                      _sftwr.lst_anomaly_mgmt[1][0],
                      _sftwr.lst_anomaly_mgmt[1][1],
                      _sftwr.lst_anomaly_mgmt[1][2],
                      _sftwr.lst_anomaly_mgmt[1][3],
                      _sftwr.lst_anomaly_mgmt[1][4],
                      _sftwr.lst_anomaly_mgmt[1][5],
                      _sftwr.lst_anomaly_mgmt[1][6],
                      _sftwr.lst_anomaly_mgmt[1][7],
                      _sftwr.lst_anomaly_mgmt[1][8],
                      _sftwr.lst_anomaly_mgmt[1][9],
                      _sftwr.lst_anomaly_mgmt[1][10],
                      _sftwr.lst_anomaly_mgmt[1][11],
                      _sftwr.lst_anomaly_mgmt[1][12],
                      _sftwr.lst_anomaly_mgmt[1][13],
                      _sftwr.lst_traceability[1][0],
                      _sftwr.lst_sftw_quality[1][0],
                      _sftwr.lst_sftw_quality[1][1],
                      _sftwr.lst_sftw_quality[1][4],
                      _sftwr.lst_sftw_quality[1][5],
                      _sftwr.lst_sftw_quality[1][12],
                      _sftwr.lst_sftw_quality[1][13],
                      _sftwr.lst_sftw_quality[1][16],
                      _sftwr.lst_sftw_quality[1][17],
                      _sftwr.lst_sftw_quality[1][18],
                      _sftwr.lst_sftw_quality[1][19],
                      _sftwr.lst_sftw_quality[1][20],
                      _sftwr.lst_sftw_quality[1][21],
                      _sftwr.lst_sftw_quality[1][22],
                      _sftwr.lst_sftw_quality[1][23], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        _query = "UPDATE rtk_pdr \
                  SET fld_value=CASE fld_question_id \
                        WHEN 17 THEN {0:d} WHEN 18 THEN {1:d} \
                        WHEN 21 THEN {2:d} WHEN 22 THEN {3:d} \
                        WHEN 23 THEN {4:d} WHEN 24 THEN {5:d} \
                        WHEN 25 THEN {6:d} WHEN 26 THEN {7:d} \
                        WHEN 29 THEN {8:d} WHEN 30 THEN {9:d} \
                    END \
                  WHERE fld_question_id IN (17, 18, 21, 22, 23, 24, 25, 26, \
                                            29, 30) \
                  AND fld_software_id={10:d}".format(
                      _sftwr.lst_sftw_quality[1][2],
                      _sftwr.lst_sftw_quality[1][3],
                      _sftwr.lst_sftw_quality[1][6],
                      _sftwr.lst_sftw_quality[1][7],
                      _sftwr.lst_sftw_quality[1][8],
                      _sftwr.lst_sftw_quality[1][9],
                      _sftwr.lst_sftw_quality[1][10],
                      _sftwr.lst_sftw_quality[1][11],
                      _sftwr.lst_sftw_quality[1][14],
                      _sftwr.lst_sftw_quality[1][15], _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

# TODO: Handle errors.
        return (_results, _error_code)

    def save_cdr_risk(self, software_id):
        """
        Method to save the Critical Design Review risk analysis answers to the
        open RTK database.

        :param int software_id: the ID of the software item to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _sftwr = self.dicSoftware[software_id]

        # Build the queries to save the risk analysis answers.
        if _sftwr.level_id == 2:            # CSCI
            _query0 = "UPDATE rtk_cdr \
                       SET fld_y=CASE fld_question_id \
                             WHEN 2 THEN {0:d} WHEN 3 THEN {1:d} \
                             WHEN 4 THEN {2:d} WHEN 5 THEN {3:d} \
                             WHEN 6 THEN {4:d} WHEN 8 THEN {5:d} \
                             WHEN 9 THEN {6:d} WHEN 10 THEN {7:d} \
                             WHEN 11 THEN {8:d} WHEN 12 THEN {9:d} \
                         END \
                       WHERE fld_question_id IN (2, 3, 4, 5, 6, 8, 9, 10, 11, \
                                                 12) \
                       AND fld_software_id={10:d}".format(
                           _sftwr.lst_anomaly_mgmt[2][2],
                           _sftwr.lst_anomaly_mgmt[2][3],
                           _sftwr.lst_anomaly_mgmt[2][4],
                           _sftwr.lst_anomaly_mgmt[2][5],
                           _sftwr.lst_anomaly_mgmt[2][6],
                           _sftwr.lst_anomaly_mgmt[2][8],
                           _sftwr.lst_anomaly_mgmt[2][9],
                           _sftwr.lst_anomaly_mgmt[2][10],
                           _sftwr.lst_traceability[2][0],
                           _sftwr.lst_traceability[2][1], _sftwr.software_id)

            _query1 = "UPDATE rtk_cdr \
                       SET fld_value=CASE fld_question_id \
                             WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} \
                             WHEN 7 THEN {2:d} WHEN 13 THEN {3:d} \
                             WHEN 14 THEN {4:d} WHEN 15 THEN {5:d} \
                             WHEN 16 THEN {6:d} WHEN 17 THEN {7:d} \
                             WHEN 18 THEN {8:d} WHEN 19 THEN {9:d} \
                             WHEN 20 THEN {10:d} WHEN 21 THEN {11:d} \
                             WHEN 22 THEN {12:d} WHEN 23 THEN {13:d} \
                             WHEN 24 THEN {14:d} WHEN 25 THEN {15:d} \
                             WHEN 26 THEN {16:d} WHEN 27 THEN {17:d} \
                             WHEN 28 THEN {18:d} WHEN 29 THEN {19:d} \
                             WHEN 30 THEN {20:d} WHEN 31 THEN {21:d} \
                             WHEN 32 THEN {22:d} WHEN 33 THEN {23:d} \
                             WHEN 34 THEN {24:d} WHEN 35 THEN {25:d} \
                             WHEN 36 THEN {26:d} \
                         END \
                       WHERE fld_question_id IN (0, 1, 7, 13, 14, 15, 16, 17, \
                                                 18, 19, 20, 21, 22, 23, 24, \
                                                 25, 26, 27, 28, 29, 30, 31, \
                                                 32, 33, 34, 35, 36) \
                       AND fld_software_id={27:d}".format(
                           _sftwr.lst_anomaly_mgmt[2][0],
                           _sftwr.lst_anomaly_mgmt[2][1],
                           _sftwr.lst_anomaly_mgmt[2][7],
                           _sftwr.lst_sftw_quality[2][0],
                           _sftwr.lst_sftw_quality[2][1],
                           _sftwr.lst_sftw_quality[2][2],
                           _sftwr.lst_sftw_quality[2][3],
                           _sftwr.lst_sftw_quality[2][4],
                           _sftwr.lst_sftw_quality[2][5],
                           _sftwr.lst_sftw_quality[2][6],
                           _sftwr.lst_sftw_quality[2][7],
                           _sftwr.lst_sftw_quality[2][8],
                           _sftwr.lst_sftw_quality[2][9],
                           _sftwr.lst_sftw_quality[2][10],
                           _sftwr.lst_sftw_quality[2][11],
                           _sftwr.lst_sftw_quality[2][12],
                           _sftwr.lst_sftw_quality[2][13],
                           _sftwr.lst_sftw_quality[2][14],
                           _sftwr.lst_sftw_quality[2][15],
                           _sftwr.lst_sftw_quality[2][16],
                           _sftwr.lst_sftw_quality[2][17],
                           _sftwr.lst_sftw_quality[2][18],
                           _sftwr.lst_sftw_quality[2][19],
                           _sftwr.lst_sftw_quality[2][20],
                           _sftwr.lst_sftw_quality[2][21],
                           _sftwr.lst_sftw_quality[2][22],
                           _sftwr.lst_sftw_quality[2][23], _sftwr.software_id)
        elif _sftwr.level_id == 3:          # Unit
            _query0 = "UPDATE rtk_cdr \
                       SET fld_y=CASE fld_question_id \
                             WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} \
                             WHEN 2 THEN {2:d} WHEN 3 THEN {3:d} \
                             WHEN 4 THEN {4:d} WHEN 5 THEN {5:d} \
                             WHEN 6 THEN {6:d} WHEN 7 THEN {7:d} \
                             WHEN 8 THEN {8:d} WHEN 9 THEN {9:d} \
                             WHEN 10 THEN {10:d} WHEN 13 THEN {11:d} \
                             WHEN 16 THEN {12:d} WHEN 23 THEN {13:d} \
                             WHEN 24 THEN {14:d} WHEN 27 THEN {15:d} \
                             WHEN 28 THEN {16:d} WHEN 29 THEN {17:d} \
                             WHEN 30 THEN {18:d} WHEN 31 THEN {19:d} \
                             WHEN 32 THEN {20:d} WHEN 33 THEN {21:d} \
                             WHEN 34 THEN {22:d} \
                         END \
                       WHERE fld_question_id IN (0, 1, 2, 3, 4, 5, 6, 7, 8, \
                                                 9, 10, 13, 16, 23, 24, 27, \
                                                 28, 29, 30, 31, 32, 33, 34) \
                       AND fld_software_id={23:d}".format(
                           _sftwr.lst_anomaly_mgmt[2][0],
                           _sftwr.lst_anomaly_mgmt[2][1],
                           _sftwr.lst_anomaly_mgmt[2][2],
                           _sftwr.lst_anomaly_mgmt[2][3],
                           _sftwr.lst_anomaly_mgmt[2][4],
                           _sftwr.lst_anomaly_mgmt[2][5],
                           _sftwr.lst_anomaly_mgmt[2][6],
                           _sftwr.lst_anomaly_mgmt[2][7],
                           _sftwr.lst_anomaly_mgmt[2][8],
                           _sftwr.lst_anomaly_mgmt[2][9],
                           _sftwr.lst_traceability[2][0],
                           _sftwr.lst_sftw_quality[2][2],
                           _sftwr.lst_sftw_quality[2][5],
                           _sftwr.lst_sftw_quality[2][12],
                           _sftwr.lst_sftw_quality[2][13],
                           _sftwr.lst_sftw_quality[2][16],
                           _sftwr.lst_sftw_quality[2][17],
                           _sftwr.lst_sftw_quality[2][18],
                           _sftwr.lst_sftw_quality[2][19],
                           _sftwr.lst_sftw_quality[2][20],
                           _sftwr.lst_sftw_quality[2][21],
                           _sftwr.lst_sftw_quality[2][22],
                           _sftwr.lst_sftw_quality[2][23], _sftwr.software_id)

            _query1 = "UPDATE rtk_cdr \
                       SET fld_value=CASE fld_question_id \
                             WHEN 11 THEN {0:d} WHEN 12 THEN {1:d} \
                             WHEN 14 THEN {2:d} WHEN 15 THEN {3:d} \
                             WHEN 17 THEN {4:d} WHEN 18 THEN {5:d} \
                             WHEN 19 THEN {6:d} WHEN 20 THEN {7:d} \
                             WHEN 21 THEN {8:d} WHEN 22 THEN {9:d} \
                             WHEN 25 THEN {10:d} WHEN 26 THEN {11:d} \
                         END \
                       WHERE fld_question_id IN (11, 12, 14, 15, 17, 18, 19, \
                                                 20, 21, 22, 25, 26) \
                       AND fld_software_id={12:d}".format(
                           _sftwr.lst_sftw_quality[2][0],
                           _sftwr.lst_sftw_quality[2][1],
                           _sftwr.lst_sftw_quality[2][3],
                           _sftwr.lst_sftw_quality[2][4],
                           _sftwr.lst_sftw_quality[2][6],
                           _sftwr.lst_sftw_quality[2][7],
                           _sftwr.lst_sftw_quality[2][8],
                           _sftwr.lst_sftw_quality[2][9],
                           _sftwr.lst_sftw_quality[2][10],
                           _sftwr.lst_sftw_quality[2][11],
                           _sftwr.lst_sftw_quality[2][14],
                           _sftwr.lst_sftw_quality[2][15], _sftwr.software_id)

        # Execute each query.
        (_results, _error_code, __) = self._dao.execute(_query0, commit=True)
        (_results, _error_code, __) = self._dao.execute(_query1, commit=True)

# TODO: Handle errors.
        return (_results, _error_code)

    def save_trr_risk(self, software_id):
        """
        Method to save the Test Readiness Review risk analysis answers to the
        open RTK database.

        :param int software_id: the ID of the software item to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _sftwr = self.dicSoftware[software_id]

        # Build the queries to save the risk analysis answers.
        if _sftwr.level_id == 2:            # CSCI
            _query1 = "UPDATE rtk_trr \
                       SET fld_value=CASE fld_question_id \
                             WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} \
                             WHEN 2 THEN {2:d} WHEN 3 THEN {3:d} \
                         END \
                       WHERE fld_question_id IN (0, 1, 2, 3) \
                       AND fld_software_id={4:d}".format(
                           _sftwr.lst_modularity[0], _sftwr.lst_modularity[1],
                           _sftwr.lst_modularity[2], _sftwr.lst_modularity[3],
                           _sftwr.software_id)

        elif _sftwr.level_id == 3:          # Unit
            _query0 = "UPDATE rtk_trr \
                       SET fld_y=CASE fld_question_id \
                             WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} \
                             WHEN 2 THEN {2:d} \
                         END \
                       WHERE fld_question_id IN (0, 1, 2) \
                       AND fld_software_id={3:d}".format(
                           _sftwr.lst_modularity[0], _sftwr.lst_modularity[1],
                           _sftwr.lst_modularity[2], _sftwr.software_id)
            _query1 = "UPDATE rtk_trr \
                       SET fld_value=CASE fld_question_id \
                             WHEN 3 THEN {0:d} WHEN 4 THEN {1:d} \
                             WHEN 5 THEN {2:d} WHEN 6 THEN {3:d} \
                             WHEN 7 THEN {4:d} WHEN 8 THEN {5:d} \
                             WHEN 9 THEN {6:d} WHEN 10 THEN {7:d} \
                             WHEN 11 THEN {8:d} WHEN 12 THEN {9:d} \
                             WHEN 13 THEN {10:d} WHEN 14 THEN {11:d} \
                             WHEN 15 THEN {12:d} WHEN 16 THEN {13:d} \
                             WHEN 17 THEN {14:d} WHEN 18 THEN {15:d} \
                         END \
                       WHERE fld_question_id IN (3, 4, 5, 6, 7, 8, 9, 10, 11, \
                                                 12, 13, 14, 15, 16, 17, 18) \
                       AND fld_software_id={16:d}".format(
                           _sftwr.lst_anomaly_mgmt[3][0],
                           _sftwr.lst_anomaly_mgmt[3][1],
                           _sftwr.lst_sftw_quality[3][0],
                           _sftwr.lst_sftw_quality[3][1],
                           _sftwr.lst_sftw_quality[3][2],
                           _sftwr.lst_sftw_quality[3][3],
                           _sftwr.lst_sftw_quality[3][4],
                           _sftwr.lst_sftw_quality[3][5],
                           _sftwr.lst_sftw_quality[3][6],
                           _sftwr.lst_sftw_quality[3][7],
                           _sftwr.lst_sftw_quality[3][8],
                           _sftwr.lst_sftw_quality[3][9],
                           _sftwr.lst_sftw_quality[3][10],
                           _sftwr.lst_sftw_quality[3][11],
                           _sftwr.lst_sftw_quality[3][12],
                           _sftwr.lst_sftw_quality[3][13], _sftwr.software_id)
            (_results,
             _error_code, __) = self._dao.execute(_query0, commit=True)

        (_results, _error_code, __) = self._dao.execute(_query1, commit=True)

# TODO: Handle errors.
        return (_results, _error_code)

    def save_test_selections(self, software_id):
        """
        Method to save the Test Selections to the open RTK database.

        :param int software_id: the ID of the software item to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _sftwr = self.dicSoftware[software_id]

        # Build the queries to save the test selection answers.
        _query = "UPDATE rtk_software_tests \
                  SET fld_recommended=CASE fld_technique_id \
                        WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} \
                        WHEN 2 THEN {2:d} WHEN 3 THEN {3:d} \
                        WHEN 4 THEN {4:d} WHEN 5 THEN {5:d} \
                        WHEN 6 THEN {6:d} WHEN 7 THEN {7:d} \
                        WHEN 8 THEN {8:d} WHEN 9 THEN {9:d} \
                        WHEN 10 THEN {10:d} WHEN 11 THEN {11:d} \
                        WHEN 12 THEN {12:d} WHEN 13 THEN {13:d} \
                        WHEN 14 THEN {14:d} WHEN 15 THEN {15:d} \
                        WHEN 16 THEN {16:d} WHEN 17 THEN {17:d} \
                        WHEN 18 THEN {18:d} WHEN 19 THEN {19:d} \
                        WHEN 20 THEN {20:d} \
                  END \
                  WHERE fld_technique_id IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, \
                                             10, 11, 12, 13, 14, 15, 16, 17, \
                                             18, 19, 20) \
                  AND fld_software_id={21:d}".format(
                      _sftwr.lst_test_selection[0][0],
                      _sftwr.lst_test_selection[1][0],
                      _sftwr.lst_test_selection[2][0],
                      _sftwr.lst_test_selection[3][0],
                      _sftwr.lst_test_selection[4][0],
                      _sftwr.lst_test_selection[5][0],
                      _sftwr.lst_test_selection[6][0],
                      _sftwr.lst_test_selection[7][0],
                      _sftwr.lst_test_selection[8][0],
                      _sftwr.lst_test_selection[9][0],
                      _sftwr.lst_test_selection[10][0],
                      _sftwr.lst_test_selection[11][0],
                      _sftwr.lst_test_selection[12][0],
                      _sftwr.lst_test_selection[13][0],
                      _sftwr.lst_test_selection[14][0],
                      _sftwr.lst_test_selection[15][0],
                      _sftwr.lst_test_selection[16][0],
                      _sftwr.lst_test_selection[17][0],
                      _sftwr.lst_test_selection[18][0],
                      _sftwr.lst_test_selection[19][0],
                      _sftwr.lst_test_selection[20][0],
                      _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        _query = "UPDATE rtk_software_tests \
                  SET fld_used=CASE fld_technique_id \
                        WHEN 0 THEN {0:d} WHEN 1 THEN {1:d} \
                        WHEN 2 THEN {2:d} WHEN 3 THEN {3:d} \
                        WHEN 4 THEN {4:d} WHEN 5 THEN {5:d} \
                        WHEN 6 THEN {6:d} WHEN 7 THEN {7:d} \
                        WHEN 8 THEN {8:d} WHEN 9 THEN {9:d} \
                        WHEN 10 THEN {10:d} WHEN 11 THEN {11:d} \
                        WHEN 12 THEN {12:d} WHEN 13 THEN {13:d} \
                        WHEN 14 THEN {14:d} WHEN 15 THEN {15:d} \
                        WHEN 16 THEN {16:d} WHEN 17 THEN {17:d} \
                        WHEN 18 THEN {18:d} WHEN 19 THEN {19:d} \
                        WHEN 20 THEN {20:d} \
                  END \
                  WHERE fld_technique_id IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, \
                                             10, 11, 12, 13, 14, 15, 16, 17, \
                                             18, 19, 20) \
                  AND fld_software_id={21:d}".format(
                      _sftwr.lst_test_selection[0][1],
                      _sftwr.lst_test_selection[1][1],
                      _sftwr.lst_test_selection[2][1],
                      _sftwr.lst_test_selection[3][1],
                      _sftwr.lst_test_selection[4][1],
                      _sftwr.lst_test_selection[5][1],
                      _sftwr.lst_test_selection[6][1],
                      _sftwr.lst_test_selection[7][1],
                      _sftwr.lst_test_selection[8][1],
                      _sftwr.lst_test_selection[9][1],
                      _sftwr.lst_test_selection[10][1],
                      _sftwr.lst_test_selection[11][1],
                      _sftwr.lst_test_selection[12][1],
                      _sftwr.lst_test_selection[13][1],
                      _sftwr.lst_test_selection[14][1],
                      _sftwr.lst_test_selection[15][1],
                      _sftwr.lst_test_selection[16][1],
                      _sftwr.lst_test_selection[17][1],
                      _sftwr.lst_test_selection[18][1],
                      _sftwr.lst_test_selection[19][1],
                      _sftwr.lst_test_selection[20][1],
                      _sftwr.software_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

# TODO: Handle errors.
        return (_results, _error_code)

    def request_calculate(self):
        """
        Requests the Software BoM calculations be performed.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.dicSoftware[0].calculate(self.dicSoftware[0])

        self.save_bom()

        return False
