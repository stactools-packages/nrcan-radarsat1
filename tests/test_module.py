import unittest

import stactools.nrcan_radarsat1


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.nrcan_radarsat1.__version__)
