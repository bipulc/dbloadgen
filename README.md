# dbloadgen

It is a very light weight command line based load generator tool for Oracle database. Developed and tested using Oracle 12.1.0.2 multitenant architecture. However, it should work with 12.2 and previous versions of database as none of the 12c specific features are used in the script.

The tool is multi-threaded and allows to specify number of write and read threads. Write threads execute a stored procedure generating OLTP style transactions i.e. large volume but small in row size. Read threads execute a pre-defined SQL query. 

The schema itself is very simple and have the following tables

-   Buyer - list of buyers
-   Merchant - list of products and merchants
-   Transaction - A buy transaction by a random buyer from Buyer table buying a random product from Merchant table.

The pl/sql stored procedure load_no_comp is called by Writer threads and does the following, 
-   read a random buyer info from buyer table 
-   read a random product and merchant info from merchant table 
-   construct a transaction and  insert into Transaction table 

## Installation of Database schema and Objects

To install Database schema and objects, connect to a database (or a pluggable database) using a privileged user and execute the setup script to create dbloadgen tablespace and user.

-   dbloadgen_setup.sql

Then connect as dbloadgen user and execute the following scripts to create schema objects.

-   dbloadgen_tables.sql
-   buyer_seed_data.sql
-   merchant_seed_data.sql
-   proc_load_no_comp.sql   

## Usage 
dbloadgen.py -h
usage: dbloadgen.py [-h] [-d D] [-i I] [-p P] [-u U] [-s S] [-w W] [-r R]
                    [-l L] [-t T]

optional arguments:
  -h, --help  show this help message and exit
  -d D        DB Service Name
  -i I        IP Address of Database Server
  -p P        Listener Port number for DB service
  -u U        username
  -s S        password
  -w W        number of write threads
  -r R        number of read threads
  -l L        logfile (fullpath)
  -t T        elapsed time to run the test in minutes

Example:

dbloadgen.py -d <DB Service name>  -i <ip address of DB server> -p <listener port> -u dbloadgen -s dbloadgen -l /tmp
/dbloadgen.log -t 5 -w 2 -r 2'

## Docker Image

Download the docker image from docker hub at https://hub.docker.com/r/bipulc/dbloadgen/

and execute as 

docker run --name dbloadgen-01 --rm <image id>  sh -c 'cd /opt/oracle/dbloadgen/bin; /bin/python /op
t/oracle/dbloadgen/bin/dbloadgen.py -d <DB Service name>  -i <ip address of DB server> -p <listener port> -u dbloadgen -s dbloadgen -l /tmp
/dbloadgen.log -t 5 -w 2 -r 2'

Additionally, a dockerfile in the repo can be used to build the image. To build an image from dockerfile, download the following files in same directory as dockerfile.

    -    Oracle Instant Client zip files  for instantclient_12_1 from OTN.

            instantclient-basic-linux.x64-12.1.0.2.0.zip
            instantclient-sdk-linux.x64-12.1.0.2.0.zip
            instantclient-sqlplus-linux.x64-12.1.0.2.0.zip

-    Additionally download epel-release-latest-7.noarch.rpm from Fedora EPEL project
-    and entrypoint.sh from this repo.

and execute 

docker build --rm -t dbloadgen .

## To Do

—> simplify schema installation process
—> allow Reader threads to pick a SQL Query from a list of queries instead of a fixed single query
