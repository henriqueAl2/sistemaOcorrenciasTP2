"""Flask prototype for AlertaDF administration and occurrence reports.

It uses the current SQL schema and does not create or alter database tables.
"""

from __future__ import annotations

import csv
import hmac
import io
import logging
import os
import secrets
from datetime import date
from functools import wraps
from urllib.parse import urlparse

import mysql.connector
from dotenv import load_dotenv
from flask import (
    Flask, Blueprint, abort, current_app, flash, jsonify, make_response, redirect,
    render_template_string, request, session, url_for,
)
from markupsafe import Markup
from mysql.connector import IntegrityError
from werkzeug.security import check_password_hash

if __package__:
    from .estatisticas.calculos import (
        contar_ocorrencias_por_mes,
        contar_pesquisas_por_regiao,
        contar_pesquisas_por_termo,
        contar_usuarios_por_perfil,
        gerar_indicadores_gerais,
    )
else:
    from estatisticas.calculos import (
        contar_ocorrencias_por_mes,
        contar_pesquisas_por_regiao,
        contar_pesquisas_por_termo,
        contar_usuarios_por_perfil,
        gerar_indicadores_gerais,
    )


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
reports_bp = Blueprint("reports", __name__, url_prefix="/relatorios")
api_reports_bp = Blueprint("api_reports", __name__, url_prefix="/api")


PAGE = """
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} · AlertaDF</title>
  <style>
    :root { color-scheme:light; --ink:#17313b; --muted:#5b7078; --line:#d8e1e4; --paper:#f4f8f8; --blue:#087e8b; --dark:#075e68; --red:#9f3434; }
    * { box-sizing:border-box }
    body { margin:0; background:var(--paper); color:var(--ink); font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif }
    header { display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:1rem max(1.2rem,calc((100vw - 1120px)/2)); background:#fff; border-bottom:1px solid var(--line) }
    .brand { color:var(--ink); font-size:1.15rem; font-weight:800; text-decoration:none }
    nav,.actions { display:flex; align-items:center; gap:.7rem; flex-wrap:wrap }
    nav a { color:var(--dark); font-weight:650; text-decoration:none }
    main { width:min(1120px,calc(100% - 2rem)); margin:2rem auto 4rem }
    h1 { margin:.2rem 0 1.25rem; font-size:clamp(1.7rem,3vw,2.3rem) }
    h2 { margin:0 0 1rem; font-size:1.15rem }
    p { color:var(--muted) }
    .card,.stat { margin:1rem 0; padding:1.2rem; background:#fff; border:1px solid var(--line); border-radius:14px; box-shadow:0 5px 18px #12333b0a }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:1rem }
    .stat { margin:0 }
    .stat strong { display:block; font-size:1.8rem; line-height:1.2 }
    .stat span,.small { color:var(--muted); font-size:.88rem }
    label { display:block; margin:.25rem 0 .35rem; font-weight:650 }
    input,select { width:100%; min-height:42px; padding:.55rem .7rem; border:1px solid #b8c8cd; border-radius:8px; color:var(--ink); background:#fff; font:inherit }
    input:focus,select:focus { outline:3px solid #087e8b2e; border-color:var(--blue) }
    .fields { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:.8rem; align-items:end }
    button,.button { display:inline-flex; align-items:center; justify-content:center; min-height:40px; padding:.55rem .9rem; border:0; border-radius:8px; background:var(--blue); color:#fff; font:inherit; font-weight:700; text-decoration:none; cursor:pointer }
    button:hover,.button:hover { background:var(--dark) }
    button.secondary,.button.secondary { background:#e8f1f2; color:var(--dark) }
    button.danger { background:#f8eaea; color:var(--red) }
    button:disabled { opacity:.5; cursor:not-allowed }
    .inline { display:inline }
    table { width:100%; border-collapse:collapse; background:#fff }
    th,td { padding:.7rem .6rem; border-bottom:1px solid var(--line); text-align:left; vertical-align:top }
    th { color:var(--muted); font-size:.85rem; text-transform:uppercase }
    .table-wrap { overflow:auto }
    .notice { margin:1rem 0; padding:.8rem 1rem; border-radius:9px; background:#eaf4f5; color:var(--dark) }
    .notice.error { background:#f9eaea; color:var(--red) }
    .notice.success { background:#e9f5ef; color:#12634c }
    footer { margin-top:2rem; color:var(--muted); font-size:.85rem }
    @media(max-width:700px) { header { align-items:flex-start; flex-direction:column } nav { gap:.7rem } th,td { min-width:115px } }
  </style>
</head>
<body>
  <header>
    <a class="brand" href="{{ url_for('reports.index') }}">AlertaDF</a>
    {% if session.get("is_admin") %}
    <nav aria-label="Navegação principal">
      <a href="{{ url_for('admin.types') }}">Tipos de ocorrência</a>
      <a href="{{ url_for('reports.index') }}">Relatórios</a>
      <form class="inline" method="post" action="{{ url_for('logout') }}">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><button class="secondary">Sair</button>
      </form>
    </nav>
    {% endif %}
  </header>
  <main>
    <h1>{{ title }}</h1>
    {% for category, message in get_flashed_messages(with_categories=true) %}
      <div class="notice {{ category }}">{{ message }}</div>
    {% endfor %}
    {{ body }}
    <footer>Protótipo local de Administração + Relatórios. Nenhuma alteração de esquema é aplicada.</footer>
  </main>
</body>
</html>
"""


