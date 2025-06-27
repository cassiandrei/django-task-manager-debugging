# 🎯 Gerenciador de Tarefas - Atividade de Debugging com IA

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/cassiandrei/django-task-manager-debugging)
[![Django](https://img.shields.io/badge/Django-5.2+-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-yellow)](LICENSE)

## 📋 Descrição
Este é um projeto Django simples de gerenciamento de tarefas criado para fins **educacionais**. O projeto contém **bugs intencionais** que devem ser corrigidos pelos alunos usando ferramentas de IA como auxílio.

## 🔐 **ACESSO RÁPIDO**
```
🌐 URL: http://127.0.0.1:8000/login/
👤 Usuário: aluno
🔑 Senha: teste123
```

## 🎯 Objetivo Pedagógico
- Aprender a interpretar testes unitários como especificação
- Praticar debugging usando IA (ChatGPT, Copilot, Claude, etc.)
- Desenvolver habilidades de leitura de código e análise de erros
- Compreender conceitos básicos de Django através da prática

## 🚀 Como Executar o Projeto

### 1. Configuração Inicial
```bash
# Ative o ambiente virtual (já configurado)
# No VSCode, o ambiente já está ativo

# Instale as dependências (já instaladas)
pip install django pytest pytest-django

# Execute as migrações
python manage.py migrate
```

### 2. Executar o Servidor
```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/login/`

### 3. 🔐 Credenciais de Teste
Para acessar o sistema, use:
- **Usuário:** `aluno`
- **Senha:** `teste123`

O sistema já vem com 5 tarefas de exemplo criadas para facilitar os testes.

### 4. Executar os Testes
```bash
# Executar todos os testes
python manage.py test tasks

# Executar um teste específico
python manage.py test tasks.tests.TaskModelTests.test_is_overdue_for_completed_task
```

### Páginas:
- `/login/` - Página de login
- `/logout/` - Logout automático
- `/` - Lista de tarefas (requer login)
- `/create/` - Criar nova tarefa (requer login)

**Importante:** Todas as funcionalidades de tarefa requerem login!

## �📝 Instruções para os Alunos

### Passo 1: Execute os testes
```bash
python manage.py test tasks
```

Você verá **7 testes falhando**. Não se preocupe, isso é esperado!

### Passo 2: Analise as falhas
Copie a saída do primeiro teste que falhou e use uma IA para entender:
- O que o teste está verificando
- Por que está falhando
- O que deveria acontecer

### Passo 3: Localize e corrija o bug
Use a IA para:
- Entender o código relacionado
- Identificar o problema
- Sugerir a correção

### Passo 4: Teste novamente
Execute os testes após cada correção para ver o progresso.

### Passo 5: Repita até todos os testes passarem
Continue até que todos os 9 testes passem.

### Passo 6: Teste a interface web
Após corrigir os bugs:
1. Acesse `http://127.0.0.1:8000/login/`
2. Faça login com `aluno` / `teste123` 
3. Teste criar, visualizar e completar tarefas
4. Verifique se tudo funciona corretamente

## 🎓 Como Usar o ChatGPT Web para Resolver os Bugs

### 🌐 Passo a Passo Usando ChatGPT (chat.openai.com)

#### 1. Primeiro, Execute os Testes
```bash
python manage.py test tasks
```

#### 2. Copie a Saída Completa do Terminal
- Selecione toda a saída dos testes que falharam
- Copie 

#### 3. Abra o ChatGPT Web ou Gemini
- Vá para [chat.openai.com](https://chat.openai.com)
- Faça login na sua conta

#### 4. Use Este Prompt Inicial
```
Sou um estudante aprendendo Django e debugging. Estou trabalhando em um projeto que tem bugs intencionais para eu praticar. 

Recebi esta saída de testes que falharam:

[COLE AQUI A SAÍDA COMPLETA DOS TESTES]

Por favor, me ajude a entender:
1. Quantos testes falharam e quais são?
2. Qual é o primeiro teste que devo focar?
3. O que esse primeiro teste está tentando verificar?
4. Por que ele está falhando?

Vou te mostrar o código relacionado em seguida.
```

#### 5. Mostre o Código Relacionado
Após a resposta inicial, copie o arquivo com bugs e cole:
```
Aqui está o código do arquivo tasks/models.py:

[COLE O CÓDIGO DO ARQUIVO]

Baseado no teste que você identificou, qual é o problema específico no código?
```

#### 6. Peça a Correção Específica
```
Perfeito! Agora me mostra exatamente como corrigir esse bug. 
Me dê:
1. O código exato que preciso alterar
2. Como deve ficar depois da correção
3. Por que essa correção resolve o problema
```

#### 7. Valide a Correção
Depois de aplicar a correção:
```
Apliquei a correção e agora executei os testes novamente. Aqui está a nova saída:

[COLE A NOVA SAÍDA DOS TESTES]

A correção funcionou? Qual é o próximo bug que devo focar?
```

### 📋 Template de Prompt Completo

```
Olá! Sou estudante e estou aprendendo debugging com Django. Estou trabalhando em um projeto educacional com bugs intencionais.

CONTEXTO:
- Projeto Django de gerenciamento de tarefas
- Há 3 bugs principais que fazem 7 testes falharem
- Os bugs estão no arquivo tasks/models.py

SAÍDA DOS TESTES:
[Cole aqui a saída completa do comando: python manage.py test tasks]

CÓDIGO ATUAL (tasks/models.py):
[Cole aqui o código do arquivo models.py]

PRECISO DE AJUDA PARA:
1. Identificar qual teste focar primeiro
2. Entender o que esse teste verifica
3. Encontrar o bug específico no código
4. Saber exatamente como corrigir

Pode me guiar passo a passo?
```

### 🔄 Processo Iterativo

1. **Execute os testes** → **Copie a saída** → **Cole no ChatGPT**
2. **Receba orientação** → **Aplique a correção** → **Execute os testes novamente**
3. **Repita** até todos os 9 testes passarem

### 💡 Dicas Importantes para o ChatGPT

#### ✅ O que FAZER:
- Cole **toda** a saída dos testes, não só parte
- Seja específico: "estou trabalhando com Django", "sou iniciante"
- Peça explicações: "por que esse código está errado?"
- Valide as correções: "funcionou! qual o próximo?"

#### ❌ O que NÃO fazer:
- Não cole apenas a mensagem de erro, cole tudo
- Não peça "resolva tudo" - vá um bug por vez
- Não copie códigos sem entender - peça explicação

## 📱 Alternativas ao ChatGPT Web

Se não tiver acesso ao ChatGPT, pode usar:
- **Claude** (claude.ai) - Use os mesmos prompts
- **Gemini** (gemini.google.com) - Use os mesmos prompts  
- **GitHub Copilot Chat** (se tiver no VS Code)
- **Perplexity** (perplexity.ai) - Boa para explicações técnicas

## � Troubleshooting Comum

### "O ChatGPT não entende meu problema"
- Copie **mais contexto** (toda a saída do teste, não só o erro)
- Explique que você é **iniciante** em Django
- Diga que está fazendo um **exercício educacional**

### "As correções não funcionam"
- Mostre ao ChatGPT a **nova saída dos testes** após a correção
- Pergunte: "funcionou? o que fazer a seguir?"
- Peça para **explicar por que** a correção deveria funcionar

### "Estou perdido com tantos erros"
- Peça: "qual erro devo focar PRIMEIRO?"
- Trabalhe **um bug por vez**
- Valide cada correção antes de partir para a próxima

### "Não entendo a explicação do ChatGPT"
- Peça: "explique de forma mais simples"
- Pergunte: "pode dar um exemplo?"
- Diga: "sou iniciante, pode detalhar mais?"

## ✅ Critérios de Sucesso

Você completou a atividade quando:
- [ ] Todos os 9 testes passam
- [ ] Você consegue acessar o site em `http://127.0.0.1:8000`
- [ ] Você entende o que cada bug fazia
- [ ] **Você conseguiu usar IA para resolver os problemas e sabe explicar como usou a IA para debugar**

### 🎖️ Critérios Avançados (Para Nota Máxima)
- [ ] Documentou no ChatGPT como resolveu cada bug
- [ ] Consegue explicar o processo de debugging que seguiu
- [ ] Entende por que cada correção funcionou (não só copiou e colou)

## 🎯 Desafio Extra (Opcional)

Após corrigir todos os bugs, tente:
1. Adicionar um novo teste que verifica outro comportamento
2. Implementar uma nova funcionalidade
3. Melhorar a interface do usuário

## 🆘 Precisa de Ajuda?

Se estiver muito perdido:
1. Releia as instruções
2. Execute um teste por vez
3. Use a IA com prompts específicos
4. Peça ajuda

Lembre-se: **o objetivo é aprender a usar IA para resolver problemas**, não dominar Django!

---

**Boa sorte e bom debugging! 🚀**
