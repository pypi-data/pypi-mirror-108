from portdatasplitter.main import PortDataSplitter
import unittest

class MainClassTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_getting_test_valuse(self):
        pds = PortDataSplitter('0.0.0.0', 1488, test_mode=True, debug=True)
        pds.start()


if __name__ == '__main__':
    unittest.main()