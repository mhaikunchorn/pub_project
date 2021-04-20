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

from enum import Enum
import io
import sys


class TokenKind(Enum):
    NONE = -1
    VERBATIM = 0
    EOF = 1
    SEMI = 2
    COLON = 3
    OPEN = 4
    CLOSE = 5

    IF = 8
    ELIF = 9
    ELSE = 10
    ENDIF = 11

    WHILE = 16
    ENDWHILE = 17
    FOR = 18
    ENDFOR = 19

    WITH = 32
    ENDWITH = 33

    DEF = 64
    ENDDEF = 65

    CLASS = 128
    ENDCLASS = 129


class Token:
    def __init__(self, kind, pos, value=""):
        self.kind = kind
        self.position = pos
        self.value = value

    def __repr__(self):
        return "T<%d(%s), %d, %s>" % (self.kind.value, self.kind.name,
                                      self.position, self.value)


NONE = Token(TokenKind.NONE, -1)

EOF_MAGIC = " <<<EOF>>>"

WHITESPACE = [' ', '\n', '\t', '\r']

TOKEN_BREAKERS = ['(', '[', '{', '}', ']', ')', ':', ';', '/', '\\', '+', '-',
                  '*', '#', '?']


class Lex:
    def __init__(self, stream, debug_messages=False):
        if debug_messages:
            def __debug(*args, **kwargs):
                kwargs['file'] = sys.stderr
                print(*args, **kwargs)
            self.__debug = __debug
        else:
            def __none(*args, **kwargs):
                pass
            self.__debug = __none

        self._s = stream
        self._last = None
        self._m = []

    def tell(self):
        """Tells the current position in the input buffer."""
        return self._s.tell()

    def mark(self):
        """Saves the current position into the jumpback stack."""
        self._m.append(self.tell())
        return self.tell()

    def last_mark(self):
        """Tells the position where the last mark() or remark() put a jumpback.
        """
        return self._m[-1]

    def remark(self):
        """Changes the last marked jumpback to the current position."""
        if not self._m:
            self.mark()
        else:
            self._m[-1] = self.tell()

    def unmark(self):
        """Removes the last jumpback position."""
        if self._m:
            self._m.pop()

    def jump(self):
        """Jumps back to the last jumpback position, and consumes it."""
        if self._m:
            self._s.seek(self._m.pop())

    def read(self, n=1):
        """Read n characters from the input, advancing the stream."""
        ch = self._s.read(n)
        if not ch:
            raise StopIteration()
        return ch

    def peek(self, n=1):
        """Read n characters from the input, but do not advance the stream."""
        self.mark()
        self._last = self._s.read(n)
        self.jump()
        return self._last

    def seek_and_peek(self, p=0, n=1):
        """Jumps to the position p and reads n characters, but then returns to
        the previous position."""
        self.mark()
        self._s.seek(p)
        ret = self._s.read(n)
        self.jump()
        return ret

    def consume(self):
        """Advances the stream's position with the last peek result's token."""
        if not self._last:
            return
        self._s.seek(self._s.tell() + len(self._last))

    def peek_and_consume(self, expected_str):
        """Peek the stream for the length of the expected string, and if found,
        consume the input.

        Returns True if the expected string was found.
        """
        if self.peek(len(expected_str)) == expected_str:
            self.consume()
            return True
        return False

    def _consume_quoted(self, start_quote):
        """Consumes the input starting at the current position and quote
        until that quote is over.
        """
        self.__debug("Encountered quote %c" % start_quote)

        ch = self.read(1)
        if ch != start_quote:
            raise ValueError("Expected input to continue with %c but found "
                             "%c instead." % (start_quote, ch))

        result = io.StringIO()
        result.write(ch)

        self.__debug("Sequencing quote: %c" % ch, end='')
        escape = False
        while True:
            try:
                ch = self.read(1)
                result.write(ch)
                self.__debug(ch, end='')
            except StopIteration:
                self.__debug()
                self.__debug("End of file while consuming quote.")
                raise

            if ch == start_quote and not escape:
                # The quote should be over, otherwise the input is ill-formed.
                break
            elif ch == start_quote and escape:
                # Skip extra logic if the quote symbol is escaped.
                escape = False
                continue

            if ch == "\\":  # \ encountered
                if not escape:
                    # \ marks the beginning of an escape.
                    escape = True
                continue

            if escape:
                # If the previous mark was escaping, it escaped the current
                # character.
                escape = False

        self.__debug()
        self.__debug("Consumed quote:", result.getvalue())
        return result.getvalue()

    def next(self):
        """Lexes the next token."""
        tok = NONE

        pos = self.mark()
        self.__debug(">> Reading @", self.tell())

        if self.peek(1) in ["'", "\""]:
            quoted = self._consume_quoted(self.peek(1))
            tok = Token(TokenKind.VERBATIM, pos, quoted)
            self.__debug("<<", tok)
            self.unmark()
            return tok

        symbol_kind = TokenKind.NONE
        if self.peek_and_consume(";"):
            symbol_kind = TokenKind.SEMI
        elif self.peek_and_consume(":"):
            symbol_kind = TokenKind.COLON
        elif self.peek_and_consume("("):
            symbol_kind = TokenKind.OPEN
        elif self.peek_and_consume("["):
            symbol_kind = TokenKind.OPEN
        elif self.peek_and_consume("{"):
            symbol_kind = TokenKind.OPEN
        elif self.peek_and_consume(")"):
            symbol_kind = TokenKind.CLOSE
        elif self.peek_and_consume("]"):
            symbol_kind = TokenKind.CLOSE
        elif self.peek_and_consume("}"):
            symbol_kind = TokenKind.CLOSE

        if symbol_kind != TokenKind.NONE:
            # Consume consecutive whitespace after the symbols.
            token_text = self._last
            self.__debug("Symbol: %s '%s'" % (symbol_kind, token_text))
            while self.peek_and_consume(" "):
                self.remark()
                token_text += self._last

            self.unmark()
            tok = Token(symbol_kind, pos, token_text)
            self.__debug("<<", tok)
            return tok

        # Try handling some keywords...
        kw_kind = TokenKind.NONE
        if self.peek_and_consume("if"):
            kw_kind = TokenKind.IF
        elif self.peek_and_consume("elif"):
            kw_kind = TokenKind.ELIF
        elif self.peek_and_consume("else"):
            kw_kind = TokenKind.ELSE
        elif self.peek_and_consume("endif"):
            kw_kind = TokenKind.ENDIF
        elif self.peek_and_consume("while"):
            kw_kind = TokenKind.WHILE
        elif self.peek_and_consume("endwhile"):
            kw_kind = TokenKind.ENDWHILE
        elif self.peek_and_consume("for"):
            kw_kind = TokenKind.FOR
        elif self.peek_and_consume("endfor"):
            kw_kind = TokenKind.ENDFOR
        elif self.peek_and_consume("with"):
            kw_kind = TokenKind.WITH
        elif self.peek_and_consume("endwith"):
            kw_kind = TokenKind.ENDWITH
        elif self.peek_and_consume("def"):
            kw_kind = TokenKind.DEF
        elif self.peek_and_consume("enddef"):
            kw_kind = TokenKind.ENDDEF
        elif self.peek_and_consume("class"):
            kw_kind = TokenKind.CLASS
        elif self.peek_and_consume("endclass"):
            kw_kind = TokenKind.ENDCLASS

        if kw_kind != TokenKind.NONE:
            tok = Token(kw_kind, pos, self._last)
            self.__debug("Keyword ", tok)

        # Now that keywords have been consumed if any found, see if the next
        # char is a whitespace separator.
        ch = self.peek(1)
        if (not ch or ch in WHITESPACE or ch in TOKEN_BREAKERS) \
                and tok.kind != TokenKind.NONE:
            # Yay, the token is separated and not continued with a letter or
            # number.
            self.unmark()
            self.__debug("<<", tok)
            return tok
        elif tok.kind != TokenKind.NONE:
            # Nay, the token continues with a different letter, so it's not a
            # keyword by itself.
            self.jump()  # Jump back to beginning of token.
            self.mark()  # And reinstate the marker.
            self.__debug("Keyword", tok, "continues with other letters")

        chars = []
        consume_whitespace_only = False
        self.__debug("Sequencing... \"", end='')
        while True:
            try:
                ch = self.read(1)
                self.__debug(ch, end='')
                if ch in TOKEN_BREAKERS:
                    # Token breaker encountered.
                    self.__debug("\"")
                    self.__debug("\tToken breaker", end='')
                    if not chars:
                        # The token breaker was the only input so far consumed.
                        self.__debug(", but only char.", end='')
                        chars.append(ch)
                        self.remark()  # Save this char as last read.
                        consume_whitespace_only = True
                        continue
                    else:
                        # Break the current token by jumping to just before the
                        # last successful read and prepare the current
                        # character to be part of the next token.
                        self.__debug(", breaking...", end='')
                        consume_whitespace_only = False
                        self.jump()
                        break
                if ch in WHITESPACE:
                    # Whitespace encountered, break off the token, but consume
                    # the whitespace.
                    chars.append(ch)
                    consume_whitespace_only = False
                    break
                if consume_whitespace_only and ch not in WHITESPACE:
                    # If whitespace reading was enabled and found not a white
                    # space, the token must end.
                    self.jump()  # Go back to before the current character.
                    consume_whitespace_only = False
                    break

                chars.append(ch)
                self.remark()  # Set last read char position.
            except StopIteration:
                self.__debug("\"")
                self.__debug("\tEOF!", end='')
                consume_whitespace_only = False
                if not chars:
                    # If nothing is read and we are at the end, produce EOF.
                    self.unmark()
                    self._s.write(EOF_MAGIC)
                    tok = Token(TokenKind.EOF, pos, EOF_MAGIC)
                    self.__debug("")
                    self.__debug("<<", tok)
                    return tok
                # Otherwise, go and return what was collected.
                self.__debug("... but we have a token.", end='')
                break

        self.__debug()
        self.unmark()  # Drop the seekback marker of this call.
        string = "".join(chars)
        if string.strip() == "":
            self.__debug("\tRead empty sequence.")
            return NONE
        tok = Token(TokenKind.VERBATIM, pos, string)
        self.__debug("<<", tok)
        return tok
