import asyncio
import unittest
from datetime import date

from app.earthquake import all_features


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_features(self):
        dt_start = date(2014, 1, 1)
        dt_end = date(2014, 1, 2)
        exp_count = 326

        # TODO: DeprecationWarning: The loop argument is deprecated
        seq = asyncio.run(all_features(dt_start, dt_end))
        self.assertEqual(exp_count, len(seq))


if __name__ == '__main__':
    unittest.main(verbosity=2)
