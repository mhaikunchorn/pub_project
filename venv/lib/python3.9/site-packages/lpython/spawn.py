# Copyright (C) 2020 Whisperity
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from contextlib import contextmanager
import os
import shutil
from subprocess import run
import sys
import tempfile


@contextmanager
def temporary(code_buffer):
    with tempfile.TemporaryDirectory(prefix="lpython-") as tempdname:
        filename = os.path.join(tempdname, "code.py")
        with open(filename, "w") as script:
            code_buffer.seek(0)
            shutil.copyfileobj(code_buffer, script)

        yield filename


def spawn(pyscript, argv):
    """Spawns a process and gives it our stdin and stdout."""
    interp = sys.executable if sys.executable else "python3"
    argv = argv if argv else []
    result = run([interp, pyscript] + argv, universal_newlines=True)
    return result.returncode
