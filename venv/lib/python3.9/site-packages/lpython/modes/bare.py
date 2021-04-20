# LPython execution context template.
#
# --- BEGIN METADATA ---
# File: bare.py
# Title: bare stream handling
# Description: The script given by the user is executed verbatim.
# Description: This mode performs no additional operation and offers no
# Description: helping logic.
#
# Var: STDIN - the Python sys.stdin stream
# Var: STDOUT - the Python sys.stdout stream
# Var: STDERR - the Python sys.stderr stream
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
#
# --- BEGIN TEMPLATE ---
import sys


ARGS = sys.argv
STDIN = sys.stdin
STDOUT = sys.stdout
STDERR = sys.stderr


# --- USER CODE GOES HERE ---


# ---  END  TEMPLATE ---
