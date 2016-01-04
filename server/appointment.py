import json
import ast

from server.models import database, DoctorModel
from server import rediscli
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
    3.2 add the appointment to the doctor's that day's schedule
    4. return if appointment exists, with reason if fail

    """
    # print(post_data)
    try:
        logger.debug('in make_appointment')

    # check db when patient is ok
        rediscli.set_data(
            post_data['doctorid']+'/'+post_data['datetimeslot']+'/'+
                post_data['patientid'], post_data)
        schedule = rediscli.get_data(post_data['doctorid']+'/'+
            post_data['datetimeslot'][:8])
        if schedule:
            schedule = ast.literal_eval(schedule)
            schedule[post_data['datetimeslot'][8:]] = '1'
            rediscli.set_data(post_data['doctorid']+'/'+post_data['datetimeslot'][:8],
                json.dumps(schedule))
        else:
            schedule = {post_data['datetimeslot'][8:]:'1'}
            logger.debug('in make_appointment, schedule:{}'.format(json.dumps(schedule)))
            rediscli.set_data(post_data['doctorid']+'/'+post_data['datetimeslot'][:8],
                json.dumps(schedule))

    except Exception as ex:
        logger.error('Exception: ', ex)
        # q = DoctorModel.delete().where(DoctorModel.uid==doctor)
        # q.execute()
        return 0, 'make_appointment failed, did not make_appointment'

    else:
        return 1, str(post_data['doctorid']+'/'+post_data['datetimeslot']+'/'+
                        post_data['patientid'])


def get_appointment(appointment_url):
    """
    Get info of an appointment in the system.

    :param appointment_url: appointment's url
    :returns: a status, a str ( appointment's info on success, err info on failure)
    """
    # print(appointment_url)
    info = {}
    try:
        logger.debug('in get_appointment')
        # check redis
        appointment = str(rediscli.get_data(appointment_url))
        logger.debug(appointment)
    # except UserNotExistException:
    #     logger.debug('in UserNotExistException')
    #     return 0, 'get doctor failed, the required Doctor Did Not Exist'
    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, 'get appointment failed'
    else:
        # appointment_json = json.dumps({'illness':appointment})
        return 1, appointment


def check_appointment(doctorid, date):
    """
    Get info of appointments for a doctor on a date in the system.

    :param appointment_url: appointment's url
    :returns: a status, a str ( appointments timeslots info on success,
                                    err info on failure)
    """
    # print(doctorid, date)
    # info = {}
    try:
        logger.debug('in check_appointment')
        schedule = rediscli.get_data(doctorid+'/'+date)
    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, 'check_appointment failed'
    else:
        logger.debug('in check_appointment schedule data:{}'.format(schedule))
        if schedule:
            logger.debug('in check_appointment schedule data:{}'.format(schedule))
            # appointments_json = json.dumps(schedule)
            return 1, schedule
        # no appointment for this doctor on this date
        else:
            return 1, '{}'


def delete_appointment(doctorid, datetimeslot, patientid):
    """
    delete_appointment in the system. The post data is in json format.

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
    3.2 add the appointment to the doctor's that day's schedule
    4. return if appointment exists, with reason if fail

    """
    # print(post_data)
    try:
        logger.debug('in delete_appointment')

    # check db when patient is ok
        rediscli.delete_data(doctorid + '/' + datetimeslot + '/' + patientid)
        schedule = rediscli.get_data(doctorid + '/' + datetimeslot[:8])
        if schedule:
            schedule = ast.literal_eval(schedule)
            del schedule[datetimeslot[8:]]
            rediscli.set_data(doctorid + '/' + datetimeslot[:8],
                json.dumps(schedule))


    except Exception as ex:
        logger.error('Exception: ', ex)
        # q = DoctorModel.delete().where(DoctorModel.uid==doctor)
        # q.execute()
        return 0, 'delete_appointment failed, did not delete_appointment'

    else:
        return 1, str(doctorid + '/' + datetimeslot + '/' + patientid)