LOGIN_BODY = """
<section class="card" style="max-width:480px">
  <p>Entre com a senha administrativa configurada no arquivo local de ambiente.</p>
  <form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <label for="password">Senha de administrador</label>
    <input id="password" name="password" type="password" autocomplete="current-password" required autofocus>
    <p><button type="submit">Entrar</button></p>
  </form>
  <p class="small">Esta senha temporária não é lida da tabela Usuario. A autenticação do grupo deve substituir este acesso local.</p>
</section>
"""


TYPES_BODY = """
<section class="card">
  <h2>Novo tipo de ocorrência</h2>
  {% if locais %}
  <form method="post" action="{{ url_for('admin.types') }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <div class="fields">
      <div><label for="nome">Nome (até 45 caracteres)</label><input id="nome" name="nome" maxlength="45" required></div>
      <div><label for="descricao">Descrição (opcional)</label><input id="descricao" name="descricao" maxlength="255"></div>
      <div><label for="local_codigo">Local associado</label>
        <select id="local_codigo" name="local_codigo" required>
          {% for local in locais %}<option value="{{ local.codigo }}">#{{ local.codigo }} · {{ local.endereco or "Endereço não informado" }}</option>{% endfor %}
        </select>
      </div>
      <div><button type="submit">Cadastrar tipo</button></div>
    </div>
  </form>
  {% else %}<p>Cadastre um local antes de criar tipos. A tabela tipoOcorrencia exige um local associado.</p>{% endif %}
</section>
<section class="card">
  <h2>Tipos cadastrados</h2>
  {% if tipos %}
  <div class="table-wrap"><table>
    <thead><tr><th>ID</th><th>Tipo e descrição</th><th>Local</th><th>Ocorrências</th><th>Alertas</th><th>Ações</th></tr></thead>
    <tbody>{% for tipo in tipos %}
      <tr>
        <td>{{ tipo.id }}</td>
        <td><form method="post" action="{{ url_for('admin.update_type', type_id=tipo.id) }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <label class="small" for="nome-{{ tipo.id }}">Nome</label>
          <input id="nome-{{ tipo.id }}" name="nome" maxlength="45" value="{{ tipo.nome or '' }}" required>
          <label class="small" for="descricao-{{ tipo.id }}">Descrição</label>
          <input id="descricao-{{ tipo.id }}" name="descricao" maxlength="255" value="{{ tipo.descricao or '' }}">
          <p class="small">O nome só muda antes de haver ocorrências associadas.</p>
          <button class="secondary" type="submit">Salvar</button>
        </form></td>
        <td>#{{ tipo.local_codigo }}<br>{{ tipo.endereco or "Endereço não informado" }}</td>
        <td>{{ tipo.ocorrencias }}</td><td>{{ tipo.alertas }}</td>
        <td><form method="post" action="{{ url_for('admin.delete_type', type_id=tipo.id) }}" onsubmit="return confirm('Excluir este tipo de ocorrência?')">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <button class="danger" {% if tipo.ocorrencias or tipo.alertas %}disabled title="Preserva tipos já usados no histórico"{% endif %}>Excluir</button>
        </form></td>
      </tr>
    {% endfor %}</tbody>
  </table></div>
  {% else %}<p>Nenhum tipo de ocorrência cadastrado.</p>{% endif %}
</section>
<p class="small">Tipos já usados em ocorrências ou alertas não podem ser renomeados nem excluídos neste protótipo.</p>
"""


