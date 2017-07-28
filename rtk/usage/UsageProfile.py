#!/usr/bin/env python
"""
####################
Usage Profile Module
####################
"""

# -*- coding: utf-8 -*-
#
#       rtk.usage.UsageProfile.py is part of The RTK Project
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
    import Configuration as _conf
except ImportError:
    import rtk.Configuration as _conf
from Mission import Model as Mission
from Phase import Model as Phase
from Environment import Model as Environment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Usage Profile data model aggregates the Mission, Phase, and Environment
    data models to produce an overall usage profile.  A Revision will consist
    of one Usage Profile.  The attributes of a Usage Profile are:

    :ivar dict dicMissions: Dictionary of the Missions associated with the
                            Usage Profile.  Key is the Mission ID; value is a
                            pointer to the instance of the Mission data model.
    :ivar int revision_id: the ID of the Revision the Usage Profile is
                           associated with.
    """

    def __init__(self, revision_id):
        """
        Method to initialize a Usage Profile data model instance.

        :param int revision_id: the Revision ID that the Usage Profile will be
                                associated with.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicMissions = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.revision_id = revision_id


class UsageProfile(object):
    """
    The Usage Profile controller provides an interface between the Usage
    Profile data model and an RTK view model.  A single Usage Profile
    controller can control one or more Usage Profile data models.

    :ivar _dao: the :py:class:`rtk.dao.DAO.DAO` used to communicate with the
                RTK Project database.
    :ivar dict dicProfiles: Dictionary of the Usage Profile data models
                            controlled.  Key is the Revision ID; value is a
                            pointer to the instance of the Usage Profile data
                            model.
    """

    def __init__(self):
        """
        Method to initialize a Usage Profile controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicProfiles = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.dao = None

    def request_profile(self, revision_id):
        """
        Method to load the entire mission profile for a Revision.  Starting at
        the Mission level, the steps to create the Usage Profile are:

        #. Create an instance of the Usage Profile (Mission, Phase,
           Environment) data model.
        #. Add instance pointer to the Profile dictionary for the passed
           Revision.
        #. Retrieve the missions (phases, environments) from the RTK Project
           database.
        #. Create an instance of the data model.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add instance pointer to the Mission (Phase, Environment)
           dictionary.

        :param int revision_id: the Revision ID that the Usage Profile will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _profile = Model(revision_id)
        self.dicProfiles[revision_id] = _profile

        _query = "SELECT * FROM tbl_missions \
                  WHERE fld_revision_id={0:d} \
                  ORDER BY fld_mission_id".format(revision_id)
        (_results, _error_code, __) = self.dao.execute(_query)
        try:
            _n_missions = len(_results)
        except TypeError:
            _n_missions = 0

        for i in range(_n_missions):
            _mission = Mission()
            _mission.set_attributes(_results[i])
            _profile.dicMissions[_mission.mission_id] = _mission

            _query = "SELECT * FROM tbl_mission_phase \
                      WHERE fld_mission_id={0:d}".format(_mission.mission_id)
            (_phases,
             _error_code,
             __) = self.dao.execute(_query, commit=False)
            try:
                _n_phases = len(_phases)
            except TypeError:
                _n_phases = 0

            for i in range(_n_phases):
                _phase = Phase()
                _phase.set_attributes(_phases[i])
                _mission.dicPhases[_phase.phase_id] = _phase

                _query = "SELECT * FROM tbl_environments \
                          WHERE fld_phase_id={0:d}".format(_phase.phase_id)
                (_environments, _error_code, __) = self.dao.execute(_query)
                try:
                    _n_environments = len(_environments)
                except TypeError:
                    _n_environments = 0

                for i in range(_n_environments):
                    _environment = Environment()
                    _environment.set_attributes(_environments[i])
                    _phase.dicEnvironments[_environment.environment_id] = _environment

        return False

    def add_profile(self, revision_id):
        """
        Method to add a new Usage Profile to the dictionary of profiles managed
        by this controller.

        :param int revision_id: the Revision ID to add the Usage Profile.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.request_profile(revision_id)

        return False

    def add_mission(self, revision_id):
        """
        Method to add a new Mission to the Usage Profile.

        :param int revision_id: the Revision ID of the Usage Profile to add the
                                new mission.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _query = "INSERT INTO tbl_missions \
                  (fld_revision_id, fld_mission_description) \
                  VALUES ({0:d}, '{1:s}')".format(revision_id,
                                                  "New Mission")
        (_results,
         _error_code,
         _last_id) = self.dao.execute(_query, commit=True)

        _mission = Mission()
        _mission.set_attributes((revision_id, _last_id, 0.0, 0.0, '', ''))
        _profile = self.dicProfiles[revision_id]
        _profile.dicMissions[_last_id] = _mission

        return(_results, _error_code, _last_id)

    def delete_mission(self, revision_id, mission_id):
        """
        Method to delete a Mission from the Usage Profile.

        :param int revision_id: the Revision ID the Mission is associated with.
        :param int mission_id: the Mission ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM tbl_missions \
                  WHERE fld_mission_id={0:d}".format(mission_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        _profile = self.dicProfiles[revision_id]
        _profile.dicMissions.pop(mission_id)

        return(_results, _error_code)

    def add_phase(self, revision_id, mission_id):
        """
        Method to add a new Phase to the Usage Profile.

        :param int revision_id: the Revision ID of the Usage Profile to add the
                                new Phase.
        :param int mission_id: the Mission ID of the Mission to add the new
                               Phase.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _profile = self.dicProfiles[revision_id]
        _mission = _profile.dicMissions[mission_id]

        _query = "INSERT INTO tbl_mission_phase \
                  (fld_revision_id, fld_mission_id, fld_phase_start, \
                   fld_phase_end, fld_phase_name, \
                   fld_phase_description) \
                  VALUES ({0:d}, {1:d}, 0.0, 0.0, '', '')".format(revision_id,
                                                                  mission_id)

        (_results,
         _error_code,
         _last_id) = self.dao.execute(_query, commit=True)

        _phase = Phase()
        _phase.set_attributes((revision_id, mission_id, _last_id,
                               0.0, 0.0, '', ''))
        _mission.dicPhases[_phase.phase_id] = _phase

        return(_results, _error_code, _last_id)

    def delete_phase(self, revision_id, mission_id, phase_id):
        """
        Method to delete a Phase from the Usage Profile.

        :param int revision_id: the Revision ID from which to delete.
        :param int mission_id: the Mission ID from which to delete.
        :param int phase_id: the Phase ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _profile = self.dicProfiles[revision_id]
        _mission = _profile.dicMissions[mission_id]
        try:
            _mission.dicPhases.pop(phase_id)
        except KeyError:
            return(True, 10)

        _query = "DELETE FROM tbl_mission_phase \
                  WHERE fld_phase_id={0:d}".format(phase_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)

    def add_environment(self, revision_id, mission_id, phase_id):
        """
        Method to add an Environment to the Usage Profile.

        :param int revision_id: the Revision ID of the Usage Profile to add the
                                new Environment.
        :param int mission_id: the Mission ID of the Mission to add the new
                               Environment.
        :param int phase_id: the Phase ID of the Phase to add the new
                             Environment.
        :return: (_results, _error_code, _last_id)
        :rtype: tuple
        """

        _profile = self.dicProfiles[revision_id]
        _mission = _profile.dicMissions[mission_id]
        _phase = _mission.dicPhases[phase_id]

        _query = "INSERT INTO tbl_environments \
                  (fld_revision_id, fld_mission_id, fld_phase_id, \
                   fld_test_id, fld_condition_name, fld_units, fld_minimum, \
                   fld_maximum, fld_mean, fld_variance) \
                  VALUES ({0:d}, {1:d}, {2:d}, {3:d}, '{4:s}', '{5:s}', \
                          {6:f}, {7:f}, {8:f}, {9:f})".format(revision_id,
                                                              mission_id,
                                                              phase_id, 0, '',
                                                              '', 0.0, 0.0,
                                                              0.0, 0.0)
        (_results,
         _error_code,
         _last_id) = self.dao.execute(_query, commit=True)

        _environment = Environment()
        _environment.set_attributes((revision_id, mission_id, phase_id, 0,
                                     _last_id, '', '', 0.0, 0.0, 0.0, 0.0))
        _phase.dicEnvironments[_environment.environment_id] = _environment

        return(_results, _error_code, _last_id)

    def delete_environment(self, revision_id, mission_id, phase_id,
                           environment_id):
        """
        Method to delete an Environment from the Usage Profile.

        :param int revision_id: the Revision ID from which to delete.
        :param int mission_id: the Mission ID from which to delete.
        :param int phase_id: the Phase ID from which to delete.
        :param int environment_id: the Environment ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _profile = self.dicProfiles[revision_id]
        _mission = _profile.dicMissions[mission_id]
        _phase = _mission.dicPhases[phase_id]
        try:
            _phase.dicEnvironments.pop(environment_id)
        except KeyError:
            return(True, 10)

        _query = "DELETE FROM tbl_environments \
                  WHERE fld_condition_id={0:d}".format(environment_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_profile(self, revision_id):
        """
        Method to save the Usage Profile.  Wrapper for the _save_mission,
        _save_phase, and _save_environment methods.

        :param int revision_id: the Revision ID of the Usage Profile to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _profile = self.dicProfiles[revision_id]

        for _mission in _profile.dicMissions.values():
            self._save_mission(_mission)

            for _phase in _mission.dicPhases.values():
                self._save_phase(_phase)

                for _environment in _phase.dicEnvironments.values():
                    self._save_environment(_environment)

    def _save_mission(self, mission):
        """
        Method to save the Mission attributes to the RTK Project database.

        :param mission: the :py:class:`rtk.usage.Mission.Model` to save.
        :return: _error_code
        :rtype: int
        """

        _query = "UPDATE tbl_missions \
                  SET fld_mission_time={0:f}, fld_mission_units='{1:s}', \
                      fld_mission_description='{2:s}' \
                  WHERE fld_mission_id={3:d}".format(mission.time,
                                                     mission.time_units,
                                                     mission.description,
                                                     mission.mission_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def _save_phase(self, phase):
        """
        Method to save the Phase attributes to the RTK Project database.

        :param phase: the :py:class:`rtk.usage.Phase.Model` to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "UPDATE tbl_mission_phase \
                  SET fld_phase_start={1:f}, fld_phase_end={2:f}, \
                      fld_phase_name='{3:s}', fld_phase_description='{4:s}' \
                  WHERE fld_phase_id={0:d}".format(phase.phase_id,
                                                   phase.start_time,
                                                   phase.end_time,
                                                   phase.code,
                                                   phase.description)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)

    def _save_environment(self, environment):
        """
        Method to save the Environment attributes to the RTK Project database.

        :param environment: the :py:class:`rtk.usage.Environment.Model` to
                            save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "UPDATE tbl_environments \
                  SET fld_condition_name='{1:s}', \
                      fld_units='{2:s}', fld_minimum={3:f}, \
                      fld_maximum={4:f}, fld_mean={5:f}, \
                      fld_variance={6:f} \
                  WHERE fld_condition_id={0:d}".format(
                      environment.environment_id, environment.name,
                      environment.units, environment.minimum,
                      environment.maximum, environment.mean,
                      environment.variance)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)
