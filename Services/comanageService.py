from Utils.pgConnector import comanagePgConnector
from Utils import configParser
from Logger import log
from Model import Metric
import time
from datetime import date, datetime, timedelta


class comanageService(object):
  logger = log.get_logger("comanageService")

  @classmethod
  def getRegisteredUsers(self):
    pgConn = comanagePgConnector()
    result = pgConn.execute_select(
        "SELECT count(*) AS total FROM cm_co_people WHERE co_person_id IS NULL AND NOT deleted AND status='A'")
    pgConn.close()
    timestamp = int(time.time())
    Metric.save(Metric(None, "registerd_users",
                result[0][0], datetime.fromtimestamp(timestamp)))
    self.logger.info("{0} total registered users".format(result[0][0]))
    return result[0][0]
