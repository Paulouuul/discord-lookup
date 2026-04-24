from discord_lookup.formatters import JSONFormatter, CSVFormatter, YAMLFormatter, HTMLFormatter, XMLFormatter, MarkdownFormatter
from fastapi import Response

class Exporter:
    """Exporta dados em diferentes formatos baseado no header Accept"""
    
    @staticmethod
    def export(user, accept: str) -> Response:
        """
        Exporta um único usuário
        
        Args:
            user: Objeto DiscordUser
            accept: Header Accept (ex: "application/json", "text/csv")
            
        Returns:
            Response: FastAPI response com o conteúdo formatado
        """
        if "text/csv" in accept:
            return Response(content=CSVFormatter.format(user), media_type="text/csv")
        elif "application/x-yaml" in accept or "text/yaml" in accept:
            return Response(content=YAMLFormatter.format(user), media_type="application/x-yaml")
        elif "text/html" in accept:
            return Response(content=HTMLFormatter.format(user), media_type="text/html")
        elif "application/xml" in accept or "text/xml" in accept:
            return Response(content=XMLFormatter.format(user), media_type="application/xml")
        elif "text/markdown" in accept:
            return Response(content=MarkdownFormatter.format(user), media_type="text/markdown")
        else:
            return Response(content=JSONFormatter.format(user), media_type="application/json")
    
    @staticmethod
    def export_batch(batch, accept: str) -> Response:
        """
        Exporta resultados de batch
        
        Args:
            batch: BatchResponse object
            accept: Header Accept
            
        Returns:
            Response: FastAPI response com o conteúdo formatado
        """
        if "text/csv" in accept:
            return Response(content=CSVFormatter.format_batch(batch.model_dump()["results"]), media_type="text/csv")
        elif "application/x-yaml" in accept or "text/yaml" in accept:
            return Response(content=YAMLFormatter.format_batch(batch.model_dump()["results"]), media_type="application/x-yaml")
        elif "text/html" in accept:
            return Response(content=HTMLFormatter.format_batch(batch.model_dump()["results"]), media_type="text/html")
        elif "application/xml" in accept or "text/xml" in accept:
            return Response(content=XMLFormatter.format_batch(batch.model_dump()["results"]), media_type="application/xml")
        elif "text/markdown" in accept:
            return Response(content=MarkdownFormatter.format_batch(batch.model_dump()["results"]), media_type="text/markdown")
        else:
            return Response(content=JSONFormatter.format_batch(batch.model_dump()["results"]), media_type="application/json")