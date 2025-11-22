"""
Script para popular o banco de dados com dados de exemplo
"""
import sys
from sqlalchemy.orm import Session
from app.db.session import engine, Base
from app.models.imovel import Imovel, TipoImovel, TipoNegocio, ImovelImagem
from app.models.lead import Lead, LeadStatus
from app.models.visita import Visita, VisitaStatus
from app.models.configuracao import Configuracao
from datetime import datetime, timedelta
import random

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

def criar_imoveis(db: Session):
    """Cria imóveis de exemplo"""
    print("Criando imóveis...")

    imoveis_data = [
        {
            "titulo": "Casa 3 quartos em Ingleses",
            "descricao": "Linda casa próxima à praia de Ingleses, com 3 quartos, sendo 1 suíte, sala ampla, cozinha planejada, área de serviço e garagem para 2 carros. Localização privilegiada!",
            "tipo_imovel": TipoImovel.casa,
            "tipo_negocio": TipoNegocio.venda,
            "preco_venda": 580000.00,
            "area_total": 180.00,
            "area_construida": 150.00,
            "quartos": 3,
            "banheiros": 2,
            "vagas_garagem": 2,
            "rua": "Rua das Gaivotas",
            "numero": "450",
            "bairro": "Ingleses",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88058-070",
            "piscina": False,
            "aceita_pets": True,
            "mobiliado": False,
            "destaque": True,
        },
        {
            "titulo": "Apartamento 2 quartos no Centro",
            "descricao": "Apartamento moderno no coração de Florianópolis, com 2 quartos, sala integrada com cozinha americana, varanda com vista para o mar. Prédio com elevador e portaria 24h.",
            "tipo_imovel": TipoImovel.apartamento,
            "tipo_negocio": TipoNegocio.aluguel,
            "valor_aluguel": 2500.00,
            "area_total": 75.00,
            "area_construida": 75.00,
            "quartos": 2,
            "banheiros": 1,
            "vagas_garagem": 1,
            "rua": "Rua Felipe Schmidt",
            "numero": "789",
            "complemento": "Apto 501",
            "bairro": "Centro",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88010-001",
            "piscina": False,
            "aceita_pets": False,
            "mobiliado": True,
            "destaque": True,
        },
        {
            "titulo": "Casa 4 quartos em Jurerê Internacional",
            "descricao": "Casa de alto padrão em condomínio fechado, 4 suítes, piscina aquecida, churrasqueira, sauna, home theater. Acabamento de primeira linha.",
            "tipo_imovel": TipoImovel.casa,
            "tipo_negocio": TipoNegocio.venda,
            "preco_venda": 1850000.00,
            "area_total": 450.00,
            "area_construida": 320.00,
            "quartos": 4,
            "banheiros": 5,
            "vagas_garagem": 4,
            "rua": "Rua das Orquídeas",
            "numero": "123",
            "bairro": "Jurerê Internacional",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88053-000",
            "piscina": True,
            "aceita_pets": True,
            "mobiliado": True,
            "destaque": True,
        },
        {
            "titulo": "Apartamento Studio no Campeche",
            "descricao": "Studio compacto e funcional, ideal para solteiros ou casal. Próximo à praia do Campeche e ao aeroporto.",
            "tipo_imovel": TipoImovel.apartamento,
            "tipo_negocio": TipoNegocio.aluguel,
            "valor_aluguel": 1200.00,
            "area_total": 35.00,
            "area_construida": 35.00,
            "quartos": 1,
            "banheiros": 1,
            "vagas_garagem": 1,
            "rua": "Avenida Pequeno Príncipe",
            "numero": "2500",
            "complemento": "Apto 302",
            "bairro": "Campeche",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88063-000",
            "piscina": False,
            "aceita_pets": True,
            "mobiliado": False,
            "destaque": False,
        },
        {
            "titulo": "Casa 3 quartos na Lagoa da Conceição",
            "descricao": "Casa charmosa na Lagoa, com vista parcial para o mar, quintal amplo, espaço gourmet e 3 quartos. Perfeita para quem busca qualidade de vida.",
            "tipo_imovel": TipoImovel.casa,
            "tipo_negocio": TipoNegocio.venda,
            "preco_venda": 950000.00,
            "area_total": 250.00,
            "area_construida": 180.00,
            "quartos": 3,
            "banheiros": 3,
            "vagas_garagem": 2,
            "rua": "Servidão da Prainha",
            "numero": "85",
            "bairro": "Lagoa da Conceição",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88062-000",
            "piscina": False,
            "aceita_pets": True,
            "mobiliado": False,
            "destaque": True,
        },
        {
            "titulo": "Terreno 450m² em Canasvieiras",
            "descricao": "Excelente terreno plano, pronto para construir. Localização privilegiada em Canasvieiras, próximo à praia e comércio local.",
            "tipo_imovel": TipoImovel.terreno,
            "tipo_negocio": TipoNegocio.venda,
            "preco_venda": 380000.00,
            "area_total": 450.00,
            "quartos": 0,
            "banheiros": 0,
            "vagas_garagem": 0,
            "rua": "Rua das Palmeiras",
            "numero": "1250",
            "bairro": "Canasvieiras",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88054-000",
            "piscina": False,
            "aceita_pets": False,
            "mobiliado": False,
            "destaque": False,
        },
        {
            "titulo": "Sala Comercial 50m² no Centro",
            "descricao": "Sala comercial em edifício corporativo, banheiro privativo, vaga de garagem. Ideal para escritório ou consultório.",
            "tipo_imovel": TipoImovel.comercial,
            "tipo_negocio": TipoNegocio.aluguel,
            "valor_aluguel": 1800.00,
            "area_total": 50.00,
            "area_construida": 50.00,
            "quartos": 0,
            "banheiros": 1,
            "vagas_garagem": 1,
            "rua": "Rua Jerônimo Coelho",
            "numero": "185",
            "complemento": "Sala 805",
            "bairro": "Centro",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88010-030",
            "piscina": False,
            "aceita_pets": False,
            "mobiliado": False,
            "destaque": False,
        },
        {
            "titulo": "Apartamento 3 quartos em Trindade",
            "descricao": "Apartamento próximo à UFSC, 3 quartos, sala, cozinha, área de serviço. Ótimo para estudantes ou investimento.",
            "tipo_imovel": TipoImovel.apartamento,
            "tipo_negocio": TipoNegocio.aluguel,
            "valor_aluguel": 2200.00,
            "area_total": 90.00,
            "area_construida": 90.00,
            "quartos": 3,
            "banheiros": 2,
            "vagas_garagem": 1,
            "rua": "Rua Lauro Linhares",
            "numero": "2055",
            "complemento": "Apto 204",
            "bairro": "Trindade",
            "cidade": "Florianópolis",
            "estado": "SC",
            "cep": "88036-002",
            "piscina": False,
            "aceita_pets": True,
            "mobiliado": False,
            "destaque": False,
        },
    ]

    imoveis_criados = []
    for imovel_data in imoveis_data:
        imovel = Imovel(**imovel_data)
        db.add(imovel)
        db.flush()
        imoveis_criados.append(imovel)

    db.commit()
    print(f"✓ {len(imoveis_criados)} imóveis criados!")
    return imoveis_criados


