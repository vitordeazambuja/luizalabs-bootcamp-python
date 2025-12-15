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
    
    @property
    def valor(self):
        return self.valor
    
    def registrar(self,conta):
        if conta.depositar(self._valor):
            conta._historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self.valor
    
    def registrar(self,conta):
        if conta.sacar(self._valor):
            conta._historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._log = []
    
    def adicionar_transacao(self, transacao):
        self._log.append(transacao)

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
        if valor <= 0:
            return False
    
        if valor > self._saldo:
            return False
        
        self._saldo -= valor
        return True

    def depositar(self, valor):     
        self._saldo += valor
        return True

class ContaCorrente(Conta):
    def __init__(self,numero, agencia, cliente, historico, limite, limite_saques):
        super().__init__(numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques

class Cliente(PessoaFisica):
    def __init__(self,cpf, nome, data_nascimento, endereco):
        super().__init__(cpf, nome, data_nascimento)
        self._endereco = endereco
        self._contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)