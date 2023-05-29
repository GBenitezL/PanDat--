from sly import Lexer

class LexerClass(Lexer):
    keywords = {
        'program': 'PROGRAM',
        'var': 'VAR',
        'int': 'INT',
        'float': 'FLOAT',
        'char': 'CHAR',
        'bool': 'BOOL',
        'true': 'TRUE',
        'false': 'FALSE',
        'function': 'FUNCTION',
        'main': 'MAIN',
        'void': 'VOID',
        'return': 'RETURN',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'for': 'FOR',
        'print': 'PRINT',
        'read': 'READ',
        'sum': 'SUM',
        'mean': 'MEAN',
        'median': 'MEDIAN',
        'variance': 'VARIANCE',
        'std': 'STD',
        'iqr': 'IQR',
        'rand': 'RAND',
        'corr': 'CORR',
        'union': 'UNION',
        'diff': 'DIFF',
        'intersect': 'INTERSECT',
        'regression': 'REGRESSION',
        'histplot': 'HISTPLOT',
        'boxplot': 'BOXPLOT',
        'scatterplot': 'SCATTERPLOT',
        'lineplot': 'LINEPLOT',
        'barplot': 'BARPLOT'
    }

    tokens = ['ID', 'CTEF', 'CTEI', 'CTEC', 'CTESTRING', 'COMMA', 'COLON', 'SEMI',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET','LBRACE', 'RBRACE',
    'EQUALS', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'OR', 'AND',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', *keywords.values()]

    ignore = r' \t'
    COMMA = r','
    COLON = r':'
    SEMI = r';'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    EQ = r'=='
    NE = r'!='
    EQUALS = r'='
    OR = r'\|\|'
    AND = r'&&'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    CTESTRING = r'\"(\\.|[^"\\])*\"'
    CTEC = r'\'(.{1})\''

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'[_a-zA-Z][_a-zA-Z0-9]{0,30}')
    def ID(self,t):
        t.type=self.keywords.get(t.value,'ID')
        return t

    @_(r'[0-9]+(\.[0-9]+)')
    def CTEF(self,t):
        try:
            t.value=float(t.value)
        except ValueError:
            print("Lexical Error:", t.value)
            t.value=0
        return t

    @_(r'[0-9]+')
    def CTEI(self,t):
        try:
            t.value=int(t.value)
        except ValueError:
            print("Lexical Error:", t.value)
            t.value=0
        return t

    def error(self, t):
        print(f"Lexer error: Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1
