from Utils.pgConnector import destinationPgConnector
from Model.Metric import Metric
from Utils import configParser
from Logger import log
import time
from datetime import date, datetime, timedelta


class nginxlogsService(object):
  logger = log.get_logger("nginxlogsService")

  @classmethod
  def getApiRequests(self):
    pgConn = destinationPgConnector()
    metrics_names = ["token", "authorize",
                     "userinfo", "devicecode", "introspect"]
    metrics_results = []
    api_requests = 0
    for metric in metrics_names:
      # Get the last date we process data
      lastMetric = Metric.getLastDateForMetric(metric)
      # Initialize whereClause
      whereClause = ''
      # Check if we have already stored metrics
      if lastMetric:
        dayFrom = lastMetric[0][0]
        previousValue = lastMetric[0][1]
        whereClause = " AND created > '{0}'".format(dayFrom)
      else:
        previousValue = 0
      # Get the date of the last log processed
      lastDate = pgConn.execute_select("SELECT max(created) FROM syslogs")
      
      if lastDate[0][0]!=None:
        lastDate = lastDate[0][0]
      else:
        lastDate = datetime.now()

      # Get the new metrics
      metrics_value = pgConn.execute_select(
          "SELECT count(*) FROM syslogs WHERE log_message LIKE '%/oidc/{0}%' AND service='nginx' {1}".format(metric, whereClause))
      metrics_results.append(Metric(
          None, metric, metrics_value[0][0] + previousValue, lastDate))
      # Add metrics to total api requests
      api_requests += metrics_value[0][0] + previousValue

    self.logger.info("{0} total api requests".format(api_requests))
    metrics_results.append(
        Metric(None, "api_requests", api_requests, lastDate))
    pgConn.close()
    # Save all metrics to database
    Metric.saveAll(metrics_results)
    return api_requests
