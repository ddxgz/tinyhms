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
    def setUp(self):
        self.test_conf = Config('tests/configuration_test')
        create_tables(self.test_conf)

        self.adminid = 'admin_{}'.format(str(uuid.uuid4()))
        self.doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        self.patientid = '{}@hms.com'.format(str(uuid.uuid4()))

        self.admin_auth()
        self.doctor_auth()
        self.patient_auth()

    def admin_auth(self):

        LoginModel.create(
            username=self.adminid,
            password='admin',
            role='admin'
            )

        headers = {
            'content-type': 'application/json'}

        adm_login = {
                'username':self.adminid,
                'password':'admin',  }

        visit = Visit(ENDPOINT)

        # visit.get(headers=headers)
        auth_code, resp_auth = visit.post(suffix_url='auth/admin', headers=headers,
            data=adm_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        resp_auth = json.loads(resp_auth)
        self.admin_token = resp_auth['token']

    def doctor_auth(self):
        visit = Visit(ENDPOINT)
        logger.debug('before doctor_auth')
        headers = {
            'content-type': 'application/json'}
        headers['token'] = self.admin_token
        headers['role'] = 'admin'
        regdoc_data = {
                'email':self.doctorid,
                'firstname':'intest',
                'lastname':'intest',
                'experience':10,
                'patients': '["{}"]'.format(self.patientid)
                }
        doc_code, resp_doc = visit.post(suffix_url='doctor', headers=headers,
            data=regdoc_data)
        # logger.info('doc_code:{}, resp_auth:{}'.format(doc_code, resp_auth))
        resp_doc = json.loads(resp_doc)
        did = resp_doc['doctorid']
        self.assertEqual(self.doctorid, did)
        self.assertIn(doc_code, SUCCESS_STATUS_CODES)

        self.doctorpass = 'doctor'
        LoginModel.create(
            username=self.doctorid,
            password=self.doctorpass,
            role='doctor'
            )

        headers = {
            'content-type': 'application/json'}

        doc_login = {
                'username':self.doctorid,
                'password':self.doctorpass,  }

        auth_code, resp_auth = visit.post(suffix_url='auth/doctor', headers=headers,
            data=doc_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        self.assertIn('token', resp_auth)
        self.assertIn(auth_code, SUCCESS_STATUS_CODES)
        # resp_auth = ast.literal_eval(resp_auth)
        resp_auth = json.loads(resp_auth)
        self.doctor_token = resp_auth['token']

    def patient_auth(self):
        visit = Visit(ENDPOINT)
        logger.debug('before patient_auth')
        headers = {
            'content-type': 'application/json'}
        headers['token'] = self.admin_token
        headers['role'] = 'admin'
        regpt_data = {
                'email':self.patientid,
                'firstname':'intest',
                'lastname':'intest',
                'height':'177'
                }
        doc_code, resp_doc = visit.post(suffix_url='patient', headers=headers,
            data=regpt_data)
        logger.info('doc_code:{}, resp_auth:{}'.format(doc_code, resp_doc))
        self.assertIn(doc_code, SUCCESS_STATUS_CODES)

        self.patientpass = 'patient'
        LoginModel.create(
            username=self.patientid,
            password=self.patientpass,
            role='patient'
            )

        headers = {
            'content-type': 'application/json'}

        pat_login = {
                'username':self.patientid,
                'password':self.patientpass,  }

        auth_code, resp_auth = visit.post(suffix_url='auth/patient', headers=headers,
            data=pat_login)
        logger.info('auth_code:{}, resp_auth:{}'.format(auth_code, resp_auth))
        self.assertIn('token', resp_auth)
        self.assertIn(auth_code, SUCCESS_STATUS_CODES)
        # resp_auth = ast.literal_eval(resp_auth)
        resp_auth = json.loads(resp_auth)
        self.pat_token = resp_auth['token']

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

    def test_prescription(self):
        visit = Visit(ENDPOINT)
        headers = {
            'content-type': 'application/json'}
        logger.debug('before test_post_prescription')
        # headers['token'] = self.admin_token
        # headers['role'] = 'admin'
        headers['token'] = self.doctor_token
        headers['role'] = 'doctor'
        # logger.debug('before patient get request')
        # headers['token'] = self.pat_token
        # headers['role'] = 'patient'
        regprescription_data = {
                'datetime':'20160101',
                'drug_name':'drug1',
                'after_meal':'yes',
                'amount':'60',
                'dosage_per_day':'2',
                'description':'with water'
                }
        pat_code, resp_presc = visit.post(suffix_url='prescription/{}/{}'.format(
            self.doctorid, self.patientid), headers=headers, data=regprescription_data)
        logger.info('pat_code:{}, resp_presc:{}'.format(pat_code, resp_presc))
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)
        regprescription_data2 = {
                'datetime':'20160102',
                'drug_name':'drug2',
                'after_meal':'yes',
                'amount':'10',
                'dosage_per_day':'1',
                'description':'with water'
                }
        pat_code, resp_presc = visit.post(suffix_url='prescription/{}/{}'.format(
            self.doctorid, self.patientid), headers=headers, data=regprescription_data2)
        logger.info('pat_code:{}, resp_presc:{}'.format(pat_code, resp_presc))
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)

        logger.debug('before test_get_prescriptions')
        headers['token'] = self.pat_token
        headers['role'] = 'patient'

        pat_code, resp_prescs = visit.get(suffix_url='prescriptions/{}'.format(
            self.patientid), headers=headers)
        logger.info('pat_code:{}, resp_prescs:{}'.format(pat_code, resp_prescs))
        # resp_prescs = json.loads(resp_prescs)
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)
        self.assertIn(self.doctorid, resp_prescs)
        self.assertIn('drug1', resp_prescs)
        self.assertIn('drug2', resp_prescs)

    def test_comment(self):
        visit = Visit(ENDPOINT)
        headers = {
            'content-type': 'application/json'}
        logger.debug('before test_comment')
        # headers['token'] = self.admin_token
        # headers['role'] = 'admin'
        headers['token'] = self.doctor_token
        headers['role'] = 'doctor'
        # logger.debug('before patient get request')
        # headers['token'] = self.pat_token
        # headers['role'] = 'patient'
        comment_data = {
                'datetime':'20160101',
                'comment':'drink water'
                }
        pat_code, resp_presc = visit.post(suffix_url='comment/{}/{}'.format(
            self.doctorid, self.patientid), headers=headers, data=comment_data)
        logger.info('pat_code:{}, resp_presc:{}'.format(pat_code, resp_presc))
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)
        comment_data2 = {
                'datetime':'20160102',
                'comment':'eat drug'
                }
        pat_code, resp_presc = visit.post(suffix_url='comment/{}/{}'.format(
            self.doctorid, self.patientid), headers=headers, data=comment_data2)
        logger.info('pat_code:{}, resp_presc:{}'.format(pat_code, resp_presc))
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)

        logger.debug('before test_get_comments')
        headers['token'] = self.pat_token
        headers['role'] = 'patient'

        pat_code, resp_prescs = visit.get(suffix_url='comments/{}'.format(
            self.patientid), headers=headers)
        logger.info('pat_code:{}, resp_prescs:{}'.format(pat_code, resp_prescs))
        # resp_prescs = json.loads(resp_prescs)
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)
        self.assertIn(self.doctorid, resp_prescs)
        self.assertIn('drink water', resp_prescs)
        self.assertIn('drink water', resp_prescs)

    def test_discharge(self):
        visit = Visit(ENDPOINT)
        headers = {
            'content-type': 'application/json'}
        logger.debug('before test_discharge')
        # headers['token'] = self.admin_token
        # headers['role'] = 'admin'
        headers['token'] = self.doctor_token
        headers['role'] = 'doctor'
        # logger.debug('before patient get request')
        # headers['token'] = self.pat_token
        # headers['role'] = 'patient'
        comment_data = {
                'datetime':'20160101',
                'indate':'20151111'
                }
        pat_code, resp_presc = visit.post(suffix_url='discharge/{}/{}'.format(
            self.doctorid, self.patientid), headers=headers, data=comment_data)
        logger.info('pat_code:{}, resp_presc:{}'.format(pat_code, resp_presc))
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)
        comment_data2 = {
                'datetime':'20160102',
                'indate':'20151212'
                }
        pat_code, resp_presc = visit.post(suffix_url='discharge/{}/{}'.format(
            self.doctorid, self.patientid), headers=headers, data=comment_data2)
        logger.info('pat_code:{}, resp_presc:{}'.format(pat_code, resp_presc))
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)

        comment_data3 = {
                'datetime':'20160201',
                'outdate':'20160202',
                'description':'well'
                }
        pat_code, resp_presc = visit.put(suffix_url='discharge/{}/{}/{}'.format(
            self.doctorid, self.patientid, '20151212'), headers=headers, data=comment_data3)
        logger.info('pat_code:{}, resp_presc:{}'.format(pat_code, resp_presc))
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)

        logger.debug('before test_get_discharges')
        headers['token'] = self.pat_token
        headers['role'] = 'patient'

        pat_code, resp_prescs = visit.get(suffix_url='discharges/{}'.format(
            self.patientid), headers=headers)
        logger.info('pat_code:{}, resp_prescs:{}'.format(pat_code, resp_prescs))
        # resp_prescs = json.loads(resp_prescs)
        self.assertIn(pat_code, SUCCESS_STATUS_CODES)
        self.assertIn(self.doctorid, resp_prescs)
        self.assertIn('20160202', resp_prescs)
        self.assertIn('20151111', resp_prescs)


if __name__ == '__main__':
    run_server()
    unittest.main()
