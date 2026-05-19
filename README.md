# 🛒 Carrinho de Compras Digital — Padrão Strategy (GoF)

> Implementação didática do padrão de projeto comportamental **Strategy** em Python, aplicado a um sistema de pagamentos intercambiáveis em um carrinho de compras digital.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Padrão Strategy](#-padrão-strategy)
- [Diagrama de Classes UML](#-diagrama-de-classes-uml)
- [Estrutura do Código](#-estrutura-do-código)
- [Estratégias Implementadas](#-estratégias-implementadas)
- [Princípios SOLID](#-princípios-solid)
- [Strategy vs if/elif vs Command](#-strategy-vs-ifelif-vs-command)
- [Como Executar](#-como-executar)
- [Tecnologias](#-tecnologias)
- [Autores](#-autores)

---

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como trabalho acadêmico para demonstrar, de forma **prática e didática**, o padrão de projeto **Strategy** (GoF – *Gang of Four*).

O sistema simula um **carrinho de compras digital** onde o processamento do pagamento é delegado a uma estratégia intercambiável. É possível alternar entre diferentes formas de pagamento **sem modificar** a classe principal (`Carrinho`), ilustrando na prática os princípios **OCP** e **DIP** do SOLID.

---

## 🧠 Padrão Strategy

O **Strategy** é um padrão comportamental que define uma família de algoritmos, encapsula cada um deles e os torna intercambiáveis. O padrão permite que o algoritmo varie independentemente dos clientes que o utilizam.

```
Problema resolvido: como trocar o comportamento de um objeto
em tempo de execução sem usar condicionais (if/elif/switch)?
```


|---|---|---|
| **Strategy** (interface) | `PaymentStrategy` | Define o contrato `processar_pagamento()` |
| **ConcreteStrategy** | `CartaoCredito`, `Pix`, `Boleto` | Implementa cada algoritmo de pagamento |
| **Context** | `Carrinho` | Mantém referência à estratégia e a delega |

--- 
## 📐 Diagrama de Classes UML

<img width="704" height="684" alt="image" src="https://github.com/user-attachments/assets/5a3bb78b-4ade-4852-848a-e009988fc7c2" />

---

## 📁 Estrutura do Código

```
carrinho_strategy.py
│
├── PaymentStrategy          # Interface abstrata (ABC)
│   ├── processar_pagamento()
│   └── nome()
│
├── CartaoCredito            # Estratégia concreta 1
├── Pix                      # Estratégia concreta 2
├── Boleto                   # Estratégia concreta 3
│
├── Carrinho                 # Contexto
│
└── main()                   # Demonstração completa
```

---

## 💳 Estratégias Implementadas

### 1. `CartaoCredito`
- Suporte a parcelamento de 1x até N vezes
- Cálculo de juros compostos com a **fórmula Price (PMT)**:

```
PMT = PV × i / (1 − (1 + i)^−n)
```

- À vista: sem acréscimo de juros
- Exibe número mascarado (`**** **** **** XXXX`)

### 2. `Pix`
- Desconto automático de **5%** sobre o valor total
- Pagamento instantâneo
- Aceita qualquer chave Pix (CPF, e-mail, telefone, aleatória)

### 3. `Boleto`
- Data de vencimento gerada dinamicamente (`hoje + N dias`)
- Geração simulada de código de barras
- Aviso de multa e juros após vencimento

---

## ✅ Princípios SOLID

### OCP — Princípio Aberto/Fechado
> *"Aberto para extensão, fechado para modificação."*

Para adicionar **PayPal**, **Criptomoeda** ou qualquer outro método, basta criar uma nova classe — a classe `Carrinho` **não precisa ser alterada**.

```python
# Nova estratégia sem tocar em Carrinho:
class PayPal(PaymentStrategy):
    def processar_pagamento(self, valor: float) -> str:
        ...
    def nome(self) -> str:
        return "PayPal"

carrinho.definir_estrategia(PayPal("usuario@email.com"))
carrinho.finalizar_compra()  # funciona imediatamente ✔
```

### DIP — Princípio da Inversão de Dependência
> *"Dependa de abstrações, não de implementações."*

```python
# ✔ Correto — depende da abstração
def definir_estrategia(self, estrategia: PaymentStrategy):
    self._estrategia = estrategia

# ✘ Errado — acoplamento à implementação concreta
def definir_estrategia(self, estrategia: CartaoCredito):
    self._estrategia = estrategia
```

---

## ⚖️ Strategy vs if/elif vs Command

### Sem o padrão (if/elif encadeado)

```python
def processar_pagamento(total, forma, **kwargs):
    if forma == "cartao":
        parcelas = kwargs.get("parcelas", 1)
        # lógica do cartão...
    elif forma == "pix":
        # lógica do pix...
    elif forma == "boleto":
        # lógica do boleto...
    # Cada nova forma exige MODIFICAR esta função → viola OCP
```

**Problemas:**
- Viola o Princípio Aberto/Fechado
- Aumenta o acoplamento e a complexidade ciclomática
- Dificulta testes unitários isolados
- Crescimento linear do método a cada novo método de pagamento

### Com o padrão Strategy

| Critério | if/elif | Strategy | Command |
|---|---|---|---|
| Adicionar novo método | Modifica função existente | Nova classe apenas | Nova classe apenas |
| Testabilidade | Difícil (tudo junto) | Fácil (isolada) | Fácil (isolada) |
| Troca em runtime | Possível, mas frágil | Nativa | Nativa |
| Histórico / desfazer | Não suporta | Não suporta | **Suporta** |
| Complexidade | Baixa (inicialmente) | Média | Alta |
| Melhor uso | Lógica simples e estável | Algoritmos intercambiáveis | Ações com undo/redo |

> **Quando usar Command ao invés de Strategy?**
> Se o sistema precisar de **histórico de transações**, **desfazer pagamentos** ou **enfileirar operações**, o padrão **Command** é mais adequado, pois encapsula a ação como um objeto com suporte a reversão.

---

## ▶️ Como Executar

### Localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/carrinho-strategy.git
cd carrinho-strategy

# Execute (sem dependências externas — apenas Python 3.10+)
python carrinho_strategy.py
```

### Google Colab

1. Acesse [colab.research.google.com](https://colab.research.google.com)
2. Crie um novo notebook
3. Faça upload do arquivo `carrinho_strategy.py` ou cole o conteúdo em uma célula
4. Execute com `Shift + Enter`

Ou use o botão abaixo:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/seu-usuario/carrinho-strategy/blob/main/carrinho_strategy.py)

> **Requisitos:** Python 3.10 ou superior (uso de `X | Y` para type hints). Nenhuma biblioteca externa necessária.

---

## 🛠 Tecnologias

- **Python 3.10+**
- `abc` — Abstract Base Classes (interface `PaymentStrategy`)
- `datetime` — Cálculo de vencimento do boleto
- `typing` — Anotações de tipo (`List`, `Tuple`)

---

## 👥 Autores

| Nome | GitHub |
|---|---|
| Cissa Fernandes | @cissaff ) (https://github.com/cissaff)  |
| Clara Bertão | [@clarabertao](https://github.com/clarabertao) |
| Eduarda Lima | [@EduardaCCampos](https://github.com/EduardaCCampos) |
| Sarah Godinho | [@Sarocaa](https://github.com/Sarocaa) |

---


<p align="center">
  Desenvolvido como trabalho acadêmico — Programação Orientada à Objetos 
</p>
