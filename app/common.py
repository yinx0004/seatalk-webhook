from dateutil import parser, tz
import json
import logging
import os


log = logging.getLogger(__name__)


def prom_object_to_str(alist):
    result = ""
    for e in alist:
        pair = "\t%s = %s \n" % (e[0], e[1])
        result += pair
    return result.rstrip()


def convert_sgt(datetime_str):
    if datetime_str is None:
        return ""
    to_zone = tz.gettz('Asia/Singapore')
    dt = parser.parse(datetime_str)
    dt_sgt = dt.astimezone(to_zone)
    return dt_sgt.strftime("%Y-%m-%dT%H:%M:%S %z")


def get_contact(agent):
    try:
        log.debug("get agent: %s" % agent)
        agents_contact = json.loads(os.getenv('agents'))
        log.debug("agent contact: %s " % agents_contact)
        mobile = agents_contact[agent]['mobile']
        email = agents_contact[agent]['email']
        log.debug("%s mobile is %s, email is %s" % (agent, mobile, email))
    except Exception as e:
        log.error(e)
    return mobile, email


class Result(dict):
    def __int__(self, data=None, error=None, code=-1, message=None):
        self['data'] = data
        self['error'] = error
        self['code'] = code
        self['msg'] = message
