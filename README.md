# Clinoryn

Fundação de um sistema web para gestão de clínicas médicas, construída com Django Templates e PostgreSQL.

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

Validação local atual: 43 testes e 83% de cobertura.

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

## Backup

Faça backups regulares do volume PostgreSQL e do volume `private_media`. Ambos são necessários para uma restauração completa. Documentos privados nunca devem ser publicados diretamente pelo Nginx.

## Screenshots

Adicione capturas dos dashboards administrativo, médico, recepção e paciente em `docs/screenshots/` antes da publicação final do portfólio. Não use dados reais ou identificáveis nas imagens.

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

## Roadmap

As próximas etapas adicionarão perfis clínicos/administrativos, especialidades, agenda, agendamentos, recepção, prontuário, documentos, financeiro, auditoria e infraestrutura de produção.
