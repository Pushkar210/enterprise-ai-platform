import os

import boto3

_ssm_client = boto3.client("ssm")
_cached_api_key = None


class Config:
    @staticmethod
    def get_gemini_api_key():
        global _cached_api_key

        if _cached_api_key:
            return _cached_api_key

        parameter_name = os.getenv(
            "GEMINI_API_KEY_PARAMETER",
            "/enterprise-ai-platform/gemini-api-key",
        )

        response = _ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True,
        )

        _cached_api_key = response["Parameter"]["Value"]
        return _cached_api_key

    @staticmethod
    def get_llm_provider():
        return os.getenv("LLM_PROVIDER", "gemini")