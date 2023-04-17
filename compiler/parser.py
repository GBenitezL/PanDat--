from compiler.lexer import LexerClass
from sly import Parser

class ParserClass(Parser):
    tokens = LexerClass.tokens

    @_('PROGRAM ID SEMI program_2',
       'PROGRAM ID SEMI vars program_2')
    def program(self, p):
        return 'ok'

    @_('function program_2',
       'main_block')
    def program_2(self, p):
        pass

    @_('MAIN LPAREN RPAREN block',
       'MAIN LPAREN RPAREN vars block')
    def main_block(self, p):
        pass

    @_('LBRACE statements RBRACE',
       'LBRACE RBRACE')
    def block(self, p):
        pass

    @_('vars_2')
    def vars(self, p):
        pass

    @_('VAR vars_3 vars_2',
       'VAR vars_3')
    def vars_2(self, p):
        pass

    @_('ID COLON type SEMI',
       'ID COMMA vars_3')
    def vars_3(self, p):
        pass

    @_('INT array',
       'FLOAT array',
       'CHAR array',
       'BOOL array')
    def type(self, p):
        pass

    @_('LBRACKET CTEI RBRACKET',
       'epsilon')
    def array(self, p):
        pass

    @_('FUNCTION ID COLON return_type LPAREN params RPAREN block',
       'FUNCTION ID COLON return_type LPAREN params RPAREN vars block',
       'FUNCTION ID COLON return_type LPAREN RPAREN block',
       'FUNCTION ID COLON return_type LPAREN RPAREN vars block')
    def function(self, p):
        pass

    @_('VOID',
       'type')
    def return_type(self, p):
        pass

    @_('ID COLON type COMMA params',
       'ID COLON type')
    def params(self, p):
        pass

    @_('ID LPAREN RPAREN',
       'ID LPAREN function_params RPAREN')
    def function_call_return(self, p):
        pass

    @_('ID LPAREN RPAREN SEMI',
       'ID LPAREN function_params RPAREN SEMI')
    def function_call_void(self, p):
        pass

    @_('expression',
       'expression COMMA function_params')
    def function_params(self, p):
        pass

    @_('RETURN expression SEMI')
    def return_stmt(self, p):
        pass

    @_('assignment statements_2',
       'condition statements_2',
       'write statements_2',
       'read statements_2',
       'loop statements_2',
       'return_stmt statements_2',
       'function_call_void statements_2',
       'plot statements_2')
    def statements(self, p):
        pass

    @_('sum',
        'mean',
        'median',
        'variance',
        'std',
        'rand',
        'corr')
    def statistics(self, p):
        pass

    @_('statements',
       'epsilon')
    def statements_2(self, p):
        pass

    @_('ID EQUALS expression SEMI',
       'ID LBRACKET expression RBRACKET EQUALS expression SEMI')
    def assignment(self, p):
        pass

    @_('IF LPAREN expression RPAREN block',
       'IF LPAREN expression RPAREN block ELSE block')
    def condition(self, p):
        pass

    @_('exp',
       'comparison',
       'logical')
    def expression(self, p):
        pass

    @_('exp LT exp',
       'exp LE exp',
       'exp GT exp',
       'exp GE exp',
       'exp EQ exp',
       'exp NE exp')
    def comparison(self, p):
        pass

    @_('expression AND expression',
       'expression OR expression')
    def logical(self, p):
        pass

    @_('term',
       'term exp_2')
    def exp(self, p):
        pass

    @_('PLUS exp',
       'MINUS exp')
    def exp_2(self, p):
        pass

    @_('factor',
       'factor term_2')
    def term(self, p):
        pass

    @_('TIMES term',
       'DIVIDE term')
    def term_2(self, p):
        pass

    @_('LPAREN expression RPAREN',
       'ID LBRACKET expression RBRACKET',
       'function_call_return',
       'factor_2',
       'statistics')
    def factor(self, p):
        pass

    @_('PLUS constant',
       'MINUS constant',
       'constant')
    def factor_2(self, p):
        pass

    @_('ID',
       'CTEI',
       'CTEF',
       'CTEC',
       'TRUE',
       'FALSE')
    def constant(self, p):
        pass
    
    @_('for_loop',
       'while_loop')
    def loop(self, p):
        pass

    @_('WHILE LPAREN expression RPAREN block')
    def while_loop(self, p):
        pass

    @_('FOR LPAREN ID EQUALS expression SEMI expression SEMI expression RPAREN block')
    def for_loop(self, p):
        pass

    @_('PRINT LPAREN write_2 RPAREN SEMI')
    def write(self, p):
        pass

    @_('expression COMMA',
       'expression',
       'CTESTRING COMMA',
       'CTESTRING')
    def write_2(self, p):
        pass

    # @_('expression COMMA',
    #    'expression',
    #    'CTESTRING COMMA',
    #    'CTESTRING')
    # def write_2_multiple(self, p):
    #     pass

    @_('READ LPAREN read_2 RPAREN SEMI')
    def read(self, p):
        pass

    @_('ID',
       'ID LBRACKET expression RBRACKET')
    def read_2(self, p):
        pass
    
    @_('SUM LPAREN ID RPAREN')
    def sum(self, p):
        pass

    @_('MEAN LPAREN ID RPAREN')
    def mean(self, p):
        pass

    @_('MEDIAN LPAREN ID RPAREN')
    def median(self, p):
        pass

    @_('VARIANCE LPAREN ID RPAREN')
    def variance(self, p):
        pass

    @_('STD LPAREN ID RPAREN')
    def std(self, p):
        pass

    @_('RAND LPAREN CTEI COMMA CTEI RPAREN')
    def rand(self, p):
        pass

    @_('CORR LPAREN ID COMMA ID RPAREN SEMI')
    def corr(self, p):
        pass
    
    @_('PLOT LPAREN ID COMMA ID COMMA CTESTRING RPAREN SEMI',
       'PLOT LPAREN ID COMMA CTESTRING')
    def plot(self, p):
        pass

    @_('')
    def epsilon(self, p):
        return None
    
    def error(self, token):
        if token:
            print(f"Syntax error at token {token.type} ({token.value}) on line {token.lineno}")
        else:
            print("Syntax error at end of input")
