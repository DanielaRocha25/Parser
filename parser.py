from ply.lex import lex
from ply.yacc import yacc
import sys

print("Parser de lingugem inventada")
print("-"*30)
# Palavras reservadas
reservadas = {
    'if': 'IF',
    'while': 'WHILE'
}
#Definição dos tokens
tokens = ['FINAL', 'IGUAL','ADD', 'SUB', 'MUL', 'DIV', 'LPAR', 'RPAR', 'NUM', 'ID', 'MAIOR', 'MENOR', 'MAIORIG', 'MENORIG', 'DIF',
             'IGUAL2', 'DOISPONTOS'
         ] + list(reservadas.values())

t_FINAL = r';'
t_IGUAL = r'='
t_ADD = r'\+'
t_SUB = r'-'
t_LPAR = r'\('
t_RPAR = r'\)'
t_IGUAL2 = r'=='
t_DIF = r'!='
t_MENOR = r'<'
t_MENORIG = r'<='
t_MAIOR = r'>'
t_MAIORIG = r'>='
t_DOISPONTOS =r':'

#Definição do token ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t
#Definição do token Numero
def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    # Se houver um caracter inválido retorna essa informação, senão sai do programa.
    if t is not None:
        print("Erro léxico: Caracter inválido: '{}'".format(t.value[0]))
        t.lexer.skip(1)
        sys.exit()

class Programa:
    def __init__(self, program):
        self.program = program

    def __repr__(self):
        return repr(self.program)


class Bloco:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        result = repr(self.statements[0])
        for st in self.statements[1:]:
            result += '; ' + repr(st)
        return result


class If:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then

    def __repr__(self):
        return 'if ' + '('+ repr(self.condition) + ':' + \
               repr(self.then) + ')'+ 'FINAL'


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'while ' + repr(self.condition) + ':' + \
               repr(self.body) + ' FINAL'


class Atribuicao:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return repr(self.identifier) + '=' + repr(self.expression)

class Comparacao:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return repr(self.left) + self.op + repr(self.right)


class Expressao:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return '(' + repr(self.left) + self.op + repr(self.right) + ')'

class Numero:
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return self.number

class Identificador:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return self.identifier

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV')
)

def p_programa(p):
    'Programa : Statements'
    p[0] = Programa(p[1])


def p_statements_statement(p):
    'Statements : Statement'
    p[0] = Bloco([p[1]])


def p_statements_statements(p):
    'Statements : Statements FINAL Statement'
    sts = p[1].statements
    sts.appFINAL(p[3])
    p[0] = Bloco(sts)


def p_statement(p):
    '''Statement : If
                 | While
                 | Assignment'''
    p[0] = p[1]


def p_if(p):
    '''If : IF LPAR Relation RPAR DOISPONTOS Statements FINAL'''
    p[0] = If(p[2], p[4])


def p_while(p):
    '''While : WHILE Comparison DOISPONTOS Statements FINAL'''
    p[0] = While(p[2], p[4])


def p_assignment(p):
    'Assignment : Id IGUAL Expression'
    p[0] = Atribuicao(p[1], p[3])


def p_comparison(p):
    '''Comparison : Expression Relation Expression
                | NUM Relation NUM
                | NUM Relation Expression
                | Expression Relation NUM'''
    p[0] = Comparacao(p[1], p[2], p[3])


def p_relation(p):
    '''Relation : MAIOR
                | MENOR
                | MAIORIG
                | MENORIG
                | IGUAL2
                | DIF '''
    p[0] = p[1]

def p_expression_binary(p):
    '''Expression : Expression ADD Expression
                  | Expression SUB Expression
                  | Expression MUL Expression
                  | Expression DIV Expression
                  | Expression ADD NUM
                  | Expression SUB NUM
                  | Expression MUL NUM
                  | Expression DIV NUM
                  | NUM ADD Expression
                  | NUM SUB Expression
                  | NUM MUL Expression
                  | NUM DIV Expression
                  | NUM ADD NUM
                  | NUM SUB NUM
                  | NUM MUL NUM
                  | NUM DIV NUM
                  '''
    p[0] = Expressao(p[1], p[2], p[3])


def p_expression_parenthesis(p):
    'Expression : LPAR Expression RPAR'
    p[0] = p[2]


def p_expression_num(p):
    'Expression : NUM'
    p[0] = Numero(p[1])


def p_expression_id(p):
    'Expression : Id'
    p[0] = p[1]

def p_id(p):
    'Id : ID'
    p[0] = Identificador(p[1])


def p_error(p):
    if p is not None:
        print("Erro de sintaxe: ", p)
        sys.exit()


scanner = lex()
teste = scanner.input('''
x=2;
y=3;
IF x>y: x=2;
''')
print("Tokens:")
for tok in scanner:
    print(tok)

print("-"*30)
parser = yacc()
ast = parser.parse(teste, lexer=scanner)

print("Resultado: O código é válido!")
