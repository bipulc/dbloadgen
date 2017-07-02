#!/bin/bash
/bin/python /opt/oracle/dbloadgen/bin/dbloadgen.py -d $DBNAME -i $IPADDR -p $PORTNUM -u $UNAME -s $PASSWORD -l $LOGFILE -t $RUNTIME -w $WRTIETHREAD -r $READTHREAD
