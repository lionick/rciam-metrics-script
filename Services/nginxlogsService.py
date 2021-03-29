from Utils.pgConnector import nginxLogsPgConnector
from Utils import configParser

class nginxlogsService(object):
  @classmethod
  def getApiRequests(self):
    # Get the last date we process data
    pgConn = nginxLogsPgConnector()
    token_metric = pgConn.execute_select("SELECT count(*) FROM access_log_z WHERE log_message LIKE '%/oidc/token%'")
    authorize_metric = pgConn.execute_select("SELECT count(*) FROM access_log_z WHERE log_message LIKE '%/oidc/authorize%'")
    userinfo_metric = pgConn.execute_select("SELECT count(*) FROM access_log_z WHERE log_message LIKE '%/oidc/userinfo%'")
    devicecode_metric = pgConn.execute_select("SELECT count(*) FROM access_log_z WHERE log_message LIKE '%/oidc/devicecode%'")
    introspect_metric = pgConn.execute_select("SELECT count(*) FROM access_log_z WHERE log_message LIKE '%/oidc/introspect%'")
    pgConn.close()
    return token_metric[0][0] + authorize_metric[0][0] + userinfo_metric[0][0] + devicecode_metric[0][0] + introspect_metric[0][0]