import io
from collections.abc import Generator
from typing import Any

from azure.ai.translation.document import SingleDocumentTranslationClient
from azure.ai.translation.document.models import DocumentTranslateContent
from azure.core.credentials import AzureKeyCredential
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class DocumentTranslationTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Ensure runtime and credentials
        if not self.runtime or not self.runtime.credentials:
            raise Exception("Tool runtime or credentials are missing")

        region = self.runtime.credentials.get("azure_ai_transtator_region")
        document_endpoint = self.runtime.credentials.get("azure_ai_transtator_document_translation_endpoint")
        api_key = self.runtime.credentials.get("azure_ai_transtator_api_key")

        if not region:
            raise Exception("Azure region is required")
        if not document_endpoint:
            raise Exception("Azure document endpoint is required")
        if not api_key:
            raise Exception("Azure API key is required")

        # Get Input Parameters
        input_document_file = tool_parameters.get("input_document_file")
        source_language: str = tool_parameters.get("source_language") or ""
        target_language: str = tool_parameters.get("target_language") or ""

        if not input_document_file:
            raise ValueError("Document file is required")
        if not target_language:
            raise Exception("Target language is required")

        try:
            # file contents
            file_name = input_document_file.filename
            file_contents = io.BytesIO(input_document_file.blob)
            file_type = input_document_file.mime_type

            # Initialize Azure AI Document Translator
            credential = AzureKeyCredential(api_key)
            client = SingleDocumentTranslationClient(endpoint=document_endpoint, credential=credential)
            document_translate_content = DocumentTranslateContent(
                document=(file_name, file_contents.getvalue(), file_type)
            )

            # Translate document
            response_stream = client.translate(
                body=document_translate_content,
                target_language=target_language,
                source_language=source_language if source_language else None,
            )
            translated_response = response_stream.decode("utf-8-sig")  # type: ignore

            if translated_response:
                yield self.create_text_message(translated_response)
            else:
                raise Exception("Failed to translate document")
        except Exception as e:
            raise Exception(f"Failed to initialize Azure AI Document Translator: {e}") from e
