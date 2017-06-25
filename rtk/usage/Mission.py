#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.Mission.py is part of The RTK Project
#
# All rights reserved.

"""
##############
Mission Module
##############
"""

# Import other RTK modules.
try:
    import Configuration as Configuration
    import Utilities as Utilities
    from dao.DAO import RTKMission
except ImportError:
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.Utilities as Utilities           # pylint: disable=E0401
    from rtk.dao.DAO import RTKMission          # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Mission data model contains the attributes and methods of a mission.
    A Usage Profile will consist of one or more missions.  The attributes of a
    Mission are:

    :cvar dict dicMission: dictionary containing all the RTKMission models
                           that are part of the Mission tree.  Key is the
                           Mission ID; value is a pointer to the instance
                           of the RTKMission model.

    :ivar int last_id: the last Mission ID used in the RTK Program database.
    :ivar dao: the `:py:class:rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    # Define public class dictionary attributes.
    dicMission = {}

    def __init__(self):
        """
        Method to initialize a Mission data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None
        self.last_id = None

    def retrieve(self, mission_id):
        """
        Method to retrieve the instance of the RTKMission data model for the
        Mission ID passed.

        :param int mission_id: the ID Of the RTKMission to retrieve.
        :return: the instance of the RTKMission class that was requested or
                 None if the requested Mission ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKMission.Model`
        """

        try:
            _mission = self.dicMission[mission_id]
        except KeyError:
            _mission = None

        return _mission

    def retrieve_all(self, dao, revision_id):
        """
        Method to retrieve all the RTKMissions from the RTK Program database.

        :param dao: the `:py:class:dao.DAO.DAO` instance connected to the RTK
                    Program database.
        :param int revision_id: the ID of the Revision to retrieve the Mission.
        :return: dicMission; the dictionary of RTKMission data models that
                 comprise the Mission tree.
        :rtype: dict
        """

        self.dao = dao

        # Clear the Mission dictionary of previous Revision's Missions.
        self.dicMission = {}
        for _mission in self.dao.session.query(RTKMission).\
                filter(RTKMission.revision_id == revision_id).all():
            self.dicMission[_mission.mission_id] = _mission

        return self.dicMission

    def add_mission(self, revision_id):
        """
        Method to add a Mission to the RTK Program database for Revision ID.

        :param int revision_id: the Revision ID to add the Mission to.
        :return: _mission
        :rtype: `:py:test:rtk.dao.DAO.RTKMission`
        """

        _mission = RTKMission()
        _mission.revision_id = revision_id

        (_error_code, _msg) = self.dao.db_add(_mission)

        # If the add was successful add the new RTKMission data model instance
        # to dicMission and log the success message to the user log.
        # Otherwise, update the error message and write it to the error log.
        if _error_code == 0:
            self.last_id = _mission.mission_id
            self.dicMission[_mission.mission_id] = _mission
            Configuration.RTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + "  Failed to add a new Mission to the RTK Program \
                           database."
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _mission = None

        return _mission

    def delete_mission(self, mission_id):
        """
        Method to remove the mission associated with Mission ID.

        :param int mission_id: the ID of the Mission to be removed.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _mission = self.dicMission[mission_id]

            (_error_code, _msg) = self.dao.db_delete(_mission)

            if _error_code == 0:
                self.dicMission.pop(mission_id)
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to delete Mission ID {0:d} from " \
                            "the RTK Program database.".format(mission_id)
                except ValueError:      # Mission ID is None.
                    _msg = _msg + "  Failed to delete Mission ID {0:s} from "\
                            "the RTK Program database.".format(mission_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to delete non-existent Mission ID {0:d}.".\
                    format(mission_id)
            except ValueError:      # Mission ID is None.
                _msg = "Attempted to delete non-existent Mission ID {0:s}.". \
                    format(mission_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_mission(self, mission_id):
        """
        Method to update the mission associated with Mission ID to the RTK
        Program database.

        :param int mission_id: the Mission ID to save to the RTK Program
                               database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _mission = self.dicMission[mission_id]

            (_error_code, _msg) = self.dao.db_update()

            if _error_code == 0:
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to save Mission ID {0:d} to the \
                                   RTK Program database".format(mission_id)
                except ValueError:      # If the revision_id = None.
                    _msg = _msg + "  Failed to save Mission ID {0:s} to the \
                                   RTK Program database".format(mission_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to save non-existent Mission ID {0:d}.".\
                    format(mission_id)
            except ValueError:          # If the revision_id = None.
                _msg = "Attempted to save non-existent Mission ID {0:s}.".\
                    format(mission_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_all_missions(self):
        """
        Method to save all Missions to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        for _mission_id in self.dicMission.keys():
            if self.save_mission(_mission_id):
                _return = True

        return _return


class Mission(object):
    """
    The Mission controller provides an interface between the Mission data model
    and an RTK view model.  A single Mission controller can control one or more
    Mission data models.  Currently the Mission controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Mission controller instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        pass
