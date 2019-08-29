import datetime
import xmltodict


class XmlDoc(object):
    def __init__(self, file):
        self.trade_id = ""

        with open(file) as fd:
            self.xml_dict = xmltodict.parse(fd.read())

        self.event_id = int(self.xml_dict['tradeEvent']['eventIdentifier']['eventId'])

        _tradeId = self.xml_dict['tradeEvent']['trade']['tradeIdentifier']['tradeId'].split(':')
        self.trade_id_prefix = _tradeId[0]
        self._trade_id_num = int(_tradeId[1])

    def get_msg(self):
        self._trade_id_num = self._trade_id_num + 1

        self.event_id = self.event_id + 1
        self.xml_dict['tradeEvent']['trade']['tradeIdentifier']['tradeId'] = \
            "{0}:{1}".format(self.trade_id_prefix, self._trade_id_num)
        _now = datetime.datetime.now()

        self.xml_dict['tradeEvent']['eventIdentifier']['eventDateTime'] = \
            self.xml_dict['tradeEvent']['trade']['tradeIdentifier']['tradeUpdateDateTime'] = \
            self.xml_dict['tradeEvent']['trade']['tradeDetails']['tradeDateTime'] = _now.strftime("%Y-%m-%dT%H:%M:%S")

        _now_plus_2d = _now + datetime.timedelta(days=2)
        self.xml_dict['tradeEvent']['trade']['tradeDetails']['equity']['settleDate'] = \
            self.xml_dict['tradeEvent']['trade']['tradeDetails']['equity']['cashSettleDate'] = \
            _now_plus_2d.strftime("%Y-%m-%d")

        return [self.event_id, xmltodict.unparse(self.xml_dict, pretty=True)]
