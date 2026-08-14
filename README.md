# Clinoryn

<p align="center">
  <strong>Plataforma full-stack para gestão segura e rastreável de clínicas médicas</strong>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img alt="Django" src="https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white">
  <img alt="REST API" src="https://img.shields.io/badge/REST_API-4B8BBE">
  <a href="https://github.com/Wwerneck/sistema-Clinoryn/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/Wwerneck/sistema-Clinoryn/actions/workflows/ci.yml/badge.svg?branch=master"></a>
  <a href="./CHANGELOG.md"><img alt="Release" src="https://img.shields.io/badge/release-v1.0.0-2ea44f"></a>
</p>

> Projeto de portfólio desenvolvido por [Weslley Werneck](https://github.com/Wwerneck).
>
> A **Clinoryn** centraliza a operação de uma clínica em uma aplicação web com controle de acesso por perfil, agenda médica, prontuário eletrônico, exames, prescrições, financeiro, auditoria e API REST versionada.

## Avaliação rápida

- **Backend e regras de negócio:** perfis, autorização por objeto, agenda transacional, prontuário, financeiro e auditoria.
- **Qualidade:** 48 testes, cobertura local de 83% e CI com lint, migrations e testes.
- **Como testar:** suba a aplicação com Docker, execute `python manage.py seed_demo` e entre com uma das contas demonstrativas descritas abaixo.

## Visão executiva

A Clinoryn foi criada para demonstrar competências de desenvolvimento backend aplicadas a um domínio com regras de negócio reais: modelagem, transações, autorização, proteção de dados, qualidade de código e execução em containers.

### Destaques técnicos

- **Controle de acesso por perfil e por objeto:** administradores, médicos, recepção e pacientes acessam somente os dados relacionados às suas responsabilidades e vínculos.
- **Agenda com regras de negócio:** disponibilidade, bloqueios, conflitos, reagendamentos e estados do atendimento são validados pelo backend.
- **Dados clínicos protegidos:** documentos privados, segregação entre dados clínicos e administrativos e auditoria de operações sensíveis.
- **API pronta para integração:** Django REST Framework, autenticação JWT, documentação OpenAPI e CORS configurável.
- **Entrega profissional:** Docker, Gunicorn, Nginx, health checks, GitHub Actions, Ruff e testes automatizados.

## Stack

| Camada | Tecnologias |
| --- | --- |
| Backend | Python, Django, Django REST Framework |
| Dados | PostgreSQL, Django ORM |
| Segurança | JWT, RBAC, permissões por objeto, auditoria |
| Infraestrutura | Docker, Gunicorn, Nginx, health checks |
| Qualidade | GitHub Actions, Ruff, testes Django, Coverage |

## Evidências no projeto

| Indicador | Evidência |
| --- | --- |
| Escopo funcional | 12 etapas implementadas |
| Testes automatizados | 48 testes |
| Cobertura local | 83% |
| API | REST versionada em `/api/v1/` |
| Integração contínua | Lint, migrations, testes e cobertura no CI |

## Escopo atual — Etapas 1 a 12

- Custom User Model criado antes da primeira migration;
- perfis `ADMIN`, `MEDICO`, `RECEPCAO` e `PACIENTE`;
- login, logout e redirecionamento por perfil;
- autorização no backend para cada dashboard;
- settings separados para desenvolvimento e produção;
- configuração PostgreSQL via ambiente;
- testes de autenticação e isolamento inicial de perfis.
- perfis de paciente, médico e profissional da recepção;
- cadastro e consulta de especialidades;
- cadastros transacionais de usuários e seus perfis;
- validação de CPF, unicidade de CPF e CRM;
- pesquisa paginada de pacientes e médicos;
- menus e permissões específicos por perfil.
- disponibilidade semanal por médico;
- duração configurável dos atendimentos;
- bloqueios por férias, feriados, reunião, compromisso ou indisponibilidade;
- prevenção de períodos inválidos, duplicados e sobrepostos;
- médico restrito à própria agenda e recepção com acesso somente de leitura.
- criação e reagendamento de consultas por administrador, recepção ou paciente;
- cancelamento com liberação do horário;
- validação transacional de jornada, bloqueios e horários passados;
- prevenção de conflito simultâneo do médico e do paciente;
- valor, especialidade e autor da operação definidos no backend.
- dashboard operacional da recepção com seis indicadores diários;
- agenda diária com filtro por data e atalhos operacionais;
- confirmação, check-in, entrada na fila e registro de ausência;
- máquina de estados transacional que impede mudanças arbitrárias;
- telas da recepção limitadas a dados administrativos.
- dashboard individual do médico;
- agenda própria e fila de pacientes aguardando;
- início e conclusão do atendimento com transições controladas;
- indicadores diários, mensais e produção estimada;
- isolamento de consultas entre médicos, inclusive nas URLs de ação.
- prontuário eletrônico vinculado à consulta;
- queixa, sintomas, histórico, alergias, antecedentes e diagnóstico;
- evoluções clínicas em timeline cronológica;
- escrita restrita ao médico responsável pelo atendimento;
- histórico disponível somente mediante vínculo assistencial;
- recepção totalmente bloqueada das informações clínicas.
- prescrições com múltiplos medicamentos e orientações;
- registro e disponibilização de exames por consulta;
- uploads limitados a PDF, JPG, JPEG e PNG, até 10 MB;
- arquivos médicos privados entregues somente por view autorizada;
- paciente acessa apenas os próprios exames e prescrições.
- pagamentos por consulta com forma, status e responsável;
- separação entre valor da consulta e valor efetivamente recebido;
- dashboards financeiros calculados no backend;
- recepção e administração registram pagamentos;
- médico e paciente visualizam apenas seus próprios valores.
- auditoria central de autenticação e operações sensíveis;
- registro de usuário, objeto, IP, user-agent e horário;
- metadados minimizados, sem replicar conteúdo clínico;
- consulta paginada de logs exclusiva do administrador.
- containers separados para PostgreSQL, Django/Gunicorn e Nginx;
- volumes persistentes para banco, estáticos e documentos privados;
- health checks de vida e prontidão;
- settings de produção com cookies seguros, HSTS e HTTPS;
- Nginx sem acesso ao volume de documentos clínicos privados.
- dashboards executivo e do paciente com dados reais;
- rankings administrativos e indicadores mensais;
- comando idempotente de dados demonstrativos;
- GitHub Actions com lint, migrations, testes e cobertura mínima;
- cobertura automatizada superior a 80%.

As doze etapas planejadas estão implementadas. Melhorias futuras estão listadas no roadmap.

## Demonstração local

Para popular um ambiente exclusivamente demonstrativo:

```powershell
python manage.py seed_demo
```

O comando pode ser repetido e cria as contas `demo_admin`, `demo_medico`, `demo_recepcao` e `demo_paciente`, todas com a senha local `Demo@123456`. Nunca execute esse comando em produção e troque as credenciais caso o ambiente fique acessível em rede.

## Integração contínua

O workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) executa em pushes e pull requests:

1. instalação das dependências;
2. Ruff;
3. verificação de migrations ausentes;
4. testes Django;
5. relatório de cobertura com mínimo de 70%.

Validação local atual: 48 testes e 83% de cobertura.

## Execução com Docker

Instale Docker Desktop, copie `.env.example` para `.env` e defina obrigatoriamente uma `SECRET_KEY` aleatória com pelo menos 50 caracteres e uma senha forte em `DATABASE_PASSWORD`.

```powershell
Copy-Item .env.example .env
docker compose config
docker compose up --build -d
docker compose exec web python manage.py createsuperuser
docker compose ps
```

Acesse `http://localhost:8080`. Para esse teste HTTP local, use `SECURE_SSL_REDIRECT=False`. Em produção real, configure TLS no proxy/load balancer, `CSRF_TRUSTED_ORIGINS=https://seu-dominio` e `SECURE_SSL_REDIRECT=True`.

```powershell
docker compose logs -f web
docker compose down
```

Não use `docker compose down -v` em ambiente com dados: a opção `-v` remove os volumes persistentes.

## Health checks

- `/health/live/`: confirma que o processo responde;
- `/health/ready/`: confirma também a conexão com o banco.

## REST API

A Clinoryn também expõe uma API REST versionada com Django REST Framework.

Base URL:

```text
/api/v1/
```

Documentação interativa:

```text
/api/schema/
/api/docs/
/api/redoc/
```

Em produção, a documentação pode ser protegida com:

```text
API_DOCS_REQUIRE_AUTH=True
```

Para consumo por frontends externos ou aplicativo mobile, configure CORS com origins explícitas:

```text
CORS_ALLOWED_ORIGINS=https://app.seu-dominio.com,https://mobile.seu-dominio.com
CORS_ALLOW_CREDENTIALS=False
```

Não use `CORS_ALLOW_ALL_ORIGINS` em produção.

Autenticação:

```text
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
GET  /api/v1/auth/me/
```

O login retorna tokens JWT `access` e `refresh`. Requisições autenticadas devem enviar:

```text
Authorization: Bearer <access-token>
```

Principais endpoints:

```text
GET  /api/v1/me/
GET  /api/v1/me/consultas/
GET  /api/v1/me/exames/
GET  /api/v1/me/prescricoes/
GET  /api/v1/me/pagamentos/

GET  /api/v1/pacientes/
POST /api/v1/pacientes/
GET  /api/v1/pacientes/{id}/
PATCH /api/v1/pacientes/{id}/

GET  /api/v1/medicos/
GET  /api/v1/medicos/{id}/
GET  /api/v1/medicos/{id}/agenda/
GET  /api/v1/medicos/{id}/consultas/

GET  /api/v1/especialidades/
POST /api/v1/especialidades/
PATCH /api/v1/especialidades/{id}/

GET  /api/v1/agenda/disponibilidades/
GET  /api/v1/agenda/bloqueios/

GET  /api/v1/consultas/
POST /api/v1/consultas/
PATCH /api/v1/consultas/{id}/
POST /api/v1/consultas/{id}/cancelar/
POST /api/v1/consultas/{id}/confirmar/
POST /api/v1/consultas/{id}/check-in/
POST /api/v1/consultas/{id}/aguardar/
POST /api/v1/consultas/{id}/iniciar/
POST /api/v1/consultas/{id}/finalizar/
POST /api/v1/consultas/{id}/nao-compareceu/
GET  /api/v1/consultas/horarios-disponiveis/?medico=&data=

GET  /api/v1/prontuarios/
POST /api/v1/prontuarios/
PATCH /api/v1/prontuarios/{id}/
POST /api/v1/prontuarios/{id}/evolucoes/

GET  /api/v1/prescricoes/
POST /api/v1/prescricoes/

GET  /api/v1/exames/
POST /api/v1/exames/
GET  /api/v1/exames/{id}/arquivo/

GET  /api/v1/financeiro/pagamentos/
POST /api/v1/financeiro/pagamentos/
PATCH /api/v1/financeiro/pagamentos/{id}/
GET  /api/v1/financeiro/pagamentos/resumo/
```

