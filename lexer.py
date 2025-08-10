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
    def consume(self):
        if self.curr_is_at_end(): return None # bound check
        ch = self.source[self.curr]
        self.curr = self.curr + 1
        return ch

    # Just take a peek at current character (Does not comsumes the char)
    def peek(self):
        if self.curr_is_at_end(): return None # bound check
        return self.source[self.curr]

    # Looks at the next character in the source (Does not comsumes the char)
    def peek_ahead(self, n=1):
        if self.curr_is_at_end(): return None # bound check
        return self.source[self.curr + n]

    # Check if the next char matches the expectation, if true comsume that char
    def match(self, expected):
        if self.curr_is_at_end():
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
    
    # no more char, curr is out
    def curr_is_at_end(self):
        if self.curr >= len(self.source):
            return True
        else:
            return False
        
    def handle_string(self, type):
        while self.peek() != type and not(self.curr_is_at_end()):
            self.consume()
        if not(self.curr_is_at_end()): 
            self.consume()
        else: 
            raise SystemError("Unterminated string")
        self.add_token(TOK_STRING)

    # ---FUNCTIONS---
    def tokenize(self):
        while not(self.curr_is_at_end()):  # There's still token
            self.start = self.curr
            ch = self.consume()
            # special one char tokens
            if   ch == '\n': self.line = self.line + 1
            elif ch == ' ':  pass
            elif ch == '\t': pass
            elif ch == '\r': pass

            # normal one char tokens
            elif ch == '+': self.add_token(TOK_PLUS)
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
            # -- comments
            elif ch == '-':
                # comsume char till new line
                # TODO: if the last line is a comment, might have problem
                if self.peek() == '-':
                    while self.peek() != '\n' and not(self.curr_is_at_end()): 
                        self.consume()  
                else:
                    self.add_token(TOK_MINUS)
            # '~': not  '~=': not equal
            elif ch == '~': 
                if self.match('='):   # not equal, next char is '='
                    self.add_token(TOK_NE)
                else:
                    self.add_token(TOK_NOT) 
            # <, <<, <=
            elif ch == '<':
                if self.match('='):   # less equal, next char is '='
                    self.add_token(TOK_LE)
                elif self.match('<'): # <<
                    self.add_token(TOK_LTLT)
                else:
                    self.add_token(TOK_LT) 

            # >, >>, >=
            elif ch == '>':
                if self.match('='):   # great equal, next char is '='
                    self.add_token(TOK_GE)
                elif self.match('>'): # >>
                    self.add_token(TOK_GTGT)
                else:
                    self.add_token(TOK_GT)

            # :, :=
            elif ch == ':':
                self.add_token(TOK_ASSIGN if self.match('=') else TOK_COLON)

            # numbers
            elif ch.isdigit():
                while not(self.curr_is_at_end()) and self.peek().isdigit(): # The next char id still a digit
                    self.consume()
                
                if self.match('.') and self.peek_ahead().isdigit():  # float
                    while self.peek().isdigit(): # The next char id still a digit
                        self.consume()
                    self.add_token(TOK_FLOAT)
                else:
                    self.add_token(TOK_INTEGER)

            
            # strings
            elif ch == '\'':
                self.handle_string('\'')
            elif ch == '\"':
                self.handle_string('\"')

            elif ch.isalnum() or ch == '_':
                while not(self.curr_is_at_end()) and self.peek().isalnum() or self.peek() == '_':
                    self.consume()
                # check if the identifier match our keyword dict
                identifier_str = self.source[self.start : self.curr]
                keyword_type = keywords.get(identifier_str)
                if keyword_type != None:
                    self.add_token(keyword_type) # is a keyword
                else:
                    self.add_token(TOK_IDENTIFIER)
            else:
                # Nothing matched
                raise SystemError(f'[Line: {self.line}] Error at \'{ch}\', unexpected character')
        return self.tokens
