#!/usr/bin/env python3

try :
    from urllib.request import urlopen
except:
    from urllib2 import urlopen
import sys
import json
from time import sleep, ctime

class Watcher(object):
    '''
    vk watcher class 
    python 2 and 3 compatible
    json response example :
    {"response":[{"uid":1,"first_name":"Pavel","last_name":"Durov","online":0,"last_seen":{"time":1398447188,"platform":7}}]}
    '''
    def __init__(self, vk_id, timeout=10, reps=5):
        self.vk_id = vk_id
        self.timeout = timeout 
        self.reps = reps
        self.url = 'https://api.vk.com/method/users.get?user_ids=' + \
                    self.vk_id + '&fields=online,last_seen&lang=en'

    def watch(self):
        '''watch method'''
        while self.reps !=0:
            self.reps -= 1
            page = urlopen(self.url)
            data = json.load(page)
            if 'error' in data:
                sys.exit("\nIt seems that such id as :", self.vk_id, " doesn't exist!")
            for i in data['response']:
                if 'deactivated' in i:
                    sys.exit("\nIt seems that such id as :" + self.vk_id + " has been deleted")
                elif i['online'] == 1:
                    print(i['first_name'],i['last_name'] + '\tis ONLiNE\n')
                else:
                    print('{} {}\t{}'.format(i['first_name'],i['last_name'], Watcher.devtime(data)))
            sleep(self.timeout)
        print('finished')


    @staticmethod
    def devtime(response):
        dev = 'pc' if response['response'][0]['last_seen']['platform'] == 7 else 'mob'
        time =  ctime(response['response'][0]['last_seen']['time'])
        return 'last seen: {} | device: {}'.format(time, dev)

if __name__ == "__main__":

    mywatcher = Watcher('durov',5,2).watch()
