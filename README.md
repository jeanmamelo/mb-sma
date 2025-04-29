# MB-SMA

Serviço em Python para captura, processamento e persistência de média móvel simples usando PostgreSQL.

API em Golang que possibilita integração através da consulta dos dados.

---

## 🛠️ Tecnologias Utilizadas

- **Python** 3.13
- **Golang** 1.24
- **Chi**
- **Pytest**
- **PostgreSQL**
- **SQLAlchemy**
- **Docker** + **Docker Compose**

---

## ⚙️ Como Rodar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/jeanmamelo/mb-sma.git
cd mb-sma
```

### 2. Subir o banco de dados

```bash
docker-compose --profile db up -d
```

### 3. Rodar o serviço em Python para popular o banco de dados

```bash
docker-compose --profile python-sma up
```

### 4. Rodar o API server em Golang

```bash
docker-compose --profile go-sma up
```

> Tudo pronto para testar a solução. ✅

### 5. Abra o seu client API de preferência e faça a requisição no seguinte formato:

Exemplo:

GET localhost:8080/BRLBTC/mms?from=1717383600&to=1719543600&range=20

Deverá receber uma resposta parecida com essa:
```json
[
    {
        "timestamp": "2024-06-04T00:00:00Z",
        "mms": 354577.359651532
    },
    ...
    {
        "timestamp": "2024-06-28T00:00:00Z",
        "mms": 353995.85744478303
    }
]
```

---

## 🛡️ Testes

Executar testes automatizados:

- Para o serviço em Python:
```bash
cd python-sma
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -svv
```

- Para o serviço em Golang:
```bash
cd go-sma
go test ./... -v
```

---

## ✨ Funcionalidades

- [x] Captura de candles de criptomoedas através da API de candles do Mercado Bitcoin
- [x] Persistência segura no PostgreSQL utilizando SQLAlchemy
- [x] Controle de duplicidade (par + timestamp)
- [x] Alerta caso falte o registro de algum dia dentre os registros dos últimos 365 dias

---

## 🔍 Estratégia para incremento diário da tabela

### Utilizar o Job python-sma/scripts/sma_increment_job.py

1. Buscar o maior `timestamp` da tabela atual.
2. Coletar/gerar dados com `timestamp > maior timestamp atual`.
3. Inserir os dados de forma incremental.
4. Evitar duplicidade usando a constraint (`pair`, `timestamp`).

### Execução

Agendar via cronjob do Kubernetes:
```yaml
schedule: "0 23 * * *"

---

## 📄 Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).

---
