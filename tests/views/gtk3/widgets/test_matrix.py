# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_matrix.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 matrix module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKBaseMatrix


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKBaseMatrix():
    """Test class for the RAMSTKBaseMatrix."""
    @pytest.mark.gui
    def test_create_matrix(self, test_toml_user_configuration):
        """__init__() should create a RAMSTKBaseMatrix."""
        DUT = RAMSTKBaseMatrix(test_toml_user_configuration, test=True,
                               matrix_type='hrdwr_rqrmnt')
        DUT._dic_matrix_labels = {
            'hrdwr_rqrmnt': [
                _('This is the button tooltip.'),
                _('This is the matrix label.'),
                _('This is the label tooltip.')
            ]
        }

        assert isinstance(DUT, RAMSTKBaseMatrix)
        assert isinstance(DUT.RAMSTK_USR_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert DUT._dic_icons == {
            0:
            DUT.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/none.png',
            1:
            DUT.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/partial.png',
            2:
            DUT.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/complete.png',
            'save':
            DUT.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/save.png',
            'save-all':
            DUT.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/save-all.png',
            'view-refresh':
            DUT.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/view-refresh.png'
        }
        assert DUT._matrix_type == 'hrdwr_rqrmnt'
        assert DUT._revision_id is None
        assert DUT._ramstk_matrix is None
        assert DUT._n_columns == 0
        assert DUT._n_rows == 0
        assert DUT.n_fixed_columns == 0
        assert isinstance(DUT.hbx_tab_label, Gtk.HBox)
        assert isinstance(DUT.matrix, Gtk.TreeView)
        assert pub.isSubscribed(DUT.do_load_matrix, 'retrieved_matrix')
