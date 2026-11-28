# Administração + Relatórios

O módulo está integrado à aplicação Flask em `sistemaOcorrencias/admin_reports.py` e usa o esquema atual de `sistemaOcorrencias/BancoDados/scriptSistema.sql`.

## O que está incluído

- Acesso administrativo local com senha armazenada como hash em variável de ambiente.
- Cadastro, edição e exclusão segura de tipos de ocorrência.
- Relatório de ocorrências filtrado por data, tipo, status e local.
- Resumos por tipo, status, local e mês; taxa de resolução; pesquisas por período, termo e região; usuários por perfil; download CSV.
- Proteção CSRF nos formulários e consultas MySQL parametrizadas.
- Validação dos nomes/descrições de tipos e do intervalo das datas conforme os domínios enviados pelo grupo.

Siga as instruções de configuração e inicialização no `README.md`. O painel usa as rotas `/login`, `/admin/tipos` e `/relatorios` no mesmo servidor da API.

## Endpoints JSON

Os endpoints administrativos usam a sessão criada em `/login`. Sem uma sessão de administrador, retornam HTTP 401 em JSON. Filtros inválidos retornam HTTP 400; falhas no banco retornam HTTP 503.

- `GET /api/statistics/overview` retorna totais e agrupamentos de ocorrências, pesquisas e usuários.
- `GET /api/reports/occurrences` retorna as ocorrências filtradas sem CPF ou outros identificadores de usuário.

Ambos aceitam os filtros opcionais `start_date`, `end_date` (`AAAA-MM-DD`), `tipo` (ID do tipo), `status` e `local` (código do local). Exemplo: `/api/reports/occurrences?start_date=2026-11-01&tipo=2&local=101`.

O relatório agrupa pesquisas por `pesquisa.regiaoConsultada`, que já existe no esquema. As ocorrências são agrupadas por local; não há uma região da ocorrência no banco até o grupo definir como representá-la.

## Como o protótipo usa o esquema atual

- `tipoOcorrencia.Local_codigo` é obrigatório, por isso cada tipo precisa de um local.
- `Ocorrencia.tipoOcorrencia_idtipoOcorrencia` liga a ocorrência ao tipo. O filtro e os agrupamentos usam essa chave estrangeira.
- Para preservar o histórico, o painel bloqueia exclusão e renomeação de tipos ligados a ocorrências ou alertas. A descrição pode ser atualizada sem alterar o nome usado no histórico.
- A data dos relatórios usa DATE(hora) quando hora está preenchida; quando está vazia, usa data.
- Os filtros de data aceitam anos de 2026 a 2999. Nomes e descrições de tipos aceitam letras, números, espaços, vírgulas e pontos, sem pontuação repetida.
- Pesquisas no período são filtradas por `pesquisa.dataHora`. O total de usuários é atual; a tabela `Usuario` não armazena data de cadastro para uma série histórica mensal.
- O acesso por hash configurado no `.env` é temporário. Ele não substitui a autenticação que o grupo ainda precisa integrar com a tabela `Usuario`.

## Decisões de esquema ainda pendentes

- Os IDs das tabelas são `INT NOT NULL` sem `AUTO_INCREMENT`. O cadastro usa `MAX(idtipoOcorrencia)+1`, que pode colidir se dois administradores criarem tipos ao mesmo tempo.
- A tabela `Usuario` define `senha VARCHAR(6)`, enquanto `scriptTesteSistema.sql` altera esse campo para `VARCHAR(255)`. O login local evita depender dessa definição, mas a autenticação final precisa de uma versão acordada.
- `Usuario` não possui data de cadastro. Um relatório mensal de novos usuários exige que o grupo acrescente e preencha esse campo antes de definir a migração.
