# import asyncio
import sys

from verbs import VisitPy2 as Visit


# visit = Visit('http://192.168.59.100:8008/v1/app')
#visit = Visit('http://192.168.59.200:8080/v1')
visit = Visit('http://127.0.0.1:8080/v1')


headers = { 'username':'user1',
            'password':'self.test_account_pw1',
            'content-type': 'application/json'}
# data = """{ 'email': {
#             'from':'password1',
#             'to':'user1@email.com' }
#         }"""
#
# data = {
#        'email': 'a@b.com',
#         'firstname':'aaa',
#         'lastname':'bbb',
#         'experience':'10'
#         }
# data = {
#     'doctorid':'d001',
#     'datetimeslot':'201511201400',
#     'patientid':'p001',
#     'illness': 'illness01',
# }
# #
data = {
        'email': 'a@b.com',
        'firstname':'aaa',
        'lastname':'bbb',
        'birthdate':'20151111'
        }

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     print(visit.post(suffix_url='doctor',
    #         headers=headers, data=data))
    # elif len(sys.argv) == 2:
    #     uid = sys.argv[1]
    #     print(visit.get(suffix_url='doctor/{}'.format(uid), headers=headers))
    #     data2 = {
    #             'firstname':'ccc',
    #             'lastname':'ddd',
    #             'experience':20
    #             }
    #     print(visit.put(suffix_url='doctor/{}'.format(uid),
    #                 headers=headers, data=data2))
    #     print(visit.get(suffix_url='doctor/{}'.format(uid), headers=headers))

    # if len(sys.argv) == 1:
    #     print(visit.post(suffix_url='appointment',
    #         headers=headers, data=data))
    # elif len(sys.argv) == 2:
    #     docidtimepaid = sys.argv[1]
    #     print(visit.get(suffix_url='appointment/{}'.format(docidtimepaid), headers=headers))
    # elif len(sys.argv) == 2:
    #     docidtime = sys.argv[1]
    #     print(visit.get(suffix_url='appointment/{}'.format(docidtime), headers=headers))


    if len(sys.argv) == 1:
        print(visit.post(suffix_url='patient',
            headers=headers, data=data))
    elif len(sys.argv) == 2:
        uid = sys.argv[1]
        print(visit.get(suffix_url='patient/{}'.format(uid), headers=headers))
        data2 = {
                'firstname':'ccc',
                'lastname':'ddd',
                'birthdate':'19999999'
                }
        print(visit.put(suffix_url='patient/{}'.format(uid),
                    headers=headers, data=data2))
        print(visit.get(suffix_url='patient/{}'.format(uid), headers=headers))
