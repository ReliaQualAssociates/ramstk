# -*- coding: utf-8 -*-
#
#       ramstk.requirement.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Requirement Package Data Controller."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.dao.programdb import (
    RAMSTKRequirement, RAMSTKSoftware, RAMSTKValidation
)
from ramstk.models.programdb import RAMSTKHardware
from ramstk.modules import RAMSTKDataController, RAMSTKDataMatrix

# RAMSTK Local Imports
from . import dtmRequirement


class RequirementDataController(RAMSTKDataController):
    """
    Provide an interface between the Requirement data model and an RAMSTK View.

    A single Requirement controller can manage one or more Requirement data
    models.  The attributes of a Requirement data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Requirement data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the Requirement
                    Data Model.
        :type dao: :class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmRequirement(dao, **kwargs),
            ramstk_module='requirement',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_rqmt_hw_matrix = RAMSTKDataMatrix(
            dao,
            row_table=RAMSTKRequirement,
            column_table=RAMSTKHardware,
            **kwargs,
        )
        self._dmx_rqmt_sw_matrix = RAMSTKDataMatrix(
            dao,
            row_table=RAMSTKRequirement,
            column_table=RAMSTKSoftware,
            **kwargs,
        )
        self._dmx_rqmt_val_matrix = RAMSTKDataMatrix(
            dao,
            row_table=RAMSTKRequirement,
            column_table=RAMSTKValidation,
            **kwargs,
        )
        self._dic_inserts = {
            'rqrmnt_hrdwr': self._dmx_rqmt_hw_matrix.do_insert,
            'rqrmnt_sftwr': self._dmx_rqmt_sw_matrix.do_insert,
            'rqrmnt_vldtn': self._dmx_rqmt_val_matrix.do_insert,
        }

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._request_do_create_matrix,
            'request_create_requirement_matrix',
        )
        pub.subscribe(self.request_do_delete, 'request_delete_requirement')
        pub.subscribe(
            self._request_do_delete_matrix,
            'request_delete_requirement_matrix',
        )
        pub.subscribe(self.request_do_insert, 'request_insert_requirement')
        pub.subscribe(
            self.request_do_insert_matrix,
            'request_insert_requirement_matrix',
        )
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(
            self._request_do_select_all_matrix,
            'request_select_requirement_matrix',
        )
        pub.subscribe(self.request_do_update, 'request_update_requirement')
        pub.subscribe(
            self.request_do_update_all,
            'request_update_all_requirements',
        )
        pub.subscribe(
            self._request_do_update_matrix,
            'request_update_requirement_matrix',
        )
        pub.subscribe(self._request_set_attributes, 'mvw_editing_requirement')
        pub.subscribe(self._request_set_attributes, 'wvw_editing_requirement')

    def _request_do_create_matrix(self, revision_id, matrix_type):
        """
        Request to create or refresh a Requirement matrix.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
                                columns for.
        :return: None
        :rtype: None
        """
        _dic_creates = {
            'rqrmnt_hrdwr':
            [self._dmx_rqmt_hw_matrix.do_create, 'hardware_id'],
            'rqrmnt_sftwr':
            [self._dmx_rqmt_sw_matrix.do_create, 'software_id'],
            'rqrmnt_vldtn':
            [self._dmx_rqmt_val_matrix.do_create, 'validation_id'],
        }
        try:
            _create_method = _dic_creates[matrix_type][0]
            _col_id = _dic_creates[matrix_type][1]
        except KeyError:
            _create_method = None

        try:
            _create_method(
                revision_id, matrix_type, rkey='requirement_id', ckey=_col_id,
            )
        except TypeError:
            _error_code = 6
            _msg = 'RAMSTK ERROR: Failed to create matrix ' \
                   '{0:s}.'.format(matrix_type)

            RAMSTKDataController.do_handle_results(
                self, _error_code, _msg,
                None,
            )

    def _request_do_select_all_matrix(self, revision_id, matrix_type):
        """
        Retrieve all the Matrices associated with the Requirement module.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Requirement matrix types are:

                                rqrmnt_hrdwr = Requirement:Hardware
                                rqrmnt_sftwr = Requirement:Software
                                rqrmnt_vldtn = Requirement:Validation

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """
        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_type == 'rqrmnt_hrdwr':
            self._dmx_rqmt_hw_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='requirement_id',
                ckey='hardware_id',
                rheader='requirement_code',
                cheader='comp_ref_des',
            )
            _matrix = self._dmx_rqmt_hw_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_hw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_hw_matrix.dic_row_hdrs

        elif matrix_type == 'rqrmnt_sftwr':
            self._dmx_rqmt_sw_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='requirement_id',
                ckey='software_id',
                rheader='requirement_code',
                cheader='description',
            )
            _matrix = self._dmx_rqmt_sw_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_sw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_sw_matrix.dic_row_hdrs

        elif matrix_type == 'rqrmnt_vldtn':
            self._dmx_rqmt_val_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='requirement_id',
                ckey='validation_id',
                rheader='requirement_code',
                cheader='name',
            )
            _matrix = self._dmx_rqmt_val_matrix.dtf_matrix
            _column_hdrs = self._dmx_rqmt_val_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_rqmt_val_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def _request_do_insert(self, revision_id, parent_id):
        """
        Request to add an RAMSTKRequirement table record.

        :param int revision_id: the Revision ID the Requirement is associated
        with.
        :param int parent_id: the ID of the parent Requirement.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=revision_id, parent_id=parent_id,
        )

        return RAMSTKDataController.do_handle_results(
            self, _error_code, _msg,
            None,
        )

    def _request_do_delete_matrix(self, matrix_type, item_id, row=True):
        """
        Request to remove a row or column from the selected Data Matrix.

        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Requirement matrix types are:

                                rqrmnt_hrdwr = Requirement:Hardware
                                rqrmnt_sftwr = Requirement:Software
                                rqrmnt_vldtn = Requirement:Validation

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_deletes = {
            'rqrmnt_hrdwr': self._dmx_rqmt_hw_matrix.do_delete,
            'rqrmnt_sftwr': self._dmx_rqmt_sw_matrix.do_delete,
            'rqrmnt_vldtn': self._dmx_rqmt_val_matrix.do_delete,
        }

        try:
            self._matrix_delete_method = _dic_deletes[matrix_type]
        except KeyError:
            self._matrix_delete_method = None

        return RAMSTKDataController.request_do_delete_matrix(
            self, matrix_type, item_id, row=row,
        )

    def _request_do_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.  Current
                                Requirement matrix types are:

                                rqrmnt_hrdwr = Requirement:Hardware
                                rqrmnt_sftwr = Requirement:Software
                                rqrmnt_vldtn = Requirement:Validation

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_updates = {
            'rqrmnt_hrdwr': self._dmx_rqmt_hw_matrix.do_update,
            'rqrmnt_sftwr': self._dmx_rqmt_sw_matrix.do_update,
            'rqrmnt_vldtn': self._dmx_rqmt_val_matrix.do_update,
        }

        try:
            self._matrix_update_method = _dic_updates[matrix_type]
        except KeyError:
            self._matrix_update_method = None

        return RAMSTKDataController.request_do_update_matrix(
            self, revision_id, matrix_type,
        )

    def _request_set_attributes(self, module_id, key, value):
        """
        Request to set a Requirement attribute.

        :param int module_id: the ID of the entity who's attribute is to
                              be set.
        :param str key: the key of the attributes to set.
        :param value: the value to set the attribute identified by the
                      key.
        :return: _error_code, _msg; the error code and error message from the
                                    called method.
        :rtype: tuple
        """
        if key == 'requirement_type':
            _value = self._dtm_data_model.do_create_code(value[0], module_id)
            RAMSTKDataController.request_set_attributes(
                self, module_id, 'requirement_code', _value,
            )

            value = value[1]

        return RAMSTKDataController.request_set_attributes(
            self, module_id, key, value,
        )
