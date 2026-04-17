# 📈 B3 Finance — Visualizador de Candlestick

Aplicação web para visualização de gráficos candlestick de ações da B3, índices de mercado e ativos estrangeiros, construída com Flask, Plotly e yFinance.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey?logo=flask)
![Plotly](https://img.shields.io/badge/Plotly-6.7-3F4F75?logo=plotly)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
  - [Com Docker (recomendado)](#com-docker-recomendado)
  - [Localmente com uv](#localmente-com-uv)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Ativos Suportados](#ativos-suportados)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Contribuindo](#contribuindo)

---

## Visão Geral

O **B3 Finance** é uma aplicação web leve e responsiva que permite visualizar gráficos de candlestick dos principais ativos negociados na B3 (Bolsa de Valores do Brasil), além de suportar índices globais e ações estrangeiras listadas no Yahoo Finance.

Os dados são obtidos em tempo real via **yFinance** e os gráficos são renderizados interativamente com **Plotly**, exibindo os últimos 90 dias de negociação.

---

## Funcionalidades

- **Sidebar** com atalhos rápidos para os 50+ principais ativos da B3
- **Campo de busca livre** para qualquer ativo disponível no Yahoo Finance (ex: `AAPL`, `^DJI`, `BTC-USD`)
- **Gráficos interativos** com zoom, pan e hover detalhado
- **Resolução automática de tickers** — o usuário digita `PETR4` e a aplicação converte para `PETR4.SA` internamente
- **Suporte ao IBOVESPA** com os aliases `IBOV`, `IBOVESPA` e `^BVSP`
- Interface responsiva compatível com dispositivos móveis

---

## Tecnologias

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.14 | Linguagem principal |
| Flask | ≥ 3.1.3 | Framework web |
| yFinance | ≥ 1.2.2 | Coleta de dados de mercado |
| Plotly | ≥ 6.7.0 | Geração de gráficos interativos |
| Pandas | ≥ 3.0.2 | Manipulação de dados |
| uv | latest | Gerenciador de pacotes e ambientes virtuais |
| Docker | — | Containerização e deploy |

---

## Pré-requisitos

**Para execução via Docker (recomendado):**
- [Docker](https://docs.docker.com/get-docker/) instalado e em execução

**Para execução local:**
- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado

---

## Instalação e Execução

### Com Docker (recomendado)

#### Opção 1 — Imagem pré-construída do Docker Hub

A forma mais rápida de colocar a aplicação no ar, sem necessidade de clonar o repositório:

```bash
docker container run --name finance -d -p 5000:5000 antoniomarcosap/b3finance:latest
```

Acesse em: [http://localhost:5000](http://localhost:5000)

#### Opção 2 — Build local da imagem

Clone o repositório e construa a imagem a partir do `Dockerfile`:

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/b3finance.git
cd b3finance

# 2. Construa a imagem
docker build -t b3finance .

# 3. Execute o container
docker container run --name finance -d -p 5000:5000 b3finance
```

#### Comandos úteis de gerenciamento do container

```bash
# Verificar logs em tempo real
docker logs -f finance

# Parar o container
docker stop finance

# Iniciar novamente
docker start finance

# Remover o container
docker rm -f finance

# Verificar status do health check
docker inspect --format='{{.State.Health.Status}}' finance
```

---

### Localmente com uv

```bash
# 1. Clone o repositório
git clone https://github.com/am-pereira/b3finance.git
cd b3finance

# 2. Instale as dependências
uv sync

# 3. Execute a aplicação
uv run python main.py
```

Acesse em: [http://localhost:5000](http://localhost:5000)

> **Nota:** Para ambiente de desenvolvimento, as dependências do grupo `dev` (pytest, ruff) serão instaladas automaticamente com `uv sync`.

---

## Uso

### Navegação pela Sidebar

A barra lateral exibe uma lista de atalhos com os principais ativos da B3. Clique em qualquer ativo para carregar seu gráfico imediatamente.

### Busca Manual

No campo de texto no topo da área principal, digite o código do ativo desejado e clique em **Buscar**. A aplicação resolve automaticamente o formato correto para a API:

| Você digita | API recebe | Descrição |
|---|---|---|
| `PETR4` | `PETR4.SA` | Ação brasileira |
| `IBOV` | `^BVSP` | Índice Bovespa |
| `AAPL` | `AAPL` | Ação estrangeira |
| `^DJI` | `^DJI` | Índice Dow Jones |
| `BTC-USD` | `BTC-USD` | Criptomoeda |

### Interatividade do Gráfico

- **Zoom:** scroll do mouse ou seleção de área
- **Pan:** clique e arraste
- **Hover:** passe o cursor sobre as velas para ver OHLC detalhado
- **Reset:** duplo clique para restaurar a visualização

---

## Estrutura do Projeto

```
b3finance/
├── main.py               # Aplicação Flask (rotas, lógica de negócio, geração de gráficos)
├── templates/
│   └── index.html        # Template HTML (Jinja2)
├── pyproject.toml        # Configuração do projeto e dependências (uv/PEP 517)
├── uv.lock               # Lock file das dependências
├── Dockerfile            # Imagem multi-stage otimizada para produção
├── .dockerignore         # Arquivos excluídos do contexto de build
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Esta documentação
```

---

## Ativos Suportados

A sidebar inclui os seguintes ativos como atalho rápido:

<details>
<summary>Ver lista completa (clique para expandir)</summary>

| Código | Empresa |
|---|---|
| IBOV | IBOVESPA |
| PETR4 | Petrobras |
| VALE3 | Vale |
| ITUB4 | Itaú Unibanco |
| BBDC4 | Bradesco |
| ABEV3 | Ambev |
| WEGE3 | WEG |
| RENT3 | Localiza |
| B3SA3 | B3 |
| SUZB3 | Suzano |
| RAIL3 | Rumo |
| GGBR4 | Gerdau |
| CSNA3 | CSN |
| KLBN11 | Klabin |
| LREN3 | Lojas Renner |
| EMBR3 | Embraer |
| VIVT3 | Telefônica Brasil |
| SANB11 | Santander Brasil |
| BBAS3 | Banco do Brasil |
| CMIG4 | Cemig |
| UGPA3 | Ultrapar |
| CCRO3 | CCR |
| EQTL3 | Equatorial |
| ELET3 | Eletrobras |
| CPFE3 | CPFL Energia |
| TRPL4 | Transmissão Paulista |
| TAEE11 | TAESA |
| EGIE3 | Engie Brasil |
| NTCO3 | Natura &Co |
| RADL3 | Raia Drogasil |
| HAPV3 | Hapvida |
| MRVE3 | MRV |
| CYRE3 | Cyrela |
| BRFS3 | BRF |
| SMTO3 | São Martinho |
| COGN3 | Cogna |
| AZUL4 | Azul |
| PCAR3 | Pão de Açúcar |
| CRFB3 | Carrefour Brasil |
| LWSA3 | Locaweb |
| JBSS3 | JBS |
| TOTS3 | Totvs |
| PRIO3 | PetroRio |
| MGLU3 | Magazine Luiza |
| SLCE3 | SLC Agrícola |
| AURE3 | Auren |
| JHSF3 | JHSF |

</details>

A busca manual aceita qualquer ticker válido no Yahoo Finance, incluindo ações americanas, índices globais e criptomoedas.

---

## Variáveis de Ambiente

A aplicação não exige configuração de variáveis de ambiente para funcionar. As seguintes variáveis são definidas internamente no `Dockerfile` para otimização:

| Variável | Valor | Descrição |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE` | `1` | Desabilita geração de arquivos `.pyc` |
| `PYTHONUNBUFFERED` | `1` | Saída de logs sem buffer |
| `VIRTUAL_ENV` | `/app/venv` | Caminho do ambiente virtual |

---

## Contribuindo

Contribuições são bem-vindas! Para reportar bugs ou sugerir melhorias, abra uma [issue](https://github.com/am-pereira/b3finance/issues). Para contribuir com código:

```bash
# 1. Faça um fork e clone o repositório
git clone https://github.com/am-pereira/b3finance.git
cd b3finance

# 2. Instale as dependências de desenvolvimento
uv sync

# 3. Crie uma branch para sua feature
git checkout -b feature/minha-melhoria

# 4. Verifique o código com ruff antes de commitar
uv run ruff check .
uv run ruff format .

# 5. Abra um Pull Request
```

---

## Aviso Legal

Os dados exibidos são fornecidos pelo **Yahoo Finance** via biblioteca yFinance e destinam-se **exclusivamente a fins informativos e educacionais**. Não constituem recomendação de investimento. O autor não se responsabiliza por decisões financeiras tomadas com base nas informações exibidas pela aplicação.

---

*Dados fornecidos por Yahoo Finance • Gráficos gerados com Plotly*
