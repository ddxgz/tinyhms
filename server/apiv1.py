from __future__ import absolute_import#, division, print_function

from wsgiref import simple_server
import json
import sys, os
import datetime
import functools

import falcon

from server import doctor
from server.utils import logger


def max_body(limit):

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)
    return hook


class RegDoctorListener:

    @falcon.before(max_body(64*1024))
    def on_post(self, req, resp):
        """
        Register a doctor in the system. The post data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's id, or other related info
                {"doctorid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as err:
            logger.error('error when try to get headers and data, ', err)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, doctorid = doctor.register_doctor(post_data)

        except Exception as err:
            logger.exception('error when register doctor, ', err)
            resp_dict['info'] = 'Error when register doctor {}'.format(
                post_data['lastname'])
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('register ok, status positive')
                resp_dict['info'] = 'Register doctor {} success'.format(
                    post_data['lastname'])
                resp_dict['doctorid'] = doctorid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(resp_dict,
                    sort_keys=True, indent=4)
            else:
                logger.exception('return error when try to register doctor, ', err)
                resp_dict['info'] = 'Error when register doctor {}'.format(
                    post_data['lastname'])
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict, sort_keys=True,
                    indent=4)

class DoctorListener:

    def on_get(self, req, resp, doctorid):

        resp.status = falcon.HTTP_200
        resp.body = 'aaaa'

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass


class MakeAppointmentListener:

    @falcon.before(max_body(64*1024))
    def on_post(self, req, resp, user, appname):
        """
        :param req.header.username: the username, should be tenant:user when dev
        :param req.header.password: password
        :returns: a json contains all objects in disk container, and metameata
                {"meta":{}, "objects":{"obj1": {}}}
        """
        resp_dict = {}
        docker_resp = 'nothing'
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            post_data = req.context['doc']
            logger.debug('username:%s, password:%s, data:%s'
                % (username, password, post_data))
            logger.debug(' user:{}, appname:{}'.format(
                user, appname))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as err:
            logger.error('error when try to get headers and data, ', err)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:

            """
            handle_request:

            """
            status, body = create_app(user, appname, post_data)

        except Exception as err:
            logger.exception('error when try to handle_request, ', err)
            resp_dict['info'] = 'user:{} password not correct'.format(user)
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(resp_dict)
        else:
            # resp.status = status or falcon.HTTP_200
            resp.status = falcon.HTTP_200
            resp.body = body or json.dumps(resp_dict,
                sort_keys=True, indent=4)

    def on_get(self, req, resp):
        logger.debug('in get for:{}'.format(req.get_header('username')))

        resp.stream = ResponseStream(resp.stream)
        service_requests = print_int(req.get_header('username'),
                callback=resp.stream.write)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(service_requests)


    def on_delete(self, req, resp):
        pass


class AppointmentListener:

    @falcon.before(max_body(64*1024))
    def on_post(self, req, resp, user, appname):
        pass

    def on_get(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
