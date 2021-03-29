from Services.comanageService import comanageService
from Services.proxystatisticsService import proxystatisticsService
import time

users = comanageService.getRegisteredUsers()
registeredUsersMetric = "aai_registered_users_total {0} {1}".format(users, int(time.time()))
logins = proxystatisticsService.getUsersLogins()
totalLoginsMetric = "aai_logins_total {0} {1}".format(logins, int(time.time()))
f = open("aai_metrics.txt", "w")
f.write("# TYPE aai_registered_users_total gauge\n")
f.write("{0}\n".format(registeredUsersMetric))
f.write("# TYPE aai_logins_total counter\n")
f.write("{0}\n".format(totalLoginsMetric))
f.write("# TYPE aai_api_requests_total counter\n")
f.write("{0}\n".format(totalLoginsMetric))
f.close()
