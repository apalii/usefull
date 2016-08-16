#!/usr/bin/env python3

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

import socket
import random
import time
import sys
import datetime

from calendar import monthrange


def rand_date():
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    last_day = monthrange(year, month)[1]
    start = datetime.datetime(year, month, 1)
    end = datetime.datetime(year, month, last_day)
    return random.randrange(int(start.strftime("%s")), int(end.strftime("%s")))


def rand_plugin():
    return random.randrange(7001, 7100)


def rand_ip():
    return "192.168.87.{}".format(random.randrange(2, 253))


class LogFiller(object):
    """Class imitates the server behaviour and
     sends lines to the logstash TCP listener
     """

    def __init__(self, lines=1000, ip='192.168.87.191', port=5142, test_mode=False):
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
        self.test_mode = test_mode

    def create_tcp_connection_and_send(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect(self.host)
        except socket.timeout as err:
            sock.shutdown(socket.SHUT_RD)
            sys.exit("There is connection problem : {}".format(err))

        for i in xrange(1, self.number_of_lines + 1):
            if self.test_mode:
                sock.shutdown(socket.SHUT_RD)
                print self.generate_line()
            else:
                sock.send(self.generate_line())
        sock.shutdown(socket.SHUT_RD)

    @staticmethod
    def generate_line():
        data_field = """data='AV - Alert - "1470314952" --> RID: "5502"; RL: "3"; RG: "pam,syslog,"; RC: "Login session closed."; USER: "None"; SRCIP: "None"; HOSTNAME: "VirtualUSMAllInOne"; LOCATION: "/var/log/auth.log"; EVENT: "[INIT]Aug  4 08:49:11 VirtualUSMAllInOne sudo: pam_unix(sudo:session): session closed for user root[END]"; '"""
        line = "<entry id='2882' v='2' fdate='2016-08-04 12:49:12' date='{1}' plugin_id='{2}' " \
               "sensor='192.168.87.191' src_ip='{3}' dst_ip='{3}' src_port='0' dst_port='0' " \
               "tzone='-4.00' datalen='307' data='{0}' plugin_sid='5502' proto='6'  " \
               "ctx='cad377ce-4772-11e6-a4c1-000c296a1093' " \
               "src_host='cb973a55-4772-11e6-a4c1-000c296a1093' dst_host='cb973a55-4772-11e6-a4c1-000c296a1093' " \
               "src_net='cad87427-4772-11e6-a4c1-000c296a1093' dst_net='cad87427-4772-11e6-a4c1-000c296a1093' " \
               "username='root' userdata1='/var/log/auth.log' userdata2='Login session closed.' " \
               "userdata3='pam,syslog,' userdata4='none' idm_host_src='VirtualUSMAllInOne' " \
               "idm_host_dst='VirtualUSMAllInOne' idm_mac_src='00:0C:29:6A:10:93' idm_mac_dst='00:0C:29:6A:10:93' " \
               "device='192.168.87.191'/>".format(
            data_field, rand_date(), rand_plugin(), rand_ip()
        )

        return line

test = LogFiller(lines=10, test_mode=True)
test.create_tcp_connection_and_send()