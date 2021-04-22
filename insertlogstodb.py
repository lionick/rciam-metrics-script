from Utils.pgConnector import destinationPgConnector
import subprocess
import signal
import datetime
from datetime import date
import sys

# Insert Nginx Logs from files 
# dateFrom: store logs with equal or bigger datetime than dateFrom
# dateTo: store logs with smaller datetime than dateTo
# creationLogFileDate: get log files with creation date bigger or equal than creationLogFileDate
pgConn = destinationPgConnector()

if(len(sys.argv) != 4):
  sys.exit("You must have exactly 3 arguments \n - date_from: 01/Jan/2021 00:00:00 +0000 \n - date_to: 02/Jan/2021 01:00:00 +0000 \n - file_creation_date: 01/01/2021 0:00:00")

date_time_from = datetime.datetime.strptime(
    sys.argv[1], '%d/%b/%Y %H:%M:%S  %z')
date_time_to = datetime.datetime.strptime(sys.argv[2], '%d/%b/%Y %H:%M:%S  %z')
file_creation_date = sys.argv[3]  # 01/01/2021 0:00:00

# for gzip
output = subprocess.check_output("find ./nginx-logs -name 'access.*' -name '*.gz' -type f -newermt '%s' -exec zcat {}  \;" % file_creation_date, shell=True,
                                 preexec_fn=lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL))
lines = [x.decode('utf8').strip() for x in output.splitlines()]

output = subprocess.check_output("find ./nginx-logs -name 'access.log' -not -name '*.gz' -type f -newermt '%s' -exec cat {}  \;" % file_creation_date, shell=True,
                                 preexec_fn=lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL))
lines += [x.decode('utf8').strip() for x in output.splitlines()]
for line in lines:
  log_message = line[line.find("nginx")+6:]
  unformatted_datetime = line[line.find("[")+1:line.find("]")]
  unformatted_date = unformatted_datetime.replace(':', ' ', 1)
  date_time_obj = datetime.datetime.strptime(
      unformatted_date, '%d/%b/%Y %H:%M:%S %z')
  if(date_time_obj >= date_time_from and date_time_obj < date_time_to):
    pgConn.execute_insert("INSERT INTO syslogs(service, log_message, created) VALUES('nginx', %s, %s) ON CONFLICT DO NOTHING", [log_message, date_time_obj])
