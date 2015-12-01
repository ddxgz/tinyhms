# import asyncio
import sys

from verbs import VisitPy2 as Visit


# visit = Visit('http://192.168.59.100:8008/v1/app')
visit = Visit('http://192.168.59.200:8080/v1')


headers = { 'username':'user1',
            'password':'self.test_account_pw1',
            'content-type': 'application/json'}
# data = """{ 'email': {
#             'from':'password1',
#             'to':'user1@email.com' }
#         }"""
#
data = {
        'firstname':'aaa',
        'lastname':'bbb',
        'experience':'10'
        }


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(visit.post(suffix_url='doctor',
            headers=headers, data=data))
    elif len(sys.argv) == 2:
        uid = sys.argv[1]
        print(visit.get(suffix_url='doctor/{}'.format(uid), headers=headers))
