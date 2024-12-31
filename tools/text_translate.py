from collections.abc import Generator
from typing import Any

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class TextTranslateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Ensure runtime and credentials
        if not self.runtime or not self.runtime.credentials:
            raise Exception("Tool runtime or credentials are missing")

        region = self.runtime.credentials.get("azure_ai_transtator_region")
        text_endpoint = self.runtime.credentials.get("azure_ai_transtator_text_translation_endpoint")
        api_key = self.runtime.credentials.get("azure_ai_transtator_api_key")

        if not region:
            raise Exception("Azure region is required")
        if not text_endpoint:
            raise Exception("Azure text endpoint is required")
        if not api_key:
            raise Exception("Azure API key is required")

        # Get Input Parameters
        input_text: str = tool_parameters.get("input_text") or ""
        source_language: str = tool_parameters.get("source_language") or ""
        target_languages: str = tool_parameters.get("target_languages") or ""

        if not input_text:
            raise Exception("Input text is required")
        if not target_languages:
            raise Exception("Target language is required")

        # Initialize Azure AI Text Translator
        try:
            credential = AzureKeyCredential(api_key)
            text_translator = TextTranslationClient(endpoint=text_endpoint, credential=credential, region=region)
            supported_languages_response = text_translator.get_supported_languages()
            supported_languages: list[str] = supported_languages_response["translation"].keys() or []

            from_language = source_language if source_language else None
            to_languages = target_languages.replace(" ", "").replace("'", "").replace('"', "").split(",")

            # check supported languages
            if from_language and from_language not in supported_languages:
                raise Exception(f"Source language '{from_language}' is not supported")
            for lang in to_languages:
                if lang not in supported_languages:
                    raise Exception(f"Target language '{lang}' is not supported")

            response = text_translator.translate(
                body=[input_text], to_language=to_languages, from_language=from_language
            )
            translation = response[0] if response else None

            if translation:
                translation_texts = [item["text"] for item in translation["translations"]]
                translated_text = " ".join(translation_texts)

                yield self.create_text_message(translated_text)
                yield self.create_json_message(translation.as_dict())
            else:
                raise Exception("Failed to translate text")
        except Exception as e:
            raise Exception(f"Failed to initialize Azure AI Text Translator: {e}") from e