
# Definição da API REST – Sistema de Gestão Educacional

## 1. Objetivo da API

API RESTful segura, desacoplada e orientada a domínio, expondo funcionalidades completas de gestão educacional (básica e superior) para consumo por web, mobile, portal do aluno/responsável e integrações externas (ex.: Censo Escolar MEC).

A API **não espelha o banco de dados**, mas reflete casos de uso reais, com ações explícitas para transições de estado e regras de negócio.

# Definição da API REST – Sistema de Gestão Educacional

## 2. Stack Tecnológica

| Item                          | Tecnologia / Ferramenta                          | Observação / Versão Recomendada                  |
|-------------------------------|--------------------------------------------------|--------------------------------------------------|
| Linguagem                     | Python                                           | 3.12                                             |
| Framework Web                 | Django                                           | 5.0+ ou 5.1                                      |
| API REST                      | Django REST Framework (DRF)                      | 3.15+                                            |
| Banco de Dados                | PostgreSQL                                       | 15+ ou 16                                        |
| Autenticação                  | JWT (Simple JWT ou djangorestframework-simplejwt) | Tokens de acesso + refresh                       |
| Gerenciamento de Configurações| python-dotenv + variáveis de ambiente (.env)     | SECRET_KEY, DATABASE_URL, etc.                   |
| Documentação Automática       | drf-spectacular (recomendado) ou drf-yasg        | OpenAPI 3.1 / Swagger UI + Redoc                 |
| Internacionalização (i18n)    | Django gettext + django-rosetta (opcional)       | Suporte a pt_BR + en_US (futuro multilíngue)     |
| Controle de Acesso            | RBAC via permissões customizadas DRF             | IsAdminUser, IsAuthenticated, permissões por papel |
| Outras recomendações          | Celery + Redis (tarefas assíncronas)             | Notificações, geração de boletins, alertas       |
|                               | django-filter + django-environ                   | Filtros avançados + env mais robusto             |

## 3. Princípios de Design da API

- Base URL: `/api/v1/`
- Versionamento explícito via path (`v1`)
- Recursos no plural
- Uso correto de verbos HTTP
- Ações de domínio via `@action` (POST em sub-recursos)
- Respostas padronizadas com `drf-spectacular`
- Internacionalização: mensagens de erro e labels traduzíveis via `gettext_lazy`
- Autenticação: `Authorization: Bearer <access_token>` (JWT)
- Paginação: PageNumberPagination ou LimitOffsetPagination
- Filtros e ordenação: django-filter + SearchFilter + OrderingFilter

## 4. Recursos Principais (Endpoints Sugeridos)

### Instituições / Mantenedoras e Unidades de Ensino

- `POST /api/v1/instituicoes/`
- `GET /api/v1/instituicoes/{id}/`
- `PATCH /api/v1/instituicoes/{id}/`
- `GET /api/v1/instituicoes/{id}/unidades/`
- `POST /api/v1/instituicoes/{instituicao_id}/unidades/`
- `GET /api/v1/unidades/{id}/`

### Períodos Letivos

- `POST /api/v1/unidades/{unidade_id}/periodos-letivos/`
- `GET /api/v1/periodos-letivos/{id}/`
- `POST /api/v1/periodos-letivos/{id}/ativar/`
- `POST /api/v1/periodos-letivos/{id}/encerrar/`

### Turmas e Matrículas

- `POST /api/v1/unidades/{unidade_id}/turmas/`
- `GET /api/v1/turmas/{id}/`
- `POST /api/v1/turmas/{id}/ativar/`
- `POST /api/v1/turmas/{id}/matriculas/`
- `GET /api/v1/alunos/{aluno_id}/matriculas/`
- `POST /api/v1/matriculas/{id}/trancar/`
- `POST /api/v1/matriculas/{id}/concluir/`

### Horários, Aulas e Frequência

- `POST /api/v1/turmas/{turma_id}/horarios/`
- `POST /api/v1/turmas/{turma_id}/aulas/`
- `POST /api/v1/aulas/{aula_id}/frequencias/` (lote possível)
- `GET /api/v1/matriculas/{matricula_id}/frequencia/`

### Avaliações e Notas

- `POST /api/v1/turmas/{turma_id}/avaliacoes/`
- `POST /api/v1/avaliacoes/{id}/aplicar/`
- `POST /api/v1/avaliacoes/{avaliacao_id}/notas/` (bulk create suportado)
- `GET /api/v1/matriculas/{matricula_id}/notas/`

### Boletins e Materiais

- `POST /api/v1/matriculas/{matricula_id}/boletins/gerar/`
- `GET /api/v1/matriculas/{matricula_id}/boletins/`
- `POST /api/v1/turmas/{turma_id}/materiais/` (upload de arquivos)

### Eventos, Busca Ativa e Notificações

- `POST /api/v1/turmas/{turma_id}/eventos/`
- `GET /api/v1/unidades/{unidade_id}/alertas-busca-ativa/`
- `POST /api/v1/notificacoes/` (com envio assíncrono via Celery)

## 5. Autenticação e Autorização (RBAC)

- **Autenticação**: `djangorestframework-simplejwt`
  - `POST /api/v1/token/` → Obter access + refresh
  - `POST /api/v1/token/refresh/` → Renovar token
- **Permissões customizadas** (exemplos):
  - `IsProfessorDaTurma`
  - `IsCoordenadorDaUnidade`
  - `IsAlunoOuResponsavelDono`
  - `IsAdminDaInstituicao`
- Uso: `@permission_classes([IsAuthenticated, IsProfessorDaTurma])`

## 6. Internacionalização (i18n)

- Configuração em `settings.py`:
  ```python
  LANGUAGE_CODE = 'pt-br'
  LANGUAGES = [('pt-br', 'Português'), ('en', 'English')]
  USE_I18N = True
  LOCALE_PATHS = [BASE_DIR / 'locale']

## 7. Conformidade e Observações

- Suporte a tipos MEC: Básica/Superior, Pública/Privada, EJA, Educação Especial
- Validações críticas: frequência ≥ 75%, nota mínima, progressão continuada (configurável por unidade)
- Exportação Censo Escolar: endpoints dedicados (futuro)
- LGPD: consentimento para notificações, logs de acesso

## 8. Valor para Portfólio

Demonstra domínio completo do ecossistema educacional brasileiro: hierarquia institucional, ciclo letivo, regras pedagógicas, conformidade MEC, portal do aluno e prevenção de evasão.

Pronto para escalar para redes públicas/privadas ou ensino superior.
```

