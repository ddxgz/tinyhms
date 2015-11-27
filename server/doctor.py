import uuid

from server.models import database, DoctorModel
from server.utils import logger


def register_doctor(post_data):
    print(post_data)
    try:
        logger.debug('in register_doctor')

        with database.atomic():
            new_user = DoctorModel.create_by_dict(post_data)
            logger.debug(new_user)
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
        q = DoctorModel.delete().where(DoctorModel.uid==new_user)
        q.execute()
        return 0, 'create doctor failed, did not create doctor'

    else:
        return 1, str(new_user)
