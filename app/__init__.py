import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.helpers import (
    SCORE_LABELS,
    resolve_image,
    restaurant_average_score,
    restaurant_fallback_image,
    review_score_average,
    stars_html,
)

db = SQLAlchemy()


def _migrate_schema(app):
    import sqlite3

    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    if not db_path or db_path == ":memory:" or not Path(db_path).exists():
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def add_column(table, column, col_type):
        cursor.execute(f"PRAGMA table_info({table})")
        cols = {row[1] for row in cursor.fetchall()}
        if column not in cols:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

    add_column("restaurants", "description", "TEXT")
    add_column("restaurants", "cover_image", "VARCHAR(500)")
    add_column("reviews", "photo", "VARCHAR(500)")
    conn.commit()
    conn.close()


def create_app(test_config=None):
    from app.logging_config import setup_logging

    setup_logging()

    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    (Path(app.root_path) / "static" / "uploads").mkdir(parents=True, exist_ok=True)

    if test_config:
        app.config.update(test_config)
    else:
        db_path = Path(app.instance_path) / "reviews.db"
        analytics_path = Path(app.instance_path) / "analytics.db"
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
            SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
            # SE — Multi-database (optional): secondary bind for analytics rows.
            SQLALCHEMY_BINDS={"analytics": f"sqlite:///{analytics_path}"},
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            MAX_CONTENT_LENGTH=5 * 1024 * 1024,
            HEALTH_PROBE_HOST="127.0.0.1",
            HEALTH_PROBE_PORT=5000,
        )

    if test_config and "SQLALCHEMY_BINDS" not in test_config:
        app.config["SQLALCHEMY_BINDS"] = {"analytics": "sqlite:///:memory:"}

    db.init_app(app)

    @app.template_filter("getattr")
    def jinja_getattr(obj, attr):
        return getattr(obj, attr)

    app.jinja_env.globals.update(
        resolve_image=resolve_image,
        restaurant_fallback_image=restaurant_fallback_image,
        restaurant_average_score=restaurant_average_score,
        review_score_average=review_score_average,
        stars_html=stars_html,
        SCORE_LABELS=SCORE_LABELS,
    )

    from app import models  # noqa: F401
    from app import secondary_db  # noqa: F401  # SE — Multi-database models
    from app.routes import bp
    from app.servlet_routes import servlet_bp  # SE — Servlet-style JSON routes

    app.register_blueprint(bp)
    app.register_blueprint(servlet_bp)

    from app.errors import register_error_handlers

    register_error_handlers(app)

    with app.app_context():
        db.create_all()
        if not test_config:
            _migrate_schema(app)

    return app
