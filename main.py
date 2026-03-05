#!/usr/bin/env python3
"""
Ancroo Voice - Push-to-Talk Speech-to-Text

STT client for the Ancroo Stack. Connects to the Ancroo Backend for
centralized speech-to-text transcription.

Simple GUI for selecting microphone, language, and hotkey.
Press and hold your configured hotkey (default: Ctrl+Space) to record audio.
Release to transcribe and insert text into the active application.

Features:
- Configurable hotkey (e.g., Ctrl+Space, Alt+R, Ctrl+Shift+V)
- Backend-managed STT model and server selection
- Automatic terminal detection for better paste support
- Settings persistence

Copyright (c) Stefan Schmidbauer
License: MIT License
GitHub: https://github.com/Stefan-Schmidbauer/ancroo-voice
"""

import os
import sys
import customtkinter as ctk

from dotenv import load_dotenv

from ancroo_voice.gui.main_window import AncrooVoiceGUI


def load_config_file():
    """Load configuration from .env or ancroo-voice.ini (Windows-friendly).

    Search order:
    1. .env (standard, Linux default)
    2. ancroo-voice.ini (Windows-friendly alternative)

    Returns the path of the loaded config file, or None if not found.
    """
    # Get the directory where the executable/script is located
    if getattr(sys, 'frozen', False):
        # Check if running as AppImage (Linux)
        appimage_path = os.environ.get('APPIMAGE')
        if appimage_path:
            # AppImage: use directory containing the .AppImage file
            base_dir = os.path.dirname(appimage_path)
        else:
            # Regular PyInstaller: use directory of the executable
            base_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    config_files = ['.env', 'ancroo-voice.ini']

    for config_file in config_files:
        config_path = os.path.join(base_dir, config_file)
        if os.path.exists(config_path):
            load_dotenv(config_path)
            return config_path

    # Fallback: try default load_dotenv behavior (searches parent dirs)
    load_dotenv()
    return None


def build_env_config():
    """Build environment config dict from loaded environment variables.

    Collects Ancroo Backend configuration from environment variables
    and returns them in a format compatible with the provider.

    Returns:
        dict: Environment config with lowercase keys matching provider config prefixes
    """
    env_config = {}

    for key in ('ANCROO_BACKEND_ENDPOINT', 'ANCROO_BACKEND_API_KEY', 'ANCROO_BACKEND_VERIFY_SSL'):
        value = os.environ.get(key)
        if value:
            env_config[key.lower()] = value

    return env_config


# Load environment variables from config file
load_config_file()


def main():
    """Main entry point"""
    # Build environment config from loaded .env / ancroo-voice.ini
    env_config = build_env_config()

    # Start GUI
    root = ctk.CTk()
    app = AncrooVoiceGUI(root, env_config=env_config)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully (same as clicking Quit)
        app.on_closing()
        sys.exit(0)


if __name__ == "__main__":
    main()
