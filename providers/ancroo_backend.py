"""
Ancroo Backend Provider

Sends audio to the Ancroo Backend's centralized /api/v1/transcribe endpoint.
Model and STT server selection is handled entirely by the backend.
"""

import os
import requests
from typing import Optional


class AncrooBackendProvider:
    """Ancroo Backend provider — centralized STT via backend proxy"""

    def __init__(self, endpoint: Optional[str] = None, api_key: Optional[str] = None,
                 verify_ssl: Optional[bool] = None, **kwargs):
        """
        Initialize Ancroo Backend provider.

        Args:
            endpoint: Backend transcribe URL (defaults to ANCROO_BACKEND_ENDPOINT env var)
            api_key: Optional API key for authentication (defaults to ANCROO_BACKEND_API_KEY env var)
            verify_ssl: Whether to verify SSL certificates (defaults to ANCROO_BACKEND_VERIFY_SSL env var, True if not set)
            **kwargs: Ignored (allows generic config forwarding)
        """
        self.endpoint = endpoint or os.getenv(
            "ANCROO_BACKEND_ENDPOINT",
            "http://localhost:8900/api/v1/transcribe"
        )
        self.api_key = api_key or os.getenv("ANCROO_BACKEND_API_KEY")

        # SSL verification - defaults to True unless explicitly disabled
        if verify_ssl is not None:
            self.verify_ssl = verify_ssl
        else:
            env_verify = os.getenv("ANCROO_BACKEND_VERIFY_SSL", "true").lower()
            self.verify_ssl = env_verify not in ("false", "0", "no")

    @property
    def name(self) -> str:
        return "Ancroo Backend"

    def validate_config(self) -> None:
        """Validate Ancroo Backend configuration."""
        if not self.endpoint:
            raise ValueError("ANCROO_BACKEND_ENDPOINT not set")

        # Health check against backend's /health endpoint
        try:
            # Derive health URL from transcribe endpoint
            base_url = self.endpoint.split("/api/")[0]
            health_url = f"{base_url}/health"
            response = requests.get(health_url, timeout=5, verify=self.verify_ssl)
            if response.status_code != 200:
                raise ValueError(f"Backend health check failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise ValueError(f"Cannot connect to Ancroo Backend at {self.endpoint}")
        except requests.exceptions.Timeout:
            raise ValueError(f"Backend timeout at {self.endpoint}")

    def transcribe(self, audio_bytes: bytes, language: Optional[str] = None) -> Optional[str]:
        """
        Transcribe audio via the Ancroo Backend.

        Args:
            audio_bytes: WAV format audio data
            language: ISO language code ('de', 'en') or None for auto-detect

        Returns:
            Transcribed text or None on error
        """
        try:
            files = {
                'file': ('audio.wav', audio_bytes, 'audio/wav')
            }
            data = {}
            if language:
                data['language'] = language

            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            response = requests.post(
                self.endpoint,
                files=files,
                data=data,
                headers=headers,
                timeout=300,
                verify=self.verify_ssl
            )

            if response.status_code == 200:
                result = response.json()
                transcript = result.get('text', '').strip()
                return transcript if transcript else None
            elif response.status_code in (401, 403):
                raise ValueError(f"Authentication failed ({response.status_code})")
            elif response.status_code == 503:
                raise RuntimeError("No STT provider configured on the backend")
            else:
                raise RuntimeError(f"Backend error ({response.status_code})")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error: {e}")
