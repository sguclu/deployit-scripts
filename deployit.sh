#!/bin/bash
export DEPLOYIT_SERVER_HOME=/ALMBOX/products/deployit/inst01
export JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk/
export DEPLOYIT_SERVER_OPTS="-Xmx1024m -XX:MaxPermSize=128m"
export DEPLOYIT_SERVER_LOG_OPTS="-Dlogback.configurationFile=${DEPLOYIT_SERVER_HOME}conf/logback.xml -Dderby.stream.error.file=${DEPLOYIT_SERVER_HOME}/log/derby.log -Djava.security.auth.login.config=${DEPLOYIT_SERVER_HOME}/conf/jaas.conf -Djava.security.krb5.conf=${DEPLOYIT_SERVER_HOME}/conf/krb5.conf"

cd ${DEPLOYIT_SERVER_HOME}
nohup bin/server.sh &
cd -
