#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import os
import time
from stat import S_IREAD

if __name__ == '__main__':
    proj = projects.primary
    if proj:
        proj.save()
        path, name = os.path.split(proj.path)
        if 'Burned-on-' not in name:
            time_str = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(path, 'Burned-on-' + time_str + '.project')
            proj.save_as(filename, password='')
            os.chmod(filename, S_IREAD)

        # retrieve active application
        app = proj.active_application
        # create online application
        online_app = online.create_online_application(app)
        # login to device
        online_app.login(OnlineChangeOption.Try, True)
        # set status of application to "run", if not in "run"
        if not online_app.application_state == ApplicationState.run:
            online_app.start()
