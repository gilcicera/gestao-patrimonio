from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True) # vai retornar o nome da categoria

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True) # aqui vai retornar o nome do departamento

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=200) # aqui vai retornar o nome do fornecedor
    contato = models.CharField(max_length=100, blank=True, null=True) # aqui vai retornar o contato do fornecedor

    def __str__(self):
        return self.nome

class Bem(models.Model):
    codigo_rfid = models.CharField(max_length=50, unique=True) # aqui vai retornar o código do rfid do bem
    nome = models.CharField(max_length=200) 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) # chave estrangeira para a categoria
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE) # chave estrangeira para o departamento
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True) # chave estrangeira para o fornecedor
    data_aquisicao = models.DateField() # data de aquisição do bem
    data_revisao = models.DateField(blank=True, null=True) # data de revisão do bem
    valor = models.DecimalField(max_digits=10, decimal_places=2) # valor do bem
    status_manutencao = models.BooleanField(default=False) # status de manutenção do bem

    def __str__(self):
        return f"{self.nome} ({self.codigo_rfid})" # aqui vai retornar o nome do bem e o código do rfid

class Movimentacao(models.Model):
    bem = models.ForeignKey(Bem, on_delete=models.CASCADE) # chave estrangeira para o bem
    origem = models.ForeignKey(Departamento, related_name="origem", on_delete=models.CASCADE) # chave estrangeria para o departamento de origem
    destino = models.ForeignKey(Departamento, related_name="destino", on_delete=models.CASCADE) # chave estrangeira para o departamento de destino
    data_movimentacao = models.DateTimeField(auto_now_add=True) # data da movimentação

    def __str__(self):
        return f"{self.bem.nome} - {self.origem} → {self.destino}" # retorna o nome do bem, de onde ele veio e aonde ele vai

