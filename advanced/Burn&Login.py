#!/bin/env python
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function

import os
import sys
import time
from stat import S_IREAD

if __name__ == '__main__':
    proj = projects.primary
    if proj:
        # retrieve active application
        app = proj.active_application
        app.build()
        CompileCategory = Guid("{97F48D64-A2A3-4856-B640-75C046E37EA9}")
        msgs = system.get_message_objects(CompileCategory, Severity.FatalError | Severity.Error)
        if msgs:
            sys.exit(1)
        path, name = os.path.split(proj.path)
        info = proj.get_project_info()
        if not info.author:
            # info.author = "e71828"
            pass
        current_version = info.version  # 类似于 .NET 中的 System.Version，其属性通常不可直接修改，
        if current_version:
            if 'Burned-on-' not in name:
                new_version = (
                    current_version.Major,
                    current_version.Minor,
                    current_version.Build + 1,
                    current_version.Revision
                )
            else:
                new_version = (
                    current_version.Major,
                    current_version.Minor,
                    current_version.Build,
                    current_version.Revision + 1
                )
        else:
            new_version = (0, 1, 0, 0)
        # info.version = new_version  # 更新
        proj.save()
        if 'Burned-on-' not in name:
            time_str = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(path, 'Burned-on-' + time_str + '.project')
            proj.save_as(filename, password='')
            # os.chmod(filename, S_IREAD)  # Can not sync to Onedrive
            if not info.description:
                # info.description = 'Only for recording diff between all versions'
                pass
            # And set the project to released
            info.released = True
            proj.save()

        # create online application
        with online.create_online_application(app) as online_app:
            # login to device
            online_app.login(OnlineChangeOption.Try, True)
            # set status of application to "run", if not in "run"
            if not online_app.application_state == ApplicationState.run:
                online_app.start()
