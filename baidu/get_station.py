#encoding:utf-8
'''
    获取redis中line uid(key_3),于read_key作差集，将未读站点写文件并写入read_key
'''

import redis
import urllib2
import sys
import json
import time
reload(sys)
sys.setdefaultencoding('utf8')

r = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_station_key = 'py_new_bs_key_2'
redis_read_key = 'py_bs_read'      #存放已经获取过的redis key
redis_read_key_1 = 'py_bs_read_1' #存放已经获取过的uid
url = 'http://map.baidu.com/?qt=bsl&tps=&newmap=1&uid='


index_i = 0
# flag = False
# bus_line = {}#总线路字典
file = open('station.txt','a+')
while(True):
    has_read = r.sdiff(redis_station_key, redis_read_key)
    print has_read
    for item in has_read:
        #if index_i % 5 ==0 and index_i !=0:
         #   print "已读取%d条线路站点" % index_i

        uid_list = item.split('__')
        for uid in uid_list:
            tmp_info = []
            exp = uid.split('||')
            if r.sismember(redis_read_key_1, str(exp[1])):
                r.sadd(redis_read_key, item)
                continue
            print exp[0], exp[1]
            urls = '%s%s' % (url, '&c=%s&uid=%s' % (exp[0], exp[1]))
            req = urllib2.Request(url=urls)
            try:
                res = urllib2.urlopen(req, None, 2)
                data = json.loads(res.read())
                tmp_info.append(data['current_city']['up_province_name'])
                tmp_info.append(data['current_city']['name'])
                tmp_info.append(data['content'][0]['name'])
                for station in data['content'][0]['stations']:
                    tstr = station['name']
                    ex = station['geo'].split(';')[0].split('|')[1]
                    tmp_info.append(tstr + ':' + ex)

                file.write('\t'.join(tmp_info)+"\n")



            except Exception as e:
                print urls
                print "error: %s" % e

            r.sadd(redis_read_key, item)
            r.sadd(redis_read_key_1, exp[1])

            index_i += 1
            time.sleep(0.8)

    time.sleep(1)

file.close()
