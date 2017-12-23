#!/usr/bin/env python
"""
=========================
Physics of Failure Module
=========================
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.PhysicsOfFailure.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration

from Mechanism import Model as Mechanism
from Load import Model as Load
from Stress import Model as Stress
from Method import Model as Method

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ParentError(Exception):
    """
    Exception raised when None is passed for the hardware ID when initializing
    an instance of the PoF model.
    """

    pass


class Model(object):
    """
    The Physics of Failure (PoF) data model aggregates the Mechanism, Load,
    Stress and Method data models to produce an overall PoF analysis.  A
    Hardware item will consist of one PoF analysis.  The attributes of a PoF
    are:

    :ivar dict dicMechanisms: Dictionary of the Mechanisms associated with the
                              PoF.  Key is the Mechanism ID; value is a pointer
                              to the instance of the Mechanism data model.
    :ivar int assembly_id: the Hardware item ID the PoF analysis is associated
                           with.
    """

    def __init__(self, assembly_id):
        """
        Method to initialize a PoF data model instance.

        :param int assembly_id: the Hardware item ID that the PoF analysis will
                                be associated with.
        """

        # Model must be associated with either a Function or Hardware item.
        if assembly_id is None:
            raise ParentError

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicMechanisms = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.assembly_id = assembly_id


class PoF(object):
    """
    The PoF data controller provides an interface between the PoF data model
    and an RTK view model.  A single PoF data controller can manage one or
    more PoF data models.

    :ivar _dao: the :py:class:`rtk.dao.DAO.DAO` used to communicate with the
                RTK Project database.
    :ivar dict dicPoF: Dictionary of the PoF data models controlled.  Key is
                       the Hardware ID; value is a pointer to the instance of
                       the PoF data model.

    """

    def __init__(self):
        """
        Method to initialize a PoF controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._dao = None

        # Define public dictionary attributes.
        self.dicPoF = {}

        # Define public list attributes.

        # Define public scalar attributes.

    def request_pof(self, dao, assembly_id=None):  # pylint: disable=R0914
        """
        Method to load the entire PoF for a Hardware item.  Starting at the
        Mechanism level, the steps to create the PoF are:

        #. Create an instance of the PoF (Mechanism, Load, Stress, Method)
           data model.
        #. Add instance pointer to the PoF dictionary for the passed
           Hardware item.
        #. Retrieve the mechanisms (loads, stresses, methods) from the
           RTK Project database.
        #. Create an instance of the data model.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add instance pointer to the Mechanism (Load, Stress, Method)
           dictionary.

        :param dao: the :py:class:`rtk.dao.DAO.DAO` to use for communicating
                    with the RTK Project database.
        :keyword int assembly_id: the Hardware item ID that the PoF will be
                                  associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Controller must be associated with a Hardware item.
        if assembly_id is None:
            raise ParentError

        self._dao = dao

        _pof = Model(assembly_id)
        self.dicPoF[assembly_id] = _pof

        _query = "SELECT fld_assembly_id, fld_mechanism_id, fld_description \
                  FROM rtk_mechanisms \
                  WHERE fld_assembly_id={0:d} \
                  AND fld_include_pof=1 \
                  ORDER BY fld_mechanism_id ASC".format(assembly_id)
        (_results, _error_code, __) = self._dao.execute(_query)
        try:
            _n_mechanisms = len(_results)
        except TypeError:
            _n_mechanisms = 0

        for i in range(_n_mechanisms):
            _mechanism = Mechanism()
            _mechanism.set_attributes(_results[i])
            _pof.dicMechanisms[_mechanism.mechanism_id] = _mechanism

            _query = "SELECT * FROM rtk_op_loads \
                      WHERE fld_mechanism_id={0:d}".format(
                _mechanism.mechanism_id)
            (_loads, _error_code, __) = self._dao.execute(_query, commit=False)
            try:
                _n_loads = len(_loads)
            except TypeError:
                _n_loads = 0

            for i in range(_n_loads):
                _load = Load()
                _load.set_attributes(_loads[i])
                _mechanism.dicLoads[_load.load_id] = _load

                _query = "SELECT * FROM rtk_op_stress \
                          WHERE fld_load_id={0:d}".format(_load.load_id)
                (_stresses, _error_code, __) = self._dao.execute(_query)
                try:
                    _n_stresses = len(_stresses)
                except TypeError:
                    _n_stresses = 0

                for j in range(_n_stresses):
                    _stress = Stress()
                    _stress.set_attributes(_stresses[j])
                    _load.dicStresses[_stress.stress_id] = _stress

                    _query = "SELECT * FROM rtk_test_methods \
                              WHERE fld_stress_id={0:d}".format(
                        _stress.stress_id)
                    (_methods, _error_code, __) = self._dao.execute(_query)
                    try:
                        _n_methods = len(_methods)
                    except TypeError:
                        _n_methods = 0

                    for k in range(_n_methods):
                        _method = Method()
                        _method.set_attributes(_methods[k])
                        _stress.dicMethods[_method.method_id] = _method

        return False

    def add_pof(self, hardware_id=None):
        """
        Method to add a new PoF to the dictionary of profiles managed by this
        controller.

        :keyword int hardware_id: the Hardware item ID to add the PoF.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.request_pof(self._dao, hardware_id)

        return False

    def add_mechanism(self, hardware_id):
        """
        Method to add a new Mechanism to the selected Hardware item.

        :param int hardware_id: the Hardware ID to add the Mechanism.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]

        _query = "INSERT INTO rtk_mechanisms \
                  (fld_assembly_id, fld_mode_id, fld_include_pof) \
                  VALUES ({0:d}, 10000, 1)".format(hardware_id)
        (_results, _error_code, _last_id) = self._dao.execute(
            _query, commit=True)

        _mechanism = Mechanism()
        _mechanism.set_attributes((hardware_id, _last_id, ''))
        _pof.dicMechanisms[_last_id] = _mechanism

        return (_results, _error_code, _last_id)

    def delete_mechanism(self, hardware_id, mechanism_id):
        """
        Method to delete the selected Mechanism.

        :param int hardware_id: the Hardware ID of the Mechanism to delete.
        :param int mechanism_id: the Mechanism ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]

        _query = "DELETE FROM rtk_mechanisms \
                  WHERE fld_mechanism_id={0:d}".format(mechanism_id)
        (_results, _error_code, _last_id) = self._dao.execute(
            _query, commit=True)

        try:
            _pof.dicMechanisms.pop(mechanism_id)
        except KeyError:
            _error_code = 60

        return (_results, _error_code)

    def add_load(self, hardware_id, mechanism_id):
        """
        Method to add a new Operating Load to the selected Mechanism.


        :param int hardware_id: the Hardware ID to add the Load.
        :param int mechanism_id: the Mechanism ID to add the Load.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]
        _mechanism = _pof.dicMechanisms[mechanism_id]

        _query = "INSERT INTO rtk_op_loads \
                  (fld_mechanism_id) \
                  VALUES ({0:d})".format(mechanism_id)
        (_results, _error_code, _last_id) = self._dao.execute(
            _query, commit=True)

        _load = Load()
        _load.set_attributes((mechanism_id, _last_id, 'Test Load', 0))
        _mechanism.dicLoads[_last_id] = _load

        return (_results, _error_code, _last_id)

    def delete_load(self, hardware_id, mechanism_id, load_id):
        """
        Method to delete the selected operating Load.


        :param int hardware_id: the Hardware ID of the operating Load to
                                delete.
        :param int mechanism_id: the Mechanism ID of the operating Load to
                                 delete.
        :param int load_id: the operating Load ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]
        _mechanism = _pof.dicMechanisms[mechanism_id]

        _query = "DELETE FROM rtk_op_loads \
                  WHERE fld_load_id={0:d}".format(load_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        try:
            _mechanism.dicLoads.pop(load_id)
        except KeyError:
            _error_code = 60

        return (_results, _error_code)

    def add_stress(self, hardware_id, mechanism_id, load_id):
        """
        Method to add a new operating Stress to the selected operating Load.


        :param int hardware_id: the Hardware ID to add the operating Stress.
        :param int mechanism_id: the Mechanism ID to add the operating Stress.
        :param int cause_id: the operating Load ID to add the operating Stress.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]
        _mechanism = _pof.dicMechanisms[mechanism_id]
        _load = _mechanism.dicLoads[load_id]

        _query = "INSERT INTO rtk_op_stress \
                  (fld_load_id) \
                  VALUES ({0:d})".format(load_id)
        (_results, _error_code, _last_id) = self._dao.execute(
            _query, commit=True)

        _stress = Stress()
        _stress.set_attributes((load_id, _last_id, '', '', '', ''))
        _load.dicStresses[_last_id] = _stress

        return (_results, _error_code, _last_id)

    def delete_stress(self, hardware_id, mechanism_id, load_id, stress_id):
        """
        Method to delete the selected operating Stress.


        :param int hardware_id: the Hardware ID of the operating Stress to
                                delete.
        :param int mechanism_id: the Mechanism ID of the operating Stress to
                                 delete.
        :param int load_id: the operating Load ID to delete.
        :param int stress_id: the operating Stress ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]
        _mechanism = _pof.dicMechanisms[mechanism_id]
        _load = _mechanism.dicLoads[load_id]

        _query = "DELETE FROM rtk_op_stress \
                  WHERE fld_stress_id={0:d}".format(stress_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        try:
            _load.dicStresses.pop(stress_id)
        except KeyError:
            _error_code = 60

        return (_results, _error_code)

    def add_method(self, hardware_id, mechanism_id, load_id, stress_id):
        """
        Method to add a new test Method to the selected operating Stress.


        :param int hardware_id: the Hardware ID to add the test Method.
        :param int mechanism_id: the Mechanism ID to add the test Method.
        :param int load_id: the operating Load ID to add the test Method.
        :param int stress_id: the operating Stress ID to add the test Method.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]
        _mechanism = _pof.dicMechanisms[mechanism_id]
        _load = _mechanism.dicLoads[load_id]
        _stress = _load.dicStresses[stress_id]

        _query = "INSERT INTO rtk_test_methods \
                  (fld_stress_id) \
                  VALUES ({0:d})".format(stress_id)
        (_results, _error_code, _last_id) = self._dao.execute(
            _query, commit=True)

        _method = Method()
        _method.set_attributes((stress_id, _last_id, '', 0, 0, ''))
        _stress.dicMethods[_last_id] = _method

        return (_results, _error_code, _last_id)

    def delete_method(self, hardware_id, mechanism_id, load_id, stress_id,
                      method_id):
        """
        Method to delete the selected test Method.


        :param int hardware_id: the Hardware ID of the test Method to delete.
        :param int mechanism_id: the Mechanism ID of the test Method to delete.
        :param int load_id: the operating Load ID of the test Method ID to
                            delete.
        :param int stress_id: the operating Stress ID of the test Method to
                              delete.
        :param int method_id: the test Method ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _pof = self.dicPoF[hardware_id]
        _mechanism = _pof.dicMechanisms[mechanism_id]
        _load = _mechanism.dicLoads[load_id]
        _stress = _load.dicStresses[stress_id]

        _query = "DELETE FROM rtk_test_methods \
                  WHERE fld_method_id={0:d}".format(method_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        try:
            _stress.dicMethods.pop(method_id)
        except KeyError:
            _error_code = 60

        return (_results, _error_code)

    def save_pof(self, hardware_id=None):
        """
        Method to save the PoF.  Wrapper for the _save_mechanism, _save_load,

        _save_stress, and _save_method methods.

        :keyword int hardware_id: the Hardware item ID of the PoF to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Controller must be associated with a Hardware item.
        if hardware_id is None:
            raise ParentError

        _pof = self.dicPoF[hardware_id]
        for _mechanism in _pof.dicMechanisms.values():
            self._save_mechanism(_mechanism)
            for _load in _mechanism.dicLoads.values():
                self._save_load(_load)
                for _stress in _load.dicStresses.values():
                    self._save_stress(_stress)
                    for _method in _stress.dicMethods.values():
                        self._save_method(_method)

        return False

    def _save_mechanism(self, mechanism):
        """
        Method to save the Mechanism attributes to the RTK Project database.

        :param mechanism: the :py:class:`rtk.analyses.pof.Mechanism.Model` data
                          model to save.

        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_mechanisms \
                  SET fld_description='{0:s}', fld_include_pof=1 \
                  WHERE fld_mechanism_id={1:d}".format(mechanism.description,
                                                       mechanism.mechanism_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return _error_code

    def _save_load(self, load):
        """
        Method to save the operating Load attributes to the RTK Project
        database.

        :param load: the :py:class:`rtk.analyses.pof.Load.Model` data model to
                     save.

        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_op_loads \
                  SET fld_load_description='{0:s}', \
                      fld_priority={1:d}, fld_damage_model={2:d} \
                  WHERE fld_load_id={3:d}".format(
            load.description, load.priority, load.damage_model, load.load_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return _error_code

    def _save_stress(self, stress):
        """
        Method to save the operating Stess attributes to the RTK Project
        database.

        :param stress: the :py:class:`rtk.analyses.pof.Stress.Model` data model
                       to save.

        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_op_stress \
                  SET fld_stress_description='{0:s}', \
                      fld_measurable_parameter={1:d}, \
                      fld_load_history={2:d}, fld_remarks='{3:s}' \
                  WHERE fld_stress_id={4:d}".format(
            stress.description, stress.measurable_parameter,
            stress.load_history, stress.remarks, stress.stress_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return _error_code

    def _save_method(self, method):
        """
        Method to save the test Method attributes to the RTK Project database.

        :param method: the :py:class:`rtk.analyses.pof.Method.Model` data model
                       to save.

        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE rtk_test_methods \
                  SET fld_stress_id={0:d}, \
                      fld_method_description='{1:s}', \
                      fld_boundary_conditions='{2:s}', \
                      fld_remarks='{3:s}' \
                  WHERE fld_method_id={4:d}".format(
            method.stress_id, method.description, method.boundary_conditions,
            method.remarks, method.method_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return _error_code
