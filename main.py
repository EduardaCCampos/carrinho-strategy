"""
=============================================================
  PADRÃO DE PROJETO STRATEGY – CARRINHO DE COMPRAS DIGITAL
=============================================================

Autores  : [Cissa, Clara, Eduarda, Sarah]
Disciplina: [Programação orientada a objeto]
Padrão   : Strategy (GoF – Comportamental)
Princípios SOLID aplicados:
    • OCP  – Aberto para extensão, fechado para modificação
    • DIP  – Dependência sobre abstrações, não implementações

Descrição:
    Simulação de um carrinho de compras que delega o processamento
    do pagamento a uma estratégia intercambiável.  O contexto
    (Carrinho) nunca precisa ser alterado para suportar novos
    meios de pagamento – basta criar uma nova classe que implemente
    PaymentStrategy.
"""

from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Tuple


# ─────────────────────────────────────────────
#  INTERFACE / CONTRATO  (PaymentStrategy)
# ─────────────────────────────────────────────

class PaymentStrategy(ABC):
    """
    Interface abstrata que define o contrato para todas as
    estratégias de pagamento.

    Qualquer nova forma de pagamento deve herdar desta classe
    e implementar o método `processar_pagamento`.

    Princípio DIP: o Carrinho depende desta abstração,
    nunca das classes concretas.
    """

    @abstractmethod
    def processar_pagamento(self, valor: float) -> str:
        """
        Processa o pagamento do valor informado.

        Parâmetros:
            valor (float): Valor total a ser pago (em R$).

        Retorna:
            str: Mensagem de confirmação / detalhes do pagamento.
        """
        pass

    @abstractmethod
    def nome(self) -> str:
        """Retorna o nome amigável da estratégia."""
        pass


# ─────────────────────────────────────────────
#  ESTRATÉGIAS CONCRETAS
# ─────────────────────────────────────────────

class CartaoCredito(PaymentStrategy):
    """
    Estratégia de pagamento via Cartão de Crédito.

    Suporta parcelamento: calcula o valor de cada parcela
    acrescido de juros compostos mensais (padrão 2,5 % a.m.).

    Atributos:
        titular     (str)  : Nome do titular do cartão.
        numero      (str)  : Últimos 4 dígitos (exibição mascarada).
        parcelas    (int)  : Número de parcelas (1 = à vista).
        juros_am    (float): Taxa de juros mensal (decimal).
    """

    JUROS_PADRAO = 0.025  # 2,5 % ao mês

    def __init__(self, titular: str, numero: str,
                 parcelas: int = 1, juros_am: float = JUROS_PADRAO):
        if parcelas < 1:
            raise ValueError("O número de parcelas deve ser >= 1.")
        self._titular  = titular
        self._numero   = numero[-4:]  # armazena só os 4 últimos dígitos
        self._parcelas = parcelas
        self._juros_am = juros_am

    def nome(self) -> str:
        return "Cartão de Crédito"

    def processar_pagamento(self, valor: float) -> str:
        if self._parcelas == 1:
            # Sem juros para compras à vista
            valor_parcela = valor
            detalhe = "à vista (sem juros)"
        else:
            # Juros compostos: PMT = PV * i / (1 - (1+i)^-n)
            i = self._juros_am
            n = self._parcelas
            valor_parcela = valor * i / (1 - (1 + i) ** (-n))
            total_pago    = valor_parcela * n
            detalhe = (
                f"{n}x de R$ {valor_parcela:.2f} "
                f"(total: R$ {total_pago:.2f} | "
                f"juros: {i * 100:.1f}% a.m.)"
            )

        return (
            f"✔ Pagamento aprovado via {self.nome()}\n"
            f"   Titular : {self._titular}\n"
            f"   Cartão  : **** **** **** {self._numero}\n"
            f"   Valor   : R$ {valor:.2f}\n"
            f"   Condição: {detalhe}"
        )


class Pix(PaymentStrategy):
    """
    Estratégia de pagamento via Pix.

    Aplica automaticamente um desconto de 5 % sobre o valor
    total, incentivando o uso do método instantâneo.

    Atributos:
        chave (str): Chave Pix do beneficiário.
    """

    DESCONTO = 0.05  # 5 % de desconto

    def __init__(self, chave: str):
        self._chave = chave

    def nome(self) -> str:
        return "Pix"

    def processar_pagamento(self, valor: float) -> str:
        desconto      = valor * self.DESCONTO
        valor_final   = valor - desconto

        return (
            f"✔ Pagamento confirmado via {self.nome()}\n"
            f"   Chave Pix  : {self._chave}\n"
            f"   Valor orig.: R$ {valor:.2f}\n"
            f"   Desconto   : R$ {desconto:.2f} ({self.DESCONTO*100:.0f}%)\n"
            f"   Valor final: R$ {valor_final:.2f}\n"
            f"   Status     : Transação processada instantaneamente ⚡"
        )


