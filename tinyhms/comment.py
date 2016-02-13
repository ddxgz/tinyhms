import json

import swiftclient

from tinyhms.models import database, CommentModel, PatientModel
from tinyhms.hmsexceptions import UserNotExistException
from tinyhms.config import conf
from tinyhms.utils import logger


def upload_comment(patientid, doctorid, post_data):
    """
    Upload an comment in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( comment's info on success, err info on failure)
    """
    # print(post_data)
    comment = ''
    try:
        logger.debug('in upload_comment')

        resp_dict = {}
        with database.atomic():
            comment = CommentModel.create_by_dict(patientid, doctorid, post_data)
            logger.debug('comment:{}'.format(comment))
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
        q = CommentModel.delete().where(CommentModel.drug_id==
            patientid + '-' + doctorid + '-' + post_data['datetime'])
        q.execute()
        return 0, {'errinfo':'create comment failed, did not create comment'}

    else:
        # resp_dict['info'] = 'make PUT request to storage_url with auth_token as "x-storage-token" in headers'
        resp_dict['comment_id'] = comment.comment_id
        return 1, resp_dict


def get_comments(patientid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    logger.debug('in get_comments')
    resp_list = []
    try:
        patient = PatientModel.get(PatientModel.email==patientid)

        for comment in CommentModel.select().where(CommentModel.patient==patient):
            logger.debug('comment_id: %s, comment: %s' % (comment.comment_id, comment.comment))
            resp_dict = {}
            resp_dict['comment'] = comment.comment
            resp_dict['datetime'] = comment.datetime
            resp_dict['response_doctor'] = comment.response_doctor
            resp_list.append(resp_dict)
        logger.debug('comments:{}'.format(resp_list))

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get comments failed'}

    else:
        return 1, resp_list




# get_comments('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
# delete_comment('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
