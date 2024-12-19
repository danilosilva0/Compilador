class Semantico:
    def __init__(self):
        self.tabela_simbolos = {}  # Tabela de símbolos para controle de variáveis e funções
        self.escopos = [{}]  # Pilha de escopos (começa com o escopo global)

    def entra_escopo(self):
        """Entra em um novo escopo."""
        self.escopos.append({})

    def sai_escopo(self):
        """Sai do escopo atual."""
        self.escopos.pop()

    def declara(self, nome, tipo):
        """Declara uma variável ou função no escopo atual."""
        escopo_atual = self.escopos[-1]
        if nome in escopo_atual:
            raise Exception(f'Erro semântico: Redeclaração de "{nome}" no mesmo escopo.')
        escopo_atual[nome] = tipo

    def verifica_declaracao(self, nome):
        """Verifica se um nome foi declarado em algum escopo válido."""
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        raise Exception(f'Erro semântico: "{nome}" não foi declarado.')

    def verifica_tipo(self, tipo_esperado, tipo_real):
        """Verifica compatibilidade de tipos em operações ou atribuições."""
        if tipo_esperado != tipo_real:
            raise Exception(f'Erro semântico: Tipo incompatível. Esperado {tipo_esperado}, mas recebido {tipo_real}.')