REPORTS_BODY = """
<section class="card"><h2>Filtros</h2>
  <form method="get" action="{{ url_for('reports.index') }}">
    <div class="fields">
      <div><label for="start_date">De</label><input id="start_date" type="date" name="start_date" min="2026-01-01" max="2999-12-31" value="{{ filters.start_date }}"></div>
      <div><label for="end_date">Até</label><input id="end_date" type="date" name="end_date" min="2026-01-01" max="2999-12-31" value="{{ filters.end_date }}"></div>
      <div><label for="tipo">Tipo</label><select id="tipo" name="tipo"><option value="">Todos</option>
        {% for tipo in tipos %}<option value="{{ tipo.id }}" {% if filters.tipo == tipo.id|string %}selected{% endif %}>{{ tipo.nome }}</option>{% endfor %}
      </select></div>
      <div><label for="status">Status</label><select id="status" name="status"><option value="">Todos</option>
        {% for item in statuses %}<option value="{{ item.status }}" {% if filters.status == item.status %}selected{% endif %}>{{ item.status }}</option>{% endfor %}
      </select></div>
      <div><label for="local">Local</label><select id="local" name="local"><option value="">Todos</option>
        {% for local in locais %}<option value="{{ local.codigo }}" {% if filters.local == local.codigo|string %}selected{% endif %}>#{{ local.codigo }} · {{ local.endereco or "Endereço não informado" }}</option>{% endfor %}
      </select></div>
      <div class="actions"><button type="submit">Aplicar filtros</button><a class="button secondary" href="{{ url_for('reports.index') }}">Limpar</a></div>
    </div>
  </form>
</section>
<div class="grid">
  <div class="stat"><strong>{{ total }}</strong><span>ocorrências encontradas</span></div>
  <div class="stat"><strong>{{ indicators.taxa_resolucao|round(1) }}%</strong><span>taxa de resolução</span></div>
  <div class="stat"><strong>{{ total_searches }}</strong><span>pesquisas no período</span></div>
  <div class="stat"><strong>{{ total_users }}</strong><span>usuários cadastrados (total atual)</span></div>
  <div class="stat"><strong>{{ by_type|length }}</strong><span>tipos presentes</span></div>
  <div class="stat"><strong>{{ by_status|length }}</strong><span>status presentes</span></div>
  <div class="stat"><strong>{{ by_local|length }}</strong><span>locais presentes</span></div>
</div>
<section class="grid">
  <div class="card"><h2>Ocorrências por mês</h2>{% if by_month %}
    <div class="table-wrap"><table><thead><tr><th>Mês</th><th>Quantidade</th></tr></thead><tbody>
      {% for row in by_month %}<tr><td>{{ row.mes }}</td><td>{{ row.total }}</td></tr>{% endfor %}
    </tbody></table></div>{% else %}<p>Sem resultados.</p>{% endif %}
  </div>
  <div class="card"><h2>Usuários por perfil</h2>{% if by_profile %}
    <div class="table-wrap"><table><thead><tr><th>Perfil</th><th>Quantidade</th></tr></thead><tbody>
      {% for row in by_profile %}<tr><td>{{ row.rotulo }}</td><td>{{ row.total }}</td></tr>{% endfor %}
    </tbody></table></div>{% else %}<p>Sem resultados.</p>{% endif %}
  </div>
</section>
<section class="grid">
  <div class="card"><h2>Pesquisas por termo</h2>{% if searches_by_term %}
    <div class="table-wrap"><table><thead><tr><th>Termo</th><th>Quantidade</th></tr></thead><tbody>
      {% for row in searches_by_term %}<tr><td>{{ row.rotulo }}</td><td>{{ row.total }}</td></tr>{% endfor %}
    </tbody></table></div>{% else %}<p>Sem resultados.</p>{% endif %}
  </div>
  <div class="card"><h2>Pesquisas por região</h2>{% if searches_by_region %}
    <div class="table-wrap"><table><thead><tr><th>Região</th><th>Quantidade</th></tr></thead><tbody>
      {% for row in searches_by_region %}<tr><td>{{ row.rotulo }}</td><td>{{ row.total }}</td></tr>{% endfor %}
    </tbody></table></div>{% else %}<p>Sem resultados.</p>{% endif %}
  </div>
</section>
<section class="grid">
  <div class="card"><h2>Por tipo</h2>{% if by_type %}
    <div class="table-wrap"><table><thead><tr><th>Tipo</th><th>Quantidade</th></tr></thead><tbody>
      {% for row in by_type %}<tr><td>{{ row.rotulo }}</td><td>{{ row.total }}</td></tr>{% endfor %}
    </tbody></table></div>{% else %}<p>Sem resultados.</p>{% endif %}
  </div>
  <div class="card"><h2>Por status</h2>{% if by_status %}
    <div class="table-wrap"><table><thead><tr><th>Status</th><th>Quantidade</th></tr></thead><tbody>
      {% for row in by_status %}<tr><td>{{ row.rotulo }}</td><td>{{ row.total }}</td></tr>{% endfor %}
    </tbody></table></div>{% else %}<p>Sem resultados.</p>{% endif %}
  </div>
  <div class="card"><h2>Por local</h2>{% if by_local %}
    <div class="table-wrap"><table><thead><tr><th>Local</th><th>Quantidade</th></tr></thead><tbody>
      {% for row in by_local %}<tr><td>#{{ row.codigo }} · {{ row.rotulo }}</td><td>{{ row.total }}</td></tr>{% endfor %}
    </tbody></table></div>{% else %}<p>Sem resultados.</p>{% endif %}
  </div>
</section>
<section class="card">
  <div class="actions" style="justify-content:space-between"><h2>Ocorrências</h2>
    <a class="button secondary" href="{{ url_for('reports.export_csv', start_date=filters.start_date, end_date=filters.end_date, tipo=filters.tipo, status=filters.status, local=filters.local) }}">Baixar CSV</a>
  </div>
  {% if ocorrencias %}<div class="table-wrap"><table>
    <thead><tr><th>ID</th><th>Data</th><th>Tipo</th><th>Status</th><th>Local</th><th>Descrição</th></tr></thead>
    <tbody>{% for row in ocorrencias %}<tr>
      <td>{{ row.id }}</td>
      <td>{% if row.hora %}{{ row.hora.strftime("%d/%m/%Y %H:%M") }}{% elif row.data %}{{ row.data.strftime("%d/%m/%Y") }}{% else %}—{% endif %}</td>
      <td>{{ row.tipo or "Sem tipo" }}</td><td>{{ row.status or "Sem status" }}</td>
      <td>#{{ row.local_codigo }}<br>{{ row.endereco or "Endereço não informado" }}</td>
      <td>{{ row.descricao or "—" }}</td>
    </tr>{% endfor %}</tbody>
  </table></div>{% else %}<p>Nenhuma ocorrência corresponde aos filtros.</p>{% endif %}
</section>
<p class="small">Ocorrências usam a relação com tipoOcorrencia. A taxa de resolução considera o status “Resolvida”. Pesquisas respeitam o intervalo pelas datas de dataHora; o total de usuários é o total atual, pois Usuario não possui data de cadastro.</p>
"""


