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

    # <prog> -> <funcao> <restoFuncoes>
    def prog(self):
        self.funcao()
        self.restoFuncoes()

    # <restoFuncoes> -> <funcao> <restoFuncoes> | LAMBDA
    def restoFuncoes(self):
        if self.tokenLido[0] == TOKEN.FUNCTION:
            self.funcao()
            self.restoFuncoes()
        else:
            pass

    # <funcao> -> function ident ( <params> ) <tipoResultado> <corpo>
    def funcao(self):
        self.consome(TOKEN.FUNCTION)
        self.consome(TOKEN.IDENT)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.params()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.tipoResultado()
        self.corpo()

    # <tipoResultado> -> LAMBDA | -> <tipo>
    def tipoResultado(self):
        if self.tokenLido[0] == TOKEN.SETA:
            self.consome(TOKEN.SETA)
            self.tipo()
        else:
            pass

    # <params> -> <tipo> ident <restoParams> | LAMBDA
    def params(self):
        if self.tokenLido[0] == TOKEN.STRING:
            self.tipo()
            self.consome(TOKEN.IDENT)
            self.restoParams()
        else:
            pass

    # <restoParams> -> LAMBDA | , <tipo> ident <restoParams>
    def restoParams(self):
        if self.tokenLido[0] == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.tipo()
            self.consome(TOKEN.IDENT)
            self.restoParams()
        else:
            pass

    # <corpo> -> begin <declaracoes> <calculo> end
    def corpo(self):
        self.consome(TOKEN.BEGIN)
        self.declaracoes()
        self.calculo()
        self.consome(TOKEN.END)

    # <declaracoes> -> <declara> <declaracoes> | LAMBDA
    def declaracoes(self):
        if self.tokenLido[0] == TOKEN.STRING:
            self.declara()
            self.declaracoes()
        else:
            pass

    # <declara> -> <tipo> <idents> ;
    def declara(self):
        self.tipo()
        self.idents()
        self.consome(TOKEN.PONTO_VIRGULA)

    # <idents> -> ident <restoIdents>
    def idents(self):
        self.consome(TOKEN.IDENT)
        self.restoIdents()

    # <restoIdents> -> , ident <restoIdents> | LAMBDA
    def restoIdents(self):
        if self.tokenLido[0] == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.consome(TOKEN.IDENT)
            self.restoIdents()
        else:
            pass

    # <tipo> -> string <opcLista> | int <opcLista> | float <opcLista>
    def tipo(self):
        if self.tokenLido[0] == TOKEN.STRING:
            self.consome(TOKEN.STRING)
            self.opcLista()
        elif self.tokenLido[0] == TOKEN.INT:
            self.consome(TOKEN.INT)
            self.opcLista()
        else:
            self.consome(TOKEN.FLOAT)
            self.opcLista()

    # <opcLista> -> [ list ] | LAMBDA
    def opcLista(self):
        if self.tokenLido[0] == TOKEN.ABRE_COLCHETES:
            self.consome(TOKEN.ABRE_COLCHETES)
            self.consome(TOKEN.LIST)
            self.consome(TOKEN.FECHA_COLCHETES)
        else:
            pass

    # <retorna> -> return <expOpc> ;
    def retorna(self):
        self.consome(TOKEN.RETURN)
        self.expOpc()

    # <expOpc> -> LAMBDA | <exp>
    def expOpc(self):
        if self.tokenLido[0] == TOKEN.NOT:
            self.exp()
        else:
            pass

    # <while> -> while ( <exp> ) <com>
    def _while_(self):
        self.consome(TOKEN.WHILE)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.exp()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.com()

    # <for> -> for ident in <range> do <com>
    def _for_(self):
        self.consome(TOKEN.FOR)
        self.consome(TOKEN.IDENT)
        self.consome(TOKEN.IN)
        self.range()
        self.consome(TOKEN.DO)
        self.com()

    # <range> -> <lista> | range ( <exp> , <exp> <opcRange> )
    def range(self):
        if self.tokenLido[0] == TOKEN.IDENT:
            self.lista()
        else:
            self.consome(TOKEN.RANGE)
            self.consome(TOKEN.ABRE_PARENTESES)
            self.exp()
            self.consome(TOKEN.VIRGULA)
            self.exp()
            self.opcRange()
            self.consome(TOKEN.FECHA_PARENTESES)

    # <lista> -> ident <opcIndice> | [ <elemLista> ]
    def lista(self):
        if self.tokenLido[0] == TOKEN.IDENT:
            self.consome(TOKEN.IDENT)
            self.opcIndice()
        else:
            self.consome(TOKEN.ABRE_COLCHETES)
            self.elemLista()
            self.consome(TOKEN.FECHA_COLCHETES)

    # <elemLista> -> LAMBDA | <elem> <restoElemLista>
    def elemLista(self):
        elem = [TOKEN.INTVAL, TOKEN.FLOATVAL, TOKEN.STRVAL, TOKEN.IDENT]
        if self.tokenLido[0] in elem:
            self.elem()
            self.restoElemLista()
        else:
            pass

    # <restoElemLista> -> LAMBDA | , <elem> <restoElemLista>
    def restoElemLista(self):
        if self.tokenLido[0] == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.elem()
            self.restoElemLista()
        else:
            pass

    # <elem> -> intVal | floatVal | strVal | ident
    def elem(self):
        if self.tokenLido[0] == TOKEN.INTVAL:
            self.consome(TOKEN.INTVAL)
        elif self.tokenLido[0] == TOKEN.FLOATVAL:
            self.consome(TOKEN.FLOATVAL)
        elif self.tokenLido[0] == TOKEN.STRVAL:
            self.consome(TOKEN.STRVAL)
        else:
            self.consome(TOKEN.IDENT)

    # <opcRange> -> , <exp> | LAMBDA
    def opcRange(self):
        if self.tokenLido[0] == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.exp()
        else:
            pass
    
    # <calculo> -> LAMBDA | <com><calculo>
    def calculo(self):
        com = [TOKEN.IDENT, TOKEN.IF, TOKEN.READ, TOKEN.WRITE, TOKEN.ABRE_CHAVES, TOKEN.FOR, TOKEN.WHILE, TOKEN.RETURN]
        entrou = False
        while self.tokenLido[0] in com:
            self.com()
            entrou = True
        
        if not entrou:
            pass 

    # <com> -> <atrib>|<if>|<leitura>|<escrita>|<bloco>|<for>|<while>|<retorna>|<call>
    def com(self):
        if self.tokenLido[0] == TOKEN.IDENT:
            self.atrib()
        elif self.tokenLido[0] == TOKEN.IF:
            self._if_()
        elif self.tokenLido[0] == TOKEN.READ:
            self.leitura()
        elif self.tokenLido[0] == TOKEN.WRITE:
            self.escrita()
        elif self.tokenLido[0] == TOKEN.ABRE_CHAVES:
            self.bloco()
        elif self.tokenLido[0] == TOKEN.FOR:
            self._for()
        elif self.tokenLido[0] == TOKEN.WHILE:
            self._while()
        elif self.tokenLido[0] == TOKEN.RETURN:
            self.retorna()
        else:
            self.call()

    # <atrib> -> ident <opcIndice> = <exp> ;
    def atrib(self):
        self.consome(TOKEN.IDENT)
        self.opcIndice()
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
        self.lista_outs()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.consome(TOKEN.PONTO_VIRGULA)

    # <lista_outs> -> <out> <restoLista_outs>
    def lista_outs(self):
        self.out()
        self.restoLista_outs()

    # <restoLista_outs> -> LAMBDA | , <out> <restoLista_outs>
    def restoLista_outs(self):
        if self.tokenLido == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.out()
            self.restoLista_outs()
        else:
            pass

    # <out> -> <folha>
    def out(self):
        self.folha()

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
        if self.tokenLido[0] in TOKEN.oprel():
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

    # <restoMult> -> LAMBDA | / <uno> <restoMult> | * <uno> <restoMult> | % <uno> 
    def restoMult(self):
        if self.tokenLido[0] == TOKEN.DIVISAO:
            self.consome(TOKEN.DIVISAO)
            self.uno()
            self.restoMult()
        elif self.tokenLido[0] == TOKEN.MULTIPLICACAO:
            self.consome(TOKEN.MULTIPLICACAO)
            self.uno()
            self.restoMult()
        elif self.tokenLido[0] == TOKEN.MOD:
            self.consome(TOKEN.MOD)
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
            
    # <folha> -> intVal | floatVal | strVal | <call> | <lista> | ( <exp> ) 
    def folha(self):
        if self.tokenLido[0] == TOKEN.INTVAL:
            self.consome(TOKEN.INTVAL)
        elif self.tokenLido[0] == TOKEN.FLOATVAL:
            self.consome(TOKEN.FLOATVAL)
        elif self.tokenLido[0] == TOKEN.STRVAL:
            self.consome(TOKEN.STRVAL)
        # <call>
        elif self.tokenLido[0] == TOKEN.IDENT:
            self.call()
        # <lista>
        elif self.tokenLido[0] == TOKEN.IDENT:
            self.lista()
        else:
            self.consome(TOKEN.ABRE_PARENTESES)
            self.exp()
            self.consome(TOKEN.FECHA_PARENTESES)

    # <call> -> ident ( <lista_outs_opc> )
    def call(self):
        self.consome(TOKEN.IDENT)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.lista_outs_opc()
        self.consome(TOKEN.FECHA_PARENTESES)

    # <lista_outs_opc> -> <lista_outs> | LAMBDA
    def lista_outs_opc(self):
        folha = [
            TOKEN.INTVAL,
            TOKEN.FLOATVAL,
            TOKEN.STRVAL,
            TOKEN.IDENT,
            TOKEN.ABRE_PARENTESES
        ]
        if self.tokenLido[0] in folha:
            self.lista_outs()
        else:
            pass

    # <opcIndice> -> LAMBDA | [ <exp> <restoElem> ]
    def opcIndice(self):
        if self.tokenLido[0] == TOKEN.ABRE_COLCHETES:
            self.consome(TOKEN.ABRE_COLCHETES)
            self.exp()
            self.restoElem()
            self.consome(TOKEN.FECHA_COLCHETES)
        else:
            pass

    # <restoElem> -> LAMBDA | : <exp>
    def restoElem(self):
        if self.tokenLido[0] == TOKEN.DOIS_PONTOS:
            self.consome(TOKEN.DOIS_PONTOS)
            self.exp()
        else:
            pass