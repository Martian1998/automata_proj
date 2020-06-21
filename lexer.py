import ply.lex as lex 
import sys


tokens = [
    'WORD',
    'INTNAME',
    'STRINGNAME',
    'CHARNAME',
    'DOUBLENAME',
    'BOOLNAME',
    'INT',
    'DOUBLE',
    'CHAR',
    'STRING',
    'BOOL',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQ',
    'EQUALS',
    'NE',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'NOT',
    'AND',
    'OR',
    'INC',
    'DEC',
    'MODULUS',
    'EXPONENT',
    'LPAREN',
    'RPAREN',
    'PRINT',
    'DELIM',
    'IF',
    'ELSEIF',
    'ELSE',
    'LCURLY',
    'RCURLY',
    'SEMICOLON',
    'STRUCT',
    'DOT'
]

t_EQ = r'=='
t_DELIM = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_INC = r'\+\+'
t_DEC = r'--'
t_MODULUS = r'%'
t_EXPONENT = r'\^'

t_ignore = r' '

def t_DOT(t):
    r'\.'
    return t

def t_STRUCT(t):
    r'STRUCT'
    return t

def t_SEMICOLON(t):
    r';'
    return t

def t_IF(t):
    r'IF'
    return t

def t_ELSEIF(t):
    r'ELSEIF'
    return t

def t_ELSE(t):
    r'ELSE'
    return t
 
def t_LCURLY(t):
    r'{'
    return t


def t_RCURLY(t):
    r'}'
    return t


def t_INTNAME(t):
    r'INT'
    return t

def t_CHARNAME(t):
    r'CHAR'
    return t

def t_DOUBLENAME(t):
    r'DOUBLE'
    return t

def t_STRINGNAME(t):
    r'STRING'
    return t

def t_BOOLNAME(t):
    r'BOOL'
    return t


def t_PRINT(t):
    r'PRINT'
    return t

def t_AND(t):
    r'AND'
    return t

def t_OR(t):
    r'OR'
    return t

def t_NOT(t):
    r'NOT'
    return t

def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'TRUE|FALSE'
    # if t.value == 'TRUE':
    #     t.value = True
    # if t.value == 'FALSE':
    #     t.value = False
    return t

def t_WORD(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'WORD'
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_CHAR(t):
    r'\'.?\''
    t.value = t.value[1:-1]
    return t

def t_error(t):
    print('Illegal Characters!')
    print(t)
    t.lexer.skip(1)

lexer = lex.lex()