def criar_leads(db: Session):
    """Cria leads de exemplo"""
    print("Criando leads...")

    leads_data = [
        {
            "nome": "João Silva",
            "email": "joao.silva@email.com",
            "telefone": "(48) 99999-1111",
            "mensagem": "Gostaria de mais informações sobre o apartamento no Centro",
            "origem": "Site",
            "status": LeadStatus.novo,
        },
        {
            "nome": "Maria Santos",
            "email": "maria.santos@email.com",
            "telefone": "(48) 99999-2222",
            "mensagem": "Tenho interesse na casa de Ingleses. Podemos agendar uma visita?",
            "origem": "Facebook",
            "status": LeadStatus.contatado,
        },
        {
            "nome": "Pedro Oliveira",
            "email": "pedro.oliveira@email.com",
            "telefone": "(48) 99999-3333",
            "mensagem": "Procuro apartamento para alugar próximo à UFSC",
            "origem": "Site",
            "status": LeadStatus.visitaAgendada,
        },
        {
            "nome": "Ana Costa",
            "email": "ana.costa@email.com",
            "telefone": "(48) 99999-4444",
            "mensagem": "Interesse em comprar casa na Lagoa",
            "origem": "Instagram",
            "status": LeadStatus.negociacao,
        },
        {
            "nome": "Carlos Ferreira",
            "email": "carlos.ferreira@email.com",
            "telefone": "(48) 99999-5555",
            "mensagem": "Fechei negócio! Obrigado pelo atendimento",
            "origem": "Indicação",
            "status": LeadStatus.convertido,
        },
    ]

    for lead_data in leads_data:
        lead = Lead(**lead_data)
        db.add(lead)

    db.commit()
    print(f"✓ {len(leads_data)} leads criados!")


