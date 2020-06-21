import lexer

tokens = lexer.tokens

precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'NE'),
    ('left', 'GTE', 'GT', 'LTE', 'LT'),
    ('left', 'PLUS', 'MINUS'),
    ('right', 'NOT'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'EXPONENT', 'MODULUS'),
)

def p_root(p):
    '''
        root    :   expression
                |   statements
                |   empty
    '''
    p[0] = p[1]

def p_statements(p):
    '''
        statements  :   statements statement SEMICOLON   
                    |   statement SEMICOLON 
                    |   statements if
                    |   if
    '''

    if len(p) == 3:
        if p[2] != ';':
            s  = p[1][1]
            s.append(p[2])
            p[0] = ('statements', s)
        else:
            p[0] = ('statements', [p[1]])
    elif len(p) == 2:
        p[0] = ('statements',[p[1]])
    else:
        s  = p[1][1]
        s.append(p[2])
        p[0] = ('statements', s)


def p_if_statement(p):
    '''
        if   :   IF LPAREN expression RPAREN LCURLY statements RCURLY elseif else   
    '''
    p[0] = ('if',p[3],p[6],p[8],p[9])

def p_else_if_statement(p):
    '''
        elseif  :   ELSEIF LPAREN expression RPAREN LCURLY statements RCURLY elseif else
                |   empty
    '''
    if len(p) < 10:
        p[0] = None
    else:
        p[0] = ('elseif', p[3],p[6],p[8],p[9])
    

def p_else_statement(p):
    '''
        else    :   ELSE LCURLY statements RCURLY
                |   empty
    '''
    if len(p) < 5:
        p[0] = None
    else:
        p[0] = ('else', p[3])




def p_struct_update(p):
    '''
        statement   :   WORD DOT WORD EQUALS expression
    '''
    p[0] = ('struct_update', p[1], p[3], p[5])

def p_print(p):
    '''
        statement  : PRINT LPAREN print_list RPAREN
    '''
    p[0] = ('print', p[3])

def p_print_list_second(p):
    '''
        print_list  : print_list DELIM expression
    '''
    l = p[1]
    l.append(p[3])
    p[0] = l

def p_print_list_first(p):
    '''
        print_list  : expression
    '''
    p[0] = [p[1]] 



def p_struct_dec(p):
    '''
        statement   :   WORD WORD
    '''
    p[0] = ('struct_dec', p[1], p[2])

def p_struct_def(p):
    '''
        statement   :   STRUCT WORD LCURLY var_decls RCURLY
    '''
    p[0] = ('struct_def', p[2], p[4])

def p_var_decls(p):
    '''
        var_decls   :   var_decls var_declare
                    |   var_declare
    '''
    if len(p) < 3:
        p[0] = [p[1]]
    else:
        v = p[1]
        v.append(p[2])
        p[0] = v



def p_statement(p):
    '''
        statement   :   var_declare
                    |   var_assign
    ''' 
   
    p[0] = p[1]



def p_paren(p):
    '''
        expression   :   LPAREN expression RPAREN
    '''

    p[0] = p[2]

def p_var_assign(p):
    '''
        var_assign  : var_declare EQUALS expression
                    | WORD EQUALS expression
    '''
    if type(p[1]) != tuple:
        p[0] = ('var_update', p[1], p[3])
    else:
        p[0] = ('var_assign', p[1][1], p[1][2], p[3])



def p_var_declare(p):
    '''
        var_declare :   INTNAME WORD 
                    |   DOUBLENAME WORD 
                    |   CHARNAME WORD 
                    |   STRINGNAME WORD 
                    |   BOOLNAME WORD 
    '''
    p[0] = ('var_declare', p[1], p[2])

def p_binop(p):
    '''
        expression  :   expression MULTIPLY expression
                    |   expression DIVIDE expression
                    |   expression PLUS expression
                    |   expression MINUS expression
                    |   expression EXPONENT expression
                    |   expression MODULUS expression
                    |   expression AND expression
                    |   expression OR expression
                    |   expression EQ expression
                    |   expression NE expression
                    |   expression LTE expression   
                    |   expression GTE expression   
                    |   expression GT expression   
                    |   expression LT expression   
    '''
    p[0] = (p[2], p[1], p[3])

def p_binop_single(p):
    '''
        expression  :   PLUS expression
                    |   MINUS expression 
    '''
    p[0] = (p[1], 0, p[2])


def p_unop(p):
    '''
        statement   :   expression INC
                    |   expression DEC
    '''
    p[0] = (p[2], p[1])


def p_not(p):
    '''
        expression  :   NOT expression
    '''
    p[0] = (p[1], p[2])


def p_expression_var(p):
    '''
        expression : WORD
    '''
    p[0] = ('var',p[1])

def p_expression(p):
    '''
        expression  :   INT
                    |   DOUBLE
                    |   CHAR
                    |   STRING
                    |   BOOL
    '''
    p[0] = p[1]






# def p_data(p):
#     '''
#         data    :   INT
#                 |   DOUBLE
#                 |   CHAR
#                 |   STRING
#                 |   BOOL
#     '''
#     p[0] = p[1]

# def p_data_var(p):
#     '''
#         data    :   WORD
#     '''
#     p[0] = ('var',p[1])
    
def p_struct_access(p):
    '''
        expression   :   WORD DOT WORD
    '''
    p[0] = ('struct_access', p[1], p[3])
    


def p_error(p):
    print("Syntax Error! ",p)

def p_empty(p):
    '''
    empty : 
    '''
    p[0] = None
