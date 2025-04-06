# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKBaseDialog as RAMSTKBaseDialog
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel

class AddControlAction(RAMSTKBaseDialog):
    rdoControl: Incomplete
    rdoAction: Incomplete
    def __init__(self, parent: Incomplete | None = None) -> None: ...
