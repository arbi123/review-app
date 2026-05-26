"""
SE — Sockets: low-level TCP connectivity (below HTTP), used for dependency checks.
"""

import socket

from app.exceptions import NetworkError


def tcp_reachable(host: str, port: int, timeout: float = 2.0) -> bool:
    """Return True when a TCP socket can be opened to host:port."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError as exc:
        raise NetworkError(f"Socket connect failed for {host}:{port} — {exc}") from exc
