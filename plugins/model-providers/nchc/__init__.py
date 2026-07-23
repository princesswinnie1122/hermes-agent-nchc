"""NCHC GenAI Portal provider profile."""

from providers import register_provider
from providers.base import ProviderProfile

nchc = ProviderProfile(
    name="nchc",
    aliases=("nchc-portal", "genai-nchc"),
    display_name="NCHC GenAI Portal",
    description="NCHC GenAI Portal — Taiwan NCHC-hosted open models",
    signup_url="https://portal.genai.nchc.org.tw/",
    env_vars=("NCHC_API_KEY",),
    base_url="https://portal.genai.nchc.org.tw/api/v1",
    auth_type="api_key",
    default_aux_model="Devstral-Small-2507",
    fallback_models=(
        "Devstral-2-123B-Instruct-2512",
        "Devstral-Small-2507",
        "Llama-3.3-70B-Instruct",
        "Llama-4-Maverick-17B-128E-Instruct-FP8",
        "Mistral-Large-3-675B-Instruct-2512",
        "gpt-oss-120b",
        "NVIDIA-Nemotron-3-Super-120B-A12B",
        "Microsoft-Phi-4",
    ),
)

register_provider(nchc)
