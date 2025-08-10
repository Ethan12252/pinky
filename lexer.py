from tokens import *

class Lexer:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.tokens = []

    # ---HELPER FUNCTIONS---

    # Advance the curr pointer (Comsumes the character)
    def advance(self):
        if self.at_EOF(): return None # bound check
        ch = self.source[self.curr]
        self.curr = self.curr + 1
        return ch

    # Just take a peek at current character (Does not comsumes the char)
    def peak(self):
        if self.at_EOF(): return None # bound check
        return self.source[self.curr]

    # Looks at the next character in the source (Does not comsumes the char)
    def lookahead(self, n=1):
        if self.at_EOF(): return None # bound check
        return self.source[self.curr + n]

    # Check if the next char matches the expectation, if true comsume that char
    def match(self, expected):
        if self.at_EOF():
            return False
        if self.source[self.curr] != expected:
            return False
        self.curr = self.curr + 1  # If it's a match, we also consume that char
        return True

    # Helper to add token
    def add_token(self, token_type):
        self.tokens.append(
            Token(token_type, self.source[self.start : self.curr], self.line)
        )
    
    # curr is at EOF
    def at_EOF(self):
        if self.curr >= len(self.source):
            return True
        else:
            return False

    # ---FUNCTIONS---
    def tokenize(self):
        while self.curr < len(self.source):  # There's still token
            self.start = self.curr
            ch = self.advance()
            # special one char tokens
            if   ch == '\n': self.line = self.line + 1
            elif ch == ' ':  pass
            elif ch == '\t': pass
            elif ch == '\r': pass
            
            # comments
            elif ch == '#':
                # comsume char till new line
                # TODO: if the last line is a comment, might have problem
                while self.peak() != '\n': 
                    self.advance()  

            # normal one char tokens
            elif ch == '+': self.add_token(TOK_PLUS)
            elif ch == '-': self.add_token(TOK_MINUS)
            elif ch == '*': self.add_token(TOK_STAR)
            elif ch == '/': self.add_token(TOK_SLASH)
            elif ch == '^': self.add_token(TOK_CARET)
            elif ch == '%': self.add_token(TOK_MOD)
            elif ch == ';': self.add_token(TOK_SEMICOLON)
            elif ch == '?': self.add_token(TOK_QUESTION)
            elif ch == '(': self.add_token(TOK_LPAREN)
            elif ch == ')': self.add_token(TOK_RPAREN)
            elif ch == '{': self.add_token(TOK_LCURLY)
            elif ch == '}': self.add_token(TOK_RCURLY)
            elif ch == '[': self.add_token(TOK_LSQUAR)
            elif ch == ']': self.add_token(TOK_LSQUAR)
            elif ch == ',': self.add_token(TOK_COMMA)
            elif ch == '.': self.add_token(TOK_DOT)
            
            # potentialy two char tokens
            # '~': not  '~=': not equal
            elif ch == '~': 
                if self.match('='):   # not equal, next char is '='
                    self.add_token(TOK_NE)
                else:
                    self.add_token(TOK_NOT) 
            # <, <=
            elif ch == '<':
                if self.match('='):   # less equal, next char is '='
                    self.add_token(TOK_LE)
                else:
                    self.add_token(TOK_LT) 

            # >, >=
            elif ch == '>':
                if self.match('='):   # great equal, next char is '='
                    self.add_token(TOK_GE)
                else:
                    self.add_token(TOK_GT)

            # :, :=
            elif ch == ':':
                if self.match(':'):   # assign, next char is '='
                    self.add_token(TOK_COLON)
                else:
                    self.add_token(TOK_ASSIGN)

        return self.tokens
