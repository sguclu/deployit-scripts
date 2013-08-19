from os.path import basename,dirname
from collections import defaultdict
#from java.util import Calendar
import re

# constants used in the script
# nbdaysbeforeeligible = 10
nbversionstokeep = 1
eligibleversionspattern = "^.*$"

# main
# date = Calendar.getInstance()
# date.add (Calendar.DAY_OF_MONTH, -nbdaysbeforeeligible)
versionpattern = re.compile(eligibleversionspattern)

# first filter : packages not modified until "nbdaysbeforeeligible" days
# candidates = repository.search('udm.DeploymentPackage', date)
candidates = repository.search('udm.DeploymentPackage')
versiondict = defaultdict(list)
# print "elected versions (imported before at least",nbdaysbeforeeligible,"days) : "
print "elected versions) : "
for c in candidates:
        try:
                #repository.delete(c))
                package = dirname(c)
                version = basename(c)
                #second filter : we check if the given version matches the given pattern, otherwise we ignore it
                if versionpattern.match(version):
                        print c
                        versiondict[package].append(version)
                        versiondict[package].sort
        except:
                #print "error during ",c," version delete"
                print "error during ",c," version analysis for inclusion"
print "Versions list : ",versiondict
print "Nb of version to keep : ",nbversionstokeep
for c in versiondict.keys():
        try:
                nbversion = len(versiondict[c])
                if nbversion>nbversionstokeep:
                        print "nbversion for ",c," : ",nbversion
                        tempver = versiondict[c]
                        print "current versions : ",tempver
                        tempver.pop(nbversionstokeep)
                        # third filter : we try to remove all versions for this application except the "nbversionstokeep" ones
                        print "versions to remove : ",tempver
                        #todo call the delete on given versions
                        for ver in tempver:
                                dptoremoveid = c+"/"+ver
                                print "Trying to remove ",dptoremoveid,"..."
                                repository.delete(dptoremoveid)
                                print dptoremoveid removed successfully
        except:
                print "error during version removal"
