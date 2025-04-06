"""
Onboarding module backend.
Provides endpoints for application initialization and WaniKani data import.
"""

from .router import create_router
from .dependencies import SettingsStore

__all__ = ['create_router', 'SettingsStore']
