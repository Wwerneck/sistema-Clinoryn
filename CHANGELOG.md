# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.

## [Unreleased]

### Adicionado
- Configuração de demonstração pública com Docker, PostgreSQL e health check via `render.yaml`.
- Modo somente leitura para proteger os dados fictícios compartilhados com recrutadores.
- Serviço de arquivos estáticos pelo próprio Django em ambiente de hospedagem.

## [1.0.0] - 2026-08-14

### Destaques
- Plataforma de gestão clínica com perfis, agenda, prontuário, exames, prescrições, financeiro, auditoria e API REST.
- Controle de acesso por perfil e por objeto, autenticação JWT e proteção de dados sensíveis.
- Execução com Docker, PostgreSQL, Gunicorn, Nginx e health checks.
- Integração contínua com lint, migrations, testes e cobertura.
