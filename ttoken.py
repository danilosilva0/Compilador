from enum import IntEnum

class TOKEN (IntEnum):
    BEGIN = 1  
    END = 2
    IDENT = 3
    ATRIBUICAO = 4
    PONTO_VIRGULA = 5
    IF = 6
    ABRE_PARENTESES = 7
    FECHA_PARENTESES = 8
    THEN = 9  
    ELSE = 10  
    READ = 11
    STRING = 12 
    VIRGULA = 13
    WRITE = 14
    INT = 15 
    ABRE_CHAVES = 16
    FECHA_CHAVES = 17
    OR = 18
    AND = 19
    NOT = 20
    IGUAL = 21
    MENOR = 22
    MAIOR = 23
    MENOR_IGUAL = 24
    MAIOR_IGUAL = 25
    DIFERENTE = 26
    SOMA = 27
    SUBTRACAO = 28
    DIVISAO = 29
    MULTIPLICACAO = 30
    EOF = 31
    ERRO = 32
    FUNCTION = 33
    DOIS_PONTOS = 34
    FLOAT = 35 
    ABRE_COLCHETES = 36
    FECHA_COLCHETES = 37
    LIST = 38
    RETURN = 39 
    WHILE = 40
    FOR = 41
    IN = 42
    DO = 43 
    RANGE = 44
    INTVAL = 45
    FLOATVAL = 46
    STRVAL = 47
    MOD = 48 
    SETA = 49

    @classmethod
    def msg(cls, token):
        nomes = {
            1: "begin",
            2: "end",
            3: "ident",
            4: "=",
            5: ";",
            6: "if",
            7: "(",
            8: ")",
            9: "then",
            10: "else",
            11: "read",
            12: "string",
            13: ",",
            14: "write",
            15: "int",
            16: "{",
            17: "}",
            18: "or",
            19: "and",
            20: "not",
            21: "==",
            22: "<",
            23: ">",
            24: "<=",
            25: ">=",
            26: "!=",
            27: "+",
            28: "-",
            29: "/",
            30: "*",
            31: "<eof>",
            32: "erro",
            33: "function",
            34: ":",
            35: "float",
            36: "[",
            37: "]",
            38: "list",
            39: "return ",
            40: "while",
            41: "for",
            42: "in",
            43: "do",
            44: "range",
            45: "intVal",
            46: "floatVal",
            47: "strVal",
            48: "%",
            49: "->"

        }
        return nomes[token]
    
    @classmethod
    def oprel(cls):
        return [
            TOKEN.IGUAL,
            TOKEN.MAIOR,
            TOKEN.MENOR,
            TOKEN.MAIOR_IGUAL,
            TOKEN.MENOR_IGUAL,
            TOKEN.DIFERENTE
            ]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'if': TOKEN.IF,
            'begin': TOKEN.BEGIN,
            'then': TOKEN.THEN,
            'end': TOKEN.END,
            'else': TOKEN.ELSE,
            'read': TOKEN.READ,
            'string': TOKEN.STRING,
            'write': TOKEN.WRITE,
            'and': TOKEN.AND,
            'or': TOKEN.OR,
            'not': TOKEN.NOT,
            'int': TOKEN.INT,
            'function': TOKEN.FUNCTION,            
            'float': TOKEN.FLOAT,
            'list': TOKEN.LIST,
            'return': TOKEN.RETURN,
            'while': TOKEN.WHILE,
            'for': TOKEN.FOR,
            'in': TOKEN.IN,
            'do': TOKEN.DO,
            'range': TOKEN.RANGE,
            'intVal': TOKEN.INTVAL,
            'floatVal': TOKEN.FLOATVAL,
            'strVal': TOKEN.STRVAL,
            
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.IDENT
        
    @classmethod
    def tabelaOperacoes(cls):
        return {
            # operações aritméticas
            frozenset({(TOKEN.TINT, False), TOKEN.mais, (TOKEN.TINT, False)}): (TOKEN.TINT, False),
            frozenset({(TOKEN.TINT, False), TOKEN.menos, (TOKEN.TINT, False)}): (TOKEN.TINT, False),
            frozenset({(TOKEN.TINT, False), TOKEN.multiplica, (TOKEN.TINT, False)}): (TOKEN.TINT, False),
            frozenset({(TOKEN.TINT, False), TOKEN.divide, (TOKEN.TINT, False)}): (TOKEN.TFLOAT, False),
            frozenset({(TOKEN.TINT, False), TOKEN.mod, (TOKEN.TINT, False)}): (TOKEN.TINT, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.mais, (TOKEN.TFLOAT, False)}): (TOKEN.TFLOAT, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.mais, (TOKEN.TINT, False)}): (TOKEN.TFLOAT, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.multiplica, (TOKEN.TINT, False)}): (TOKEN.TFLOAT, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.divide, (TOKEN.TINT, False)}): (TOKEN.TFLOAT, False),

            # operações de concatenação
            frozenset({(TOKEN.TSTRING, False), TOKEN.mais, (TOKEN.TSTRING, False)}): (TOKEN.TSTRING, False),
            frozenset({(TOKEN.TSTRING, True), TOKEN.mais, (TOKEN.TSTRING, True)}): (TOKEN.TSTRING, True),
            frozenset({(TOKEN.TINT, True), TOKEN.mais, (TOKEN.TINT, True)}): (TOKEN.TINT, True),
            frozenset({(TOKEN.TFLOAT, True), TOKEN.mais, (TOKEN.TFLOAT, True)}): (TOKEN.TFLOAT, True),
            frozenset({(TOKEN.TBOOLEAN, True), TOKEN.mais, (TOKEN.TBOOLEAN, True)}): (TOKEN.TBOOLEAN, True),
            frozenset({(None, True), TOKEN.mais, (None, True)}): (None, True),
            frozenset({(None, True), TOKEN.mais, (TOKEN.TSTRING, True)}): (None, True),
            frozenset({(None, True), TOKEN.mais, (TOKEN.TINT, True)}): (None, True),
            frozenset({(None, True), TOKEN.mais, (TOKEN.TFLOAT, True)}): (None, True),
            frozenset({(None, True), TOKEN.mais, (TOKEN.TBOOLEAN, True)}): (None, True),

            # operações relacionais
            frozenset({(TOKEN.TINT, False), TOKEN.igual, (TOKEN.TINT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.diferente, (TOKEN.TINT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.menor, (TOKEN.TINT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.menorIgual, (TOKEN.TINT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.maior, (TOKEN.TINT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.maiorIgual, (TOKEN.TINT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.igual, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.diferente, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.menor, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.menorIgual, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.maior, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TFLOAT, False), TOKEN.maiorIgual, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TSTRING, False), TOKEN.igual, (TOKEN.TSTRING, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TSTRING, False), TOKEN.diferente, (TOKEN.TSTRING, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.igual, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.diferente, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.menor, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.menorIgual, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TINT, False), TOKEN.maior, (TOKEN.TFLOAT, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TBOOLEAN, False), TOKEN.igual, (TOKEN.TBOOLEAN, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TBOOLEAN, False), TOKEN.diferente, (TOKEN.TBOOLEAN, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TBOOLEAN, False), TOKEN.AND, (TOKEN.TBOOLEAN, False)}): (TOKEN.TBOOLEAN, False),
            frozenset({(TOKEN.TBOOLEAN, False), TOKEN.OR, (TOKEN.TBOOLEAN, False)}): (TOKEN.TBOOLEAN, False),

            # operações unárias
            frozenset({TOKEN.mais, (TOKEN.TINT, False)}): (TOKEN.TINT, False),
            frozenset({TOKEN.menos, (TOKEN.TINT, False)}): (TOKEN.TINT, False),
            frozenset({TOKEN.mais, (TOKEN.TFLOAT, False)}): (TOKEN.TFLOAT, False),
            frozenset({TOKEN.menos, (TOKEN.TFLOAT, False)}): (TOKEN.TFLOAT, False),
            frozenset({TOKEN.NOT, (TOKEN.TBOOLEAN, False)}): (TOKEN.TBOOLEAN, False),

            # valores hardcoded
            frozenset([(TOKEN.TINT, False)]): (TOKEN.TINT, True),
            frozenset([(TOKEN.TFLOAT, False)]): (TOKEN.TFLOAT, True),
            frozenset([(TOKEN.TSTRING, False)]): (TOKEN.TSTRING, True),
            frozenset([(TOKEN.TINT, False), (TOKEN.TFLOAT, False)]): (TOKEN.TFLOAT, True),

            frozenset({(TOKEN.TSTRING, False), TOKEN.mais, (TOKEN.TSTRING, False)}): (TOKEN.TSTRING, False),
            frozenset({(TOKEN.TSTRING, True), TOKEN.mais, (TOKEN.TSTRING, False)}): (TOKEN.TSTRING, True),
        } 