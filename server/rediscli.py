import time
import ast

import redis

from server.config import conf
from server.utils import logger



ADDR = conf.redis_ip


def set_data(addr, data):
    logger.debug('redis set_data, addr:{}, data:{}'.format(addr, data))
    r = redis.Redis(host=ADDR)
    r.set(addr, data)
    #r.publish(addr, data)



def get_data(addr):
    logger.debug('redis get_data, addr:{}'.format(addr))
    r = redis.Redis(host=ADDR)
    # pipe = r.pipeline()
    # pipe.get(addr)
    # pipe.execute()
    data = r.get(addr).decode('utf-8')
    logger.debug('redis get_data, data:{}, type:{}'.format(data, type(data)))
    return data



def tst():
    #pool = redis.ConnectionPool(host='some-redis', port=6379)
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    p = r.pubsub()
    p.subscribe('first-channel')
    p.psubscribe('fir*')

    r.publish('first-channel', 'thedata')

    print('the message:{}'.format(p.get_message()))


def test_sche():
    da = get_data('p001/20141014')
    print(da)
    print(type(da))
    # if da isinstance(None):
    #     print('is None')
    if not da:
        print('not da')
    setdata = """
    {
        '1300':'1',
        '1400':'0'
    }"""

    set_data('p001/20141012', setdata)
    da1 = get_data('p001/20141012')
    da1decode = da1.decode('utf-8').strip(' \n')

    da1_ast = ast.literal_eval(da1decode)

# set_data('d001/2015/p001', 'illness2')
# time.sleep(1)
# print('the data: {}'.format(get_data('d001/2015/p001')))

# test_sche()
