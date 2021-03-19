from Utils.pgConnector import comanagePgConnector
from Utils import configParser

class comanageService(object):
  @classmethod
  def getRegisteredUsers(self):
    pgConn = comanagePgConnector()
    result = pgConn.execute_select("SELECT count(*) AS total FROM cm_co_people WHERE co_person_id IS NULL AND NOT deleted AND status='A'")
    pgConn.close()
    return result[0][0]