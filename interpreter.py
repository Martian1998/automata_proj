import ply.yacc as yacc
import parser
import sys
from copy import deepcopy


yaplParser = yacc.yacc(module=parser)

env = {}


#FALSE == FALSE AND TRUE

#add compatibility with vars
def eval_binary(p, env):
    if type(p[1]) == tuple:
        l, env = execute(p[1], env)
        p = (p[0], l, p[2])

    if type(p[2]) == tuple:
        r,env = execute(p[2], env)
        p = (p[0], p[1], r)

    if type(p[1]) == str and type(p[2]) == int:
        print("TYPE ERROR")
        sys.exit()
        return (None, env)

    if type(p[2]) == str and type(p[1]) == int:
        print("TYPE ERROR")
        sys.exit()
        return (None, env)

    if p[0] == '+':
        return p[1] + p[2], env
    elif p[0] == '-':
        return p[1] - p[2], env
    elif p[0] == '/':
        if p[2] == 0:
            print('Division by zero error!')
            sys.exit()
            return (None, env)
        return p[1]/p[2], env
    elif p[0] == '*':
        return p[1] * p[2], env
    elif p[0] == '^':
        return p[1] ** p[2], env
    elif p[0] == '%':
        return p[1] % p[2], env
    elif p[0] == 'AND':
        return p[1] and p[2], env
    elif p[0] == 'OR':
        return p[1] or p[2], env
    elif p[0] == '<':
        return p[1] < p[2], env
    elif p[0] == '>':
        return p[1] > p[2], env
    elif p[0] == '>=':
        return p[1] >= p[2], env
    elif p[0] == '<=':
        return p[1] <= p[2], env
    elif p[0] == '!=':
        return p[1] != p[2], env
    elif p[0] == '==':
        return p[1] == p[2], env
    
#add compatibility with vars
def eval_unary(p, env):
    if p[0] == '++':
        res = execute(p[1], env)[0]
        if type(res) != int:
            print("Type Error: Can't increment.")
            sys.exit()
            return (None, env)
        if type(p[1]) != tuple:
            print("Type Error: Can't increment.")
            sys.exit()
            return (None, env)
        if p[1][0]!='var':
            print("Type Error: Can't increment > not a variable.")
            sys.exit()
            return (None, env)
        if p[1][1] in  env.keys():
            if env[p[1][1]][0] == 'INT':
                env[p[1][1]] = ('INT', env[p[1][1]][1] + 1) 
            else:
                print('CAN\'T DECREMENT NON INT TYPE! :(')
        else:
            print('Undeclared Variable :(')
        return None,env
    elif p[0] == '--':
        res = execute(p[1], env)[0]
        if type(res) != int:
            print("Type Error: Can't increment.")
            sys.exit()
            return (None, env)
        if type(p[1]) != tuple:
            print("Type Error: Can't increment.")
            sys.exit()
            return (None, env)
        if p[1][0]!='var':
            print("Type Error: Can't increment > not a variable.")
            sys.exit()
            return (None, env)
        if p[1][1] in  env.keys():
            if env[p[1][1]][0] == 'INT':
                env[p[1][1]] = ('INT', env[p[1][1]][1] + 1) 
            else:
                print('CAN\'T DECREMENT NON INT TYPE! :(')
        else:
            print('Undeclared Variable :(')
        return None, env
    elif p[0] == 'NOT':
        return not p[1],env

