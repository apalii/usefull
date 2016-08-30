#!/usr/bin/env python

"""
Log line example :
<entry id='2874' v='2' fdate='2016-08-04 12:49:12' date='1470314952' plugin_id='7009'
sensor='192.168.87.191' src_ip='192.168.87.191' dst_ip='192.168.87.191' src_port='0'
dst_port='0' tzone='-4.00' datalen='346'
data='AV - Alert - "1470314952" --> RID: "5501"; RL: "3"; RG: "pam,syslog,authentication_success,"; RC: "Login session opened."; USER: "None"; SRCIP: "None"; HOSTNAME: "VirtualUSMAllInOne"; LOCATION: "/var/log/auth.log"; EVENT: "[INIT]Aug  4 08:49:11 VirtualUSMAllInOne sudo: pam_unix(sudo:session): session opened for user root by avapi(uid=0)[END]"; '
plugin_sid='5501' proto='6'  ctx='cad377ce-4772-11e6-a4c1-000c296a1093'
src_host='cb973a55-4772-11e6-a4c1-000c296a1093'
dst_host='cb973a55-4772-11e6-a4c1-000c296a1093'
src_net='cad87427-4772-11e6-a4c1-000c296a1093'
dst_net='cad87427-4772-11e6-a4c1-000c296a1093' username='root' userdata1='/var/log/auth.log'
userdata2='Login session opened.' userdata3='pam,syslog,authentication_success,' userdata4='none'
idm_host_src='VirtualUSMAllInOne' idm_host_dst='VirtualUSMAllInOne' idm_mac_src='00:0C:29:6A:10:93'
idm_mac_dst='00:0C:29:6A:10:93' device='192.168.87.191'/>
"""

import time
import datetime
import sys
import socket
import random
import redis

from calendar import monthrange

now = datetime.datetime.now()
month = now.month
year = now.year
last_day = monthrange(year, month)[1]
start = datetime.datetime(year, month, 1)
end = datetime.datetime(year, month, last_day)
start, end = int(start.strftime("%s")), int(end.strftime("%s"))


def rand_date():
    """
    Returns random date(within current month) in unix time
    :return: int
    """
    return random.randrange(start, end)


def rand_plugin():
    return random.randrange(7001, 7050)


class LogFiller(object):
    """Class imitates the server behaviour and
     sends lines to the logstash TCP listener
     """

    def __init__(self, lines=1000, ip='192.168.87.191', port=5142, debug=False):
        """
        Logstash config example :
        # cat /etc/logstash/conf.d/01-beaver_test.conf
        input {
          tcp {
            host => '192.168.87.191'
            port => '5142'
          }
        }
        """
        self.number_of_lines = lines
        self.ip = ip
        self.port = port
        self.host = (self.ip, self.port)
        self.debug = debug

    def through_mongodb_connection(self):
        pass

    def through_redis_connection(self):
        instance = redis.Redis()
        key = 'logstash:cache:test'
        for i in xrange(1, self.number_of_lines + 1):
            instance.lpush(key, self.generate_line())

    def through_tcp_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.host)
        except socket.timeout as err:
            sock.close()
            err_msg = "Please check iptables rules or logstash conf: {0}".format(err)
            sys.exit(err_msg)
        except socket.error as err:
            sock.close()
            err_msg = "Please check iptables rules: {0}".format(err)
            sys.exit(err_msg)
        counter = 0
        start = time.time()
        for i in xrange(1, self.number_of_lines + 1):
            counter += 1
            line_to_send = self.generate_line()
            if self.debug and counter % 500 == 0:
                print "{0} messages in {1} seconds".format(counter, time.time() - start)
                start = time.time()
            try:
                sock.sendall(line_to_send)
            except socket.error as err:
                print("Unable to send a msg : {0}".format(err))
            # time.sleep(0.01)
        print "\nTotal {0} seconds".format(start - time.time())
        sock.close()

    @staticmethod
    def generate_line():
        data_field = """AV - Alert - "1470314952" --> RID: "5502"; RL: "3"; RG: "pam,syslog,"; RC: "Login session closed."; USER: "None"; SRCIP: "None"; HOSTNAME: "VirtualUSMAllInOne"; LOCATION: "/var/log/auth.log"; EVENT: "[INIT]Aug  4 08:49:11 VirtualUSMAllInOne sudo: pam_unix(sudo:session): session closed for user root[END]";"""
        line = "<entry id='2882' v='2' fdate='2016-08-04 12:49:12' date='{1}' plugin_id='{2}' " \
               "sensor='192.168.87.191' src_ip='192.168.87.{3}' dst_ip='192.168.87.{3}' src_port='0' dst_port='0' " \
               "tzone='-4.00' datalen='307' data='{0}' plugin_sid='5502' proto='6'  " \
               "ctx='cad377ce-4772-11e6-a4c1-000c296a1093' " \
               "src_host='cb973a55-4772-11e6-a4c1-000c296a1093' dst_host='cb973a55-4772-11e6-a4c1-000c296a1093' " \
               "src_net='cad87427-4772-11e6-a4c1-000c296a1093' dst_net='cad87427-4772-11e6-a4c1-000c296a1093' " \
               "username='root' userdata1='/var/log/auth.log' userdata2='Login session closed.' " \
               "userdata3='pam,syslog,' userdata4='none' idm_host_src='VirtualUSMAllInOne' " \
               "idm_host_dst='VirtualUSMAllInOne' idm_mac_src='00:0C:29:6A:10:93' idm_mac_dst='00:0C:29:6A:10:93' " \
               "device='192.168.87.191'/>\n".format(data_field, rand_date(), rand_plugin(), random.randrange(2, 99))

        return line

test = LogFiller(lines=10000, ip='192.168.100.243', debug=True)
test.through_tcp_socket()
#test.through_redis_connection()
