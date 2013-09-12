# Applications cleanup script
from java.util import Calendar
import re
snapshotsPattern="^.*\d{8}-\d{6}$"
versionpattern = re.compile(snapshotsPattern)

for application in repository.search("udm.Application"):
  try:
    app=repository.read(application)
    DaysToKeepSnapshots=app.getSyntheticProperty("DaysToKeepSnapshots")
    MaxNbOfSnapshotsToKeep=app.getSyntheticProperty("MaxNbOfSnapshotsToKeep")
    DaysToKeepReleases=app.getSyntheticProperty("DaysToKeepReleases")
    MaxNbOfReleasesToKeep=app.getSyntheticProperty("MaxNbOfReleasesToKeep")

    cleanup=false


    print "Application ",app
    print "Versions : ",repository.search("udm.DeploymentPackage",application)
    print "DaysToKeepSnapshots : ",app.getSyntheticProperty("DaysToKeepSnapshots")
    print "MaxNbOfSnapshotsToKeep",app.getSyntheticProperty("MaxNbOfSnapshotsToKeep")
    print "DaysToKeepReleases",app.getSyntheticProperty("DaysToKeepReleases")
    print "MaxNbOfReleasesToKeep",app.getSyntheticProperty("MaxNbOfReleasesToKeep")
  except:
    print "KAPUT"
