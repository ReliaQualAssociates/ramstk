#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.Phase.py is part of The RTK Project
#
# All rights reserved.

"""
####################
Mission Phase Module
####################
"""

# Import other RTK modules.
try:
    import Configuration as Configuration
    import Utilities as Utilities
    from dao.DAO import RTKMissionPhase
except ImportError:
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.Utilities as Utilities           # pylint: disable=E0401
    from rtk.dao.DAO import RTKMissionPhase     # pylint: disable=E0401
__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Phase data model contains the attributes and methods of a mission
    phase.  A Mission will consist of one or more mission phases.  The
    attributes of a Phase are:

    :cvar dict dicPhase: dictionary containing all the RTKMissionPhase models
                         that are part of the Phase tree.  Key is the
                         Phase ID; value is a pointer to the instance
                         of the RTKMissionPhase model.

    :ivar int last_id: the last Phase ID used in the RTK Program database.
    :ivar dao: the `:py:class:rtk.dao.DAO` object used to communicate with the
               RTK Program database.

    """

    # Define public class dictionary attributes.
    dicPhase = {}

    def __init__(self):
        """
        Method to initialize a Phase data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.last_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None

    def retrieve(self, phase_id):
        """
        Method to retrieve the instance of the RTKMissionPhase data model for
        the Phase ID passed.

        :param int phase_id: the ID Of the RTKMissionPhase to retrieve.
        :return: the instance of the RTKMissionPhase class that was requested
                 or None if the requested Phase ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKMissionPhase.Model`
        """

        try:
            _phase = self.dicPhase[phase_id]
        except KeyError:
            _phase = None

        return _phase

    def retrieve_all(self, dao, mission_id):
        """
        Method to retrieve all the Phases from the RTK Program database.

        :return: dicPhase; the dictionary of RTKMissionPhase data models that
                 comprise the Mission Phase tree.
        :rtype: dict
        """

        self.dao = dao

        # Clear the Phase dictionary of previous Mission's Phases.
        self.dicPhase = {}
        for _phase in self.dao.session.query(RTKMissionPhase).\
                filter(RTKMissionPhase.mission_id == mission_id).all():
            self.dicPhase[_phase.phase_id] = _phase

        return self.dicPhase

    def add_phase(self, mission_id):
        """
        Method to add a Mission Phase to the RTK Program database for Mission
        ID.

        :param int mission_id: the Mission ID to add the Mission Phase to.
        :return: _phase
        :rtype: `:py:class:rtk.dao.DAO.RTKMissionPhase`
        """

        _phase = RTKMissionPhase()
        _phase.mission_id = mission_id
        (_error_code, _msg) = self.dao.db_add(_phase)

        self.last_id = _phase.phase_id

        # If the add was successful add the new RTKMissionPhase data model
        # instance to dicPhase and log the success message to the user log.
        # Otherwise, update the error message and write it to the error log.
        if _error_code == 0:
            self.dicPhase[_phase.phase_id] = _phase
            Configuration.RTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + "  Failed to add a new Phase to the RTK Program \
                           database."
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _phase = None

        return _phase

    def delete_phase(self, phase_id):
        """
        Method to remove the phase associated with Phase ID.

        :param int phase_id: the ID of the Phase to be removed.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _phase = self.dicPhase[phase_id]

            (_error_code, _msg) = self.dao.db_delete(_phase)

            if _error_code == 0:
                self.dicPhase.pop(phase_id)
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to delete Phase ID {0:d} from " \
                            "the RTK Program database.".format(phase_id)
                except ValueError:      # Phase ID is None.
                    _msg = _msg + "  Failed to delete Phase ID {0:s} from "\
                            "the RTK Program database.".format(phase_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to delete non-existent Phase ID {0:d}.".\
                    format(phase_id)
            except ValueError:      # Phase ID is None.
                _msg = "Attempted to delete non-existent Phase ID {0:s}.". \
                    format(phase_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_phase(self, phase_id):
        """
        Method to update the phase associated with Phase ID to the RTK
        Program database.

        :param int phase_id: the Phase ID to save to the RTK Program
                             database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _phase = self.dicPhase[phase_id]

            (_error_code, _msg) = self.dao.db_update()

            if _error_code == 0:
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to save Phase ID {0:d} to the \
                                   RTK Program database".format(phase_id)
                except ValueError:      # If the phase_id = None.
                    _msg = _msg + "  Failed to save Phase ID {0:s} to the \
                                   RTK Program database".format(phase_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to save non-existent Phase ID {0:d}.".\
                    format(phase_id)
            except ValueError:          # If the phase_id = None.
                _msg = "Attempted to save non-existent Phase ID {0:s}.".\
                    format(phase_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_all_phases(self):
        """
        Method to save all Mission Phases to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        for _phase_id in self.dicPhase.keys():
            if self.save_phase(_phase_id):
                _return = True

        return _return


class Phase(object):
    """
    The Phase controller provides an interface between the Phase data model
    and an RTK view model.  A single Phase controller can control one or more
    Phase data models.  Currently the Phase controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Phase controller instance.
        """

        pass
