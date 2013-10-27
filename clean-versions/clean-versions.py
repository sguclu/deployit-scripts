# Applications cleanup script
# Releases/snapshots versions are cleaned
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
def computeVersionTree(someVersions,nbOfReleasesToKeep,nbOfSnapshotsToKeep):
  resultList=[] ; snapshotsList=[] ; releasesList=[]
  for aVersion in someVersions:
    if snapshotsExpression.match(aVersion): snapshotsList.append(aVersion)
    else:   releasesList.append(aVersion)
  nbOfReleases=len(releasesList) ;  nbOfSnapshots=len(snapshotsList)
  if debug:
    print "DEBUG - ",nbOfReleases,"releases (",nbOfReleasesToKeep,"versions to keep)"
    print "DEBUG - ",nbOfSnapshots,"snapshots (",nbOfSnapshotsToKeep,"versions to keep)"  
    print "DEBUG - releasesList=",releasesList
    print "DEBUG - snapshotsList=",snapshotsList
  if 0 < nbOfReleasesToKeep < nbOfReleases:  resultList.append(releasesList[0 : nbOfReleases - nbOfReleasesToKeep])
  if 0 < nbOfSnapshotsToKeep < nbOfSnapshots:  resultList.append(snapshotsList[0 : nbOfSnapshots - nbOfSnapshotsToKeep])
  if debug:  print "DEBUG - Versions to remove: ",resultList	  
  return resultList

#cleanup function checking the dryrun mode
def deleteVersion(aVersion):
  ver=aVersion
  try:
    if dryrun:  
      print " -> NOT REMOVED (dryrun mode)"
      versionsNotRemoved.append(ver)
    else:  
      repository.delete(ver)
      versionsRemoved.append(ver)
      print " -> REMOVED"
  except:
    if debug:  print sys.exc_info()
    versionsNotRemoved.append(ver)
    print " -> NOT REMOVED (still referenced?)"

# main loop
print "APPLICATIONS VERSIONS CLEANUP TOOL\n"
applications=repository.search("udm.Application")
for application in applications:
  try: 
    app=repository.read(application) 
    versions=repository.search("udm.DeploymentPackage",application)
    maxNbOfSnapshotsToKeep=int(app.MaxNbOfSnapshotsToKeep)
    maxNbOfReleasesToKeep=int(app.MaxNbOfReleasesToKeep)
    print "Application : ",app
  except:
    print sys.exc_info()
  removableVersions=computeVersionTree(versions,maxNbOfReleasesToKeep,maxNbOfSnapshotsToKeep)
  if removableVersions == []: print "No versions to remove.\n"
  for list in removableVersions:
    for version in list:
      print "Version to delete : ", version
      deleteVersion(version)

print "\nExecution summary:"
if dryrun:
  print  len(versionsNotRemoved), "versions candidates for removal but not removed (dryrun mode)"
  if debug:  print "DEBUG - details : ", versionsNotRemoved
else:
  print len(versionsRemoved), "candidate versions removed"
  if debug:  print "DEBUG - details : ", versionsRemoved
  print len(versionsNotRemoved), "candidate versions not removed (still used?)"
  if debug:  print "DEBUG - details : ", versionsNotRemoved
