from abc import ABC, abstractmethod

AGENCIA = "001"
NUMERO = "989041"

class PessoaFisica():
    def __init__(self, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    def registrar(self, conta):
        conta.depositar(self._valor)
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        pass

class Historico:
    def adicionar_transacao(self, transacao):
        pass

class Conta:
    def __init__(self, numero, agencia, cliente, historico):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico
    
    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return Conta(numero,AGENCIA,cliente,Historico())

    def sacar(self, valor):
        pass

    def depositar(self, valor):
        pass

class ContaCorrente(Conta):
    def __init__(self,numero, agencia, cliente, historico, limite, limite_saques):
        super().__init__
        self._limite = limite
        self._limite_saques = limite_saques

class Cliente(PessoaFisica):
    def __init__(self, endereco, contas):
        super().__init__
        self._endereco = endereco
        self._contas = contas
    
    def realizar_transacao(self, conta, transacao):
        pass

    def adicionar_conta(self, conta):
        pass