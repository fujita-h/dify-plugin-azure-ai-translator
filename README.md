![Icon](./_assets/00800-icon-service-Translator-Text.svg)

# Azure AI Translator

[![GitHub Repo](https://img.shields.io/badge/GitHub_Repo-fujita--h/dify--plugin--azure--ai--translator-blue?logo=github)](https://github.com/fujita-h/dify-plugin-azure-ai-translator)
![GitHub Release](https://img.shields.io/github/v/release/fujita-h/dify-plugin-azure-ai-translator)
![GitHub License](https://img.shields.io/github/license/fujita-h/dify-plugin-azure-ai-translator)


This extension provides a simple way to translate text using Azure AI Translator.

> [!IMPORTANT]  
> This plugin requires an Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Learn more about the free trial [here](https://azure.microsoft.com/free/).

## Tools provided by this plugin

Break language barriers with text translation.

### Text Translation

Text Translation provides a simple way to translate text between multiple languages. Returns single source-language text to multiple target-language texts with a single request.

https://learn.microsoft.com/azure/ai-services/translator/text-translation-overview

### Document Translation

Document Translation translates can translate complex documents in various formats while preserving the document's layout and structure. 

https://learn.microsoft.com/azure/ai-services/translator/document-translation/overview

> [!Note]
> This tool provides Syncronous Translation only.
> For more information, such as supported language and file formats, please see https://learn.microsoft.com/azure/ai-services/translator/document-translation/overview#synchronous-translation

## Notes

### Document Translation data residency

Text Translation and Document Translation data residency depends on the Azure region where your Translator resource was created. See below for more information.

https://learn.microsoft.com/azure/ai-services/translator/text-translation-overview#text-translation-data-residency

https://learn.microsoft.com/azure/ai-services/translator/document-translation/overview#document-translation-data-residency

## Contributing

This plugin is open-source and contributions are welcome. Please visit the GitHub repository to contribute.
