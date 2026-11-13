"""Vercel ASGI entrypoint served at /api/extract."""

from backend.app import app

__all__ = ["app"]