class Boleto(PaymentStrategy):
    """
    Estratégia de pagamento via Boleto Bancário.

    Gera automaticamente a data de vencimento (padrão: 3 dias
    úteis a partir de hoje) e simula um código de barras.

    Atributos:
        dias_vencimento (int): Dias corridos até o vencimento.
    """

    def __init__(self, dias_vencimento: int = 3):
        if dias_vencimento < 1:
            raise ValueError("O vencimento deve ser de pelo menos 1 dia.")
        self._dias_vencimento = dias_vencimento

    def nome(self) -> str:
        return "Boleto Bancário"

    def _gerar_codigo_barras(self, valor: float) -> str:
        """Simula a geração de um código de barras (fins didáticos)."""
        import random
        random.seed(int(valor * 100))
        grupos = [
            "".join([str(random.randint(0, 9)) for _ in range(5)]),
            "".join([str(random.randint(0, 9)) for _ in range(5)]),
            "".join([str(random.randint(0, 9)) for _ in range(5)]),
            str(random.randint(0, 9)),
            "".join([str(random.randint(0, 9)) for _ in range(14)]),
        ]
        return " ".join(grupos)

    def processar_pagamento(self, valor: float) -> str:
        vencimento   = date.today() + timedelta(days=self._dias_vencimento)
        cod_barras   = self._gerar_codigo_barras(valor)

        return (
            f"✔ Boleto gerado com sucesso!\n"
            f"   Valor     : R$ {valor:.2f}\n"
            f"   Vencimento: {vencimento.strftime('%d/%m/%Y')}\n"
            f"   Código    : {cod_barras}\n"
            f"   ⚠ Após o vencimento, sujeito a multa e juros."
        )


# ─────────────────────────────────────────────
#  CONTEXTO  (Carrinho de Compras)
# ─────────────────────────────────────────────

class Carrinho:
    """
    Contexto do padrão Strategy.

    Mantém uma lista de itens (produto, preço, quantidade) e
    delega o processamento do pagamento à estratégia configurada.

    O Carrinho não conhece *como* o pagamento é feito – apenas
    que a estratégia implementa PaymentStrategy.

    Princípio OCP: adicionar uma nova forma de pagamento exige
    apenas criar uma nova classe concreta, sem tocar aqui.
    """

    def __init__(self):
        # Lista de tuplas: (nome_produto, preco_unitario, quantidade)
        self._itens: List[Tuple[str, float, int]] = []
        self._estrategia: PaymentStrategy | None  = None

    # ── gerenciamento de itens ──────────────────

    def adicionar_item(self, produto: str, preco: float, quantidade: int = 1):
        """Adiciona um produto ao carrinho."""
        if preco < 0 or quantidade < 1:
            raise ValueError("Preço deve ser ≥ 0 e quantidade ≥ 1.")
        self._itens.append((produto, preco, quantidade))
        print(f"   + {quantidade}x {produto} — R$ {preco:.2f} cada")

    def remover_item(self, produto: str):
        """Remove a primeira ocorrência de um produto pelo nome."""
        for item in self._itens:
            if item[0].lower() == produto.lower():
                self._itens.remove(item)
                print(f"   - {produto} removido do carrinho.")
                return
        print(f"   ⚠ Produto '{produto}' não encontrado no carrinho.")

    def limpar(self):
        """Esvazia o carrinho."""
        self._itens.clear()
        print("   Carrinho esvaziado.")

    # ── cálculo de valor ───────────────────────

    @property
    def total(self) -> float:
        """Calcula o total do carrinho (sem descontos de pagamento)."""
        return sum(preco * qtd for _, preco, qtd in self._itens)

    def exibir_itens(self):
        """Exibe todos os itens presentes no carrinho."""
        if not self._itens:
            print("   Carrinho vazio.")
            return
        print("\n   ┌─────────────────────────────────────────┐")
        print("   │           ITENS DO CARRINHO             │")
        print("   ├──────────────────┬───────────┬──────────┤")
        print("   │ Produto          │  Preço    │ Qtd      │")
        print("   ├──────────────────┼───────────┼──────────┤")
        for produto, preco, qtd in self._itens:
            print(f"   │ {produto:<16} │ R${preco:>7.2f} │ {qtd:<8} │")
        print("   ├──────────────────┴───────────┴──────────┤")
        print(f"   │ TOTAL: R$ {self.total:>30.2f} │")
        print("   └─────────────────────────────────────────┘")

    # ── estratégia de pagamento ────────────────

    def definir_estrategia(self, estrategia: PaymentStrategy):
        """
        Injeta (ou troca) a estratégia de pagamento em tempo de execução.

        Princípio DIP: recebe a abstração, não a implementação.
        """
        self._estrategia = estrategia
        print(f"   Forma de pagamento definida: {estrategia.nome()}")

    def finalizar_compra(self):
        """
        Finaliza a compra delegando o pagamento à estratégia atual.

        Lança RuntimeError se nenhuma estratégia foi definida ou
        se o carrinho estiver vazio.
        """
        if not self._itens:
            raise RuntimeError("Não é possível finalizar: carrinho vazio.")
        if self._estrategia is None:
            raise RuntimeError("Nenhuma forma de pagamento foi selecionada.")

        print("\n" + "=" * 55)
        print("  FINALIZANDO COMPRA")
        print("=" * 55)
        self.exibir_itens()
        print("\n  Processando pagamento...")
        print("-" * 55)
        resultado = self._estrategia.processar_pagamento(self.total)
        print(resultado)
        print("=" * 55)


