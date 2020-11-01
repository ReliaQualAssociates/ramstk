# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.frame.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 frame Module."""

# Standard Library Imports
from typing import Any, Dict, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject, Gtk

# RAMSTK Local Imports
from .label import RAMSTKLabel


class RAMSTKFrame(Gtk.Frame):
    """The RAMSTK Frame class."""
    def __init__(self) -> None:
        """Initialize an instance of the RAMSTK Frame."""
        GObject.GObject.__init__(self)

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set the RAMSTKFrame properties."""
        _bold: Union[Dict[str, Any], bool] = kwargs.get('bold', False)
        _shadow = kwargs.get('shadow', Gtk.ShadowType.ETCHED_OUT)
        _title: Union[Dict[str, Any], str] = kwargs.get('title', "")

        _label: RAMSTKLabel = RAMSTKLabel(_title)   # type: ignore
        _label.do_set_properties(bold=_bold)
        _label.show_all()
        self.set_label_widget(_label)

        self.set_shadow_type(_shadow)
