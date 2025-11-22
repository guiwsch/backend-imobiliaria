"""
Script para adicionar imagens reais aos imóveis
Baixa imagens do Unsplash e salva localmente
"""
import os
import requests
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.imovel import Imovel, ImovelImagem
from app.core.config import settings

def adicionar_imagens_reais():
    """Baixa e adiciona imagens reais aos imóveis"""
    print("\n" + "="*50)
    print("ADICIONANDO IMAGENS REAIS AOS IMÓVEIS")
    print("="*50 + "\n")

    db = Session(bind=engine)

    try:
        # Remove todas as imagens antigas
        print("Removendo imagens antigas...")
        db.query(ImovelImagem).delete()
        db.commit()
        print("✓ Imagens antigas removidas\n")

        imoveis = db.query(Imovel).all()

        # URLs de imagens do Unsplash para diferentes tipos de imóveis
        imagens_por_tipo = {
            "casa": [
                "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
            ],
            "apartamento": [
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",
            ],
            "terreno": [
                "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1464146072230-91cabc968266?w=800&h=600&fit=crop",
            ],
            "comercial": [
                "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800&h=600&fit=crop",
            ],
        }

        total_imagens = 0

        for imovel in imoveis:
            print(f"Processando: {imovel.titulo}")

            # Cria diretório de uploads para o imóvel
            upload_dir = os.path.join(settings.UPLOAD_DIR, "imoveis", str(imovel.id))
            os.makedirs(upload_dir, exist_ok=True)

            # Pega as imagens do tipo correspondente
            tipo_imovel = imovel.tipo_imovel.value
            imagens_urls = imagens_por_tipo.get(tipo_imovel, imagens_por_tipo["casa"])

            # Adiciona de 2 a 3 imagens por imóvel
            num_imagens = min(3, len(imagens_urls))

            for i in range(num_imagens):
                url = imagens_urls[i % len(imagens_urls)]

                try:
                    # Baixa a imagem
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()

                    # Salva a imagem localmente
                    filename = f"imagem_{i + 1}.jpg"
                    file_path = os.path.join(upload_dir, filename)

                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    # Cria registro no banco com caminho relativo
                    imagem_url = f"/uploads/imoveis/{imovel.id}/{filename}"

                    db_imagem = ImovelImagem(
                        imovel_id=imovel.id,
                        imagem_url=imagem_url,
                        ordem=i,
                        principal=(i == 0)  # Primeira imagem é principal
                    )
                    db.add(db_imagem)
                    total_imagens += 1

                    print(f"  ✓ Imagem {i + 1} baixada e salva")

                except Exception as e:
                    print(f"  ✗ Erro ao baixar imagem {i + 1}: {e}")

            db.commit()
            print(f"  ✓ {num_imagens} imagens adicionadas\n")

        print("="*50)
        print(f"✓ TOTAL: {total_imagens} IMAGENS ADICIONADAS!")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n✗ Erro ao adicionar imagens: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    adicionar_imagens_reais()
