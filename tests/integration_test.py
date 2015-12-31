import os
import unittest
import uuid
import ast
import time
import threading
from wsgiref import simple_server
import urllib
import json

import requests

from server.gateway import app
from server.verbs import Visit

from server.doctor import register_doctor, get_doctor, edit_doctor
from server.patient import register_patient, get_patient, edit_patient
from server.appointment import make_appointment, get_appointment, check_appointment
from server.obj import upload_obj, get_obj, get_objs, delete_obj
from server.models import create_tables, DoctorModel, PatientModel, ObjectModel, LoginModel
from server.auth import authentication, get_token
from server import rediscli
from server.config import Config
from server.utils import logger


HOST = 'http://127.0.0.1:8080'
ENDPOINT = HOST + '/v1'
SUCCESS_STATUS_CODES = [200, 201, 202, 204]
FAILURE_STATUS_CODES = [400, 401, 403, 404, 405]

def runserver():
    httpd = simple_server.make_server('127.0.0.1', 8080, app)
    httpd.serve_forever()


def run_server():
    thread = threading.Thread(target=runserver)
    thread.daemon = True
    thread.start()
    # # Wait a moment for the thread to start up
    time.sleep(0.5)


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.test_conf = Config('tests/configuration_test')
        create_tables(self.test_conf)

    def tearDown(self):
        os.remove('{}.sqlite3'.format(self.test_conf.db_filename))