Listagens usam paginação DRF:

```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": []
}
```

Filtros, busca e ordenação estão disponíveis nos endpoints compatíveis via `django-filter`, `search` e `ordering`. Campos sensíveis não são expostos por serializers públicos, e dados clínicos/financeiros são filtrados no backend conforme o perfil autenticado.

## API Architecture

A arquitetura atual mantém a interface web Django Templates e a API REST em paralelo:

```text
Django Templates
↓
Views web existentes
↓
Services / Selectors
↓
Django ORM
↓
PostgreSQL

API REST
↓
Django REST Framework
↓
Services / Selectors
↓
Django ORM
↓
PostgreSQL
```

Essa abordagem evita duplicar models, tabelas e regras de negócio. Operações críticas, como agendamento, cancelamento, transição de status de consulta e registro de pagamento, reutilizam os services existentes (`consultas.services` e `financeiro.services`). Assim, a interface web e a API compartilham a mesma fonte de verdade para validações, transações, auditoria e persistência.

Os endpoints aplicam isolamento por perfil e permissão por objeto para reduzir risco de IDOR. Pacientes acessam seus dados preferencialmente por `/api/v1/me/...`, médicos ficam restritos aos vínculos assistenciais e à própria agenda, e a recepção não recebe acesso a conteúdo clínico sensível.

## Backup

Faça backups regulares do volume PostgreSQL e do volume `private_media`. Ambos são necessários para uma restauração completa. Documentos privados nunca devem ser publicados diretamente pelo Nginx.

## Evidências visuais

O diretório [`docs/screenshots/`](docs/screenshots/) está reservado para capturas feitas apenas com dados sintéticos. O [roteiro de demonstração](docs/screenshots/README.md) define as telas mais relevantes e as regras para não expor dados identificáveis.

## Roadmap

- notificações por e-mail/SMS com consentimento;
- emissão de prescrições e comprovantes em PDF;
- testes de concorrência executados diretamente em PostgreSQL no CI;
- política automatizada de retenção e anonimização LGPD;
- integração com provedores de pagamento e assinatura digital.

## Arquitetura

```text
config/settings/       configurações base, desenvolvimento e produção
accounts/              identidade, autenticação e autorização inicial
dashboards/            roteamento e páginas iniciais por perfil
especialidades/         catálogo de especialidades médicas
pacientes/              perfil e cadastro administrativo de pacientes
medicos/                perfil profissional dos médicos
recepcao/               perfis individuais da equipe de recepção
agenda/                 disponibilidade semanal e bloqueios médicos
consultas/              agendamento, reagendamento e cancelamento
prontuarios/             registro clínico e timeline de evoluções
prescricoes/             prescrições e itens de medicamentos
exames/                  exames e downloads privados
financeiro/              pagamentos e indicadores financeiros
auditoria/               rastreabilidade de operações sensíveis
templates/             templates compartilhados
static/                CSS e futuros assets
```

## Instalação local

Requer Python 3.11+, PostgreSQL e um banco/usuário compatíveis com o `.env`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
python manage.py makemigrations accounts
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

O superusuário recebe automaticamente o perfil `ADMIN`. Acesse `http://127.0.0.1:8000/conta/entrar/`.

## Testes e qualidade

```powershell
python manage.py test
ruff check .
```

Por padrão, a suíte rápida usa SQLite em memória. Testes futuros de concorrência e constraints específicas também serão executados contra PostgreSQL.

## Permissões atuais

- `ADMIN`: gerencia especialidades, médicos, recepção e pacientes;
- `RECEPCAO`: pesquisa e cadastra pacientes, consulta médicos e especialidades;
- `MEDICO`: pesquisa pacientes e consulta especialidades;
- `PACIENTE`: consulta médicos ativos e especialidades ativas.

Na agenda, `ADMIN` gerencia qualquer médico, `MEDICO` gerencia apenas a própria configuração e `RECEPCAO` possui acesso somente de leitura.

Todas as permissões são verificadas no backend. A alteração do menu não substitui autorização.

## Segurança

Produção exige `SECRET_KEY`, cookies seguros, HTTPS e HSTS. O acesso às dashboards é validado no backend; ocultar links no frontend nunca é tratado como autorização.