def _csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def _valid_csrf():
    submitted = request.form.get("csrf_token", "")
    stored = session.get("_csrf_token", "")
    return bool(submitted and stored and hmac.compare_digest(submitted, stored))


def _page(title, body_template, **context):
    body = render_template_string(body_template, **context)
    return render_template_string(PAGE, title=title, body=Markup(body))


def _connect():
    return mysql.connector.connect(
        host=current_app.config["DB_HOST"],
        port=current_app.config["DB_PORT"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        database=current_app.config["DB_NAME"],
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
    )


def _fetch_all(sql, params=()):
    connection = _connect()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def _fetch_one(sql, params=()):
    rows = _fetch_all(sql, params)
    return rows[0] if rows else None


def _execute(sql, params=()):
    connection = _connect()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def _admin_only(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("login", next=request.full_path.rstrip("?")))
        return view(*args, **kwargs)
    return wrapped


def _api_admin_only(view):
    """Require an administrative session and return JSON for API clients."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return jsonify({"erro": "Autenticação administrativa necessária."}), 401
        return view(*args, **kwargs)
    return wrapped


def _require_csrf():
    if not _valid_csrf():
        abort(400, description="Formulário expirado. Atualize a página e tente novamente.")


def _valid_domain_text(value):
    if not value or value[0] in ",. " or value[-1] in ",. ":
        return False
    if not all(character.isalpha() or character.isdigit() or character in " ,." for character in value):
        return False
    for current, following in zip(value, value[1:]):
        if current in ",." and following in ",.":
            return False
        if current == " " and not following.isalnum():
            return False
    return True


def _type_form_values():
    name = (request.form.get("nome") or "").strip()
    description = (request.form.get("descricao") or "").strip()
    try:
        local_code = int(request.form.get("local_codigo", ""))
    except ValueError:
        return None, "Selecione um local válido."
    if not name or len(name) > 45:
        return None, "Informe um nome com até 45 caracteres."
    if len(description) > 255:
        return None, "A descrição pode ter até 255 caracteres."
    if not _valid_domain_text(name):
        return None, "O nome aceita letras, números, espaços, vírgulas e pontos, sem pontuação repetida."
    if description and not _valid_domain_text(description):
        return None, "A descrição aceita letras, números, espaços, vírgulas e pontos, sem pontuação repetida."
    return {"nome": name, "descricao": description or None, "local_codigo": local_code}, None


def _filters():
    values = {
        "start_date": (request.args.get("start_date") or "").strip(),
        "end_date": (request.args.get("end_date") or "").strip(),
        "tipo": (request.args.get("tipo") or "").strip(),
        "status": (request.args.get("status") or "").strip(),
        "local": (request.args.get("local") or "").strip(),
    }
    for key in ("start_date", "end_date"):
        if values[key]:
            try:
                parsed_date = date.fromisoformat(values[key])
                if not 2026 <= parsed_date.year <= 2999:
                    raise ValueError("Data fora do intervalo permitido.")
            except ValueError:
                flash("Informe datas válidas entre 2026 e 2999.", "error")
                values[key] = ""
    if values["start_date"] and values["end_date"] and values["start_date"] > values["end_date"]:
        flash("A data inicial deve ser anterior à data final.", "error")
        values["start_date"] = values["end_date"] = ""
    if values["local"]:
        try:
            int(values["local"])
        except ValueError:
            flash("Selecione um local válido.", "error")
            values["local"] = ""
    if values["tipo"]:
        try:
            if int(values["tipo"]) <= 0:
                raise ValueError
        except ValueError:
            flash("Selecione um tipo de ocorrência válido.", "error")
            values["tipo"] = ""
    return values


def _api_filters():
    """Parse and strictly validate report filters for JSON endpoints."""
    values = {
        "start_date": (request.args.get("start_date") or "").strip(),
        "end_date": (request.args.get("end_date") or "").strip(),
        "tipo": (request.args.get("tipo") or "").strip(),
        "status": (request.args.get("status") or "").strip(),
        "local": (request.args.get("local") or "").strip(),
    }
    for key in ("start_date", "end_date"):
        if values[key]:
            try:
                parsed_date = date.fromisoformat(values[key])
            except ValueError:
                return None, "Informe datas no formato AAAA-MM-DD."
            if not 2026 <= parsed_date.year <= 2999:
                return None, "As datas devem estar entre 2026 e 2999."
    if values["start_date"] and values["end_date"] and values["start_date"] > values["end_date"]:
        return None, "A data inicial deve ser anterior ou igual à data final."
    for key, label in (("tipo", "tipo"), ("local", "local")):
        if values[key]:
            try:
                if int(values[key]) <= 0:
                    raise ValueError
            except ValueError:
                return None, f"Informe um identificador de {label} válido."
    if len(values["status"]) > 45:
        return None, "O status pode ter até 45 caracteres."
    return values, None


def _where(filters):
    clauses, params = ["1=1"], []
    if filters["start_date"]:
        clauses.append("COALESCE(DATE(o.hora), o.data) >= %s")
        params.append(filters["start_date"])
    if filters["end_date"]:
        clauses.append("COALESCE(DATE(o.hora), o.data) <= %s")
        params.append(filters["end_date"])
    if filters["tipo"]:
        clauses.append("o.tipoOcorrencia_idtipoOcorrencia = %s")
        params.append(int(filters["tipo"]))
    if filters["status"]:
        clauses.append("o.status = %s")
        params.append(filters["status"])
    if filters["local"]:
        clauses.append("o.Local_codigo = %s")
        params.append(int(filters["local"]))
    return " AND ".join(clauses), tuple(params)


def _occurrences(filters):
    where_sql, params = _where(filters)
    return _fetch_all(
        f"""SELECT o.idOcorrencia AS id, t.nome AS tipo, o.descricao, o.data, o.hora, o.status,
                   l.codigo AS local_codigo, l.endereco
            FROM Ocorrencia o
            JOIN tipoOcorrencia t ON t.idtipoOcorrencia = o.tipoOcorrencia_idtipoOcorrencia
            JOIN Local l ON l.codigo = o.Local_codigo
            WHERE {where_sql}
            ORDER BY COALESCE(o.hora, TIMESTAMP(o.data)) DESC, o.idOcorrencia DESC""",
        params,
    )


def _group(filters, select_sql, group_sql, order_sql):
    where_sql, params = _where(filters)
    return _fetch_all(
        f"""SELECT {select_sql}, COUNT(*) AS total
            FROM Ocorrencia o
            JOIN tipoOcorrencia t ON t.idtipoOcorrencia = o.tipoOcorrencia_idtipoOcorrencia
            JOIN Local l ON l.codigo = o.Local_codigo
            WHERE {where_sql}
            GROUP BY {group_sql} ORDER BY {order_sql}""",
        params,
    )


def _report_data(filters):
    rows = _occurrences(filters)
    indicators = gerar_indicadores_gerais(
        [{"status": (row["status"] or "").strip() or "Sem status"} for row in rows]
    )
    dated_occurrences = []
    for row in rows:
        occurrence_date = row["hora"].date() if row["hora"] else row["data"]
        if occurrence_date:
            dated_occurrences.append({"data": occurrence_date.isoformat()})
    monthly_counts = contar_ocorrencias_por_mes(dated_occurrences)

    search_clauses, search_params = [], []
    if filters["start_date"]:
        search_clauses.append("DATE(p.dataHora) >= %s")
        search_params.append(filters["start_date"])
    if filters["end_date"]:
        search_clauses.append("DATE(p.dataHora) <= %s")
        search_params.append(filters["end_date"])
    search_where = " AND ".join(search_clauses) or "1=1"
    searches = _fetch_all(
        f"SELECT p.termoPesquisado AS termo, p.regiaoConsultada AS regiao "
        f"FROM pesquisa p WHERE {search_where}",
        tuple(search_params),
    )
    search_terms = contar_pesquisas_por_termo(
        [{"termo": (row["termo"] or "").strip() or "Sem termo"} for row in searches]
    )
    search_regions = contar_pesquisas_por_regiao(
        [{"regiao": (row["regiao"] or "").strip() or "Sem região"} for row in searches]
    )
    profiles = _fetch_all("SELECT tipo AS perfil FROM Usuario")
    profile_counts = contar_usuarios_por_perfil(
        [{"perfil": (row["perfil"] or "").strip() or "Sem perfil"} for row in profiles]
    )
    return {
        "tipos": _fetch_all("SELECT idtipoOcorrencia AS id, nome FROM tipoOcorrencia ORDER BY nome, idtipoOcorrencia"),
        "locais": _fetch_all("SELECT codigo, endereco FROM Local ORDER BY codigo"),
        "statuses": _fetch_all("SELECT DISTINCT status FROM Ocorrencia WHERE status IS NOT NULL AND status <> '' ORDER BY status"),
        "ocorrencias": rows,
        "total": len(rows),
        "indicators": indicators,
        "by_month": [
            {"mes": month, "total": total} for month, total in monthly_counts.items()
        ],
        "total_searches": len(searches),
        "searches_by_term": [
            {"rotulo": label, "total": total}
            for label, total in sorted(search_terms.items(), key=lambda item: (-item[1], item[0]))
        ],
        "searches_by_region": [
            {"rotulo": label, "total": total}
            for label, total in sorted(search_regions.items(), key=lambda item: (-item[1], item[0]))
        ],
        "total_users": len(profiles),
        "by_profile": [
            {"rotulo": label, "total": total}
            for label, total in sorted(profile_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "by_type": _group(filters, "COALESCE(NULLIF(t.nome, ''), 'Sem tipo') AS rotulo", "t.idtipoOcorrencia, t.nome", "total DESC, rotulo"),
        "by_status": _group(filters, "COALESCE(NULLIF(o.status, ''), 'Sem status') AS rotulo", "o.status", "total DESC, rotulo"),
        "by_local": _group(filters, "l.codigo AS codigo, COALESCE(NULLIF(l.endereco, ''), 'Endereço não informado') AS rotulo", "l.codigo, l.endereco", "total DESC, l.codigo"),
        "filters": filters,
    }


@api_reports_bp.get("/statistics/overview")
@_api_admin_only
def api_statistics_overview():
    """Return the report dashboard aggregates as a JSON API response."""
    filters, error = _api_filters()
    if error:
        return jsonify({"erro": error}), 400
    try:
        data = _report_data(filters)
    except (mysql.connector.Error, ConnectionError):
        current_app.logger.exception("Falha ao consultar as estatísticas.")
        return jsonify({"erro": "Falha ao consultar o banco de dados."}), 503

    return jsonify({
        "filters": {
            "start_date": filters["start_date"] or None,
            "end_date": filters["end_date"] or None,
            "type_id": int(filters["tipo"]) if filters["tipo"] else None,
            "status": filters["status"] or None,
            "location_id": int(filters["local"]) if filters["local"] else None,
        },
        "occurrences": {
            "total": data["total"],
            "resolved": data["indicators"]["resolvidas"],
            "resolution_rate": data["indicators"]["taxa_resolucao"],
            "by_month": [
                {"month": row["mes"], "total": row["total"]}
                for row in data["by_month"]
            ],
            "by_type": [
                {"label": row["rotulo"], "total": row["total"]}
                for row in data["by_type"]
            ],
            "by_status": [
                {"label": row["rotulo"], "total": row["total"]}
                for row in data["by_status"]
            ],
            "by_location": [
                {"id": row["codigo"], "label": row["rotulo"], "total": row["total"]}
                for row in data["by_local"]
            ],
        },
        "searches": {
            "total": data["total_searches"],
            "by_term": [
                {"label": row["rotulo"], "total": row["total"]}
                for row in data["searches_by_term"]
            ],
            "by_region": [
                {"label": row["rotulo"], "total": row["total"]}
                for row in data["searches_by_region"]
            ],
        },
        "users": {
            "total": data["total_users"],
            "by_profile": [
                {"label": row["rotulo"], "total": row["total"]}
                for row in data["by_profile"]
            ],
        },
    })


@api_reports_bp.get("/reports/occurrences")
@_api_admin_only
def api_report_occurrences():
    """Return filtered occurrence records without user-identifying fields."""
    filters, error = _api_filters()
    if error:
        return jsonify({"erro": error}), 400
    try:
        rows = _occurrences(filters)
    except (mysql.connector.Error, ConnectionError):
        current_app.logger.exception("Falha ao consultar o relatório de ocorrências.")
        return jsonify({"erro": "Falha ao consultar o banco de dados."}), 503

    items = []
    for row in rows:
        occurrence_date = row["hora"] or row["data"]
        items.append({
            "id": row["id"],
            "type": row["tipo"],
            "description": row["descricao"],
            "date": occurrence_date.isoformat() if occurrence_date else None,
            "status": row["status"],
            "location": {
                "id": row["local_codigo"],
                "address": row["endereco"],
            },
        })
    return jsonify({
        "filters": {
            "start_date": filters["start_date"] or None,
            "end_date": filters["end_date"] or None,
            "type_id": int(filters["tipo"]) if filters["tipo"] else None,
            "status": filters["status"] or None,
            "location_id": int(filters["local"]) if filters["local"] else None,
        },
        "total": len(items),
        "occurrences": items,
    })


@admin_bp.get("/tipos")
@_admin_only
def types():
    tipos = _fetch_all(
        """SELECT t.idtipoOcorrencia AS id, t.nome, t.descricao,
                  t.Local_codigo AS local_codigo, l.endereco,
                  (SELECT COUNT(*) FROM Ocorrencia o
                   WHERE o.tipoOcorrencia_idtipoOcorrencia = t.idtipoOcorrencia) AS ocorrencias,
                  (SELECT COUNT(*) FROM alerta a
                   WHERE a.tipoOcorrencia_idtipoOcorrencia = t.idtipoOcorrencia) AS alertas
           FROM tipoOcorrencia t JOIN Local l ON l.codigo = t.Local_codigo
           ORDER BY t.nome, t.idtipoOcorrencia"""
    )
    locais = _fetch_all("SELECT codigo, endereco FROM Local ORDER BY codigo")
    return _page("Tipos de ocorrência", TYPES_BODY, tipos=tipos, locais=locais)


@admin_bp.post("/tipos")
@_admin_only
def create_type():
    _require_csrf()
    values, error = _type_form_values()
    if error:
        flash(error, "error")
        return redirect(url_for("admin.types"))
    try:
        connection = _connect()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT codigo FROM Local WHERE codigo = %s", (values["local_codigo"],))
            if not cursor.fetchone():
                flash("O local selecionado não existe.", "error")
                return redirect(url_for("admin.types"))
            cursor.execute(
                "SELECT idtipoOcorrencia FROM tipoOcorrencia WHERE Local_codigo = %s AND nome = %s",
                (values["local_codigo"], values["nome"]),
            )
            if cursor.fetchone():
                flash("Já existe um tipo com esse nome para o local.", "error")
                return redirect(url_for("admin.types"))
            cursor.execute("SELECT COALESCE(MAX(idtipoOcorrencia), 0) + 1 FROM tipoOcorrencia")
            next_id = cursor.fetchone()[0]
            cursor.execute(
                """INSERT INTO tipoOcorrencia (idtipoOcorrencia, nome, descricao, Local_codigo)
                   VALUES (%s, %s, %s, %s)""",
                (next_id, values["nome"], values["descricao"], values["local_codigo"]),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
    except IntegrityError:
        flash("Não foi possível cadastrar. Confira os dados e tente novamente.", "error")
    else:
        flash("Tipo cadastrado.", "success")
    return redirect(url_for("admin.types"))


@admin_bp.post("/tipos/<int:type_id>/editar")
@_admin_only
def update_type(type_id):
    _require_csrf()
    name = (request.form.get("nome") or "").strip()
    description = (request.form.get("descricao") or "").strip()
    if not name or len(name) > 45 or len(description) > 255:
        flash("Confira o nome (até 45 caracteres) e a descrição (até 255 caracteres).", "error")
        return redirect(url_for("admin.types"))
    if not _valid_domain_text(name) or (description and not _valid_domain_text(description)):
        flash("Use apenas letras, números, espaços, vírgulas e pontos, sem pontuação repetida.", "error")
        return redirect(url_for("admin.types"))
    current = _fetch_one(
        """SELECT t.idtipoOcorrencia AS id, t.nome, t.Local_codigo AS local_codigo,
                  (SELECT COUNT(*) FROM Ocorrencia o
                   WHERE o.tipoOcorrencia_idtipoOcorrencia = t.idtipoOcorrencia) AS ocorrencias,
                  (SELECT COUNT(*) FROM alerta a
                   WHERE a.tipoOcorrencia_idtipoOcorrencia = t.idtipoOcorrencia) AS alertas
           FROM tipoOcorrencia t WHERE t.idtipoOcorrencia = %s""",
        (type_id,),
    )
    if not current:
        flash("Esse tipo não existe mais.", "error")
        return redirect(url_for("admin.types"))
    if (current["ocorrencias"] or current["alertas"]) and name != current["nome"]:
        flash("O nome não pode mudar porque o tipo já está ligado ao histórico; a descrição pode ser atualizada.", "error")
        return redirect(url_for("admin.types"))
    duplicate = _fetch_one(
        """SELECT idtipoOcorrencia FROM tipoOcorrencia
           WHERE Local_codigo = %s AND nome = %s AND idtipoOcorrencia <> %s""",
        (current["local_codigo"], name, type_id),
    )
    if duplicate:
        flash("Já existe um tipo com esse nome para o local.", "error")
        return redirect(url_for("admin.types"))
    _execute(
        "UPDATE tipoOcorrencia SET nome = %s, descricao = %s WHERE idtipoOcorrencia = %s",
        (name, description or None, type_id),
    )
    flash("Tipo atualizado.", "success")
    return redirect(url_for("admin.types"))


@admin_bp.post("/tipos/<int:type_id>/excluir")
@_admin_only
def delete_type(type_id):
    _require_csrf()
    current = _fetch_one(
        """SELECT t.nome, t.Local_codigo AS local_codigo,
                  (SELECT COUNT(*) FROM Ocorrencia o
                   WHERE o.tipoOcorrencia_idtipoOcorrencia = t.idtipoOcorrencia) AS ocorrencias,
                  (SELECT COUNT(*) FROM alerta a
                   WHERE a.tipoOcorrencia_idtipoOcorrencia = t.idtipoOcorrencia) AS alertas
           FROM tipoOcorrencia t WHERE t.idtipoOcorrencia = %s""",
        (type_id,),
    )
    if not current:
        flash("Esse tipo não existe mais.", "error")
    elif current["ocorrencias"] or current["alertas"]:
        flash("O tipo está ligado a ocorrências ou alertas e foi preservado no histórico.", "error")
    else:
        _execute("DELETE FROM tipoOcorrencia WHERE idtipoOcorrencia = %s", (type_id,))
        flash("Tipo excluído.", "success")
    return redirect(url_for("admin.types"))


@reports_bp.get("/")
@_admin_only
def index():
    return _page("Relatórios de ocorrências", REPORTS_BODY, **_report_data(_filters()))


@reports_bp.get("/exportar.csv")
@_admin_only
def export_csv():
    rows = _occurrences(_filters())
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["ID", "Data/hora", "Tipo", "Status", "Local", "Descrição"])
    for row in rows:
        if row["hora"]:
            when = row["hora"].strftime("%d/%m/%Y %H:%M")
        elif row["data"]:
            when = row["data"].strftime("%d/%m/%Y")
        else:
            when = ""
        writer.writerow([row["id"], when, row["tipo"] or "", row["status"] or "",
                         row["endereco"] or f"Local #{row['local_codigo']}", row["descricao"] or ""])
    response = make_response("\ufeff" + output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio-ocorrencias.csv"
    return response


def register_admin_reports(app, *, register_home=True):
    """Register admin and report routes on the group's existing Flask app."""
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = os.getenv("ALERTADF_SECRET_KEY") or secrets.token_hex(32)
    app.config.setdefault("ADMIN_PASSWORD_HASH", os.getenv("ALERTADF_ADMIN_PASSWORD_HASH", ""))
    app.config.setdefault("DB_HOST", os.getenv("ALERTADF_DB_HOST", "127.0.0.1"))
    app.config.setdefault("DB_PORT", int(os.getenv("ALERTADF_DB_PORT", "3306")))
    app.config.setdefault("DB_NAME", os.getenv("ALERTADF_DB_NAME", "sistemaOcorrencias"))
    app.config.setdefault("DB_USER", os.getenv("ALERTADF_DB_USER", ""))
    app.config.setdefault("DB_PASSWORD", os.getenv("ALERTADF_DB_PASSWORD", ""))
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")
    app.jinja_env.globals["csrf_token"] = _csrf_token
    app.register_blueprint(admin_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_reports_bp)

    if register_home:
        @app.get("/")
        def home():
            return redirect(url_for("reports.index" if session.get("is_admin") else "login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            _require_csrf()
            password_hash = current_app.config["ADMIN_PASSWORD_HASH"]
            if not password_hash:
                flash("Defina ALERTADF_ADMIN_PASSWORD_HASH no arquivo .env antes de entrar.", "error")
            elif check_password_hash(password_hash, request.form.get("password", "")):
                session.clear()
                session["is_admin"] = True
                _csrf_token()
                next_url = request.args.get("next", "")
                parsed = urlparse(next_url)
                if next_url.startswith("/") and not next_url.startswith("//") and not parsed.netloc:
                    return redirect(next_url)
                return redirect(url_for("reports.index"))
            else:
                flash("Senha incorreta.", "error")
        return _page("Acesso administrativo", LOGIN_BODY)

    @app.post("/logout")
    @_admin_only
    def logout():
        _require_csrf()
        session.clear()
        flash("Você saiu do painel.", "success")
        return redirect(url_for("login"))

    @app.errorhandler(mysql.connector.Error)
    def database_error(error):
        current_app.logger.exception("Database request failed: %s", error)
        return (
            _page(
                "Banco de dados indisponível",
                """<section class="card"><p>Não foi possível acessar o MySQL. Confira se o serviço está ligado e se ALERTADF_DB_* está correto no arquivo .env.</p>
                   <a class="button secondary" href="{{ url_for('reports.index') }}">Voltar aos relatórios</a></section>""",
            ),
            503,
        )

    return app


def create_app():
    """Create the standalone prototype for local use."""
    load_dotenv()
    app = Flask(__name__)
    register_admin_reports(app)
    return app


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    create_app().run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
