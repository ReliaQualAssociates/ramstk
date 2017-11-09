# -*- coding: utf-8 -*-
#
#       rtk.stakeholder.Stakeholder.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Stakeholder Package Data Module
###############################################################################
"""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel  # pylint: disable=E0401
from datamodels import RTKDataController  # pylint: disable=E0401
from dao import RTKStakeholder  # pylint: disable=E0401


class Model(RTKDataModel):
    """
    The Stakeholder data model contains the attributes and methods of a
    stakeholder input.  A :class:`rtk.requirement.Requirement` will consist
    of one or more Stakeholder inputs.  The attributes of a Stakeholder are:

    :ivar int _revision_id: the ID of the :class:`rtk.revision.Revision` the
                            Stakeholder input is associated with.
    """

    _tag = 'Stakeholders'

    def __init__(self, dao):
        """
        Method to initialize a Stakeholder data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, stakeholder_id):
        """
        Method to retrieve the instance of the RTKStakeholder data model for
        the Stakeholder ID passed.

        :param int stakeholder_id: the ID Of the Stakeholder input to retrieve.
        :return: the instance of the RTKStakeholder class that was requested or
                 None if the requested Stakeholder ID does not exist.
        :rtype: :class:`rtk.dao.RTKStakeholder.RTKStakeholder`
        """

        return RTKDataModel.select(self, stakeholder_id)

    def select_all(self, revision_id):
        """
        Method to retrieve all the Stakeholders from the RTK Program database.
        Then add each to the treelib Tree().

        :param int revision_id: the ID of the Revision to retrieve all the
                                Stakeholder inputs for.
        :return: tree; the Tree() of RTKStakeholder data models.
        :rtype: :class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _stakeholder in _session.query(RTKStakeholder).filter(
                RTKStakeholder.revision_id == revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _stakeholder.get_attributes()
            _stakeholder.set_attributes(_attributes[2:])
            self.tree.create_node(
                _stakeholder.description,
                _stakeholder.stakeholder_id,
                parent=0,
                data=_stakeholder)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _stakeholder.stakeholder_id)

        _session.close()

        self._revision_id = revision_id

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Stakeholder input to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _stakeholder = RTKStakeholder()
        _stakeholder.revision_id = kwargs['revision_id']

        _error_code, _msg = RTKDataModel.insert(self, [
            _stakeholder,
        ])

        if _error_code == 0:
            self.tree.create_node(
                _stakeholder.description,
                _stakeholder.stakeholder_id,
                parent=0,
                data=_stakeholder)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _stakeholder.stakeholder_id

        return _error_code, _msg

    def delete(self, stakeholder_id):
        """
        Method to remove the Stakeholder associated with Stakeholder ID.

        :param int stakeholder_id: the ID of the Stakeholder to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _stakeholder = self.tree.get_node(stakeholder_id).data
            _error_code, _msg = RTKDataModel.delete(self, _stakeholder)

            if _error_code == 0:
                self.tree.remove_node(stakeholder_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Stakeholder ' \
                   'ID {0:d}.'.format(stakeholder_id)

        return _error_code, _msg

    def update(self, stakeholder_id):
        """
        Method to update the stakeholder input associated with Stakeholder ID
        to the RTK Program database.

        :param int stakeholder_id: the Stakeholder ID of the stakeholder input
                                   to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, stakeholder_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Stakeholder ' \
                   'ID {0:d}.'.format(stakeholder_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Stakeholders to the RTK Program database.

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
                          'rtk.stakeholder.Stakeholder.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.stakeholder.Stakeholder.Model.update_all().'

        return _error_code, _msg

    def calculate_weight(self, stakeholder_id):
        """
        Method to calculate the improvement factor and overall weighting of a
        Stakeholder input.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _stakeholder = self.tree.get_node(stakeholder_id).data

        _stakeholder.improvement = 1.0 + 0.2 * (
            _stakeholder.planned_rank - _stakeholder.customer_rank)
        _stakeholder.overall_weight = float(_stakeholder.priority) * \
            _stakeholder.improvement * _stakeholder.user_float_1 * \
            _stakeholder.user_float_2 * _stakeholder.user_float_3 * \
            _stakeholder.user_float_4 * _stakeholder.user_float_5

        return _return


class Stakeholder(RTKDataController):
    """
    The Stakeholder data controller provides an interface between the
    Stakeholder data model and an RTK view model.  A single Stakeholder
    controller can manage one or more Stakeholder data models.  The attributes
    of a Stakeholder data controller are:

    :ivar __test: control variable used to suppress certain code during
                  testing.
    :ivar _dtm_stakeholder: the :class:`rtk.Stakeholder.Model` associated
                            with the Stakeholder Data Controller.
    :ivar _configuration: the :class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Stakeholder data controller instance.
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_stakeholder = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, stakeholder_id):
        """
        Method to request the Stakeholder Data Model to retrieve the
        RTKStakeholder model associated with the Stakeholder ID.

        :param int revision_id: the Stakeholder ID to retrieve.
        :return: the RTKStakeholder model requested.
        :rtype: `:class:rtk.dao.DAO.RTKStakeholder` model
        """

        return self._dtm_stakeholder.select(stakeholder_id)

    def request_select_all(self, revision_id):
        """
        Method to retrieve the Stakeholder tree from the Stakeholder Data
        Model.

        :param int revision_id: the ID of the Revision the requested
                                Stakeholder inputs are associated with.
        :return: tree; the treelib Tree() of RTKStakeholder models in the
                 Stakeholder tree.
        :rtype: dict
        """

        return self._dtm_stakeholder.select_all(revision_id)

    def request_insert(self, revision_id):
        """
        Method to request the Stakeholder Data Model to add a new Stakeholder
        to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_stakeholder.insert(
            revision_id=revision_id)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedStakeholder',
                stakeholder_id=self._dtm_stakeholder.last_id)
        else:
            _msg = _msg + '  Failed to add a new Stakeholder to the RTK ' \
                'Program database.'

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_delete(self, stakeholder_id):
        """
        Method to request the Stakeholder Data Model to delete a Stakeholder
        from the RTK Program database.

        :param int stakeholder_id: the Stakeholder ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_stakeholder.delete(stakeholder_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'deletedStakeholder')

    def request_update(self, stakeholder_id):
        """
        Method to request the Stakeholder Data Model save the RTKStakeholder
        attributes to the RTK Program database.

        :param int stakeholder_id: the ID of the Stakeholder to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_stakeholder.update(stakeholder_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'savedStakeholder')

    def request_update_all(self):
        """
        Method to request the Stakeholder Data Model to save all RTKStakeholder
        model attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = self._dtm_stakeholder.update_all()

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_calculate_weight(self, stakeholder_id):
        """
        Method to request the model calculate the Stakeholder input.

        :param int stakeholder_id: the Stakholder ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtm_stakeholder.calculate_weight(stakeholder_id)
