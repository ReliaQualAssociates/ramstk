#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.Environment.py is part of The RTK Project
#
# All rights reserved.

"""
##################
Environment Module
##################
"""

<<<<<<< HEAD
# Import other RTK modules.
try:
    import Configuration as Configuration
    import Utilities as Utilities
    from dao.DAO import RTKEnvironment
except ImportError:
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.Utilities as Utilities           # pylint: disable=E0401
    from rtk.dao.DAO import RTKEnvironment      # pylint: disable=E0401
=======
# -*- coding: utf-8 -*-
#
#       rtk.usage.Environment.py is part of The RTK Project
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
>>>>>>> master

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Environment data model contains the attributes and methods of a mission
    phase environment.  A Phase will consist of zero or more environments.  The
    attributes of an Environment are:

    :cvar dict dicEnvironment: dictionary containing all the RTKEnvironment
                               data models that are part of the Environment
                               tree.  Key is the Environment ID; value is a
                               pointer to the instance of the RTKEnvironment
                               data model.

    :ivar int last_id: the last Environment ID used in the RTK Program
                       database.
    :ivar dao: the `:py:class:rtk.dao.DAO.DAO` object used to communicate with
               the RTK Program database.

    """

    # Define public class dictionary attributes.
    dicEnvironment = {}

    def __init__(self):
        """
        Method to initialize an Environment data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.last_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None

    def retrieve(self, environment_id):
        """
        Method to retrieve the instance of the RTKEnvironment data model for
        the Environment ID passed.

        :param int environment_id: the ID Of the RTKEnvironment to retrieve.
        :return: the instance of the RTKEnvironment class that was requested
                 or None if the requested Environment ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKEnvironment.Model`
        """

        try:
            _environment = self.dicEnvironment[environment_id]
        except KeyError:
            _environment = None

        return _environment

    def retrieve_all(self, dao, phase_id):
        """
        Method to retrieve all the Environments from the RTK Program database.

        :return: dicEnvironment; the dictionary of RTKEnvironment data models
                 that comprise the Environment tree.
        :rtype: dict
        """

        self.dao = dao

        # Clear the Environment dictionary of previous Phases's Environments.
        self.dicEnvironment = {}
        for _environment in self.dao.session.query(RTKEnvironment). \
                filter(RTKEnvironment.phase_id == phase_id).all():
            self.dicEnvironment[_environment.environment_id] = _environment

        return self.dicEnvironment

    def add_environment(self, phase_id):
        """
        Method to add an Evnironmental condition to the RTK Program database
        for Environment ID.

        :param int phase_id: the Mission Phase ID to add the Environment to.
        :return: _environment
        :rtype: `:py:test:rtk.dao.DAO.RTKEnvironment`
        """

        _environment = RTKEnvironment()
        _environment.phase_id = phase_id
        (_error_code, _msg) = self.dao.db_add(_environment)

        self.last_id = _environment.environment_id

        # If the add was successful add the new RTKEnvironment data model
        # instance to dicEnvironment and log the success message to the user
        # log.  Otherwise, update the error message and write it to the error
        # log.
        if _error_code == 0:
            self.dicEnvironment[_environment.environment_id] = _environment
            Configuration.RTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + "  Failed to add a new Environment to the RTK \
                             Program database."
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _environment = None

        return _environment

    def delete_environment(self, environment_id):
        """
        Method to remove the phase associated with Environment ID.

        :param int environment_id: the ID of the Environment to be removed.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _environment = self.dicEnvironment[environment_id]

            (_error_code, _msg) = self.dao.db_delete(_environment)

            if _error_code == 0:
                self.dicEnvironment.pop(environment_id)
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to delete Environment ID {0:d} " \
                                  "from the RTK Program database.". \
                        format(environment_id)
                except ValueError:  # Environment ID is None.
                    _msg = _msg + "  Failed to delete Environment ID {0:s} " \
                                  "from the RTK Program database.". \
                        format(environment_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to delete non-existent Environment ID " \
                       "{0:d}.".format(environment_id)
            except ValueError:  # Environment ID is None.
                _msg = "Attempted to delete non-existent Environment ID " \
                       "{0:s}.".format(environment_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_environment(self, environment_id):
        """
        Method to update the environment associated with Phase ID to the RTK
        Program database.

        :param int environment_id: the Environment ID to save to the RTK
                                   Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _environment = self.dicEnvironment[environment_id]

            (_error_code, _msg) = self.dao.db_update()

            if _error_code == 0:
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to save Environment ID {0:d} to " \
                                  "the RTK Program database".\
                        format(environment_id)
                except ValueError:  # If the environment_id = None.
                    _msg = _msg + "  Failed to save Environment ID {0:s} to " \
                                  "the RTK Program database".\
                        format(environment_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to save non-existent Environment ID {0:d}.".\
                    format(environment_id)
            except ValueError:  # If the environment_id = None.
                _msg = "Attempted to save non-existent Environment ID {0:s}.".\
                    format(environment_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_all_environments(self):
        """
        Method to save all Environments to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        for _environment_id in self.dicEnvironment.keys():
            if self.save_environment(_environment_id):
                _return = True

        return _return


class Environment(object):
    """
    The Environment controller provides an interface between the Environment
    data model and an RTK view model.  A single Environment controller can
    control one or more Environment data models.  Currently the Environment
    controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Environment controller instance.
        """

        pass
