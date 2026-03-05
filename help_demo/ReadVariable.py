# encoding:utf-8
from __future__ import print_function

# close open project if necessary:
if projects.primary:
    projects.primary.close()

# opens project
proj = projects.open(r"D:\data\projects\Ampel.project")

# set "Ampel.project" to active application
app = proj.active_application
onlineapp = online.create_online_application(app)

# login to device
onlineapp.login(OnlineChangeOption.Try, True)

# set status of application to "run", if not in "run"
if not onlineapp.application_state == ApplicationState.run:
    onlineapp.start()

# wait 1 second
system.delay(1000)

# read value of iVar1
value = onlineapp.read_value("PLC_PRG.iVar1")

# display value in message view or command line
print(value)

# log out from device and close "Ampel.project"
onlineapp.logout()
proj.close()