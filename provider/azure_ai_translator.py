from typing import Any

from azure.ai.translation.document import DocumentTranslationClient
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AzureAiTranslatorProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            region = credentials.get("azure_ai_transtator_region")
            text_endpoint = credentials.get("azure_ai_transtator_text_translation_endpoint")
            document_endpoint = credentials.get("azure_ai_transtator_document_translation_endpoint")
            api_key = credentials.get("azure_ai_transtator_api_key")

            if not region:
                raise Exception("Azure region is required")
            if not text_endpoint:
                raise Exception("Azure text endpoint is required")
            if not document_endpoint:
                raise Exception("Azure document endpoint is required")
            if not api_key:
                raise Exception("Azure API key is required")

            try:
                credential = AzureKeyCredential(api_key)
                text_translator = TextTranslationClient(endpoint=text_endpoint, credential=credential, region=region)
                _ = text_translator.get_supported_languages()
            except Exception as e:
                raise Exception("Failed to initialize Azure AI Text Translator") from e

            try:
                credential = AzureKeyCredential(api_key)
                document_translator = DocumentTranslationClient(endpoint=document_endpoint, credential=credential)
                _ = document_translator.get_supported_document_formats()
            except Exception as e:
                raise Exception("Failed to initialize Azure AI Document Translator") from e

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
