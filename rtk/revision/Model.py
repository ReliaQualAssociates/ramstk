# -*- coding: utf-8 -*-
#
#       rtk.revision.Revision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Revision Package Data Model Module
===============================================================================
"""

# Import other RTK modules.
from datamodels import RTKDataModel  # pylint: disable=E0401
from dao import RTKRevision  # pylint: disable=E0401


class RevisionDataModel(RTKDataModel):
    """
    The Revision data model contains the attributes and methods of a revision.
    An RTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:
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

    def select_all(self, revision_id):
        """
        Method to retrieve all the Revisions from the RTK Program database.
        Then add each to

        :param int revision_id: unused, only required for compatibility with
                                underlying RTKDataModel.
        :return: tree; the Tree() of RTKRevision data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self, revision_id)

        for _revision in _session.query(RTKRevision).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _revision.get_attributes()
            _revision.set_attributes(_attributes[2:])
            self.tree.create_node(
                _revision.name,
                _revision.revision_id,
                parent=0,
                data=_revision)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _revision.revision_id)

        _session.close()

        return self.tree

    def insert(self, entities):     # pylint: disable=unused-argument
        """
        Method to add a Revision to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _revision = RTKRevision()
        _error_code, _msg = RTKDataModel.insert(self, [
            _revision,
        ])

        if _error_code == 0:
            self.tree.create_node(
                _revision.name,
                _revision.revision_id,
                parent=0,
                data=_revision)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _revision.revision_id

        return _error_code, _msg

    def delete(self, node_id):
        """
        Base method to remove the instance of RTK<Module> from the RTK Program
        database.

        :param int node_id entity: the ID of the RTK<Module> record to be
                                   removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.delete(self, node_id)

        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Revision ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update(self, node_id):
        """
        Method to update the revision associated with Revision ID to the RTK
        Program database.

        :param int node_id: the Revision ID of the Revision to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Revision ID ' \
                   '{0:d}.'.format(node_id)

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

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.revision.Revision.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.revision.Revision.Model.update_all().'

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
        _revision.hazard_rate_logistics = (
            _revision.hazard_rate_active + _revision.hazard_rate_dormant +
            _revision.hazard_rate_software)

        # Calculate the logistics MTBF.
        try:
            _revision.mtbf_logistics = 1.0 / _revision.hazard_rate_logistics
        except (ZeroDivisionError, OverflowError):
            _revision.mtbf_logistics = 0.0
            _error_code = 2008
            _msg = 'RTK ERROR: Zero Division or Overflow Error when ' \
                   'calculating the logistics MTBF for Revision ID ' \
                   '{0:d}.  Logistics hazard rate: {1:f}.'. \
                format(_revision.revision_id, _revision.hazard_rate_logistics)

        # Calculate the mission MTBF.
        try:
            _revision.mtbf_mission = 1.0 / _revision.hazard_rate_mission
        except (ZeroDivisionError, OverflowError):
            _revision.mtbf_mission = 0.0
            _error_code = 2008
            _msg = 'RTK ERROR: Zero Division or Overflow Error when ' \
                   'calculating the mission MTBF for Revision ID ' \
                   '{0:d}.  Mission hazard rate: {1:f}.'. \
                format(_revision.revision_id, _revision.hazard_rate_logistics)

        # Calculate reliabilities.
        _revision.reliability_logistics = exp(
            -1.0 * _revision.hazard_rate_logistics * mission_time / multiplier)
        _revision.reliability_mission = exp(
            -1.0 * _revision.hazard_rate_mission * mission_time / multiplier)

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
            _revision.availability_logistics = (_revision.mtbf_logistics / (
                _revision.mtbf_logistics + _revision.mttr))
        except (ZeroDivisionError, OverflowError):
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
            _revision.availability_mission = (_revision.mtbf_mission / (
                _revision.mtbf_mission + _revision.mttr))
        except (ZeroDivisionError, OverflowError):
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

        _revision.cost_failure = (
            _revision.cost * _revision.hazard_rate_logistics)
        try:
            _revision.cost_hour = _revision.cost / mission_time
        except (ZeroDivisionError, OverflowError):
            _revision.cost_hour = 0.0
            _error_code = 2010
            _msg = 'RTK ERROR: Zero Division Error or Overflow Error when ' \
                   'calculating the cost per mission hour for Revision ID ' \
                   '{0:d}.  Mission time: {1:f}.'. \
                format(_revision.revision_id, mission_time)

        return _error_code, _msg
