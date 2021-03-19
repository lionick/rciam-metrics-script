from Services.comanageService import comanageService
from Services.proxystatisticsService import proxystatisticsService
import time

users = comanageService.getRegisteredUsers()
registeredUsersMetric = "aai_registered_users_total {0} {1}".format(users, time.time())
logins = proxystatisticsService.getUsersLogins()
totalLoginsMetric = "aai_logins_total {0} {1}".format(logins, time.time())
f = open("aai_stats.txt", "w")
f.write("{0}\n".format(registeredUsersMetric))
f.write("{0}\n".format(totalLoginsMetric))
f.close()
