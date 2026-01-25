# Regras de Negócio e Validações Críticas – Sistema de Gestão Educacional

## 1. Objetivo deste Documento

Definir as políticas, critérios e validações obrigatórias do domínio educacional, independentes da implementação técnica (API, frontend ou banco).
Estas regras devem ser aplicadas em todos os pontos de entrada (API, jobs, interface admin, portal do aluno) para garantir conformidade legal, pedagógica e operacional.

Referências principais:
- Lei de Diretrizes e Bases da Educação (LDB – Lei 9.394/1996 e atualizações)
- Base Nacional Comum Curricular (BNCC)
- Resoluções CNE/CP e normativas estaduais/municipais
- Requisitos do Censo Escolar (INEP/MEC)
- Boas práticas de gestão escolar (progressão continuada vs. reprovação fundamentada)

## 2. Regras Gerais do Domínio

- Todo lançamento (frequência, nota, aula) só é permitido em **período letivo ativo** e **turma ativa**.
- Matrículas só podem ser criadas/trancadas/canceladas/concluídas em período letivo ativo.
- Ações de estado (ativar turma, aplicar avaliação, gerar boletim) são irreversíveis ou exigem justificativa auditável.
- Todas as validações de negócio retornam 422 Unprocessable Entity com código legível (ex: `frequencia_insuficiente_para_aprovacao`).

## 3. Validações por Recurso / Fluxo Crítico

### 3.1 Períodos Letivos
- Não pode haver sobreposição de datas entre períodos letivos da mesma instituição.
- Só um período pode estar **ativo** por vez (regra configurável por instituição).
- Encerrar período → bloqueia novos lançamentos de nota/frequência nesse período.

### 3.2 Turmas e Horários
- Turma só pode ser ativada se associada a período letivo ativo e com pelo menos 1 matrícula.
- Conflito de horário: professor não pode ter 2 aulas no mesmo dia/horário; sala idem.
- Substituição temporária de professor válida apenas para data específica.

### 3.3 Matrículas
- Aluno só pode ter 1 matrícula ativa por turma/classe no mesmo período.
- Trancamento: só permitido após X dias letivos iniciados (configurável, ex: 30 dias).
- Cancelamento: permitido a qualquer momento, mas gera registro para Censo (abandono).
- Conclusão automática ao final do período se critérios de aprovação atendidos.

### 3.4 Frequência
- Percentual mínimo de frequência para aprovação: configurável por instituição (padrão MEC: 75% para ensino fundamental/médio regular).
- Faltas injustificadas ≥ 5 consecutivas → alerta automático de Busca Ativa.
- Percentual < 75% → reprovação automática (salvo justificativa pedagógica aprovada por coordenador).
- Frequência consolidada só gerada após encerramento do período ou bimestre.

### 3.5 Avaliações e Notas
- Avaliação só pode ser aplicada se turma ativa e período letivo em andamento.
- Lançamento de nota só para matrículas ativas e avaliação aplicada/não encerrada.
- Nota mínima para aprovação por avaliação: configurável (ex: 5.0 ou 60%).
- Média final: ponderada por pesos das avaliações (configurável por classe/disciplina).
- Recuperação: aluno com média < 5.0 ou frequência insuficiente entra em recuperação paralela ou final (regra por BNCC/LDB).

### 3.6 Boletins e Aprovação/Reprovação
- Critérios de aprovação por disciplina (média ≥ mínima E frequência ≥ mínima).
- Aprovação global: todas disciplinas aprovadas OU recuperação aprovada.
- Reprovação: pelo menos 1 disciplina reprovada sem recuperação OU frequência global insuficiente.
- Boletim final só gerado após encerramento do período letivo.
- Histórico escolar mantém registro de todas as reprovações (para fins de transferência).

### 3.7 Busca Ativa / Monitoramento de Evasão
- Alerta automático se:
  - ≥ 5 faltas consecutivas (não justificadas)
  - ≥ 25% de faltas no bimestre
  - Ausência prolongada > 15 dias letivos
- Registro de contato obrigatório antes de marcar como "evadido".
- Relatório para Censo Escolar: exporta alunos com status de abandono/evasão.

### 3.8 Notificações e Comunicação
- Notificação automática para responsável em casos de:
  - Faltas excessivas
  - Nota baixa lançada
  - Boletim disponível
  - Evento próximo (prova, reunião)
- Notificações sensíveis (ex: reprovação) exigem confirmação de leitura.

## 4. Regras Legais e Conformidade (Brasil 2025–2026)

- Censo Escolar: exportação anual de matrículas, frequência, abandono, reprovações (formato INEP).
- Progressão continuada vs. reprovação fundamentada: configurável por instituição (algumas redes estaduais adotam progressão; outras reprovam com base em nota/frequência).
- Acessibilidade: portal do aluno deve suportar WCAG 2.1 (leitura de tela para boletins).
- LGPD: consentimento explícito para envio de notificações; logs de acesso a dados pessoais.

## 5. Mapeamento para a API

| Regra de Negócio                          | Endpoint/Ação Afetada                  | Código de Erro Esperado                  |
|-------------------------------------------|----------------------------------------|------------------------------------------|
| Frequência < 75% impede aprovação         | POST /boletins/gerar                   | `frequencia_insuficiente`                |
| Conflito de horário professor             | POST /horarios/                        | `conflito_horario_professor`             |
| Lançar nota em avaliação encerrada        | POST /notas/                           | `avaliacao_encerrada`                    |
| Matrícula duplicada no período            | POST /matriculas/                      | `matricula_duplicada`                    |
| Alerta busca ativa                        | (job assíncrono)                       | Gera notificação + alerta no dashboard   |

## 6. Manutenção e Evolução

- Regras configuráveis pela instituição (via admin) sempre que possível (ex: % frequência mínima, nota mínima).
- Toda mudança em regra crítica deve gerar migration + teste de integração.
- Auditoria: log de quem alterou estado crítico (ex: encerrou período, gerou boletim).
