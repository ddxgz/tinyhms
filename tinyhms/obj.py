import json

import swiftclient

from tinyhms.models import database, ObjectModel, PatientModel
from tinyhms.hmsexceptions import UserNotExistException
from tinyhms.config import conf
from tinyhms.utils import logger


def upload_obj(patientid, post_data):
    """
    Upload an obj in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( obj's info on success, err info on failure)
    """
    # print(post_data)
    obj = ''
    try:
        logger.debug('in upload_obj')
        logger.debug('auth_url:{}, account_username:{}, password:{}'.format(
            conf.auth_url, conf.account_username, conf.password))

        resp_dict = {}
        storage_url, auth_token = swiftclient.client.get_auth(
                                        conf.auth_url,
                                        conf.account_username,
                                      conf.password,
                                      auth_version=conf.auth_version)
        resp_dict['auth_token'] = auth_token
        resp_dict['storage_url'] = storage_url + '/' + \
                        conf.container + '/' + patientid + '/' + \
                        patientid + '-' + post_data['objname'] + '-' + post_data['datetime']
        with database.atomic():
            obj = ObjectModel.create_by_dict(patientid, post_data)
            logger.debug(obj)
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
        q = ObjectModel.delete().where(ObjectModel.objid==
            patientid + '-' + post_data['objname'] + '-' + post_data['datetime'])
        q.execute()
        return 0, {'errinfo':'create obj failed, did not create obj'}

    else:
        resp_dict['info'] = 'make PUT request to storage_url with auth_token as "x-storage-token" in headers'
        return 1, resp_dict


def get_obj(patientid, objid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    info = {}
    try:
        resp_dict = {}
        obj = ObjectModel.get(ObjectModel.objid==objid)

        storage_url, auth_token = swiftclient.client.get_auth(
                                        conf.auth_url,
                                        conf.account_username,
                                      conf.password,
                                      auth_version=conf.auth_version)
        resp_dict['auth_token'] = auth_token
        resp_dict['storage_url'] = storage_url + '/' + \
                        conf.container + '/' + patientid + '/' + objid

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get obj failed'}

    else:
        return 1, resp_dict


def get_objs(patientid):
    """
    Get info of a doctor in the system.

    :param doctorid: doctor's uid
    :returns: a status, a str ( doctor's info on success, err info on failure)
    """
    # print(doctorid)
    logger.debug('in get_objs')
    resp_list = []
    try:
        patient = PatientModel.get(PatientModel.email==patientid)

        for obj in ObjectModel.select().where(ObjectModel.patient==patient):
            logger.debug('objid: %s, descrip: %s' % (obj.objid, obj.description))
            resp_dict = {}
            resp_dict['objid'] = obj.objid
            resp_dict['objname'] = obj.objname
            resp_dict['description'] = obj.description
            resp_dict['datetime'] = obj.datetime
            resp_list.append(resp_dict)
        logger.debug('objs:{}'.format(resp_list))

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'get objs failed'}

    else:
        return 1, resp_list


def delete_obj(patientid, objid):
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
        meta, objects = conn.get_container(conf.container,
            prefix=patientid + '/' + objid)
        logger.debug('meta: %s,  \n objects: %s' % (meta, objects))
        if objects:
            for obj in objects:
                conn.delete_object(conf.container, obj['name'])
                resp_dict['description_'+obj['name']] = \
                    '{} have been deleted'.format(obj['name'])
        else:
            resp_dict['description'] = 'There is no file to be deleted'
        logger.debug('resp_dict:%s' % resp_dict)

        q = ObjectModel.delete().where(ObjectModel.objid==objid)
        q.execute()
        resp_dict[objid] = 'deleted from db'
        logger.debug('resp_dict:%s' % resp_dict)

    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, {'errinfo':'delete obj failed, did not delete obj'}

    else:
        return 1, resp_dict

# get_objs('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
# delete_obj('67dae658-4274-4261-9e6f-6af018a50862@hms.com')
