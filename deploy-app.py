import sys

# check deployment status
def checkDeploymentStatus(taskId):
  task = deployit.retrieveTaskInfo(taskId)
  if task.state != "DONE":
    raise Exception("Errors during deployment, status : ",task.state)
  #print task.state  

# Load environment
package = repository.read(sys.argv[1])
print "Application to deploy : ", package
#deployedId = sys.argv[2]
deployed = repository.read(sys.argv[2])
print "Deployed : ",deployed
#deployed = repository.read(environment.id + "/" + #package.id.split('/')[-1]) 
#print "Deployed : ",deployed

# Start deployment
#print " --> deployment.prepareInitial"
#deploymentRef = deployment.prepareInitial(package.id, deployed.id)
#print " --> deployment.generateAllDeployeds"
#deploymentRef = deployment.generateAllDeployeds(deploymentRef)
print " --> deployment.prepareUpgrade"
deploymentRef = deployment.prepareUpgrade(package.id, deployed.id)
print " --> deployment.validate"
deploymentRef = deployment.validate(deploymentRef)
print " --> deployment.deploy"
taskID = deployment.deploy(deploymentRef).id
print "--> deployit.startTaskAndWait(taskID : ", taskID, ")"
deployit.startTaskAndWait(taskID)
checkDeploymentStatus(taskID)
