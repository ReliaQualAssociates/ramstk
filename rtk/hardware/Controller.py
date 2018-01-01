# -*- coding: utf-8 -*-
#
#       rtk.hardware.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Controller."""  # pragma: no cover

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataController  # pylint: disable=E0401
from datamodels import RTKDataMatrix  # pylint: disable=E0401
from dao import RTKHardware, RTKTest, RTKValidation  # pylint: disable=E0401
from . import dtmHardwareBoM


class HardwareBoMDataController(RTKDataController):
    """
    Provide an interface between the Hardware data model and an RTK view model.

    A single Hardware controller can manage one or more Hardware data models.
    The attributes of a Hardware data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Hardware data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Hardware Data
                    Model.
        :type dao: :class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmHardwareBoM(dao),
            rtk_module='hardware BOM',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_hw_tstng_matrix = RTKDataMatrix(dao, RTKHardware, RTKTest)
        self._dmx_hw_vldtn_matrix = RTKDataMatrix(dao, RTKHardware,
                                                  RTKValidation)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, node_id, table):
        """
        Request the RTK Program database record associated with Node ID.

        :param int node_id: the Node ID to retrieve from the Tree.
        :param str table: the name of the RTK Program database table to
                          select the entity from.
        :return: the RTK Program database record requested from the desired
                 table.
        :rtype: object
        """
        return self._dtm_data_model.select(node_id, table)

    def request_select_all_matrix(self, revision_id, matrix_type):
        """
        Retrieve all the Matrices associated with the Hardware.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Hardware matrix types are:

                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """
        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_type == 'hrdwr_tstng':
            self._dmx_hw_tstng_matrix.select_all(
                revision_id,
                matrix_type,
                rkey='hardware_id',
                ckey='test_id',
                rheader='comp_ref_des',
                cheader='name')
            _matrix = self._dmx_hw_tstng_matrix.dtf_matrix
            _column_hdrs = self._dmx_hw_tstng_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_hw_tstng_matrix.dic_row_hdrs

        elif matrix_type == 'hrdwr_vldtn':
            self._dmx_hw_vldtn_matrix.select_all(
                revision_id,
                matrix_type,
                rkey='hardware_id',
                ckey='validation_id',
                rheader='comp_ref_des',
                cheader='description')
            _matrix = self._dmx_hw_vldtn_matrix.dtf_matrix
            _column_hdrs = self._dmx_hw_vldtn_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_hw_vldtn_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def request_insert(self, revision_id=0, parent_id=0, part=0):
        """
        Request to add an RTKHardware table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id, parent_id=parent_id, part=part)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage(
                    'insertedHardware',
                    hardware_id=self._dtm_data_model.dtm_hardware.last_id)
        else:
            _msg = _msg + '  Failed to add a new Hardware item to the RTK ' \
                'Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_insert_matrix(self, matrix_type, item_id, heading, row=True):
        """
        Request the to add a new row or column to the Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Hardware matrix types are:

                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'hrdwr_tstng':
            _error_code, _msg = self._dmx_hw_tstng_matrix.insert(
                item_id, heading, row=row)

        elif matrix_type == 'hrdwr_vldtn':
            _error_code, _msg = self._dmx_hw_vldtn_matrix.insert(
                item_id, heading, row=row)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedMatrix',
                matrix_type=matrix_type,
                item_id=item_id,
                row=row)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, hardware_id):
        """
        Request to delete an RTKHardware table record.

        :param int hardware_id: the Hardware ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.delete(hardware_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedHardware')

    def request_delete_matrix(self, matrix_type, item_id, row=True):
        """
        Request to remove a row or column from the selected Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Hardware matrix types are:

                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'hrdwr_tstng':
            _error_code, _msg = self._dmx_hw_tstng_matrix.delete(
                item_id, row=row)

        if matrix_type == 'hrdwr_vldtn':
            _error_code, _msg = self._dmx_hw_vldtn_matrix.delete(
                item_id, row=row)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedMatrix')

    def request_update(self, hardware_id):
        """
        Request to update an RTKHardware table record.

        :param int hardware_id: the ID of the hardware to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update(hardware_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedHardware')

    def request_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.  Current
                                Hardware matrix types are:

                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'hrdwr_tstng':
            _error_code, _msg = self._dmx_hw_tstng_matrix.update(
                revision_id, matrix_type)

        elif matrix_type == 'hrdwr_vldtn':
            _error_code, _msg = self._dmx_hw_vldtn_matrix.update(
                revision_id, matrix_type)
        else:
            _error_code = 6
            _msg = 'RTK ERROR: Attempted to update non-existent matrix ' \
                   '{0:s}.'.format(matrix_type)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedMatrix')

    def request_update_all(self):
        """
        Request to update all records in the RTKHardware table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_get_attributes(self, node_id):
        """
        Get the attributes of the record associated with Node ID and table.

        :param int node_id: the ID of the Hardware item to get attributes for.
        :return: attributes; the {attribute:value} dict.
        :rtype: dict
        """
        return self._dtm_data_model.tree.get_node(node_id).data

    def request_set_attributes(self, node_id, attributes):
        """
        Set the attributes of the record associated with the Node ID.

        :param int node_id: the ID of the record in the RTK Program database
                            table whose attributes are to be set.
        :param dict attributes: the dictionary of attributes and values.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Set the overall BoM attributes.
        self._dtm_data_model.tree.get_node(node_id).data = attributes

        # Set the attributes for the individual tables.
        _error_code, _msg = self._dtm_data_model.dtm_hardware.select(
            node_id).set_attributes(attributes)
        _return = (_return or RTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_design_electric.select(
            node_id).set_attributes(attributes)
        _return = (_return or RTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_design_mechanic.select(
            node_id).set_attributes(attributes)
        _return = (_return or RTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_mil_hdbk_f.select(
            node_id).set_attributes(attributes)
        _return = (_return or RTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_nswc.select(
            node_id).set_attributes(attributes)
        _return = (_return or RTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_reliability.select(
            node_id).set_attributes(attributes)
        _return = (_return or RTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        return _return

    def request_make_composite_reference_designator(self, node_id=1):
        """
        Request the composite reference designators be created.

        :keyword int node_id: the Treelib tree() node ID to start with to make
                              composite reference designators.  Defaults to the
                              top node.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        # Create the composite reference designators in the Hardware model.
        if self._dtm_data_model.dtm_hardware.make_composite_ref_des(node_id):
            _error_code = 3005
            _msg = 'RTK ERROR: Failed to create all composite reference ' \
                   'designators for Node ID {0:d} and ' \
                   'children.'.format(node_id)

        # If that was successful, update the BoM attributes.
        if _error_code == 0:
            for _node_id in self._dtm_data_model.tree.nodes:
                if _node_id != 0:
                    _attributes = self.request_get_attributes(_node_id)
                    _comp_ref_des = self._dtm_data_model.dtm_hardware.select(
                        _node_id).comp_ref_des
                    _attributes['comp_ref_des'] = _comp_ref_des

        return _error_code, _msg

    def request_calculate(self, node_id):
        """
        Request to calculate the hardware item.

        :param int node_id: the Hardware ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtm_data_model.calculate(node_id)

        if (not self.request_set_attributes(node_id, _attributes)
                and not self._test):
            pub.sendMessage('calculatedHardware', module_id=node_id)
        else:
            _return = True

        return _return

    def request_calculate_all(self):
        """
        Request to calculate the hardware item.

        :param int node_id: the Hardware ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _results = self._dtm_data_model.calculate_all()

        if not self._test:
            pub.sendMessage('calculatedHardware', module_id=1)
        else:
            _return = True

        return _return
