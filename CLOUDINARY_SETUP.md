# Configuração do Cloudinary

Este guia mostra como configurar o Cloudinary para armazenamento de imagens em produção.

## Por que usar Cloudinary?

O Railway (e outros serviços PaaS) usa filesystem efêmero, ou seja, **arquivos locais são perdidos a cada deploy**. O Cloudinary resolve isso oferecendo:

- ✅ **Armazenamento persistente** de imagens
- ✅ **CDN global** para entrega rápida
- ✅ **Otimização automática** (WebP, compressão, etc)
- ✅ **Free tier generoso**: 25 GB de armazenamento + 25 GB de bandwidth
- ✅ **Transformações on-the-fly** (resize, crop, thumbnails)

## Passo a Passo

### 1. Criar conta no Cloudinary

1. Acesse: https://cloudinary.com/users/register_free
2. Crie uma conta gratuita
3. Confirme seu email

### 2. Obter credenciais

1. Acesse o Dashboard: https://cloudinary.com/console
2. Na página inicial, você verá:
   - **Cloud Name** (ex: `dxxxxxxxxxxxxx`)
   - **API Key** (ex: `123456789012345`)
   - **API Secret** (clique em "Reveal" para ver)

### 3. Configurar variáveis de ambiente

#### Para desenvolvimento local (.env):

```env
USE_CLOUDINARY=true
CLOUDINARY_CLOUD_NAME=seu-cloud-name-aqui
CLOUDINARY_API_KEY=sua-api-key-aqui
CLOUDINARY_API_SECRET=seu-api-secret-aqui
```

#### Para produção (Railway):

1. Acesse o projeto no Railway
2. Vá em **Variables**
3. Adicione as seguintes variáveis:
   - `USE_CLOUDINARY` = `true`
   - `CLOUDINARY_CLOUD_NAME` = seu cloud name
   - `CLOUDINARY_API_KEY` = sua API key
   - `CLOUDINARY_API_SECRET` = seu API secret

### 4. Deploy

Após configurar as variáveis de ambiente:

```bash
# Commit e push das alterações
git add .
git commit -m "feat: Adiciona integração com Cloudinary para armazenamento de imagens"
git push
```

O Railway vai fazer o deploy automaticamente.

## Como funciona

### Upload de Imagens

Quando `USE_CLOUDINARY=true`:
- As imagens são enviadas diretamente para o Cloudinary
- O backend recebe a URL da imagem hospedada no Cloudinary
- A URL é salva no banco de dados PostgreSQL

Quando `USE_CLOUDINARY=false`:
- As imagens são salvas localmente (⚠️ serão perdidas no próximo deploy)

### Estrutura de pastas no Cloudinary

As imagens são organizadas automaticamente:
```
imobiliaria/
  └── imoveis/
      ├── 1/
      │   ├── imovel_1_20231123_143022.jpg
      │   └── imovel_1_20231123_143045.jpg
      ├── 2/
      │   └── imovel_2_20231123_150000.jpg
      └── ...
```

### URLs otimizadas

O Cloudinary gera URLs otimizadas automaticamente:
- Formato WebP quando o navegador suporta
- Compressão automática
- Qualidade ajustada (`auto:good`)

Exemplo de URL:
```
https://res.cloudinary.com/seu-cloud-name/image/upload/imobiliaria/imoveis/1/imovel_1_20231123_143022.jpg
```

## Transformações (Opcional)

Você pode criar thumbnails e variações de tamanho on-the-fly:

```python
# Exemplo: thumbnail de 300x200px
from app.services.cloudinary_service import cloudinary_service

thumbnail_url = cloudinary_service.get_optimized_url(
    public_id="imobiliaria/imoveis/1/imovel_1_20231123_143022",
    width=300,
    height=200,
    crop="fill"
)
```

## Monitoramento

- Acesse https://cloudinary.com/console/media_library para ver todas as imagens
- Veja estatísticas de uso em https://cloudinary.com/console/usage
- O free tier oferece 25 GB - suficiente para milhares de imagens de imóveis

## Migração de imagens existentes (se houver)

Se você já tem imagens armazenadas localmente e quer migrar para o Cloudinary, você pode:

1. Criar um script de migração
2. Fazer upload manual via interface do Cloudinary
3. Atualizar as URLs no banco de dados

## Troubleshooting

### Erro: "Cloudinary está habilitado mas as credenciais não foram configuradas"

- Verifique se as 3 variáveis estão configuradas: `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
- Certifique-se de que não há espaços extras nas variáveis

### Imagens não carregam no frontend

- Verifique se a URL no banco de dados começa com `https://res.cloudinary.com/`
- Teste a URL diretamente no navegador
- Verifique se o CORS está configurado corretamente

### Limite de armazenamento excedido

- O free tier oferece 25 GB
- Monitore o uso em https://cloudinary.com/console/usage
- Se necessário, faça upgrade do plano ou remova imagens antigas
