# Golden Raspberry Awards API
A Golden Raspberry Awards API é uma aplicação RESTful desenvolvida para permitir a leitura da lista de indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards. Esta API possibilita obter informações sobre os produtores com maior e menor intervalo entre prêmios consecutivos e fornece endpoints para manipulação dos dados de filmes.

## Instruções para rodar o projeto

1. Instale as dependências:
    ```bash/cmd
    pip install -r requeriments.txt
    ```

2. Execute a aplicação:
    ```bash/cmd
    uvicorn app.main:app --reload
    ```

3. Execute os testes de integração:
    ```bash/cmd
    pytest tests/
    ```

## Endpoints

- `GET /vencedores/intervalos/`: Retorna os produtores com maior e menor intervalo entre prêmios consecutivos.
- `GET /filmes/`: Retorna os filmes no banco de dados.
- `POST /uploadarquivo/`: Envia arquivo para upload.
