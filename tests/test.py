import os
import unittest
import uuid
import ast
import time

from server.doctor import register_doctor, get_doctor, edit_doctor
from server.patient import register_patient, get_patient
from server.appointment import make_appointment, get_appointment, check_appointment
from server.models import create_tables, DoctorModel, PatientModel
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

    def test_register_doctor(self):
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


    def test_get_doctor(self):
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


if __name__ == '__main__':
    unittest.main()
