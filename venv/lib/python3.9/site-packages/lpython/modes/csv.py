# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: csv.py
# Title: CSV filter and transformer
# Description: Loads a CSV from the standard input, and executes the user code
# Description: in a loop for each row, allowing transformation. After that,
# Description: writes the CSV file to the standard output.
#
# Var: ROW - one row from the input to be handled.
#
# Fun: HEADER() - True if the first row is in ROW, False otherwise.
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
import csv
import sys


ARGS = sys.argv
__READER__ = csv.reader(sys.stdin)
__OUTPUT__ = []
__HEADER__ = True


def HEADER():
    return __HEADER__


for ROW in __READER__:
    # --- USER CODE GOES HERE ---

    __OUTPUT__.append(ROW)
    if __HEADER__:
        __HEADER__ = False


__WRITER__ = csv.writer(sys.stdout)
__WRITER__.writerows(__OUTPUT__)

# ---  END  TEMPLATE ---
