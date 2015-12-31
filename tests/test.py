import os
import unittest
from unittest import mock
import uuid
import ast
import time

import requests

from server.doctor import register_doctor, get_doctor, edit_doctor
from server.patient import register_patient, get_patient, edit_patient
from server.appointment import make_appointment, get_appointment, check_appointment
from server.obj import upload_obj, get_obj, get_objs, delete_obj
from server.models import create_tables, DoctorModel, PatientModel, ObjectModel, LoginModel
from server.auth import authentication, get_token
from server import rediscli
from server.config import Config
from server.utils import logger


class DoctorTest(unittest.TestCase):

    def setUp(self):
        self.test_conf = Config('tests/configuration_test')
        # create db, tables
        create_tables(self.test_conf)


    def tearDown(self):
        os.remove('{}.sqlite3'.format(self.test_conf.db_filename))
        # db point to testdb when db point works ok
        # os.remove('{}.sqlite3'.format('hms'))

    def test_register_doctor(self):
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':doctorid,
                'firstname':'aaa',
                'lastname':'bbb',
                'experience':10
                }
        status, did = register_doctor(data)

        self.assertTrue(status)
        self.assertIn('-', did)

        doctor = DoctorModel.get(DoctorModel.email==doctorid,
            DoctorModel.firstname=='aaa',
            DoctorModel.lastname=='bbb')
        self.assertEqual(10, doctor.experience)


    def test_get_doctor(self):
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':doctorid,
                'firstname':'aaa',
                'lastname':'bbb',
                'experience':10
                }
        status, did = register_doctor(data)
        status, doctorinfo = get_doctor(doctorid)
        self.assertTrue(status)
        self.assertIn(doctorid, doctorinfo)
        self.assertIn('10', doctorinfo)

    def test_edit_doctor(self):
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':doctorid,
                'firstname':'aaa',
                'lastname':'bbb',
                'experience':'10',
                'profession':'profession1',
                'qualification':'qualification1',
                'gender':'gender1'
                }
        status, did = register_doctor(data)

        self.assertTrue(status)

        doctor = DoctorModel.get(DoctorModel.email==doctorid)
        self.assertEqual(10, doctor.experience)
        self.assertEqual('profession1', doctor.profession)
        self.assertEqual('qualification1', doctor.qualification)
        self.assertEqual('gender1', doctor.gender)

        data2 = {
                'experience':'20',
                'profession':'profession2',
                'qualification':'qualification2',
                'gender':'gender2'
                }
        status2, did = edit_doctor(doctorid, data2)
        doctor2 = DoctorModel.get(DoctorModel.email==doctorid)
        self.assertTrue(status2)
        self.assertEqual(20, doctor2.experience)
        self.assertEqual('profession2', doctor2.profession)
        self.assertEqual('qualification2', doctor2.qualification)
        self.assertEqual('gender2', doctor2.gender)


