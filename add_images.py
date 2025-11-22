"""
Script para adicionar imagens aos imóveis
"""
from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.imovel import Imovel, ImovelImagem

def adicionar_imagens():
    """Adiciona imagens de placeholder aos imóveis"""
    print("\n" + "="*50)
    print("ADICIONANDO IMAGENS AOS IMÓVEIS")
    print("="*50 + "\n")

    db = Session(bind=engine)

    try:
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
            print(f"Adicionando imagens para: {imovel.titulo}")

            # Pega as imagens do tipo correspondente
            tipo_imovel = imovel.tipo_imovel.value
            imagens = imagens_por_tipo.get(tipo_imovel, imagens_por_tipo["casa"])

            # Adiciona de 2 a 3 imagens por imóvel
            num_imagens = min(3, len(imagens))

            for i in range(num_imagens):
                # Verifica se já existe imagem para evitar duplicatas
                existe = db.query(ImovelImagem).filter(
                    ImovelImagem.imovel_id == imovel.id,
                    ImovelImagem.ordem == i
                ).first()

                if not existe:
                    imagem = ImovelImagem(
                        imovel_id=imovel.id,
                        imagem_url=imagens[i % len(imagens)],
                        ordem=i,
                        principal=(i == 0)  # Primeira imagem é principal
                    )
                    db.add(imagem)
                    total_imagens += 1

            db.commit()
            print(f"  ✓ {num_imagens} imagens adicionadas")

        print("\n" + "="*50)
        print(f"✓ TOTAL: {total_imagens} IMAGENS ADICIONADAS!")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n✗ Erro ao adicionar imagens: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    adicionar_imagens()
