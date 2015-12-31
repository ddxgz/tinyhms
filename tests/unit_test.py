import os
import uuid
import unittest
from unittest import mock

from server import auth
from server.models import create_tables, DoctorModel, PatientModel, ObjectModel, LoginModel
from server.config import Config
from server.utils import logger


class UtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_auth_success(self):
        logger.debug('in test_auth_success')
        adminid = 'admin_{}'.format(str(uuid.uuid4()))
        LoginModel.create(
            username=adminid,
            password='admin',
            role='admin'
            )
        adm_login = {
                'username':adminid,
                'password':'admin',  }

        success_token = mock.Mock(return_value='admintoken')
        auth.get_token = success_token
        self.assertEqual(auth.authentication('admin', adm_login)[0], 1)
        self.assertEqual(auth.authentication('admin', adm_login)[1], 'admintoken')
        # status, adm_token = auth.authentication('admin', adm_login)
        # self.assertTrue(status)
        # logger.debug('adm_token:{}'.format(adm_token))

    def test_auth_fail(self):
        logger.debug('in test_auth_success fail')
        adminid = 'admin_{}'.format(str(uuid.uuid4()))
        LoginModel.create(
            username=adminid,
            password='admin',
            role='admin'
            )
        adm_login = {
                'username':adminid,
                'password':'failpass',  }

        fail_token = mock.Mock(return_value='admintoken')
        auth.get_token = fail_token
        self.assertEqual(auth.authentication('admin', adm_login)[0], 0)
        self.assertEqual(auth.authentication('admin', adm_login)[1], 'auth failed, password not match')
        self.assertEqual(auth.authentication('doctor', adm_login)[0], 0)
        self.assertEqual(auth.authentication('doctor', adm_login)[1], 'auth failed')


if __name__ == '__main__':
    unittest.main()
