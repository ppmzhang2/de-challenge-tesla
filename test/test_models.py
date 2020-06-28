import unittest
from datetime import date

from app.models.dao import Dao


class TestModel(unittest.TestCase):
    dao = None

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass started')
        cls.dao = Dao()
        cls.dao.reset_db()
        print('setUpClass ended')

    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass started')
        cls.dao.reset_db()
        print('tearDownClass ended')

    def setUp(self):
        print('setUp started')
        self.dao = Dao()
        self.dao.reset_db()
        print('setUp ended')

    def tearDown(self):
        print('tearDown started')
        self.dao.reset_db()
        print('tearDown ended')

    def test_bulk_save(self):
        """bulk save

        methods:
          * dao.bulk_save
          * dao.bulk_save_events
          * dao.count_events
        :return:
        """
        dt_start = date(2014, 1, 1)
        dt_end = date(2014, 1, 2)
        exp_count = 324

        self.assertEqual(0, self.dao.count_events())
        self.dao.bulk_save_events(dt_start, dt_end)
        self.assertEqual(exp_count, self.dao.count_events())


if __name__ == '__main__':
    unittest.main(verbosity=2)