class TestApiv1(BaseTestCase):
    """
    put an account
    delete an account

    TODO: test 40x situations
    """
    def test_reg_doctor(self):
        adminid = 'admin_{}'.format(str(uuid.uuid4()))

        LoginModel.create(
            username=adminid,
            password='admin',
            role='admin'
            )

        headers = {
            'content-type': 'application/json'}

        adm_login = {
                'username':adminid,
                'password':'admin',  }

        visit = Visit(ENDPOINT)

        # visit.get(headers=headers)
        auth_code, resp_auth = visit.post(suffix_url='auth/admin', headers=headers,
            data=adm_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        self.assertIn('token', resp_auth)
        self.assertIn(auth_code, SUCCESS_STATUS_CODES)
        # resp_auth = ast.literal_eval(resp_auth)
        resp_auth = json.loads(resp_auth)
        admin_token = resp_auth['token']

        logger.debug('before admin requests')
        headers['token'] = admin_token
        headers['role'] = 'admin'
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        regdoc_data = {
                'email':doctorid,
                'firstname':'intest',
                'lastname':'intest',
                'experience':10
                }
        doc_code, resp_doc = visit.post(suffix_url='doctor', headers=headers,
            data=regdoc_data)
        # logger.info('doc_code:{}, resp_auth:{}'.format(doc_code, resp_auth))
        resp_doc = json.loads(resp_doc)
        did = resp_doc['doctorid']
        self.assertEqual(doctorid, did)
        self.assertIn(doc_code, SUCCESS_STATUS_CODES)

        headers['token'] = 'wrong_token'
        headers['role'] = 'admin'
        doc_code, resp_doc = visit.post(suffix_url='doctor', headers=headers,
            data=regdoc_data)
        # logger.info('doc_code:{}, resp_auth:{}'.format(doc_code, resp_auth))
        self.assertIn(doc_code, FAILURE_STATUS_CODES)

    def test_put_doctor(self):
        adminid = 'admin_{}'.format(str(uuid.uuid4()))

        LoginModel.create(
            username=adminid,
            password='admin',
            role='admin'
            )

        headers = {
            'content-type': 'application/json'}

        adm_login = {
                'username':adminid,
                'password':'admin',  }

        visit = Visit(ENDPOINT)

        # visit.get(headers=headers)
        auth_code, resp_auth = visit.post(suffix_url='auth/admin', headers=headers,
            data=adm_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        self.assertIn('token', resp_auth)
        self.assertIn(auth_code, SUCCESS_STATUS_CODES)
        # resp_auth = ast.literal_eval(resp_auth)
        resp_auth = json.loads(resp_auth)
        admin_token = resp_auth['token']

        logger.debug('before admin requests')
        headers['token'] = admin_token
        headers['role'] = 'admin'
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        regdoc_data = {
                'email':doctorid,
                'firstname':'intest',
                'lastname':'intest',
                'experience':10
                }
        doc_code, resp_doc = visit.post(suffix_url='doctor', headers=headers,
            data=regdoc_data)
        # logger.info('doc_code:{}, resp_auth:{}'.format(doc_code, resp_auth))
        resp_doc = json.loads(resp_doc)
        did = resp_doc['doctorid']
        self.assertEqual(doctorid, did)
        self.assertIn(doc_code, SUCCESS_STATUS_CODES)


        LoginModel.create(
            username=doctorid,
            password='doctor',
            role='doctor'
            )

        headers = {
            'content-type': 'application/json'}

        doc_login = {
                'username':doctorid,
                'password':'doctor',  }

        auth_code, resp_auth = visit.post(suffix_url='auth/doctor', headers=headers,
            data=doc_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        self.assertIn('token', resp_auth)
        self.assertIn(auth_code, SUCCESS_STATUS_CODES)
        # resp_auth = ast.literal_eval(resp_auth)
        resp_auth = json.loads(resp_auth)
        doctor_token = resp_auth['token']

        logger.debug('before doctor requests')
        headers['token'] = doctor_token
        headers['role'] = 'doctor'
        putdoc_data = {
                'email':doctorid,
                'firstname':'intest_modi',
                'lastname':'intest_modi',
                'experience':11
                }
        doc_code, resp_doc = visit.put(suffix_url='doctor/{}'.format(doctorid), headers=headers,
            data=putdoc_data)
        logger.info('doc_code:{}, resp_doc:{}'.format(doc_code, resp_doc))
        resp_doc = json.loads(resp_doc)
        did = resp_doc['doctorid']
        self.assertEqual(doctorid, did)
        self.assertIn(doc_code, SUCCESS_STATUS_CODES)

        headers['role'] = 'admin'
        putdoc_data = {
                'email':doctorid,
                'firstname':'intest_modi',
                'lastname':'intest_modi',
                'experience':11
                }
        doc_code, resp_doc = visit.put(suffix_url='doctor/{}'.format(doctorid), headers=headers,
            data=putdoc_data)
        logger.info('doc_code:{}, resp_doc:{}'.format(doc_code, resp_doc))
        self.assertIn(doc_code, FAILURE_STATUS_CODES)


    def test_get_patient(self):
        adminid = 'admin_{}'.format(str(uuid.uuid4()))

        LoginModel.create(
            username=adminid,
            password='admin',
            role='admin'
            )

        headers = {
            'content-type': 'application/json'}

        adm_login = {
                'username':adminid,
                'password':'admin',  }

        visit = Visit(ENDPOINT)

        # visit.get(headers=headers)
        auth_code, resp_auth = visit.post(suffix_url='auth/admin', headers=headers,
            data=adm_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        self.assertIn('token', resp_auth)
        self.assertIn(auth_code, SUCCESS_STATUS_CODES)
        # resp_auth = ast.literal_eval(resp_auth)
        resp_auth = json.loads(resp_auth)
        admin_token = resp_auth['token']

        logger.debug('before admin requests')
        headers['token'] = admin_token
        headers['role'] = 'admin'
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        regpt_data = {
                'email':patientid,
                'firstname':'intest',
                'lastname':'intest',
                'height':'177'
                }
        doc_code, resp_doc = visit.post(suffix_url='patient', headers=headers,
            data=regpt_data)
        logger.info('doc_code:{}, resp_auth:{}'.format(doc_code, resp_auth))
        resp_doc = json.loads(resp_doc)
        did = resp_doc['patientid']
        self.assertEqual(patientid, did)
        self.assertIn(doc_code, SUCCESS_STATUS_CODES)


        LoginModel.create(
            username=patientid,
            password='patient',
            role='patient'
            )

        headers = {
            'content-type': 'application/json'}

        pat_login = {
                'username':patientid,
                'password':'patient',  }

        auth_code, resp_auth = visit.post(suffix_url='auth/patient', headers=headers,
            data=pat_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        self.assertIn('token', resp_auth)
        self.assertIn(auth_code, SUCCESS_STATUS_CODES)
        # resp_auth = ast.literal_eval(resp_auth)
        resp_auth = json.loads(resp_auth)
        pat_token = resp_auth['token']

        logger.debug('before patient get request')
        headers['token'] = pat_token
        headers['role'] = 'patient'

        pat_code, resp_pat = visit.get(suffix_url='patient/{}'.format(patientid), headers=headers)
        logger.info('pat_code:{}, resp_pat:{}'.format(pat_code, resp_pat))
        resp_pat = json.loads(resp_pat)
        did = resp_pat['email']
        self.assertEqual(patientid, did)
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)


if __name__ == '__main__':
    run_server()
    unittest.main()
