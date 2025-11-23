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
        if settings.USE_CLOUDINARY:
            if not all([
                settings.CLOUDINARY_CLOUD_NAME,
                settings.CLOUDINARY_API_KEY,
                settings.CLOUDINARY_API_SECRET
            ]):
                raise ValueError(
                    "Cloudinary está habilitado mas as credenciais não foram configuradas. "
                    "Defina CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY e CLOUDINARY_API_SECRET"
                )

            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True
            )
            logger.info("Cloudinary configurado com sucesso")

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
        if not settings.USE_CLOUDINARY:
            raise HTTPException(
                status_code=500,
                detail="Cloudinary não está habilitado"
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
        if not settings.USE_CLOUDINARY:
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
        if not settings.USE_CLOUDINARY:
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
