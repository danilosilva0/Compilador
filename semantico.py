from ttoken import TOKEN
class Semantico:
    def __init__(self):
        #len, trunc, str2Num, num2Str
        self.escopos = [{}]  # Pilha de escopos (começa com o escopo global)
        self.declara("len", (TOKEN.FUNCTION, [(None, (None, True)), ("retorno", (TOKEN.INT, False))]))
        self.declara("trunc", (TOKEN.FUNCTION, [(None, (TOKEN.FLOAT, False)), ("retorno", (TOKEN.INT, False))]))
        self.declara("str2num", (TOKEN.FUNCTION, [(None, (TOKEN.STRING, False)), ("retorno", (TOKEN.FLOAT, False))]))
        self.declara("num2str", (TOKEN.FUNCTION, [(None, (TOKEN.FLOAT, False)), ("retorno", (TOKEN.STRING, False))]))

        # Tabela de operações usando apenas tokens para o operador
        self.tabelaOperacoes = TOKEN.tabelaOperacoes()

    def entra_escopo(self):
        """Entra em um novo escopo."""
        self.escopos.append({})
        pass

    def sai_escopo(self):
        """Sai do escopo atual."""
        self.escopos.pop()
        pass

    def declara(self, nome, tipo):
        escopo_atual = self.escopos[-1]
        if nome in escopo_atual:
            raise Exception(f'Erro semântico: Redeclaração de "{nome}" no mesmo escopo.')
        escopo_atual[nome] = tipo  # Registra o tipo da variável ou função



    def verifica_declaracao(self, nome):
        """Verifica se um nome foi declarado em algum escopo válido."""
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        print(f'Erro semântico: "{nome}" não foi declarado.')
        raise Exception(f'Erro semântico: "{nome}" não foi declarado.')

    def verifica_tipo(self, tipo_esperado, tipo_real):
        """Verifica compatibilidade de tipos em operações ou atribuições."""
        if tipo_esperado != tipo_real:
            raise Exception(f'Erro semântico: Tipo incompatível. Esperado {tipo_esperado}, mas recebido {tipo_real}.')
    
    def obter_tipo_token(self, ident, linha, coluna):
        try:
            for escopo in self.escopos:
                if ident in escopo:
                    return escopo[ident]
            raise Exception(f'Variável "{ident}" não declarada. Linha: {linha}, coluna: {coluna}')
        except Exception as e:
            print(f"Erro inesperado: {e}")
            exit(1)
            
    def verificaOperacao(self, e1, op, e2=None):
        if e2 is None:
            # Operação unária
            entrada = frozenset({op, e1[0]})  # Use apenas o primeiro elemento
        else:
            # Operação binária
            entrada = frozenset({e1[0], op, e2[0]})  # Use apenas os primeiros elementos de e1 e e2

        if entrada in self.tabelaOperacoes:
            teste = self.tabelaOperacoes[entrada]
            return teste
        else:
            msg = f"Operação inválida: {e1} {op} {e2}" if e2 else f"Operação inválida: {op} {e1}"
            raise Exception(msg)