# -*- coding: utf-8 -*-
#
#       rtk.revision.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Import other RTK modules.
from datamodels import RTKDataModel  # pylint: disable=E0401
from dao import RTKRevision  # pylint: disable=E0401


class RevisionDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Revision.

    An RTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:
    """

    _tag = 'Revisions'

    def __init__(self, dao):
        """
        Initialize a Revision data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, revision_id):  # pylint: disable=unused-argument
        """
        Retrieve all the Revisions from the RTK Program database.

        This method retrieves all the records from the RTKRevision table in the
        connected RTK Program database.  It then add each to the Revision data
        model treelib.Tree().

        :param int revision_id: unused, only required for compatibility with
                                underlying RTKDataModel.
        :return: tree; the Tree() of RTKRevision data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        for _revision in _session.query(RTKRevision).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _revision.get_attributes()
            _revision.set_attributes(_attributes)
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

    def insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RTKRevision table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = RTKRevision()
        _error_code, _msg = RTKDataModel.insert(self, entities=[
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
        Remove a record from the RTKRevision table.

        :param int node_id entity: the ID of the RTKRevision record to be
                                   removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Revision ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

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
        Update all RTKRevision table records in the RTK Program database.

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
                          'rtk.revision.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.revision.Model.update_all().'

        return _error_code, _msg

    def calculate_hazard_rate(self, revision_id):
        """
        Calculate the hazard rate metrics.

        This method calculates the active, dormant, software, logistics, and
        mission hazard rates.

        :param int revision_id: the ID of the Revision record to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = self.tree.get_node(revision_id).data

        return _revision.calculate_hazard_rate()

    def calculate_mtbf(self, revision_id):
        """
        Calculate the MTBF metrics.

        This method calculates the logistics and mission mean time between
        failures (MTBF).

        :param int revision_id: the ID of the Revision record to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = self.tree.get_node(revision_id).data

        return _revision.calculate_mtbf()

    def calculate_reliability(self, revision_id, mission_time, multiplier):
        """
        Calculate reliability metrics.

        This method calculates the logistics and mission reliability.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the reliability
                                   calculations.
        :param float multiplier: the hazard rate multiplier.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = self.tree.get_node(revision_id).data

        return _revision.calculate_reliability(mission_time, multiplier)

    def calculate_availability(self, revision_id):
        """
        Calculate the availability metrics.

        This method calculate logistics and mission availability.

        :param int revision_id: the Revision ID to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = self.tree.get_node(revision_id).data

        return _revision.calculate_availability()

    def calculate_costs(self, revision_id, mission_time):
        """
        Calculate the cost metrics.

        This method calculates the total cost, cost per failure, and cost per
        operating hour.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time over which to calculate costs.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = self.tree.get_node(revision_id).data

        return _revision.calculate_costs(mission_time)
