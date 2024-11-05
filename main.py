from lexico import Lexico

class Tradutor:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def inicializa(self):
        self.arq = open(self.nomeArq, "r")
        self.lexico = Lexico(self.arq)

    def testaLexico(self):
        while not self.lexico.fimDoArquivo():
            self.lexico.imprimeToken(self.lexico.getToken())

    def finaliza(self):
        self.arq.close()

# inicia a traducao
if __name__ == '__main__':
    x = Tradutor('codigoFonte.txt')
    x.inicializa()
    x.testaLexico()
    x.finaliza()