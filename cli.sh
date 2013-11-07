#!/bin/bash
export JAVA_HOME=/home/dpyprd02/deployit/tools/java/current
export DEPLOYIT_CLI_HOME=/home/dpyprd02/deployit/data/deployit01/cli

export DEPLOYIT_CLI_OPTS="-Xms512m -Xmx2g"

env | grep DEPLOYIT
${DEPLOYIT_CLI_HOME}/bin/cli.sh -secure -host dpyprdap01.fr.world.socgen -port 4517 $*

