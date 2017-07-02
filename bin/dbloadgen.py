#!/usr/bin/env python
''' Light weight toolkit to generate Database Load
    To be used for comparison of Oracle DB performance across two instances
    Developed and Tested using Oracle 12c
'''


import sys, os, argparse, getpass, time, logging, cx_Oracle, threading
sys.path.append('../lib')
import helper

parser = argparse.ArgumentParser()
parser.add_argument("-d", type=str, help="DB Service Name")
parser.add_argument("-i", type=str, help="IP Address of Database Server")
parser.add_argument("-p", type=str, help="Listener Port number for DB service")
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-s", type=str, default=None, help="password")
parser.add_argument("-w", type=int, default=2, help="number of write threads")
parser.add_argument("-r", type=int, default=2, help="number of read threads")
parser.add_argument("-l", type=str, help="logfile (fullpath)")
parser.add_argument("-t", type=int, default=1, help="elapsed time to run the test in minutes")
#parser.add_argument("-a", type=str, default='y', help="take awr snapshot")
#parser.add_argument("-n", type=str, help="generate network workload", nargs='?')
args = parser.parse_args()



username = args.u
db_service = args.d
db_ipaddr = args.i
db_listnerport = args.p
numth_write = args.w
numth_read = args.r
logfile = args.l
test_duration = args.t

# Get password
if args.s:
    password = args.s
else:
    password = getpass.getpass('password: ')

#gen_awr = args.a
#gen_network_load = args.n

# Set logging and print name of logfile to check
loglevel="INFO"
nloglevel =getattr(logging, loglevel, None)
helper.t_logsetting(logfile, nloglevel)
print ("\nMain: execution information in logfile %s " %logfile)
helper.t_log('\n')
helper.t_log('Thread| Main : Starting')
helper.t_log('Thread| Main : ' + 'DB Load Gen Arguments:')
helper.t_log('Thread| Main : ' + 'Num writer thread: %s' %numth_write)
helper.t_log('Thread| Main : ' + 'Num reader thread: %s' %numth_read)
helper.t_log('Thread| Main : ' + 'Test Run Duration (min): %s' %test_duration)

# Build dns for DB Connection

database = cx_Oracle.makedsn(db_ipaddr, db_listnerport, service_name = db_service)
# Collect pre load gen Stats

helper.t_log('Thread| Main : ' + 'Collect pre load statistics')
preloadstats = helper.Statsretreiver(username,password,database)
prestats =  preloadstats.getStats()

# Start Writer Threads

writerthreads = []

for i in range(numth_write):
    threadname = 'Thread ' + str(i)
    tw = threading.Thread(target=helper.runWriterProc, args=(threadname, username, password, database, test_duration))
    writerthreads.append(tw)
    tw.start()

# Start Reader Threads

readerthreads = []

for i in range(numth_read):
    threadname = 'Thread ' + str(i)
    tr = threading.Thread(target=helper.runReaderProc, args=(threadname, username, password, database, test_duration))
    readerthreads.append(tr)
    tr.start()

if numth_write > 0:
    tw.join()
if numth_read > 0:
    tr.join()

# Collect post load gen Stats

helper.t_log('Thread| Main : ' + 'Collect post load statistics')
postloadstats = helper.Statsretreiver(username,password,database)
poststats = postloadstats.getStats()

# Compare the Stats and print perf report

helper.t_log('Thread| Main : ' + 'Resource Consumption Summary \n')
for metric in prestats.keys():
    val = poststats[metric] - prestats[metric]
    helper.t_log('Thread| Main : %s : %i' %(metric,val))

helper.t_log('Thread| Main : Completed')
