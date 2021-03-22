from Services.comanageService import comanageService
from Services.proxystatisticsService import proxystatisticsService
import time

users = comanageService.getRegisteredUsers()
registeredUsersMetric = "aai_registered_users_total {0} {1}".format(users, int(time.tme()))
logins = proxystatisticsService.getUsersLogins()
totalLoginsMetric = "aai_logins_total {0} {1}".format(logins, int(time.time()))
f = open("aai_metrics.txt", "w")
f.write("{0}\n".format(registeredUsersMetric))
f.write("{0}\n".format(totalLoginsMetric))
f.close()
