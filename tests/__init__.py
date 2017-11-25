import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))) +
                '.', )

from test_setup import setUp, tearDown

setUp()
tearDown()
