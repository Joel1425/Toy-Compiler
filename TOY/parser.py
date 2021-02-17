from rply import ParserGenerator
from ast import *

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE', 'CLOSE_BRACE', 'IF', 'ELSE',
             'SEMI_COLON', 'SUM', 'SUB', 'MUL', 'DIV', 'MOD', 'AND', 'OR',
             'TRUE', 'FALSE', 'INT', 'ID', 'EQ']
        )
        self.module = module
        self.builder = builder
        self.printf = printf
       

    def parse(self):
        global variable
        @self.pg.production('program : statements')
        def program(p):
            return Program(self.builder, self.module, p[0])

        @self.pg.production('statements : statements statement')
        @self.pg.production('statements : statement')
        def statements(p):
            return Statements(self.builder, self.module, p)
       

        @self.pg.production('statement : expression SEMI_COLON')
        def statement(p):
            return Expression(p[0])

        @self.pg.production('statement : IF expression OPEN_BRACE expression CLOSE_BRACE ELSE OPEN_BRACE expression CLOSE_BRACE')
        def if_stmt(p):
            if int(p[1].value) != 0:
                print(p[3])
                return p[3]
            else :
                print(p[7])
                return p[7]

        @self.pg.production('statement : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def statement(p):
            return Print(self.builder, self.module, self.printf, p[2])


        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        @self.pg.production('expression : expression MOD expression')
        @self.pg.production('expression : expression AND expression')
        @self.pg.production('expression : expression OR expression')
        @self.pg.production('expression : TRUE')
        @self.pg.production('expression : FALSE')
        def expression(p):

            if len(p)==1 and p[0].gettokentype() != 'ID':
                if p[0].gettokentype()=='TRUE':
                    return TRUE(self.builder, self.module, 1)
                elif p[0].gettokentype()=='FALSE':
                    return FALSE(self.builder, self.module, 0)
            elif len(p) > 1:
                left = p[0]
                right = p[2]
                operator = p[1]
                if operator.gettokentype() == 'SUM':
                    return Sum(self.builder, self.module, left, right)
                elif operator.gettokentype() == 'SUB':
                    return Sub(self.builder, self.module, left, right)
                elif operator.gettokentype() == 'MUL':
                    return Mul(self.builder, self.module, left, right)
                elif operator.gettokentype() == 'DIV':
                    return Div(self.builder, self.module, left, right)
                elif operator.gettokentype() == 'MOD':
                    return Mod(self.builder, self.module, left, right)
                elif operator.gettokentype() == 'AND':
                    return And(self.builder, self.module, left, right)
                elif operator.gettokentype() == 'OR':
                    return Or(self.builder, self.module, left, right)