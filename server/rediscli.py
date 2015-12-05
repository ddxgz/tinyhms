import time
from server.config import conf

import redis


ADDR = conf.redis_ip


def set_data(addr, data):
    r = redis.Redis(host=ADDR)
    r.set(addr, data)
    #r.publish(addr, data)



def get_data(addr):
    r = redis.Redis(host=ADDR)
    # pipe = r.pipeline()
    # pipe.get(addr)
    # pipe.execute()
    return r.get(addr)



def tst():
    #pool = redis.ConnectionPool(host='some-redis', port=6379)
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    p = r.pubsub()
    p.subscribe('first-channel')
    p.psubscribe('fir*')

    r.publish('first-channel', 'thedata')

    print('the message:{}'.format(p.get_message()))


# set_data('d001/2015/p001', 'illness2')
# time.sleep(1)
# print('the data: {}'.format(get_data('d001/2015/p001')))

#tst()