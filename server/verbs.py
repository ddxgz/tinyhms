import ast
try:
    import urllib2
except:
    import urllib as urllib2
import requests
import logging
import time
import json
# import asyncio

from utils import logger
# logging.basicConfig(format='===========%(levelname)s:%(message)s=========',
#     level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG,
#                 format='\n[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
#                 datefmt='%d %b %Y %H:%M:%S')

"""
requests doc:
http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
"""

class VisitPy2():
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def _rslash(self, suffix_url):
        return '/' + suffix_url.lstrip('/')

    # @asyncio.coroutine
    def get(self, suffix_url='', headers=None, data=None, wait=0):
        # print('%s sleep:%s' % (headers['username'], 1/wait))
        # yield from asyncio.sleep(1/wait)
        # req = urllib2.Request(self.baseurl+suffix_url, headers=headers)
        req = urllib2.Request(self.baseurl+self._rslash(suffix_url),
                                headers=headers)
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+self._rslash(suffix_url),
            headers=headers,
            data=data)
        req.get_method = lambda: 'PUT'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put_file(self, filename='', suffix_url='', headers=None, data=None):
        code_url, resp_str = self.put(suffix_url=self._rslash(suffix_url),
            headers=headers)
        resp = ast.literal_eval(resp_str)
        logging.debug('resp:%s' % (resp))
        token = resp.get('auth_token')
        storage_url = resp.get('storage_url')
        headers = {'x-storage-token':token}
        files = {'file': open(filename)}
        put_resp = requests.put(storage_url, files=files, headers=headers)
        page = put_resp.headers
        code = put_resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page


    def post(self, suffix_url='', headers=None, data=None):
        # req = urllib2.Request(self.baseurl+self._rslash(suffix_url),
        #     headers=headers, data=data)
        # resp = urllib2.urlopen(req)
        # page = resp.read()
        # code = resp.getcode()
        # logging.debug('code:%s, page:%s' % (code, page))
        # return code, page
        return self._requests_post(suffix_url=suffix_url, headers=headers,
            data=data)

    def _requests_post(self, suffix_url='', headers=None, data=None):
        if isinstance(data, dict):
            logger.debug('data is dict')
            resp = requests.post(self.baseurl+self._rslash(suffix_url),
                headers=headers, data=json.dumps(data))
        elif isinstance(data, str):
            logger.debug('data is dict')
            resp = requests.post(self.baseurl+self._rslash(suffix_url),
                headers=headers, json=data)
        # page = resp.headers
        page = resp.text
        code = resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page


    def delete(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+self._rslash(suffix_url),
            headers=headers,
            data=data)
        req.get_method = lambda: 'DELETE'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page


class Visit():
    def __init__(self, baseurl):
        self.baseurl = baseurl

    # @asyncio.coroutine
    def get(self, suffix_url='', headers=None, data=None, wait=0):
        print('%s sleep:%s' % (headers['username'], 1/wait))
        # yield from asyncio.sleep(1/wait)
        # req = urllib2.Request(self.baseurl+suffix_url, headers=headers)
        req = urllib2.request.Request(self.baseurl+suffix_url, headers=headers)
        resp = urllib2.request.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers,
            data=data)
        req.get_method = lambda: 'PUT'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page

    def put_file(self, filename='', suffix_url='', headers=None, data=None):
        code_url, resp_str = self.put(suffix_url=suffix_url, headers=headers)
        resp = ast.literal_eval(resp_str)
        logging.debug('resp:%s' % (resp))
        token = resp.get('auth_token')
        storage_url = resp.get('storage_url')
        headers = {'x-storage-token':token}
        files = {'file': open(filename)}
        put_resp = requests.put(storage_url, files=files, headers=headers)
        page = put_resp.headers
        code = put_resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page


    def post(self, suffix_url='', headers=None, data=None):
        req = urllib2.request.Request(self.baseurl+suffix_url,
            headers=headers, data=data)
        resp = urllib2.request.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page


    def delete(self, suffix_url='', headers=None, data=None):
        req = urllib2.Request(self.baseurl+suffix_url, headers=headers,
            data=data)
        req.get_method = lambda: 'DELETE'
        resp = urllib2.urlopen(req)
        page = resp.read()
        code = resp.getcode()
        logging.debug('code:%s, page:%s' % (code, page))
        return code, page
