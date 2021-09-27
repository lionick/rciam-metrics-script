from Utils.pgConnector import destinationPgConnector
from Utils import configParser
class Metric(object):
  METRICSTABLE = "aai_metrics"

  def __init__(self, id, metric_name, metric_value, created):
    self.id = id
    self.metric_name = metric_name
    self.metric_value = metric_value
    self.created = created

  @classmethod
  def getLastDateForMetric(self, metric_name):
    pgConn = destinationPgConnector()
    result = pgConn.execute_select("SELECT created, metric_value FROM {0} WHERE created IN (SELECT max(created) FROM {0} WHERE metric_name='{1}') AND metric_name='{1}'".format(Metric.METRICSTABLE, metric_name))
    return result

  @classmethod
  def save(self, metrics):
    pgConn = destinationPgConnector()  
    pgConn.execute_and_commit(
      "INSERT INTO {0}(metric_name, metric_value, created) VALUES ('{1}', '{2}', '{3}')".format(Metric.METRICSTABLE, metrics.metric_name, metrics.metric_value, metrics.created)
    )
    pgConn.close()
  
  @classmethod
  def saveAll(self, metricsList):
    pgConn = destinationPgConnector()
    values = ''
    for item in metricsList:
      values += "INSERT INTO {0}(metric_name, metric_value, created) VALUES ('{1}', '{2}', '{3}');".format(Metric.METRICSTABLE, item.metric_name, item.metric_value, item.created)
    pgConn.execute_and_commit(values)
    pgConn.close()