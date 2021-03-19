from Utils.pgConnector import proxystatisticsPgConnector
from Utils import configParser

class proxystatisticsService(object):
  @classmethod
  def getUsersLogins(self):
    pgConn = proxystatisticsPgConnector()
    result = pgConn.execute_select("SELECT sum(count) AS total FROM statistics")
    pgConn.close()
    return result[0][0]