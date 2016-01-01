import json

import swiftclient

from server.models import database, PrescriptionModel, PatientModel
from server.hmsexceptions import UserNotExistException
from server.config import conf
from server.utils import logger


def upload_prescription(patientid, post_data):
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
            prescription = PrescriptionModel.create_by_dict(patientid, post_data)
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


def get_prescription(patientid, prescriptionid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    info = {}
    try:
        resp_dict = {}
        prescription = PrescriptionModel.get(PrescriptionModel.prescriptionid==prescriptionid)

        storage_url, auth_token = swiftclient.client.get_auth(
                                        conf.auth_url,
                                        conf.account_username,
                                      conf.password,
                                      auth_version=conf.auth_version)
        resp_dict['auth_token'] = auth_token
        resp_dict['storage_url'] = storage_url + '/' + \
                        conf.container + '/' + patientid + '/' + prescriptionid

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get prescription failed'}

    else:
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
            logger.debug('prescriptionid: %s, descrip: %s' % (prescription.prescriptionid, prescription.description))
            resp_dict = {}
            resp_dict['prescriptionid'] = prescription.prescriptionid
            resp_dict['prescriptionname'] = prescription.prescriptionname
            resp_dict['description'] = prescription.description
            resp_dict['datetime'] = prescription.datetime
            resp_list.append(resp_dict)
        logger.debug('prescriptions:{}'.format(resp_list))

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get prescriptions failed'}

    else:
        return 1, resp_list


def delete_prescription(patientid, prescriptionid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    info = {}
    try:
        resp_dict = {}

        conn = swiftclient.client.Connection(conf.auth_url,
                        conf.account_username,
                        conf.password,
                        auth_version=conf.auth_version)
        meta, prescriptionects = conn.get_container(conf.container,
            prefix=patientid + '/' + prescriptionid)
        logger.debug('meta: %s,  \n prescriptionects: %s' % (meta, prescriptionects))
        if prescriptionects:
            for prescription in prescriptionects:
                conn.delete_prescriptionect(conf.container, prescription['name'])
                resp_dict['description_'+prescription['name']] = \
                    '{} have been deleted'.format(prescription['name'])
        else:
            resp_dict['description'] = 'There is no file to be deleted'
        logger.debug('resp_dict:%s' % resp_dict)

        q = PrescriptionModel.delete().where(PrescriptionModel.prescriptionid==prescriptionid)
        q.execute()
        resp_dict[prescriptionid] = 'deleted from db'
        logger.debug('resp_dict:%s' % resp_dict)

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'delete prescription failed, did not delete prescription'}

    else:
        return 1, resp_dict

# get_prescriptions('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
# delete_prescription('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
