#!/usr/bin/env python
#

#   -*- coding: utf-8 -*-
#
#   This file is part of PyBuilder
#
#   Copyright 2011-2015 PyBuilder Team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#
# This script allows to support installation via:
#   pip install git+git://<project>@<branch>
#
# This script is designed to be used in combination with `pip install` ONLY
#
# DO NOT RUN MANUALLY
#

import os
import subprocess
import sys
import glob
import shutil

from sys import version_info

script_dir = os.path.dirname(os.path.realpath(__file__))
exit_code = 0
try:
    subprocess.check_call(["pyb", "--version"])
except FileNotFoundError as e:
    try:
        subprocess.check_call([sys.executable, "-m", "pip.__main__", "install", "pybuilder"])
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
try:
    subprocess.check_call(["pyb", "clean", "install_build_dependencies", "package", "-o"])
    dist_dir = glob.glob(os.path.join(script_dir, "target", "dist", "*"))[0]
    for src_file in glob.glob(os.path.join(dist_dir, "*")):
        file_name = os.path.basename(src_file)
        target_file_name = os.path.join(script_dir, file_name)
        if os.path.exists(target_file_name):
            if os.path.isdir(target_file_name):
                os.removedirs(target_file_name)
            else:
                os.remove(target_file_name)
        shutil.move(src_file, script_dir)
    setup_args = sys.argv[1:]
    subprocess.check_call([sys.executable, "setup.py"] + setup_args, cwd=script_dir)
except subprocess.CalledProcessError as e:
    exit_code = e.returncode
sys.exit(exit_code)
