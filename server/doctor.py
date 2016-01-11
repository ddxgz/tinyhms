import json

from server.models import database, DoctorModel, LoginModel
from server.hmsexceptions import UserNotExistException
from server.utils import logger


def register_doctor(post_data):
    """
    Register a doctor in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( doctor's info on success, err info on failure)
    """
    # print(post_data)
    doctor = ''
    try:
        logger.debug('in register_doctor')

        with database.atomic():
            doctor = DoctorModel.create_by_dict(post_data)
            logger.debug(doctor)
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
        q = DoctorModel.delete().where(DoctorModel.email==doctor)
        q.execute()
        return 0, 'create doctor failed, did not create doctor', ''
    try:
        with database.atomic():
            user = LoginModel.create_by_dict('doctor', post_data)
            logger.debug(doctor)
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
        q = LoginModel.delete().where(LoginModel.username==doctor)
        q.execute()
        return 0, 'create doctor failed, did not create doctor', ''

    else:
        return 1, str(doctor), str(user.password)


def edit_doctor(doctorid, post_data):
    """
    Edit a doctor in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( doctor's info on success, err info on failure)
    """
    # print(post_data)
    try:
        logger.debug('in edit_doctor')
        DoctorModel.update_by_dict(doctorid, post_data)
        logger.debug('executed')
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
        return 0, 'edit_doctor failed, did not edit doctor'
    else:
        return 1, str(doctorid)


def get_doctor(doctorid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
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
        logger.debug(doctor_json)

        return 1, doctor_json


def get_doctors():
    """
    Get info of doctors in the system.

    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    logger.debug('in get_doctors')
    resp_list = []
    try:
        # patient = DoctorModel.get(DoctorModel.email==patientid)
        doctors = DoctorModel.select()
        print(doctors)
        for doc in doctors:
            print('doc')
            logger.debug('docid: %s' % (doc))
            resp_dict = {}
            resp_dict['doctorid'] = doc.email
            resp_dict['last_name'] = doc.last_name
            resp_dict['first_name'] = doc.first_name
            resp_list.append(resp_dict)
        logger.debug('doctors:{}'.format(resp_list))

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get doctors failed'}

    else:
        return 1, resp_list
