#!/usr/bin/env python

import logging, cx_Oracle, threading, time

def t_logsetting(logfile, loglevel):

    logging.basicConfig(level=loglevel,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=logfile,
                        filemode='a')

def t_log(logmessage):
    logging.info(logmessage)

class Statsretreiver:
    def __init__(self,username,password,database):
        self.username = username
        self.password = password
        self.database = database
        self.dbquery = "select name, value from v$sysstat where name in ('physical write total bytes','physical read total bytes','execute count','db block changes','CPU used by this session','redo size')"

    def getStats(self):
        conn = cx_Oracle.connect(self.username,self.password,self.database)
        curr = conn.cursor()
        curr.execute(self.dbquery)
        res = dict(curr.fetchall())
        curr.callproc("DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT")
        curr.close()
        conn.close()
        return res

class Writerproc:
    def __init__(self, threadname, username, password, database):
        self.threadname = threadname
        self.username = username
        self.password = password
        self.database = database
        self.writerproc = "load_no_comp"
        self.transize = 100000

    def execproc(self):
        t_log('Thread| Writer %s executing ' %self.threadname)
        conn = cx_Oracle.connect(self.username, self.password, self.database)
        curr = conn.cursor()
        curr.callproc(self.writerproc,[self.transize])
        curr.close()
        conn.close()
        t_log('Thread| %s DB Writer Proc completed ' %self.threadname)

class Readerproc:
    def __init__(self, threadname, username, password, database):
        self.threadname = threadname
        self.username = username
        self.password = password
        self.database = database
        self.readerquery = "select merchant_name, sum(qty*unit_price) from transaction_no_comp where upper(substr(merchant_name,1,1)) = (Select dbms_random.string('U',1) from dual) group by merchant_name"

    def execproc(self):
        t_log('Thread| Reader %s executing ' %self.threadname)
        conn = cx_Oracle.connect(self.username, self.password, self.database)
        curr = conn.cursor()
        curr.execute(self.readerquery)
        res = dict(curr.fetchall())
        curr.close()
        conn.close()
        t_log('Thread| %s DB Reader Proc completed ' %self.threadname)

def runWriterProc(threadname, username, password, database, test_duration):
    t_log('Thread| %s starting ' % threadname)
    w1 = Writerproc(threadname, username, password, database)
    t_end = time.time() + 60 * test_duration
    while time.time() < t_end:
        w1.execproc()
    return

def runReaderProc(threadname, username, password, database, test_duration):
    t_log('Thread| Reader %s starting ' % threadname)
    r1 = Readerproc(threadname, username, password, database)
    t_end = time.time() + 60 * test_duration
    while time.time() < t_end:
        r1.execproc()
    return

if __name__ == "__main__":
    l_logfile = '/tmp/pythontest.log'
    l_loglevel = logging.INFO

    t_logsetting(l_logfile, l_loglevel)

    t_log('A DEBUG MESSAGE')
    username = 'bipul'
    password = getpass.getpass('password: ')
    database = 'DEMODB01_LOCAL'
    test_duration = 1

    obj1 = Statsretreiver(username,password,database)
    print obj1.getStats()

    threads = []
    numth = 5
    for i in range(numth):
        threadname = 'Thread ' + str(i)
        t = threading.Thread(target=runWriterProc, args=(threadname, username, password, database, test_duration))
        threads.append(t)
        t.start()
    t.join()

    obj2 = Statsretreiver(username,password,database)
    print obj2.getStats()





