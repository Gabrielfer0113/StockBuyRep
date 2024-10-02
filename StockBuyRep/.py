class Animal:
    def __init__(self, nome, tipo, cor):
        self.nome = nome
        self.tipo = tipo
        self.cor = cor

    
    def cadastro_animal(self):
        nome = self.nome
        tipo = self.tipo
        cor = self.cor
        return nome, tipo, cor

    def exibir_animal(self):
        return Animal.cadastro_animal(self)
    

animal = Animal('Tigre', 'Felino', 'Preto e laranja')
print(animal.exibir_animal())

class Produto:
    imposto = 1.05
    def __init__(self, nome, descricao, valor, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor
        self.quantidade = quantidade


    def produto_descricao(self):
        return f'''
        --------Compra realizada--------
        Produto: {self.nome} - {self.descricao}
        Valor unitario: {self.valor}
        Quantidade: {self.quantidade}
        Total: {self.valor * self.quantidade * Produto.imposto}'''
    


produto = Produto('PlayStation 4', 'Video Game', 2000.00, 2)
print(produto.produto_descricao())