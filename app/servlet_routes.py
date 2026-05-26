"""
SE — Servlets (analogue): Flask blueprint routes act like Java servlets — one handler per HTTP endpoint.

This module exposes small JSON controllers separate from HTML page rendering.
"""

import logging

from flask import Blueprint, current_app, jsonify

from app.background_stats import get_cached_stats, schedule_stats_refresh
from app.exceptions import NetworkError, TasteMapError
from app.http_client import fetch_json
from app.socket_probe import tcp_reachable

servlet_bp = Blueprint("servlet", __name__, url_prefix="/api")
logger = logging.getLogger(__name__)


@servlet_bp.route("/health")
def health_servlet():
    """
    SE — HTTP + Sockets: servlet-style handler returning JSON over HTTP.
    """
    host = current_app.config.get("HEALTH_PROBE_HOST", "127.0.0.1")
    port = int(current_app.config.get("HEALTH_PROBE_PORT", 5000))
    socket_ok = False
    socket_error = None
    try:
        socket_ok = tcp_reachable(host, port, timeout=0.5)
    except NetworkError as exc:
        socket_error = str(exc)

    http_sample = None
    http_error = None
    try:
        # Public HTTP echo service (demonstrates outbound HTTP from the app).
        http_sample = fetch_json("https://httpbin.org/get", timeout=2.0)
        http_sample = {"url": http_sample.get("url"), "origin": http_sample.get("origin")}
    except (NetworkError, TasteMapError) as exc:
        http_error = str(exc)

    schedule_stats_refresh(current_app._get_current_object())
    stats = get_cached_stats()

    return jsonify(
        {
            "status": "ok",
            "socket_probe": {"host": host, "port": port, "ok": socket_ok, "error": socket_error},
            "http_probe": {"ok": http_error is None, "sample": http_sample, "error": http_error},
            "stats": stats,
        }
    )
