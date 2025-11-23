# 📧 Guia de Configuração de Notificações por Email

## ✅ Sistema Implementado!

O sistema de notificações por email está **totalmente funcional** e enviará emails automaticamente quando:

1. **Novo Lead** - Alguém preencher formulário de contato
2. **Visita Agendada** - Uma nova visita for marcada no sistema

---

## 🔧 Como Configurar (Gmail - GRATUITO)

### Passo 1: Preparar sua conta Gmail

1. Acesse sua conta Google
2. Vá em **Segurança** → https://myaccount.google.com/security
3. Ative a **"Verificação em duas etapas"** (se ainda não estiver ativa)
4. Após ativar, vá em **"Senhas de app"** → https://myaccount.google.com/apppasswords
5. Selecione:
   - **App**: E-mail
   - **Dispositivo**: Outro (nome personalizado) → coloque "ImobiLux"
6. Clique em **Gerar**
7. **COPIE A SENHA GERADA** (16 caracteres sem espaços)

### Passo 2: Configurar o arquivo .env

Edite o arquivo `/backend/.env` e adicione:

```bash
# Frontend URL
FRONTEND_URL=http://localhost:5173

# SMTP Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Senha de app gerada no passo anterior (cole sem espaços)
SMTP_FROM_EMAIL=seu-email@gmail.com
SMTP_FROM_NAME=ImobiLux
```

**Exemplo real:**
```bash
SMTP_USER=guilherme@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
SMTP_FROM_EMAIL=guilherme@gmail.com
SMTP_FROM_NAME=Junior Corretor
```

### Passo 3: Reiniciar o backend

```bash
# Pare o servidor
pkill -f uvicorn

# Inicie novamente
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Passo 4: Ativar notificações no painel

1. Faça login no painel admin
2. Vá em **Configurações** → **Empresa**
3. Preencha o **email** que receberá as notificações
4. Vá na aba **Notificações**
5. **Ative "E-mail"**
6. Clique em **Salvar Preferências**

---

## 🎨 Templates de Email

Os emails enviados são **HTML profissionais** com:
- ✅ Design moderno e responsivo
- ✅ Cores do tema (dourado/preto)
- ✅ Informações organizadas
- ✅ Botão direto para o painel admin
- ✅ Fallback em texto plano

### Email de Novo Lead

Inclui:
- Nome, email, telefone do cliente
- Origem (formulário de contato, interesse em imóvel, etc.)
- Mensagem deixada
- Imóvel de interesse (se aplicável)
- Botão para ver no painel

### Email de Visita Agendada

Inclui:
- Nome e telefone do cliente
- Imóvel a visitar
- Data e horário
- Observações
- Botão para ver no painel

---

## 🔍 Testando

### Teste 1: Novo Lead
1. Vá no site público → Página "Contato"
2. Preencha o formulário
3. Envie
4. **Você deve receber um email em segundos!**

### Teste 2: Visita Agendada
1. Faça login no painel admin
2. Vá em "Visitas" → "Agendar Visita"
3. Preencha os dados
4. Salve
5. **Você deve receber um email!**

---

## ⚠️ Troubleshooting

### Não estou recebendo emails

**1. Verifique o console do backend:**
```bash
tail -f /tmp/backend.log
```

Procure por mensagens como:
- ✅ `Notificação de novo lead enviada para: ...`
- ❌ `Erro ao enviar email: ...`

**2. Verifique as configurações:**
- Email está preenchido nas configurações da empresa?
- Notificações por email estão ativadas?
- Senha de app está correta (sem espaços)?

**3. Problemas comuns:**

| Erro | Solução |
|------|---------|
| `Authentication failed` | Senha de app incorreta, gere uma nova |
| `Connection refused` | Porta 587 bloqueada, verifique firewall |
| `Sender address rejected` | SMTP_FROM_EMAIL diferente do SMTP_USER |

---

## 🚀 Outros Provedores de Email

### Outlook/Hotmail
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=seu-email@outlook.com
SMTP_PASSWORD=sua-senha
```

### SendGrid (Até 100 emails/dia grátis)
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxxxxxxxxxxxx  # API Key do SendGrid
```

### Mailgun (Gratuito até 5.000 emails/mês)
```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@seu-dominio.mailgun.org
SMTP_PASSWORD=sua-api-key
```

---

## 📊 Monitoramento

Para ver logs de emails enviados:
```bash
grep "Notificação" /tmp/backend.log
```

---

## 🎉 Pronto!

Seu sistema de notificações está **100% funcional e gratuito**!

Qualquer dúvida, consulte este guia ou verifique os logs do backend.
