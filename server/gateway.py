#!/usr/bin/env python3

#from __future__ import absolute_import#, division, print_function

from wsgiref import simple_server
import json

import falcon
#
from server.config import conf


#conf = Config()


class AuthMiddleware(object):

    def process_request(self, req, resp):
        token = req.get_header('X-Auth-Token')
        project = req.get_header('X-Project-ID')

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token, project):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          href='http://docs.example.com/auth',
                                          scheme='Token; UUID')

    def _token_is_valid(self, token, project):
        return True


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])


if conf.api_version == "1":
    from server.apiv1 import RegDoctorListener, DoctorListener, RegPatientListener, \
        PatientListener, MakeAppointmentListener, AppointmentListener, \
        AppointmentListListener, AppointmentSinkAdapter, PostObjListener, ObjectListener, \
        ObjectListListener, AuthListener, PostPrescriptionListener

# elif conf.api_version is "2":
#     from apiv2 import HomeListener, AccountListener, \
#         DiskSinkAdapter
else:
    print('api_version in configuration is wrong!')

app = falcon.API(middleware=[
            # AuthMiddleware(),
            RequireJSON(),
            JSONTranslator(),
        ])

appointment_listener = AppointmentListener()
make_appointment_listener = MakeAppointmentListener()
appointment_list_listener = AppointmentListListener()
appointment_sink = AppointmentSinkAdapter()

reg_doctor_listener = RegDoctorListener()
doctor_listener = DoctorListener()
reg_patient_listener = RegPatientListener()
patient_listener = PatientListener()

post_obj_listener = PostObjListener()
obj_listener = ObjectListener()
objlist_listener = ObjectListListener()

post_prescription_listener = PostPrescriptionListener()

auth_listener = AuthListener()

app.add_route('/v1/appointment', make_appointment_listener)
app.add_route('/v1/appointment/{doctorid}/{datetimeslot}/{patientid}',
                appointment_listener)
# app.add_route('/v1/appointment/{doctorid}/{date}}',appointment_list_listener)
app.add_sink(appointment_sink, r'^/v1/appointment/(?P<doctor_date>.+?)$')

app.add_route('/v1/doctor', reg_doctor_listener)
app.add_route('/v1/doctor/{doctorid}', doctor_listener)

app.add_route('/v1/patient', reg_patient_listener)
app.add_route('/v1/patient/{patientid}', patient_listener)

app.add_route('/v1/obj/{patientid}', post_obj_listener)
app.add_route('/v1/objs/{patientid}', objlist_listener)
app.add_route('/v1/obj/{patientid}/{objid}', obj_listener)

app.add_route('/v1/prescription/{doctorid}/{patientid}', post_prescription_listener)

app.add_route('/v1/auth/{role}', auth_listener)


def start_gateway_service(ip='0.0.0.0', port=8080):
    httpd = simple_server.make_server(ip, port, app)
    httpd.serve_forever()

## Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    # create db
    # create admin account
    # create hms container in swift
    start_gateway_service()
