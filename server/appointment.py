import json

from server.models import database, DoctorModel
from server.hmsexceptions import UserNotExistException
from server.utils import logger


def make_appointment(post_data):
    """
    make_appointment in the system. The post data is in json format.

    :param post_data: dict
    :returns: a status, a str( appointment's url on success, err info on failure)

    with database.atomic():
                doctor = DoctorModel.create_by_dict(post_data)
                logger.debug(doctor)
                logger.debug('in database.atomic')
        except peewee.IntegrityError:
            logger.warning('in doctor model create except')

    1. check if patient and doctor exist in db
    2. check if the appointment exist in redis
    3. make appointment if 1 and 2 ok
    4. return if appointment exists, with reason if fail

    """
    print(post_data)
    try:
        logger.debug('in make_appointment')

    # check db when patient is ok

    except Exception as ex:
        logger.error('Exception: ', ex)
        # q = DoctorModel.delete().where(DoctorModel.uid==doctor)
        # q.execute()
        return 0, 'make_appointment failed, did not make_appointment'

    else:
        return 1, str('d001/2015/pa002')


def get_appointment(appointment_url):
    """
    Get info of an appointment in the system.

    :param appointment_url: appointment's url
    :returns: a status, a str ( appointment's info on success, err info on failure)
    """
    print(appointment_url)
    info = {}
    try:
        logger.debug('in get_appointment')
        # check redis
        # appointment = DoctorModel.get_dict(appointment_url)
        logger.debug(appointment)
    # except UserNotExistException:
    #     logger.debug('in UserNotExistException')
    #     return 0, 'get doctor failed, the required Doctor Did Not Exist'
    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, 'get appointment failed'
    else:
        appointment_json = json.dumps(appointment)
        return 1, appointment_json
