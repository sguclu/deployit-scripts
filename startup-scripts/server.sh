#!/bin/bash
export DEPLOYIT_SERVER_HOME=/ALMBOX/data/deployit/inst01/server/
export JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk/
export DEPLOYIT_SERVER_OPTS="-Xmx1024m -XX:MaxPermSize=128m"
export DEPLOYIT_SERVER_LOG_OPTS="-Dlogback.configurationFile=${DEPLOYIT_SERVER_HOME}conf/logback.xml -Dderby.stream.error.file=${DEPLOYIT_SERVER_HOME}/log/derby.log -Djava.security.auth.login.config=${DEPLOYIT_SERVER_HOME}/conf/jaas.conf -Djava.security.krb5.conf=${DEPLOYIT_SERVER_HOME}/conf/krb5.conf"

export JAVA_HOME
export DEPLOYIT_SERVER_HOME
export DEPLOYIT_SERVER_OPTS

function usage {
  echo "Usage : $0 [start|console|stop|restart|status]"
}

function start {
  echo "Starting ${DEPLOYIT_SERVER_HOME} deployit server..."
  env | grep DEPLOYIT
  cd ${DEPLOYIT_SERVER_HOME}
  bin/server.sh >/dev/null 2>&1 &
  MYPID=$!
  # check the deployit java process itself
  sleep 2
  JAVAPID="`pstree -p ${MYPID} | head -n 1 |  sed 's/^.*---java(\([0-9]*\)).*$/\1/g'`"
  if [ "$JAVAPID" == "" ]
  then
    echo "Server could not start."
    exit 1
  fi
  echo "Server started, PID : $JAVAPID"
  echo ${JAVAPID} > ${DEPLOYIT_SERVER_HOME}/server.pid
  cd -
}

function console {
  echo "Starting ${DEPLOYIT_SERVER_HOME} deployit server..."
  env | grep DEPLOYIT
  cd ${DEPLOYIT_SERVER_HOME}
  bin/server.sh $*
  cd -
}

function stop {
  echo "Stopping ${DEPLOYIT_SERVER_HOME} deployit server..."
  JAVAPID="`cat ${DEPLOYIT_SERVER_HOME}/server.pid 2>/dev/null`"
    if [ "$JAVAPID" == "" ]
  then
   echo "Deployit instance apparently not started."
   exit 1
  fi
  kill $JAVAPID
  sleep 2
  if [ "$?" != "0" ]
  then
    echo "Could not stop Deployit server (PID : ${JAVAPID})."
    exit 1
  fi
  echo "Server stopped"
  rm ${DEPLOYIT_SERVER_HOME}/server.pid
}

function status {
  echo "Checking ${DEPLOYIT_SERVER_HOME} deployit server status..."
  PID="`cat ${DEPLOYIT_SERVER_HOME}/server.pid 2>/dev/null`"
  pstree -p "$PID" >/dev/null 2>&1
  if [ "$?" != 0 ] || [ "$PID" == "" ]
  then
    echo "Server stopped"
  else
    echo "Server started, PID : $PID"
  fi
}

function restart {
  echo "Restarting ${DEPLOYIT_SERVER_HOME} deployit server..."
  stop
  start
}

# MAIN
OPTION=$1
if [ "$OPTION" == "" ]
then
  usage
  exit 0
fi


case $OPTION in
      start)  start ;;
      stop) stop ;;
      restart) restart ;;
      status) status ;;
      console) shift ; console $* ;;
      **usage) usage ; exit 1;;
esac