def execute(p,env):
    old_env = deepcopy(env)
    if type(p) == tuple:
        if p[0] == 'print':
            for i in range(len(p[1])):
                val, env = execute(p[1][i],env)
                if val == False and type(val) == bool:
                    val = 'FALSE'
                elif val == True and type(val) == bool:
                    val = 'TRUE'

                if i == len(p[1]) - 1:
                    print(val, end = '\n')
                else:
                    print(val, end = ' ')
            return None,env
        elif p[0] == 'statements':
            for i in p[1]:
                _,env = execute(i, env)
            return None,env

        elif p[0] == 'struct_update':
            if p[1] in env.keys():
                if env[p[1]][0] == 'struct_dec':
                    if p[2] in  env[p[1]][1].keys():
                        org_type = env[p[1]][1][p[2]][0]
                        var_value, env = execute(p[3], env)
                        if type(var_value) == str and org_type=='INT':
                            print('TypeError')
                            sys.exit()
                            return None,env
                        elif type(var_value) == str and org_type=='DOUBLE':
                            print('TypeError')
                            sys.exit()
                            return None,env
                        elif type(var_value) != str and org_type=='STRING':
                            print('TypeError')
                            sys.exit()
                            return None,env
                        if org_type=='BOOL' and var_value!='TRUE' and var_value!='FALSE':
                            var_value = bool(var_value)
                            if var_value:
                                var_value = 'TRUE'
                            else:
                                var_value = 'FALSE'
                    
                        if org_type=='DOUBLE':
                            var_value = float(var_value)
                        if org_type=='INT':
                            var_value = int(var_value)
                    
                        env[p[1]][1][p[2]] = (org_type,var_value)
                        return None,env

                    else:
                        print("NO SUCH VARIABLE IN THIS STRUCT")
                        sys.exit()
                else:
                    print("NO SUCH STRUCT DECLARED!")
                    sys.exit()
                    return None,env
            else:
                print("NO SUCH STRUCT OR VARIABLE DECLARED!")
                sys.exit()
        
        elif p[0] == 'struct_access':
            
            if p[1] in env.keys():
                if env[p[1]][0] != 'struct_dec':
                    print('NO SUCH STRUCT AVAILABLE!')
                    sys.exit()
                if p[2] in env[p[1]][1].keys():
                    return env[p[1]][1][p[2]][1],env
                else:
                    print('NO SUCH VARIABLE IN STRUCT!')
                    sys.exit()
                    return None,env
            else:
                print('NO SUCH STRUCT INITIALIZED!')
                sys.exit()
                return  None,env

        elif p[0] == 'struct_dec':
            if p[1] in  env.keys():
                if env[p[1]][0] == 'struct_def':
                    n = deepcopy(env[p[1]])
                    n = ('struct_dec', n[1])
                    env[p[2]] = n
                    return None,env   

                else:
                    print("Error ---->  NO Such Struct Defined!")
                    sys.exit()
                    return None,env
            else:
                print("Error  ----->  NO Such Variable or Struct Defined!")
                sys.exit()
                return None,env
        elif p[0] == 'struct_def':
            env[p[1]] = ('struct_def', {})
            for i in  p[2]:
                env[p[1]][1][i[2]] = (i[1], None)
            return None,env

        elif p[0] == 'var':
            if p[1] in env.keys():
                res = env[p[1]]
                if res[0] == 'BOOL':
                    if res[1] == 'TRUE':
                        return True,env
                    else:
                        return False,env
                else:
                    return res[1],env 
            else:
                print("Undeclared Variable")
                sys.exit()
                return None,env

        elif p[0] == 'var_update':
            if p[1] in env.keys():
                var_value,env = execute(p[2], env)
                if type(var_value) == str and env[p[1]][0]=='INT':
                    print('TypeError')
                    sys.exit()
                    return None,env
                elif type(var_value) == str and env[p[1]][0]=='DOUBLE':
                    print('TypeError')
                    sys.exit()
                    return None,env
                elif type(var_value) != str and env[p[1]][0]=='STRING':
                    print('TypeError')
                    sys.exit()
                    return (None, env)
                if env[p[1]][0]=='BOOL' and var_value!='TRUE' and var_value!='FALSE':
                    var_value = bool(var_value)
                    if var_value:
                        var_value = 'TRUE'
                    else:
                        var_value = 'FALSE'

                if env[p[1]][0]=='DOUBLE':
                    var_value = float(var_value)
                if env[p[1]][0]=='INT':
                    var_value = int(var_value)

                env[p[1]] = (env[p[1]][0], var_value)
                return None,env
            else:
                print("Variable Undeclared")
                sys.exit()

        elif p[0] == 'var_declare':
            if p[2] not in env.keys():
                env[p[2]] = (p[1], None)
                return None,env
            else:
                print("Redeclaration Error!")
                sys.exit()
                return None,env

        elif p[0] == 'var_assign':
            if p[2] not in env.keys():
                var_value,env = execute(p[3], env)
                if type(var_value) == str and p[1]=='INT':
                    print('TypeError')
                    sys.exit()
                    return None,env
                elif type(var_value) == str and p[1]=='DOUBLE':
                    print('TypeError')
                    sys.exit()
                    return None,env
                elif type(var_value) != str and p[1]=='STRING':
                    print('TypeError')
                    sys.exit()
                    return None,env
                if p[1]=='BOOL' and var_value!='TRUE' and var_value!='FALSE':
                    var_value = bool(var_value)
                    if var_value:
                        var_value = 'TRUE'
                    else:
                        var_value = 'FALSE'
                
                if p[1]=='DOUBLE':
                    var_value = float(var_value)
                if p[1]=='INT':
                    var_value = int(var_value)

                env[p[2]] = (p[1], var_value)
                return None,env
            else:
                print("Redeclaration Error!")
                sys.exit()
                return None,env
        elif p[0] == 'if':
            rest =execute(p[1],env)[0]
            if rest:
                return execute(p[2],env),old_env
            elif p[3]:
                return execute(p[3], env), old_env
            elif p[4]:
                return execute(p[4],env), old_env
            else:
                return None,old_env
        elif p[0] == 'elseif':
            if execute(p[1], env)[0]:
                return execute(p[2],env), old_env
            elif p[3]:
                return execute(p[3],env), old_env
            elif p[4]:
                return execute(p[4],env), old_env
            else:
                return None, old_env
        elif p[0] == 'else':
            return execute(p[1], env), old_env
        elif len(p) == 2:
            if p[1] == 'TRUE':
                p = (p[0], True)
            elif p[1] == 'FALSE':
                p = (p[0], False)
            res, env = eval_unary(p, env)
            return res, env

        elif len(p) == 3:
            if p[1] == 'TRUE':
                p = (p[0], True, p[2])
            elif p[1] == 'FALSE':
                p = (p[0], False, p[2])

            if p[2] == 'TRUE':
                p = (p[0], p[1], True)
            elif p[2] == 'FALSE':
                p = (p[0], p[1], False)

            res,env =  eval_binary(p, env)
            return res, env
    else:
        return p, env






# toaLexer.input(code)

def main():
    # while True:
    #     try:
    #         inp = input(">>>  ")
    #     except EOFError:
    #         break
    if len(sys.argv)!=2:
        print('Kindly use proper format for using interpreter.py! :)')
        return
    file = sys.argv[1]
    f = open(file, 'r')
    code = f.read()
    code  = code.replace('\n','')
    env = {}
    inp = yaplParser.parse(code)
    print('Welcome to the MyYAPL Interpreter!')
    print('Output:')
    execute(inp,env)

main()