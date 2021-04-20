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
import sys

from .args import args
from .builder import load
from .parser import Parser
from .spawn import temporary, spawn
from .tokeniser import Lex


def transpile(code_stream, debug_lex=False, debug_parse=False):
    """Rewrites the input stream of program code according to LPython rules."""
    lexer = Lex(code_stream, debug_lex)
    parser = Parser(lexer, debug_parse)
    output_stream = io.StringIO()

    while not parser.eof:
        stmt = parser.parse()
        output_stream.write(stmt)

    return output_stream


def build(mode, code_stream):
    """Inject the given program code into the template specified by 'mode'."""
    code_stream.seek(0)

    context = load(mode)
    return context(code_stream)


def main(argv=None):
    """The real entry point handler for the program."""
    argd = args.parse_args(argv)

    if not argd.CODE and argd.mode:
        # No code specified, but a mode was specified.
        print("No code specified. Showing help for mode '%s'..." % argd.mode,
              file=sys.stderr)
        print("Specify '--help' for help about 'lpython' itself.",
              file=sys.stderr)

        template = load(argd.mode)
        print("Name:", template.name)
        print("Title:", template.title)
        print("Description:", template.description)
        print()
        if template.vars:
            print("Available variables:")
            for var in template.vars:
                print("  *", var)
            print()
        if template.funs:
            print("Available functions:")
            for fun in template.funs:
                print("  *", fun)
        return 1

    code = io.StringIO(" ".join(argd.CODE))
    code = transpile(code, argd.verbose_lex, argd.verbose_parse)

    if argd.dry_run:
        # Dry run - emit only the rewritten code.
        print(code.getvalue())
        return 0

    code = build(argd.mode, code)

    if argd.build_only:
        print(code.getvalue())
        return 0

    if argd.verbose_lex or argd.verbose_parse:
        return 0

    with temporary(code) as script:
        return_code = spawn(script, argd.argfwd)

    return return_code
