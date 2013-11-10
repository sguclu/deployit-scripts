#!/bin/bash
export JAVA_HOME=/usr/lib/jvm/java-1.6.0-openjdk/
export DEPLOYIT_CLI_HOME=/ALMBOX/data/deployit/inst01/server/

export DEPLOYIT_CLI_OPTS="-Xms512m -Xmx2g"

env | grep DEPLOYIT
${DEPLOYIT_CLI_HOME}/bin/cli.sh -secure -host deploynode -port 4516 $*

