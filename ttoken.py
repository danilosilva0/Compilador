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
    NUM = 15
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
            15: "num",
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
            32: "erro"
        }
        return nomes[token]
    
    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'if': TOKEN.IF,
            'while': TOKEN.WHILE,
            'begin': TOKEN.BEGIN,
            'then': TOKEN.THEN,
            'end': TOKEN.END,
            'else': TOKEN.ELSE,
            'read': TOKEN.READ,
            'write': TOKEN.WRITE,
            'and': TOKEN.AND,
            'or': TOKEN.OR,
            'not': TOKEN.NOT
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.IDENT