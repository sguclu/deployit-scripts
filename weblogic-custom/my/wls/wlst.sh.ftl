<#assign envVars=container.envVars />
<#list envVars?keys as envVar>
${envVar}="${envVars[envVar]}"
export ${envVar}
</#list>

# set up common environment
. "${WL_HOME}/server/bin/setWLSEnv.sh"

echo
echo CLASSPATH=${CLASSPATH}

"${JAVA_HOME}/bin/java" ${WLST_OPTS} -Dprod.props.file=${WL_HOME}/.product.properties weblogic.WLST "$@"
