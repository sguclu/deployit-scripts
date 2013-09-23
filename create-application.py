import sys

# TODOS : 
# Restore the report#view privilege
# Create the "final" directories with the appropriate privileges (with config???)
# Create a pipeline ?? 

# constants acting on the authorization matrix behaviour
items = [ 'Infrastructure', 'Environments', 'Applications', 'Configuration' ]
roles = [ 'SYSADMIN', 'OPERATOR', 'APPADMIN' ]
globalprivileges = {}
# globalprivileges['SYSADMIN'] = [ "discovery", "login", "report#view" ]
globalprivileges['SYSADMIN'] = [ "discovery", "login" ]
# globalprivileges['APPADMIN'] = [ "login", "report#view" ]
globalprivileges['APPADMIN'] = [ "login" ]
#globalprivileges['OPERATOR'] = [ "controltask#execute", "login", "report#view", "task#assign", "task#move_step", "task#preview_step", "task#skip_step" ]
globalprivileges['OPERATOR'] = [ "controltask#execute", "login", "task#assign", "task#move_step", "task#preview_step", "task#skip_step" ]


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

# creates the "directory" tree  
departmentpaths=department.split("/")
departmentpaths.append(application)
for i in range(len(departmentpaths)):
  if (i>0): departmentpaths[i]=departmentpaths[i-1]+'/'+departmentpaths[i]  
  
# creates all the roles required for this application
for env in environments:
  for role in roles:
    # roles created : for each application the role is instanciated on each environment
    app_env_role = application + "_" + env + "_" + role
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
        app_env_role = application + "_" + env + "_" + role
        print " ---- giving 'read' privilege to : " + app_env_role
        security.grant("read",app_env_role, [ temppath ])
		
		