class PatientTest(unittest.TestCase):

    def setUp(self):
        self.test_conf = Config('tests/configuration_test')
        # create db, tables
        create_tables(self.test_conf)


    def tearDown(self):
        os.remove('{}.sqlite3'.format(self.test_conf.db_filename))
        # db point to testdb when db point works ok
        # os.remove('{}.sqlite3'.format('hms'))

    def test_register_patient(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                'birthdate':'19601010'
                }
        status, did = register_patient(data)

        self.assertTrue(status)
        self.assertIn('-', did)

        patient = PatientModel.get(PatientModel.email==patientid,
            PatientModel.firstname=='aaa',
            PatientModel.lastname=='bbb')
        self.assertEqual('19601010', patient.birthdate)


    def test_get_patient(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                'birthdate':'19601010',
                'allergy':'allergy1'
                }
        status, did = register_patient(data)
        status, patientinfo = get_patient(patientid)
        self.assertTrue(status)
        self.assertIn(patientid, patientinfo)
        self.assertIn('19601010', patientinfo)

    def test_edit_patient(self):
        """
            email = CharField(max_length=100, unique=True)
            firstname = CharField(max_length=100)
            lastname = CharField(max_length=100)
            # email = CharField()
            birthdate = CharField()
            address = CharField()
            mobile_phone = CharField()
            gender = CharField()
            height = IntegerField()
            weight = IntegerField()
            blood_group = CharField()
            occupation = CharField()
            marriage = CharField()
            reference = CharField(max_length=100)
            doctor_in_charge = CharField()
            allergy = CharField()
            accompanied_by = CharField()
        """
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                'birthdate':'19881010',
                'mobile_phone':'0717771717',
                'height':'100',
                'doctor_in_charge':'d1'
                }
        status, patientid = register_patient(data)

        self.assertTrue(status)

        patient = PatientModel.get(PatientModel.email==patientid)
        self.assertEqual('19881010', patient.birthdate)
        self.assertEqual('0717771717', patient.mobile_phone)
        self.assertEqual('100', patient.height)
        self.assertEqual('d1', patient.doctor_in_charge)

        data2 = {
                'birthdate':'19981010',
                'mobile_phone':'0717771799',
                'height':'120',
                'doctor_in_charge':'d2'
                }
        status2, pid = edit_patient(patientid, data2)
        patient2 = PatientModel.get(PatientModel.email==patientid)
        self.assertTrue(status2)
        self.assertEqual('19981010', patient2.birthdate)
        self.assertEqual('0717771799', patient2.mobile_phone)
        self.assertEqual('120', patient2.height)
        self.assertEqual('d2', patient2.doctor_in_charge)


