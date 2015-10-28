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


try:
    from survival.Dataset import Model as Dataset
except ImportError:
    from rtk.survival.Dataset import Model as Dataset


def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:       # Type error
        _error_code = 10                                            # pragma: no cover
    elif 'invalid literal for int() with base 10' in message[0]:    # Value error
        _error_code = 10
    elif 'index out of range' in message[0]:                        # Index error
        _error_code = 40
    else:                                                           # Unhandled error
        _error_code = 1000                                          # pragma: no cover

    return _error_code


class Model(object):                       # pylint: disable=R0902, R0904
    """
    The Survival data model contains the attributes and methods for an
    Survival. The attributes of an Survival model are:

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
        self.dicDatasets = {}

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
        # [Scale-Shape, Scale-Location, Shape-Location estimate]
        self.covariance = [0.0, 0.0, 0.0]

        # Initialize public scalar attributes.
        self.revision_id = 0
        self.survival_id = 0
        self.assembly_id = 0
        self.description = ''
        self.source = 0
        self.distribution_id = 0
        self.confidence = 0.75
        self.confidence_type = 0
        self.confidence_method = 0          # 0=lower, 1=upper, 2=two-sided
        self.fit_method = 0
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
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
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

        return(_results, _error_code)

    def request_datasets(self, survival_id):
        """
        Method to read the RTK Project database and load all the Datasets
        associated with the selected Survival object.  For each Dataset
        returned:

        #. Retrieve the datasets from the RTK Project database.
        #. Create a Dataset data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Datasets associated with
           the Survival object.

        :param int survival_id: the Survival ID to select the datasets for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT DISTINCT fld_survival_id, fld_dataset_id \
                  FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d}".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_datasets = len(_results)
        except TypeError:
            _n_datasets = 0

        for i in range(_n_datasets):
            _values = (_results[i][0], _results[i][1])
            (_records, __) = self.request_records(_results[i][1])
            _dataset = Dataset()
            _dataset.set_attributes(_values)
            _dataset.load_records(_records)
            _survival = self.dicSurvival[survival_id]
            _survival.dicDatasets[_results[i][1]] = _dataset

        return(_results, _error_code)

    def add_dataset(self, survival_id):
        """
        Adds a new Dataset to the RTK Program's database.

        :param int survival_id: the Survival ID to add the new Dataset to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT MAX(fld_dataset_id) \
                  FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d}".format(survival_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        if _results[0][0] is None:
            _last_id = 1
        else:
            _last_id = _results[0][0] + 1

        _query = "INSERT INTO rtk_survival_data \
                  (fld_survival_id, fld_dataset_id) \
                  VALUES ({0:d}, {1:d})".format(survival_id, _last_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new Dataset was added successfully to the RTK Project
        # database:
        #   1. Retrieve the ID of the newly inserted Dataset.
        #   2. Create a new Dataset model instance.
        #   3. Set the attributes of the new Dataset model instance.
        #   4. Add the new Dataset model to the Survival model dataset
        #      dictionary.
        if _results:
            _dataset = Dataset()
            _dataset.set_attributes((survival_id, _last_id))
            _survival = self.dicSurvival[survival_id]
            _survival.dicDatasets[_last_id] = _dataset

        return(_results, _error_code)

    def delete_dataset(self, survival_id, dataset_id):
        """
        Method to delete the selected Dataset from the open RTK Program
        database.

        :param int survival_id: the ID of the Survival analysis the dataset
                                belongs to.
        :param int dataset_id: the ID of the Dataset to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_survival_data \
                  WHERE fld_dataset_id={0:d}".format(dataset_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Remove the dataset from the Survival analysis Dataset dictionary.
        if _results:
            _survival = self.dicSurvival[survival_id]
            _survival.dicDatasets.pop(dataset_id)

        return(_results, _error_code)

    def save_dataset(self, survival_id, dataset_id):
        """
        Method to save the Dataset information to the open RTK Program
        database.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int dataset_id: the ID of the Dataset to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _survival = self.dicSurvival[survival_id]
        _dataset = _survival.dicDatasets[dataset_id]

        for _record_id in _dataset.dicRecords.keys():
            (_results,
             _error_code) = self.save_record(survival_id, dataset_id,
                                             _record_id,
                                             _dataset.dicRecords[_record_id])

        return(_results, _error_code)

    def request_records(self, dataset_id):
        """
        Method to read the RTK Project database and load all the records
        associated with the selected Dataset object.

        :param int dataset_id: the Dataset ID to retrieve the records for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

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
                  WHERE fld_dataset_id={0:d}".format(dataset_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        return(_results, _error_code)

    def add_record(self, survival_id, dataset_id):
        """
        Method to add a Record to the selected Dataset.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int dataset_id: the ID of the Dataset to add the Record to.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "SELECT MAX(fld_record_id) \
                  FROM rtk_survival_data \
                  WHERE fld_dataset_id={0:d}".format(dataset_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        if _results[0][0] is None:
            _last_id = 1
        else:
            _last_id = _results[0][0] + 1

        _query = "INSERT INTO rtk_survival_data \
                  (fld_survival_id, fld_dataset_id, fld_record_id) \
                  VALUES ({0:d}, {1:d}, {2:d})".format(survival_id, dataset_id,
                                                       _last_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            _survival = self.dicSurvival[survival_id]
            _dataset = _survival.dicDatasets[dataset_id]
            _dataset.dicRecords[_last_id] = (0, 719163, 0.0, 0.0, 0, 1, 0.0, 1,
                                             0, 719163, 1, 719163, 0, 0.0, 0.0,
                                             0.0, 0, 0, 0, '', '', '')

        return(_results, _error_code)

    def delete_record(self, survival_id, dataset_id, record_id):
        """
        Method to delete the selected Record.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int dataset_id: the ID of the Dataset the Record belongs to.
        :param int record_id: the ID of the Record to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_survival_data \
                  WHERE fld_survival_id={0:d} \
                  AND fld_dataset_id={1:d} \
                  AND fld_record_id={2:d}".format(survival_id, dataset_id,
                                                  record_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            _survival = self.dicSurvival[survival_id]
            _dataset = _survival.dicDatasets[dataset_id]
            _dataset.dicRecords.pop(record_id)

        return(_results, _error_code)

    def save_record(self, survival_id, dataset_id, record_id, record):
        """
        Method to save a Dataset Record to the open RTK Program database.

        :param int survival_id: the ID of the Survival analysis the Dataset
                                belongs to.
        :param int dataset_id: the ID of the Dataset the Record belongs to.
        :param int record_id: the ID of the Record to save.
        :param list record: the record values to save.
        :return: (_results, _error_code)
        :rype: tuple
        """

        _query = "UPDATE rtk_survival_data \
                  SET fld_assembly_id={3:d}, fld_failure_date={4:d}, \
                      fld_left_interval={5:f}, fld_right_interval={6:f}, \
                      fld_status={7:d}, fld_quantity={8:d}, fld_tbf={9:f}, \
                      fld_mode_type={10:d}, fld_nevada_chart={11:d}, \
                      fld_ship_date={12:d}, fld_number_shipped={13:d}, \
                      fld_return_date={14:d}, fld_number_returned={15:d}, \
                      fld_user_float_1={16:f}, fld_user_float_2={17:f}, \
                      fld_user_float_3={18:f}, fld_user_integer_1={19:d}, \
                      fld_user_integer_2={20:d}, fld_user_integer_3={21:d}, \
                      fld_user_string_1='{22:s}', fld_user_string_2='{23:s}', \
                      fld_user_string_3='{24:s}' \
                  WHERE fld_survival_id={0:d} \
                  AND fld_dataset_id={1:d} \
                  AND fld_record_id={2:d}".format(survival_id, dataset_id,
                                                  record_id, record[0],
                                                  record[1], record[2],
                                                  record[3], record[4],
                                                  record[5], record[6],
                                                  record[7], record[8],
                                                  record[9], record[10],
                                                  record[11], record[12],
                                                  record[13], record[14],
                                                  record[15], record[16],
                                                  record[17], record[18],
                                                  record[19], record[20],
                                                  record[21])
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if not _results:
            print survival_id, dataset_id, record_id

        return(_results, _error_code)
