import json
import uuid
import ast

from server.models import database, LoginModel, DoctorModel, PatientModel
from server import rediscli
from server.hmsexceptions import UserNotExistException
from server.utils import logger


def authentication(role, post_data):
    """
    Register a patient in the system. The post data is in json format.
    :param post_data: dict
    :returns: a status, a str( patient's info on success, err info on failure)
    """
    # print(post_data)
    auth_dict = {}
    try:
        logger.debug('in register_patient')

        user = LoginModel.get(LoginModel.username==post_data['username'],
                                LoginModel.role==role)
    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, 'auth failed'
    else:
        logger.debug("user.password:{}, post_data['password']:{}".format(
            user.password, post_data['password']))
        if user.password==post_data['password']:
            try:
                # auth_dict['token'] = get_token(post_data['username'], role)
                token = get_token(post_data['username'], role)
            except Exception as ex:
                logger.error('Exception: ', ex)
                return 0, 'auth failed, get token failed'
            else:
                # auth_json = json.dumps(auth_dict)
                logger.debug(token)
                return 1, token
        else:
            return 0, 'auth failed, password not match'


def get_token(username, role):
    if role == 'admin':
        token = uuid.uuid4().hex
        rediscli.set_data('auth/admin', token)
        return token
    elif role == 'doctor':
        logger.debug('in doctor get_token, username:{}, role:{}'.format(username, role))
        user = DoctorModel.get(DoctorModel.email==username)
        logger.debug('user.patients:{}, type:{}'.format(user.patients, type(user.patients)))
        # patient_list = json.loads(str(user.patients))
        if user.patients:
            patient_list = ast.literal_eval(user.patients)
        else:
            patient_list = []
        logger.debug('patient_list:{}, type:{}'.format(patient_list, type(patient_list)))
        token = uuid.uuid4().hex
        rediscli.set_data('auth/{}'.format(username), token)
        for patient in patient_list:
            rediscli.set_data('auth/{}/{}'.format(username, patient), token)
        return token
    elif role == 'patient':
        token = uuid.uuid4().hex
        rediscli.set_data('auth/{}'.format(username), token)
        return token
