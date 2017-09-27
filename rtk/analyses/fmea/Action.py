# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Action.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
FMEA Action Module
###############################################################################
"""

from pubsub import pub                          # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel             # pylint: disable=E0401
from datamodels import RTKDataController        # pylint: disable=E0401
from dao.RTKAction import RTKAction             # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class Model(RTKDataModel):
    """
    The Action data model contains the attributes and methods of a FMEA
    action.  A Mechanism or a Cause will contain of one or more Actions.
    """

    _tag = 'Actions'

    def __init__(self, dao):
        """
        Method to initialize an Action data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.last_id = None

    def select(self, action_id):
        """
        Method to retrieve the instance of the RTKAction data model for the
        Action ID passed.

        :param int action_id: the ID Of the Action to retrieve.
        :return: the instance of the RTKAction class that was requested or
                 None if the requested Action ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKAction.RTKAction`
        """

        return RTKDataModel.select(self, action_id)

    def _select_all(self, parent_id, functional):
        """
        Helper method to retrieve all the Actions.

        :param int parent_id: the Mode ID (functional FMEA) or the Cause ID
                              (hardware FMEA) to select the Controls for.
        :param bool functional: indicates whether the Controls are for a
                                functional FMEA or a hardware FMEA (default).
        """

        _session = RTKDataModel.select_all(self)

        if functional:
            _actions = _session.query(RTKAction).filter(RTKAction.mode_id ==
                                                        parent_id).all()
        else:
            _actions = _session.query(RTKAction).filter(RTKAction.cause_id ==
                                                        parent_id).all()

        _session.close()

        return _actions

    def select_all(self, parent_id, functional=False):
        """
        Method to retrieve all the Actions from the RTK Program database.
        Then add each to the Mode treelib Tree().

        :param int parent_id: the MOde ID (for a functional FMEA) or the
                              Cause ID (for a hardware FMEA) to select the
                              Actions for.
        :param bool functional: indicates whether to return Functional
                                failure modes or Hardware failure modes.
        :return: tree; the Tree() of RTKAction data models.
        :rtype: :py:class:`treelib.Tree`
        """

        for _action in self._select_all(parent_id, functional):
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _action.get_attributes()
            _action.set_attributes(_attributes[3:])
            self.tree.create_node(_action.action_due_date, _action.action_id,
                                  parent=0, data=_action)
            self.last_id = max(self.last_id, _action.action_id)

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Mode to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _action = RTKAction()
        _action.mode_id = kwargs['mode_id']
        _action.cause_id = kwargs['cause_id']
        _error_code, _msg = RTKDataModel.insert(self, [_action, ])

        if _error_code == 0:
            self.tree.create_node(_action.action_due_date, _action.action_id,
                                  parent=0, data=_action)
            self.last_id = max(self.last_id, _action.action_id)

        return _error_code, _msg

    def delete(self, action_id):
        """
        Method to remove the action associated with Action ID.

        :param int action_id: the ID of the Action to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _action = self.tree.get_node(action_id).data
            _error_code, _msg = RTKDataModel.delete(self, _action)

            if _error_code == 0:
                self.tree.remove_node(action_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Action ' \
                   'ID {0:d}.'.format(action_id)

        return _error_code, _msg

    def update(self, action_id):
        """
        Method to update the action associated with Action ID to the RTK
        Program database.

        :param int action_id: the Action ID of the Action to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, action_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Action ID ' \
                   '{0:d}.'.format(action_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Actions to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Saving all Actions in the FMEA.'

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.action_id)

                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.analyses.fmea.Action.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.analyses.fmea.Action.Model.update_all().'

        return _error_code, _msg


class Action(RTKDataController):
    """
    The Action data controller provides an interface between the Action data
    model and an RTK view model.  A single Action controller can control one
    or more Action data models.  Action data controller attributes are:

    :ivar _dtm_action: the :py:class:`rtk.analyses.fmea.Action.Model` data
                       model associated with this data controller.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Action data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Mode Data
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
        self._dtm_action = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, action_id):
        """
        Method to request the Action Data Model to retrieve the RTKAction
        model associated with the Action ID.

        :param int action_id: the Action ID to retrieve.
        :return: the RTKAction model requested.
        :rtype: `:py:class:rtk.dao.DAO.RTKAction` model
        """

        return self._dtm_action.select(action_id)

    def request_select_all(self, parent_id, functional=False):
        """
        Method to retrieve the Action tree from the Action Data Model.

        :param int parent_id: the Mode ID (functional FMEA) or Cause ID
                              (hardware FMEA) to select the Actions for.
        :param bool functional: indicates whether or not to select the Modes
                                for a functional FMEA or hardware FMEA
                                (default).
        :return: tree; the treelib Tree() of RTKAction models in the
                 Action tree.
        :rtype: dict
        """

        return self._dtm_action.select_all(parent_id, functional)

    def request_insert(self, mode_id, cause_id):
        """
        Method to request the Action Data Model to add a new Action to the
        RTK Program database.

        :param int mode_id: the ID of the Mode the new Action is to be
                            associated with.
        :param int cause_id: the ID of the Cause the new Action is to be
                             associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_action.insert(mode_id=mode_id,
                                                    cause_id=cause_id)

        if _error_code == 0 and not self._test:
            _parent_id = max(mode_id, cause_id)
            pub.sendMessage('insertedAction',
                            action_id=self._dtm_action.last_id,
                            parent_id=_parent_id)
        else:
            _msg = _msg + '  Failed to add a new Action to the RTK ' \
                'Program database.'

        return RTKDataController.request_insert(self, _error_code, _msg)

    def request_delete(self, action_id):
        """
        Method to request the Action Data Model to delete an Action from the
        RTK Program database.

        :param int action_id: the ID of the Action to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_action.delete(action_id)

        return RTKDataController.request_delete(self, _error_code, _msg,
                                                'deletedAction')

    def request_update(self, action_id):
        """
        Method to request the Action Data Model save the RTKAction
        attributes to the RTK Program database.

        :param int action_id: the ID of the action to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_action.update(action_id)

        return RTKDataController.request_update(self, _error_code, _msg,
                                                'savedAction')

    def request_update_all(self):
        """
        Method to request the Action Data Model to save all RTKAction
        model attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        return self._dtm_action.update_all()
