# -*- coding: utf-8 -*-
#
#       rtk.requirement.Requirement.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Requirement Package
===============================================================================
"""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel  # pylint: disable=E0401
from datamodels import RTKDataMatrix  # pylint: disable=E0401
from datamodels import RTKDataController  # pylint: disable=E0401
from dao import RTKRequirement, RTKHardware, RTKSoftware, RTKValidation  # pylint: disable=E0401


class Model(RTKDataModel):
    """
    The Requirement data model contains the attributes and methods of a
    requirement.  A :class:`rtk.revision.Revision` will consist of one or
    more Requirements.  The attributes of a Requirement are:
    """

    _tag = 'requirement'

    def __init__(self, dao):
        """
        Method to initialize a Requirement data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, requirement_id):
        """
        Method to retrieve the instance of the RTKRequirement data model for
        the Requirement ID passed.

        :param int requirement_id: the ID Of the Requirement to retrieve.
        :return: the instance of the RTKRequirement class that was requested or
                 None if the requested Requirement ID does not exist.
        :rtype: :class:`rtk.dao.RTKRequirement.RTKRequirement`
        """

        return RTKDataModel.select(self, requirement_id)

    def select_all(self, revision_id):
        """
        Method to retrieve all the Requirements from the RTK Program database.
        Then add each to

        :param int revision_id: the Revision ID to select the Requirements for.
        :return: tree; the Tree() of RTKRequirement data models.
        :rtype: :class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _requirement in _session.query(RTKRequirement).filter(
                RTKRequirement.revision_id == revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _requirement.get_attributes()
            _requirement.set_attributes(_attributes[2:])
            self.tree.create_node(
                _requirement.requirement_code,
                _requirement.requirement_id,
                parent=_requirement.parent_id,
                data=_requirement)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _requirement.requirement_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Requirement to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _requirement = RTKRequirement()
        _requirement.revision_id = kwargs['revision_id']
        _requirement.parent_id = kwargs['parent_id']
        _error_code, _msg = RTKDataModel.insert(self, [
            _requirement,
        ])

        if _error_code == 0:
            self.tree.create_node(
                _requirement.requirement_code,
                _requirement.requirement_id,
                parent=_requirement.parent_id,
                data=_requirement)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _requirement.requirement_id

        return _error_code, _msg

    def delete(self, requirement_id):
        """
        Method to remove the Requirement associated with Requirement ID.

        :param int requirement_id: the ID of the Requirement to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _requirement = self.tree.get_node(requirement_id).data
            _error_code, _msg = RTKDataModel.delete(self, _requirement)

            if _error_code == 0:
                self.tree.remove_node(requirement_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Requirement ' \
                   'ID {0:d}.'.format(requirement_id)

        return _error_code, _msg

    def update(self, requirement_id):
        """
        Method to update the Requirement associated with Requirement ID to the
        RTK Program database.

        :param int requirement_id: the Requirement ID of the Requirement to
                                   save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, requirement_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Requirement ' \
                   'ID {0:d}.'.format(requirement_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Requirements to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Saving all Requirements.'

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.requirement_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.requirement.Requirement.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.requirement.Requirement.Model.update_all().'

        return _error_code, _msg


class Requirement(RTKDataController):
    """
    The Requirement data controller provides an interface between the
    Requirement data model and an RTK view model.  A single Requirement
    controller can manage one or more Requirement data models.  The attributes
    of a Requirement data controller are:

    :ivar _dtm_data_model: the Requirement Data Model being used by this
                            controller.
    :ivar _dmx_rqmt_hw_matrix: the Requirement:Hardware Data Matrix being used
                               by this controller.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Requirement data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Requirement
                    Data Model.
        :type dao: :class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(
            self, configuration, module=Model(dao), **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_rqmt_hw_matrix = RTKDataMatrix(dao, RTKRequirement,
                                                 RTKHardware)
        self._dmx_rqmt_sw_matrix = RTKDataMatrix(dao, RTKRequirement,
                                                 RTKSoftware)
        self._dmx_rqmt_val_matrix = RTKDataMatrix(dao, RTKRequirement,
                                                  RTKValidation)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select_all_matrix(self, revision_id, matrix_id):
        """
        Method to retrieve all the Matrices associated with the Requirement
        module.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_id: the ID of the Matrix to retrieve.  Current matrix
                              IDs are:

                              11 = Requirement:Hardware
                              12 = Requirement:Software
                              13 = Requirement:Validation

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """

        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_id == 11:
            self._dmx_rqmt_hw_matrix.select_all(
                revision_id,
                matrix_id,
                rindex=1,
                cindex=1,
                rheader=9,
                cheader=6)
            _matrix = self._dmx_rqmt_hw_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_hw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_hw_matrix.dic_row_hdrs

        elif matrix_id == 12:
            self._dmx_rqmt_sw_matrix.select_all(
                revision_id,
                matrix_id,
                rindex=1,
                cindex=1,
                rheader=9,
                cheader=3)
            _matrix = self._dmx_rqmt_sw_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_sw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_sw_matrix.dic_row_hdrs

        elif matrix_id == 13:
            self._dmx_rqmt_val_matrix.select_all(
                revision_id,
                matrix_id,
                rindex=1,
                cindex=1,
                rheader=9,
                cheader=3)
            _matrix = self._dmx_rqmt_val_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_val_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_val_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def request_insert(self, revision_id, parent_id, sibling=True):
        """
        Method to request the Requirement Data Model to add a new Requirement
        to the RTK Program database.

        :param int revision_id: the ID of the Revision to add the new
                                Requirement to.
        :param int parent_id: the ID of the parent Requirement to add the new
                              Requirement to.
        :keyword bool sibling: indicates whether or not to insert a sibling
                               (default) or child (derived) Requirement.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_error_code, _msg) = self._dtm_data_model.insert(
            revision_id=revision_id, parent_id=parent_id)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedRequirement',
                requirement_id=self._dtm_data_model.last_id,
                parent_id=parent_id,
                sibling=sibling)
        else:
            _msg = _msg + '  Failed to add a new Requirement to the RTK ' \
                'Program database.'

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_insert_matrix(self, matrix_id, item_id, heading, row=True):
        """
        Method to request the selected Requirement Data Matrix to add a new row
        or column to the Matrix.

        :param int matrix_id: the ID of the Matrix to retrieve.  Current matrix
                              IDs are:

                              11 = Requirement:Hardware
                              12 = Requirement:Software
                              13 = Requirement:Validation

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if matrix_id == 11:
            _error_code, _msg = self._dmx_rqmt_hw_matrix.insert(
                item_id, heading, row=row)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedMatrix',
                matrix_id=matrix_id,
                item_id=item_id,
                row=row)

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_delete(self, requirement_id):
        """
        Method to request the Requirement Data Model to delete a Requirement
        from the RTK Program database.

        :param int requirement_id: the Requirement ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_data_model.delete(requirement_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'deletedRequirement')

    def request_delete_matrix(self, matrix_id, item_id, row=True):
        """
        Method to request to remove a row or column from the selected
        Requirement Data Matrix.

        :param int matrix_id: the ID of the Matrix to retrieve.  Current matrix
                              IDs are:

                              11 = Requirement:Hardware
                              12 = Requirement:Software
                              13 = Requirement:Validation

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if matrix_id == 11:
            _error_code, _msg = self._dmx_rqmt_hw_matrix.delete(
                item_id, row=row)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'deletedMatrix')

    def request_update(self, requirement_id):
        """
        Method to request the Requirement Data Model save the RTKRequirement
        attributes to the RTK Program database.

        :param int requirement_id: the ID of the Requirement to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_data_model.update(requirement_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'savedRequirement')

    def request_update_matrix(self, revision_id, matrix_id):
        """
        Method to request the Requirement Data Matrix save the RTKRequirement
        attributes to the RTK Program database.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_id: the ID of the Matrix to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if matrix_id == 11:
            _error_code, _msg = self._dmx_rqmt_hw_matrix.update(
                revision_id, matrix_id)
        else:
            _error_code = 6
            _msg = 'RTK ERROR: Attempted to update non-existent matrix ' \
                   '{0:d}.'.format(matrix_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'savedMatrix')

    def request_update_all(self):
        """
        Method to request the Requirement Data Model to save all RTKRequirement
        model attributes to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.handle_results(self, _error_code, _msg, None)
