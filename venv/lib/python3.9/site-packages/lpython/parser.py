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

import functools
import io
import sys

from .tokeniser import TokenKind


CLOSE_TO_OPEN_PAIR = {')': '(',
                      ']': '[',
                      '}': '{'
                      }


HANDLERS = {}


class Parser:
    def __init__(self, lexer, debug_messages=False):
        if debug_messages:
            def __debug(*args, **kwargs):
                kwargs['file'] = sys.stderr
                print(*args, **kwargs)
            self.__debug = __debug
        else:
            def __none(*args, **kwargs):
                pass
            self.__debug = __none

        self._l = lexer
        self._o = io.StringIO()
        self._eof = False
        self._parens = []
        self._announced_blocks = []
        self._opened_blocks = []

    @property
    def eof(self):
        return self._eof

    def _preceding_context_for_token(self, token, length=16):
        """Returns some preceding context for a token in the input stream."""
        start_position = token.position - length
        read_length = length
        if start_position < 0:
            # If the start would underflow the buffer, start reading from the
            # start of the buffer instead, and read a smaller text.
            read_length = token.position
            start_position = 0

        self.__debug("Reading", read_length, "at", start_position, "for "
                     "precontext of", token)
        return self._l.seek_and_peek(start_position, read_length)

    def _succeeding_context_for_token(self, token, length=16):
        """Returns some succeeding context for a token in the input stream."""
        start_position = token.position + len(token.value)
        self.__debug("Reading", length, "at", start_position, "for "
                     "postcontext of", token)
        return self._l.seek_and_peek(start_position, length)

    def _error(self, msg, token):
        print("\r" + "-" * 60, file=sys.stderr)
        print("Syntax error: %s" % msg, file=sys.stderr)
        print("  when parsing at position %d of a %s: '%s'"
              % (token.position, token.kind, token.value), file=sys.stderr)
        prefix_ctx = self._preceding_context_for_token(token)
        print("    %s%s%s"
              % (prefix_ctx,
                 token.value,
                 self._succeeding_context_for_token(token)),
              file=sys.stderr)
        print("    %s^%s" % (' ' * len(prefix_ctx),
                             '~' * (len(token.value) - 1)),
              file=sys.stderr)
        print("", file=sys.stderr)

        if False:
            print("[DEBUG]: Paren stack:", self._parens,
                  file=sys.stderr)
            print("[DEBUG]: Announced scopes:", self._announced_blocks,
                  file=sys.stderr)
            print("[DEBUG]: Open scopes:", self._opened_blocks,
                  file=sys.stderr)

    def _note(self, msg, token):
        print("\r" + "-" * 60, file=sys.stderr)
        print("Note: %s" % msg, file=sys.stderr)
        print("  for position %d where %s was parsed: '%s'"
              % (token.position, token.kind, token.value), file=sys.stderr)
        prefix_ctx = self._preceding_context_for_token(token)
        print("    %s%s%s"
              % (prefix_ctx,
                 token.value,
                 self._succeeding_context_for_token(token)),
              file=sys.stderr)
        print("    %s^%s" % (' ' * len(prefix_ctx),
                             '~' * (len(token.value) - 1)),
              file=sys.stderr)
        print("", file=sys.stderr)

    def handler_for(*kinds):
        def decorator(function_to_decorate):
            @functools.wraps(function_to_decorate)
            def wrapper(*args, **kwargs):
                function_to_decorate(*args, **kwargs)
            for kind in kinds:
                HANDLERS[kind] = wrapper
            return wrapper
        return decorator

    def handle(self, token):
        try:
            return HANDLERS[token.kind](self, token)
        except KeyError:
            self._error("unimplemented token lexed", token)
            raise

    def parse(self):
        self._o.seek(0)
        self._o.truncate()

        while True:
            tok = self._l.next()
            self.__debug(">> Handling", tok)
            if tok.kind == TokenKind.NONE:
                continue

            continue_parsing = self.handle(tok)
            if not continue_parsing:
                self.__debug("<<", self._o.getvalue())
                return self._o.getvalue()

    def _write(self, string):
        self._o.write(string)

    def _copy(self, tok):
        self._write(tok.value)

    def _indent(self, indent_per_level=4):
        """Print indentation to the output buffer according to the number of
        blocks open."""
        self._write(" " * indent_per_level * len(self._opened_blocks))

    @handler_for(TokenKind.SEMI, TokenKind.EOF)
    def _end(self, tok):
        self._write("\n")
        self._indent()

        if tok.kind == TokenKind.EOF:
            self._eof = True

            if self._parens:
                self._error("input ended but there were unclosed parens", tok)
                self._note("last paren opened here", self._parens[-1])
                return False
            if self._opened_blocks:
                self._error("input ended but there were unclosed blocks", tok)
                self._note("last block opened here", self._opened_blocks[-1])
                return False
        return False

    @handler_for(TokenKind.VERBATIM)
    def _verbatim(self, tok):
        self._copy(tok)
        return True

    @handler_for(TokenKind.OPEN)
    def _open_paren(self, tok):
        self._parens.append(tok)
        self._copy(tok)
        self.__debug("Open paren", tok, "New paren-stack:", self._parens)
        return True

    @handler_for(TokenKind.CLOSE)
    def _close_paren(self, tok):
        self.__debug("Closing paren", tok, "for paren-stack:", self._parens)
        try:
            last_paren = self._parens[-1]
            if last_paren.value != CLOSE_TO_OPEN_PAIR[tok.value.strip()]:
                self._error("last opened %s closed by %s" % (last_paren.value,
                                                             tok.value),
                            tok)
                self._note("opened here", last_paren)
                return False
        except KeyError:
            self._parens.pop()
            self._error("unhandled closing paren, no opening pair implemented",
                        tok)
            return False
        except IndexError:
            self._error("closing paren without open one", tok)
            return False

        self._parens.pop()
        self._copy(tok)
        return True

    @handler_for(TokenKind.IF, TokenKind.WHILE, TokenKind.FOR,
                 TokenKind.WITH, TokenKind.DEF, TokenKind.CLASS)
    def _open_kwscope(self, tok):
        if self._parens:
            # If there are some open parentheses, the keywords do not open
            # a block.
            self._copy(tok)
            self._write(" ")
            return True

        self._announced_blocks.append(tok)
        self._copy(tok)
        self._write(" ")
        self.__debug("Block announced by", tok,
                     "open-blocks:", self._opened_blocks,
                     "announced-blocks:", self._announced_blocks)
        return True

    @handler_for(TokenKind.ELIF, TokenKind.ELSE)
    def _if_continuity(self, tok):
        if self._parens:
            # If there are some open parens, the : does not herald the begin
            # of a block.
            self._copy(tok)
            self._write(" ")
            return True

        # An elif or else requires a previously open "if", but needs to close
        # the if's block, put the elif on the same indent level as the if was,
        # and open a new block.
        try:
            if self._opened_blocks[-1].kind not in [TokenKind.IF,
                                                    TokenKind.ELIF]:
                self._error("'%s' encountered but no previous 'if'"
                            % tok.value,
                            tok)
                self._note("previous unclosed block here",
                           self._opened_blocks[-1])
                return False
        except IndexError:
            self._error("'%s' encountered but no previous 'if'" % tok.value,
                        tok)
            return False

        # Close the if.
        self._opened_blocks.pop()
        self._announced_blocks.pop()

        self.__debug("Block closed by", tok,
                     "open-blocks:", self._opened_blocks,
                     "announced-blocks:", self._announced_blocks)

        # Write the elif/else and start a new block.
        self._write("\n")
        self._indent()
        ret = self._open_kwscope(tok)
        return ret

    @handler_for(TokenKind.COLON)
    def _colon(self, tok):
        if self._parens:
            # If there are some open parens, the : does not herald the begin
            # of a block.
            self._copy(tok)
            return True

        if len(self._opened_blocks) == len(self._announced_blocks) - 1:
            self._opened_blocks.append(self._announced_blocks[-1])
            self._write(tok.value.rstrip() + "\n")
            self._indent()
            self.__debug("Block opening", tok,
                         "open-blocks:", self._opened_blocks,
                         "announced-blocks:", self._announced_blocks)
            return False
        else:
            self._error("unskipped : encountered, but no block is opened", tok)
            return False

    @handler_for(TokenKind.ENDIF, TokenKind.ENDWHILE, TokenKind.ENDFOR,
                 TokenKind.ENDWITH, TokenKind.ENDDEF, TokenKind.ENDCLASS)
    def _close_kwscope(self, tok):
        if self._parens:
            self._error("block closing keyword, but unclosed parens", tok)
            self._note("last unclosed paren opened", self._parens[-1])
            return

        self.__debug("Block closing", tok,
                     "open-blocks:", self._opened_blocks,
                     "announced-blocks:", self._announced_blocks)
        try:
            previous_block = self._opened_blocks[-1].value
            if previous_block in ["elif", "else"]:
                # elif/else's block is just like an if block.
                previous_block = "if"

            if previous_block != tok.value.replace("end", ""):
                self._error("last opened block '%s' closed by %s"
                            % (self._opened_blocks[-1].value, tok.value), tok)
                self._note("last block opened here", self._opened_blocks[-1])
                return False

            if self._opened_blocks[-1] != self._announced_blocks[-1]:
                self._error("[internal compiler error] closing last "
                            "opened block '%s' but announced was '%s'"
                            % (self._opened_blocks[-1],
                               self._announced_blocks[-1]), tok)
                self._note("announced here", self._announced_blocks[-1])
                return False
        except IndexError:
            self._error("closing a scope while none was opened", tok)
            return False

        self._opened_blocks.pop()
        self._announced_blocks.pop()
        return True
