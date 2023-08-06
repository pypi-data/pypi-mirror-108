from portdatasplitter.main import PortDataSplitter
from portdatasplitter.tests import test_settings as s
import unittest

class MainClassTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_getting_test_valuse(self):
        pds = PortDataSplitter(s.my_ip, s.my_port, test_mode=True, debug=True)
        pds.start()


if __name__ == '__main__':
    unittest.main()