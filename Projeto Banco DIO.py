from abc import ABC, abstractmethod
from datetime import date

# Interface Transacao
class Transacao(ABC):
    def __init__(self, valor: float):
        self.valor = valor

    @abstractmethod
    def registrar(self, conta):
        pass


# Depósito implementa Transacao
class Deposito(Transacao):
    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)


# Saque implementa Transacao
class Saque(Transacao):
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# Histórico guarda lista de transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

    def extrato(self):
        if not self.transacoes:
            return "Não foram realizadas movimentações."
        resultado = ""
        for t in self.transacoes:
            tipo = "Depósito" if isinstance(t, Deposito) else "Saque"
            resultado += f"{tipo}:\tR$ {t.valor:.2f}\n"
        return resultado


# Conta base
class Conta:
    def __init__(self, cliente, numero: int, agencia: str = "0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor: float) -> bool:
        if valor > 0 and self.saldo >= valor:
            self.saldo -= valor
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.saldo += valor
            return True
        return False


# ContaCorrente especializa Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, numero: int, limite: float = 500, limite_saques: int = 3, agencia: str = "0001"):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor: float) -> bool:
        if valor > self.limite:
            print("Valor do saque excede o limite.")
            return False
        if self.saques_realizados >= self.limite_saques:
            print("Número máximo de saques excedido.")
            return False
        sucesso = super().sacar(valor)
        if sucesso:
            self.saques_realizados += 1
        return sucesso


# Cliente base
class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)


# PessoaFisica especializa Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# Exemplo de uso
if __name__ == "__main__":
    cliente = PessoaFisica("12345678900", "Ana Silva", date(1990, 5, 20), "Rua A, 123")
    conta = ContaCorrente(cliente, numero=1)
    cliente.adicionar_conta(conta)

    deposito = Deposito(1000)
    cliente.realizar_transacao(conta, deposito)

    saque = Saque(200)
    cliente.realizar_transacao(conta, saque)

    print("Extrato:")
    print(conta.historico.extrato())
    print(f"Saldo final: R$ {conta.saldo_atual():.2f}")
