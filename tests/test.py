import os
import unittest

from server.doctor import register_doctor, get_doctor
from server.models import create_tables
from server.config import Config


class DoctorTest(unittest.TestCase):

    def setUp(self):
        test_conf = Config('configuration_test')
        # create db, tables
        create_tables()


    def tearDown(self):
        os.remove('{}.sqlite3'.format(test_conf.db_filename))

    def test_register_doctor(self):
        pass

    def test_get_doctor(self):
        pass


if __name__ == '__main__':
    unittest.main()
