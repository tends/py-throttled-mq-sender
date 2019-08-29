import datetime
from time import strftime, gmtime

import xmltodict


class XmlDoc(object):
    # xml_dict = ""
    def __init__(self, file):
        with open(file) as fd:
            self.xml_dict = xmltodict.parse(fd.read())

        self.event_id = int(self.xml_dict['tradeEvent']['eventIdentifier']['eventId'])
        _tradeId = self.xml_dict['tradeEvent']['trade']['tradeIdentifier']['tradeId'].split(':')
        self.trade_id_prefix = _tradeId[0]
        self.trade_id_num = int(_tradeId[1])

    def get_trade_id(self):
        return "{0}:{1}".format(self.trade_id_prefix, self.trade_id_num)

    # def increment_numbers(self):

    def get_doc(self):
        self.event_id = self.event_id + 1
        self.trade_id_num = self.trade_id_num + 1

        _now = datetime.now()
        _now_plus_2d = _now + datetime.timedelta(days=2)

        # TODO: strftime("%Y-%m-%dT%H:%M:%S", gmtime())


        return xmltodict.unparse(self.xml_dict)
