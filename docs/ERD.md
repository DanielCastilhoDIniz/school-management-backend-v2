
### Visão Geral do Modelo de Dados

O modelo representa o domínio completo de uma instituição de ensino (escolas de educação básica ou instituições de ensino superior), cobrindo desde a estrutura organizacional até o acompanhamento pedagógico, financeiro e de comunicação com alunos e responsáveis.

O sistema é hierárquico e parte de entidades institucionais de alto nível até chegar aos registros individuais de alunos (matrículas, frequência, notas, boletins e alertas).

### Nível Institucional (Estrutura Organizacional)

**Instituição / Mantenedora**
Representa a entidade jurídica ou administrativa superior. Pode ser uma rede de ensino, uma universidade, um grupo educacional ou uma única escola que não possui filiais.
Exemplos: “Rede Municipal de Ensino de São Paulo”, “Universidade Federal do Rio de Janeiro”, “Grupo Educacional Alfa”.
Principais atributos: nome oficial, CNPJ, razão social.

**Unidade de Ensino**
Entidade operacional concreta onde ocorrem as atividades letivas. Uma mantenedora pode ter várias unidades.
Exemplos: “Escola Estadual João Silva – Unidade Centro”, “Campus Norte da UFABC”, “Polo EAD Curitiba”.
Principais atributos: nome da unidade/campus, endereço, código INEP (para unidades da educação básica), código e-MEC (para superior).
Relacionamento: uma Instituição mantém várias Unidades de Ensino.

**Classificação / Tipo da Instituição ou Unidade**
Define o perfil legal e pedagógico da unidade (ou da mantenedora).
Principais classificações:
- Nível de ensino: Educação Básica ou Ensino Superior
- Dependência administrativa: Federal, Estadual, Municipal, Privada, Filantrópica, Confessional, Comunitária
- Organização acadêmica (apenas superior): Universidade, Centro Universitário, Faculdade, Instituto Federal/CEFET
- Modalidade especial: Regular, Educação de Jovens e Adultos (EJA), Educação Especial, Ensino Profissional, Educação Indígena, Quilombola
- Oferece EAD: sim ou não
- Porte aproximado: Pequena, Média, Grande (baseado no número de alunos)

### Ciclo Letivo e Organização Pedagógica

**Período Letivo**
Representa o ciclo temporal de referência (ano letivo, bimestre, trimestre, semestre).
Exemplos: “Ano Letivo 2026”, “Bimestre 1 – 2026”.
Principais atributos: ano letivo, data de início, data de fim, estado (Inativo, Ativo, Encerrado).
Relacionamento: cada Unidade de Ensino oferece vários Períodos Letivos.

**Turma**
Grupo específico de alunos que cursam o mesmo conjunto de disciplinas em um período letivo.
Exemplos: “9º Ano A – Manhã – 2026”, “Engenharia Civil – Turma 2025.1”.
Principais atributos: código da turma, estado (Inativa, Ativa, Encerrada).
Relacionamento: cada Período Letivo contém várias Turmas.

### Vínculo Aluno–Turma e Pessoas

**Matrícula**
Registro do vínculo entre um aluno e uma turma em um determinado período.
Principais atributos: data da matrícula, estado (Pendente, Ativa, Trancada, Cancelada, Concluída).
Relacionamentos:
- Pertence a exatamente 1 Aluno
- Pertence a exatamente 1 Turma

**Aluno**
Discente matriculado ou em processo de matrícula.
Principais atributos: nome, CPF, data de nascimento, etc.
Relacionamentos: pode ter vários Responsáveis legais.

**Professor**
Docente vinculado à unidade de ensino.
Principais atributos: nome, CPF, disciplinas que pode lecionar.
Relacionamentos: pode ser alocado em horários, ministrar aulas.

**Responsável**
Pai, mãe ou representante legal do aluno.
Relacionamento: recebe notificações em nome do aluno.

### Elementos Pedagógicos da Turma

**Horário / Grade Horária**
Planejamento semanal das aulas da turma (dia, horário, professor, disciplina, sala).
Relacionamento: pertence a 1 Turma.

**Aula**
Registro efetivo de uma aula ministrada (conteúdo dado, data, professor).
Relacionamento: pertence a 1 Turma e é ministrada por 1 Professor.

**Frequência**
Registro de presença ou ausência de um aluno em uma aula específica.
Relacionamentos:
- Gerada a partir de 1 Aula
- Vinculada a 1 Matrícula

**Avaliação**
Instrumento de verificação de aprendizagem (prova, trabalho, seminário, etc.).
Principais atributos: tipo, data de aplicação, peso, estado (Criada, Aplicada, Encerrada).
Relacionamento: pertence a 1 Turma (e geralmente a 1 Disciplina).

**Nota**
Resultado obtido pelo aluno em uma avaliação específica.
Relacionamentos:
- Vinculada a 1 Matrícula
- Gerada por 1 Avaliação

**Boletim**
Documento consolidado de desempenho do aluno em um período letivo (notas + frequência + status de aprovação).
Relacionamento: gerado a partir de 1 Matricula.

### Recursos de Apoio e Comunicação

**Material Didático**
Arquivos ou links (PDF, vídeo, texto) disponibilizados para estudo.
Relacionamento: pode estar vinculado a 1 Turma ou a 1 Disciplina.

**Evento**
Atividades agendadas (prova, reunião de pais, feriado, recuperação, evento cultural).
Relacionamento: pode estar associado a 1 Turma ou à Unidade de Ensino.

**Notificação**
Comunicado enviado para aluno, responsável ou turma inteira.
Exemplos: aviso de falta, nota lançada, boletim disponível, evento próximo.
Relacionamentos: pode ser direcionada a Aluno, Responsável ou Turma.

**Alerta de Busca Ativa**
Registro automático ou manual de risco de evasão escolar.
Exemplos: 5 faltas consecutivas, frequência abaixo de 75%, ausência prolongada.
Relacionamento: gerado para 1 Aluno.

### Resumo da Hierarquia Principal

Instituição → Unidade de Ensino
↓
Período Letivo
↓
Turma
↓
Matrícula → Aluno
↓
Aulas / Horários / Avaliações / Materiais / Eventos
↓
Frequência + Notas → Boletim
↓
Alertas de Busca Ativa + Notificações

Essa estrutura permite rastrear todo o ciclo educacional desde a configuração institucional até o acompanhamento individualizado do aluno, respeitando as particularidades de educação básica e superior, redes públicas e privadas, modalidades especiais (EJA, educação especial, profissionalizante) e requisitos de conformidade com MEC/INEP (Censo Escolar, Censo da Educação Superior).
