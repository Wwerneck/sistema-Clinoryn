# Como contribuir

Obrigado por contribuir com a Clinoryn.

## Antes de enviar uma mudança

1. Crie uma branch a partir de `master`.
2. Instale as dependências de desenvolvimento com `pip install -r requirements-dev.txt`.
3. Execute `ruff check .` e `python manage.py test`.
4. Nunca use dados clínicos reais, chaves ou credenciais em commits, screenshots ou exemplos.

## Padrão de commits

Use mensagens curtas no formato:

```text
feat: adiciona recurso
fix: corrige comportamento
test: cobre cenário
docs: atualiza documentação
ci: ajusta automação
```

## Pull requests

Descreva o problema, a solução, os testes executados e qualquer impacto em permissões, segurança ou dados.
