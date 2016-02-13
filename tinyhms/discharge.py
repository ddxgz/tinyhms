import json

import swiftclient

from tinyhms.models import database, DischargeModel, PatientModel
from tinyhms.hmsexceptions import UserNotExistException
from tinyhms.config import conf
from tinyhms.utils import logger


def upload_discharge(patientid, doctorid, post_data):
    """
    Upload an discharge in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( discharge's info on success, err info on failure)
    """
    # print(post_data)
    discharge = ''
    try:
        logger.debug('in upload_discharge')

        resp_dict = {}
        with database.atomic():
            discharge = DischargeModel.create_by_dict(patientid, doctorid, post_data)
            logger.debug('discharge:{}'.format(discharge))
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
        q = DischargeModel.delete().where(DischargeModel.discharge_id==
            patientid + '-' + doctorid + '-' + post_data['indate'])
        q.execute()
        return 0, {'errinfo':'create discharge failed, did not create discharge'}

    else:
        # resp_dict['info'] = 'make PUT request to storage_url with auth_token as "x-storage-token" in headers'
        resp_dict['discharge_id'] = discharge.discharge_id
        return 1, resp_dict


def update_discharge(patientid, doctorid, indate, post_data):
    """
    Upload an discharge in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( discharge's info on success, err info on failure)
    """
    # print(post_data)
    discharge = ''
    try:
        logger.debug('in update_discharge')

        resp_dict = {}

        DischargeModel.update_by_dict(patientid, doctorid,
                indate, post_data)
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
        return 0, {'errinfo':'update discharge failed, did not create discharge'}

    else:
        # resp_dict['info'] = 'make PUT request to storage_url with auth_token as "x-storage-token" in headers'
        resp_dict['discharge_id'] = patientid + '-' + doctorid + '-' + \
            indate
        return 1, resp_dict


def get_discharges(patientid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    logger.debug('in get_discharges')
    resp_list = []
    try:
        patient = PatientModel.get(PatientModel.email==patientid)

        for discharge in DischargeModel.select().where(DischargeModel.patient==patient):
            logger.debug('discharge_id: %s, indate: %s' % (discharge.discharge_id, discharge.indate))
            resp_dict = {}
            resp_dict['indate'] = discharge.indate
            resp_dict['outdate'] = discharge.outdate
            resp_dict['response_doctor'] = discharge.response_doctor
            resp_dict['description'] = discharge.description
            resp_dict['datetime'] = discharge.datetime
            resp_list.append(resp_dict)
        logger.debug('discharges:{}'.format(resp_list))

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get discharges failed'}

    else:
        return 1, resp_list




# get_comments('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
# delete_comment('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
