# sistemaOcorrenciasTP2

Aplicação Flask + MySQL para registro e consulta de ocorrências, com API para o mapa e uma área administrativa para tipos de ocorrência e relatórios.

## Iniciar localmente

1. Instale Python 3.9 ou superior e MySQL.
2. Na pasta do projeto, crie e ative um ambiente virtual:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências e crie a configuração local:

   ```sh
   pip install -r requirements.txt
   cp .env.example .env
   ```

4. Edite `.env` com a conexão MySQL local. Gere o hash da senha administrativa sem exibir a senha no terminal:

   ```sh
   .venv/bin/python -c 'from getpass import getpass; from dotenv import set_key; from werkzeug.security import generate_password_hash; set_key(".env", "ALERTADF_ADMIN_PASSWORD_HASH", generate_password_hash(getpass("Senha administrativa: "), method="pbkdf2:sha256"))'
   ```

5. Prepare uma base de desenvolvimento com o esquema de `sistemaOcorrencias/BancoDados/scriptSistema.sql`. Inicie a aplicação:

   ```sh
   python -m sistemaOcorrencias.app
   ```

O servidor local escuta em `127.0.0.1:8000`. A aplicação não executa migrações nem scripts SQL automaticamente. `scriptTesteSistema.sql` apaga e recria dados; use-o somente em uma base descartável.

## Executar os testes

Instale as dependências de desenvolvimento com `pip install -r requirements-dev.txt`. Em seguida, a partir da pasta `sistemaOcorrencias`, execute:

```sh
python -m pytest -q teste_dominios.py teste_entidades.py teste_api_relatorios.py
```

## Rotas

- `GET /api/occurrences` — lista ocorrências para o mapa com `id`, `type`, `description`, `date`, `latitude` e `longitude`. O `id` combina os dois campos da chave primária composta.
- `/login` — acesso administrativo local com hash guardado em `.env`.
- `/admin/tipos` — cadastro, edição e exclusão de tipos de ocorrência.
- `/relatorios` — filtros por período, tipo, status e local; resumos por tipo, status, local e mês; taxa de resolução; pesquisas por termo e região; usuários por perfil; exportação CSV.

## Relatórios e esquema

O módulo administrativo usa `Ocorrencia.tipoOcorrencia_idtipoOcorrencia` para relacionar ocorrências ao tipo do banco. O relatório conta pesquisas por `pesquisa.dataHora` e mostra o total atual de usuários. A tabela `Usuario` ainda não tem data de cadastro, portanto não é possível calcular quantos usuários foram cadastrados em cada mês sem uma alteração de esquema acordada pelo grupo.

Os IDs de `tipoOcorrencia` não são `AUTO_INCREMENT`; o cadastro usa `MAX(idtipoOcorrencia) + 1`. Isso pode colidir se dois administradores cadastrarem tipos ao mesmo tempo. Definam a estratégia de geração de IDs com quem mantém o esquema antes de colocar o cadastro em uso concorrente.

O login com hash local é provisório. Integre-o com a autenticação administrativa do grupo quando ela estiver definida. Nunca adicione `.env` ao Git.
