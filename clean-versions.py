# Applications cleanup script
# Releases/snapshots versions are processed separately, depending on options defined for each package
# Applications snapshots/release versions older than 30 days will be removed, except the last MaxNbOfSnapshotsToKeep / MaxNbOfReleasesToKeep
from java.util import Calendar
import sys,re

# command-line options for debug and dry run
dryrun="dryrun" in sys.argv
debug="debug" in sys.argv

# global constants and variables
snapshotsPattern="^.*-\d{8}-\d{6}$"
snapshotsExpression = re.compile(snapshotsPattern)
versionsRemoved = []
versionsNotRemoved = []

#creates a "Version tree" containing the versions to remove for each application
def computeVersionTree(someVersions,nbOfSnapshotsToKeep,nbOfReleasesToKeep):
  resultList=[]
  snapshotsList=[]
  releasesList=[]
  for aVersion in someVersions:
    if snapshotsExpression.match(aVersion):  snapshotsList.append(aVersion)
    else:  releasesList.append(aVersion)
  if debug:  print "releasesList=",releasesList
  if debug:  print "nbOfReleasesToKeep=",nbOfReleasesToKeep  
  if debug:  print "snapshotsList=",snapshotsList	  
  if debug:  print "nbOfSnapshotsToKeep=",nbOfSnapshotsToKeep  
  if (len(releasesList) > nbOfReleasesToKeep):  resultList.append(releasesList[0:len(releasesList)-nbOfReleasesToKeep])
  if debug:  print "Versions to remove: ",resultList	  
  if (len(snapshotsList) > nbOfSnapshotsToKeep):  resultList.append(snapshotsList[0:len(snapshotsList)-nbOfSnapshotsToKeep])  
  if debug:  print "Versions to remove: ",resultList	  
  return resultList

#cleanup function checking the dryrun mode
def deleteVersion(aVersion):
  if dryrun:  print "DRY RUN ACTIVATED, ",aVersion, "PACKAGE NOT REMOVED"
  else:
    try:
      repository.delete(aVersion)
      versionsRemoved.append(aVersion)
    except:
      print "ERROR DURING ",aVersion, "REMOVAL"
      versionsNotRemoved.append(aVersion)

# main loop
applications=repository.search("udm.Application")
if debug:  print "applications : ",applications	  
for application in applications:
  try: 
    app=repository.read(application) 
    versions=repository.search("udm.DeploymentPackage",application)
    maxNbOfSnapshotsToKeep=app.getSyntheticProperty("MaxNbOfSnapshotsToKeep")
    maxNbOfReleasesToKeep=app.getSyntheticProperty("MaxNbOfReleasesToKeep")
    print "Application : ",app, "(MaxNbOfReleasesToKeep : ",maxNbOfReleasesToKeep,", MaxNbOfSnapshotsToKeep :",maxNbOfSnapshotsToKeep,")"
    if debug:  print "Versions : ",versions
    removableVersions=computeVersionTree(versions,maxNbOfSnapshotsToKeep,maxNbOfReleasesToKeep)
    for version in removableVersions:
	print "Version to delete : ",version
	deleteVersion(version)
  except:
    print sys.exc_info()

print "Candidate versions removed : ", versionsRemoved
print "Planned but still used versions : ", versionsNotRemoved
