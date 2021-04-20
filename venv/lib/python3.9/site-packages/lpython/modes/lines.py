# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: lines.py
# Title: line-by-line text operation
# Description: Executes the script in a loop that iterates over every line in
# Description: the standard input. The user's code is automatically placed
# Description: inside an appropriate loop.
#
# Var: LINE - one line from the input as handled in the loop.
#
# Fun: OUT(...) - write to the standard output, explicitly (no newline at end)
# Fun: ERR(...) - write to the standard error, explicitly (no newline at end)
# ---  END  METADATA ---
#
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
#
# --- BEGIN TEMPLATE ---
import fileinput
import sys


ARGS = sys.argv


def OUT(*args):
    print(*args, end='')


def ERR(*args):
    print(*args, end='', file=sys.stderr)


for LINE in fileinput.input("-"):
    if LINE[-1] == "\n":
        LINE = LINE[:-1]
    # --- USER CODE GOES HERE ---
    pass

# ---  END  TEMPLATE ---
