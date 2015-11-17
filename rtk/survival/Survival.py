#!/usr/bin/env python
"""
############################
Survival Package Data Module
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.survival.Survival.py is part of The RTK Project
#
# All rights reserved.

from collections import OrderedDict

try:
    import analyses.survival.MCF as _mcf
    from analyses.statistics.Distributions import *
    from utilities import error_handler
except ImportError:
    import rtk.analyses.survival.MCF as _mcf
    from rtk.analyses.statistics.Distributions import *
    from rtk.utilities import error_handler


class Model(object):                       # pylint: disable=R0902, R0904
    """
    The Survival data model contains the attributes and methods for an
    Survival. The attributes of an Survival model are:

    :ivar dicRecords: default value: {}
    :ivar _nevada_chart: default value: False
    :ivar scale: default value: [0.0, 0.0, 0.0]
    :ivar shape: default value: [0.0, 0.0, 0.0]
    :ivar location: default value: [0.0, 0.0, 0.0]
    :ivar variance: default value: [0.0, 0.0, 0.0]
    :ivar covariance: default value: [0.0, 0.0, 0.0]
    :ivar revision_id: default value: 0
    :ivar survival_id: default value: 0
    :ivar assembly_id: default value: 0
    :ivar description: default value: ''
    :ivar source: default value: 0
    :ivar distribution_id: default value: 0
    :ivar confidence: default value: 0.75
    :ivar confidence_type: default value: 0
    :ivar confidence_method: default value: 0
    :ivar fit_method: default value: 0
    :ivar rel_time: default value: 100.0
    :ivar n_rel_points: default value: 0
    :ivar n_suspensions: default value: 0
    :ivar n_failures: default value: 0
    :ivar mhb: default value: 0.0
    :ivar lp: default value: 0.0
    :ivar lr: default value: 0.0
    :ivar aic: default value: 0.0
    :ivar bic: default value: 0.0
    :ivar mle: default value: 0.0
    :ivar start_time: default value: 0.0
    :ivar end_time: default value: 0.0
    :ivar start_date: default value: 0
    :ivar end_date: default value: 0
    """

    def __init__(self):
        """
        Method to initialize a Survival data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._nevada_chart = False      # Dataset created from a Nevada chart.

        # Initialize public dict attributes.
        # Key is the record ID, value is a list with the following:
        #   Position    Information
        #       0       Assembly ID
        #       1       Date of failure
        #       2       Left of interval
        #       3       Right of interval (same as left for exact time)
        #       4       Status of event
        #       5       Number of failures in interval
        #       6       Interarrival time (TBF)
        #       7       Failure mode type
        #       8       Record is from Nevada chart
        #       9       Ship date
        #      10       Number shipped
        #      11       Return date
        #      12       Number returned
        #      13       User float 1
        #      14       User float 2
        #      15       User float 3
        #      16       User integer 1
        #      17       User integer 2
        #      18       User integer 3
        #      19       User string 1
        #      20       User string 2
        #      21       User string 3
        self.dicRecords = {}

        # Initialize public list attributes.
        # The following lists are for storing bounded statistics associated
        # with the Survival model.  Each has the format:
        # [Lower bound estimate, Point estimate, Upper bound estimate]
        self.scale = [0.0, 0.0, 0.0]
        self.shape = [0.0, 0.0, 0.0]
        self.location = [0.0, 0.0, 0.0]

        # The following list is for storing the variance for each statistic.
        # The format is:
        # [Scale parameter, Shape parameter, Location parameter]
        self.variance = [0.0, 0.0, 0.0]

        # The following list is for storing the covariance for all statistics.
        # The format is:
        # [Scale-Shape, Scale-Location, Shape-Location]
        self.covariance = [0.0, 0.0, 0.0]

        # Initialize public scalar attributes.
        self.revision_id = 0
        self.survival_id = 0
        self.assembly_id = 0
        self.description = ''
        self.source = 0
        self.distribution_id = 0            # 1=MCF, 2=Kaplan-Meier,
                                            # 3=NHPP-Power Law,
                                            # 4=NHPP-LogLinear, 5=Exponential,
                                            # 6=Lognormal, 7=Normal, 8=Weibull,
                                            # 9=WeiBayes
        self.confidence = 0.75
        self.confidence_type = 0            # 1=Lower, 2=Upper, 3=Two-sided
        self.confidence_method = 0          # 1=Crow, 2=Duane, 3=Fisher,
                                            # 4=Likelihood, 5=Bootstrap
        self.fit_method = 0                 # 1=MLE, 2=Rank Regression
        self.rel_time = 100.0
        self.n_rel_points = 0
        self.n_suspensions = 0
        self.n_failures = 0
        self.mhb = 0.0                      # MIL-HDBK trend statistic
        self.lp = 0.0                       # Laplace trend statistic
        self.lr = 0.0                       # Lewis-Robinson trend statistic
        self.aic = 0.0                      # Aikake information criterion
        self.bic = 0.0                      # Bayesian information criterion
        self.mle = 0.0                      # Maximum likelihood estimate
        self.start_time = 0.0
        self.end_time = 0.0
        self.start_date = 0
        self.end_date = 0
        self.n_datasets = 0

    def set_attributes(self, values):
        """
        Method to set the Survival data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.survival_id = int(values[1])
            self.assembly_id = int(values[2])
            self.description = str(values[3])
            self.source = int(values[4])
            self.distribution_id = int(values[5])
            self.confidence = float(values[6])
            self.confidence_type = int(values[7])
            self.confidence_method = int(values[8])
            self.fit_method = int(values[9])
            self.rel_time = float(values[10])
            self.n_rel_points = int(values[11])
            self.n_suspensions = int(values[12])
            self.n_failures = int(values[13])
            self.mhb = float(values[14])
            self.lp = float(values[15])
            self.lr = float(values[16])
            self.aic = float(values[17])
            self.bic = float(values[18])
            self.mle = float(values[19])
            self.start_time = float(values[20])
            self.end_time = float(values[21])
            self.start_date = int(values[22])
            self.end_date = int(values[23])
            self.scale[0] = float(values[24])
            self.scale[1] = float(values[25])
            self.scale[2] = float(values[26])
            self.shape[0] = float(values[27])
            self.shape[1] = float(values[28])
            self.shape[2] = float(values[29])
            self.location[0] = float(values[30])
            self.location[1] = float(values[31])
            self.location[2] = float(values[32])
            self.variance[0] = float(values[33])
            self.variance[1] = float(values[34])
            self.variance[2] = float(values[35])
            self.covariance[0] = float(values[36])
            self.covariance[1] = float(values[37])
            self.covariance[2] = float(values[38])
        except IndexError as _err:
            _code = error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Verificaiton data model attributes.

        :return: (revision_id, survival_id, assembly_id, description, source,
                  distribution_id, confidence, confidence_type,
                  confidence_method, fit_method, rel_time, n_rel_points,
                  n_suspensions, n_failures, mhb, lp, lr, aic, bic, mle,
                  start_time, end_time, start_date, end_date, scale, shape,
                  location, variance, covariance)
        :rtype: tuple
        """

        _values = (self.revision_id, self.survival_id, self.assembly_id,
                   self.description, self.source, self.distribution_id,
                   self.confidence, self.confidence_type,
                   self.confidence_method, self.fit_method, self.rel_time,
                   self.n_rel_points, self.n_suspensions, self.n_failures,
                   self.mhb, self.lp, self.lr, self.aic, self.bic, self.mle,
                   self.start_time, self.end_time, self.start_date,
                   self.end_date, self.scale, self.shape, self.location,
                   self.variance, self.covariance)

        return _values

    def calculate_tbf(self, previous_id, current_id):
        """
        Method to calculate the time between failure of subsequent failures in
        a dataset.

        :param int previous_id: the Record ID of the previous failure or
                                suspension.
        :param int current_id: the Record ID of the current failure or
                               suspension.
        :return: False on success or True if an error is encountered.
        :rtype: boolean
        """

        _p_record = self.dicRecords[previous_id]
        _c_record = self.dicRecords[current_id]

        _previous = [previous_id, _p_record[0], _p_record[2], _p_record[3],
                     _p_record[5], _p_record[4]]
        _current = [current_id, _c_record[0], _c_record[2], _c_record[3],
                    _c_record[5], _c_record[4]]

        _c_record[6] = time_between_failures(_previous, _current)

        return False

    def estimate_parameters(self):
        """
        Method to fit data a parametric distribution and estimate the
        parameters of the fitted distribution.

                * 0 = Observed unit ID
                * 1 = Interval start time
                * 2 = Interval end time
                * 3 = Time between failures or interarrival time
                * 4 = Status of observation
                * 5 = Quantity of observations
                * 6 = Date of observation

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _data = []
        for _record in self.dicRecords.values():
            _data.append((_record[0], _record[2], _record[3], _record[6],
                          _record[4], _record[5], _record[1]))

        if self.distribution_id == 1:
            _data = _mcf.format_data(self.dicRecords)
            _meancf = _mcf.mean_cumulative_function(_data)
            print _meancf
        elif self.distribution_id == 2:
            print "Kaplan-Meier"
        elif self.distribution_id == 3:
            print "NHPP - Power Law"
        elif self.distribution_id == 4:
            print "NHPP - Log Linear"
        elif self.distribution_id == 5:
            if self.fit_method == 1:
                _results = Exponential().maximum_likelihood_estimate(
                                _data, self.start_time, self.end_time)
                self.scale[1] = _results[0][0]
                self.variance[0] = _results[1][0]
                self.mle = _results[2][0]
                self.aic = _results[2][1]
                self.bic = _results[2][2]
            elif self.fit_method == 2:
                print "Exponential Rank Regression"
        elif self.distribution_id == 6:
            if self.fit_method == 1:
                _results = LogNormal().maximum_likelihood_estimate(
                                _data, self.start_time, self.end_time)
                self.scale[1] = _results[0][0]
                self.shape[1] = _results[0][1]
                self.variance[0] = _results[1][0]   # Scale
                self.variance[1] = _results[1][2]   # Shape
                self.covariance[0] = _results[1][1] # Scale-Shape
                self.mle = _results[2][0]
                self.aic = _results[2][1]
                self.bic = _results[2][2]
            elif self.fit_method == 2:
                print "LogNormal Rank Regression"
        elif self.distribution_id == 7:
            if self.fit_method == 1:
                _results = Gaussian().maximum_likelihood_estimate(
                                _data, self.start_time, self.end_time)
                self.scale[1] = _results[0][0]
                self.shape[1] = _results[0][1]
                self.variance[0] = _results[1][0]   # Scale
                self.variance[1] = _results[1][2]   # Shape
                self.covariance[0] = _results[1][1] # Scale-Shape
                self.mle = _results[2][0]
                self.aic = _results[2][1]
                self.bic = _results[2][2]
            elif self.fit_method == 2:
                print "Normal Rank Regression"
        elif self.distribution_id == 8:
            if self.fit_method == 1:
                _results = Weibull().maximum_likelihood_estimate(
                                _data, self.start_time, self.end_time)
                self.scale[1] = _results[0][0]
                self.shape[1] = _results[0][1]
                self.variance[0] = _results[1][0]   # Scale
                self.variance[1] = _results[1][2]   # Shape
                self.covariance[0] = _results[1][1] # Scale-Shape
                self.mle = _results[2][0]
                self.aic = _results[2][1]
                self.bic = _results[2][2]
            elif self.fit_method == 2:
                print "Weibull Rank Regression"

        return False


class Survival(object):
    """
    The Survival data controller provides an interface between the Survival
    data model and an RTK view model.  A single Survival controller can
    manage one or more Survival data models.  The attributes of a
    Survival data controller are:

    :ivar _dao: the :class:`rtk.dao.DAO` to use when communicating with the RTK
                Project database.
    :ivar int _last_id: the last Survival ID used.
    :ivar dict dicSurvivals: Dictionary of the Survival data models managed.
                             Key is the Survival ID; value is a pointer to the
                             Survival data model instance.
    """

    def __init__(self):
        """
        Initializes a Survival data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicSurvival = {}

    def request_survival(self, dao, revision_id):
        """
        Method to read the RTK Project database and load all the Survivals
        associated with the selected Revision.  For each Survival returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Survival data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Survivals being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the tasks for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_survival')[0]

        _query = "SELECT * FROM rtk_survival \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_survivals = len(_results)
        except TypeError:
            _n_survivals = 0

        for i in range(_n_survivals):
            _survival = Model()
            _survival.set_attributes(_results[i])
            self.dicSurvival[_survival.survival_id] = _survival

        return(_results, _error_code)

    def add_survival(self, revision_id):
        """
        Adds a new Survival to the RTK Program's database.

        :param int revision_id: the Revision ID to add the new Survival to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        try:
            _description = "New Survival Analysis " + str(self._last_id + 1)
        except TypeError:                   # No tasks exist.
            _description = "New Survival Analysis 1"

        _query = "INSERT INTO rtk_survival \
                  (fld_revision_id, fld_description) \
                  VALUES (%d, '%s')" % (revision_id, _description)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new Survival analysis was added successfully to the RTK
        # Project database:
        #   1. Retrieve the ID of the newly inserted Survival analysis.
        #   2. Create a new Survival model instance.
        #   3. Set the attributes of the new Survival model instance.
        #   4. Add the new Survival model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_survival')[0]

            _survival = Model()
            _survival.set_attributes((revision_id, self._last_id, 0,
                                      _description, 0, 0, 0.75, 0, 2, 0, 100.0,
                                      0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 0, 0, 0))
            self.dicSurvival[_survival.survival_id] = _survival

        return(_results, _error_code)

    def delete_survival(self, survival_id):
        """
        Method to delete the selected Survival analysis from the open RTK
        Program database.

        :param int survival_id: the ID of the Survival analysis to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_survival \
                  WHERE fld_survival_id={0:d}".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Remove the Survival analysis from the survival dictionary.
        if _results:
            self.dicSurvival.pop(survival_id)

        return(_results, _error_code)

    def save_all_survivals(self):
        """
        Method to save all the Survival objects associated with the selected
        revision to the open RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _survival in self.dicSurvival.values():
            self.save_survival(_survival.survival_id)

        return False

    def save_survival(self, survival_id):
        """
        Method to save the Survival model information to the open RTK Program
        database.

        :param int survival_id: the ID of the Survival task to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _survival = self.dicSurvival[survival_id]

        _query = "UPDATE rtk_survival \
                  SET fld_assembly_id={2:d}, fld_description='{3:s}', \
                      fld_source={4:d}, fld_distribution_id={5:d}, \
                      fld_confidence={6:f}, fld_confidence_type={7:d}, \
                      fld_confidence_method={8:d}, fld_fit_method={9:d}, \
                      fld_rel_time={10:f}, fld_num_rel_points={11:d}, \
                      fld_num_suspension={12:d}, fld_num_failures={13:d}, \
                      fld_scale_ll={14:f}, fld_scale={15:f}, \
                      fld_scale_ul={16:f}, fld_shape_ll={17:f}, \
                      fld_shape={18:f}, fld_shape_ul={19:f}, \
                      fld_location_ll={20:f}, fld_location={21:f}, \
                      fld_location_ul={22:f}, fld_variance_1={23:f}, \
                      fld_variance_2={24:f}, fld_variance_3={25:f}, \
                      fld_covariance_1={26:f}, fld_covariance_2={27:f}, \
                      fld_covariance_3={28:f}, fld_mhb={29:f}, fld_lp={30:f}, \
                      fld_lr={31:f}, fld_aic={32:f}, fld_bic={33:f}, \
                      fld_mle={34:f}, fld_start_time={35:f}, \
                      fld_start_date={36:d}, fld_end_date={37:d}, \
                      fld_nevada_chart={38:d} \
                  WHERE fld_revision_id={0:d} \
                  AND fld_survival_id={1:d}".format(
                      _survival.revision_id, _survival.survival_id,
                      _survival.assembly_id, _survival.description,
                      _survival.source, _survival.distribution_id,
                      _survival.confidence, _survival.confidence_type,
                      _survival.confidence_method, _survival.fit_method,
                      _survival.rel_time, _survival.n_rel_points,
                      _survival.n_suspensions, _survival.n_failures,
                      _survival.scale[0], _survival.scale[1],
                      _survival.scale[2], _survival.shape[0],
                      _survival.shape[1], _survival.shape[2],
                      _survival.location[0], _survival.location[1],
                      _survival.location[2], _survival.variance[0],
                      _survival.variance[1], _survival.variance[2],
                      _survival.covariance[0], _survival.covariance[1],
                      _survival.covariance[2], _survival.mhb, _survival.lp,
                      _survival.lr, _survival.aic, _survival.bic,
                      _survival.mle, _survival.start_time,
                      _survival.start_date, _survival.end_date,
                      _survival._nevada_chart)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Save all the records.
        for _record_id in _survival.dicRecords.keys():
            (_results,
             _error_code) = self.save_record(survival_id, _record_id,
                                             _survival.dicRecords[_record_id])

        return(_results, _error_code)

    def request_records(self, survival_id):
        """
        Method to read the RTK Project database and load all the records
        associated with the selected Survival analysis object.

        :param int survival_id: the Survival ID the dataset is associated with.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _dict = {}

        _query = "SELECT fld_record_id, fld_assembly_id, fld_failure_date, \
                         fld_left_interval, fld_right_interval, \
                         fld_status, fld_quantity, fld_tbf, \
                         fld_mode_type, fld_nevada_chart, fld_ship_date, \
                         fld_number_shipped, fld_return_date, \
                         fld_number_returned, fld_user_float_1, \
                         fld_user_float_2, fld_user_float_3, \
                         fld_user_integer_1, fld_user_integer_2, \
                         fld_user_integer_3, fld_user_string_1, \
                         fld_user_string_2, fld_user_string_3 \
                  FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d} \
                  ORDER BY fld_left_interval".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_records = len(_results)
        except TypeError:
            _n_records = 0

        _survival = self.dicSurvival[survival_id]
        for i in range(_n_records):
           _dict[_results[i][0]] = list(_results[i][1:])

        _survival.dicRecords = OrderedDict(sorted(_dict.items(),
                                           key=lambda t: t[1][3]))

        return(_results, _error_code)

    def add_record(self, survival_id):
        """
        Method to add a Record to the selected Dataset.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT MAX(fld_record_id) \
                  FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d}".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        if _results[0][0] is None:
            _last_id = 1
        else:
            _last_id = _results[0][0] + 1

        _query = "INSERT INTO rtk_survival_data \
                  (fld_survival_id, fld_record_id) \
                  VALUES ({0:d}, {1:d})".format(survival_id, _last_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            _survival = self.dicSurvival[survival_id]
            _survival.dicRecords[_last_id] = (0, 719163, 0.0, 0.0, 0, 1, 0.0,
                                              1, 0, 719163, 1, 719163, 0, 0.0,
                                              0.0, 0.0, 0, 0, 0, '', '', '')

        return(_results, _error_code)

    def delete_record(self, survival_id, record_id):
        """
        Method to delete the selected Record.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int record_id: the ID of the Record to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d} \
                  AND fld_record_id={1:d}".format(survival_id, record_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            _survival = self.dicSurvival[survival_id]
            _survival.dicRecords.pop(record_id)

        return(_results, _error_code)

    def save_record(self, survival_id, record_id, record):
        """
        Method to save a Dataset Record to the open RTK Program database.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int record_id: the ID of the Record to save.
        :param list record: the record values to save.
        :return: (_results, _error_code)
        :rype: tuple
        """

        _query = "UPDATE rtk_survival_data \
                  SET fld_assembly_id={2:d}, fld_failure_date={3:d}, \
                      fld_left_interval={4:f}, fld_right_interval={5:f}, \
                      fld_status={6:d}, fld_quantity={7:d}, fld_tbf={8:f}, \
                      fld_mode_type={9:d}, fld_nevada_chart={10:d}, \
                      fld_ship_date={11:d}, fld_number_shipped={12:d}, \
                      fld_return_date={13:d}, fld_number_returned={14:d}, \
                      fld_user_float_1={15:f}, fld_user_float_2={16:f}, \
                      fld_user_float_3={17:f}, fld_user_integer_1={18:d}, \
                      fld_user_integer_2={19:d}, fld_user_integer_3={20:d}, \
                      fld_user_string_1='{21:s}', fld_user_string_2='{22:s}', \
                      fld_user_string_3='{23:s}' \
                  WHERE fld_survival_id={0:d} \
                  AND fld_record_id={1:d}".format(survival_id, record_id,
                                                  record[0], record[1],
                                                  record[2], record[3],
                                                  record[4], record[5],
                                                  record[6], record[7],
                                                  record[8], record[9],
                                                  record[10], record[11],
                                                  record[12], record[13],
                                                  record[14], record[15],
                                                  record[16], record[17],
                                                  record[18], record[19],
                                                  record[20], record[21])
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if not _results:
            print survival_id, dataset_id, record_id

        return(_results, _error_code)
