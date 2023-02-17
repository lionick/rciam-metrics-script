#!/usr/local/bin/python3
import os
import sys
# change working directory
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

from Services.comanageService import comanageService
from Services.proxystatisticsService import proxystatisticsService
from Services.nginxlogsService import nginxlogsService
import time
#Delete Logs if the relative option is set up
nginxlogsService.deleteOldLogs()

users = comanageService.getRegisteredUsers()
registeredUsersMetric = "aai_registered_users_total {0}".format(users)
logins = proxystatisticsService.getUsersLogins()
totalLoginsMetric = "aai_logins_total {0}".format(logins)
api_requests = nginxlogsService.getApiRequests()
totalApiRequestsMetric = "aai_api_requests_total {0}".format(api_requests)
lastTimeChanged = "aai_last_metrics_updater_run_timestamp_seconds {0}".format(int(time.time()))
f = open("metrics.txt", "w")
f.write("# TYPE aai_registered_users_total gauge\n")
f.write("{0}\n".format(registeredUsersMetric))
f.write("# TYPE aai_logins_total counter\n")
f.write("{0}\n".format(totalLoginsMetric))
f.write("# TYPE aai_api_requests_total counter\n")
f.write("{0}\n".format(totalApiRequestsMetric))
users_memberships_in_cous = comanageService.getUsersMembershipsInCOUs()
if users_memberships_in_cous != None:
  activeConnectSubscriptions = "aai_active_connect_subscriptions {0}".format(users_memberships_in_cous)
  f.write("{0}\n".format(activeConnectSubscriptions))
f.write("{0}\n".format(lastTimeChanged))
f.close()
