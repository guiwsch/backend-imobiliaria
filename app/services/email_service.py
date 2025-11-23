"""
Serviço de envio de emails usando SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Envia um email usando SMTP

        Args:
            to_emails: Lista de emails destinatários
            subject: Assunto do email
            html_content: Conteúdo HTML do email
            text_content: Conteúdo texto plano (opcional)

        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject

            # Adicionar conteúdo texto plano
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)

            # Adicionar conteúdo HTML
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)

            # Conectar ao servidor SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Segurança TLS
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email enviado com sucesso para: {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            return False

    def send_new_lead_notification(self, lead_data: dict, admin_email: str) -> bool:
        """
        Envia notificação de novo lead para o admin
        """
        subject = f"🏠 Novo Lead - {lead_data.get('nome')}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #d4af37, #ffd700); color: #000; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .info-row {{ margin: 15px 0; padding: 10px; background: white; border-left: 4px solid #d4af37; }}
                .label {{ font-weight: bold; color: #d4af37; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Novo Lead Recebido!</h1>
                </div>
                <div class="content">
                    <p>Você recebeu um novo lead através do site:</p>

                    <div class="info-row">
                        <span class="label">Nome:</span> {lead_data.get('nome', 'N/A')}
                    </div>

                    <div class="info-row">
                        <span class="label">Email:</span> {lead_data.get('email', 'N/A')}
                    </div>

                    <div class="info-row">
                        <span class="label">Telefone:</span> {lead_data.get('telefone', 'N/A')}
                    </div>

                    <div class="info-row">
                        <span class="label">Origem:</span> {lead_data.get('origem', 'N/A')}
                    </div>

                    {f'<div class="info-row"><span class="label">Mensagem:</span><br>{lead_data.get("mensagem", "")}</div>' if lead_data.get('mensagem') else ''}

                    {f'<div class="info-row"><span class="label">Imóvel Interesse:</span> {lead_data.get("imovel_titulo", "N/A")}</div>' if lead_data.get('imovel_titulo') else ''}

                    <p style="margin-top: 20px;">
                        <a href="{settings.FRONTEND_URL}/admin/leads"
                           style="background: linear-gradient(135deg, #d4af37, #c09a2a);
                                  color: white;
                                  padding: 12px 24px;
                                  text-decoration: none;
                                  border-radius: 5px;
                                  display: inline-block;">
                            Ver no Painel Admin
                        </a>
                    </p>
                </div>
                <div class="footer">
                    <p>Esta é uma notificação automática do sistema ImobiLux</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Novo Lead Recebido!

        Nome: {lead_data.get('nome', 'N/A')}
        Email: {lead_data.get('email', 'N/A')}
        Telefone: {lead_data.get('telefone', 'N/A')}
        Origem: {lead_data.get('origem', 'N/A')}
        {f"Mensagem: {lead_data.get('mensagem', '')}" if lead_data.get('mensagem') else ''}

        Acesse o painel admin para mais detalhes.
        """

        return self.send_email([admin_email], subject, html_content, text_content)

    def send_visit_scheduled_notification(self, visit_data: dict, admin_email: str) -> bool:
        """
        Envia notificação de visita agendada para o admin
        """
        subject = f"📅 Visita Agendada - {visit_data.get('lead_nome')}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4096ff, #1677ff); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .info-row {{ margin: 15px 0; padding: 10px; background: white; border-left: 4px solid #4096ff; }}
                .label {{ font-weight: bold; color: #4096ff; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📅 Nova Visita Agendada!</h1>
                </div>
                <div class="content">
                    <p>Uma nova visita foi agendada:</p>

                    <div class="info-row">
                        <span class="label">Cliente:</span> {visit_data.get('lead_nome', 'N/A')}
                    </div>

                    <div class="info-row">
                        <span class="label">Telefone:</span> {visit_data.get('lead_telefone', 'N/A')}
                    </div>

                    <div class="info-row">
                        <span class="label">Imóvel:</span> {visit_data.get('imovel_titulo', 'N/A')}
                    </div>

                    <div class="info-row">
                        <span class="label">Data:</span> {visit_data.get('data_visita', 'N/A')}
                    </div>

                    <div class="info-row">
                        <span class="label">Horário:</span> {visit_data.get('horario', 'N/A')}
                    </div>

                    {f'<div class="info-row"><span class="label">Observações:</span><br>{visit_data.get("observacoes", "")}</div>' if visit_data.get('observacoes') else ''}

                    <p style="margin-top: 20px;">
                        <a href="{settings.FRONTEND_URL}/admin/visitas"
                           style="background: linear-gradient(135deg, #4096ff, #1677ff);
                                  color: white;
                                  padding: 12px 24px;
                                  text-decoration: none;
                                  border-radius: 5px;
                                  display: inline-block;">
                            Ver no Painel Admin
                        </a>
                    </p>
                </div>
                <div class="footer">
                    <p>Esta é uma notificação automática do sistema ImobiLux</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Nova Visita Agendada!

        Cliente: {visit_data.get('lead_nome', 'N/A')}
        Telefone: {visit_data.get('lead_telefone', 'N/A')}
        Imóvel: {visit_data.get('imovel_titulo', 'N/A')}
        Data: {visit_data.get('data_visita', 'N/A')}
        Horário: {visit_data.get('horario', 'N/A')}
        {f"Observações: {visit_data.get('observacoes', '')}" if visit_data.get('observacoes') else ''}

        Acesse o painel admin para mais detalhes.
        """

        return self.send_email([admin_email], subject, html_content, text_content)


# Instância única do serviço
email_service = EmailService()
