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

import io
import os
import shutil
import sys


basedir = os.path.join(os.path.dirname(__file__), "modes")


class ExecutionContext:
    def __init__(self, text):
        """Load an LPython execution template from the given text."""
        lines = text.splitlines(False)
        if lines[0] != "# LPython execution context template.":
            raise ValueError("Invalid headerline")

        metadata_start = lines.index("# --- BEGIN METADATA ---") + 1
        metadata_end = lines.index("# ---  END  METADATA ---")
        metablock = lines[metadata_start:metadata_end]

        self.file = ""
        self.name = ""
        self.title = ""
        self.description = ""
        self.vars = []
        self.funs = []

        for line in metablock:
            line = line.lstrip("#").lstrip().rstrip()
            if not line:
                continue
            k, v = tuple(map(lambda s: s.strip(), line.split(":")))
            if not k:
                continue
            if k == "File":
                self.file = os.path.join(basedir, v)
                self.name = v.replace(".py", "")
            elif k == "Title":
                self.title = v
            elif k == "Description":
                if self.description:
                    self.description += " "
                self.description += v
            elif k == "Var":
                self.vars.append(v)
            elif k == "Fun":
                self.funs.append(v)

        template_start = lines.index("# --- BEGIN TEMPLATE ---") + 1
        template_end = lines.index("# ---  END  TEMPLATE ---")
        template = lines[template_start:template_end]

        self.text_head = io.StringIO()
        self.text_tail = io.StringIO()
        insertion_found = False
        for idx, line in enumerate(template):
            line += "\n"
            if "# --- USER CODE GOES HERE ---" in line:
                if insertion_found:
                    raise ValueError("Multiple insertion lines")
                insertion_found = idx
                self.leading_spaces = len(line) - len(line.lstrip())
            else:
                if line.lstrip().startswith("# "):
                    # Ignore comments.
                    continue

                if line.rstrip().endswith("pass") and \
                        idx == insertion_found + 1:
                    # Ignore a null statement ("pass") right after the
                    # insertion line.
                    continue

                if not insertion_found:
                    self.text_head.write(line)
                else:
                    self.text_tail.write(line)

        if not insertion_found:
            raise ValueError("No insertion line "
                             "'# --- USER CODE GOES HERE ---' "
                             "found")

    def __call__(self, user_code):
        """Inject the given user code into the parsed template."""
        self.text_head.seek(0)
        self.text_tail.seek(0)
        output = io.StringIO()

        shutil.copyfileobj(self.text_head, output)

        line = user_code.readline()
        while line:
            output.write(" " * self.leading_spaces)
            output.write(line)
            line = user_code.readline()

        output.write("\n")
        shutil.copyfileobj(self.text_tail, output)

        return output


def load(mode_name):
    file_path = os.path.join(basedir, mode_name + ".py")
    try:
        with open(file_path, "r") as f:
            return ExecutionContext(f.read())
    except OSError as ose:
        print("[system error] %s when loading context %s" % (ose, mode_name),
              file=sys.stderr)
        return None


def load_all():
    result = []
    for f in os.listdir(os.path.join(os.path.dirname(__file__), "modes")):
        if not f.endswith(".py"):
            continue
        result.append(load(f.replace(".py", "")))
    return result
