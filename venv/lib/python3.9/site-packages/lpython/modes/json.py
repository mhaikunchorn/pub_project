# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: json.py
# Title: JSON filter and transformer
# Description: Loads a JSON from the standard input, offers it for
# Description: transformation, and after, writes it to the standard output.
#
# Var: DATA - the parsed JSON input, in whatever format the input represents.
#
# Fun: PRETTY - Sets the JSON output to be prettified.
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
import json
import sys


ARGS = sys.argv
__PRETTY_JSON__ = False


def PRETTY():
    global __PRETTY_JSON__
    __PRETTY_JSON__ = True


DATA = json.load(sys.stdin)


# --- USER CODE GOES HERE ---

if DATA:
    if not __PRETTY_JSON__:
        print(json.dumps(DATA))
    else:
        print(json.dumps(DATA, sort_keys=True, indent=4))

# ---  END  TEMPLATE ---
