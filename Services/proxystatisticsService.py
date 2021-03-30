from Utils.pgConnector import proxystatisticsPgConnector
from Utils import configParser
from Model import Metric
from Logger import log
import time
from datetime import date, datetime, timedelta


class proxystatisticsService(object):
  logger = log.get_logger("proxystatisticsService")

  @classmethod
  def getUsersLogins(self):
    pgConn = proxystatisticsPgConnector()
    result = pgConn.execute_select(
        "SELECT sum(count) AS total FROM statistics")
    pgConn.close()
    timestamp = int(time.time())
    Metric.save(
        Metric(None, "logins", result[0][0], datetime.fromtimestamp(timestamp)))
    self.logger.info("{0} total logins".format(result[0][0]))
    return result[0][0]
