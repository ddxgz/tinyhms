import json

from server.models import database, DoctorModel
from server.hmsexceptions import UserNotExistException
from server.utils import logger


def register_doctor(post_data):
    """
    Register a doctor in the system. The post data is in json format.

    :param post_data: dict
    :returns: a status, a str( doctor's info on success, err info on failure)
    """
    print(post_data)
    try:
        logger.debug('in register_doctor')

        with database.atomic():
            doctor = DoctorModel.create_by_dict(post_data)
            logger.debug(doctor)
            logger.debug('in database.atomic')
    except peewee.IntegrityError:
        logger.warning('in doctor model create except')

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
        q = DoctorModel.delete().where(DoctorModel.uid==doctor)
        q.execute()
        return 0, 'create doctor failed, did not create doctor'

    else:
        return 1, str(doctor)


def get_doctor(doctorid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    print(doctorid)
    info = {}
    try:
        logger.debug('in get_doctor')
        doctor_dict = DoctorModel.get_dict(doctorid)
        logger.debug(doctor_dict)
    except UserNotExistException:
        logger.debug('in UserNotExistException')
        return 0, 'get doctor failed, the required Doctor Did Not Exist'
    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, 'get doctor failed'
    else:
        doctor_json = json.dumps(doctor_dict)
        return 1, doctor_json
