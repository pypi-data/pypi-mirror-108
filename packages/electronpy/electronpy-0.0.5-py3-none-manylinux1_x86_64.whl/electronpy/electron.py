# coding: utf-8
# Copyright 2021 yuncliu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
"""electronpy entry"""

import sys
import subprocess
import os

CUR_DIR = os.path.dirname(__file__)


def main_linux(app_path):
    """
    entry for linux
    """
    cmds = [os.path.join(CUR_DIR, "electron", "electron")]
    if app_path is not None:
        cmds.append(app_path)
    cmds.extend(sys.argv[1:])
    if os.getuid() == 0:
        cmds.append('--no-sandbox')
    try:
        subprocess.Popen(cmds).wait()
    except KeyboardInterrupt:
        pass


def main_win32(app_path):
    """
    entry for win32
    """
    cmds = [os.path.join(CUR_DIR, "electron", "electron.exe")]
    if app_path is not None:
        cmds.append(app_path)
    cmds.extend(sys.argv[1:])
    try:
        subprocess.Popen(cmds).wait()
    except KeyboardInterrupt:
        pass

def main(app_path=None):
    """
    :param: app_path    the path of electron app
    """
    if sys.platform.lower() == 'win32':
        main_win32(app_path)
    else:
        main_linux(app_path)

if __name__ == '__main__':
    main()
