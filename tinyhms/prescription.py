import json

import swiftclient

from tinyhms.models import database, PrescriptionModel, PatientModel
from tinyhms.hmsexceptions import UserNotExistException
from tinyhms.config import conf
from tinyhms.utils import logger


def upload_prescription(patientid, doctorid, post_data):
    """
    Upload an prescription in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( prescription's info on success, err info on failure)
    """
    # print(post_data)
    prescription = ''
    try:
        logger.debug('in upload_prescription')

        resp_dict = {}
        with database.atomic():
            prescription = PrescriptionModel.create_by_dict(patientid, doctorid, post_data)
            logger.debug('prescription:{}'.format(prescription))
            logger.debug('in database.atomic')
    # except peewee.IntegrityError:
    #     logger.warning('in doctor model create except')

        # # `username` is a unique column, so this username already exists,
        # # making it safe to call .get().
        # old_user = AccountModel.get(AccountModel.username == username)
        # logger.warning('user exists...')
        # resp_dict['info'] = 'user exists, did not create user:%s' % username
        # resp.status = falcon.HTTP_409
        # try:
        #     change_user = AccountModel.get(AccountModel.username==username,
        #                     AccountModel.password==password)
        # except:
        #     logger.debug('change user data failed...')
    except Exception as ex:
        logger.error('Exception: ', ex)
        q = PrescriptionModel.delete().where(PrescriptionModel.drug_id==
            patientid + '-' + post_data['drug_name'] + '-' + post_data['datetime'])
        q.execute()
        return 0, {'errinfo':'create prescription failed, did not create prescription'}

    else:
        # resp_dict['info'] = 'make PUT request to storage_url with auth_token as "x-storage-token" in headers'
        resp_dict['drug_id'] = prescription.drug_id
        return 1, resp_dict


def get_prescriptions(patientid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    logger.debug('in get_prescriptions')
    resp_list = []
    try:
        patient = PatientModel.get(PatientModel.email==patientid)

        for prescription in PrescriptionModel.select().where(PrescriptionModel.patient==patient):
            logger.debug('drug_id: %s, descrip: %s' % (prescription.drug_id, prescription.description))
            resp_dict = {}
            resp_dict['drug_name'] = prescription.drug_name
            resp_dict['after_meal'] = prescription.after_meal
            resp_dict['description'] = prescription.description
            resp_dict['datetime'] = prescription.datetime
            resp_dict['amount'] = prescription.amount
            resp_dict['dosage_per_day'] = prescription.dosage_per_day
            resp_dict['response_doctor'] = prescription.response_doctor
            resp_list.append(resp_dict)
        logger.debug('prescriptions:{}'.format(resp_list))

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get prescriptions failed'}

    else:
        return 1, resp_list




# get_prescriptions('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
# delete_prescription('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
