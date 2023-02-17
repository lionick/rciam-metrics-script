from Utils.pgConnector import destinationPgConnector
from Utils import configParser
class Log(object):
  LOGSTABLE = "syslogs"

  def __init__(self, id, log_message, service, created):
    self.id = id
    self.log_message = log_message
    self.service = service
    self.created = created
  
  def deleteOldLogs(days):
    if(days.isnumeric()):
      pgConn = destinationPgConnector()  
      pgConn.execute_and_commit(
       "DELETE FROM {0} WHERE created < (CURRENT_DATE - INTERVAL '{1}' DAY)".format(Log.LOGSTABLE, days)
      )
      pgConn.close()