class AppointmentTest(unittest.TestCase):

    def setUp(self):
        # need to ensure redis is running
        # self.test_conf = Config('tests/configuration_test')
        # create db, tables
        pass


    def tearDown(self):
        pass
        # delete test data on redis
        # os.remove('{}.sqlite3'.format(self.test_conf.db_filename))
        # db point to testdb when db point works ok
        # os.remove('{}.sqlite3'.format('hms'))

    def test_make_appointment(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        timeslot = '201511201300'
        data = {
            'doctorid':doctorid,
            'datetimeslot':timeslot,
            'patientid':patientid,
            'illness': 'xxx',
        }
        # need to register patient and doctor first
        # status, pid = register_patient(data)
        # status, did = register_doctor(data)
        logger.debug('test_make_appointment')
        status, appurl = make_appointment(data)
        self.assertTrue(status)

        self.assertIn(doctorid, appurl)
        self.assertIn(patientid, appurl)
        self.assertIn(timeslot, appurl)

        appdata = rediscli.get_data(appurl)
        self.assertIn(doctorid, appdata)
        self.assertIn(patientid, appdata)
        self.assertIn('illness', appdata)

        schedule = rediscli.get_data(doctorid+'/'+timeslot[:8])
        logger.debug('test_make_appointment, schedule:{}'.format(schedule))
        schedule_dict = ast.literal_eval(schedule)
        self.assertEqual('1', schedule_dict[timeslot[8:]])

    def test_get_appointment(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        timeslot = '201511201300'
        data = {
            'doctorid':doctorid,
            'datetimeslot':timeslot,
            'patientid':patientid,
            'illness': 'xxx',
        }
        # need to register patient and doctor first
        # status, pid = register_patient(data)
        # status, did = register_doctor(data)
        logger.debug('test_get_appointment')
        status, appurl = make_appointment(data)
        self.assertTrue(status)

        status, appdata = get_appointment(doctorid+'/'+timeslot+'/'+patientid)
        self.assertTrue(status)
        self.assertIn(doctorid, appdata)
        self.assertIn(patientid, appdata)
        self.assertIn('illness', appdata)

    def test_check_appointment(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        timeslot1 = '201511201300'
        data = {
            'doctorid':doctorid,
            'datetimeslot':timeslot1,
            'patientid':patientid,
            'illness': 'xxx',
        }
        # need to register patient and doctor first
        # status, pid = register_patient(data)
        # status, did = register_doctor(data)
        logger.debug('test_check_appointment')
        status, appurl = make_appointment(data)
        self.assertTrue(status)

        status, schedule = check_appointment(doctorid, timeslot1[:8])
        self.assertTrue(status)
        schedule_dict = ast.literal_eval(schedule)
        self.assertIn(timeslot1[8:], schedule)
        self.assertEqual('1', schedule_dict[timeslot1[8:]])

        patientid2 = '{}@hms.com'.format(str(uuid.uuid4()))
        timeslot2 = '201511201400'
        data2 = {
            'doctorid':doctorid,
            'datetimeslot':timeslot2,
            'patientid':patientid2,
            'illness': 'xxx',
        }
        status, appurl = make_appointment(data2)
        self.assertTrue(status)
        status, schedule = check_appointment(doctorid, timeslot1[:8])
        self.assertTrue(status)
        schedule_dict = ast.literal_eval(schedule)
        self.assertIn(timeslot2[8:], schedule)
        self.assertEqual('1', schedule_dict[timeslot2[8:]])


class ObjectTest(unittest.TestCase):

    def setUp(self):
        self.test_conf = Config('./tests/configuration_test')
        # create db, tables
        create_tables(self.test_conf)


    def tearDown(self):
        os.remove('{}.sqlite3'.format(self.test_conf.db_filename))
        # delete obj in swift
        # db point to testdb when db point works ok
        # os.remove('{}.sqlite3'.format('hms'))

    def test_upload_obj(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                'birthdate':'19601010'
                }
        status, did = register_patient(data)

        self.assertTrue(status)
        self.assertIn('-', did)

        patient = PatientModel.get(PatientModel.email==patientid,
            PatientModel.firstname=='aaa',
            PatientModel.lastname=='bbb')
        self.assertEqual('19601010', patient.birthdate)

        objectname = str(uuid.uuid4())
        odata = {
                    "objname": objectname,
                    "datetime": "201511201300",
                    "description": "x-ray"
                }
        status, odict = upload_obj(patientid, odata)

        self.assertTrue(status)
        self.assertIsInstance(odict, dict)
        logger.debug('token:{}, storage_url:{}'.format(odict['auth_token'],
            odict['storage_url']))
        self.assertIn('auth_token', odict.keys())
        self.assertIn('storage_url', odict.keys())

        patient = PatientModel.get(PatientModel.email==patientid)
        obj = ObjectModel.get(ObjectModel.objid==patientid+'-'+objectname+'-'+odata['datetime'])
        self.assertIn(odata['description'], obj.description)
        self.assertEqual(patient, obj.patient)

    def test_get_obj(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                'birthdate':'19601010'
                }
        status, did = register_patient(data)


        patient = PatientModel.get(PatientModel.email==patientid,
            PatientModel.firstname=='aaa',
            PatientModel.lastname=='bbb')

        objectname = str(uuid.uuid4())
        odata = {
                    "objname": objectname,
                    "datetime": "201511201300",
                    "description": "x-ray"
                }
        status, odict0 = upload_obj(patientid, odata)

        status, odict = get_obj(patientid, patientid+'-'+objectname+'-'+odata['datetime'])

        logger.debug('get token:{}, storage_url:{}'.format(odict['auth_token'],
            odict['storage_url']))
        self.assertIn('auth_token', odict.keys())
        self.assertIn('storage_url', odict.keys())

    def test_get_objs(self):
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                'birthdate':'19601010'
                }
        status, did = register_patient(data)


        patient = PatientModel.get(PatientModel.email==patientid,
            PatientModel.firstname=='aaa',
            PatientModel.lastname=='bbb')

        objectname = str(uuid.uuid4())
        odata = {
                    "objname": objectname,
                    "datetime": "201511201300",
                    "description": "x-ray"
                }
        status, odict0 = upload_obj(patientid, odata)

        objectname2 = str(uuid.uuid4())
        odata2 = {
                    "objname": objectname2,
                    "datetime": "201511201300",
                    "description": "y-ray"
                }
        status2, odict2 = upload_obj(patientid, odata2)

        status, odict_list = get_objs(patientid)

        # logger.debug('get token:{}, storage_url:{}'.format(odict['auth_token'],
        #     odict['storage_url']))
        self.assertEqual(2, len(odict_list))
        odict_str = str(odict_list)
        self.assertIn('x-ray', odict_str)
        self.assertIn('y-ray', odict_str)

    def test_delete_obj(self):
        logger.debug('in test_delete_obj')
        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                'birthdate':'19601010'
                }
        status, did = register_patient(data)

        patient = PatientModel.get(PatientModel.email==patientid,
            PatientModel.firstname=='aaa',
            PatientModel.lastname=='bbb')

        objectname = str(uuid.uuid4())
        odata = {
                    "objname": objectname,
                    "datetime": "201511201300",
                    "description": "x-ray"
                }
        status, odictu = upload_obj(patientid, odata)
        logger.debug('upload token:{}, storage_url:{}'.format(odictu['auth_token'],
            odictu['storage_url']))
        status, odict = get_obj(patientid, patientid+'-'+objectname+'-'+odata['datetime'])

        logger.debug('get token:{}, storage_url:{}'.format(odict['auth_token'],
            odict['storage_url']))
        self.assertEqual(status, 1)

        SUCCESS_STATUS_CODES = [200, 201, 202, 204]
        storage_url = odictu['storage_url']
        headers = {'x-storage-token':odictu['auth_token']}
        files = {'file': open('configuration')}
        put_resp = requests.put(storage_url, files=files, headers=headers)
        page = put_resp.headers
        code = put_resp.status_code
        self.assertIn(code, SUCCESS_STATUS_CODES)

        status2, odict = delete_obj(patientid, patientid+'-'+objectname+'-'+odata['datetime'])
        self.assertEqual(status2, 1)


class AuthTest(unittest.TestCase):

    def setUp(self):
        self.test_conf = Config('tests/configuration_test')
        # create db, tables
        create_tables(self.test_conf)


    def tearDown(self):
        os.remove('{}.sqlite3'.format(self.test_conf.db_filename))
        # db point to testdb when db point works ok
        # os.remove('{}.sqlite3'.format('hms'))

    def test_authentication(self):
        logger.debug('in test_authentication')
        adminid = 'admin_{}'.format(str(uuid.uuid4()))
        LoginModel.create(
            username=adminid,
            password='admin',
            role='admin'
            )
        adm_login = {
                'username':adminid,
                'password':'admin',  }

        status, adm_token = authentication('admin', adm_login)
        self.assertTrue(status)
        logger.debug('adm_token:{}'.format(adm_token))

        doctorid = '{}@hms.com'.format(str(uuid.uuid4()))
        doc_data = {
                'email':doctorid,
                'firstname':'aaa',
                'lastname':'bbb',
                'experience':10,
                'patients': "['p1@a.com', 'p2@c.com']"
                }
        status, did = register_doctor(doc_data)
        self.assertTrue(status)
        LoginModel.create(
                    username=doctorid,
                    password='admin',
                    role='doctor')

        doc_login = {
                'username':doctorid,
                'password':'admin',  }

        status, doc_token = authentication('doctor', doc_login)
        self.assertTrue(status)
        logger.debug('doc_token:{}'.format(doc_token))

        patientid = '{}@hms.com'.format(str(uuid.uuid4()))
        p_data = {
                'email':patientid,
                'firstname':'aaa',
                'lastname':'bbb',
                }
        status, did = register_patient(p_data)
        self.assertTrue(status)
        LoginModel.create(
                    username=patientid,
                    password='admin',
                    role='patient')

        p_login = {
                'username':patientid,
                'password':'admin',  }

        status, patient_token = authentication('patient', p_login)
        self.assertTrue(status)
        logger.debug('patient_token:{}'.format(patient_token))



if __name__ == '__main__':
    unittest.main()
    os.remove('{}.sqlite3'.format('hms'))
