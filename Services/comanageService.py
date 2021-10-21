from Utils.pgConnector import comanagePgConnector
from Utils import configParser
from Logger import log
from Model.Metric import Metric
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
    Metric.save(Metric(None, "registered_users",
                result[0][0], datetime.fromtimestamp(timestamp)))
    self.logger.info("{0} total registered users".format(result[0][0]))
    return result[0][0]

  @classmethod
  def getUsersMembershipsInCOUs(self):
    pgConn = comanagePgConnector()
    # check if section 'metric_users_memberships_in_cous' exists in configuration file and name attribute is not empty
    if configParser.hasSection('metric_users_memberships_in_cous') == False or not 'name' in configParser.getConfig('metric_users_memberships_in_cous').keys() or \
      configParser.getConfig('metric_users_memberships_in_cous')['name'] == '':
      return None
    metric_name = configParser.getConfig('metric_users_memberships_in_cous')['name']
    coSubQuery = ''
    subCouSubQuery = ''
    # if 'co_id' attribute exists and is not empty
    if 'co_id' in configParser.getConfig('metric_users_memberships_in_cous').keys() and \
      configParser.getConfig('metric_users_memberships_in_cous')['co_id']!='':
      coSubQuery = ' AND "CoPeople"."co_id"=' +  configParser.getConfig('metric_users_memberships_in_cous')['co_id']
    
    # if 'regex_cou_name' attribute exists and is not empty
    if 'regex_cou_name' in configParser.getConfig('metric_users_memberships_in_cous').keys() and \
      configParser.getConfig('metric_users_memberships_in_cous')['regex_cou_name']!='':
      subCouSubQuery = ' "Cous"."name" ~ \'' + configParser.getConfig('metric_users_memberships_in_cous')['regex_cou_name'] + '\' AND '
      
    result = pgConn.execute_select('SELECT count("CoPersonRole"."co_person_id") AS "CoPersonRole__co_person_id" \
                                    FROM "public"."cm_co_person_roles" AS "CoPersonRole" \
                                    INNER JOIN "public"."cm_co_people" AS "CoPeople" \
                                    ON("CoPeople"."id"="CoPersonRole"."co_person_id" AND "CoPeople"."co_person_id" IS NULL AND \
                                        "CoPeople"."status"=\'A\' AND "CoPeople"."deleted" IS NOT true ' + coSubQuery + ') \
                                    INNER JOIN "public"."cm_cous" AS "Cous" \
                                    ON("Cous"."id"="CoPersonRole"."cou_id" AND "Cous"."cou_id" IS NULL \
                                        AND "Cous"."deleted" IS NOT true) \
                                    WHERE '+ subCouSubQuery + '\
                                    ("CoPersonRole".status=\'A\' OR "CoPersonRole".status=\'GP\') \
                                    AND "CoPersonRole"."co_person_role_id" IS NULL \
                                    AND "CoPersonRole"."deleted" IS NOT true \
                                    ')
    timestamp = int(time.time())
    pgConn.close()
    Metric.save(Metric(None, metric_name,
                result[0][0], datetime.fromtimestamp(timestamp)))
    self.logger.info("{0} user's memberships in cous".format(result[0][0]))
    return result[0][0]
