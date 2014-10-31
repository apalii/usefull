#!/usr/bin/env python
# May be imported.

import urllib2 as u
import sys
import json as j


def timeh(x):
    ''' Convert UNIX time to human-readable :)'''
    from time import ctime
    return ctime(x)


def output(x):
    """Print the string of symbols '-' eq to input data len"""
    line = '-' * len(x)
    out = line + '\n' + x + '\n' + line
    return out


def online(id):
    '''Checking status of the needed user via API, parsing, analyzing and print results'''
    root = 'https://api.vk.com/method/users.get?user_ids='
    ending = '&fields=online,last_seen&lang=en'
    url = root + id + ending
    page = u.urlopen(url)
    data = j.load(page)
    if 'error' in data:
        print "\nIt seems that such id as :\n\n", output(id), "\n\ndoesn't exist, type a valid id !"
        sys.exit()
    for i in data['response']:
        if 'deactivated' in i:
            print "\nIt seems that such id as :\n\n", output(id), "\n\nhas been deleted, type a valid id !"
            sys.exit()
        elif i['online'] == 1:
            print i['first_name'], i['last_name'], '\tis ONLiNE\n'
        else:
            print i['first_name'], i['last_name'], '\tis OFFLiNE\tLast_seen :', timeh(i['last_seen']['time'])

if __name__ == "__main__":
    online(sys.argv[1])
