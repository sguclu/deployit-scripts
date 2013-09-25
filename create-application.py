import sys

# TODO : Create a pipeline ?? 

# constants acting on the authorization matrix behaviour
items = [ 'Infrastructure', 'Environments', 'Applications', 'Configuration' ]
roles = [ 'CITOOL', 'SYSADMIN', 'OPERATOR', 'APPADMIN' ]
globalprivileges = {}
appprivileges = {}
# authorization matrix rules
globalprivileges['SYSADMIN'] = [ "discovery", "login", "report#view" ]
globalprivileges['APPADMIN'] = [ "login", "report#view" ]
globalprivileges['OPERATOR'] = [ "login", "report#view", "task#assign", "task#preview_step" ]
globalprivileges['CITOOL'] = [ "login", "report#view" ]
appprivileges['SYSADMIN'] = { 'Applications' : [], 'Infrastructure' : [ "controltask#execute","read","repo#edit" ], 'Environments' : [], 'Configuration' : [] }
appprivileges['OPERATOR'] = { 'Applications' : [ "read" ], 'Infrastructure': [], 'Environments' : [ "controltask#execute", "deploy#initial", "deploy#undeploy", "deploy#upgrade", "read", "repo#edit", "task#move_step", "task#skip_step" ], 'Configuration' : [ "read" ] }
appprivileges['APPADMIN'] = { 'Applications' : [ "controltask#execute", "import#initial", "import#remove", "import#upgrade", "read", "repo#edit" ], 'Environments' : [ "controltask#execute", "read", "repo#edit" ], 'Configuration' : [ "controltask#execute", "read", "repo#edit" ] } 
appprivileges['CITOOL'] = { 'Applications' : [ "controltask#execute", "import#initial", "import#upgrade" ], 'Infrastructure' : [], 'Environments' : [], 'Configuration' : [] }

# generic create function
def create(id, type):
  if not repository.exists(id):
    repository.create(factory.configurationItem(id, type, {}))

# MAIN CODE

# checks the mandatory parameters
try:
  department = sys.argv[1].upper()
  application = sys.argv[2].upper()
  environments = sys.argv[3].split(",")
except:
  print sys.exc_info()
  raise Exception("EXCEPTION : Department,application and environments are mandatories")

# initiates the list of "directories"  
departmentpaths=department.split("/")
departmentpaths.append(application)
for i in range(len(departmentpaths)):
  if (i>0): departmentpaths[i]=departmentpaths[i-1]+'/'+departmentpaths[i]  
  
# creates all the roles required for this application
for env in environments:
  for role in roles:
    # roles created : for each application the role is instanciated on each environment except CITOOL
    if (role == "CITOOL"):  app_env_role = application + "_" + role
    else:  app_env_role = application + "_" + env + "_" + role
    print " -- create role " + app_env_role
    security.assignRole(app_env_role, [])
    # global privileges attribution for each role instance
    for globalprivilege in globalprivileges[role]:
      print " ---- grant " + globalprivilege + " to " + app_env_role
      security.grant(globalprivilege,app_env_role)

# creates the Applications, Infrastructure, Environments and Configuration intermediate directories
for item in items:
  for path in departmentpaths:
    temppath = item + "/" + path
    print " -- create directory : " + temppath
    create(temppath, "core.Directory")
    # applies read privilege for all roles
    for env in environments:
      for role in roles:
        if (role == "CITOOL"):  app_env_role = application + "_" + role
        else:  app_env_role = application + "_" + env + "_" + role
        print " ---- giving 'read' privilege to : " + app_env_role
        security.grant("read",app_env_role, [ temppath ]) 
		
# binds application roles with "final" directories
for item in items:
  directoryList = []
  if (item == 'Applications'):
    directoryList = [ item + "/" + department + "/" + application ]
  else:
    for environment in environments:
      directoryList.append(item + "/" + department + "/" + application + "/" + environment)
  for directory in directoryList:
    print "-- creating directory : " + directory
    create(directory, "core.Directory")
    for role in roles:
      if ( role == "CITOOL"):  app_env_role = application + "_" + role
      else:  app_env_role = application + "_" + env + "_" + role
      roleprivileges=appprivileges[role].get(item)
      if (roleprivileges is not None):
        for privilege in roleprivileges:
          print "---- giving'" + privilege + "' to '" + app_env_role + "' role on directory : " + directory
          security.grant(privilege, app_env_role, [directory])

# finally, creates a pipeline with the different environments

