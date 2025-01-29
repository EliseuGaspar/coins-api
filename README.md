## Coins API

**Status**: Terminado!

#### DESCRIÇÃO

Este projeto é uma API Rest aberta com as informações de câmbio dos principais bancos de Angola.

#### INDICE
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuindo](#contribuindo)
- [Licença](./LICENCE)

#### INSTALAÇÃO

#### Requisitos
- Python 3.12.*
- Conexão a Internet

#### Instalação

**1º Clone o Projeto**
```bash
git clone https://github.com/EliseuGaspar/coins-api.git
```

**2º Crie um ambiente virtual e instale as dependências**

```bash
# Criar um ambiente virtual
python -m venv venv # no windows
python3 -m venv venv # no mac/linux

# Acesse o ambiente virtual
venv\Scripts\activate # no windows
source venv/bin/activate # no mac/linux

# Instalar as dependências
pip install -r requirements.txt
```

#### USO

Agora com tudo instalado precisamos rodar o nosso server e setar as primeiras configurações.

**1º Rodar o projeto**

```bash
fastapi run server.py
```

**2º Alimentar o banco de dados com os dados do cambio**

```bash
python bot.add_exchanges.py #no windows

python3 bot.add_exchanges.py #no mac/linux
```

**3º Acessar a documentação swagger**

```
http://localhost:8000/docs
```

#### FUNCIONALIDADES

As principais funcionalidades do projeto são:

- **Raspagem de Dados**: WebScrappy das atualizações do cambio no site de cada banco de uma em uma hora

- **Listagem dos Cambios**: Disponibilidade de acesso aos dados de Scrappy nos endpoints (**/exchanges** & **/exchanges/detail/bank_name**)

- **Webhook**: Envio dos dados atualizados para as urls ativas após processo de Scrappy.

- **Verificação de urls**: Verifica o estado e disponibilidade de cada url registrada e deleta as defeituosas.

#### CONTRIBUINDO

Este projeto é **Open-Source** então está disponível a opniões e melhorias.

- **Faça um fork do projeto**

- **Crie uma branch para suas alterações**

    ```git
    git checkout -b feature/sua-funcionalidade
    ```
- **Faça um Pull Request**.


<br/><br/>
<small>Copyright Eliseu Gaspar 01/2025</small>
