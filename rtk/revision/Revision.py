#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.revision.Revision.py is part of The RTK Project
#
# All rights reserved.

"""
############################
Revision Package Data Module
############################
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as Configuration
    import Utilities as Utilities
    from dao.DAO import RTKRevision
except ImportError:
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.Utilities as Utilities           # pylint: disable=E0401
    from rtk.dao.DAO import RTKRevision         # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):

    """
    The Revision data model contains the attributes and methods of a revision.
    An RTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:

    :cvar dict dicRevisions: dictionary containing all the RTKRevision models
                             that are part of the Revision tree.  Key is the
                             Revision ID; value is a pointer to the instance
                             of the RTKRevision model.

    :ivar int _last_id: the last Revision ID used in the RTK Program database.
    :ivar dao: the `:py:class:rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    # Define public class dictionary attributes.
    dicRevision = {}

    def __init__(self, dao):
        """
        Method to initialize a Revision data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._last_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = dao

    def retrieve(self, revision_id):
        """
        Method to retrieve the instance of the RTKRevision data model for the
        Revision ID passed.

        :param int revision_id: the ID Of the Revision to retrieve.
        :return: the instance of the RTKRevision class that was requested or
                 None if the requested Revision ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKRevision`
        """

        try:
            _revision = self.dicRevision[revision_id]
        except KeyError:
            _revision = None

        return _revision

    def retrieve_all(self, dao):
        """
        Method to retrieve all the Revisions from the RTK Program database.

        :return: dicRevision; the dictionary of RTKRevision data models that
                 comprise the Revision tree.
        :rtype: dict
        """

        self.dao = dao

        for _revision in self.dao.session.query(RTKRevision).all():
            self.dicRevision[_revision.revision_id] = _revision

        return self.dicRevision

    def add_revision(self):
        """
        Method to add a Revision to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _revision = RTKRevision()
        (_error_code, _msg) = self.dao.db_add(_revision)

        self._last_id = _revision.revision_id

        # If the add was successful add the new RTKRevision data model instance
        # to dicRevision and log the success message to the user log.
        # Otherwise, update the error message and write it to the error log.
        if _error_code == 0:
            self.dicRevision[_revision.revision_id] = _revision
            Configuration.RTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + "  Failed to add a new Revision to the RTK Program \
                           database."
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def delete_revision(self, revision_id):
        """
        Method to remove the revision associated with Revision ID.

        :param int revision_id: the ID of the Revision to be removed.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _revision = self.dicRevision[revision_id]

            (_error_code, _msg) = self.dao.db_delete(_revision)

            if _error_code == 0:
                self.dicRevision.pop(revision_id)
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to delete Revision ID {0:d} from "\
                            "the RTK Program database.".format(revision_id)
                except ValueError:      # Revision ID is None.
                    _msg = _msg + "  Failed to delete Revision ID {0:s} from "\
                            "the RTK Program database.".format(revision_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to delete non-existent Revision ID {0:d}.".\
                    format(revision_id)
            except ValueError:      # Revision ID is None.
                _msg = "Attempted to delete non-existent Revision ID {0:s}.". \
                    format(revision_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_revision(self, revision_id):
        """
        Method to update the revision associated with Revision ID to the RTK
        Program database.

        :param int revision_id:
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        try:
            _revision = self.dicRevision[revision_id]

            (_error_code, _msg) = self.dao.db_update()

            if _error_code == 0:
                Configuration.RTK_USER_LOG.info(_msg)
            else:
                try:
                    _msg = _msg + "  Failed to save Revision ID {0:d} to the \
                                   RTK Program database".format(revision_id)
                except ValueError:      # If the revision_id = None.
                    _msg = _msg + "  Failed to save Revision ID {0:s} to the \
                                   RTK Program database".format(revision_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                _return = True
        except KeyError:
            try:
                _msg = "Attempted to save non-existent Revision ID {0:d}.".\
                    format(revision_id)
            except ValueError:          # If the revision_id = None.
                _msg = "Attempted to save non-existent Revision ID {0:s}.".\
                    format(revision_id)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def save_all_revisions(self):
        """
        Method to save all Revisions to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        for _revision_id in self.dicRevision.keys():
            if self.save_revision(_revision_id):
                _return = True

        return _return

    def calculate(self, revision_id, mission_time):
        """
        Method to calculate various attributes for the requested Revision.

        :param int revision_id: the Revision ID to get attributes for.
        :param float mission_time: the Mission Time to calculate the various
                                   Revision attributes for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _revision = self.dicRevision[revision_id]

        if(_revision.calculate_reliability(mission_time) or
               _revision.calculate_availability() or
               _revision.calculate_costs(mission_time)):
            _return = True

        return _return


class Revision(object):
    """
    The Revision data controller provides an interface between the Revision
    data model and an RTK view model.  A single Revision controller can manage
    one or more Revision data models.  The attributes of a Revision data
    controller are:

    :ivar revision_model: the `:py:class:rtk.Revision.Model` associated with
                          the Revision Data Controller.
    """

    def __init__(self, dao, page=-1, **kwargs):
        """
        Method to initialize a Revision data controller instance.

        :param dao: the `:py:class:rtk.dao.DAO` instance to pass to the
                    Revision Data Model.
        :keyword int page: the position in the ModuleBook to place the Revision
                           ModuleView page.  Defaults to -1 (the end).
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.moduleview = ModuleView(page, kwargs['modulebook'])
        self.revision_model = Model(dao)
        self.workview = WorkView(kwargs['workbook'])

    def request_revision(self, revision_id):
        """
        Method to request the Revision Data Model to retrive the RTKRevision
        model associated with the Revision ID.

        :param int revision_id: the Revision ID to retrieve.
        :return: the RTKRevision model requested.
        :rtype: `:py:class:rtk.dao.DAO.RTKRevision` model
        """

        return self.revision_model.retrieve(revision_id)

    def request_revision_tree(self):
        """
        Method to retrieve the Revision tree from the Revision Data Model.

        :return: dicRevision; the dictinary of RTKRevision models in the
                 Revision tree.
        :rtype: dict
        """

        return self.revision_model.retrieve_all()

    def request_add_revision(self):
        """
        Method to request the Revision Data Model to add a new Revision to the
        RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self.revision_model.add_revision()

    def request_delete_revision(self, revision_id):
        """
        Method to request the Revision Data Model to delete a Revision from the
        RTK Program database.

        :param int revision_id: the Revision ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self.revision_model.delete_revision(revision_id)

    def request_save_revision(self, revision_id):
        """
        Method to request the Revision Data Model save the RTKRevision
        attributes to the RTK Program database.

        :param int revision_id: the ID of the revision to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self.revision_model.save_revision(revision_id)

    def request_save_all_revisions(self):
        """
        Method to request the Revision Data Model to save all RTKRevision
        model attributes to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self.revision_model.save_all_revisions()

    def request_calculate_revision(self, revision_id, mission_time):
        """
        Method to request reliability, availability, and cost attributes be
        calculated for the Revision ID passed.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the calculations.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self.revision_model.calculate(revision_id, mission_time)
