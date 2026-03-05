# Security Policy

For the overall Ancroo security policy, roadmap, and Phase 1 limitations, see the [central security policy](https://github.com/Stefan-Schmidbauer/ancroo/blob/main/SECURITY.md).

## Client-Specific Notes

- Audio is recorded locally and sent directly to the configured Ancroo Backend endpoint. No audio data is stored on disk after transmission.
- Configuration files (`.env` / `ancroo-voice.ini`) may contain an API key (`ANCROO_BACKEND_API_KEY`). Protect these files with appropriate file permissions.
- SSL certificate verification can be disabled (`ANCROO_BACKEND_VERIFY_SSL=false`) for self-signed certificates. Only do this in trusted networks.

## Reporting a Vulnerability

Please report security vulnerabilities through [GitHub's private vulnerability reporting](https://github.com/Stefan-Schmidbauer/ancroo-voice/security/advisories/new).

Do not open a public issue for security vulnerabilities.
