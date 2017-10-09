# -*- coding: utf-8 -*-
#
#       rtk.revision.Revision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Revision Package Data Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub

# Import other RTK modules.
from datamodels import RTKDataModel                 # pylint: disable=E0401
from datamodels import RTKDataController            # pylint: disable=E0401
from dao import RTKRevision                         # pylint: disable=E0401

_ = gettext.gettext


class Model(RTKDataModel):
    """
    The Revision data model contains the attributes and methods of a revision.
    An RTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:

    :ivar int _last_id: the last Revision ID used in the RTK Program database.
    :ivar dao: the :py:class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    _tag = 'Revisions'

    def __init__(self, dao):
        """
        Method to initialize a Revision data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, revision_id):
        """
        Method to retrieve the instance of the RTKRevision data model for the
        Revision ID passed.

        :param int revision_id: the ID Of the Revision to retrieve.
        :return: the instance of the RTKRevision class that was requested or
                 None if the requested Revision ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKRevision.RTKRevision`
        """

        return RTKDataModel.select(self, revision_id)

    def select_all(self):
        """
        Method to retrieve all the Revisions from the RTK Program database.
        Then add each to

        :return: tree; the Tree() of RTKRevision data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _revision in _session.query(RTKRevision).all():
            self.tree.create_node(_revision.name, _revision.revision_id,
                                  parent=0, data=_revision)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Revision to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _revision = RTKRevision()
        _error_code, _msg = RTKDataModel.insert(self, [_revision, ])

        if _error_code == 0:
            self.tree.create_node(_revision.name, _revision.revision_id,
                                  parent=0, data=_revision)
            self._last_id = _revision.revision_id

        return _error_code, _msg

    def delete(self, revision_id):
        """
        Method to remove the revision associated with Revision ID.

        :param int revision_id: the ID of the Revision to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _revision = self.tree.get_node(revision_id).data
            _error_code, _msg = RTKDataModel.delete(self, _revision)

            if _error_code == 0:
                self.tree.remove_node(revision_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Revision ' \
                   'ID {0:d}.'.format(revision_id)

        return _error_code, _msg

    def update(self, revision_id):
        """
        Method to update the revision associated with Revision ID to the RTK
        Program database.

        :param int revision_id: the Revision ID of the Revision to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, revision_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Revision ID ' \
                   '{0:d}.'.format(revision_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Revisions to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.revision_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg

    def calculate_reliability(self, revision_id, mission_time, multiplier):
        """
        Method to calculate the active hazard rate, dormant hazard rate,
        software hazard rate, inherent hazard rate, mission hazard rate,
        MTBF, mission MTBF, inherent reliability, and mission reliability.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the reliability
                                   calculations.
        :param float multiplier: the hazard rate multiplier.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        from math import exp

        _revision = self.tree.get_node(revision_id).data

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating reliability metrics for Revision ' \
               'ID {0:d}.'.format(_revision.revision_id)

        # Calculate the logistics h(t).
        _revision.hazard_rate_logistics = (_revision.hazard_rate_active
                                           + _revision.hazard_rate_dormant
                                           + _revision.hazard_rate_software)

        # Calculate the logistics MTBF.
        try:
            _revision.mtbf_logistics = 1.0 / _revision.hazard_rate_logistics
        except(ZeroDivisionError, OverflowError):
            _revision.mtbf_logistics = 0.0
            _error_code = 2008
            _msg = 'RTK ERROR: Zero Division or Overflow Error when ' \
                   'calculating the logistics MTBF for Revision ID ' \
                   '{0:d}.  Logistics hazard rate: {1:f}.'. \
                format(_revision.revision_id, _revision.hazard_rate_logistics)

        # Calculate the mission MTBF.
        try:
            _revision.mtbf_mission = 1.0 / _revision.hazard_rate_mission
        except(ZeroDivisionError, OverflowError):
            _revision.mtbf_mission = 0.0
            _error_code = 2008
            _msg = 'RTK ERROR: Zero Division or Overflow Error when ' \
                   'calculating the mission MTBF for Revision ID ' \
                   '{0:d}.  Mission hazard rate: {1:f}.'. \
                format(_revision.revision_id, _revision.hazard_rate_logistics)

        # Calculate reliabilities.
        _revision.reliability_logistics = exp(-1.0
                                              * _revision.hazard_rate_logistics
                                              * mission_time / multiplier)
        _revision.reliability_mission = exp(-1.0
                                            * _revision.hazard_rate_mission
                                            * mission_time / multiplier)

        return _error_code, _msg

    def calculate_availability(self, revision_id):
        """
        Method to calculate the logistics availability and mission
        availability.

        :param int revision_id: the Revision ID to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _revision = self.tree.get_node(revision_id).data

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating availability metrics for Revision ' \
               'ID {0:d}.'.format(_revision.revision_id)

        # Calculate logistics availability.
        try:
            _revision.availability_logistics = (_revision.mtbf_logistics
                                                / (_revision.mtbf_logistics
                                                   + _revision.mttr))
        except(ZeroDivisionError, OverflowError):
            _revision.availability_logistics = 1.0
            _error_code = 2009
            _msg = 'RTK ERROR: Zero Division or Overflow Error when  ' \
                   'calculating the logistics availability for Revision ID ' \
                   '{0:d}.  Logistics MTBF: {1:f} and MTTR: {2:f}.'. \
                format(_revision.revision_id,
                       _revision.mtbf_logistics,
                       _revision.mttr)

        # Calculate mission availability.
        try:
            _revision.availability_mission = (_revision.mtbf_mission
                                              / (_revision.mtbf_mission
                                                 + _revision.mttr))
        except(ZeroDivisionError, OverflowError):
            _revision.availability_mission = 1.0
            _error_code = 2009
            _msg = 'RTK ERROR: Zero Division or Overflow Error when ' \
                   'calculating the mission availability for Revision ID ' \
                   '{0:d}.  Mission MTBF: {1:f} and MTTR: {2:f}.'. \
                format(_revision.revision_id,
                       _revision.mtbf_mission,
                       _revision.mttr)

        return _error_code, _msg

    def calculate_costs(self, revision_id, mission_time):
        """
        Method to calculate the total cost, cost per failure, and cost per
        operating hour.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time over which to calculate costs.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _revision = self.tree.get_node(revision_id).data

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating cost metrics for Revision ID ' \
               '{0:d}.'.format(_revision.revision_id)

        # Calculate costs.
        _revision.cost_failure = (_revision.cost
                                  * _revision.hazard_rate_logistics)
        try:
            _revision.cost_hour = _revision.cost / mission_time
        except(ZeroDivisionError, OverflowError):
            _revision.cost_hour = 0.0
            _error_code = 2010
            _msg = 'RTK ERROR: Zero Division Error or Overflow Error when ' \
                   'calculating the cost per mission hour for Revision ID ' \
                   '{0:d}.  Mission time: {1:f}.'. \
                format(_revision.revision_id, mission_time)

        return _error_code, _msg


class Revision(RTKDataController):
    """
    The Revision data controller provides an interface between the Revision
    data model and an RTK view model.  A single Revision controller can manage
    one or more Revision data models.  The attributes of a Revision data
    controller are:

    :ivar __test: control variable used to suppress certain code during
                  testing.
    :ivar _dtm_revision: the :py:class:`rtk.Revision.Model` associated with
                         the Revision Data Controller.
    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Revision data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Revision Data
                    Model.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.__test = kwargs['test']
        self._dtm_revision = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, revision_id):
        """
        Method to request the Revision Data Model to retrieve the RTKRevision
        model associated with the Revision ID.

        :param int revision_id: the Revision ID to retrieve.
        :return: the RTKRevision model requested.
        :rtype: `:py:class:rtk.dao.DAO.RTKRevision` model
        """

        return self._dtm_revision.select(revision_id)

    def request_select_all(self):
        """
        Method to retrieve the Revision tree from the Revision Data Model.

        :return: tree; the treelib Tree() of RTKRevision models in the
                 Revision tree.
        :rtype: dict
        """

        return self._dtm_revision.select_all()

    def request_insert(self):
        """
        Method to request the Revision Data Model to add a new Revision to the
        RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_revision.insert()

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('insertedRevision')
        else:
            _msg = _msg + '  Failed to add a new Revision to the RTK Program \
                           database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, revision_id):
        """
        Method to request the Revision Data Model to delete a Revision from the
        RTK Program database.

        :param int revision_id: the Revision ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_revision.delete(revision_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('deletedRevision')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update(self, revision_id):
        """
        Method to request the Revision Data Model save the RTKRevision
        attributes to the RTK Program database.

        :param int revision_id: the ID of the revision to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_revision.update(revision_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedRevision')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Revision Data Model to save all RTKRevision
        model attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        return self._dtm_revision.update_all()

    def request_calculate_reliability(self, revision_id, mission_time):
        """
        Method to request reliability attributes be calculated for the
        Revision ID passed.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the calculations.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_revision.calculate_reliability(
                revision_id, float(mission_time),
                float(self._configuration.RTK_HR_MULTIPLIER))

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('calculatedRevision')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_calculate_availability(self, revision_id):
        """
        Method to request availability attributes be calculated for the
        Revision ID passed.

        :param int revision_id: the Revision ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, \
            _msg = self._dtm_revision.calculate_availability(revision_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('calculatedRevision')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_calculate_costs(self, revision_id, mission_time):
        """
        Method to request cost attributes be calculated for the Revision ID
        passed.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the calculations.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_revision.calculate_costs(
                revision_id, float(mission_time))

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('calculatedRevision')
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return
