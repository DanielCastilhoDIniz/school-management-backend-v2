Aqui vai um **mapeamento detalhado de user stories** para o seu SaaS de gestão escolar, baseado diretamente nas **personas** que construímos (Ana Clara, Mariana, Juliana, Prof. Carlos e Fernanda).

Usei o formato clássico:
**Como [tipo de usuário / persona], eu quero [funcionalidade/ação] para que [benefício/razão]**.

Incluí **critérios de aceitação** (Acceptance Criteria) detalhados para cada história, tornando-as prontas para refinamento em backlog, sprint planning ou desenvolvimento. Agrupei por persona e por módulo principal (ex.: Dashboard, Pedagógico, Financeiro, Comunicação, Portais).

Foco no **MVP**: priorizei histórias de alto impacto diário e valor imediato para adoção.

### 1. Ana Clara – Diretora/Gestora
**Módulo: Dashboard Executivo e Relatórios**

- **US-001**
  Como diretora, eu quero um dashboard com KPIs em tempo real na tela inicial para que eu acompanhe a saúde da escola sem precisar navegar em múltiplos menus.
  **Critérios de aceitação**:
  - Exibe inadimplência atual (%), frequência média global (%), retenção projetada (%), caixa do mês, NPS dos pais e % de rematrículas.
  - Atualização automática a cada 5 min (ou refresh manual).
  - Gráficos simples (pizza/barra) + números grandes.
  - Filtros por período (mês/ano/bimestre) e por unidade (se rede).
  - Alertas visuais (vermelho/amarelo) para indicadores críticos (<80% frequência, >15% inadimplência).

- **US-002**
  Como diretora, eu quero receber alertas automáticos por e-mail/push sobre alunos em risco de evasão para que eu intervenha cedo.
  **Critérios**:
  - Alerta disparado se aluno tiver >30% faltas OU média <5,0 no bimestre.
  - Lista com nome, turma, % faltas, média e link para perfil do aluno.
  - Configurável por regra (ex.: % mínimo de faltas).

- **US-003**
  Como diretora, eu quero gerar relatórios MEC prontos em PDF/Excel para que eu cumpra obrigações sem retrabalho manual.
  **Critérios**:
  - Relatórios Censo, Rendimento, Matrícula.
  - Exportação em 1 clique com dados filtrados por ano letivo.

### 2. Mariana – Coordenadora Pedagógica
**Módulo: Pedagógico e Acompanhamento**

- **US-004**
  Como coordenadora pedagógica, eu quero ver gráficos de desempenho por turma/disciplina/aluno para que eu identifique padrões de baixo rendimento rapidamente.
  **Critérios**:
  - Drill-down: escola → turma → aluno.
  - Métricas: média, % aprovados, faltas %.
  - Comparativo bimestre anterior.

- **US-005**
  Como coordenadora, eu quero configurar alertas automáticos para alunos de risco pedagógico para que eu acompanhe intervenções sem cobrança manual.
  **Critérios**:
  - Regras configuráveis (ex.: média <6 + faltas >20%).
  - Notificação push/e-mail + tarefa no sistema para criar plano de recuperação.

- **US-006**
  Como coordenadora, eu quero aprovar planos de aula e conteúdos postados pelos professores para que eu garanta alinhamento curricular.
  **Critérios**:
  - Fluxo de aprovação/rejeição com comentário.
  - Status visível no diário do professor.

### 3. Juliana – Secretária/Administrativa
**Módulo: Administrativo e Financeiro Básico**

- **US-007**
  Como secretária, eu quero cadastrar matrícula/rematrícula com busca rápida por CPF para que eu agilize o atendimento no balcão.
  **Critérios**:
  - Autocomplete por CPF/nome/responsável.
  - Validação automática de duplicidade.
  - Geração automática de contrato + boleto inicial.

- **US-008**
  Como secretária, eu quero gerar documentos escolares (declaração, histórico, transferência) em PDF automaticamente para que eu evite digitação repetitiva.
  **Critérios**:
  - Modelos editáveis pela escola.
  - Preenchimento automático com dados do aluno.
  - Assinatura digital opcional.

- **US-009**
  Como secretária, eu quero integrar envio de boletos/avisos via WhatsApp oficial para que eu reduza fila e chamadas.
  **Critérios**:
  - Envio em massa ou individual.
  - Template com link de pagamento Pix/boleto.

### 4. Prof. Carlos – Professor
**Módulo: Portal do Professor / Diário Digital**

- **US-010**
  Como professor, eu quero lançar frequência diária via lista ou QR code no app mobile para que eu faça isso em <30 segundos no recreio.
  **Critérios**:
  - Modo swipe (presente/ausente/justificado).
  - QR code para auto-registro (opcional).
  - Registro offline + sync quando online.

- **US-011**
  Como professor, eu quero lançar notas, anexar atividades e enviar aviso para a turma/pais em massa para que eu centralize comunicação sem WhatsApp pessoal.
  **Critérios**:
  - Cálculo automático de média.
  - Anexo (PDF/foto/vídeo).
  - Envio push para responsáveis + e-mail opcional.

- **US-012**
  Como professor, eu quero ver histórico completo do aluno (todas as notas/faltas anteriores) para que eu personalize o atendimento.
  **Critérios**:
  - Acesso rápido no perfil do aluno.
  - Gráfico de evolução por bimestre.

### 5. Fernanda – Responsável/Pai ou Mãe
**Módulo: Portal/App do Responsável**

- **US-013**
  Como responsável, eu quero visualizar boletim digital com notas, faltas e médias em tempo real para que eu acompanhe o desempenho do meu filho diariamente.
  **Critérios**:
  - Layout simples, mobile-first.
  - Gráfico de evolução.
  - Notificação push ao lançar nova nota/falta.

- **US-014**
  Como responsável, eu quero pagar mensalidade via Pix, cartão ou boleto diretamente no app para que eu evite atrasos e perda de boleto.
  **Critérios**:
  - Integração com gateway (ex.: PagSeguro/Stripe).
  - Histórico de pagamentos + comprovante automático.

- **US-015**
  Como responsável, eu quero justificar falta online com anexo (foto atestado) e receber confirmação para que eu evite ir à escola.
  **Critérios**:
  - Upload de arquivo + texto.
  - Status: Pendente/Aprovado/Rejeitado.
  - Notificação ao professor/coordenador.

Essas 15 user stories formam um **MVP sólido** (cobrem ~80% das dores diárias). Elas podem ser priorizadas com MoSCoW (Must-have: US-001,004,007,010,013) ou pontuadas em planning poker.

