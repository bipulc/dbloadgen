# Pull base image
# ---------------
FROM oraclelinux:latest

# Maintainer
# ----------
MAINTAINER Bipul Kumar <bipul.kumar@oracle.com>

# Set environment variables required for this build
# -------------------------------------------------
ENV ORACLE_BASE=/opt/oracle \
    ORACLE_HOME=/opt/oracle/instantclient_12_1 \
    INSTALL_FILE_1="instantclient-basic-linux.x64-12.1.0.2.0.zip" \
    INSTALL_FILE_2="instantclient-sdk-linux.x64-12.1.0.2.0.zip" \
    INSTALL_FILE_3="instantclient-sqlplus-linux.x64-12.1.0.2.0.zip" \
    LOADGENSRC="dbloadgen.tar" \
    ENTRYFILE="entrypoint.sh" \
    EPELFILE="epel-release-latest-7.noarch.rpm" \
    DBNAME="PDB1" \
    IPADDR="192.168.56.102" \
    PORTNUM=1521 \
    UNAME="aco_demo" \
    PASSWORD="aco_demo" \
    LOGFILE="/tmp/dbloadgen.log" \
    RUNTIME=2 \
    WRTIETHREAD=2 \
    READTHREAD=0     


# Use second ENV so that variable get substituted
ENV PATH=$ORACLE_HOME:$PATH \
    LD_LIBRARY_PATH=$ORACLE_HOME:/usr/lib 

COPY $EPELFILE $ENTRYFILE $INSTALL_FILE_1 $INSTALL_FILE_2 $INSTALL_FILE_3 $LOADGENSRC $ORACLE_BASE/

# Set up oracle user and install rpms
# -----------------------------------

RUN groupadd -g 500 oracle && \
    useradd -u 500 -d /home/oracle -g oracle -m -s /bin/bash oracle && \
    rpm -ivh $ORACLE_BASE/epel-release-latest-7.noarch.rpm && \
    yum -y install gcc unzip libaio python-pip python-devel && \
    yum clean all

RUN chown -R oracle:oracle /opt

# Install Oracle Client (as oracle user) and cx_Oracle as root
# ------------------------------------------------------------
USER oracle
WORKDIR $ORACLE_BASE
RUN unzip $INSTALL_FILE_1 && \
    unzip $INSTALL_FILE_2 && \
    unzip $INSTALL_FILE_3 && \
    ln -s $ORACLE_HOME/libclntsh.so.12.1 $ORACLE_HOME/libclntsh.so && \
    ln -s $ORACLE_HOME/libocci.so.12.1 $ORACLE_HOME/libocci.so

USER root
RUN pip install cx_Oracle 

USER oracle
WORKDIR $ORACLE_BASE
RUN tar xvf dbloadgen.tar

ENTRYPOINT ["/opt/oracle/entrypoint.sh"]