# ─────────────────────────────────────────────
#  DEMONSTRAÇÃO  –  main()
# ─────────────────────────────────────────────

def main():
    """
    Demonstração completa do padrão Strategy.

    Mostra como o mesmo Carrinho processa pagamentos com três
    estratégias distintas sem nenhuma alteração no contexto.
    """

    print("\n" + "█" * 55)
    print("  PADRÃO STRATEGY – CARRINHO DE COMPRAS DIGITAL")
    print("█" * 55)

    # ── Montando o carrinho ────────────────────
    print("\n[1] Adicionando itens ao carrinho...")
    carrinho = Carrinho()
    carrinho.adicionar_item("Teclado Mecânico",  350.00, 1)
    carrinho.adicionar_item("Mouse Gamer",       180.00, 1)
    carrinho.adicionar_item("Mousepad XL",        75.00, 2)
    carrinho.adicionar_item("Hub USB-C",          99.90, 1)

    # ── Estratégia 1: Cartão de Crédito ───────
    print("\n[2] Pagamento via Cartão de Crédito (6x com juros)")
    carrinho.definir_estrategia(
        CartaoCredito(titular="Maria Silva", numero="1234567890124321", parcelas=6)
    )
    carrinho.finalizar_compra()

    # ── Estratégia 2: Pix ─────────────────────
    print("\n[3] Pagamento via Pix (5% de desconto)")
    carrinho.definir_estrategia(
        Pix(chave="maria.silva@email.com")
    )
    carrinho.finalizar_compra()

    # ── Estratégia 3: Boleto ──────────────────
    print("\n[4] Pagamento via Boleto (vencimento em 5 dias)")
    carrinho.definir_estrategia(
        Boleto(dias_vencimento=5)
    )
    carrinho.finalizar_compra()

    # ── Extensibilidade: nova estratégia ──────
    print("\n[5] Extensibilidade: adicionando PayPal sem alterar Carrinho")
    print("    (demonstra o Princípio Aberto/Fechado)\n")

    class PayPal(PaymentStrategy):
        """
        Nova estratégia criada SEM modificar o Carrinho.
        Demonstra o Princípio OCP na prática.
        """
        def __init__(self, email: str):
            self._email = email

        def nome(self) -> str:
            return "PayPal"

        def processar_pagamento(self, valor: float) -> str:
            return (
                f"✔ Pagamento realizado via {self.nome()}\n"
                f"   Conta  : {self._email}\n"
                f"   Valor  : R$ {valor:.2f}\n"
                f"   Status : Aprovado instantaneamente 🌐"
            )

    carrinho.definir_estrategia(PayPal("maria.silva@email.com"))
    carrinho.finalizar_compra()

    # ── Comparação sem o padrão Strategy ──────
    print("\n" + "─" * 55)
    print("  COMPARAÇÃO: Abordagem SEM Strategy (if/elif)")
    print("─" * 55)
    print("""
  def processar_pagamento_sem_strategy(total, forma):
      if forma == "cartao":
          # lógica do cartão aqui...
      elif forma == "pix":
          # lógica do pix aqui...
      elif forma == "boleto":
          # lógica do boleto aqui...
      # Cada nova forma exige MODIFICAR esta função!
      # → Viola OCP e aumenta o acoplamento.
    """)
    print("  Com Strategy: novas formas = novas classes.")
    print("  Carrinho nunca muda. ✔\n")


if __name__ == "__main__":
    main()
