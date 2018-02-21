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

def t_exception(exception):
    error, = exception.args
    t_log('Error code - %s' %error.code)
    t_log('Error Message - %s' %error.message)


class Statsretreiver:
    def __init__(self,username,password,database):
        self.username = username
        self.password = password
        self.database = database
        self.dbquery = "select name, value from v$sysstat where name in ('physical write total bytes','physical read total bytes','execute count','db block changes','CPU used by this session','redo size', 'bytes sent via SQL*Net to client', 'bytes received via SQL*Net from client', 'SQL*Net roundtrips to/from client')"

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

class Writerproc_network:
    '''
    Class to generate network load. A use case where app server is in AWS or Google Cloud and DB in Oracle Cloud
    Purpose of this class is to measure the network latency / performance
    when App Server and DB are not in two different cloud
    '''
    def __init__(self, threadname, username, password, database):
        self.threadname = threadname
        self.username = username
        self.password = password
        self.database = database
        self.transize = 100000

    def execproc(self):
        t_log('Thread| Writer %s executing ' %self.threadname)
        try:
            conn = cx_Oracle.connect(self.username, self.password, self.database)
            curr = conn.cursor()
        except cx_Oracle.DatabaseError, exception:
            t_log('Thread| Writer %s Failed to Connect to DB' % self.threadname)
            t_exception(exception)
            exit(1)

        # Loop over number of transize
        for i in range(self.transize):

        # SQL to get Merchant Name - single value

            query_string = 'SELECT MERCHANT_NAME FROM MERCHANTS WHERE MERCHANT_ID = floor(dbms_random.value(1, 100))'
            try:
                curr.execute(query_string)
            except cx_Oracle.DatabaseError, exception:
                t_log('Thread| Writer %s Error in executing query' % self.threadname)
                t_exception(exception)
                exit(1)
            lv_merchant_name = curr.fetchone ()[0]
            #t_log('Thread| Writer %s: Merchant Name - %s' % (self.threadname,lv_merchant_name) )

        # SQL to get Buyer Info - Dictionary
            query_string = 'SELECT first_name,last_name,company_name,address ,city,county,postal,phone1,phone2,email,web FROM BUYER WHERE buyer_id = floor(dbms_random.value(1,500))'
            try:
                curr.execute(query_string)
            except cx_Oracle.DatabaseError, exception:
                t_log('Thread| Writer %s Error in executing query' % self.threadname)
                t_exception(exception)
                exit(1)
            resultset = curr.fetchone()
            lv_first_name = resultset[0]
            lv_last_name  = resultset[1]
            lv_company_name = resultset[2]
            lv_address = resultset[3]
            lv_city = resultset[4]
            lv_county = resultset[5]
            lv_postal = resultset[6]
            lv_phone1 = resultset[7]
            lv_phone2 = resultset[8]
            lv_email = resultset[9]
            lv_web = resultset[10]

            #t_log('Thread| Writer %s: First Name - %s' % (self.threadname, lv_first_name))
            #t_log('Thread| Writer %s: Last Name - %s' % (self.threadname, lv_last_name))
            #t_log('Thread| Writer %s: Web - %s' % (self.threadname, lv_web))

        # Insert into Transaction_No_Comp Table
        # Build keys using dbms_random
            query_string = ( 'SELECT DBMS_RANDOM.STRING(:X,30), floor(dbms_random.value(1,10000)), '
                             'floor(dbms_random.value(1,1000)), floor(dbms_random.value(1,100)) '
                             'FROM DUAL' )
            try:
                curr.execute(query_string, X='X')
            except cx_Oracle.DatabaseError, exception:
                t_log('Thread| Writer %s Error in executing query' % self.threadname)
                t_exception(exception)
                exit(1)
            resultset = curr.fetchone()
            lv_tran_id = resultset[0]
            lv_prd_id  = resultset[1]
            lv_qty     = resultset[2]
            lv_unit_price = resultset[3]


            insert_string = ('INSERT INTO TRANSACTION_NO_COMP ( '
                             'tran_id , merchant_name ,buyer_first_name ,buyer_last_name, '
                             'buyer_company_name ,buyer_address ,buyer_city,buyer_county, '
                             'buyer_postal,buyer_phone1,buyer_phone2,buyer_email,buyer_web,prd_id ,qty ,unit_price '
                             ') Values (:tran_id, :merchant_name, :buyer_first_name, :buyer_last_name, '
                             ':buyer_company_name, :buyer_address, :buyer_city, :buyer_county, '
                             ':buyer_postal, :buyer_phone1, :buyer_phone2, :buyer_email, :buyer_web, '
                             ':prd_id, :qty, :unit_price )')
            try:
                curr.execute(insert_string, tran_id=lv_tran_id, merchant_name=lv_merchant_name,
                             buyer_first_name=lv_first_name, buyer_last_name=lv_last_name, buyer_company_name=lv_company_name,
                             buyer_address=lv_address, buyer_city=lv_city, buyer_county=lv_county, buyer_postal=lv_postal,
                             buyer_phone1=lv_phone1, buyer_phone2=lv_phone2, buyer_email=lv_email, buyer_web=lv_web,
                             prd_id=lv_prd_id, qty=lv_qty, unit_price=lv_unit_price)
            except cx_Oracle.DatabaseError, exception:
                t_log('Thread| Writer %s Error in executing query' % self.threadname)
                t_exception(exception)
                exit(1)

        # End Loop

        curr.close()
        conn.commit()
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

def runWriterProc_network(threadname, username, password, database, test_duration):
    t_log('Thread| %s starting ' % threadname)
    w1 = Writerproc_network(threadname, username, password, database)
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





