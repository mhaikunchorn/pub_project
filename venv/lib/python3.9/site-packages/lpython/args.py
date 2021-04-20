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

import argparse
import sys

from .builder import load_all


def default_mode():
    """Sets the default mode to line-by-line execution if the standard input
    it not a terminal. In most cases, this means it is a pipe, or a file.
    """
    if not sys.stdin.isatty():
        return "lines"
    return "bare"


args = argparse.ArgumentParser(
        prog="lpython",
        description="Rewrite Python scripts written in a linear code fashion "
                    "to real Python scripts, and execute them for quick & "
                    "dirty shell pipeline operations.",
        epilog="Linear Python scripts differ from real Python in a few "
               "crucial ways. First, there is no need to handle indentation, "
               "because it is meant to be written in one line like a shell "
               "command. Second, there is no need for newlines, as the "
               "semicolon (';') line separator, common in many other "
               "programming languages, have been reintroduced. To emphasise "
               "blocks, instead of indentation, explicit closing keywords are "
               "used: \"with X: print(); endwith;\"."
        )

stage_stop = args.add_mutually_exclusive_group()

stage_stop.add_argument("-n",
                        dest="dry_run",
                        action="store_true",
                        help="Do not execute, just rewrite the input code, "
                             "without the execution context, as Python script "
                             "and emit the result to the standard output.")

stage_stop.add_argument("-b",
                        dest="build_only",
                        action="store_true",
                        help="Do not execute, but rewrite the input code and "
                             "build the full execution context, and emit the "
                             "result to the standard output.")

args.add_argument("-vl",
                  dest="verbose_lex",
                  action="store_true",
                  help="Enable verbose debugging messages of the lexer's "
                       "internal workings. Implies disabling execution.")

args.add_argument("-vp",
                  dest="verbose_parse",
                  action="store_true",
                  help="Enable verbose debugging messages of the parser's "
                       "internal workings. Implies disabling execution.")

args.add_argument("-t",
                  dest="mode",
                  choices=list(map(lambda c: c.name, load_all())),
                  default=default_mode(),
                  help="The operational framework to embed the script into "
                       "during execution. Different choices here affect what "
                       "variables are available during execution and how the "
                       "code is structured. When called with a '-t' argument "
                       "but without code to execute, a help text about the "
                       "specified mode is shown. Defaults to \"bare\" mode "
                       "if the standard input is a shell, and \"lines\" mode "
                       "otherwise, i.e. when it is a pipe or a file."
                  )

args.add_argument("-X",
                  dest="argfwd",
                  metavar="arg",
                  action='append',
                  help="Forward the arguments in the order they are specified "
                       "to the executed script. To forward more arguments, "
                       "specify the option multiple times: "
                       "\"-X arg1 -X arg2\".")

args.add_argument("CODE",
                  nargs="*",
                  help="The LPython code to transpile and execute.")
