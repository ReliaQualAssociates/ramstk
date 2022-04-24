# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.__base.dbrecord_test_class.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test meta-classes for database record, table, and view models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class UnitTestGetterSetterMethods:
    """Class for unit testing table model methods that get or set."""

    __test__ = False

    _id_columns = []

    _test_attr = None
    _test_default_value = None

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_record_model):
        """Should return None on success."""
        for _id in self._id_columns:
            test_attributes.pop(_id)

        assert test_record_model.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self,
        test_attributes,
        test_record_model,
    ):
        """Should set an attribute to its default value when passed a None value."""
        test_attributes[self._test_attr] = None
        for _id in self._id_columns:
            test_attributes.pop(_id)

        assert test_record_model.set_attributes(test_attributes) is None
        assert (
            test_record_model.get_attributes()[self._test_attr]
            == self._test_default_value
        )

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self,
        test_attributes,
        test_record_model,
    ):
        """Should raise an AttributeError when passed an unknown attribute."""
        for _id in self._id_columns:
            test_attributes.pop(_id)

        with pytest.raises(AttributeError):
            test_record_model.set_attributes({"shibboly-bibbly-boo": 0.9998})
