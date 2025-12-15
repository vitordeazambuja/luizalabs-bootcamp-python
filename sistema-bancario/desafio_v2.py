from abc import ABC

class Transacao(ABC):
    def registrar(conta):
        pass

class Deposito(Transacao):
    def __init__(self, _valor):
        self._valor = _valor
    
    def registrar(_conta):
        pass

class Saque(Transacao):
    def __init__(self, _valor):
        self._valor = _valor

    def registrar():
        pass

class Historico:
    def adicionar_transacao(transacao):
        pass


class Cliente():
    def __init__(self, _endereco, _contas):
        self._endereco = _endereco
        self._contas = _contas
    
    def realizar_transacao(conta, transacao):
        pass

    def adicionar_conta(conta):
        pass

class PessoaFisica(Cliente):
    def __init__(self, _cpf, _nome, _data_nascimento):
        self._cpf = _cpf
        self._nome = _nome
        self._data_nascimento = _data_nascimento

class Conta:
    def __init__(self, _saldo, _numero, _agencia, _cliente, _historico):
        self._saldo = _saldo
        self._numero = _numero
        self._agencia = _agencia
        self._cliente = _cliente
        self._historico = _historico
    
    def saldo():
        pass

    def nova_conta(cliente, numero):
        pass

    def sacar(valor):
        pass

    def depositar(valor):
        pass

class ContaCorrente(Conta):
    def __init__(self, _limite, _limite_saques):
        self._limite = _limite
        self._limite_saques = _limite_saques