def criar_visitas(db: Session, imoveis):
    """Cria visitas de exemplo"""
    print("Criando visitas...")

    hoje = datetime.now()

    visitas_data = [
        {
            "imovel_id": imoveis[0].id,
            "nome_cliente": "Roberto Almeida",
            "email_cliente": "roberto.almeida@email.com",
            "telefone_cliente": "(48) 99999-6666",
            "data_hora": hoje + timedelta(days=1, hours=10),
            "status": VisitaStatus.agendada,
            "observacoes": "Cliente preferiu horário da manhã",
        },
        {
            "imovel_id": imoveis[1].id,
            "nome_cliente": "Fernanda Lima",
            "email_cliente": "fernanda.lima@email.com",
            "telefone_cliente": "(48) 99999-7777",
            "data_hora": hoje + timedelta(days=2, hours=14),
            "status": VisitaStatus.confirmada,
            "observacoes": "Levar chaves do portão",
        },
        {
            "imovel_id": imoveis[2].id,
            "nome_cliente": "Lucas Martins",
            "email_cliente": "lucas.martins@email.com",
            "telefone_cliente": "(48) 99999-8888",
            "data_hora": hoje + timedelta(days=3, hours=16),
            "status": VisitaStatus.agendada,
        },
        {
            "imovel_id": imoveis[4].id,
            "nome_cliente": "Juliana Rocha",
            "email_cliente": "juliana.rocha@email.com",
            "telefone_cliente": "(48) 99999-9999",
            "data_hora": hoje + timedelta(days=5, hours=11),
            "status": VisitaStatus.agendada,
            "observacoes": "Interessada em financiamento",
        },
    ]

    for visita_data in visitas_data:
        visita = Visita(**visita_data)
        db.add(visita)

    db.commit()
    print(f"✓ {len(visitas_data)} visitas criadas!")


def criar_configuracao(db: Session):
    """Cria configuração inicial"""
    print("Criando configuração...")

    config = db.query(Configuracao).first()
    if config:
        print("✓ Configuração já existe!")
        return

    config = Configuracao(
        nome_empresa="Imobiliária MVP",
        email="contato@imobiliariamvp.com.br",
        telefone="(48) 3333-4444",
        whatsapp="(48) 99999-0000",
        site="www.imobiliariamvp.com.br",
        endereco="Rua Principal, 100 - Centro, Florianópolis - SC",
        sobre="Somos uma imobiliária moderna e comprometida em encontrar o imóvel perfeito para você. Com anos de experiência no mercado, oferecemos as melhores opções de compra, venda e locação em Florianópolis e região.",
        notificacao_email=True,
        notificacao_sms=False,
        notificacao_whatsapp=True,
    )

    db.add(config)
    db.commit()
    print("✓ Configuração criada!")


def main():
    """Função principal"""
    print("\n" + "="*50)
    print("POPULANDO BANCO DE DADOS")
    print("="*50 + "\n")

    db = Session(bind=engine)

    try:
        # Criar dados
        imoveis = criar_imoveis(db)
        criar_leads(db)
        criar_visitas(db, imoveis)
        criar_configuracao(db)

        print("\n" + "="*50)
        print("✓ BANCO POPULADO COM SUCESSO!")
        print("="*50 + "\n")

        print("Resumo:")
        print(f"  • {len(imoveis)} imóveis")
        print(f"  • 5 leads")
        print(f"  • 4 visitas agendadas")
        print(f"  • 1 configuração\n")

    except Exception as e:
        print(f"\n✗ Erro ao popular banco: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
