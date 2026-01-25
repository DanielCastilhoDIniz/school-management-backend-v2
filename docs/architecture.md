```markdown
# Definição da API REST – Sistema de Gestão Educacional

## 1. Objetivo da API

Esta API REST expõe funcionalidades completas do domínio educacional brasileiro de forma segura, previsível e desacoplada, permitindo o consumo por aplicações web, mobile, portal do aluno/responsável e integrações externas.

A API é 100% orientada a recursos e casos de uso reais, nunca espelhando diretamente as entidades do banco de dados.

---

## 2. Princípios de Design

* Versionamento explícito da API (`v1`)
* Uso consistente e correto de verbos HTTP
* Recursos nomeados no plural
* Estados do domínio controlam rigorosamente as ações permitidas
* Todas as regras de negócio são aplicadas antes da persistência
* Endpoints aninhados para hierarquias naturais (turma → aulas, matrículas, materiais, etc.)

---

## 3. Recursos Principais

### Instituições · Períodos Letivos · Classes · Disciplinas
(Conforme versão anterior – mantidos)

### Turmas · Matrículas · Alunos · Professores · Registros de Aula · Frequência · Avaliações · Notas · Boletins · Notificações
(Conforme versão anterior – mantidos e aprimorados)

### Horários / Grade Horária

Recurso responsável pelo planejamento semanal de aulas e gestão de alocação de professores e salas.

Ações expostas:

* Criar grade horária para uma turma ou período letivo
* Associar professor, disciplina e sala a cada horário
* Validar conflitos (professor ou sala já alocados no mesmo horário)
* Listar horários por turma, professor, sala ou período letivo
* Consultar grade completa da turma (visualização semanal)
* Substituir professor temporariamente (aula avulsa)

Observação:
* Validação automática de conflitos é obrigatória
* Integração com registros de aula (professor só pode dar aula em horário alocado)

### Gestão de Conteúdo / Materiais Didáticos / Biblioteca Digital

Recurso responsável pelo upload, organização e distribuição de materiais pedagógicos.

Ações expostas:

* Upload de material (PDF, vídeo, link externo, imagem, etc.)
* Vincular material a turma, disciplina, aula específica ou período letivo
* Listar materiais por turma/disciplina
* Consultar materiais disponíveis para o aluno logado
* Remover ou arquivar material
* Marcar material como "obrigatório" ou "complementar"

Observação:
* Alunos e responsáveis só têm acesso de leitura aos materiais das turmas em que estão matriculados
* Professores só podem gerenciar materiais de suas próprias turmas/disciplinas

### Eventos / Agenda Escolar

Recurso responsável pelo calendário institucional e comunicações de datas importantes.

Ações expostas:

* Criar evento (prova, reunião de pais, feriado, recuperação, atividade extracurricular, etc.)
* Associar evento a turmas, classes ou instituição inteira
* Listar agenda por período, turma, aluno ou responsável
* Enviar notificação automática antes do evento (configurável: 1 dia, 3 dias, 1 semana)
* Marcar evento como "prova" para integração com avaliações

Observação:
* Eventos do tipo "prova" podem bloquear lançamento de notas se ainda não aplicados
* Integração total com Notificações e Portal do Aluno

### Busca Ativa / Monitoramento de Evasão

Recurso responsável pela identificação precoce de risco de abandono escolar.

Ações expostas:

* Consultar alunos com ausência acima de X dias consecutivos ou percentual crítico
* Listar alertas ativos de busca ativa (por turma, classe ou instituição)
* Registrar contato com responsável (data, meio, observações)
* Marcar aluno como "retornado" ou "evadido"
* Gerar relatório de busca ativa (obrigatório para redes públicas – Educacenso)

Observação:
* Geração automática de alerta com base em regras configuráveis (ex: ≥ 5 faltas seguidas ou ≥ 25% de falta no bimestre)
* Disparo automático de notificação para coordenador e responsável
* Histórico completo de contatos mantido para auditoria

---

## 4. Ações de Domínio (não-CRUD)

* Ativar/Encerrar período letivo
* Ativar/Encerrar turma
* Trancar/Cancelar/Concluir matrícula
* Aplicar/Encerrar avaliação
* Consolidar frequência
* Gerar boletim parcial/final
* Validar conflitos de horário
* Disparar alerta de busca ativa
* Registrar contato de busca ativa

Essas ações representam transições de estado ou regras complexas de negócio – nunca são simples PATCHs.

---

## 5. Controle de Acesso (RBAC)

* Administradores → acesso total
* Coordenadores/Pedagógicos → acesso a horários, relatórios, busca ativa, materiais, eventos
* Professores → suas turmas (aulas, frequência, notas, materiais, horários, notificações)
* Alunos/Responsáveis → apenas dados próprios (boletim, frequência, materiais, agenda, notificações)
* Secretaria → matrículas, documentos, busca ativa (leitura/edição parcial)
* Financeiro → (módulo futuro)

---

## 6. Padrões de Resposta

* JSON padronizado com `_links` quando aplicável
* Códigos HTTP corretos (201, 422, 403, etc.)
* Erros de domínio sempre com `code` legível

Exemplo:
```json
422 Unprocessable Entity
{
  "detail": "Conflito de horário: o professor já possui aula alocada neste dia/horário.",
  "code": "conflito_horario_professor",
  "conflito": {
    "turma": "9º Ano A",
    "horario": "Segunda-feira 07:30-08:15"
  }
}
```

---

## 7. Uso no Projeto

Este documento orienta diretamente:

* Definição de ViewSets, GenericAPIView e @action no Django REST Framework
* Criação de permissões customizadas (IsProfessorDaTurma, IsAlunoDono, IsCoordenador, etc.)
* Serializers específicos por caso de uso (Create, List, Detail, Action)
* Documentação OpenAPI com drf-spectacular
* Implementação de regras de negócio via métodos de domínio ou services
* Jobs assíncronos (Celery) para alertas de busca ativa, notificações e validação de horários

---

## 8. Valor para Portfólio

Esta definição de API demonstra:

* Domínio profundo do ecossistema escolar brasileiro (2024–2026)
* Arquitetura REST madura, orientada a casos de uso e regras de negócio
* Suporte completo ao ciclo letivo real: planejamento → execução → avaliação → acompanhamento → intervenção → comunicação
* Preparação para redes públicas (busca ativa, Educacenso) e privadas (portal do aluno, materiais digitais)
* Visão de produto completa: do pedagógico ao engajamento familiar

