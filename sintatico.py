from lexico import TOKEN, Lexico

class Sintatico:
    
    def __init__(self, lexico: Lexico):
        self.lexico = lexico

    def traduz(self):
        self.tokenLido = self.lexico.getToken()
        try:
            self.prog()
            print('Traduzido com sucesso.')
        except:
            pass

    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token:
            self.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f'Erro na linha {linha}, coluna {coluna}:')
            if token == TOKEN.ERRO:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f'Era esperado "{msgTokenAtual}" mas veio "{msg}"')
            raise Exception

    def testaLexico(self):
        self.tokenLido = self.lexico.getToken()
        (token, _, _, _) = self.tokenLido
        while token != TOKEN.EOF:
            self.lexico.imprimeToken(self.tokenLido)
            self.tokenLido = self.lexico.getToken()
            (token, _, _, _) = self.tokenLido

#-------- segue a gramatica -----------------------------------------

    # <prog> -> <funcao> <RestoFuncoes>
    def prog(self):
        self.funcao()
        self.restoFuncoes()

    # <calculo> -> LAMBDA | <com><calculo>
    def calculo(self):
        com = [TOKEN.IDENT, TOKEN.IF, TOKEN.READ, TOKEN.WRITE, TOKEN.ABRE_CHAVES]
        entrou = False
        while self.tokenLido[0] in com:
            self.com()
            entrou = True
        
        if not entrou:
            pass 

    # <com> -> <atrib>|<if>|<leitura>|<impressao>|<bloco>
    def com(self):
        if self.tokenLido[0] == TOKEN.IDENT:
            self.atrib()
        elif self.tokenLido[0] == TOKEN.IF:
            self._if_()
        elif self.tokenLido[0] == TOKEN.READ:
            self.leitura()
        elif self.tokenLido[0] == TOKEN.WRITE:
            self.impressao()
        else:
            self.bloco()

    # <atrib> -> ident = <exp> ;
    def atrib(self):
        self.consome(TOKEN.IDENT)
        self.consome(TOKEN.ATRIBUICAO)
        self.exp()
        self.consome(TOKEN.PONTO_VIRGULA)

    # <if> ->  if ( <exp> ) then <com> <else_opc>
    def _if_(self):
        self.consome(TOKEN.IF)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.exp()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.consome(TOKEN.THEN)
        self.com()
        self.else_opc()

    # <else_opc> -> LAMBDA | else <com> 
    def else_opc(self):
        if self.tokenLido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.com()
        else:
            pass

    # <leitura> -> read ( strVal , ident ) ;
    def leitura(self):
        self.consome(TOKEN.READ)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.consome(TOKEN.STRVAL)
        self.consome(TOKEN.VIRGULA)
        self.consome(TOKEN.IDENT)
        self.consome(TOKEN.FECHA_PARENTESES)
        self.consome(TOKEN.PONTO_VIRGULA)

    # <escrita> -> write ( <lista_outs> ) ;
    def escrita(self):
        self.consome(TOKEN.WRITE)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.lista_out()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.consome(TOKEN.PONTO_VIRGULA)

    # <lista_out> -> <out><restoOut>
    def lista_out(self):
        self.out()
        self.restoOut()

    # <restoLista_outs> -> LAMBDA | , <out> <restoLista_outs>
    def restoLista_outs(self):
        if self.tokenLido == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.out()
            self.restoLista_outs()
        else:
            pass
        

    # <out> -> num | ident | string
    def out(self):
        if self.tokenLido[0] == TOKEN.NUMERO:
            self.consome(TOKEN.NUMERO)
        elif self.tokenLido[0] == TOKEN.IDENT:
            self.consome(TOKEN.IDENT)
        else:
            self.consome(TOKEN.STRING)

    # <bloco> -> { <calculo> }
    def bloco(self):
        self.consome(TOKEN.ABRE_CHAVES)
        self.calculo()
        self.consome(TOKEN.FECHA_CHAVES)
        
    # <exp> -> <disj>
    def exp(self):
        self.disj()
            
    # <disj> -> <conj> <restoDisj>
    def disj(self):
        self.conj() 
        self.restoDisj()

    # <restoDisj> -> LAMBDA | or <conj> <restoDisj>
    def restoDisj(self):
        if self.tokenLido[0] == TOKEN.OR:
            self.consome(TOKEN.OR)
            self.conj()
            self.restoDisj()
        else:
            pass

    # <conj> -> <nao> <restoConj>
    def conj(self):
        self.nao()
        self.restoConj()

    # <restoConj> -> LAMBDA | and <nao> <restoConj>
    def restoConj(self):
        if self.tokenLido[0] == TOKEN.AND:
            self.consome(TOKEN.AND)
            self.nao()
            self.restoConj()
        else:
            pass

    # <nao> -> not <nao> | <rel>
    def nao(self):
        if self.tokenLido[0] == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            self.nao()
        else:
            self.rel()

    # <rel> -> <soma> <restoRel>
    def rel(self):
        self.soma()
        self.restoRel()

    # <restoRel> -> LAMBDA | oprel <soma>
    def restoRel(self):
        if self.tokenLido[0] in [TOKEN.IGUAL, TOKEN.MAIOR, TOKEN.MENOR, TOKEN.MAIOR_IGUAL, TOKEN.MENOR_IGUAL, TOKEN.DIFERENTE]:
            self.consome(self.tokenLido[0])
            self.soma()
        else:
            pass

    # <soma> -> <mult> <restoSoma>
    def soma(self):
        self.mult()
        self.restoSoma()

    # <restoSoma> -> LAMBDA | + <mult> <restoSoma> | - <mult> <restoSoma>
    def restoSoma(self):
        if self.tokenLido[0] == TOKEN.SOMA:
            self.consome(TOKEN.SOMA)
            self.mult()
            self.restoSoma()
        elif self.tokenLido[0] == TOKEN.SUBTRACAO:
            self.consome(TOKEN.SUBTRACAO)
            self.mult()
            self.restoSoma()
        else:
            pass

    # <mult> -> <uno> <restoMult>
    def mult(self):
        self.uno()
        self.restoMult()

    # <restoMult> -> LAMBDA | / <uno> <restoMult> | * <uno> <restoMult>
    def restoMult(self):
        if self.tokenLido[0] == TOKEN.DIVISAO:
            self.consome(TOKEN.DIVISAO)
            self.uno()
            self.restoMult()
        elif self.tokenLido[0] == TOKEN.MULTIPLICACAO:
            self.consome(TOKEN.MULTIPLICACAO)
            self.uno()
            self.restoMult()
        else:
            pass

    # <uno> -> + <uno> | - <uno> | <folha>
    def uno(self):
        if self.tokenLido[0] == TOKEN.SOMA:
            self.consome(TOKEN.SOMA)
            self.uno()
        elif self.tokenLido[0] == TOKEN.SUBTRACAO:
            self.consome(TOKEN.SUBTRACAO)
            self.uno()
        else:
            self.folha()
            
    # <folha> -> num | ident | ( <exp> )
    def folha(self):
        if self.tokenLido[0] == TOKEN.NUMERO:
            self.consome(TOKEN.NUMERO)
        elif self.tokenLido[0] == TOKEN.IDENT:
            self.consome(TOKEN.IDENT)
        else:
            self.consome(TOKEN.ABRE_PARENTESES)
            self.exp()
            self.consome(TOKEN.FECHA_PARENTESES)
