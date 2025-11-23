import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class CloudinaryService:
    """Serviço para gerenciar upload de imagens no Cloudinary"""

    def __init__(self):
        self._configured = False
        self._config_attempted = False

    def _ensure_configured(self):
        """Configura o Cloudinary apenas quando necessário (lazy loading)"""
        if self._config_attempted:
            return

        self._config_attempted = True

        if not settings.USE_CLOUDINARY:
            logger.info("Cloudinary está desabilitado (USE_CLOUDINARY=false)")
            return

        try:
            if not all([
                settings.CLOUDINARY_CLOUD_NAME,
                settings.CLOUDINARY_API_KEY,
                settings.CLOUDINARY_API_SECRET
            ]):
                logger.warning(
                    "Cloudinary está habilitado mas as credenciais não foram configuradas. "
                    "Defina CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY e CLOUDINARY_API_SECRET"
                )
                return

            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True
            )
            self._configured = True
            logger.info(f"Cloudinary configurado com sucesso - Cloud Name: {settings.CLOUDINARY_CLOUD_NAME}")
        except Exception as e:
            logger.error(f"Erro ao configurar Cloudinary: {str(e)}", exc_info=True)

    async def upload_image(
        self,
        file: UploadFile,
        folder: str = "imoveis",
        public_id: Optional[str] = None,
        transformation: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Faz upload de uma imagem para o Cloudinary

        Args:
            file: Arquivo de upload do FastAPI
            folder: Pasta no Cloudinary onde a imagem será armazenada
            public_id: ID público customizado (opcional)
            transformation: Transformações a aplicar na imagem (opcional)

        Returns:
            Dict contendo url, secure_url e public_id da imagem
        """
        # Garante que Cloudinary está configurado
        self._ensure_configured()

        if not settings.USE_CLOUDINARY or not self._configured:
            raise HTTPException(
                status_code=500,
                detail="Cloudinary não está habilitado ou configurado corretamente"
            )

        try:
            # Validar tipo de arquivo
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
            if file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Tipo de arquivo não permitido. Use: {', '.join(allowed_types)}"
                )

            # Validar tamanho do arquivo
            file_content = await file.read()
            if len(file_content) > settings.MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Arquivo muito grande. Tamanho máximo: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB"
                )

            # Reset do ponteiro do arquivo
            await file.seek(0)

            # Opções de upload
            upload_options = {
                "folder": folder,
                "resource_type": "image",
                "quality": "auto:good",  # Otimização automática de qualidade
                "fetch_format": "auto",  # Formato automático (WebP quando suportado)
            }

            if public_id:
                upload_options["public_id"] = public_id

            if transformation:
                upload_options["transformation"] = transformation

            # Upload para o Cloudinary
            result = cloudinary.uploader.upload(
                file.file,
                **upload_options
            )

            logger.info(f"Imagem enviada com sucesso para Cloudinary: {result.get('public_id')}")

            return {
                "url": result.get("url"),
                "secure_url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro ao fazer upload para Cloudinary: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao fazer upload da imagem: {str(e)}"
            )

    def delete_image(self, public_id: str) -> bool:
        """
        Remove uma imagem do Cloudinary

        Args:
            public_id: ID público da imagem no Cloudinary

        Returns:
            True se deletado com sucesso
        """
        self._ensure_configured()

        if not settings.USE_CLOUDINARY or not self._configured:
            return False

        try:
            result = cloudinary.uploader.destroy(public_id)
            logger.info(f"Imagem removida do Cloudinary: {public_id}")
            return result.get("result") == "ok"
        except Exception as e:
            logger.error(f"Erro ao deletar imagem do Cloudinary: {str(e)}", exc_info=True)
            return False

    def get_optimized_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: str = "fill",
        quality: str = "auto:good"
    ) -> str:
        """
        Gera URL otimizada de uma imagem com transformações

        Args:
            public_id: ID público da imagem
            width: Largura desejada
            height: Altura desejada
            crop: Modo de crop (fill, fit, scale, etc)
            quality: Qualidade da imagem

        Returns:
            URL da imagem com transformações aplicadas
        """
        self._ensure_configured()

        if not settings.USE_CLOUDINARY or not self._configured:
            return ""

        transformation = {
            "quality": quality,
            "fetch_format": "auto"
        }

        if width:
            transformation["width"] = width
        if height:
            transformation["height"] = height
        if width or height:
            transformation["crop"] = crop

        url, _ = cloudinary.utils.cloudinary_url(
            public_id,
            transformation=transformation,
            secure=True
        )

        return url


# Instância singleton do serviço
cloudinary_service = CloudinaryService()
