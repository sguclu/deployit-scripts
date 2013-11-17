import sys

# constants acting on the authorization matrix behaviour
# some entities will have environment-specific directories, others not
nonEnvItems = [ 'Applications', 'Configuration' ]
envItems = [ 'Infrastructure', 'Environments' ]
items = nonEnvItems + envItems
# some roles are environment-specific, others not
nonEnvRoles = [ 'IMPORTER' ]
envRoles = [ 'SYSADMIN', 'OPERATOR', 'APPADMIN' ]
roles = nonEnvRoles + envRoles
# authorization matrix rules
globalprivileges = {}
appprivileges = {}
globalprivileges['SYSADMIN'] = [ "discovery", "login", "report#view" ]
globalprivileges['APPADMIN'] = [ "login", "report#view" ]
globalprivileges['OPERATOR'] = [ "login", "report#view", "task#assign", "task#preview_step" ]
globalprivileges['IMPORTER'] = [ "login", "report#view" ]
appprivileges['SYSADMIN'] = { 'Applications' : [], 'Infrastructure' : [ "controltask#execute","read","repo#edit" ], 'Environments' : [], 'Configuration' : [] }
appprivileges['OPERATOR'] = { 'Applications' : [ "read" ], 'Infrastructure': [], 'Environments' : [ "controltask#execute", "deploy#initial", "deploy#undeploy", "deploy#upgrade", "read", "repo#edit", "task#move_step", "task#skip_step" ], 'Configuration' : [ "read" ] }
appprivileges['APPADMIN'] = { 'Applications' : [ "controltask#execute", "import#initial", "import#remove", "import#upgrade", "read", "repo#edit" ], 'Environments' : [ "controltask#execute", "read", "repo#edit" ], 'Configuration' : [ "controltask#execute", "read", "repo#edit" ] }
appprivileges['IMPORTER'] = { 'Applications' : [ "controltask#execute", "import#initial", "import#upgrade" ], 'Infrastructure' : [], 'Environments' : [], 'Configuration' : [] }

# generic CI create function
def create(id, type):
  if not repository.exists(id):
    repository.create(factory.configurationItem(id, type, {}))

# role creation and global rights assignment function
def rolecreate(roletype,roleid):
    print " -- create role " + roleid
    security.assignRole(roleid, [])
    # global privileges attribution for each role instance
    print " ---- global grants given : ",
    for globalprivilege in globalprivileges[roletype]:
      print globalprivilege + " ",
      security.grant(globalprivilege,roleid)
    print ""

# gives "read" write to a given role on a given path
def grantreaddir(roleid,path):
  print roleid,
  security.grant("read",roleid, [ path ])

# MAIN CODE

# checks the mandatory parameters
print "######### APPLICATION CREATION SCRIPT #########"
print ""
try:
  department = sys.argv[1].upper()
  application = sys.argv[2].upper()
  environments = sys.argv[3].split(",")
except:
  print sys.exc_info()
  print "Usage : create-application.py '<OU1>/<OU2>/<OU3>', '<APP>', '<ENV1>,<ENV2>,<ENV3>')" 
  raise Exception("EXCEPTION : Department,application and environments are mandatories")

# initiates the list of "directories"
departmentpaths=department.split("/")
departmentpaths.append(application)
for i in range(len(departmentpaths)):
  if (i>0): departmentpaths[i]=departmentpaths[i-1]+'/'+departmentpaths[i]

# creates all the roles required for this application
print " 1 - ROLES CREATION AND GLOBAL RIGHTS SETUP"
for role in roles:
  # roles created : for each application the role is instanciated on each environment except nonEnvRoles ones
    if (role in nonEnvRoles):  rolecreate(role, application + "_" + role)
    else:
      for env in environments: rolecreate(role,application + "_" + env + "_" + role)
print ""

# creates the Applications, Infrastructure, Environments and Configuration intermediate directories
print " 2 - INTERMEDIATE DIRECTORIES CREATION AND RIGHTS SETUP"
for item in items:
  for path in departmentpaths:
    temppath = item + "/" + path
    print " -- create directory : " + temppath
    create(temppath, "core.Directory")
    print " ---- read rights granted to : ",
    # applies read privilege for all roles
    for role in roles:
      if (role in nonEnvRoles):
        grantreaddir(application + "_" + role, temppath)
      else:  
        for env in environments:  grantreaddir(application + "_" + env + "_" + role, temppath)
    print ""
print ""

# Create "non environment entities" rights
print " 3 - NON-ENVIRONMENT ENTITIES RIGHTS SETUP"
for item in nonEnvItems:
  directory =  item + "/" + department + "/" + application
  print " -- create directory : " + directory
  create( directory, "core.Directory")
  for role in roles:
    for env in environments:
      if ( role in nonEnvRoles): app_env_role = application + "_" + role
      else: app_env_role = application + "_" + env + "_" + role
      roleprivileges=appprivileges[role].get(item)
      if (roleprivileges is not None):
        print " ---- given privileges to " + app_env_role + " role :  ",
        for privilege in roleprivileges:
          security.grant(privilege, app_env_role, [directory])
          print privilege,
        print ""
print ""

# binds application roles with "final" directories
print " 4 - ENVIRONMENT ENTITIES RIGHTS SETUP"
for item in envItems:
  directoryList = []
#  if (item in envItems):
  for environment in environments:
    directoryList.append(item + "/" + department + "/" + application + "/" + environment)
  for directory in directoryList:
    print " -- create directory : " + directory
    create(directory, "core.Directory")
    for role in roles:
      if ( role in nonEnvRoles): app_env_role = application + "_" + role
      else: app_env_role = application + "_" + directory.split("/")[-1] + "_" + role
      roleprivileges=appprivileges[role].get(item)
      if (roleprivileges is not None):
        print " ---- given privileges to '" + app_env_role + " role : ",
        for privilege in roleprivileges:
          security.grant(privilege, app_env_role, [directory])
          print privilege,
        print ""
print ""

