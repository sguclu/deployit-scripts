#!/bin/bash
JAVA_HOME=/home/dpyprd02/deployit/tools/java/current
DEPLOYIT_SERVER_HOME=/home/dpyprd02/deployit/data/deployit01/server
DEPLOYIT_CFG_JAAS="${DEPLOYIT_SERVER_HOME}/kerberos/jaas.conf"
DEPLOYIT_CFG_KRB5="${DEPLOYIT_SERVER_HOME}/kerberos/krb5.conf"

DEPLOYIT_SERVER_OPTS="-Xmx6G -XX:MaxPermSize=128m -Djava.io.tmpdir=/home/dpyprd02/deployit/data/deployit01/tmp"
DEPLOYIT_SERVER_OPTS="${DEPLOYIT_SERVER_OPTS} -Djavax.net.ssl.trustStore=/home/dpyprd02/deployit/data/.ssl/dpyprdap01.fr.world.socgen.jks"
DEPLOYIT_SERVER_OPTS="${DEPLOYIT_SERVER_OPTS} -Djava.security.auth.login.config=${DEPLOYIT_CFG_JAAS}"
DEPLOYIT_SERVER_OPTS="${DEPLOYIT_SERVER_OPTS} -Djava.security.krb5.conf=${DEPLOYIT_CFG_KRB5}"

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
