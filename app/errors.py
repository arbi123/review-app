import logging

from flask import render_template
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def error_response(
    code: int, headline: str, message: str, icon: str, detail: str | None = None
):
    return (
        render_template(
            "errors/error_page.html",
            code=code,
            headline=headline,
            message=message,
            icon=icon,
            detail=detail,
        ),
        code,
    )


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        logger.info("404 Not Found: %s", error)
        return error_response(
            404,
            "Page not found",
            "We could not find that page. It may have moved or the link might be wrong.",
            "🍽️",
        )

    @app.errorhandler(500)
    def internal_error(error):
        logger.exception("500 Internal Server Error: %s", error)
        return error_response(
            500,
            "Something went wrong",
            "The server ran into a problem. Please try again in a moment.",
            "⚠️",
            detail="Our team has been notified (demo — button not wired).",
        )

    @app.errorhandler(HTTPException)
    def http_exception(error: HTTPException):
        if error.code == 404:
            return not_found(error)
        if error.code and error.code >= 500:
            return internal_error(error)
        logger.warning("HTTP %s: %s", error.code, error.description)
        return error_response(
            error.code or 500,
            error.name.replace("_", " ").title(),
            error.description or "An error occurred while handling your request.",
            "❗",
        )
