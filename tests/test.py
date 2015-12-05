import os
import unittest
import time

from server.doctor import register_doctor, get_doctor
from server.models import DoctorModel, create_tables
from server.config import Config


class DoctorTest(unittest.TestCase):

    def setUp(self):
        self.test_conf = Config('tests/configuration_test')
        # create db, tables
        create_tables(self.test_conf)


    def tearDown(self):
        os.remove('{}.sqlite3'.format(self.test_conf.db_filename))

    def test_register_doctor(self):
        data = {
                'firstname':'aaa',
                'lastname':'bbb',
                'experience':10
                }
        status, did = register_doctor(data)

        self.assertTrue(status)
        self.assertIn('-', did)

        doctor = DoctorModel.get(DoctorModel.firstname=='aaa',
            DoctorModel.lastname=='bbb')
        self.assertEqual(10, doctor.experience)


    def test_get_doctor(self):
        pass


if __name__ == '__main__':
    unittest.main()
